from flask import Flask, render_template, request, redirect, url_for
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
        return count
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

@app.route('/manager_console', methods=['POST', 'GET'])
def managerConsole():
    ssn = request.form['ssn']
    table = 'manager'
    query = """SELECT * FROM manager WHERE ssn=""" + ssn
    data = fetchFromTable(table, query)
    mName = data[0][2]
    return render_template('manager_console.html', mName=mName)

@app.route('/manager_process/<managerName>', methods=['POST'])
def managerProcess(managerName):
    managerAction = False
    addCustomer = False
    addTeller = False
    manageCustomer = False

    if request.form.get('button', None) is not None:
        managerAction = True
        print("Intial Action detected")
    if request.form.get('addCustomer', None) is not None:
        addCustomer = True
        print("add customer process detected")
    if request.form.get('addTeller', None) is not None:
        addTeller = True
        print("add teller process detected")
    if request.form.get('manageCustomer', None) is not None:
        manageCustomer = True 
        print("Manage customer process deteced.")
    if managerAction:
        process = request.form['button']
        if process == 'Add Customer':
            return render_template('add_customer.html', name=managerName)
        if process == 'Add Teller':
            return render_template('add_teller.html', name=managerName)
        if process == 'Manage Customer':
            return render_template('manage_customer.html', name=managerName)
    if addCustomer:
        c_id = request.form['c_id']
        cname = request.form['name']
        state = request.form['state']
        city = request.form['city']
        zip_code = request.form['zip_code']
        salary = request.form['salary']
        print(c_id, cname, state, city, zip_code, salary)
        print("IN ADD CUSTOMER")
        table = 'customer'
        query = """INSERT INTO customer VALUES (%s,%s,%s,%s,%s,%s)"""
        values = (str(c_id), str(cname), str(state), str(city), int(zip_code), int(salary))
        count = updateTable(table, query, values)
        if count > 0:
           return render_template('success.html', name=managerName)
    if addTeller:
        ssn = request.form['ssn']
        branch_id = request.form['branch_id']
        tname = request.form['name']
        state = request.form['state']
        city = request.form['city']
        zip_code = request.form['zip_code']
        salary = request.form['salary']
        booth = request.form['booth']
        #TODO: QUERY TO TELLER TABLE
    if manageCustomer:
        c_id = request.form['c_id']
        table = 'customer'
        query = f"""SELECT * FROM customer where c_id = '{c_id}'"""
        data = fetchFromTable(table, query)
        print(data)
        return "MANAGING CUSTOMER"
        #TODO: QUERY TO TELLER TABLE
    return render_template('manager_console.html', mName=managerName)


if __name__ == '__main__':
    app.debug = True
    app.run()