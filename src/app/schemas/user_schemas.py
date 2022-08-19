from marshmallow import Schema, fields, ValidationError, validates
from src.app.utils.error_messages import handle_error_messages


def validate_password(password):
    if len(password) < 8:
        raise ValidationError('A senha precisa ser maior ou igual a 8.')

    if password.isalnum():
        raise ValidationError('A precisa ter pelo menos 1 caracter especial.')


class LoginBodySchema(Schema):
    email = fields.Email(required=True, error_messages=handle_error_messages('email'))
    password = fields.Str(required=True, error_messages=handle_error_messages('password'))

    @validates('password')
    def validate(self, password):
        validate_password(password)


class CreateUserBodySchema(Schema):
    city = fields.Str()
    gender = fields.Str()
    role = fields.Str()
    name = fields.Str(required=True, error_messages=handle_error_messages('name'))
    age = fields.DateTime(required=True, error_messages=handle_error_messages('age'))
    email = fields.Email(required=True, error_messages=handle_error_messages('email'))
    phone = fields.Str(required=True, error_messages=handle_error_messages('phone'))
    password = fields.Str(required=True, error_messages=handle_error_messages('password'))
    cep = fields.Str(required=True, error_messages=handle_error_messages('cep'))
    street = fields.Str(required=True, error_messages=handle_error_messages('street'))
    number_street = fields.Str(required=True, error_messages=handle_error_messages('number_street'))
    district = fields.Str(required=True, error_messages=handle_error_messages('district'))
    complement = fields.Str(required=True, error_messages=handle_error_messages('complement'))
    landmark = fields.Str(required=True, error_messages=handle_error_messages('landmark'))

    @validates('password')
    def validate(self, password):
        validate_password(password)
