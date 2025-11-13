# ThesisBR – Brazilian Theses & Dissertations

O **ThesisBR** é uma iniciativa de ciência aberta que visa facilitar o **acesso e utilização de dados de teses e dissertações brasileiras**, com base no **Catálogo de Teses e Dissertações da CAPES**. O projeto busca combinar ferramentas de **coleta automatizada**, estruturação documental e enriquecimento semântico.

---

## 🎯 Objetivos e Status Atual

Legenda de status:
* 🟢 **Concluído:** Funcionalidade estável e disponível.
* 🟡 **Em Andamento:** Em desenvolvimento ativo ou fase de testes.
* 🔴 **Planejado:** No roadmap, mas ainda não iniciado.

### Roadmap de Funcionalidades

🔴 **Coleta de Dados**
* Extração robusta de metadados (título, autor, ano, etc.) do Catálogo CAPES.
* Download em lote dos PDFs de teses e dissertações.

🔴 **Tratamento e Estruturação**
* Extração de texto completo dos PDFs.
* Limpeza, normalização de campos (datas, nomes) e checagem de integridade (duplicatas, nulos).
* Geração de dicionário de dados e relatórios de qualidade.

🔴 **Disponibilização e Acesso**
* Disponibilização dos dados tratados (ex: Parquet, SQLite).
* Notebooks (Jupyter/Colab) com exemplos de análise exploratória.
* App Web (Streamlit/Dash) com dashboards e busca SQL customizada.

🔴 **Enriquecimento Semântico (LLM)**
* Geração de resumos automáticos (quando aplicável).
* Classificação temática avançada.
* Implementação de um chatbot experimental (Q&A via RAG) para consultar o *conteúdo* das teses.

🔴 **Disseminação e Reuso**
* Empacotamento das funções de coleta e tratamento no pacote PyPI `thesisbr`.
* Documentação técnica completa e tutoriais.

---

## Índice (Opcional)
* [Como usar o projeto](#como-usar-o-projeto)
* [Autores](#autores)
* [Licença](#licença)
* [Como contribuir](#como-contribuir-para-o-projeto)
* [Testes](#testes)


## Como usar o projeto
Forneça instruções e exemplos para que os usuários/colaboradores possam usar o projeto. 

### Instalação

Para acessar o site é necessário rodar o código abaixo no seu terminal...


## Autores
- [@octokatherine](https://www.github.com/octokatherine)


## Licença

[MIT](https://choosealicense.com/licenses/mit/)


## Insígnias
(Aqui você pode colocar insígnias de status da build, cobertura de testes, versão do PyPI, etc.)


## Como contribuir para o projeto
Isso será especialmente útil se você estiver desenvolvendo um projeto de código aberto...


## Testes

Escreva testes para sua aplicação...

## Observações 
(Seu texto sobre idioma)