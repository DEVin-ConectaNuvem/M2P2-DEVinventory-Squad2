from marshmallow import Schema, fields, post_load
from src.app.utils.error_messages import handle_error_messages


class ProductBodySchema(Schema):
    product_category_id = fields.Integer(required=True, error_messages=handle_error_messages('product_category_id'))
    user_id = fields.Integer()
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
