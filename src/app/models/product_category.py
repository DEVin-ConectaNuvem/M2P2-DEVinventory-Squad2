from src.app import db, ma


class ProductCategory(db.Model):
    __tablename__ = 'product_categories'
    id = db.Column(db.Integer, autoincrement = True, primary_key = True)
    description = db.Column(db.String(84), nullable = False)

    def __init__(self, description):
        self.description = description

    @classmethod
    def seed(cls, description):
        product = ProductCategory(
        description = description
        )
        product.save()

    def save(self):
        db.session.add(self)
        db.session.commit()


class ProductCategorySchema(ma.Schema):
    class Meta:
        fields = ('id', 'description')
    
    
product_share_schema = ProductCategorySchema()
products_share_schema = ProductCategorySchema(many = True)
