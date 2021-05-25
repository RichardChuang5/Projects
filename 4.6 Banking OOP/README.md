**4.6 BANKING OOP README**

There are 3 main files uploaded and used in the course of this project:
  1. Banking_Projectv2.py -  This is where the main file/code is located. All classes and functions are held and run from this file.
  2. PreStage_Banking_Information.txt - This is where the data storage is located. For the purposes of this project, I am using JSON as my storage system.
  3. test.log - This is where I ran my debugger and used to identify any issues during testing that the file may have encountered. Not necessary to run the code.
 
**INTRODUCTION - RUNNING THE FILE**

As per the instructions outlined at the start of the project, my implementation uses JSON as the main storage system. When running the file in the terminal, the file should automatically request user information to determine whether or not they are held within the PreStage_Banking_Information.txt. The first initial user inputs will be your first name, last name, and date of birth. These will be stored as variables and stored as a key within the JSON dictionary to pull relevant information related to the user. When an instantiation ends, all the information collected during current script will be stored within the JSON file and can be retrieved when you rerun the program again.

Once the intial user information is collected, you will select a number corresponding to whether you are a new or returning customer. Whatever the number you select, the code should be able to determine whether you have selected the correct category based on what is already recorded within the PreStage_Banking_Information.txt file. After you designate yourself as a new or returning customer, the code will then move into class methods and functions defined further below.

**CLASS 'UserInputs' - NEW & RETURNING CUSTOMERS**

new_customer: This function is responsible for ingesting your 5 digit pin number. Your 5 digit pin will be stored within the JSON database and a random 8-12 numerical bank account will be created and stored along with 'balance', 'loan', and 'credit card balance' which are set to 0 balances as you are a new customer with no activity.

if you select this option when your information is already recorded in the databse, i.e. you are a returning customer, the code should identify this and request your 5 digit pin number instead of recreating a new profile.

returning_customer: This function is reponsible for checking and comparing the 5 digit pin provided vs. what is recorded in the database and request any corrections if necessary.

json_loads: This class also contains the function json_loads. This function is reponsible for reading, copying, and updating any new information into the json database as needed. The function was implemented in order to reduce redundant code made throughout the project.

When new_customer or returning_customer are selected, the class 'Options' is called and allows the user to input more selections which calls on json_loads to store or retrieve the appropriate information.

**CLASS 'Services'**

This class is responsible for returning bank account information such as the account number, routing number, and current balance

**CLASS 'Options'**

There exists only one function within this class called 'new' and is responsible for ingesting, storing, and calling the appropriate functions for the options selected by the user. It calls on json_loads to store or retrieve the appropriate information. Options included are 
  1. Check account details/balance
  2. Deposit cash
  3. Withdraw cash
  4. View credit card balance
  5. Use your credit card
  6. Pay off your credit card
  7. Request your loan status
  8. Get a loan
  9. In order to terminate the current session, select 9 to exit.
