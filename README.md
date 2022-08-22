<h2 align="center">Projeto DEVinventory</h1>

![Image](https://user-images.githubusercontent.com/101053966/185769837-ccf6b9cc-4d90-43f7-835a-7ad3feabf94a.jpeg)


## Empresa

<p>A empresa responsável pelo projeto é a M2P2 Software Ltda e o squad responsável pelo desenvolvimento é a equipe Black Mirror.</p>

## Tópicos

- [Descrição do projeto](#descrição-do-projeto)
- [Realização do projeto](#realização-do-projeto)
- [Funcionalidades](#funcionalidades)
- [Como executar](#como-executar)
- [Endpoints](#endpoints)
- [Tecnologias utilizadas](#tecnologias-utilizadas)
- [Agradecimentos](#agradecimentos)
- [Desenvolvedores](#desenvolvedores)

## Descrição do projeto
<p align="justify">
 Este é o segundo projeto do módulo 2 do curso DEVinHouse do Serviço Nacional de Aprendizagem Industrial - SENAI em parceria com o LAB365 e a empresa Conecta Nuvem. A proposta deste projeto é a construção de uma API com sistema backend de cadastro e empréstimos de itens das empresas para seus funcionários.
 A proposta tem como base um arquivo com requisitos da aplicação e contém um modelo de entidade relacionamento para construção do banco de dados através da utilização das tecnologias python, SQL, postgresql e flask.
</p>

## Realização do projeto
<p align="justify">
 O desenvolvimento foi realizado em grupo simulando o dia-a-dia de uma empresa do ramo de tecnologia através das metodologias ágeis. Utilizamos a metodologia scrum, onde nosso squad é formado por 7 desenvolvedores full stack e o product owner é o professor da turma.
</p>
<p align="justify">
 No primeiro dia nos praparamos em uma sprint planning juntamente com a sprint backlog (visto o prazo curto), definindo o formato dos commits, nomes de branchs, realização dos pull requests, taks, e ferramenta para organização do desenvolvimento. Para realização das atividades definimos utilizar o trello, separando os cards como tasks, onde cada desenvolvedor está livre para escolher sua task e arrastar entre os campos definidos na ferramenta, lembrando sempre de deixar o card no campo 'code review' enquanto o pull requst estiver sendo testado.
</p>
<p align="justify">
 Todos os dias fizemos a daily, repassando o que foi desenvolvido e se houveram dificuldades. Como o prazo para entrega é curto, todos ajudavam quando ocorria alguma dificuldade entre os desenvolvedores.
</p>

![imagem_2022-08-18_104446081](https://user-images.githubusercontent.com/101053966/185410294-83c9b492-d931-47bb-8247-09bc27997d17.png)

## Funcionalidades

✔️ `Login:` Efetuar login no sistema.

✔️ `Login/Cadastro:` Efetuar login com uma conta google.

✔️ `Cadastro:` Realizar cadastro dos colaboradores da empresa.

✔️ `Cadastro:` Realizar o cadastro de itens no inventário.

✔️ `Emprestimo:` Realizar o empréstimo de itens para os colaboradores.

✔️ `Contagem:` Efetuar a contagem de itens emprestados, total de itens cadastrados, soma dos valores totais de todos os itens e total de colaboradores cadastrados.

✔️ `Atualização:` Efetuar a atualização dos dados do colaborador e/ou itens quando necessário.

## Como executar

- Primeiramente você precisará ter instalado em sua máquina: **Python 3.10**, **Poetry**, **Postgresql** e uma plataforma de sua preferência: pgAdmin, DBeaver ou outro.
<p align="justify">
    Para instalação utilizar:
</p>

Python:
```
https://www.python.org/downloads/windows/
```
```
https://python.org.br/instalacao-linux/
```
Poetry:
* osx / linux / bashonwindows install instructions
```
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
```
* windows powershell install instructions
```
(Invoke-WebRequest -Uri https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py -UseBasicParsing).Content | python -
```
Postgresql:
```
https://www.postgresql.org/download/
```
`Sugestão`: pgAdmin:
```
https://www.pgadmin.org/download/
```

Em seguida você precisará executar os comandos a seguir para criar o ambiente virtual local, ativá-lo e instalar as dependências do projeto:

```
poetry config --local virtualenvs.in-project true
```
```
.\.venv\Scripts\activate
```
```
poetry install
```
<p align="justify">
 A seguir você precisará criar um arquivo de variáveis de ambiente chamado *.env*. Para isso você utilizará como exemplo o arquivo *.env_example*, apenas trocando os dados de exemplo para os dados que você irá utilizar em sua máquina para testes.
</p>

Feito isso, você irá utilizar os comandos a seguir para criar suas tabelas:

```
poetry run flask db init
```
```
poetry run flask db migrate
```
```
poetry run flask db upgrade
```
Para ter alguns dados no banco e manipulá-los:
```
poetry run flask populate_db
```
`OBS`: Caso precise, pode utilizar o comando **_poetry run flask drop_all_tables_** para retirar todas as tabelas do banco e recomeçar novamente (não sendo necessário o comando 'poetry run flask db init'). 

## Endpoints
1. `[POST] /user/login (users)` - [Regras endpoint 1](#regras-endpoint-1)
2. `[POST] /auth/google (users)` - [Regras endpoint 2](#regras-endpoint-2)
3. `[GET] /callback (users)` - [Regras endpoint 3](#regras-endpoint-3)
4. `[POST] /user/create (users)` - [Regras endpoint 4](#regras-endpoint-4)
5. `[GET] /user?<int:id> ou <string:name> (users)` - [Regras endpoint 5](#regras-endpoint-5)
6. `[PATCH] /user/<int:users> (users)` - [Regras endpoint 6](#regras-endpoint-6)
7. `[POST] /inventory (inventories)` - [Regras endpoint 7](#regras-endpoint-7)
8. `[PATCH] /user/<int:inventory> (inventory)` - [Regras endpoint 8](#regras-endpoint-8)
9. `[GET] /inventory?<int:id> ou <string:name> (inventories)` - [Regras endpoint 9](#regras-endpoint-9)
10. `[GET] /inventory/results (inventories)` - [Regras endpoint 10](#regras-endpoint-10)

### Regras ENDPOINT 1:

- o body da requisição deve conter obrigatoriamente as chaves email e password;
- o usuário deve estar desconectado para este endpoint de usuário;
- se estiver faltando algum dos campos obrigatórios, será retornada uma mensagem de erro com o Status 400;
- se o e-mail que for enviado não existir no banco de dados, será retornado um erro informando que não foi possível efetuar o login, utilizando o status 401;
- se a senha estiver errada, será retornado um erro informando que não foi possível efetuar o login, utilizando o status 401;
- Caso, todas as informações estejam corretas, será retornado o token da aplicação utilizando o código 200.
- Após realizado o login, o usuário receberá um token. O token deve ser adicionado ao HEADERS da requisição com o tipo Bearer.

#### Body parameters

```js
{
  email (obrigatório),
  password (obrigatório)
}
```

### Regras ENDPOINT 2:

- O usuário deve estar desconectado para este endpoint de usuário.
- Utilizar a configuração do OAuth2 previamente configurada.
- Caso, todas as informações estejam corretas, irá retornar a url do redirecionamento da aplicação utilizando o código 200.

### Regras ENDPOINT 3:

- Verificar se o e-mail recebido está cadastrado no banco de dados, se não estiver deve cadastrar.
- Realizar o redirecionamento após validar os valores enviados da url e do client do backend.

### Regras ENDPOINT 4:

- O usuário deve estar logado e possuir autorização (READ, WRITE, UPDATE e DELETE) para este endpoint de usuário. Caso não possua, irá retornar o Status de Erro 403 (Forbidden).
- Se estiver faltando algum dos campos obrigatórios, irá retornar uma mensagem de erro com o Status 400.
- Se o e-mail que for enviado já existir no banco de dados, irá retornar um erro status 400 informando que não é possível cadastrar o usuário.
- O password será criptografado no banco de dados, a regra está no respectivo model.
- O password deve conter 8 dígitos e pelo menos um caracter especial.
- O telefone deve conter 11 dígitos e não pode conter nenhuma letra ou caracter especial.
- Ao criar o usuário, deve-se retornar o Status 201 (Created)

### Regras ENDPOINT 5:

- O usuário deve estar logado e possuir autorização READ para este endpoint de usuário. Caso não possua, irá retornar o Status de Erro 403 (Forbidden).
- Irá retornar os usuários que contenham o nome (name) que foi enviado via param.
- O endpoint é paginado, retornando 20 usuários por página.
- Em caso de não ser enviado nenhum queryParam, irá retornar todos os usuários de acordo com a paginação.
- Caso não seja encontrado nenhum resultado, irá retornar o Status 204 (No Content).
- Caso seja encontrado ao menos um resultado, irá retornar um JSON contendo o id, name, email, phone e a role.name dos usuários, além do Status 200 (OK).

#### Query Param (não obrigatório)

`EXAMPLE: http:127.0.0.1:5000/user/1` - Para ver a página 1 que irá retornar 20 itens por página. Caso não exista a página, irá retornar erro NOT FOUND status 404.

`EXAMPLE: http:127.0.0.1:5000/user/NOME ALEATÓRIO` - Irá fazer requisição de algum nome de sua escolha e irá listar o(s) usuário(s) encontrado(s).
Se não, irá dar NO CONTENT 204

`EXAMPLE: http:127.0.0.1:5000/user` - Irá te levar para a página 1 caso você não envie parametro de página e mostrará uma lista de até 20 usuários.

### Regras ENDPOINT 6:

- O usuário deve estar logado e possuir autorização UPDATE para este endpoint de usuário. Caso não possua, será retornado o Status de Erro 403 (Forbidden).
- Há validação caso não encontrar o id enviado e retorna erro status 404.
- Os campos preenchidos na database não podem ser alterados para campos vazios ou que não respeitem as validações da model (user).
- Caso seja alterado será retornado o Status 204 (No Content).

#### Query Param (obrigatório)

`EXAMPLE: http:127.0.0.1:5000/user/5` - Para atualizar usuário com id 5, caso não exista a página irá retornar erro NOT FOUND status 404.

#### Body parameter

```js
{
  city_id (obrigatório),
  gender_id (obrigatório),
  role_id (obrigatório),
  name (obrigatório),
  age (obrigatório),
  email (obrigatório),
  phone (obrigatório),
  password (obrigatório),
  cep (obrigatório),
  street (obrigatório),
  number_street (obrigatório),
  district (obrigatório),
  complement (opcional),
  landmark (opcional)
}
```

### Regras ENDPOINT 7:

- O usuário deve estar logado e possuir autorização WRITE para este endpoint de usuário. Caso não possua, irá retornar o Status de Erro 403 (Forbidden).
- Se estiver faltando algum dos campos obrigatórios, irá retornar uma mensagem de erro com o Status 400.
- Se o product_code que for enviado já existir no banco de dados, retornará um erro informando que não é possível criar um novo produto no inventário, utilizando o status 400.
- O value não pode ser menor ou igual a zero.
- Ao criar o item, retornará o Status 201 (Created).

#### Body parameter

```js
{
    product_category_id (obrigatório), 
    user_id  (opcional), 
    product_code (obrigatório), 
    title  (obrigatório), 
    value  (obrigatório), 
    brand  (obrigatório), 
    template  (obrigatório), 
    description  (obrigatório)
}
```

### Regras ENDPOINT 8:

- O usuário deve estar logado e possuir autorização UPDATE para este endpoint de usuário. Caso não possua, irá retornar o Status de Erro 403 (Forbidden).
- É possível alterar todos os campos, exceto product_category_id e product_code, retornando 400 caso algum deles seja enviado.
- Irá respeitar as validações da respectiva model.
- Ao atualizar o item, irá retornar o Status 204 (No Content).

#### Entradas

- id: integer (Path param required)
- quaisquer campos (Body param não required)

### Regras ENDPOINT 9:

- O usuário deve estar logado e possuir autorização READ para este endpoint de usuário. Caso não possua, retornará o Status de Erro 403 (Forbidden).
- Retornará todos os itens que contenham o nome (title) passado no query param.
- O endpoint é paginado, retornando 20 itens por página.
- Obs: em caso de não ser enviado nenhum queryParam, irá retornar todos os itens de acordo com a paginação.
- Caso o user_id seja null, retornar o nome do usuário como {id: None, name: “Na Empresa”}.
- Caso não seja encontrado nenhum resultado, retornará o Status 204 (No Content).
- Caso seja encontrado ao menos um resultado, retornará um JSON contendo o id, product_code, title, product_category, user, além do Status 200 (OK).

#### Entrada:
name: string (Query param não obrigatório)

### Regras ENDPOINT 10

- O usuário deve estar logado e possuir autorização READ para este endpoint de inventário. Caso não possua, irá retornar o Status de Erro 403 (Forbidden).
- Retorna o número de usuários cadastrados no sistema.
- Retorna o número de itens cadastrados no sistema.
- Retorna o total da soma de todos os valores dos itens.
- Retorna quantos itens estão emprestados para usuários.
- Retorna as estatísticas, além do Status 200 (OK).

## Tecnologias utilizadas

<p align="left"> 
<a href="https://flask.palletsprojects.com/" target="_blank" rel="noreferrer"> <img src="https://www.vectorlogo.zone/logos/pocoo_flask/pocoo_flask-icon.svg" alt="flask" width="40" height="40"/> 
</a> 
<a href="https://www.sqlalchemy.org" target="_blank" rel="noreferrer"> <img src="https://butecotecnologico.com.br/comecando-com-sql-alchemy/sql-alchemy-logo_hu9aaae5cb0138810bd2a9b3020b120bcf_12170_200x200_resize_q90_bgffffff_linear_2.jpg" alt="sqlalchemy" width="40" height="40"/> 
</a> 
<a href="https://www.sqlalchemy.org" target="_blank" rel="noreferrer"> <img src="https://cdn-icons-png.flaticon.com/512/2772/2772165.png" alt="sql" width="40" height="40"/> 
</a> 
<a href="https://flask-marshmallow.readthedocs.io/en/latest/" target="_blank" rel="noreferrer"> <img src="https://w7.pngwing.com/pngs/1009/741/png-transparent-python-serialization-object-marshmallow-database-marshmellow-angle-white-face-thumbnail.png" alt="marshmallow" width="40" height="40"/> 
</a> 
<a href="https://git-scm.com/" target="_blank" rel="noreferrer"> <img src="https://www.vectorlogo.zone/logos/git-scm/git-scm-icon.svg" alt="git" width="40" height="40"/> 
</a> 
<a href="https://www.postgresql.org" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/postgresql/postgresql-original-wordmark.svg" alt="postgresql" width="40" height="40"/> 
</a> 
<a href="https://www.python.org" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/python/python-original.svg" alt="python" width="40" height="40"/> 
</a> 
</p>

## Agradecimentos

<p align="justify">
 Agradecemos a toda a equipe DEVinHouse, SENAI e LAB365 pela oportunidade e os desafios propostos durante o curso.
</p>
<p align="justify">
 Um agradecimento especial para o nosso professor, criador da proposta do projeto e Product Owner do squad <a href="https://github.com/pedrohbsilva" target="_blank" rel="noreferrer">Pedro Henrique B. da Silva</a>, pelas aulas sobre banco de dados, as orientações durante o desenvolvimento do projeto e vínculo de amizade criado.  
</p>

## Desenvolvedores

| [<sub>Breno Martins</sub><br><img src="https://avatars.githubusercontent.com/u/95316873?v=4" width=100><br>](https://github.com/Breno-MT) | [<sub>Luiz Gustavo Seeman</sub><br><img src="https://avatars.githubusercontent.com/u/101838119?v=4" width=100><br>](https://github.com/Gustavo-Seemann) | [<sub>Marcelo Coelho</sub><br><img src="https://avatars.githubusercontent.com/u/92119579?v=4" width=100><br>](https://github.com/MCoelho222) | 
| :---: | :---: | :---: |
| [<sub>Rafael Telles Carneiro</sub><br><img src="https://avatars.githubusercontent.com/u/98103640?v=4" width=100><br>](https://github.com/rafatellescarneiro) | [<sub>Josinaldo Andrade Pereira</sub><br><img src="https://avatars.githubusercontent.com/u/101839277?v=4" width=100><br>](https://github.com/josinaldoandradepereira) | [<sub>Thiago William</sub><br><img src="https://avatars.githubusercontent.com/u/94487053?v=4" width=100><br>](https://github.com/ThiagoW21) | 
[<sub>Vinicius Possatto Stormoski</sub><br><img src="https://avatars.githubusercontent.com/u/101053966?v=4" width=100><br>](https://github.com/ViniciusPosssatto)
