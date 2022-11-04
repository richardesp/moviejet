from database.get_connection import get_connection


def get_movies():
    connection = get_connection()
    with connection.cursor() as cursor:
        cursor.execute('SELECT titulo, categoria, descripcion, empresa_proveedora, unidades FROM Pelicula')
        movies = cursor.fetchall()
    connection.close()
    return movies


def insert_movie(title, category, description, provider, units):
    connection = get_connection()
    with connection.cursor() as cursor:
        cursor.execute(
            'INSERT INTO Pelicula (titulo, categoria, descripcion, empresa_proveedora, unidades) VALUES (%s, %s, %s, %s, %s)',
            (title, category, description, provider, units))


def delete_movie(title):
    connection = get_connection()
    with connection.cursor() as cursor:
        cursor.execute('DELETE FROM Pelicula WHERE titulo = %s', (title,))


def get_movie_by_title(title):
    connection = get_connection()
    with connection.cursor() as cursor:
        cursor.execute(
            'SELECT titulo, categoria, descripcion, empresa_proveedora, unidades FROM Pelicula WHERE titulo = %s',
            (title,))
        movie = cursor.fetchone()
    connection.close()
    return movie


def update_movie(title, category, description, provider, units):
    connection = get_connection()
    with connection.cursor() as cursor:
        cursor.execute(
            'UPDATE Pelicula SET categoria = %s, descripcion = %s, empresa_proveedora = %s, unidades = %s WHERE titulo = %s',
            (category, description, provider, units, title))
