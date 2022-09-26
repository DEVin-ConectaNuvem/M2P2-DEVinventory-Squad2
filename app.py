import os
import click
from flask.cli import with_appcontext
from src.app import create_app, db
from src.app.database import populate_db
from src.app.routes import routes

app = create_app(os.getenv('FLASK_ENV'))

routes(app)

@click.command(name='populate_db')
@with_appcontext
def call_command():
    populate_db()

@click.command(name='drop_all_tables') # a tabela alembic_version continuará existindo
@with_appcontext
def drop_all_tables():
    db.drop_all()

app.cli.add_command(call_command)
app.cli.add_command(drop_all_tables)


if __name__ == "__main__":
    app.run()
