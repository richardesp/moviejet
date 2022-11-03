from flask import Flask
from database.get_connection import get_connection
from schema.records import instructions

app = Flask(__name__)
app.config.from_pyfile("../config/config.py")


def insert_db():
    connection = get_connection()
    with connection.cursor() as cursor:
        for instruction in instructions:
            cursor.execute(instruction)
    connection.commit()
    connection.close()
