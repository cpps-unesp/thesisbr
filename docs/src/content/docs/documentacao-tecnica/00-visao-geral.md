---
title: Visão Geral e Objetivos
---

O **ThesisBR** é uma iniciativa de ciência aberta que visa facilitar o **acesso e utilização de dados de teses e dissertações brasileiras**, com base no **Catálogo de Teses e Dissertações da CAPES**. O projeto busca combinar ferramentas de **coleta automatizada**, estruturação documental e enriquecimento semântico.

Abaixo estão os objetivos detalhados do projeto.

---

## 1. Coleta de Dados
Coletar dados do Catálogo de Teses e Dissertações da CAPES, incluindo:
* Metadados (título, autor, instituição, orientador, área, ano, etc.);
* Dados completos (PDFs das teses e dissertações);
* Extração e estruturação de conteúdo dos PDFs.

## 2. Tratamento e Normalização
* Padronizar colunas e campos (nomes, tipos, domínios e formatos de data).
* Implementar verificações de integridade (duplicatas, valores ausentes, coerência entre campos).
* Gerar relatórios de qualidade dos dados e dicionários de variáveis.

## 3. Disponibilizar Acesso e Análises
Disponibilizar acesso aos dados e análises por meio de:
* Notebooks interativos (Jupyter/Colab);
* Um aplicativo web com dashboards de visualização e busca SQL personalizada;
* Um chatbot experimental capaz de responder a perguntas sobre os dados e os textos das teses.

## 4. Enriquecimento Semântico e Análise Textual
Utilizar modelos de linguagem (LLMs) de código aberto para tarefas de alto nível, como:
* Geração de resumos automáticos das teses (quando permitido);
* Classificação temática;
* Criação de um chatbot de perguntas e respostas (Q&A) baseado em retrieval-augmented generation (RAG), permitindo consultas sobre o conteúdo das teses.

## 5. Facilitar a Utilização dos Dados
* Desenvolver notebooks Jupyter/Colab com exemplos reprodutíveis de exploração dos dados.
* Criação de um aplicativo com:
    * Dashboards prontos de visualização
    * Buscas customizadas/avançadas
    * Chatbot de perguntas e respostas (Q&A) baseado em retrieval-augmented generation (RAG), permitindo consultas sobre o conteúdo das teses.

## 6. Disseminação e Reuso (Pacote PyPI)
* Empacotar as principais funções em um pacote Python (thesisbr), disponibilizado via PyPI.
* Documentação completa, incluindo tutoriais e exemplos.