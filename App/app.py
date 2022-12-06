from flask import Flask, render_template, request, redirect, url_for
import ast
import psycopg2
import random


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
def deleteFromTable(table, query):
    try:
        #This code below is inspired from the examples professor provided us
        conn = psycopg2.connect(**connection) 
        cur = conn.cursor()
        cur.execute(query)
        conn.commit()
        count = cur.rowcount
        print(count, "Record successfully deleted from " + table + " table")
        cur.close()
        conn.close()
        return count
    except (Exception, psycopg2.Error) as error:
        print("Failed to delete record into " + table + " table:", error)

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
        if request.form.get('username', None) is not None and request.form.get('password', None) is not None:
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
        if request.form.get('addBranch', None) is not None:
            print("INSIDE branch")
            return addBranch()
        return "<h1>Incorrect Login Credentials Provided</h1>"
@app.route('/add_branch', methods=['POST', 'GET'])
def addBranch():
    b_id = request.form['b_id']
    state = request.form['state']
    city = request.form['city']
    zip = request.form['zipcode']
    table = 'branch'
    query = f"""SELECT * FROM branch WHERE branch_id = '{b_id}'"""
    branchExists = fetchFromTable(table, query)
    if len(branchExists) == 0:
        query = """INSERT INTO branch VALUES (%s,%s,%s,%s)"""
        values = (b_id, state, city, zip)
        updateBranch = updateTable(table, query, values)
        if updateBranch:
            return "<h1>SUCCESS. GO BACK TO CONTINUE</h1>"
        else:
            return "<h1>FAILED. GO BACK TO TRY AGAIN</h1>"
    else:
        return "<h1>BRANCH ALREADY EXISTS. GO BACK TO CONTINUE. </h1>"
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
    query = f"""SELECT name,ssn FROM teller WHERE ssn = '{SSN}'"""

    tableA = "hasaccount, usesbranch"
    queryA = """SELECT acc_id::int, branch_id FROM hasaccount AS ha, usesbranch AS ub WHERE ha.c_id = ub.c_id"""
    accounts = fetchFromTable(tableA, queryA)
    name = fetchFromTable(table, query)
    if name:
        return render_template('teller_console.html', name=name[0][0], ssn=SSN, accounts=accounts)

