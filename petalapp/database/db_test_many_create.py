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

    def setUp(self):
        db.drop_all()
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
        db.session.add(derek)
        db.session.add(mac_hospital)
        db.session.add(pro_hospital)
        db.session.add(mac_data)
        db.session.add(pro_data)

        #commit
        db.session.commit()

        #create links
        mac_hospital.data(mac_data)
        pro_hospital.data(pro_data)
        drew.hospitals(mac_hospital)
        drew.hospitals(pro_hospital)
        db.session.commit()



if __name__ == "__main__":
    unittest.main()
