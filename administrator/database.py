import sqlite3
import pandas as pd
# Create Connection Object
def connection_object(filename):
    '''
    Accept Database name and create connection object
    '''
    con = sqlite3.connect(filename)
    return con

# Create a Table in Database
def create_table(database,tablename,columns):
    '''
    Accept database name, tablename , columns with datatype as dictionary
    '''
    con = connection_object(database)
    SQL_QUERY = f"CREATE TABLE {tablename} ("
    for column in columns.keys():
        SQL_QUERY += f"{column} {columns[column]},"
    SQL_QUERY = SQL_QUERY[:len(SQL_QUERY)-1]
    SQL_QUERY += ")"

    print(SQL_QUERY)
    con.execute(SQL_QUERY)
    con.commit()
    print("Table Created Successfully!!")
    con.close()

# Retrive the Data from Database
def retrive_table_by_query(database, query):
    '''
    Accept the database name and user query to retrive the data
    '''
    con = connection_object(database)
    cursor = con.execute(query)
    rows = cursor.fetchall()
    print("Query Executed Sucessfully")
    con.close()
    return rows

# Insert into the table
def insert_into_table(database,tablename,values):
    '''
    database: database name,
    tablename: Name of the table,
    values: List of tuples or lists containing the data
    '''
    con = connection_object(database)
    no_of_cols = len(values[0])
    insert_query = f"INSERT INTO {tablename} VALUES(" + "?,"*no_of_cols
    insert_query = insert_query[:len(insert_query)-1]+")"
    con.executemany(insert_query,values)
    print("Data Inserted Successfully")
    con.commit()

# Insert inbo the table using Excel File
def insert_into_table_with_excel(database,tablename,filename):
    dfe = pd.read_csv(filename)
    rows = []
    for index in range(len(dfe)):
        row = dfe.iloc[[index]]
        print(row.values)
        rows.append(row.values[0])
    insert_into_table(database,tablename,rows)
    
# Download to csv file
def retrieve_data_as_csv(database,tablename):
    query = "SELECT * FROM "+tablename
    rows = retrive_table_by_query(database,query)
    dfe = pd.DataFrame(rows)
    dfe.to_csv('data.csv')
    print("Csv created successfully")



