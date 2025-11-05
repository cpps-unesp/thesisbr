

#  Título do Projeto

Este é o nome do projeto. Ele descreve todo o projeto em uma frase e ajuda as pessoas a entenderem qual é o objetivo principal e a finalidade do projeto.

# Descrição do Projeto
Uma descrição bem elaborada permite que você mostre seu trabalho a outros desenvolvedores e também a potenciais empregadores.



## Índice (Opcional)
Se o seu arquivo README for muito extenso, talvez seja interessante adicionar um sumário para facilitar a navegação dos usuários entre as diferentes seções. Isso tornará a leitura do projeto mais fácil e intuitiva.

## Instalação

Para acessar o site é necessário rodar o código abaixo no seu terminal, sua função é justamente para que o site funcione: 

``` bash
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/master/install.sh | bash
source ~/.bashrc
nvm install --lts
``` 

Pra utilizar o Projeto deve ser inserido no terminal este código que permitirá acesso, abrirá o site: 
```bash
cd docs && npm i && npm run dev
```

Incluir as etapas necessárias para instalar o projeto e também as dependências necessárias, se houver.
Forneça uma descrição passo a passo de como configurar e executar o ambiente de desenvolvimento.

Instale my-project com npm

```bash
  npm install my-project
  cd my-project
```
    
## Como usar o projeto
Forneça instruções e exemplos para que os usuários/colaboradores possam usar o projeto. 
## Autores
Inclua também links para seus perfis no GitHub e redes sociais.
- [@octokatherine](https://www.github.com/octokatherine)


## Licença

[MIT](https://choosealicense.com/licenses/mit/)


## Insígnias
Os distintivos não são necessários, mas usá-los é uma maneira simples de mostrar a outros desenvolvedores que você sabe o que está fazendo.

## Como contribuir para o projeto
Isso será especialmente útil se você estiver desenvolvendo um projeto de código aberto que precisará da contribuição de outros desenvolvedores. Você precisará adicionar diretrizes para que eles saibam como podem contribuir para o seu projeto.

## Testes

Escreva testes para sua aplicação. Em seguida, forneça exemplos de código e instruções sobre como executá-los.
## Pontos extras

:mag_right:
## observações 

Caso haja alterações, certifique-se de atualizar o arquivo quando necessário.
escolha um idioma — Todos nós viemos de regiões diferentes e falamos idiomas diferentes. Mas isso não significa que você precise traduzir seu código para o seu idioma nativo. Escrever seu README em inglês funcionará, já que o inglês é um idioma globalmente aceito.
Você pode usar uma ferramenta de tradução se o seu público-alvo não estiver familiarizado com o inglês.







###################################################################################################################


# ThesisBR – Brazilian Theses & Dissertations

O ThesisBr visa facilitar a utilização do [Catálogo de Teses e Dissertações da Capes](https://dadosabertos.capes.gov.br/group/catalogo-de-teses-e-dissertacoes-brasil)


## Instalação

De preferência para instalar o repositório via SSH. Para instruções de como configurar o ssh [clique aqui](https://labriunesp.org/docs/projetos/ensino/trilha-dados/ambiente/versionamento/chave-ssh)


#### Via SSH

```
git clone git@github.com:cpps-unesp/thesisbr.git

```

#### Clone com HTTPS

```
git clone https://github.com/cpps-unesp/thesisbr.git

```

## Versionamento

Abaixo são as nistruções para a realização do versiamentos de suas contribuições

### ETAPA 01: Gravando mudanças

Utilize o seguinte comando para gravar modificações feitas no código:

``` git add . && git commit -m 'inserir mensagem' ```

**Onde:**

`git add .` adiciona as últimas mudanças nos conteúdos do diretório atual (referida como `.`) à lista de mudanças a serem gravadas no repositório. Deve ser efetuado sempre que novas mudanças são feitas.

`&&` encadeia comandos para que sejam executados sequencialmente.

`git commit` "comete" as mudanças feitas nos arquivos monitorados, gravando-as no repositório.

`-m 'mensagem'` especifica mensagem que descreva as mudanças. A descrição deve estar entre aspas simples ou duplas.


### ETAPA 02: Sincronizando o repositório

Ao usar os comandos acima, as mudanças são salvas (gravadas) apenas na sua máquina local.

É necessário sincronizar o repositório local com o repositório remoto, o que é feito através dos seguinte comando:

```git pull origin main && git push origin main```

**Onde:**

`git pull origin main` sincroniza todos os commits mais recentes do repositório remoto e os integra no repositório local.

`git push origin main` envia as alterações do repositório local para o repositório remoto 

 o `origin main` são argumentos para especificar que a origem dos commits a serem integrados é o ramo `main` do repositório remoto. Estes argumentos não são mandatório, no entanto, explicitá-los garante que não hajam conflitos.

 - É importante que qualquer mudança no repositório seja salva/gravada (ver etapa 01) antes da sincronização com o repositório remoto (etapa 02). 
 - Recomendamos que o `git pull` sempre ser executado antes de `git push` para evitar conflitos ao mesclar as modificações do repositório local com o remoto.

## Criação do ambiente virtual

Vá a raiz do repositório. Em geral, a raiz do repositório é a pasta com o nome do projeto, nesse caso `thesisbr`

### Etapa 01: Configuração e criação do ambiente virtual

```
conda config --set pip_interop_enabled True && conda config --set env_prompt '({name})' && conda config --add envs_dirs ./env && conda env create -f environment.yml 
```

### Etapa 02: Ativar o ambiente virtual

. A partir dessa pasta, ative o ambiente a partir do seguinte comando:

``` conda activate env_thesisbr ```


## 📁 Estrutura do Projeto

```
thesisbr/
 ├── app/      
 ├── docs/              # Starlight
 │    ├── public/       
 │    ├── src/content/  
 │    │    └── docs/    # páginas de documentação
 │    └── astro.config.mjs
 ├── package.json
 ├── notebooks/         # exemplos
 ├── scrapers/         
 ├── README.md
 └── ...

 ```
