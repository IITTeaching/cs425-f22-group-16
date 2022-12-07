# Group 16
### Allysa, Xavier, Eric

#### [ER-Diagram](https://github.com/IITTeaching/cs425-f22-group-16/blob/30eee1f99cd71f7d8c14084af92f617b34d6b3c9/ER-Diagram)

#### [Relational Data Model](https://github.com/IITTeaching/cs425-f22-group-16/blob/5b94079072f04ed48ae7a360377b9e095324c9e5/Relational%20Data%20Model&DDL_Script/RDM.drawio.pdf)

#### [DDL Script](https://github.com/IITTeaching/cs425-f22-group-16/blob/5b94079072f04ed48ae7a360377b9e095324c9e5/Relational%20Data%20Model&DDL_Script/Script-3.sql)

#### [App](https://github.com/IITTeaching/cs425-f22-group-16/tree/master/App)

### We created our web app using the Flask web framework in Python.

### Both our app and database is hosted on a raspberry pi server here: http://192.168.0.116:5000/

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
  #### Click on the account you want to login as.
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
      
