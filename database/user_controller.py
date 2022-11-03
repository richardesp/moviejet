from database.get_connection import get_connection


def get_users():
    connection = get_connection()
    with connection.cursor() as cursor:
        cursor.execute('SELECT nick, email, nombre_y_apellidos FROM Usuario')
        users = cursor.fetchall()
    connection.close()
    return users


def insert_user(nick, email, full_name):
    connection = get_connection()
    with connection.cursor() as cursor:
        cursor.execute('INSERT INTO Usuario (nick, email, nombre_y_apellidos) VALUES (%s, %s, %s)',
                       (nick, email, full_name))


def delete_user(nick):
    connection = get_connection()
    with connection.cursor() as cursor:
        cursor.execute('DELETE FROM Usuario WHERE nick = %s', (nick,))


def get_user_by_nick(nick):
    connection = get_connection()
    with connection.cursor() as cursor:
        cursor.execute('SELECT nick, email, nombre_y_apellidos FROM Usuario WHERE nick = %s', (nick,))
        user = cursor.fetchone()
    connection.close()
    return user


def update_user(nick, email, full_name):
    connection = get_connection()
    with connection.cursor() as cursor:
        cursor.execute('UPDATE Usuario SET email = %s, nombre_y_apellidos = %s WHERE nick = %s',
                       (email, full_name, nick))
