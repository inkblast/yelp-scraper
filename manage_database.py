import sys
import pyodbc as odbc



DRIVER = "SQL Sever"
SEVER = "LAPTOP-V2DHN538"
DATABASE = "resturents"
USERNAME = "inkblast"
PASSWORD = "!d0ntkn0w"

conn_string = f"""Driver={DRIVER};Sever={SEVER};Database={DATABASE}; username={USERNAME};password={PASSWORD};Trust_Connection=yes;"""

#CONNECT DATABASE
try:
    conn = odbc.connect('Driver={SQL Server};'
                          'Server=;LAPTOP-V2DHN538;'
                          'Database=resturents;'
                          'Trusted_Connection=yes;',autocommit=True)
except Exception as e:
    print(e)
    print("task is terminated")
    sys.exit()
else:
    cursor = conn.cursor()



#DATA INSERT
def insertData(tablename,data):
    insert_satatment = f""" INSERT INTO {tablename} VALUES (?,?,?,?,?,?)"""

    try:
        for records in data:
            record = [records.profileName,records.profileLocation,records.rating, records.ratingDate,records.comment, records.profileLink]
            cursor.execute(insert_satatment,record)
    except Exception as e:
        cursor.rollback()
        print(e)
        print("transaction rolled back")
    else:
        print("inserted succesfully")



#CREATE TABLE
def createTable(tablename):
    create_statement = f'''CREATE TABLE {tablename} (profile_Name nvarchar(50),profile_location nvarchar(50),rate int,rate_date nvarchar(10),review nvarchar(MAX),profile_link nvarchar(MAX))'''
    cursor.execute(create_statement)
    conn.commit()
    print(f"{tablename} table created succesfully")

#Delete Table
def deleteTable(tablename):
    delete_statement = f'drop table {tablename}'
    cursor.execute(delete_statement)
    conn.commit()
    print("deleted!")


#Read Table Date
def readdata(tablename):
	read_statement = f"select * from {tablename}"
	cursor.execute(read_statement)
	rows = cursor.fetchall()
	for row in rows:
		print(row)


resturentsList=['CaféSusubySuitsupply', 'Carmelinas', 'FogodeChão', 'KantipurCafe','Ostra', 'SaltieGirl','Tanám', 'Toro']

'''for elm in resturentsList:
    deleteTable(elm)
'''
