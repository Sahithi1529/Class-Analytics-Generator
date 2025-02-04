import database_operations as db

# db.create_table('database.sqlite','admins',{'adminID':'INT','adminName':'VARCHAR(50)',
#                                             'adminEmail':'VARCHAR(20)','adminDepartment':'VARCHAR(20)',
#                                             'adminPassword':'VARCHAR(20)'})

# db.insert_into_table('database.sqlite','admins',[[101,'Karthik','karthik@gmail.com','AI','test@123'],
#                                                  [102,'Sahithi','sahithi@gmail.com','AI','test@321'],
#                                                  [103,'Darahas','darahas@gmail.com','CSE','Darahas3332']])

# print(db.retrieve_data('database.sqlite','admins',['adminName','adminPassword'],'adminID = 101'))

# db.insert_into_table_from_file('database.sqlite','admins','test.csv')
# print(db.retrieve_data('../database.sqlite','admins'))

# db.download_data_as_csv('../database.sqlite','admins','Data.csv')
# print(db.retrieve_data('database.sqlite','admins',['adminPassword'],'adminID = '+str(101)))

# print(db.update_data('../database.sqlite','admins',{'adminPassword':'Darahas1','adminName':'Darahas'},'adminID = 103'))

# db.delete_data('../database.sqlite','admins','adminID = 105')


## CREATING FACULTY TABLE 
# db.create_table('database.sqlite','FACULTIES',{
#     'facultyId':'INT',
#     'fname':'VARCHAR(50)',
#     'facultyEmail':"VARCHAR(20)",
#     'facultyPassword':"VARCHAR(20)",
#     'facultyDepartment':'VARCHAR(20)'
# })

# db.insert_into_table('database.sqlite','FACULTIES',[
#     [101, "Karthik","test@gmail.com","test@123","Artificial Intelligence"]])

# db.create_table('database.sqlite','admins',{'adminID':'INT','adminName':'VARCHAR(50)',
#                                             'adminEmail':'VARCHAR(20)','adminDepartment':'VARCHAR(20)',
#                                             'adminPassword':'VARCHAR(20)'})

# db.insert_into_table('database.sqlite','admins',[[101,'Karthik','karthik@gmail.com','AI','test@123'],
#                                                  [102,'Sahithi','sahithi@gmail.com','AI','test@321'],
#                                                  [103,'Darahas','darahas@gmail.com','CSE','Darahas3332']])


# 
# db.create_table('coredb.sqlite','ADMIN',{'adminID':'INT','adminName':'VARCHAR(50)',
#                                             'adminEmail':'VARCHAR(20)','adminDepartment':'VARCHAR(20)',
#                                             'adminPassword':'VARCHAR(20)'})
# db.insert_into_table('coredb.sqlite','ADMIN',[[
#     101,'Karthik','karthik@gmail.com','AI','test@123'
# ]])

# print(db.retrieve_data('coredb.sqlite','ADMIN'))

# db.create_table('coredb.sqlite','FACULTY',{'facultyID':'INT','facultyName':'VARCHAR(50)',
#                                             'facultyEmail':'VARCHAR(20)','facultyDepartment':'VARCHAR(20)',
#                                             'facultyPassword':'VARCHAR(20)'})
# db.insert_into_table('coredb.sqlite','FACULTY',[[
#     102,'Vishwas','viswas@gmail.com','AI','vish'
# ]])

# print(db.retrieve_data('coredb.sqlite','FACULTY'))

# db.create_table('coredb.sqlite','MESSAGES',{
#     'SENDERID':'VARCHAR(20)',
#     'RECEIVERID':'VARCHAR(20)',
#     'SENTDATE':'DATE',
#     'SENTTIME':'TIME',
#     'MESSAGE':'VARCHAR(100)'
# })
from datetime import datetime
curr = str(datetime.today()).split()
date = curr[0]
time = curr[1][:8]
# db.insert_into_table('coredb.sqlite','MESSAGES',[["101","102",date,time,"This is Message 1"]])
# print(date,time)
print(db.retrieve_data('coredb.sqlite','MESSAGES'))
# con = db.connection_object('coredb.sqlite')
# con.execute("DROP TABLE MESSAGES")
# con.commit()