@app.route('/teller_process/<name>/<ssn>', methods = ['POST', 'GET'])
def tellerProcess(name, ssn):
    tellerAction = False
    updateAccount = False
    openAccount = False
    deleteCustomer = False
    addCustomer = False
    if request.form.get('button', None) is not None:
        tellerAction = True
    if request.form.get('updateAccount', None) is not None:
        updateAccount = True
    if request.form.get('openAccount', None) is not None:
        openAccount = True
    if request.form.get('deleteCustomer', None) is not None:
        deleteCustomer = True
    if request.form.get('addCustomer', None) is not None:
        addCustomer = True
    if tellerAction:
        process = request.form['button']
        if process == 'Manage Customer':
            c_id = request.form['c_id']
            table = 'customer'
            print("CID IS", c_id)
            query = f"""SELECT * FROM customer WHERE c_id='{c_id}'"""
            cInfo = fetchFromTable(table, query)
            if cInfo:
                cInfo = [str(x).strip() for x in cInfo[0]] #This is basically taking a list with format [(x),(y),(z)] and changing it to [x, y, z] while also removing any existing whitespace.
                table = "hasaccount"
                query = f"""SELECT acc_id::int FROM hasaccount WHERE c_id='{c_id}'"""
                customerAccounts = fetchFromTable(table, query)
                if customerAccounts:
                    acc_ids = [id[0] for id in customerAccounts]
                    table = 'account'
                    lst = []
                    for i in range(0, len(customerAccounts)):
                        query = f"""SELECT * FROM account WHERE acc_id='{acc_ids[i]}'"""
                        acc = fetchFromTable(table, query)
                        j = 0
                        for x in acc:
                            acc = [str(i).strip() for i in x]
                            lst.append(acc)
                headings = ("Customer ID", "Name", "State", "City", "Zip Code", "Salary")
                headingsTwo = ("Account ID: ", "Account Type: ", "Balance: $", "Interest Rate: ")
                return render_template('teller_cinfo.html', name=name, ssn=ssn, cInfo=cInfo, headings=headings, headingsTwo=headingsTwo, data=lst)
            else:
                return "<h1>FAILED! CUSTOMER MAY HAVE BEEN DELETED OR DOES NOT EXIST. GO BACK TO TRY AGAIN.</h1>"
        if process == 'Add Customer':
            table = 'branch'
            query = """SELECT branch_id FROM branch"""
            branches = fetchFromTable(table, query)
            branches = [b[0] for b in branches]
            return render_template('teller_addcustomer.html', name=name, ssn=ssn, branches=branches)
        if process == 'Deposit':
            accID = request.form['accID']
            amount = request.form['amount']
            if float(amount) < 0:
                return "<h1> WITHDRAWAL AMOUNT CANNOT BE NEGATIVE. TRY AGAIN."
            if accID and amount:
                table = 'customer'
                query = f"""SELECT * FROM account WHERE acc_id = '{accID}'"""
                customer = fetchFromTable(table, query)
                if customer:
                    table = 'account'
                    query = """UPDATE account SET balance = balance + (%s) WHERE acc_id = (%s)"""
                    values = (amount, accID)
                    updateAcc = updateTable(table, query, values)
                    if updateAcc:
                        return "<h1>SUCCESS! GO BACK TO PERFORM MORE ACTIONS</h1>"
                    else:
                        return "<h1>FAILED! GO BACK TO TRY AGAIN</h1>"
            else:
                return "<h1>FAILED! GO BACK TO TRY AGAIN</h1>"
        if process == 'Withdrawal':
            accID = request.form['accIDW']
            amount = request.form['amountW']
            if float(amount) < 0:
                return "<h1> WITHDRAWAL AMOUNT CANNOT BE NEGATIVE. TRY AGAIN."
            if accID and amount:
                table = 'customer'
                query = f"""SELECT * FROM account WHERE acc_id = '{accID}'"""
                customer = fetchFromTable(table, query)
                if customer:
                    table = 'account'
                    query = """UPDATE account SET balance = balance - (%s) WHERE acc_id = (%s)"""
                    values = (amount, accID)
                    updateAcc = updateTable(table, query, values)
                    if updateAcc:
                        return "<h1>SUCCESS! GO BACK TO PERFORM MORE ACTIONS</h1>"
                    else:
                        return "<h1>FAILED! GO BACK TO TRY AGAIN</h1>"
            else:
                return "<h1>FAILED! GO BACK TO TRY AGAIN</h1>"
        if process == 'Transfer':
            accIDFrom = request.form['accIDFrom']
            accIDTo = request.form['accIDTo']
            amount = request.form['amountTrans']
            if float(amount) < 0:
                return "<h1> WITHDRAWAL AMOUNT CANNOT BE NEGATIVE. TRY AGAIN."
            if accIDFrom and accIDTo and amount:
                if accIDFrom != accIDTo:
                    table = 'account'
                    queryFrom = """UPDATE account SET balance = balance - (%s) WHERE acc_id = (%s)"""
                    queryTo = """UPDATE account SET balance = balance + (%s) WHERE acc_id = (%s)"""
                    valuesFrom = (amount, accIDFrom)
                    valuesTo = (amount, accIDTo)
                    updateTo = updateTable(table, queryFrom, valuesFrom)
                    updateFrom = updateTable(table, queryTo, valuesTo)
                    if updateTo and updateFrom:
                        return "<h1>SUCCESS! GO BACK TO PERFORM MORE ACTIONS</h1>"
                    else:
                        return "<h1>FAIL! GO BACK TO TRY AGAIN</h1>"
                else:
                    return "<h1>FAIL! YOU CAN'T TRANSFER TO THE SAME ACCOUNT. GO BACK TO TRY AGAIN.</h1>"
            else:
                return "<h1>FAILED. GO BACK TO TRY AGAIN.</h1>"
        if process == 'Update My Account':
            table = 'teller'
            query = f"""SELECT * FROM teller where ssn = '{ssn}'"""
            tInfo = fetchFromTable(table, query)
            if tInfo:
                tInfo = [str(x).strip() for x in tInfo[0]] #This is basically taking a list with format [(x),(y),(z)] and changing it to [x, y, z] while also removing any existing whitespace.
                headings = ("SSN", "Branch ID", "Name", "State", "City", "Zip Code", "Salary", "Booth")
                return render_template('teller_info.html', name=name, ssn=ssn, tInfo=tInfo, headings=headings)
            else:
                return "<h1>FAILED</h1>"
        if process == 'Submit External Transfer':
            fromAcc = request.form['accIDFromExt'].replace('-', ' ').split()
            toAcc = request.form['accIDToExt'].replace('-', ' ').split()
            amount = request.form['amountExtTrans']
            if float(amount) < 0:
                return "<h1> WITHDRAWAL AMOUNT CANNOT BE NEGATIVE. TRY AGAIN."
            if fromAcc and toAcc and amount:
                if fromAcc[0] != toAcc[0] and fromAcc[1] != toAcc[1]:
                    table = 'account'
                    queryFrom = """UPDATE account SET balance = balance - (%s) WHERE acc_id = (%s)"""
                    queryTo = """UPDATE account SET balance = balance + (%s) WHERE acc_id = (%s)"""
                    valuesFrom = (amount, fromAcc[0])
                    valuesTo = (amount, toAcc[0])
                    updateTo = updateTable(table, queryFrom, valuesFrom)
                    updateFrom = updateTable(table, queryTo, valuesTo)
                    if updateTo and updateFrom:
                        return "<h1>SUCCESS! GO BACK TO PERFORM MORE ACTIONS</h1>"
                    else:
                        return "<h1>FAILED! GO BACK TO TRY AGAIN</h1>"
                else:
                    return "<h1>FAILED! YOU MUST TRANSFER TO AN EXTERNAL ACCOUNT. GO BACK TO TRY AGAIN.</h1>"
            else:
                return "<h1>FAILED! GO BACK TO TRY AGAIN.</h1>"
    if updateAccount:
        print("IN UPDATE ACCOUNT")
        state = request.form['state']
        city = request.form['city']
        zip = request.form['zipcode']
        if state and city and zip:
            table = 'teller'
            query = """UPDATE teller SET state = (%s), city = (%s), zip_code = (%s) WHERE ssn = (%s)"""
            values = (state, city, zip, ssn)
            updateTeller = updateTable(table, query, values)
            if updateTeller:
                return "<h1>SUCCESS! GO BACK TO PERFORM MORE ACTIONS.</h1>"
            else: 
                return "<h1>FAILED! GO BACK AND TRY AGAIN.</h1>"
        else:
            return "<h1>FAILED! GO BACK AND TRY AGAIN.</h1>"
    if openAccount:
        print("INSIDE OPEN ACCOUNT")
        c_id = request.form['c_id']
        acc_type = request.form['acc_type']
        balance = request.form['balance']
        if float(balance) < 0:
            return "<h1> BALANCE CANNOT BE NEGATIVE. TRY AGAIN."
        int_rate = request.form['int_rate']
        table = 'account'
        
        queryMax = """SELECT MAX(acc_id) FROM account"""
        maxID = fetchFromTable(table, queryMax)
        acc_id = int(maxID[0][0]) + 1

        queryAccount = """INSERT INTO account VALUES (%s,%s,%s,%s)"""
        values = (acc_id, acc_type, balance, int_rate)
        addAccount = updateTable(table, queryAccount, values)
        if addAccount:
            table2 = 'hasaccount'
            query = """INSERT INTO hasaccount VALUES (%s, %s)"""
            values = (c_id, acc_id)
            addRelation = updateTable(table2, query, values)
            if addRelation:
                return "<h1>SUCCESS. GO BACK TO PERFORM MORE ACTIONS.</h1>"
            else:
                return "<h1>FAILED. GO BACK TO TRY AGAIN.</h1>"
        else:
            return "<h1>FAILED. GO BACK TO TRY AGAIN.</h1>"
    if deleteCustomer:
        print("INSIDE DELETE ACCOUNT")
        option = request.form['deleteCustomer']
        c_id = option.split('-')[1].strip()
        table = 'customer'
        query = f"""DELETE FROM customer WHERE c_id ='{c_id}'"""
        deleteCustomer = deleteFromTable(table, query)
        if deleteCustomer:
            return "<h1>SUCCESS! GO BACK TO PERFORM MORE ACTIONS.</h1>"
        else:
            return "<h1>FAILED! GO BACK TO TRY AGAIN.</h1>"
    if addCustomer:
        c_id = request.form['c_id']
        cname = request.form['name']
        state = request.form['state']
        city = request.form['city']
        zip_code = request.form['zip_code']
        salary = request.form['salary']
        branch = request.form['branch'].strip()
        print(branch)
        
        table = 'customer'
        query = """INSERT INTO customer VALUES (%s,%s,%s,%s,%s,%s)"""
        values = (str(c_id), str(cname), str(state), str(city), int(zip_code), int(salary))
        count = updateTable(table, query, values)
        if count:
            tableA = 'usesbranch'
            queryA = """INSERT INTO usesbranch VALUES (%s,%s)"""
            valuesA = (str(c_id), str(branch))
            addBranch = updateTable(tableA, queryA, valuesA)
            if addBranch:
                return "<h1>SUCCESS! GO BACK TO PERFORM MORE ACTIONS.</h1>"
            else:
                return "<h1>FAILED. THAT CUSTOMER MAY ALREADY EXIST! TRY AGAIN.</h1>"
        else:
            return "<h1>FAILED. THAT CUSTOMER MAY ALREADY EXIST! TRY AGAIN.</h1>"


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
                headings = ("Account ID: ", "Account Type: ", "Balance: $", "Interest Rate: ")
                return render_template('customer_bank_accs.html', data=lst, headings=headings, name=name, cInfo=customerData)
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
            table = 'usesbranch'
            queryB = f"""SELECT branch_id FROM usesbranch WHERE c_id = '{customerData[0]}'"""
            customerBranch = fetchFromTable(table, queryB)
            if customerBranch:
                tableA = "hasaccount, usesbranch"
                queryA = f"""SELECT acc_id::int FROM hasaccount AS ha, usesbranch AS ub WHERE ha.c_id = ub.c_id AND ha.c_id != '{customerData[0]}' AND branch_id != '{customerBranch[0][0]}'"""
                externalAccs = fetchFromTable(tableA, queryA)
            if externalAccs:
                table = "hasaccount"
                c_id = customerData[0]
                queryOne = f"""SELECT acc_id::int FROM hasaccount WHERE c_id='{c_id}'"""
                accIDs = fetchFromTable(table, queryOne)
                if accIDs:
                    accIDs = [id[0] for id in accIDs]
                    externalAccs = [id[0] for id in externalAccs]
                    return render_template('customer_ext_transfer.html', accIDs=accIDs, extAccsIDs=externalAccs, name=name, data=customerData)
        if process == 'Update Account Info':
            table = 'customer'
            query = f"""SELECT * FROM customer where c_id = '{customerData[0]}'"""
            cInfo = fetchFromTable(table, query)
            if cInfo:
                 cInfo = [str(x).strip() for x in cInfo[0]] #This is basically taking a list with format [(x),(y),(z)] and changing it to [x, y, z] while also removing any existing whitespace.
                 headings = ("Customer ID", "Name", "State", "City", "Zip Code", "Salary")
                 return render_template('customer_account.html', name=name, cInfo=cInfo, headings=headings, data=customerData)
            else:
                return "<h1>FAILED! GO BACK TO TRY AGAIN.</h1>"
    if statements:
        return "TODO"
        #Use timestamps
    if deposit:
        accID = request.form['account']
        amount = request.form['depositAmount']
        if float(amount) < 0:
            return "<h1> WITHDRAWAL AMOUNT CANNOT BE NEGATIVE. TRY AGAIN."
        table = 'account'
        query = """UPDATE account SET balance = balance + (%s) WHERE acc_id = (%s)"""
        values = (float(amount), str(accID))
        print(values)
        updateAcc = updateTable(table, query, values)
        if updateAcc:
            return render_template('success_cust.html', name=name, data=customerData)
        else:
            return "<h1>FAILED! GO BACK TO TRY AGAIN.</h1>"
    if withdrawal:
        accID = request.form['account']
        amount = request.form['withdrawAmount']
        if float(amount) < 0:
            return "<h1> WITHDRAWAL AMOUNT CANNOT BE NEGATIVE. TRY AGAIN."
        table = 'account'
        query = f"""SELECT balance FROM account WHERE acc_id = '{accID}'"""
        balance = fetchFromTable(table, query)
        if balance:
            if float(balance[0][0]) - float(amount) < 0:
                return "<h1>THE WITHDRAWAL AMOUNT IS MORE THAN YOUR AVAILABLE BALANCE. TRY AGAIN.</h1>" 
            else:
                query = """UPDATE account SET balance = balance - (%s) WHERE acc_id = (%s)"""
                values = (float(amount), str(accID))
                updateAcc = updateTable(table, query, values)
                if updateAcc:
                    return render_template('success_cust.html', name=name, data=customerData)
        else:
            return "<h1>FAILED! GO BACK TO TRY AGAIN.</h1>"
    if transfer:
        fromAcc = request.form['accountFrom']
        toAcc = request.form['accountTo']
        amount = request.form['transferAmount']
        if float(amount) < 0:
            return "<h1> WITHDRAWAL AMOUNT CANNOT BE NEGATIVE. TRY AGAIN."
        table = 'account'
        queryOne = """UPDATE account SET balance = balance - (%s) WHERE acc_id = (%s)"""
        queryTwo = """UPDATE account SET balance = balance + (%s) WHERE acc_id = (%s)"""
        valuesOne = (float(amount), str(fromAcc))
        valuesTwo = (float(amount), str(toAcc))
        queryThree = f"""SELECT balance FROM account WHERE acc_id = '{fromAcc}'"""
        balance = fetchFromTable(table, queryThree)
        if balance:
            if float(balance[0][0]) - float(amount) < 0:
                return "<h1>THE WITHDRAWAL AMOUNT IS MORE THAN YOUR AVAILABLE BALANCE. TRY AGAIN.</h1>"
            else:
                if fromAcc != toAcc:
                    updateFromAcc = updateTable(table, queryOne, valuesOne)
                    updateToAcc = updateTable(table, queryTwo, valuesTwo)
                    if updateFromAcc > 0 and updateToAcc > 0:
                        return render_template('success_cust.html', name=name, data=customerData)
                else:
                    return "<h1>FAILED! YOU CAN'T TRANSFER TO YOUR OWN ACCOUNT. TRY AGAIN.</h1>"
        else:
            return "<h1>FAILED! GO BACK TO TRY AGAIN.</h1>"
    if externalTransfer:
        fromAcc = request.form['accountFrom']
        toAcc = request.form['accountTo']
        amount = request.form['transferAmount']
        table = 'account'
        quertThree = f"""SELECT balance FROM account WHERE acc_id='{fromAcc}'"""
        balance = fetchFromTable(table, quertThree)
        if balance:
            if float(balance[0][0]) - float(amount) < 0:
                return "<h1>THE WITHDRAWAL AMOUNT IS MORE THAN YOUR AVAILABLE BALANCE. TRY AGAIN.</h1>"
            else:
                queryOne = """UPDATE account SET balance = balance - (%s) WHERE acc_id = (%s)"""
                queryTwo = """UPDATE account SET balance = balance + (%s) WHERE acc_id = (%s)"""
                valuesOne = (float(amount), fromAcc)
                valuesTwo = (float(amount), toAcc)
                updateFromAcc = updateTable(table, queryOne, valuesOne)
                updateToAcc = updateTable(table, queryTwo, valuesTwo)
                if updateFromAcc and updateToAcc:
                    return render_template('success_cust.html', name=name, data=customerData)
        else:
            return "<h1>FAILED! GO BACK TO TRY AGAIN.</h1>"
    if updateAccount:
        state = request.form['state']
        city = request.form['city']
        zip = request.form['zipcode']
        table = "customer"
        query = """UPDATE customer SET state = (%s), city = (%s), zip_code = (%s) WHERE c_id = (%s)"""
        values = (state, city, zip, customerData[0])
        updateCustomer = updateTable(table, query, values)
        if updateCustomer:
            return render_template('success_cust.html', name=name, data=customerData)
        else:
            return "<h1>FAILED! GO BACK TO TRY AGAIN.</h1>"
    if myAccounts:
        print("INSIDE IF")
        accID = request.form['myAccounts']
        if accID:
            accID = accID.replace('-', ' ')
            accID = [s for s in accID.split() if s.isdigit()]
            table = 'hasaccount'
            tableTwo = 'account'
            query = f"""DELETE FROM hasaccount WHERE acc_id = '{accID[0]}'"""
            queryTwo = f"""DELETE FROM account WHERE acc_id = '{accID[0]}'"""
            deleteHA = deleteFromTable(table,query)
            deleteAcc = deleteFromTable(tableTwo, queryTwo)
            if deleteHA and deleteAcc:
                return render_template('success_cust.html', name=name, data=customerData)
            else:
                return "<h1>FAILED! GO BACK TO TRY AGAIN."
        else:
            return "<h1>FAILED! GO BACK TO TRY AGAIN."
    return render_template('customer_console.html', name=name, data=customerData)

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
    tableA = 'hasaccount'
    queryA = """SELECT acc_id FROM hasaccount"""
    accs = fetchFromTable(tableA, queryA)
    accounts = [a[0] for a in accs]
    tableB = "hasaccount, usesbranch"
    queryB = """SELECT acc_id::int, branch_id FROM hasaccount AS ha, usesbranch AS ub WHERE ha.c_id = ub.c_id"""
    accs = fetchFromTable(tableB, queryB)
    return render_template('manager_console.html', mName=mName, accounts=accounts, accs=accs)
