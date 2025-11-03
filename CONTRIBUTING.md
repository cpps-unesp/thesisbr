# 🧭 Política de Contribuição

Este repositório segue uma política de **colaboração baseada em Pull Requests (PRs)** para manter a qualidade e a rastreabilidade do código.

## 🔒 Proteção da branch `main`

A branch `main` é protegida — **não são permitidos commits ou push diretos**. Todas as alterações devem passar pelo fluxo de revisão via Pull Request.

## 🚀 Como contribuir

1. Crie uma nova branch a partir da `main`. No comando abaixo subtitua `nome-da-sua-branch` pelo nome da branch que você criará (coloque um nome relacionado ao que você está fazendo):

   ```
   git checkout main
   git pull origin main
   git checkout -b nome-da-sua-branch
   ```

2. Faça suas alterações e commit:

   ```
   git add .
   git commit -m "Descrição clara da alteração"
   ```

3. Envie sua branch:
   ```
   git push origin nome-da-sua-branch
   ```

4. Abra um **Pull Request (PR)** no GitHub, descrevendo:
   - O que foi alterado
   - Por que a alteração é necessária

5. Aguarde a **revisão e aprovação** antes do merge.

## ✅ Boas práticas

- Prefira PRs pequenos e específicos.  
- Use mensagens de commit descritivas.  
- Atualize sua branch com a `main` antes de pedir o merge:
  
  ```
  git fetch origin main
  git rebase origin/main
  ```
