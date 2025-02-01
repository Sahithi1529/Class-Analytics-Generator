import sqlite3
import pandas as pd

#PENDING
# 1 UPDATE DATA
# 2 DELETE DATA

# Create Connection Object
def connection_object(filename):
    '''
    filename: database name
    returns --> Connection Object
    '''
    try:
        con = sqlite3.connect(filename)
        return con
    except Exception as e:
        print(f"Exception '{e}' occured while connecting to database")
        return None

# Create a Table in Database
def create_table(database,tablename,columns):
    '''
    database : database name
    tablename : table name
    columns : Dictionary with column names as Keys and column types as Values
    '''
    SQL_QUERY = f"CREATE TABLE {tablename} ("
    for column in columns.keys():
        SQL_QUERY += f"{column} {columns[column]},"
    SQL_QUERY = SQL_QUERY[:len(SQL_QUERY)-1]
    SQL_QUERY += ");"
    try:
     con = connection_object(database)
     con.execute(SQL_QUERY)
     con.commit()
     print("Table Created Successfully!!")
     con.close()
     return True
    except Exception as e:
        print(f"Exception '{e}' Occured while creating table")
        return False

# Retrive the Data from Database

# Retrieve data from the Database
def retrieve_data(database,tablename,columns=["*"],condition=None):
    list_of_columns = ",".join(columns)
    base_sql_query = f"SELECT {list_of_columns} from {tablename} "
    if condition:
        base_sql_query += 'WHERE ' + condition
    base_sql_query += ';'
    try:
        con = connection_object(database)  
        cursor = con.execute(base_sql_query)
        cols_of_db = []
        for element in cursor.description:
            cols_of_db.append(element[0])
        rows = cursor.fetchall()
        return rows,cols_of_db
    except Exception as e:
        print(f"Exception '{e}' occured while retrieving the data")
        return None


# Insert into the table
def insert_into_table(database,tablename,values):
    '''
    database: database name,
    tablename: Name of the table,
    values: List of tuples or lists containing the data
    '''
    try:
        con = connection_object(database)
        cursor = con.execute(f"SELECT * FROM {tablename} ;")
        no_of_cols = len(cursor.description)
        insert_query = f"INSERT INTO {tablename} VALUES(" + "?,"*no_of_cols
        insert_query = insert_query[:len(insert_query)-1]+");"
        con.executemany(insert_query,values)
        print("Data Inserted Successfully")
        con.commit()
        return True
    except Exception as e:
        print("Exception '{e}' occured while inserting data into table")

# Insert into the table using file
def insert_into_table_from_file(database,tablename,filename,filetype='.csv'):
    if filetype=='xlsx':
        dfe = pd.read_excel(filename)
    else:
        dfe = pd.read_csv(filename)
    rows = []
    for index in range(len(dfe)):
        row = dfe.iloc[[index]]
        rows.append(row.values[0])
    insert_into_table(database,tablename,rows)
    return True

    
# Download as csv file
def download_data_as_csv(database,tablename,filename):
    rows,cols_of_db = retrieve_data(database,tablename)
    dfe = pd.DataFrame(rows,columns=cols_of_db)
    print(dfe.columns)
    dfe.to_csv(filename)
    print("Csv created successfully")



