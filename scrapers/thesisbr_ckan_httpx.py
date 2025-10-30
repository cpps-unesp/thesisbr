#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
thesisbr_ckan_httpx.py — CKAN helpers using only httpx (no requests / urllib.parse)

This single script implements three utilities against a CKAN instance (e.g., CAPES):

1) download-dataset-xlsx
   Download all .xlsx resources from a dataset (by UUID or slug).

2) list-dataset-xlsx
   List (without downloading) all .xlsx resources from a dataset.

3) list-group
   List all datasets inside a CKAN "group" and each dataset's resources.
   Optional --format filter (e.g., --format xlsx) and optional CSV export.

Why httpx?
- Modern async-capable client, HTTP/2 support, robust streaming, fine-grained timeouts.
- Replaces both "requests" and "urllib.parse" in this codebase.

--------------------------------------------------------------------------
Usage examples:

# 1) List XLSX files of a dataset
python thesisbr_ckan_httpx.py list-dataset-xlsx \
  --base https://dadosabertos.capes.gov.br \
  --dataset 36d1c92c-f9e0-4da1-a4f0-633e6ebefe03

# 2) Download all XLSX files of a dataset
python thesisbr_ckan_httpx.py download-dataset-xlsx \
  --base https://dadosabertos.capes.gov.br \
  --dataset 36d1c92c-f9e0-4da1-a4f0-633e6ebefe03 \
  --out ./downloads

# 3) List a CKAN group (optionally filter by format and export CSV)
python thesisbr_ckan_httpx.py list-group \
  --base https://dadosabertos.capes.gov.br \
  --group catalogo-de-teses-e-dissertacoes-brasil \
  --format xlsx \
  --csv ckan_group_catalogo-de-teses-e-dissertacoes-brasil_xlsx.csv

