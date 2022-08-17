import random
import time
import requests
from flask import json
from sqlalchemy.sql.expression import func
from src.app.models.country import Country, countries_share_schema
from src.app.models.state import State, states_share_schema
from src.app.models.city import City, cities_share_schema
from src.app.models.gender import Gender, gender_share_schema
from src.app.models.permission import Permission
from src.app.models.role import Role
from src.app.models.user import User, user_share_schema
from src.app.models.product_category import ProductCategory
from src.app.models.inventory import Inventory


def read_json():
    try:
        with open(f'src\\app\database\dados_inventario.json', 'r') as File:
            json_object = json.load(File)
            return json_object

    except:
        return None


def gera_password(): 
    letras = "abcdefghijklmnopqrstuvwxyzABCEFGHIJKLMNOPQRSTUVWXYZ123456789"
    caracter = '!@#$%&^*-_'

    password = ""

    for i in range(0, 1):
        password_caracter = random.choice(caracter)
        password += password_caracter
        for h in range(0, 14):
            password_letras = random.choice(letras)
            password += password_letras
    return password


def populate_db():

    country = Country.query.first()

    if country != None:
        print("Já existem dados populados no banco.")
        return 
    
    brasil_code = 76
    country_data_request = requests.get(f"https://servicodados.ibge.gov.br/api/v1/localidades/paises/{brasil_code}")
    states_data_request = requests.get("https://servicodados.ibge.gov.br/api/v1/localidades/estados")
    cities_data_request = requests.get("https://servicodados.ibge.gov.br/api/v1/localidades/municipios")

    country_name = country_data_request.json()[0]['nome']
    Country.seed(name=country_name, language='Português')

    country_db_data = Country.query.all()
    country_db_dict = countries_share_schema.dump(country_db_data)

    for state in states_data_request.json():
        State.seed(
            country_id=country_db_dict[0]['id'],
            name=state['nome'],
            initials=state['sigla']
        )

    states_db_data = State.query.order_by(State.name.asc()).all()
    state_db_dict = states_share_schema.dump(states_db_data)

    for city in cities_data_request.json():
        state_id = 0
        for state in state_db_dict:
            if state['initials'] == city['microrregiao']['mesorregiao']['UF']['sigla']:
                state_id = state['id']
        City.seed(
            state_id=state_id,
            name=city['nome']
        )

    genders_descriptions = ["Masculino", "Feminino"]

    for gender in genders_descriptions:
        Gender.seed(description=gender)
    
    permissions = ['DELETE', 'READ', 'WRITE', 'UPDATE']

    for permission in permissions:
        Permission.seed(
            description=permission
        )

    roles = ["Desenvolvedor Frontend", "Desenvolvedor Backend", "Coordenador", "Administrador do Sistema"]
    
    roles_description = {
        'dev_front': 'O usuário dev. front end poderá ler e escrever no sistema.',
        'dev_back': 'O usuário dev. back end poderá ler, escrever, atualizar os itens no sistema.',
        'coordenador': 'O usuário coordenador poderá somente fazer a leitura dos dados no sistema.',
        'admin': 'O usuário administrador do sistema poderá ler, escrever, deletar e atualizar os dados no sistema.'
        }       

    permissions_dev_front = Permission.query.filter(Permission.description.in_(['READ', 'WRITE'])).all()
    permissions_dev_back = Permission.query.filter(Permission.description.in_(['READ', 'WRITE', 'UPDATE'])).all()
    permissions_coord = Permission.query.filter(Permission.description.in_(['READ'])).all()
    permissions_admin_sist = Permission.query.filter(Permission.description.in_(['DELETE', 'READ', 'WRITE', 'UPDATE'])).all()

    for index, role in enumerate(roles):
        if index == 0:
            Role.seed(
                description=roles_description['dev_front'],
                name=role,
                permissions=permissions_dev_front
            )
        elif index == 1:
            Role.seed(
                description=roles_description['dev_back'],
                name=role,
                permissions=permissions_dev_back
            )
        elif index == 2:
            Role.seed(
                description=roles_description['coordenador'],
                name=role,
                permissions=permissions_coord
            )
        else:
            Role.seed(
                description=roles_description['admin'],
                name=role,
                permissions=permissions_admin_sist
            )
    
    categories = ["Perifericos", "Eletronicos", "Eletrodomesticos", "Ferramentas", "Outros acessorios"]

    for category in categories:
        ProductCategory.seed(
            description=category
        )

    dados_inventario = read_json()

    for item in dados_inventario:
        for category in categories:
            if category == item['categoria']:
                Inventory.seed(
                    product_category_id=category,
                    title= item['name'],
                    product_code=int(round(time.time() * 1000)),
                    value= item['price'],
                    brand= item['brand'],
                    template= item['template'],
                    description=item['description']
                )

    users_data_request = requests.get('https://randomuser.me/api?nat=br&results=10')

    gender_description = {"male": "Masculino", "female" :"Feminino"}

    cities_db_data = City.query.order_by(City.name.asc()).all()
    cities_db_dict = cities_share_schema.dump(cities_db_data)

    for user in users_data_request.json()['results']:
        if user['gender'] in gender_description:
            gender = gender_description[user['gender']]
        for city in cities_db_dict:    
            if city['name'] == user['location']['city']:
                User.seed(
                gender_id = gender,
                city_id= city['id'],
                name = user['name']['first'] + ' ' + user['name']['last'],
                age = user['dob']['date'],
                email = user['email'],
                phone = user['cell'],
                password = gera_password(),
                street = user['location']['street']['name'],
                number_street = user['location']['street']['number']
                )
    print('Dados inseridos na database.')
    return