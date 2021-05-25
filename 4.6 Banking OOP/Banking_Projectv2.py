'''
import logging in order to record items to the debugger.
import json in order to store data in json strings.
import random to randomly generate an 8-12 digit number to be used as a new user's bank account number.
import sys in order to use the exit() method.
'''
import logging
import json
import random
import sys

"""
DEBUG is a variable set as an integer in the background. The default is set to warning, so we need to change it to DEBUG. DEBUG=10, INFO=20, WARNING=30, ERROR=40, CRITICAL=50. The criteria
filename='test.log' will create a txt file within the root directory for logging.
"""
logging.basicConfig(filename='test.log', level=logging.DEBUG, format='%(asctime)s:%(levelname)s:%(message)s')

"""
The inputs immediately below are performed in order to validate whether or not a customer is a new or existing customer. Existing customers may 
perform actions allowed by your typical bank transactions such as withdrawals, deposits, loans, and transfers. New customers must first 'sign' up 
with the bank before utilizing the services.
"""
Global_fname=input("Please verify your identity. Please provide your first name: ")
Global_lname=input("Please provide your last name: ")
Global_DOB=str(input("Please verify your date of birth in the format mm/dd/yyyy: "))
check=False
while check==False:
    if len(Global_DOB)>10 or len (Global_DOB)<10:
        print('Not a valid date of birth. Please re-enter')
        Global_DOB=str(input("Please verify your date of birth in the format mm/dd/yyyy: "))
        continue
    for i in range(2,6,3):
        if Global_DOB[i]!= '/':
            print('Not a valid date of birth. Please re-enter')
            Global_DOB=str(input("Please verify your date of birth in the format mm/dd/yyyy: "))
    print('Thank you\n')        
    break
    
login_details=Global_fname+Global_lname+Global_DOB

#The items below are done to store the information in JSON format.
path='C:\\Users\\SquareBear\\Python\\Projects\\Banking Project\\PreStage_Banking_Information.txt'
data={}
data[login_details]=[]
data[login_details].append({
     'first name':Global_fname,
     'last name': Global_lname,
     'date of birth': Global_DOB
     
})

try:
    with open(path, 'r') as read_file:             #the try is implemented to bypass an empty JSON file. 
        read_data=json.load(read_file)             #If the except is triggered, we know that the file is 
        logging.debug('open read')                 #empty and need to write the JSON string.
    
except:
    with open(path, 'w') as outfile:
        json.dump(data, outfile, indent=4)
        read_data={}
        logging.debug('json except')

##############################################################
class UserInputs:
'''
The function defined below is performed to determine whether or not the current instantiation is considered a new customer
or not and checks whether or not the information entered agrees with any information held within the JSON repository.
If they are a new customer, bank account information such as balance, account number, loan amounts, and credit card
balances are set at 0 values.
'''
    def new_customer(self):
        with open(path,'r') as read:                  
            temp=json.load(read)  
            if login_details in temp:
                print('You have a file already within the system\n')
                return UserInputs().returning_customer()
        while True:
            logging.debug('while true')
            try:
                new_pin=int(input('Please register as a new user. Enter a 5 digit pin number: '),10)
                if len(str(new_pin))==5:
                    print('\nThank you\n')
                    break
                else:
                    logging.debug('while,else')
                    print('Not a valid PIN')
            except:
                print('Not a valid PIN.')
                new_pin=int(input('Please register as a new user. Enter a 5 digit pin number: '),10)
                logging.debug('while,except')
        print('What would you like to do?\n')

        gen=random.randint(100000000000,999999999999) #To generate a new account for a new customer

        with open(path,'r') as read:                  #To read and '.update' current existing JSON file with new customer         
            temp=json.load(read)       
        temp.update({login_details:[
            {
            'first name':Global_fname,
            'last name': Global_lname,
            'date of birth':Global_DOB,
            'pin': new_pin,
            'account': gen,
            'balance': 0,
            'loan': 0,
            'credit card balance': 0
            }]})                             
        with open(path, 'w') as outfile:
            json.dump(temp, outfile, indent=4)

        return Options().new()
'''
The function returning_customer validates whether or not a customer is returning or not and validates the pin entered.
If a customer is considered returning, i.e. the first name, last name, and date of birth are already within the
JSON repository, then the pin must match the data recorded within the file
'''
    def returning_customer(self):
        with open(path,'r') as read:                  #To read and '.update' current existing JSON file with new customer         
            temp=json.load(read)
            if login_details not in temp:
                print('You do not have a file on record. Please register as a new customer\n')
                return UserInputs().new_customer()
        old_pin=input('Please enter your 5 digit pin number: ')
        n=0
        while n<4:
            if old_pin != str(temp[login_details][0]['pin']):
                print('{} attempts remaining...'.format(4-n))
                old_pin=input('Wrong PIN entered.\nPlease enter your 5 digit pin number: ')      
                n+=1
            elif old_pin ==str(temp[login_details][0]['pin']):
                print('Welcome {}!\n'.format(data[login_details][0]['first name']))
                break
        if n==4:
            print('Maximum number of attempts exceeded. Please re-login or contact your administrator')
            sys.exit()
        return Options().new()
