from flask import Flask, render_template, request, redirect
from database.get_connection import get_connection
from database.init_db import init_db
from database.insert_db import insert_db
import click
from flask.cli import with_appcontext
import database.user_controller as user_controller
import database.providers_controller as providers_controller
import database.movies_controller as movies_controller
import database.rentals_controller as rentals_controller
from datetime import date

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


@app.route('/peliculas')
def get_movies():
    movies = movies_controller.get_movies()
    return render_template('movies.html', movies=movies)


@app.route('/alquileres')
def get_rentals():
    rentals = rentals_controller.get_rentals()
    return render_template('rentals.html', rentals=rentals)


@app.route('/methods/crear_pelicula', methods=['POST'])
def create_movie():
    title = request.form['title']
    category = request.form['category']
    description = request.form['description']
    provider = request.form['provider']
    units = request.form['units']

    # First primary key check
    exists = movies_controller.get_movie_by_title(title)
    if exists is not None:
        return render_template('add_movie.html',
                               error='Violación de integridad de clave primaria: La película ya ha sido agregada')

    # Second foreign key check
    exists = providers_controller.get_provider_by_company(provider)
    if exists is None:
        return render_template('add_movie.html',
                               error='Violación de integridad de clave foránea: La empresa proveedora no existe')

    movies_controller.insert_movie(title, category, description, provider, units)
    return redirect('/peliculas')


@app.route('/methods/crear_alquiler', methods=['POST'])
def create_rental():
    title = request.form['title']
    owner = request.form['owner']
    start = request.form['start']
    end = request.form['end']
    type_query = request.form['type']

    # First primary key check
    exists = rentals_controller.get_rental_by_title_and_owner(title, owner)
    if exists is not None:
        return render_template('add_rental.html',
                               error='Violación de integridad de clave primaria: El alquiler ya ha sido creado')

    # Second foreign key check (with movie)
    exists = movies_controller.get_movie_by_title(title)
    if exists is None:
        return render_template('add_rental.html',
                               error='Violación de integridad de clave foránea: La película introducida no existe')

    # Third foreign key check (with user)
    exists = user_controller.get_user_by_nick(owner)
    if exists is None:
        return render_template('add_rental.html',
                               error='Violación de integridad de clave foránea: El usuario introducido no existe')

    # We must check if the movie is available with the total units
    units = movies_controller.get_movie_units(title)

    if units <= 0:
        return render_template('add_rental.html',
                               error='Restricción del dominio del problema: No hay unidades disponibles 🧿')

    # We must check if introduced date is greater than the current date
    if start < date.today().strftime("%Y-%m-%d"):
        return render_template('add_rental.html',
                               error='Restricción del dominio del problema: La fecha de alquiler no puede ser menor que la fecha actual 🧿')

    # We must check that the return date is greater than the rental date
    if start > end:
        rental = rentals_controller.get_rental_by_title_and_owner(title, owner)
        return render_template('add_rental.html',
                               error='Restricción del dominio del problema: La fecha de devolución no puede ser menor que la fecha de alquiler 🧿')

    rentals_controller.insert_rental(title, owner, start, end, type_query)

    # We must decrease the final units of the movie
    movies_controller.decrease_units(title)

    return redirect('/alquileres')


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


@app.route('/methods/eliminar_pelicula', methods=['POST'])
def delete_movie():
    title = request.form['title']
    movies_controller.delete_movie(title)
    return redirect('/peliculas')


@app.route('/alquileres/agregar_alquiler')
def add_rental():
    return render_template('add_rental.html')


@app.route('/proveedores/agregar_proveedor')
def add_provider():
    return render_template('add_provider.html')


@app.route('/usuarios/agregar_usuario')
def add_user():
    return render_template('add_user.html')


@app.route('/peliculas/agregar_pelicula')
def add_movie():
    return render_template('add_movie.html')


@app.route('/usuarios/editar_usuario/<string:id>')
def edit_user(id):
    user = user_controller.get_user_by_nick(id)
    return render_template('edit_user.html', user=user)


@app.route('/alquileres/editar_alquiler/<string:owner>/<string:title>')
def edit_rental(owner, title):
    rental = rentals_controller.get_rental_by_title_and_owner(title, owner)
    return render_template('edit_rental.html', rental=rental)


@app.route('/peliculas/editar_pelicula/<string:id>')
def edit_movie(id):
    movie = movies_controller.get_movie_by_title(id)
    return render_template('edit_movie.html', movie=movie)


@app.route('/methods/editar_usuario', methods=['POST'])
def update_user():
    nick = request.form['nick']
    name = request.form['name']
    email = request.form['email']
    user_controller.update_user(nick, name, email)
    return redirect('/usuarios')


@app.route('/methods/editar_pelicula', methods=['POST'])
def update_movie():
    title = request.form['title']
    category = request.form['category']
    description = request.form['description']
    provider = request.form['provider']
    units = request.form['units']

    # Second foreign key check
    exists = providers_controller.get_provider_by_company(provider)
    if exists is None:
        movie = movies_controller.get_movie_by_title(title)

        return render_template('edit_movie.html',
                               error='Violación de integridad de clave foránea: La empresa proveedora no existe',
                               movie=movie)

    movies_controller.update_movie(title, category, description, provider, units)
    return redirect('/peliculas')


@app.route('/methods/editar_alquiler', methods=['POST'])
def update_rental():
    owner = request.form['owner']
    title = request.form['title']
    rental_date = request.form['start']
    return_date = request.form['end']
    type_query = request.form['type']

    # We must check if introduced date is greater than the current date
    if rental_date < date.today().strftime("%Y-%m-%d"):
        rental = rentals_controller.get_rental_by_title_and_owner(title, owner)
        return render_template('edit_rental.html',
                               error='Restricción del dominio del problema: La fecha de alquiler no puede ser menor que la fecha actual 🧿',
                               rental=rental)

    # We must check that the return date is greater than the rental date
    if rental_date > return_date:
        rental = rentals_controller.get_rental_by_title_and_owner(title, owner)
        return render_template('edit_rental.html',
                               error='Restricción del dominio del problema: La fecha de devolución no puede ser menor que la fecha de alquiler 🧿',
                               rental=rental)

    rentals_controller.update_rental(title, owner, rental_date, return_date, type_query)

    return redirect('/alquileres')


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


@app.route('/methods/eliminar_alquiler', methods=['POST'])
def delete_rental():
    owner = request.form['owner']
    title = request.form['title']
    rentals_controller.delete_rental(title, owner)

    # We must increase the final units of the movie
    movies_controller.increase_units(title)

    return redirect('/alquileres')


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
