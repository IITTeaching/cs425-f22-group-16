# Group 16
### Allysa, Xavier, Eric

#### [ER-Diagram](https://github.com/IITTeaching/cs425-f22-group-16/blob/30eee1f99cd71f7d8c14084af92f617b34d6b3c9/ER-Diagram)

#### [Relational Data Model](https://github.com/IITTeaching/cs425-f22-group-16/blob/5b94079072f04ed48ae7a360377b9e095324c9e5/Relational%20Data%20Model&DDL_Script/RDM.drawio.pdf)

#### [DDL Script](https://github.com/IITTeaching/cs425-f22-group-16/blob/5b94079072f04ed48ae7a360377b9e095324c9e5/Relational%20Data%20Model&DDL_Script/Script-3.sql)

#### [App](https://github.com/IITTeaching/cs425-f22-group-16/tree/master/App)

### We created our web app using the Flask web framework in Python.

## PRIOR TO USING APP:
##### The app login functionality will not work without some already existing data in the database. Therefore, here are some SQL queries to get started:
    
    INSERT INTO branch VALUES ('B01','IL', 'Chicago', 60411);
    INSERT INTO branch VALUES ('B02','IL', 'Chicago', 60411);
    INSERT INTO branch VALUES ('B03','IL', 'Chicago', 60411);
    
    INSERT INTO manager VALUES (789451592, 'B01', 'Ryan Google', 'IL', 'Chicago', 60411, 34500);
    INSERT INTO manager VALUES (360451590, 'B02', 'Elon Wesley', 'IL', 'Chicago', 60411, 45000);
    
    INSERT INTO teller VALUES (364515492, 'B03', 'Anthony Meta', 'IL', 'City', 60411, 54500.00, '1');
    INSERT INTO teller VALUES (387515490, 'B03', 'Robby William', 'IL', 'City', 60411, 56500.00, '2');
    
    INSERT INTO account VALUES (123, 'savings', 4562.00, 0.08);
    INSERT INTO account VALUES (456, 'checkings', 5693.00, 0.09);
    INSERT INTO account VALUES (789, 'checkings', 1950.00, 0.05);
    
    INSERT INTO customer VALUES ('C0835', 'Eric Zacarias', 'IL', 'Chicago', 60411, 45000.00);
    INSERT INTO customer VALUES ('C0836', 'Sally Rad', 'IL', 'Chicago', 60411, 50500.00);
    INSERT INTO customer VALUES ('C0842', 'John Doe', 'IL', 'Chicago Heights', 60411, 65240.00);
    
    INSERT INTO hasaccount VALUES ('C0835', 123);
    INSERT INTO hasaccount VALUES ('C0836', 456);
    INSERT INTO hasaccount VALUES ('C0842', 789);
    
    INSERT INTO usesbranch VALUES ('C0835', 'B01');
    INSERT INTO usesbranch VALUES ('C0836', 'B02');
    INSERT INTO usesbranch VALUES ('C0842', 'B03');
    
# HOW TO USE:
## Login In Page:
  #### - To Login as a Manager/Teller: 
         - Username: admin
         - Password: iit2022
         Once logged in, you have the option to click on 'Teller' or 'Manager' or 'Add a Branch'
  #### - To Login in as customer:
         - Username: <Enter an Existing Customer ID in the database>
         - Password: customer
## If logged in as manager:
  #### Click on the avaiable manager accounts you want to login as.
  #### This brings up the manager console where you can do the following:
    - Add A Customer
      - Fill in the fields, select a branch and submit.
    - Add A Teller
      - Fill in the fields, and submit.
    - Manage A Customer (View Account, Update, Delete, Open Bank Account)
      - Select an ID from the dropdown list.
      - Once selected, hit submit. You'll now have the option to view the customers accounts, delete the customer account (and their accounts),
        open an account or update the customer account.
    - Manage Teller
      - Choose a teller from the dropdown list and submit.
      - After choosing a teller, you have to option to delete the teller account or update the teller account.
    - Transaction Functions
       - Choose an account(s) to deposit, withdrawal, or transfer to (including external transfer).
    - Bank Analytics
       - scroll all the way down to select some of the analytics options we have available.

## If logged in as teller:
  #### Click on the account you want to login as.
  #### This brings up the teller console where you can do the following:
    - Add A Customer
      - Fill in the fields, select a branch and submit.
    - Manage A Customer (View Account, Update, Delete, Open Bank Account)
      - Enter in an existing customer ID in the text field and submit
      - You'll now have the option to view the customers accounts, delete the customer account (and their bank accounts),
        open an account or update the customer account.
    - Transaction Functions
       - Choose an account(s) from the dropdown menu to deposit, withdrawal, or transfer to (including external transfer).
    - Update Teller Account
      - Update the corresponding teller account
 
## If Logged In As A Customer:
  #### After loggin in, you are directed to the customer console page. Where you can do the following:
    - Click on 'My Accounts' to
      - View or delete your bank accounts.
    - Click on 'Statements' to
      - View the statements
    - Transaction function
      - Click on 'Deposit', 'Withdrawal', or 'Transfer' to perform either one of those transaction functions. Make sure to select an account from the dropdown menu.
    - Click on 'External Transfer' to perform an external transfer
      - Choose accounts from the dropdown menu.
    - Click on 'Update Account Info' to:
      - View your customer account info
      - Or to update your account info.
      
