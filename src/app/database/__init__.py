import requests
import time
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
    