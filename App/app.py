from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import psycopg2

app = Flask(__name__)

# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:m2O2aBz!@localhost/bank'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# db = SQLAlchemy(app)

connection = {
    'dbname': 'bank',
    'user': 'postgres',
    'host': '127.0.0.1',
    'password': '-----',
    'port': 5432
    }
conn = psycopg2.connect(**connection)

def executeQuery(table, query, values):
    try:
        cur = conn.cursor()
        cur.execute(query, values)
        conn.commit()
        count = cur.rowcount
        print(count, "Record inserted successfully into " + table + " table")
    except (Exception, psycopg2.Error) as error:
        print("Failed to insert record into " + table + " table:", error)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        table = "branch"
        query = """INSERT INTO branch (branch_id, state, city, zip_code) VALUES (%s, %s, %s, %s)"""
        values = ("B123", 'IL', 'Chicago', 60411)
        executeQuery(table, query, values)
        return render_template('login.html')
if __name__ == '__main__':
    app.debug = True
    app.run()