#'''
#File: db_test_many_create.py
#Date: 2012-12-06
#Author: Drew Verlee
#Description: functions to build a many-to-many relationship
#'''
#import unittest
#from petalapp.database.models import User, Organization, ROLE_USER
#from petalapp import db
#
#class BuildDestroyTables(unittest.TestCase):
#
#    def setUp(self):
#        db.drop_all()
#        db.create_all()
#
#
#    def tearDown(self):
#        db.session.remove()
#        db.drop_all()
#
#
#    def test_user_setup(self):
#
#        user_test_1 = User("test_user_nickname","user_email",ROLE_USER)
#        db.session.add(user_test_1)
#        db.session.commit()
#
#
#    def test_data_setup(self):
#
#        data_test_1 = Data(1)
#        db.session.add(data_test_1)
#        db.session.commit()
#
#    def test_organization_setup(self):
#
#        organization_test_1 = Organization("test_organization_1")
#        db.session.add(organization_test_1)
#        db.session.commit()
#
#
#    def test_make_unique_nickname(self):
#        u = User(nickname = 'john', email = 'john@example.com')
#        db.session.add(u)
#        db.session.commit()
#        nickname = User.make_unique_nickname('john')
#        assert nickname != 'john'
#        u = User(nickname = nickname, email = 'susan@example.com')
#        db.session.add(u)
#        db.session.commit()
#        nickname2 = User.make_unique_nickname('john')
#        assert nickname2 != 'john'
#        assert nickname2 != nickname
#
#
#    def test_multiple_link_table(self):
#
#
#        #create
#        drew = User(nickname= "Drew", email="Drew@gmail.com",role=ROLE_USER)
#        mac_organization = Organization("Mac_organization")
#        pro_organization = Organization("pro_organization")
#        mac_data = Data(1,2,3)
#        pro_data = Data(10,9,8)
#
#        #add
#        db.session.add(drew)
#        db.session.add(mac_organization)
#        db.session.add(pro_organization)
#        db.session.add(mac_data)
#        db.session.add(pro_data)
#
#        #commit
#        db.session.commit()
#
#        #create links
#        mac_organization.data.append(mac_data)
#        pro_organization.data.append(pro_data)
#        drew.organizations.append(mac_organization)
#        drew.organizations.append(pro_organization)
#        db.session.commit()
#
#    def functions_of_add_remove(self):
#        johns_organization_data = Data('johns_organization_data')
#        johns_organization = Organization('johns_organization')
#        john = User('john', 'john@gmail.com')
#
#        db.session.add(johns_organization_data)
#        db.session.add(johns_organization)
#        db.session.add(john)
#
#        #TODO make a function for this?
#        johns_organization.append(johns_organization_data)
#        #do  i need a commit?
#        db.session.commit()
#
#        self.assertEqual(john.remove_organization(johns_organization), None)
#
#        john_has_organization = john.add_organization(johns_organization)
#        db.session.add(john_has_organization)
#        db.session.commit()
#
#        self.assertEqual(john.add_organization(johns_organization), None)
#        self.assertEqual(len(john.organizations), 1)
#
#
#if __name__ == "__main__":
#    unittest.main()
