from src.app.models.inventory import Inventory, inventories_share_schema
from src.app.services import user_services


def create_product(product_category_id, product_code, title, value,brand, template, description, user_id=None):
    try:
        Inventory.seed(
            product_category_id= product_category_id, 
            user_id = user_id,  
            product_code = product_code, 
            title = title, 
            value = value,
            brand = brand, 
            template = template, 
            description = description
        )

        return ({'message': 'Item cadastrado com sucesso'})
    
    except:
        return ({'error': 'Erro ao cadastrar item'})


def generate_user_data(user_id):
    user = user_services.get_by_id(user_id) if user_id else None
        
    user_data = {
        'id': user['id'] if user else None,
        'name': user['name'] if user else 'Na empresa'
    }
    
    return user_data


def format_result(inventories):
    for inventory in inventories:  
        inventory['user_id'] = generate_user_data(inventory['user_id'])
        
    return inventories


def get_inventories_by_name(name, page=None):
    result = Inventory.query.filter(Inventory.title.ilike(f"%{name}%")).paginate(per_page=20, page=page)
    inventories = inventories_share_schema.dump(result.items)
        
    return format_result(inventories) if result else None

    
def get_all_inventories(page=None):
    inventories = inventories_share_schema.dump(Inventory.query.paginate(per_page=20, page=page).items)
    
    return format_result(inventories) if inventories else None
