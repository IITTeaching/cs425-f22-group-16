from flask import Flask, render_template, request, redirect, url_for
import ast
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
        elif password == 'customer':
            table = 'customer'
            query = f"""SELECT * FROM customer where c_id = '{username}'"""
            data = fetchFromTable(table, query)
            if len(data) > 0:
                data = [str(x).strip() for x in data[0]]
                name = data[1]
                return render_template('customer_console.html', name=name, data=data)
            return "<h1>Incorrect Login Credentials Provided</h1>"

#A route to the teller home page.
@app.route('/teller_home', methods=['POST'])
def tellerHome():
    table = 'teller'
    query = """SELECT ssn::varchar, name FROM teller"""
    data = fetchFromTable(table, query)
    return render_template('teller_home.html', data=data)

@app.route('/teller_console', methods = ['POST'])
def tellerConsole():
    SSN = request.form['ssn']
    table = 'teller_console'
    query = f"""SELECT name FROM teller WHERE ssn = '{SSN}'"""
    name = fetchFromTable(table, query)
    if name is not None:
        return render_template('teller_console.html', name=name[0][0])

@app.route('/teller_process', methods = ['POST', 'GET'])
def tellerProcess():
    return "TODO"
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

@app.route('/customer_process/<name>/<data>', methods=['POST', 'GET'])
def customerProcess(name,data):
    if isinstance(data,str):
        customerData = ast.literal_eval(data)
    customerAction = False
    myAccounts = False
    statements = False
    deposit = False
    withdrawal = False
    transfer = False
    externalTransfer = False
    updateAccount = False

    if request.form.get('button', None) is not None:
        customerAction = True
        print("Intial Customer Action detected")
    if request.form.get('myAccounts', None) is not None:
        myAccounts = True
    if request.form.get('statements', None) is not None:
        statements = True
    if request.form.get('deposit', None) is not None:
        deposit = True 
    if request.form.get('withdraw', None) is not None:
        withdrawal = True 
    if request.form.get('transfer', None) is not None:
        transfer = True 
    if request.form.get('externalTransfer', None) is not None:
        externalTransfer = True
    if request.form.get('updateAccount', None) is not None:
        updateAccount = True
    
    if customerAction:
        process = request.form['button']
        if process == 'My Accounts':
            table = "hasaccount"
            c_id = customerData[0]
            query = f"""SELECT acc_id::int FROM hasaccount WHERE c_id='{c_id}'"""
            customerAccounts = fetchFromTable(table, query)
            if len(customerAccounts) > 0:
                acc_id = customerAccounts[0][0]
                table = 'account'
                lst =[]
                for i in range(0, len(customerAccounts)):
                    query = f"""SELECT * FROM account WHERE acc_id='{customerAccounts[i][0]}'"""
                    allAccs = fetchFromTable(table, query)
                    j = 0
                    for x in allAccs:
                        allAccs = [str(i).strip() for i in x]
                        lst.append(allAccs)
                print(lst)
                headings = ("Account ID: ", "Account Type: ", "Balance: $", "Interest Rate: ")
                return render_template('customer_bank_accs.html', data=lst, headings=headings)
        if process == 'Statements':
            return "<h1>TODO</h1>"
            #return render_template('customer_statements.html', name=name)
        if process == 'Deposit':
            table = "hasaccount"
            c_id = customerData[0]
            query = f"""SELECT acc_id::int FROM hasaccount WHERE c_id='{c_id}'"""
            accIDs = fetchFromTable(table, query)
            if len(accIDs) > 0:
                accIDs = [id[0] for id in accIDs]
                accTypes = []
                table = 'account'
                for i in range(0,len(accIDs)):
                    query = f"""SELECT acc_type FROM account WHERE acc_id='{accIDs[i]}'"""
                    accType = fetchFromTable(table, query)
                    print(accType)
                    if len(accType) > 0:
                        accTypes.append(accType[0][0].strip().capitalize())
                return render_template('customer_deposit.html', accIDs=accIDs, accTypes=accTypes, name=name, data=customerData)
        if process == 'Withdrawal':
            table = "hasaccount"
            c_id = customerData[0]
            query = f"""SELECT acc_id::int FROM hasaccount WHERE c_id='{c_id}'"""
            accIDs = fetchFromTable(table, query)
            if len(accIDs) > 0:
                accIDs = [id[0] for id in accIDs]
                accTypes = []
                table = 'account'
                for i in range(0,len(accIDs)):
                    query = f"""SELECT acc_type FROM account WHERE acc_id='{accIDs[i]}'"""
                    accType = fetchFromTable(table, query)
                    if len(accType) > 0:
                        accTypes.append(accType[0][0].strip().capitalize())
                return render_template('customer_wthdrwl.html', accIDs=accIDs, accTypes=accTypes, name=name, data=customerData)
        if process == 'Transfer':
            table = "hasaccount"
            c_id = customerData[0]
            query = f"""SELECT acc_id::int FROM hasaccount WHERE c_id='{c_id}'"""
            accIDs = fetchFromTable(table, query)
            if len(accIDs) > 0:
                accIDs = [id[0] for id in accIDs]
                accTypes = []
                table = 'account'
                for i in range(0,len(accIDs)):
                    query = f"""SELECT acc_type FROM account WHERE acc_id='{accIDs[i]}'"""
                    accType = fetchFromTable(table, query)
                    if len(accType) > 0:
                        accTypes.append(accType[0][0].strip().capitalize())
                return render_template('customer_transfer.html', accIDs=accIDs, accTypes=accTypes, name=name, data=customerData)
        if process == 'External Transfer':
            return "<h1>TODO</h1>"
        if process == 'Update Account Info':
            table = 'customer'
            query = f"""SELECT * FROM customer where c_id = '{customerData[0]}'"""
            cInfo = fetchFromTable(table, query)
            if len(cInfo) > 0:
                 cInfo = [str(x).strip() for x in cInfo[0]] #This is basically taking a list with format [(x),(y),(z)] and changing it to [x, y, z] while also removing any existing whitespace.
                 headings = ("Customer ID", "Name", "State", "City", "Zip Code", "Salary")
                 return render_template('customer_account.html', name=name, cInfo=cInfo, headings=headings, data=customerData)
            else:
                return "HELLO"
                #TODO: Return false html here
    if statements:
        return "TODO"
        #Use timestamps
    if deposit:
        accID = request.form['account']
        amount = request.form['depositAmount']
        table = 'account'
        query = """UPDATE account SET balance = balance + (%s) WHERE acc_id = (%s)"""
        values = (float(amount), str(accID))
        print(values)
        updateAcc = updateTable(table, query, values)
        if updateAcc > 0:
            return render_template('success_cust.html', name=name, data=customerData)
    if withdrawal:
        accID = request.form['account']
        amount = request.form['withdrawAmount']
        table = 'account'
        query = """UPDATE account SET balance = balance - (%s) WHERE acc_id = (%s)"""
        values = (float(amount), str(accID))
        updateAcc = updateTable(table, query, values)
        if updateAcc > 0:
            return render_template('success_cust.html', name=name, data=customerData)
    if transfer:
        fromAcc = request.form['accountFrom']
        toAcc = request.form['accountTo']
        amount = request.form['transferAmount']
        table = 'account'
        queryOne = """UPDATE account SET balance = balance - (%s) WHERE acc_id = (%s)"""
        queryTwo = """UPDATE account SET balance = balance + (%s) WHERE acc_id = (%s)"""
        valuesOne = (float(amount), str(fromAcc))
        valuesTwo = (float(amount), str(toAcc))
        if fromAcc != toAcc:
            updateFromAcc = updateTable(table, queryOne, valuesOne)
            updateToAcc = updateTable(table, queryTwo, valuesTwo)
            if updateFromAcc > 0 and updateToAcc > 0:
                return render_template('success_cust.html', name=name, data=customerData)
    if externalTransfer:
        return
    if updateAccount:
        state = request.form['state']
        city = request.form['city']
        zip = request.form['zipcode']
        table = "customer"
        query = """UPDATE customer SET state = (%s), city = (%s), zip_code = (%s) WHERE c_id = (%s)"""
        values = (state, city, zip, customerData[0])
        updateCustomer = updateTable(table, query, values)
        return "SUCCESS"
    return render_template('customer_console.html', name=name, data=customerData)

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
    manageTeller = False
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
    if request.form.get('manageTeller', None) is not None:
        manageTeller = True 
        print("Manage Teller process deteced.")
    if request.form.get('analytic', None) is not None:
        analytics = True 
        print("Analytics process deteced.")

    #This is only true when the manager clicks on a button inside of the manager console.
    if managerAction:
        process = request.form['button']
        if process == 'Add Customer':
            return render_template('add_customer.html', name=managerName)
        if process == 'Add Teller':
            return render_template('add_teller.html', name=managerName)
        if process == 'Manage Customer':
            return render_template('manage_customer.html', name=managerName)
        if process == 'Manage Teller':
            return render_template('manage_teller.html',name=managerName)
        if process == 'Analytics':
            return render_template('analytics.html', name=managerName)

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
        if len(data) > 0:
            data = [str(x).strip() for x in data[0]] #This is basically taking a list with format [(x),(y),(z)] and changing it to [x, y, z] while also removing any existing whitespace.
            headings = ("Customer ID", "Name", "State", "City", "Zip Code", "Salary")
            return render_template('manager_cinfo.html', data=data, headings=headings)
        else:
            return render_template('fail.html', name= managerName)
    if manageTeller:
        t_id =request.form['t_id']
        table = 'teller'
        query = f"""SELECT * FROM teller where ssn = '{t_id}'"""
        data = fetchFromTable(table, query)

        if len(data) > 0:
            data = [str(x).strip() for x in data[0]] #This is basically taking a list with format [(x),(y),(z)] and changing it to [x, y, z] while also removing any existing whitespace.
            headings = ("Teller ID", "Branch ID", "Name", "State", "City", "Zip Code", "Salary")
            return render_template('manager_tinfo.html', data=data, headings=headings)
        else:
            return render_template('fail.html', name= managerName)
    if analytics:
        analyticOption = request.form['analytic']
        print("Analytics is true")
        return "Chose option: " + str(analyticOption)
    return render_template('manager_console.html', mName=managerName)

#Run the app
if __name__ == '__main__':
    app.debug = True
    app.run()
