from src.app import db
from src.app.models.city import City, cities_share_schema, city_share_schema
from src.app.models.gender import Gender, gender_share_schema, genders_share_schema
from src.app.models.inventory import Inventory, inventories_share_schema, inventory_share_schema
from src.app.models.user import User, users_share_schema, user_share_schema
from src.app.models.role import Role, role_share_schema, roles_share_schema


options_schema = {
    'inventory': inventory_share_schema, 'inventories': inventories_share_schema,
    'user': user_share_schema, 'user': users_share_schema,
    'city': city_share_schema, 'cities': cities_share_schema,
    'role': role_share_schema, 'roles': roles_share_schema,
    'gender': gender_share_schema, 'genders': genders_share_schema
    }

options_models = {
    'inventory': Inventory,
    'user': User, 
    'city': City,
    'role': Role,
    'gender': Gender
}


def queries(model, type_request, schema=None, filter_param=None):
    if type_request == 'filter':
        query_db_data = options_models[model].query.filter(options_models[model].name.ilike(f"%{filter_param}%")).all()
    if type_request == 'filter_by':
        query_db_data = options_models[model].query.filter_by(id=filter_param).first()
    if type_request == 'all':
        query_db_data = options_models[model].query.all()
    if schema:
        dict_query = options_schema[schema].dump(query_db_data)
        return dict_query
    return query_db_data


def check_existence(model: db.Model, id):
    return model.query.filter(model.id==id).first()
