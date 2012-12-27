'''
File: db_test_many_create.py
Date: 2012-12-06
Author: Drew Verlee
Description: functions to build a many-to-many relationship
'''

db.session.drop_all()
from models import db, User, Hospital, Data


data_test_1 = Data(1)
user_test_1 = User("test_user_nickname")
hospital_test_1 = Hospital("test_hospital_1")

for database_entry in [data_test_1, user_test_1, hospital_test_1]:
    db.session.add(database_entry)

db.session.commit()

example = User.query.get(1)
print(example)

users = Users.query.all()
for u in users:
    db.session.delete(u)

hospitals = Hospital.query.all()
for h in hospitals:
    db.session.delete(h)

data = Data.query.all()
for d in data:
    db.session.delete(d)




