from marshmallow import Schema, fields, post_load, validates, ValidationError
from src.app.utils.error_messages import handle_error_messages


class ProductBodySchema(Schema):
    product_category_id = fields.Integer(required=True, error_messages=handle_error_messages('product_category_id'))
    product_code = fields.Integer(required=True, error_messages=handle_error_messages('product_code'))
    title = fields.Str(required=True, error_messages=handle_error_messages('title'))
    value = fields.Float(required=True, error_messages=handle_error_messages('value'))
    brand = fields.Str(required=True, error_messages=handle_error_messages('brand'))
    template = fields.Str(required=True, error_messages=handle_error_messages('template'))
    description = fields.Str(required=True, error_messages=handle_error_messages('description'))

    @post_load()
    def change_decimal_places(self, data, **kwargs):
        value = data.get('value')

        return round(value, 2)

    @validates('product_code')
    def validate_product_code(self, product_code):
        if product_code < 8:
            raise ValidationError('O código do produto não pode ser menor que 8.')

class UpdateProductBodySchema(Schema):
    product_category_id = fields.Integer(required=True, error_messages=handle_error_messages('product_category_id'))
    product_code = fields.Integer(required=True, error_messages=handle_error_messages('product_code'))
    title = fields.Str()
    value = fields.Float()
    brand = fields.Str()
    template = fields.Str()
    description = fields.Str()
    
    @validates('product_code', 'product_category_id')
    def validate_product(self, product_code, product_category_id):
        if product_code or product_category_id:
            raise ValidationError('Esse campo não pode ser alterado.')

schema = ProductBodySchema()
print(schema.load({'product_code': 8}))
