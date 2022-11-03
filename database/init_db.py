from flask import Flask
from database.get_connection import get_connection
from schema.schema import instructions

app = Flask(__name__)
app.config.from_pyfile("../config/config.py")


def init_db():
    connection = get_connection()
    with connection.cursor() as cursor:
        for instruction in instructions:
            cursor.execute(instruction)
    connection.commit()
    connection.close()
