import click
from flask.cli import with_appcontext
from src.app import create_app
from src.app.database import populate_db


app = create_app()


@click.command(name='populate_db')
@with_appcontext
def call_command():
    populate_db()


app.cli.add_command(call_command)


if __name__ == "__main__":
    app.run()
