
def handle_error_messages(field):
    error_message = {
        'required': f'O campo {field} é obrigatório.',
        'invalid': 'Não é um campo válido.'
    }

    return error_message
