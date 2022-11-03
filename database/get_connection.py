import pymysql
from flask import Flask

app = Flask(__name__)
app.config.from_pyfile("../config/config.py")


def get_connection():
    return pymysql.connect(host=app.config['FLASK_DATABASE_HOST'],
                           user=app.config['FLASK_DATABASE_USER'],
                           password=app.config['FLASK_DATABASE_PASSWORD'],
                           db=app.config['FLASK_DATABASE'], )
