# Data Pipeline Mini Project Instructions

The purpose of this project is to read a csv file and write the contents of the table to an SQL database using the MySQL connector available via Python.

## Steps

1. Initialize the database connection by providing the username, password, host, port, and database name housed within the get_db_connection() function. In this instance, the information was hosted on my local machine. Depending on where the information is stored on your local machine, the information will need to be changed accordingly:

def get_db_connection():
	connection = None
	try:
	connection = mysql.connector.connect(user='<username>',	password='<some password>',
								host='<some hostname>',
								port='<some port>',
								database='<some database')	

2. The connection will then be executed via the load_third_party() connection which intakes the variables connection and file_path_csv. Connection is the function call of the first step, get_db_connection and the variable file_path_csv is the directory in which the csv file is stored on your local machine. It will be executed via the code below:

def load_third_party (connection, file_path_csv):
	
	#assigns the SQL connection a cursor. A cursor is needed to point to the database connection to 'do something'
	cursor = connection.cursor()

	#reads the CSV in a dataframe format so we can then send the info into SQL
	columns=['Ticket_ID', 'Trans_Date', 'Event_ID', 'Event_Name', 'Event_Date', 'Event_Type','Event_City', 'Customer_ID', 'Price', 'Num-Tickets']
	data=pd.read_csv(file_path_csv, names=columns)

	#creating a new item in our dictionary titled 'sales'. You can have multiple items within the dictionary, however to print the items \
	#into the dataframe, you will need to iterate.
	table = {}
	table['sales'] = (
		"create table sales("
		"Ticket_ID int not null,"
		"Trans_Date varchar(16) not null,"
		"Event_ID int not null,"
		"Event_Name varchar(50) not null,"
		"Event_Date varchar(16) not null,"
		"Event_Type varchar(16) not null,"
		"Event_City varchar(16) not null,"
		"Customer_ID int not null,"
		"Price int not null,"
		"Num_Tickets int not null"
		")")

	#for table_name in table: (You only need to iterate if you have multiple items within your dictionary, otherwise the try except statement works.)
	table_description = table['sales']
	try:
		print('Creating table {}: '.format('sales'), end='')
		cursor.execute(table_description)
	except Exception as err:
		print('Table already exists')
		cursor.execute('drop table sales')
	else:
		print('OK')

	#to populate the newly created table 'sales. Per the MySQL doc, you must implement both the special character reader %s and val.'
	insert="""insert into sales (Ticket_ID, Trans_Date, Event_ID, Event_Name, Event_Date, Event_Type, Event_City, Customer_ID, Price, Num_Tickets) 
			values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""

	#To iterate through each row and populate the table. Itertuples is more efficient than iterrows. Overall, iterating through a df is slow\
	#and if you can do something else (vectorizing) it will be more efficient.
	for row in data.itertuples():
		val=row.Ticket_ID, row.Trans_Date, row.Event_ID, row.Event_Name, row.Event_Date, row.Event_Type, row.Event_City, row.Customer_ID, row.Price, row._10
		cursor.execute(insert, val)
	#As we are now importing actual information and not just creating a table, you need to commit your changes otherwise the information won't be loaded in SQL.
	connection.commit()
	cursor.close()
	return
										
3. The final step once the data has been loaded into the SQL database is to use whatever statistical approach you wish to use to extract the data. In this case, I searched for the events that sold the most tickets to produce an easy to read output:
										
#depending on where the database is, your from statement will need to be changed accordingly
def query_popular_tickets(connection):
	sql_statement="""
	select Event_Name, Num_Tickets
	from pipeline.sales
	order by Num_Tickets desc"""

	cursor=connection.cursor()
	cursor.execute(sql_statement)
	records=cursor.fetchall()
	cursor.close()
	final="""
	Here are the most popular tickets in the past month, in order of most popular to least:
	  -{}: Number of tickets {}
	  -{}: Number of tickets {}
	  -{}: Number of tickets {}
	  -{}: Number of tickets {}
	  -{}: Number of tickets {}""".format(records[0][0],records[0][1],records[1][0],records[1][1],records[2][0],records[2][1],records[3][0],records[3][1],records[4][0],records[4][1])
	return final
