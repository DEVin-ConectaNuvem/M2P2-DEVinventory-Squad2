import random
import os
import time
import requests
from flask import json
from src.app.models.country import Country, countries_share_schema
from src.app.models.state import State, states_share_schema
from src.app.models.city import City
from src.app.models.gender import Gender
from src.app.models.permission import Permission
from src.app.models.role import Role
from src.app.models.user import User
from src.app.models.product_category import ProductCategory
from src.app.models.inventory import Inventory
from src.app.utils import gera_password


def read_json():
    try:
        with open(f'{os.getcwd()}/src/app/database/dados_inventario.json', 'r') as File:
            json_object = json.load(File)
            return json_object

    except:
        return None


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

    genders_descriptions = ["Masculino", "Feminino", "Outro"]

    for gender in genders_descriptions:
        Gender.seed(description=gender)
    
    permissions = ['DELETE', 'READ', 'WRITE', 'UPDATE']

    for permission in permissions:
        Permission.seed(
            description=permission
        )

    roles = ["devfront", "devback", "coordenador", "admin"]
    
    roles_description = { "devfront": "Desenvolvedor Frontend", "devback": "Desenvolvedor Backend", "coordenador": "Coordenador", "admin": "Administrador do Sistema" }       

    permissions_dev_front = Permission.query.filter(Permission.description.in_(['READ', 'WRITE'])).all()
    permissions_dev_back = Permission.query.filter(Permission.description.in_(['READ', 'WRITE', 'UPDATE'])).all()
    permissions_coord = Permission.query.filter(Permission.description.in_(['READ'])).all()
    permissions_admin_sist = Permission.query.filter(Permission.description.in_(['DELETE', 'READ', 'WRITE', 'UPDATE'])).all()

    for index, role in enumerate(roles):
        if index == 0:
            Role.seed(
                description=roles_description['devfront'],
                name=role,
                permissions=permissions_dev_front
            )
        elif index == 1:
            Role.seed(
                description=roles_description['devback'],
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

    category_db_data = ProductCategory.query.all()
    dados_inventario = read_json()

    for item in dados_inventario:
        for category in category_db_data:
            if category.description == item['categoria']:
                cat_id = category.id
        cod = str(round(time.time() * 1000))
        cod_split = cod[7:]
        time.sleep(1)
        Inventory.seed(
            product_category_id=cat_id,
            user_id=None,
            title= item['name'],
            product_code=int(cod_split),
            value= item['price'],
            brand= item['brand'],
            template= item['template'],
            description=item['description']
        )

    users_data_request = requests.get('https://randomuser.me/api?nat=br&results=10')

    gender_description = {"male": "Masculino", "female" :"Feminino"}

    cities_db_data = City.query.order_by(City.name.asc()).all()
    genders_db_data = Gender.query.all()

    for user in users_data_request.json()['results']:
        if user['gender'] in gender_description:
            gender = gender_description[user['gender']]
        for gen in genders_db_data: 
            if gen.description == gender:
                gender_id = gen.id
        for city in cities_db_data:    
            if city.name == user['location']['city']:
                city_id = city.id
        User.seed(
        gender_id = gender_id,
        city_id= city_id,
        role_id=random.randint(1,4),
        name = user['name']['first'] + ' ' + user['name']['last'],
        age = user['dob']['date'],
        email = user['email'],
        phone = user['cell'],
        password = gera_password(),
        cep=None,
        complement=None,
        landmark=None,
        district=None,
        street = user['location']['street']['name'],
        number_street = user['location']['street']['number']
        )
    User.seed(
    gender_id = 1,
    city_id= 1,
    role_id=random.randint(1,4),
    name = 'Luis Lopes',
    age = "1991-12-21",
    email = "luislopes@gmail.com",
    phone = "9999999999",
    password = "123Mudar!",
    cep=None,
    complement=None,
    landmark=None,
    district=None,
    street = "Rua teste",
    number_street = 171
    )
    return print('Dados inseridos na database.')
