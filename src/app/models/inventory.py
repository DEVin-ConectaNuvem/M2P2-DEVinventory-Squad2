from src.app import db, ma
from src.app.models.product_category import ProductCategory, products_share_schema
from src.app.models.user import User, user_share_schema


class Inventory(db.Model):
    __tablename__ = 'inventories'
    id = db.Column(db.Integer, autoincrement = True, primary_key = True)
    product_category_id = db.Column(db.Integer, db.ForeignKey(ProductCategory.id), nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable = True)
    title = db.Column(db.String(84), nullable = False)
    product_code = db.Column(db.Integer, nullable = False, unique = True)
    value = db.Column(db.Float, nullable = False)
    brand = db.Column(db.String(84), nullable = False)
    template = db.Column(db.String(84), nullable = False)
    description = db.Column(db.String(200), nullable = False)
    product_category = db.relationship("ProductCategory", foreign_keys=[product_category_id])
    user = db.relationship("User", foreign_keys=[user_id])

    def __init__(self, product_category_id, user_id, title, product_code, value, brand, template, description):
        self.product_category_id = product_category_id
        self.user_id = user_id
        self.title = title
        self.product_code = product_code
        self.value = value
        self.brand = brand
        self.template = template
        self.description = description
      
    @classmethod
    def seed(cls, product_category_id, user_id, title, product_code, value, brand, template, description):
        inventory = Inventory(
            product_category_id = product_category_id,
            user_id = user_id,
            title = title,
            product_code = product_code,
            value = value,
            brand = brand,
            template = template,
            description = description
        )
        inventory.save()

    def save(self): 
        db.session.add(self)
        db.session.commit()


class InventorySchema(ma.Schema):
    product_category = ma.Nested(products_share_schema)
    user = ma.Nested(user_share_schema)
    class Meta:
        fields = ('id', 'product_category_id', 'user_id', 'title', 'product_code', 'value', 'brand', 'template', 'description')


inventory_share_schema = InventorySchema()
inventories_share_schema = InventorySchema(many = True)
