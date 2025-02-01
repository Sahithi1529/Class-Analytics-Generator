import database_operations as db

# db.create_table('database.sqlite','admins',{'adminID':'INT','adminName':'VARCHAR(50)',
#                                             'adminEmail':'VARCHAR(20)','adminDepartment':'VARCHAR(20)',
#                                             'adminPassword':'VARCHAR(20)'})

# db.insert_into_table('database.sqlite','admins',[[101,'Karthik','karthik@gmail.com','AI','test@123'],
#                                                  [102,'Sahithi','sahithi@gmail.com','AI','test@321'],
#                                                  [103,'Darahas','darahas@gmail.com','CSE','Darahas3332']])

# print(db.retrieve_data('database.sqlite','admins',['adminName','adminPassword'],'adminID = 101'))

# db.insert_into_table_from_file('database.sqlite','admins','test.csv')
# print(db.retrieve_data('database.sqlite','admins'))


# db.download_data_as_csv('database.sqlite','admins','Data.csv')
print(db.retrieve_data('database.sqlite','admins',['adminPassword'],'adminID = '+str(101)))