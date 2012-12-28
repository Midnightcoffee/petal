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

    def setUp(self):
        db.drop_all()
        db.create_all()


    def tearDown(self):
        db.session.remove()
        db.drop_all()


    def test_user_setup(self):

        user_test_1 = User("test_user_nickname","user_email",ROLE_USER)
        db.session.add(user_test_1)
        db.session.commit()


    def test_data_setup(self):

        data_test_1 = Data(1)
        db.session.add(data_test_1)
        db.session.commit()

    def test_hospital_setup(self):

        hospital_test_1 = Hospital("test_hospital_1")
        db.session.add(hospital_test_1)
        db.session.commit()


    def test_make_unique_nickname(self):
        u = User(nickname = 'john', email = 'john@example.com')
        db.session.add(u)
        db.session.commit()
        nickname = User.make_unique_nickname('john')
        assert nickname != 'john'
        u = User(nickname = nickname, email = 'susan@example.com')
        db.session.add(u)
        db.session.commit()
        nickname2 = User.make_unique_nickname('john')
        assert nickname2 != 'john'
        assert nickname2 != nickname


    def test_multiple_link_table(self):


        #create
        drew = User(nickname= "Drew", email="Drew@gmail.com",role=ROLE_USER)
        mac_hospital = Hospital("Mac_hospital")
        pro_hospital = Hospital("pro_hospital")
        mac_data = Data(1,2,3)
        pro_data = Data(10,9,8)

        #add
        db.session.add(drew)
        db.session.add(mac_hospital)
        db.session.add(pro_hospital)
        db.session.add(mac_data)
        db.session.add(pro_data)

        #commit
        db.session.commit()

        #create links
        mac_hospital.data.append(mac_data)
        pro_hospital.data.append(pro_data)
        drew.hospitals.append(mac_hospital)
        drew.hospitals.append(pro_hospital)
        db.session.commit()

    def functions_of_add_remove(self):
        johns_hospital_data = Data('johns_hospital_data')
        johns_hospital = Hospital('johns_hospital')
        john = User('john', 'john@gmail.com')

        db.session.add(johns_hospital_data)
        db.session.add(johns_hospital)
        db.session.add(john)

        #TODO make a function for this?
        johns_hospital.append(johns_hospital_data)
        #do  i need a commit?
        db.session.commit()

        self.assertEqual(john.remove_hospital(johns_hospital), None)

        john_has_hospital = john.add_hospital(johns_hospital)
        db.session.add(john_has_hospital)
        db.session.commit()

        self.assertEqual(john.add_hospital(johns_hospital), None)
        self.assertEqual(len(john.hospitals), 1)


if __name__ == "__main__":
    unittest.main()
