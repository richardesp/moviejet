from flask import Flask, render_template, request, redirect
from database.get_connection import get_connection
from database.init_db import init_db
from database.insert_db import insert_db
import click
from flask.cli import with_appcontext
import database.user_controller as user_controller
import database.providers_controller as providers_controller

app = Flask(__name__)
app.config.from_pyfile("config/config.py")


@app.route('/usuarios')
def get_users():
    users = user_controller.get_users()
    return render_template('users.html', users=users)


@app.route('/proveedores')
def get_providers():
    providers = providers_controller.get_providers()
    return render_template('providers.html', providers=providers)


@app.route('/methods/crear_proveedor', methods=['POST'])
def create_provider():
    company = request.form['company']
    nif = request.form['nif']
    phone = request.form['phone']

    exists = providers_controller.get_provider_by_company(company)
    if exists is not None:
        return render_template('add_provider.html',
                               error='Violación de integridad de clave primaria: La empresa ya ha sido creada')

    providers_controller.insert_provider(company, nif, phone)
    return redirect('/proveedores')


@app.route('/methods/eliminar_proveedor', methods=['POST'])
def delete_provider():
    company = request.form['company']
    providers_controller.delete_provider(company)
    return redirect('/proveedores')


@app.route('/proveedores/agregar_proveedor')
def add_provider():
    return render_template('add_provider.html')


@app.route('/usuarios/agregar_usuario')
def add_user():
    return render_template('add_user.html')


@app.route('/usuarios/editar_usuario/<string:id>')
def edit_user(id):
    user = user_controller.get_user_by_nick(id)
    return render_template('edit_user.html', user=user)


@app.route('/methods/editar_usuario', methods=['POST'])
def update_user():
    nick = request.form['nick']
    name = request.form['name']
    email = request.form['email']
    user_controller.update_user(nick, name, email)
    return redirect('/usuarios')


@app.route('/methods/crear_usuario', methods=['POST'])
def create_user():
    nick = request.form['nick']

    exists = user_controller.get_user_by_nick(nick)
    if exists is not None:
        return render_template('add_user.html', error='Violación de integridad de clave primaria: El nick ya existe')

    name = request.form['name']
    email = request.form['email']

    user_controller.insert_user(nick, name, email)
    return redirect('/usuarios')


@app.route('/methods/eliminar_usuario', methods=['POST'])
def delete_user():
    nick = request.form['nick']
    user_controller.delete_user(nick)
    return redirect('/usuarios')


@app.route('/proveedores/editar_proveedor/<string:id>')
def edit_provider(id):
    provider = providers_controller.get_provider_by_company(id)
    return render_template('edit_provider.html', provider=provider)


@app.route('/methods/editar_proveedor', methods=['POST'])
def update_provider():
    company = request.form['company']
    nif = request.form['nif']
    phone = request.form['phone']
    providers_controller.update_provider(company, nif, phone)
    return redirect('/proveedores')


@click.command("init-db")
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables"""
    init_db()
    click.echo("Database initialized correctly! 🚀")
    insert_db()
    click.echo("All records in the database have been inserted correctly! 🔋")


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
def get_index():  # put application's code here
    return render_template('base.html')


if __name__ == '__main__':
    app.run(debug=True)
