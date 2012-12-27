'''
File: db_test_many_create.py
Date: 2012-12-06
Author: Drew Verlee
Description: functions to build a many-to-many relationship
'''


from petalapp.database.models import User, Hospital, Data, ROLE_USER
from petalapp import db


data_test_1 = Data(1)
user_test_1 = User("test_user_nickname","user_email",ROLE_USER)
hospital_test_1 = Hospital("test_hospital_1")


# add them to the database
for database_entry in [data_test_1, user_test_1, hospital_test_1]:
    db.session.add(database_entry)

db.session.commit()

example = User.query.get(1)
print(example)

users = User.query.all()
print("********************** users **************")
for u in users:
    print(u)
    db.session.delete(u)

hospitals = Hospital.query.all()
print("********** hostpitals ***************")
for h in hospitals:
    print(h)
    db.session.delete(h)

data = Data.query.all()
print("******************* data **************")
for d in data:
    print(d)
    db.session.delete(d)


db.session.commit()