##This route/function is for when a manager clicks on button inside of the manager console.
## In here the following actions are handled:
## 1. Add Customer 
## 2. Add  Teller
## 3. Manage Customer
## 4. Manage Teller
## 5. Analytics
@app.route('/manager_process/<managerName>', methods=['POST', 'GET'])
def managerProcess(managerName):
    managerAction = False
    addCustomer = False
    addTeller = False
    manageCustomer = False
    manageTeller = False
    updateTeller = False
    updateCustomer = False
    openAccount = False
    analytics = False

    print("BACK AT TOP")

    if request.form.get('button', None) is not None:
        managerAction = True
    if request.form.get('addCustomer', None) is not None:
        addCustomer = True
    if request.form.get('addTeller', None) is not None:
        addTeller = True
    if request.form.get('manageCustomer', None) is not None:
        manageCustomer = True 
    if request.form.get('updateCustomer', None) is not None:
        updateCustomer = True 
    if request.form.get('openAccount', None) is not None:
        openAccount = True 
    if request.form.get('manageTeller', None) is not None:
        manageTeller = True 
    if request.form.get('updateTeller', None) is not None:
        updateTeller = True 
    if request.form.get('analytics', None) is not None:
        analytics = True 

    #This is only true when the manager clicks on a button inside of the manager console.
    if managerAction:
        process = request.form['button']
        if process == 'Add Customer':
            table = 'branch'
            query = """SELECT branch_id FROM branch"""
            branches = fetchFromTable(table, query)
            branches = [b[0] for b in branches]
            return render_template('add_customer.html', name=managerName, branches=branches)
        if process == 'Add Teller':
            return render_template('add_teller.html', name=managerName)
        if process == 'Manage Customer':
            table = 'customer'
            query = """SELECT c_id FROM customer"""
            cIDs = fetchFromTable(table, query)
            cIDs = [id[0] for id in cIDs]
            if cIDs:
                return render_template('manage_customer.html', name=managerName, cIDs=cIDs)
            return "<h1> FAILED! THERE MIGHT NOT BE CUSTOMERS AVAILABLE TO MANAGE. GO BACK TO TRY AGAIN."
        if process == 'Manage Teller':
            table = 'Teller'
            query = """SELECT name,ssn FROM teller"""
            tellers = fetchFromTable(table, query)
            if tellers:
                return render_template('manage_teller.html',name=managerName, tellers=tellers)
            else:
                return "<h1> FAILED! THERE MIGHT NOT BE TELLERS AVAILABLE TO MANAGE. GO BACK TO TRY AGAIN."
        if process == 'Deposit':
            accID = request.form['accID']
            amount = request.form['amount']
            if float(amount) < 0:
                return "<h1> WITHDRAWAL AMOUNT CANNOT BE NEGATIVE. TRY AGAIN."
            if accID and amount:
                table = 'customer'
                query = f"""SELECT * FROM account WHERE acc_id = '{accID}'"""
                customer = fetchFromTable(table, query)
                if customer:
                    table = 'account'
                    query = """UPDATE account SET balance = balance + (%s) WHERE acc_id = (%s)"""
                    values = (amount, accID)
                    updateAcc = updateTable(table, query, values)
                    if updateAcc:
                        return "<h1>SUCCESS. GO BACK TO PERFORM MORE ACTIONS.</h1>"
                    else:
                        return "<h1>FAILED. GO BACK TO TRY AGAIN.</h1>"
        if process == 'Withdrawal':
            accID = request.form['accIDW']
            amount = request.form['amountW']
            if float(amount) < 0:
                return "<h1> WITHDRAWAL AMOUNT CANNOT BE NEGATIVE. TRY AGAIN."
            table = 'account'
            query = f"""SELECT balance FROM account WHERE acc_id ='{accID}'"""
            balance = fetchFromTable(table, query)
            if balance:
                if float(balance[0][0]) - float(amount) < 0:
                    return "<h1>FAILED! WITHDRAWAL AMOUNT CAN'T BE MORE THAN AVAILABLE BALANCE</h1>" 
                else:
                    if accID and amount:
                        table = 'customer'
                        query = f"""SELECT * FROM account WHERE acc_id = '{accID}'"""
                        customer = fetchFromTable(table, query)
                        if customer:
                            table = 'account'
                            query = """UPDATE account SET balance = balance - (%s) WHERE acc_id = (%s)"""
                            values = (amount, accID)
                            updateAcc = updateTable(table, query, values)
                            if updateAcc:
                                return "<h1>SUCCESS! GO BACK TO PERFORM MORE ACTIONS.</h1>"
                            else:
                                return "<h1>FAILED! GO BACK TO TRY AGAIN.</h1>"
            else:
                return "<h1>FAILED! GO BACK TO TRY AGAIN.</h1>"
        if process == 'Transfer':
            print("Transfer")
            accIDFrom = request.form['accIDFrom']
            accIDTo = request.form['accIDTo']
            amount = request.form['amountTrans']
            if float(amount) < 0:
                return "<h1> WITHDRAWAL AMOUNT CANNOT BE NEGATIVE. TRY AGAIN."
            if accIDFrom and accIDTo and amount:
                table = 'account'
                queryBal = f"""SELECT balance FROM account WHERE acc_id='{accIDFrom}'"""
                balance = fetchFromTable(table, queryBal)
                if balance:
                    if float(balance[0][0]) - float(amount) < 0:
                        return "<h1>FAILED! THE TRANSFER AMOUNT IS MORE THAN THE AVAILABLE BALANCE. TRY AGAIN.</h1>" 
                    else:
                        table = 'customer'
                        queryOne = f"""SELECT * FROM account WHERE acc_id = '{accIDFrom}'"""
                        queryTwo = f"""SELECT * FROM account WHERE acc_id = '{accIDTo}'"""

                        customerOne = fetchFromTable(table, queryOne)
                        customerTwo = fetchFromTable(table, queryTwo)
                        if customerOne and customerTwo:
                            table = 'account'
                            queryFrom = """UPDATE account SET balance = balance - (%s) WHERE acc_id = (%s)"""
                            queryTo = """UPDATE account SET balance = balance + (%s) WHERE acc_id = (%s)"""
                            valuesFrom = (amount, accIDFrom)
                            valuesTo = (amount, accIDTo)
                            updateTo = updateTable(table, queryFrom, valuesFrom)
                            updateFrom = updateTable(table, queryTo, valuesTo)
                            if updateTo and updateFrom:
                                return "<h1>SUCCESS! GO BACK TO PERFORM MORE ACTIONS.</h1>"
                            else:
                                return "<h1>FAILED! GO BACK TO PERFORM MORE ACTIONS.</h1>"
            else:
                return "<h1>FAILED! GO BACK TO TRY AGAIN.</h1>"
        if process == "Submit External Transfer":
            fromAcc = request.form['accIDFromExt'].replace('-', ' ').split()
            toAcc = request.form['accIDToExt'].replace('-', ' ').split()
            amount = request.form['amountExtTrans']
            if float(amount) < 0:
                return "<h1> WITHDRAWAL AMOUNT CANNOT BE NEGATIVE. TRY AGAIN."
            elif fromAcc and toAcc and amount:
                if fromAcc[0] != toAcc[0] and fromAcc[1] != toAcc[1]:
                    table = 'account'
                    queryFrom = """UPDATE account SET balance = balance - (%s) WHERE acc_id = (%s)"""
                    queryTo = """UPDATE account SET balance = balance + (%s) WHERE acc_id = (%s)"""
                    valuesFrom = (amount, fromAcc[0])
                    valuesTo = (amount, toAcc[0])
                    updateTo = updateTable(table, queryFrom, valuesFrom)
                    updateFrom = updateTable(table, queryTo, valuesTo)
                    if updateTo and updateFrom:
                        return "<h1>SUCCESS! GO BACK TO PERFORM MORE ACTIONS.</h1>"
                    else:
                        return "<h1>FAILED! GO BACK TO TRY AGAIN.</h1>"
                else:
                    return "<h1>FAILED! YOU MUST TRANSFER TO AN EXTERNAL ACCOUNT. GO BACK TO TRY AGAIN.</h1>"
            else:
                return "<h1>FAILED! GO BACK TO TRY AGAIN.</h1>"
        if process == 'Analytics':
            return render_template('analytics.html', name=managerName)

    #This is only true when the manager adds a customer after filling out the customer information.
    if addCustomer:
        c_id = request.form['c_id']
        cname = request.form['name']
        state = request.form['state']
        city = request.form['city']
        zip_code = request.form['zip_code']
        salary = request.form['salary']
        branch = request.form['branch']

        
        table = 'customer'
        query = """INSERT INTO customer VALUES (%s,%s,%s,%s,%s,%s)"""
        values = (str(c_id), str(cname), str(state), str(city), int(zip_code), int(salary))
        count = updateTable(table, query, values)
        if count:
            table = 'usesbranch'
            query = """INSERT INTO usesbranch VALUES (%s,%s)"""
            values = (c_id, branch)
            addBranch = updateTable(table, query, values)
            if addBranch:
                return "<h1>SUCCESS! GO BACK TO PERFORM MORE ACTIONS.</h1>"
            else:
                return "<h1>FAILED. THAT CUSTOMER MAY ALREADY EXIST! TRY AGAIN.</h1>"
        else:
            return "<h1>FAILED. THAT CUSTOMER MAY ALREADY EXIST! TRY AGAIN.</h1>"
            
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
        if count:
            return "<h1>SUCCESS! GO BACK TO PERFORM MORE ACTIONS.</h1>"
        else:
            return "<h1>FAILED TO ADD TELLER. THE TELLER MAY ALREADY EXIST!  TRY AGAIN.</h1>"

    #This is only true when the manager searches a customer ID to manage that customer.
    if manageCustomer:
        c_id = request.form['c_id']
        table = 'customer'
        query = f"""SELECT * FROM customer WHERE c_id = '{c_id}'"""
        data = fetchFromTable(table, query)
        table = "hasaccount"
        query = f"""SELECT acc_id::int FROM hasaccount WHERE c_id='{c_id}'"""
        customerAccounts = fetchFromTable(table, query)
        if customerAccounts:
            acc_ids = [id[0] for id in customerAccounts]
            table = 'account'
            lst = []
            for i in range(0, len(customerAccounts)):
                query = f"""SELECT * FROM account WHERE acc_id='{acc_ids[i]}'"""
                acc = fetchFromTable(table, query)
                j = 0
                for x in acc:
                    acc = [str(i).strip() for i in x]
                    lst.append(acc)
            if data:
                data = [str(x).strip() for x in data[0]] #This is basically taking a list with format [(x),(y),(z)] and changing it to [x, y, z] while also removing any existing whitespace.
                headings = ("Customer ID", "Name", "State", "City", "Zip Code", "Salary")
                headingsTwo = ("Account ID: ", "Account Type: ", "Balance: $", "Interest Rate: ")
                return render_template('manager_cinfo.html', name=managerName, data=data, headings=headings, headingsTwo = headingsTwo, accs=lst)
            else:
                return "<h1>FAILED! GO BACK TO PERFORM MORE ACTIONS.</h1>"
        else:
            if data:
                data = [str(x).strip() for x in data[0]] #This is basically taking a list with format [(x),(y),(z)] and changing it to [x, y, z] while also removing any existing whitespace.
                headings = ("Customer ID", "Name", "State", "City", "Zip Code", "Salary")
                headingsTwo = ("")
                lst = []
                return render_template('manager_cinfo.html', name=managerName, data=data, headings=headings, headingsTwo = headingsTwo, accs=lst)
            else:
                return "<h1>FAILED! GO BACK TO TRY AGAIN.</h1>"
    if manageTeller:
        t_id =request.form['t_id']
        table = 'teller'
        query = f"""SELECT * FROM teller where ssn = '{t_id}'"""
        data = fetchFromTable(table, query)

        if data:
            data = [str(x).strip() for x in data[0]] #This is basically taking a list with format [(x),(y),(z)] and changing it to [x, y, z] while also removing any existing whitespace.
            headings = ("Teller ID", "Branch ID", "Name", "State", "City", "Zip Code", "Salary")
            return render_template('manager_tinfo.html', name=managerName, data=data, headings=headings)
        else:
            return "<h1>FAILED! GO BACK TO TRY AGAIN.</h1>"
    if updateTeller:
        option = request.form['updateTeller']
        if option:
            if option == 'Update':
                state = request.form['state']
                city = request.form['city']
                zipcode = request.form['zipcode']
                ssn = request.form['ssn']
                table = 'teller'
                query = """UPDATE teller SET state = (%s), city = (%s), zip_code = (%s) WHERE ssn = (%s)"""
                values = (state, city, zipcode, ssn) 
                updateTeller = updateTable(table, query, values)
                if updateTeller:
                    return "<h1>SUCCESS! GO BACK TO PERFORM MORE ACTIONS.</h1>"
                else:
                    return "<h1>FAILED! GO BACK TO TRY AGAIN.</h1>"
            else:
                string = request.form['updateTeller']
                ssn = [s for s in string.split() if s.isdigit()]
                table = 'teller'
                query = f"""DELETE FROM teller WHERE ssn ='{ssn[0]}'"""
                deleteTeller = deleteFromTable(table, query)
                if deleteTeller:
                    return "<h1>FAILED! GO BACK TO PERFORM MORE ACTIONS.</h1>"
                else:
                    return "<h1>FAILED! GO BACK TO TRY AGAIN.</h1>"
        return "<h1>FAILED! GO BACK TO TRY AGAIN.</h1>"
    if updateCustomer:
        option = request.form['updateCustomer']
        if option:
            if option == 'Update':
                state = request.form['state']
                city = request.form['city']
                zipcode = request.form['zipcode']
                c_id = request.form['c_id']
                table = 'customer'
                query = """UPDATE customer SET state = (%s), city = (%s), zip_code = (%s) WHERE c_id = (%s)"""
                values = (state, city, zipcode, c_id) 
                updateCustomer = updateTable(table, query, values)
                if updateCustomer:
                    return "<h1>SUCCESS! GO BACK TO PERFORM MORE ACTIONS.</h1>"
                else:
                    return "<h1>FAILED! GO BACK TO TRY AGAIN.</h1>"
            else:
                c_id = option.split('-')[1].strip()
                table = 'customer'
                query = f"""DELETE FROM customer WHERE c_id ='{c_id}'"""
                deleteCustomer = deleteFromTable(table, query)
                if deleteCustomer:
                    return "<h1>SUCCESS! GO BACK TO PERFORM MORE ACTIONS.</h1>"
                else:
                    return "<h1>FAILED! GO BACK TO TRY AGAIN.</h1>"
        return "<h1>FAILED! GO BACK TO TRY AGAIN.</h1>"
    if openAccount:
        print("INSIDE OPEN ACCOUNT")
        c_id = request.form['c_id']
        acc_type = request.form['acc_type']
        balance = request.form['balance']
        if float(balance) < 0:
            return "<h1> BALANCE CANNOT BE NEGATIVE. TRY AGAIN."
        int_rate = request.form['int_rate']
        table = 'account'
        
        queryMax = """SELECT MAX(acc_id) FROM account"""
        maxID = fetchFromTable(table, queryMax)
        acc_id = int(maxID[0][0]) + random.randint(1,11)

        queryAccount = """INSERT INTO account VALUES (%s,%s,%s,%s)"""
        values = (acc_id, acc_type, balance, int_rate)
        addAccount = updateTable(table, queryAccount, values)
        if addAccount:
            table2 = 'hasaccount'
            query = """INSERT INTO hasaccount VALUES (%s, %s)"""
            values = (c_id, acc_id)
            addRelation = updateTable(table2, query, values)
            if addRelation:
                return "<h1>SUCCESS! GO BACK TO PERFORM MORE ACTIONS.</h1>"
            else:
                return "<h1>FAILED! GO BACK TO TRY AGAIN.</h1>"
        else:
            return "<h1>FAILED. GO BACK TO TRY AGAIN.</h1>"
    if analytics:
        analyticOption = request.form['analytics']
        if analyticOption == 'Analyze Customer Average Salary Across All Branches':
            query = """SELECT cast(avg(salary) AS decimal(100,2)) FROM customer"""
            data = fetchFromTable('customer', query)
            return "<h1>Customer Average Salary Across All Branches: $" +  str(data[0][0]) + "</h1>"
        elif analyticOption == 'Analyze Customer Average Salary For Each Branch':
            query = """SELECT branch_id, cast(avg(salary) AS decimal(100,2)) FROM customer NATURAL JOIN usesbranch GROUP BY branch_id"""
            data = fetchFromTable('customer,usesbranch', query)
            return render_template("analytics.html", data=data, title="Customer Average Salary For Each Branch")
        elif analyticOption == 'Analyze Customer Average Interest Rate Across All Branches':
            query = """SELECT avg(int_rate) FROM account"""
            data = fetchFromTable('account', query)
            return "<h1>Customer Average Interest Rate Across All Branches: " +  str(round(data[0][0],2)) + "</h1>"
        elif analyticOption == 'Analyze Customer Average Interest Rate For Each Branch':
            query = """WITH c_avg_rate AS (SELECT branch_id, avg(int_rate) FROM account NATURAL JOIN customer NATURAL JOIN usesbranch NATURAL JOIN hasaccount GROUP BY branch_id)
                        SELECT branch.branch_id, avg FROM branch FULL OUTER JOIN c_avg_rate ON branch.branch_id=c_avg_rate.branch_id"""
            data = fetchFromTable('tables', query)
            return render_template('analytics.html', data=data, title="Customer Average Interest Rate For Each Branch")
        elif analyticOption == 'Analyze Branch Usage Statistics':
            query = """SELECT b.branch_id, count(c_id) FROM branch b JOIN usesbranch u ON b.branch_id = u.branch_id GROUP BY b.branch_id"""
            data = fetchFromTable('', query)
            return render_template('analytics.html', data=data, title ="Branch Usage Statistics (Branch : Customer Count)")
        elif analyticOption == 'Analyze Number of Transactions Per Branch':
            query = """WITH trans_acc AS (SELECT branch_id, count(trans_id) FROM transact NATURAL JOIN usesbranch NATURAL JOIN hasaccount GROUP BY branch_id)
                       SELECT branch.branch_id, count FROM branch FULL OUTER JOIN trans_acc ON branch.branch_id= trans_acc.branch_id"""
            data = fetchFromTable('', query)
            return render_template('analytics.html', data=data, title ="Number of Transactions Per Branch")
        elif analyticOption == 'Analyze Customers Eligible For A Fee (balance < $50.00)':
            query = """SELECT c_id, acc_id FROM customer NATURAL JOIN hasaccount NATURAL JOIN account WHERE (balance < 50.00)"""
            data = fetchFromTable('', query)
            return render_template('analytics.html', data=data, title="Customers Eligible For A Fee (C_ID : ACC_ID)")
        elif analyticOption == 'Analyze Total Balance For Each Customer Across All Accounts':
            query = """SELECT c_id, sum(balance) AS tot_am FROM customer NATURAL JOIN hasaccount NATURAL JOIN account GROUP BY c_id"""
            data = fetchFromTable('', query)
            return render_template('analytics.html', data=data, title ="Total Balance For Each Customer Across Their Accounts")
        return "Chose option: " + str(analyticOption)
    
    return render_template('manager_console.html', mName=managerName)

#Run the app
if __name__ == '__main__':
    app.debug = True
    app.run()
