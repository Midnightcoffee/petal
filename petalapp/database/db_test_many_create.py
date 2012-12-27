'''
File: db_test_many_create.py
Date: 2012-12-06
Author: Drew Verlee
Description: functions to build a many-to-many relationship
'''
import unittest
from petalapp.database.models import User, Hospital, Data, ROLE_USER
from petalapp import db

class BuildDestroyTables(unittest.TestCase):

    user_test_1 = User("test_user_nickname","user_email",ROLE_USER)
    data_test_1 = Data(1)
    hospital_test_1 = Hospital("test_hospital_1")

    def setUP(self):
        db.create_all()


    def tearDown(self):
        db.session.remove()
        db.drop_all()


    def test_user_setup(self):

        db.session.add(self.user_test_1)
        db.session.commit()


    def test_data_setup(self):

        db.session.add(self.data_test_1)
        db.session.commit()

    def test_hospital_setup(self):

        db.session.add(self.hospital_test_1)
        db.session.commit()


    def test_print(self):
        example = User.query.get(1)
        print("our user {0}".format(example)) 


    def test_user_hospital_link(self):
        self.user_test_1.hospitals(self.hospital_test_1)
        db.session.commit()

    def test_hospital_data_link(self):
        self.hospital_test_1.data(self.data_test_1)
        db.session.commit()


    def test_print_verbose(self):
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


