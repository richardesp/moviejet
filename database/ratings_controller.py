from database.get_connection import get_connection


def get_ratings():
    connection = get_connection()
    with connection.cursor() as cursor:
        cursor.execute('SELECT titulo_pelicula, puntuacion, comentario, nick_autor FROM Valoracion')
        ratings = cursor.fetchall()
    connection.close()
    return ratings


def insert_rating(title, score, comment, author):
    connection = get_connection()
    with connection.cursor() as cursor:
        cursor.execute(
            'INSERT INTO Valoracion (titulo_pelicula, puntuacion, comentario, nick_autor) VALUES (%s, %s, %s, %s)',
            (title, score, comment, author))


def delete_rating(title, author):
    connection = get_connection()
    with connection.cursor() as cursor:
        cursor.execute('DELETE FROM Valoracion WHERE titulo_pelicula = %s AND nick_autor = %s', (title, author))


def get_rating_by_title_and_author(title, author):
    connection = get_connection()
    with connection.cursor() as cursor:
        cursor.execute(
            'SELECT titulo_pelicula, puntuacion, comentario, nick_autor FROM Valoracion WHERE titulo_pelicula = %s AND nick_autor = %s',
            (title, author))
        rating = cursor.fetchone()
    connection.close()
    return rating


def update_rating(title, score, comment, author):
    connection = get_connection()
    with connection.cursor() as cursor:
        cursor.execute(
            'UPDATE Valoracion SET puntuacion = %s, comentario = %s WHERE titulo_pelicula = %s AND nick_autor = %s',
            (score, comment, title, author))
