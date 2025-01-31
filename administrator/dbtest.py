import database as db
# db.create_table('database.sqlite','USER',{'Name':'VARCHAR(20)','Age':'INT'})
values = [
    ("Vishwas","21"),
    ("Karthik","21")
]
# db.insert_into_table('database.sqlite','USER',values)
# db.insert_into_table_with_excel('database.sqlite','USER','users.csv')
# print(db.retrive_table_by_query('database.sqlite',"SELECT * FROM USER"))
db.retrieve_data_as_csv('database.sqlite','USER')