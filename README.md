# 🍄 PLASTICOME 🍄
### Essa é uma ferramenta para identificar genes que possuem a capacidade de degradar plástico no genoma de um fungo.

## 💙 Notas da desenvolvedora:
Esse projeto foi desenvolvido em ambiente windows 10 com python 3.11, pode precisar de ajustes ao ser executada em um ambiente diferente

## 🔍Escolhas para o ambiente de desenvolvimento:
> ### Poetry
> O Poetry é uma ferramenta de gerenciamento de dependências e construção de projetos Python. Seu gerenciamento de dependências é completamente simplificado, garantindo que todas as dependências estejam documentadas em seu arquivo  [`pyproject.toml`](pyproject.toml), evitando a necessidade de criar um arquivo manual `requirements.txt. Além disso ele cria e gerencia ambientes virtuais automaticamente em cada projeto, e facilita a instalação e atualização de dependências.
>
> ### Pytest
> Além de oferecer uma abordagem simplificada e uma estrutura limpa que pode ser compreendida até por quem nunca mexeu com testes.
>
> ### Blue
> Blue é um formatador de código python que segue todas as convenções de boas práticas e organização de código lançadas na PEP8.
>
> ### iSort
>Tembém para seguir a PEP8, o iSort gerencia e organiza os imports de todo o projeto.
>
> ### Taskipy
> Simplifica a forma de fazer comandos, por exemplo invés de lembrar todos os parâmetros pra rodar um teste (`test --v --cov=plasticome`) contruir uma automatização para rodar apenas `test`, e da mesma forma com os linters, docs e rodar a aplicação de fato.

## 😎 Quero mexer nesse projeto preciso de que?
1. Certifique-se de ter o python 3.10+
2. Tenha o gerenciador de pacotes do poetry instalado (pode usar outro e instalar as bibliotecas manualmente, mas recomendo fortemente o poetry)
2. Crie o ambiente virtual do poetry na raiz do projeto com `poetry shell`
2. Instale as dependências com `poetry install`
2. Seja feliz e pode brincar com o plasticome!

## 🔍 Comandos impotantes para o desenvolvimento:
`task - l`: Comando do taskipy para listar as tarefas configuradas

`task lint`: Verifica se o código está seguindo as convenções da PEP8, usando blue e isort

`task docs`: Serve a documentação

`task teste`: Executa os testes da aplicação

`task run`: Executa o servidor flask
