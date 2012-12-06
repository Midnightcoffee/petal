'''
File: db_test_many_create.py
Date: 2012-12-06
Author: Drew Verlee
Description: functions to build a many-to-many relationship
'''

from models import db, User, Hospital, Data

db.drop_all()
data_test_1 = Data(1)
user_test_1 = User("test_user_1")
hospital_test_1 = Hospital("test_hospital_1")

for database_entry in [data_test_1, user_test_1, hospital_test_1]:
    db.session.add(database_entry)

db.session.commit()

hospital_test_1.data.append(data_test_1)
user_test_1.hospitals.append(hospital_test_1)

db.session.commit()

print("user_test_1: {0}".format(user_test_1.hospitals))


