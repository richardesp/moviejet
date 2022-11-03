from flask import Flask
import pymysql

app = Flask(__name__)


def get_connection():
    return pymysql.connect(host='oraclepr.uco.es',
                           user='i92esper',
                           password='1234',
                           db='i92esper')

@app.route('/getSelect')
def get_select():
    connection = get_connection()
    with connection.cursor() as cursor:
        cursor.execute('SELECT * FROM prueba')
        result = cursor.fetchall()
    connection.close()
    return str(result)

@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


if __name__ == '__main__':
    app.run(debug=True)