'''
json_loads reads, copies, and updates the data repository anytime we need to make any changes or updates to a 
pre-existing user.
'''
    def json_loads(self, string, amount=0):
        self.balance=int(amount)
        with open(path,'r') as read:                  #To read and '.update' current existing JSON file with new customer         
            temp=json.load(read)   
        newtemp=temp[login_details][0].copy()
        checker=self.balance
        if newtemp[string]+ checker<0:
            print('\nCannot exceed a $0 balance. Please re-select options\n')
            return Options().new()
        else:
            newtemp[string]+=self.balance
            temp.update({login_details:[newtemp]})
            with open(path, 'w') as outfile:
                json.dump(temp, outfile, indent=4)   
            if string =='balance':
                return('\nYour current account balance is ${}\n'.format(newtemp[string]))
            if string =='credit card balance':
                return('\nYour current card balance is ${}\n'.format(newtemp[string]))
            if string=='loan':
                return('\nLoan status: ${} outstanding'.format(newtemp[string]))

'''
The class Services is designed to set up to return bank, routing, and current account balance information and takes in 
UserInputs as a parameter
'''
class Services(UserInputs):
    def __init__(self):
        self.balance=0
        self.credit=0    

    def account(self, account_num, routing_num=121000358,balance=0):
        self.account_num=account_num
        self.routing_num=routing_num
        self.balance=balance
        print(f'\nAccount Number: {self.account_num}\nRouting Number: {self.routing_num}')
        print(UserInputs().json_loads('balance'))
        return Options().new()

'''
The Options class ingests the users options to return a specific output.
'''
class Options:
    def new(self):
        logging.debug('first init')
        self.new_cust_inputs=input('Please input a number from the following options:\n1. Check account details and current balance\
                                        \n2. Deposit cash\n3. Withdraw cash\n4. View credit card balance\n5. Use credit card\n6. Pay credit card balance\
                                        \n7. Request loan status\n8. Get a loan\n9. Exit\nEnter your response: ')
        if self.new_cust_inputs ==str(1):
            with open(path,'r') as read:                  #To read and '.update' current existing JSON file with new customer         
                temp=json.load(read)
            print(Services().account(str(temp[login_details][0]['account'])))
        if self.new_cust_inputs ==str(2):
            while True:
                deposit_amnt=input('Enter a numerical amount you wish to deposit: ')
                if deposit_amnt.isdigit():
                    print(UserInputs().json_loads('balance',deposit_amnt))
                    return Options().new()
                else:
                    print('\nNot a valid selection.\n')
        if self.new_cust_inputs ==str(3):
            while True:
                withdraw_amnt=input('Enter a numerical amount you wish to withdraw: ')
                if withdraw_amnt.isdigit():
                    new_amnt='-'+ withdraw_amnt
                    print(UserInputs().json_loads('balance',new_amnt))
                    return Options().new()
                else:
                    print('\nNot a valid selection.\n')
        if self.new_cust_inputs ==str(4):
            print(UserInputs().json_loads('credit card balance'))
            return Options().new()
        if self.new_cust_inputs ==str(5):
            while True:
                credit_pay_amnt=input('Enter a numerical amount you wish to pay with your credit card: ')
                if credit_pay_amnt.isdigit():
                    print(UserInputs().json_loads('credit card balance',credit_pay_amnt))
                    return Options().new()
                else:
                    print('\nNot a valid selection.\n')
        if self.new_cust_inputs ==str(6):
            while True:
                credit_pay_amnt=input('Enter a numerical amount outstanding you wish to pay: ')
                if credit_pay_amnt.isdigit():
                    new_amnt='-'+credit_pay_amnt
                    print(UserInputs().json_loads('credit card balance',new_amnt))
                    return Options().new()
                else:
                    print('\nNot a valid selection.\n')
        if self.new_cust_inputs ==str(7):
            print(UserInputs().json_loads('loan'))
            return Options().new()
        if self.new_cust_inputs ==str(8):
            while True:
                loan_amnt=input('Enter a numerical amount you wish to borrow: ')
                if loan_amnt.isdigit():
                    print(UserInputs().json_loads('loan',loan_amnt))
                    return Options().new()
                else:
                    print('\nNot a valid selection.\n')
        if self.new_cust_inputs==str(9):
            print('\nThank you!\n')
            sys.exit()
        
        if isinstance(self.new_cust_inputs,str):
            print('\nNot a valid entry\n')
            return Options().new()
  
"""
The code immediately below is to help guide the user input specific information
necessary to run the class methods defined above.
"""
tracker=0
while tracker==0:
    user_inputs=input('Please enter the number from the following options:\
                        \n1. New customer\n2. Returning customer\n\
                        \nEnter your response: ')

    if user_inputs==str(1):
        print(UserInputs().new_customer())
        tracker+=1
    if user_inputs==str(2):
        print(UserInputs().returning_customer())
        tracker+=1
    if isinstance(user_inputs,str):
        print('\nNot a valid selection\n')
        
