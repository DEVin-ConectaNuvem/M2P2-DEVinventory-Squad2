from functools import wraps
from marshmallow import Schema, ValidationError
from flask import request, jsonify


def validate_body(schema: Schema):
    def body_required(function_current):
        @wraps(function_current)
        def wrapper(*args, **kwargs):
            body = request.json

            try:
                load_schema = schema.load(body)

                return function_current(body=load_schema, *args, **kwargs)

            except ValidationError as error:
                return jsonify(error.messages), 400

        return wrapper

    return body_required
