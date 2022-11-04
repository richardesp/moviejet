from database.get_connection import get_connection


def get_rentals():
    connection = get_connection()
    with connection.cursor() as cursor:
        cursor.execute(
            'SELECT titulo_pelicula, nick_propietario, alquiler_inicio, alquiler_fin, tipo_alquiler FROM Alquiler')
        rentals = cursor.fetchall()
    connection.close()
    return rentals


def insert_rental(title, owner, start, end, type_query):
    connection = get_connection()
    with connection.cursor() as cursor:
        cursor.execute(
            'INSERT INTO Alquiler (titulo_pelicula, nick_propietario, alquiler_inicio, alquiler_fin, tipo_alquiler) VALUES (%s, %s, %s, %s, %s)',
            (title, owner, start, end, type_query))


def delete_rental(title, owner):
    connection = get_connection()
    with connection.cursor() as cursor:
        cursor.execute('DELETE FROM Alquiler WHERE titulo_pelicula = %s AND nick_propietario = %s', (title, owner))


def get_rental_by_title_and_owner(title, owner):
    connection = get_connection()
    with connection.cursor() as cursor:
        cursor.execute(
            'SELECT titulo_pelicula, nick_propietario, alquiler_inicio, alquiler_fin, tipo_alquiler FROM Alquiler WHERE titulo_pelicula = %s AND nick_propietario = %s',
            (title, owner))
        rental = cursor.fetchone()
    connection.close()
    return rental


def update_rental(title, owner, start, end, type_query):
    connection = get_connection()
    with connection.cursor() as cursor:
        cursor.execute(
            'UPDATE Alquiler SET alquiler_inicio = %s, alquiler_fin = %s, tipo_alquiler = %s WHERE titulo_pelicula = %s AND nick_propietario = %s',
            (start, end, type_query, title, owner))
