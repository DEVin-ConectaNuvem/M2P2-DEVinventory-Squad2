from src.app.models.inventory import Inventory

def create_product(product_category_id, user_id,  product_code, title, value,brand, template, description):
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
        
        return ('Item cadastrado com sucesso')
    
    except:
        return ('Erro ao cadastrar item')