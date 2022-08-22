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
    user_id = fields.Integer()

    @post_load()
    def change_decimal_places(self, data, **kwargs):
        value = data.get('value')
        data['value'] = round(value, 2)
        return data

    @validates('product_code')
    def validate_product_code(self, product_code):
        if len(str(product_code)) > 8 or product_code <= 0:
            raise ValidationError('O código do produto deve ser maior que 0 com no máximo 8 dígitos.')


class UpdateProductBodySchema(Schema):
    user_id = fields.Integer()
    title = fields.Str()
    value = fields.Float()
    brand = fields.Str()
    template = fields.Str()
    description = fields.Str()
    
    @post_load
    def validate_user_id(self, data, **kwargs):
        if not data.get('user_id'):
            data['user_id'] = None
            return data
        return data
