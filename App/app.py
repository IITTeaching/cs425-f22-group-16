from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import psycopg2

app = Flask(__name__)

connection = {
    'dbname': 'bank',
    'user': 'postgres',
    'host': '127.0.0.1',
    'password': 'group16IIT',
    'port': 5432
    }


def updateTable(table, query, values):
    try:
        conn = psycopg2.connect(**connection)
        cur = conn.cursor()
        cur.execute(query, values)
        conn.commit()
        count = cur.rowcount
        print(count, "Record inserted successfully into " + table + " table")
        cur.close()
        conn.close()
    except (Exception, psycopg2.Error) as error:
        print("Failed to insert record into " + table + " table:", error)
    

def fetchFromTable(table, query):
    try:
        conn = psycopg2.connect(**connection)
        cur = conn.cursor()
        cur.execute(query)
        data = cur.fetchall()
        count = cur.rowcount
        print(count, "Records successfully fetched from " + table + " table")
        cur.close()
        conn.close()
        return data
    except (Exception, psycopg2.Error) as error:
        print("Failed to fetch record from " + table + " table:", error)
    
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'admin' and password == 'iit2022':
            return render_template('admin.html')
        else:
            return render_template('login.html')

@app.route('/teller_home', methods=['POST'])
def tellerHome():
    table = 'teller'
    query = """SELECT ssn::varchar, name FROM teller"""
    data = fetchFromTable(table, query)
    return render_template('teller_home.html', data=data)

@app.route('/manager_home', methods=['POST'])
def managerHome():
    table = 'manager'
    query = """SELECT ssn::varchar, name FROM manager"""
    data = fetchFromTable(table, query)
    return render_template('manager_home.html', data=data)

@app.route('/manager_console', methods=['POST'])
def managerConsole():
    ssn = request.form['ssn']
    table = 'manager'
    query = """SELECT * FROM manager WHERE ssn=""" + ssn
    data = fetchFromTable(table, query)
    name = data[0][2]
    return render_template('manager_console.html', data=data, name=name)

if __name__ == '__main__':
    app.debug = True
    app.run()