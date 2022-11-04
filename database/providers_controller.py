from database.get_connection import get_connection


def get_providers():
    connection = get_connection()
    with connection.cursor() as cursor:
        cursor.execute('SELECT empresa, NIF, telefono FROM Proveedor')
        providers = cursor.fetchall()
    connection.close()
    return providers


def insert_provider(company, NIF, phone):
    connection = get_connection()
    with connection.cursor() as cursor:
        cursor.execute('INSERT INTO Proveedor (empresa, NIF, telefono) VALUES (%s, %s, %s)',
                       (company, NIF, phone))


def delete_provider(company):
    connection = get_connection()
    with connection.cursor() as cursor:
        cursor.execute('DELETE FROM Proveedor WHERE empresa = %s', (company,))


def get_provider_by_company(company):
    connection = get_connection()
    with connection.cursor() as cursor:
        cursor.execute('SELECT empresa, NIF, telefono FROM Proveedor WHERE empresa = %s', (company,))
        provider = cursor.fetchone()
    connection.close()
    return provider


def update_provider(company, NIF, phone):
    connection = get_connection()
    with connection.cursor() as cursor:
        cursor.execute('UPDATE Proveedor SET NIF = %s, telefono = %s WHERE empresa = %s',
                       (NIF, phone, company))
