from flask import Flask
from database.get_connection import get_connection
from database.init_db import init_db
from database.insert_db import insert_db
import click
from flask.cli import with_appcontext

app = Flask(__name__)
app.config.from_pyfile("config/config.py")


@app.route('/getSelect')
def get_select():
    connection = get_connection()
    with connection.cursor() as cursor:
        cursor.execute('SELECT * FROM Usuario')
        result = cursor.fetchall()
    connection.close()
    return str(result)


@click.command("init-db")
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables"""
    init_db()
    click.echo("Database initialized correctly!")
    insert_db()
    click.echo("All records in the database have been inserted correctly!")


app.cli.add_command(init_db_command)


@app.route('/restoreDatabaseEmpty')
def create_database():
    init_db()
    return str("The database has been successfully restored!")


@app.route('/restoreDatabaseInitialized')
def insert_records():
    # We must restore the database to its original state for insert the vanilla records
    init_db()
    insert_db()
    return str("The database has been successfully restored and initialized!")


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


if __name__ == '__main__':
    app.run(debug=True)