Environment defaults (overridable by flags):
- CKAN_BASE (default: https://dadosabertos.capes.gov.br)
- CKAN_DATASET_ID
- CKAN_GROUP_ID
- TIMEOUT (seconds, default: 120)
- RETRY (default: 3)
- SLEEP_BETWEEN (seconds, default: 2.0)
--------------------------------------------------------------------------
"""

from __future__ import annotations

import os
import re
import sys
import csv
import time
import json
import math
import shutil
import typing as t
import pathlib
import argparse

import httpx

# =====================
# Defaults / settings
# =====================
DEFAULT_BASE = os.getenv("CKAN_BASE", "https://dadosabertos.capes.gov.br").rstrip("/")
DEFAULT_DATASET = os.getenv("CKAN_DATASET_ID", "36d1c92c-f9e0-4da1-a4f0-633e6ebefe03")
DEFAULT_GROUP = os.getenv("CKAN_GROUP_ID", "catalogo-de-teses-e-dissertacoes-brasil")

TIMEOUT_S = float(os.getenv("TIMEOUT", "120"))
RETRY = int(os.getenv("RETRY", "3"))
SLEEP_BETWEEN = float(os.getenv("SLEEP_BETWEEN", "2.0"))

# ===========================================
# Small helpers to avoid urllib.parse usage
# ===========================================
_pct_pat = re.compile(r"%([0-9A-Fa-f]{2})")

def pct_decode(s: str) -> str:
    """Minimal percent-decoder for filename tokens (RFC 3986-ish).
    We only decode %HH sequences into bytes then UTF-8-decode, ignoring errors.
    """
    if not s or "%" not in s:
        return s
    # Convert to bytes using a bytearray
    out = bytearray()
    i = 0
    b = s.encode("utf-8", "ignore")  # raw bytes of string (best effort)
    # We decode pattern on the string level to keep it simple:
    # replace %HH by its byte value; otherwise keep the original byte.
    while i < len(s):
        ch = s[i]
        if ch == "%" and i + 2 < len(s):
            hexpart = s[i+1:i+3]
            try:
                out.append(int(hexpart, 16))
                i += 3
                continue
            except ValueError:
                pass
        # default: append original char bytes
        out.extend(s[i].encode("utf-8", "ignore"))
        i += 1
    return out.decode("utf-8", "replace")


def sanitize_filename(name: str) -> str:
    """Restrict filename to safe characters for most filesystems."""
    name = re.sub(r"[\\/:*?\"<>|\r\n\t]+", "_", name.strip())
    # collapse spaces/underscores
    name = re.sub(r"\s+", " ", name).strip()
    name = name.replace(" ", "_")
    return name or "arquivo"


def ensure_suffix(path: pathlib.Path, suffix: str) -> pathlib.Path:
    return path if str(path).lower().endswith(suffix.lower()) else path.with_name(path.name + suffix)


# =====================
# HTTP client factory
# =====================
def make_client(timeout_s: float = TIMEOUT_S) -> httpx.Client:
    # Conservative pool; enable HTTP/2 if available
    limits = httpx.Limits(max_connections=10, max_keepalive_connections=5)
    return httpx.Client(timeout=timeout_s, limits=limits, http2=True, follow_redirects=True)


# =====================
# CKAN API helpers
# =====================
def ckan_call(base: str, action: str, params: dict) -> dict:
    url = f"{base}/api/3/action/{action}"
    with make_client() as client:
        r = client.get(url, params=params)
        r.raise_for_status()
        data = r.json()
    if not data.get("success"):
        raise RuntimeError(f"CKAN {action} falhou: {data}")
    return data["result"]


def ckan_package_show(base: str, dataset_id_or_slug: str) -> dict:
    return ckan_call(base, "package_show", {"id": dataset_id_or_slug})


def ckan_group_show(base: str, group_id_or_name: str, include_datasets: bool = True) -> dict:
    return ckan_call(base, "group_show", {"id": group_id_or_name, "include_datasets": include_datasets})


# =====================
# Resource filters
# =====================
def is_xlsx_resource(res: dict) -> bool:
    fmt = (res.get("format") or "").strip().lower()
    url = (res.get("url") or res.get("download_url") or "").strip().lower()
    return fmt == "xlsx" or url.endswith(".xlsx")


def res_pretty_name(res: dict) -> str:
    return res.get("name") or res.get("description") or res.get("id") or "arquivo"


def res_url(res: dict) -> str:
    return res.get("url") or res.get("download_url") or ""


# ====================================
# Filename guessing (no urllib.parse)
# ====================================
_cd_fname_re = re.compile(r'filename\*?=(?:UTF-8\'\')?"?([^";]+)"?', re.IGNORECASE)

def guess_filename(resp: httpx.Response, fallback_url: str, name_hint: str | None) -> str:
    # 1) Content-Disposition
    cd = resp.headers.get("content-disposition", "")
    m = _cd_fname_re.search(cd)
    if m:
        return sanitize_filename(pct_decode(m.group(1)))

    # 2) Final URL path
    try:
        parsed = httpx.URL(str(resp.url) if resp.url else fallback_url)
        path = parsed.path or ""
        if path:
            fn = pathlib.Path(path).name
            if fn:
                return sanitize_filename(pct_decode(fn))
    except Exception:
        pass

    # 3) Fallback to name_hint
    if name_hint:
        fn = sanitize_filename(name_hint)
        if not fn.lower().endswith(".xlsx"):
            fn += ".xlsx"
        return fn

    return "arquivo.xlsx"


# =====================
# Download helpers
# =====================
def download_stream(url: str, dest_dir: pathlib.Path, name_hint: str | None = None,
                    timeout_s: float = TIMEOUT_S) -> pathlib.Path:
    """Stream a file to disk with progress. Retries are handled by caller."""
    dest_dir.mkdir(parents=True, exist_ok=True)
    with httpx.stream("GET", url, timeout=timeout_s, follow_redirects=True) as r:
        r.raise_for_status()
        filename = guess_filename(r, url, name_hint)
        out_path = dest_dir / filename
        tmp_path = out_path.with_suffix(out_path.suffix + ".part")
        total = int(r.headers.get("content-length") or 0)
        downloaded = 0
        t0 = time.time()
        with open(tmp_path, "wb") as f:
            for chunk in r.iter_bytes(chunk_size=1024 * 1024):
                f.write(chunk)
                downloaded += len(chunk)
                if total:
                    pct = (downloaded / total) * 100
                    # Simple progress line (overwritable)
                    sys.stdout.write(f"\rBaixando {filename}: {pct:6.2f}%")
                    sys.stdout.flush()
        tmp_path.replace(out_path)
        if total:
            sys.stdout.write("\n")
        dt = max(1e-6, time.time() - t0)
        rate = downloaded / dt / (1024 * 1024)
        print(f"✓ Salvo: {out_path}  ({downloaded/1_048_576:.2f} MiB em {dt:.1f}s, {rate:.2f} MiB/s)")
        return out_path


def download_with_retry(url: str, dest_dir: pathlib.Path, name_hint: str | None = None,
                        retry: int = RETRY, sleep_between: float = SLEEP_BETWEEN,
                        timeout_s: float = TIMEOUT_S) -> pathlib.Path:
    last_err: Exception | None = None
    for attempt in range(1, retry + 1):
        try:
            return download_stream(url, dest_dir, name_hint=name_hint, timeout_s=timeout_s)
        except Exception as e:
            last_err = e
            print(f"\n[tentativa {attempt}/{retry}] Erro ao baixar {url}: {e}")
            if attempt < retry:
                time.sleep(sleep_between)
    assert last_err is not None
    raise last_err


# =====================
# CLI actions
# =====================
def action_list_dataset_xlsx(args: argparse.Namespace) -> int:
    base = args.base.rstrip("/")
    dataset = args.dataset
    result = ckan_package_show(base, dataset)
    resources = result.get("resources", [])
    xlsx = [r for r in resources if is_xlsx_resource(r)]

    if not xlsx:
        fmts = sorted(set((r.get("format") or "").upper() for r in resources))
        print("Nenhum XLSX encontrado. Formats disponíveis:", ", ".join(fmts) or "(nenhum)")
        return 0

    print(f"Arquivos XLSX encontrados para dataset {dataset}:\n")
    for r in xlsx:
        print(f"- {res_pretty_name(r)}")
        print(f"  {res_url(r)}\n")
    return 0


def action_download_dataset_xlsx(args: argparse.Namespace) -> int:
    base = args.base.rstrip("/")
    dataset = args.dataset
    out_dir = pathlib.Path(args.out).resolve()

    print(f"Consultando package_show para dataset: {dataset}")
    result = ckan_package_show(base, dataset)
    resources = result.get("resources", [])
    xlsx = [r for r in resources if is_xlsx_resource(r)]

    if not xlsx:
        fmts = sorted(set((r.get("format") or "").upper() for r in resources))
        print("Nenhum XLSX encontrado. Formats disponíveis:", ", ".join(fmts) or "(nenhum)")
        return 0

    out_dir.mkdir(parents=True, exist_ok=True)
    print(f"Foram encontrados {len(xlsx)} resources XLSX. Pasta de saída: {out_dir}")

    for i, r in enumerate(xlsx, 1):
        url = res_url(r)
        name = res_pretty_name(r) or f"arquivo_{i}.xlsx"
        if not url:
            print(f"[{i}] Resource sem URL, pulando: {r.get('id')}")
            continue

        print(f"\n[{i}/{len(xlsx)}] {name}")
        print(f"URL: {url}")
        try:
            download_with_retry(url, out_dir, name_hint=name, retry=args.retry, sleep_between=args.sleep)
        except Exception as e:
            print(f"Falhou: {e}")
    print("\nConcluído.")
    return 0


def action_list_group(args: argparse.Namespace) -> int:
    base = args.base.rstrip("/")
    group = args.group
    fmt_filter = (args.format or "").strip().lower()
    csv_out: str | None = args.csv

    res = ckan_group_show(base, group, include_datasets=True)
    packages = res.get("packages") or res.get("datasets") or []

    if not packages:
        print("Nenhum dataset encontrado no group.")
        return 0

    rows: list[dict] = []
    for i, pkg in enumerate(packages, start=1):
        ds_title = pkg.get("title") or pkg.get("name") or pkg.get("id")
        ds_name  = pkg.get("name") or pkg.get("id")
        ds_id    = pkg.get("id")
        print(f"\n[{i}/{len(packages)}] Dataset: {ds_title} ({ds_name})")

        try:
            ds = ckan_package_show(base, ds_id or ds_name)
            resources = ds.get("resources", [])
        except Exception as e:
            print(f"  ! Falha ao obter resources: {e}")
            continue

        if not resources:
            print("  (sem resources)")
            continue

        for r in resources:
            fmt = (r.get("format") or "").strip()
            url = res_url(r)
            rname = res_pretty_name(r)
            # Optional format filter
            if fmt_filter and fmt.lower() != fmt_filter and not url.lower().endswith(f".{fmt_filter}"):
                continue

            print(f"  - {rname}  |  format={fmt}  |  url={url}")
            rows.append({
                "dataset_title": ds_title,
                "dataset_name": ds_name,
                "dataset_id": ds_id,
                "resource_name": rname,
                "resource_format": fmt,
                "resource_url": url,
                "resource_id": r.get("id"),
            })

    if csv_out and rows:
        # Write a simple CSV without pandas dependency
        fieldnames = [
            "dataset_title", "dataset_name", "dataset_id",
            "resource_name", "resource_format", "resource_url", "resource_id"
        ]
        with open(csv_out, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=fieldnames)
            w.writeheader()
            for row in rows:
                w.writerow(row)
        print(f"\n✓ Exportado CSV: {csv_out}")
    elif csv_out and not rows:
        print("\nNada para exportar; verifique o filtro --format.")
    return 0


# =====================
# Main / argparse
# =====================
def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="thesisbr_ckan_httpx",
        description="CKAN utilities using httpx only (dataset/group listing and XLSX downloads).",
    )
    p.add_argument("--base", default=DEFAULT_BASE, help=f"CKAN base URL (default: {DEFAULT_BASE})")
    p.add_argument("--timeout", type=float, default=TIMEOUT_S, help=f"Timeout em segundos (default: {TIMEOUT_S})")
    sub = p.add_subparsers(dest="cmd", required=True)

    # list-dataset-xlsx
    sp1 = sub.add_parser("list-dataset-xlsx", help="Listar .xlsx de um dataset")
    sp1.add_argument("--dataset", default=DEFAULT_DATASET, help=f"Dataset UUID ou slug (default: {DEFAULT_DATASET})")
    sp1.set_defaults(func=action_list_dataset_xlsx)

    # download-dataset-xlsx
    sp2 = sub.add_parser("download-dataset-xlsx", help="Baixar .xlsx de um dataset")
    sp2.add_argument("--dataset", default=DEFAULT_DATASET, help=f"Dataset UUID ou slug (default: {DEFAULT_DATASET})")
    sp2.add_argument("--out", default="downloads", help="Diretório de saída (default: ./downloads)")
    sp2.add_argument("--retry", type=int, default=RETRY, help=f"Número de tentativas (default: {RETRY})")
    sp2.add_argument("--sleep", type=float, default=SLEEP_BETWEEN, help=f"Intervalo entre tentativas (default: {SLEEP_BETWEEN}s)")
    sp2.set_defaults(func=action_download_dataset_xlsx)

    # list-group
    sp3 = sub.add_parser("list-group", help="Listar datasets e resources de um group CKAN")
    sp3.add_argument("--group", default=DEFAULT_GROUP, help=f"Group ID/slug (default: {DEFAULT_GROUP})")
    sp3.add_argument("--format", default="", help="Filtrar por formato (ex.: xlsx)")
    sp3.add_argument("--csv", default="", help="Exportar CSV para este caminho")
    sp3.set_defaults(func=action_list_group)

    return p


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    # Apply timeout globally by monkey-patching TIMEOUT_S used by helpers
    global TIMEOUT_S
    TIMEOUT_S = float(args.timeout)

    try:
        return args.func(args)
    except KeyboardInterrupt:
        print("\nInterrompido pelo usuário.")
        return 130
    except httpx.HTTPError as e:
        print(f"Erro HTTP: {e}")
        return 2
    except Exception as e:
        print(f"Erro: {e}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())