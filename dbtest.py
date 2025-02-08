import database_operations as db

from datetime import datetime
curr = str(datetime.today()).split()
date = curr[0]
time = curr[1][:8]
# db.insert_into_table('coredb.sqlite','MESSAGES',[["101","102",date,time,"This is Message 1"]])
# print(date,time)
# print(db.retrieve_data('coredb.sqlite','FACULTY'))
# con = db.connection_object('coredb.sqlite')
# con.execute("DROP TABLE MAPPING")
# con.commit()

# ADMIN SCHEMA
# db.create_table('coredb.sqlite','ADMIN',{
#     'adminId':'INT PRIMARY KEY',
#     'adminName':'VARCHAR(20)',
#     'adminEmail':'VARCHAR(20)',
#     'adminPassword':'VARCHAR(20)',
#     'adminDepartment':'VARCHAR(20)',
#     'adminPhone':'VARCHAR(20)'
# })

# FACULTY SCHEMA
# db.create_table('coredb.sqlite','FACULTY',{
#     'facultyId':'INT PRIMARY KEY',
#     'facultyName':'VARCHAR(20)',
#     'facultyEmail':'VARCHAR(20)',
#     'facultyPassword':'VARCHAR(20)',
#     'facultyDepartment':'VARCHAR(20)',
#     'facultyPhone':'VARCHAR(20)'
# })

# MESSAGES SCHEMA
# db.create_table('coredb.sqlite','MESSAGES',{
#     'senderId':'INT',
#     'receiverId':'INT',
#     'sentDate':'DATE',
#     'sentTime':'TIME',
#     'Message':'VARCHAR(99)',
# })

# CLASSROOM SCHEMA
# db.create_table('coredb.sqlite','CLASSROOM',{
#     'department':'VARCHAR(20)',
#     'year':'VARCHAR(5)',
#     'section':'VARCHAR(5)',
#     'classId':'INT PRIMARY KEY',
# })

# COURSE SCHEMA
# db.create_table('coredb.sqlite','COURSE',{
#     'subjectId':'INT PRIMARY KEY',
#     'subjectName':'VARCHAR(50)',
# })

# MAPPING SCHEMA
# db.create_table('coredb.sqlite','MAPPING',{
#     'facultyId':'INT ',
#     'subjectId':'INT',
#     'classId':'INT', 
#     'classDate': 'DATE, FOREIGN KEY(facultyId) REFERENCES FACULTY(facultyId), FOREIGN KEY(subjectId) REFERENCES COURSES(subjectId)',
# })

# INSERT INTO ADMIN
# db.insert_into_table('coredb.sqlite','ADMIN',[[101,'Karthik','21eg106b26@anurag.edu.in','test@123','AI','9999999999']])
# FETCH DATA FROM ADMIN
# print(db.retrieve_data('coredb.sqlite','ADMIN'))

# INSERT INTO FACULTY
# db.insert_into_table('coredb.sqlite','FACULTY',[[201,'Vishwas','21eg106b38@anurag.edu.in','3814316','CSE','8888888888']])
# # FETCH DATA FROM ADMIN
# print(db.retrieve_data('coredb.sqlite','FACULTY'))

# INSERT INTO CLASSROOM
# db.insert_into_table('coredb.sqlite','CLASSROOM',[['AI','IV','A',302]])
# # # FETCH DATA FROM CLASSROOM
# print(db.retrieve_data('coredb.sqlite','CLASSROOM'))

# INSERT INTO COURSE
# db.insert_into_table('coredb.sqlite','COURSE',[[402,'Machine Learning']])
# # # # FETCH DATA FROM COURSE
# print(db.retrieve_data('coredb.sqlite','COURSE'))

# INSERT INTO MAPPING
# db.insert_into_table('coredb.sqlite','MAPPING',[[201,401,301,'2025-02-09'],[201,402,302,'2025-02-08']])
# # # # FETCH DATA FROM MAPPING
# print(db.retrieve_data('coredb.sqlite','MAPPING'))

# con = db.connection_object('coredb.sqlite')
# rows = con.execute(f"SELECT * FROM MAPPING WHERE FACULTYID = 201 AND CLASSDATE = '{date}'")
# for row in rows:
#     print(row)
