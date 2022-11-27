from flask import Flask, render_template, request, redirect, url_for
import psycopg2

#We are using a Python library called Flask which is used to create web applications.
#We are also using a Python library called Psycopg2 which is used to access and query our database. 

#This creates an instance of our app.
app = Flask(__name__)  

#To be used to connect to our database using Psycopg2. This only works locally. 
connection = {
    'dbname': 'bank',
    'user': 'postgres',
    'host': '127.0.0.1',
    'password': 'group16IIT',
    'port': 5432
    }

#This function updates a table in the database.
def updateTable(table, query, values):
    try:
        #This code below is inspired from the examples professor provided us
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
    
#This function gets data from a table in the database
def fetchFromTable(table, query):
    try:
        conn = psycopg2.connect(**connection)
        cur = conn.cursor()
        cur.execute(query)
        data = cur.fetchall() #fetchall returns the result after the query. It returns a list of tuples, where each tuple represents a row [ (...), (...), etc]
        count = cur.rowcount
        print(count, "Records successfully fetched from " + table + " table")
        cur.close()
        conn.close()
        return data
    except (Exception, psycopg2.Error) as error:
        print("Failed to fetch record from " + table + " table:", error)

#This is a route for the home page.   
@app.route('/')
def index():
    return render_template('index.html')

#This is a route for the login page.
@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'admin' and password == 'iit2022':
            return render_template('admin.html')
        else:
            return render_template('login.html')

#A route to the teller home page.
@app.route('/teller_home', methods=['POST'])
def tellerHome():
    table = 'teller'
    query = """SELECT ssn::varchar, name FROM teller"""
    data = fetchFromTable(table, query)
    return render_template('teller_home.html', data=data)

#A route to the manager home page. Displays the available managers one can choose to login as
@app.route('/manager_home', methods=['POST'])
def managerHome():
    table = 'manager'
    query = """SELECT ssn::varchar, name FROM manager"""
    data = fetchFromTable(table, query)
    return render_template('manager_home.html', data=data)

#The manager console. Displays the actions available that a manager can take.
@app.route('/manager_console', methods=['POST', 'GET'])
def managerConsole():
    ssn = request.form['ssn']
    table = 'manager'
    query = """SELECT * FROM manager WHERE ssn=""" + ssn
    data = fetchFromTable(table, query)
    mName = data[0][2]
    return render_template('manager_console.html', mName=mName)


##This route/function is for when a manager clicks on button inside of the manager console.
## In here the following actions are handled:
## 1. Add Customer 
## 2. Add  Teller
## 3. Manage Customer
## 4. Manage Teller
## 5. Analytics
@app.route('/manager_process/<managerName>', methods=['POST'])
def managerProcess(managerName):
    managerAction = False
    addCustomer = False
    addTeller = False
    manageCustomer = False
    analytics = False

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
    if request.form.get('Analytics', None) is not None:
        analytics = True 
        print("Manage customer process deteced.")

    #This is only true when the manager clicks on a button inside of the manager console.
    if managerAction:
        process = request.form['button']
        if process == 'Add Customer':
            return render_template('add_customer.html', name=managerName)
        if process == 'Add Teller':
            return render_template('add_teller.html', name=managerName)
        if process == 'Manage Customer':
            return render_template('manage_customer.html', name=managerName)
        #TODO: Check if the process == 'Analytics' and return the HTML page. (HTML page needs to be created)

    #This is only true when the manager adds a customer after filling out the customer information.
    if addCustomer:
        print("IN ADD CUSTOMER")
        c_id = request.form['c_id']
        cname = request.form['name']
        state = request.form['state']
        city = request.form['city']
        zip_code = request.form['zip_code']
        salary = request.form['salary']
        print(c_id, cname, state, city, zip_code, salary)
        
        table = 'customer'
        query = """INSERT INTO customer VALUES (%s,%s,%s,%s,%s,%s)"""
        values = (str(c_id), str(cname), str(state), str(city), int(zip_code), int(salary))
        count = updateTable(table, query, values)
        if count > 0:
           return render_template('success.html', name=managerName)
    #This is only true when the manager adds a teller after filling out the teller information.
    if addTeller:
        ssn = request.form['ssn']
        branch_id = request.form['branch_id']
        tname = request.form['name']
        state = request.form['state']
        city = request.form['city']
        zip_code = request.form['zip_code']
        salary = request.form['salary']
        booth = request.form['booth']
        table = 'teller'
        query = """INSERT INTO teller VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"""
        values = (int(ssn), str(branch_id), str(tname), str(state), str(city), int(zip_code), int(salary), int(booth))
        count = updateTable(table, query, values)
        if count > 0:
            return render_template('success.html', name=managerName)
        else:
            #TODO: Create a HTML page that shows that the process failed. And return it here. 
            return "<h1>FAILED TO ADD TELLER</h2>"

    #This is only true when the manager searches a customer ID to manage that customer.
    if manageCustomer:
        c_id = request.form['c_id']
        table = 'customer'
        query = f"""SELECT * FROM customer where c_id = '{c_id}'"""
        data = fetchFromTable(table, query)
        if data is not None:
            data = [str(x).strip() for x in data[0]] #This is basically taking a list with format [(x),(y),(z)] and changing it to [x, y, z] while also removing any existing whitespace.
            headings = ("Customer ID", "Name", "State", "City", "Zip Code", "Salary")
            return render_template('manager_cinfo.html', data=data, headings=headings)
        else:
            #TODO: Create a HTML page that shows that the process failed. And return it here. 
            return "<h1>CUSTOMER DOES NOT EXIST.</h1>"
    #TODO: Create an if statement to check for the 'analytics' boolean variable being True here
    #If any of the if statements above are not true, then we just return back to manager console.
    return render_template('manager_console.html', mName=managerName)

#Run the app
if __name__ == '__main__':
    app.debug = True
    app.run()