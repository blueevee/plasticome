[tag1-image]: https://img.shields.io/badge/-1.0.0-purple

[python-image]:https://img.shields.io/badge/python-^3.10-yellow
[blast-image]:https://img.shields.io/badge/blast-^2.15-gree
[poetry-image]: https://img.shields.io/badge/poetry-^1.5.1-blue


# 🍄 PLASTICOME 🍄
![1.0.0][python-image] ![1.0.0][poetry-image] ![1.0.0][blast-image]
### Essa é uma ferramenta para identificar genes que possuem a capacidade de degradar plástico no genoma de um fungo. Ela é composta por uma pelo back-end que se caracteriza por essa API, um front-end [plasticome-frontend](https://github.com/G2BC/plasticome-frontend), e uma api que lida com as informações a serem registradas/consultadas no banco de dados [plasticome-metadata](https://github.com/G2BC/plasticome-metadata)

## 💙 Notas da desenvolvedora:
Esse projeto foi desenvolvido em ambiente windows 10 com python 3.11, pode precisar de ajustes ao ser executado em um ambiente diferente

### Versões
>![1.0.0][tag1-image] `07/11/2023`
> Plasticome funcionando apenas com dbCAN e ecPred, encontra muitas enzimas já que a comparação com a cazy family e ec numbers é bem ampla, mas já funciona!

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
2. Tenha o blast instalado e adicione o caminho para a pasta `\bin` na variável de ambiente `BLAST_PATH`
3. Tenha o gerenciador de pacotes do poetry instalado (pode usar outro e instalar as bibliotecas manualmente, mas recomendo fortemente o poetry)
4. Crie o ambiente virtual do poetry na raiz do projeto com `poetry shell`
5. Instale as dependências com `poetry install`
6. Tenha o docker instalado, pois as imagens do Dbcan e ECPred precisam dele para executar.
6. Duplique o arquivo [.env.example](/plasticome-backend/.env.example).
7. Apaque o sufixo `.example` e preencha nessa arquivo todas as informações necessárias.
7. Seja feliz e pode brincar com o plasticome!

## 🔍 Comandos importantes para o desenvolvimento:
`task - l`: Comando do taskipy para listar as tarefas configuradas

`task lint`: Verifica se o código está seguindo as convenções da PEP8, usando blue e isort

`task docs`: Serve a documentação

`task teste`: Executa os testes da aplicação

`task run`: Executa o servidor flask

## 🧾 TO DO list para a eu do futuro:
- [X] Adicionar o predição de `Ec numbers`
- [ ] Melhorar  a documentação
- [ ] Criar um container docker para publicar essa api online
- [ ] Adicionar SignalP na esteira de análise