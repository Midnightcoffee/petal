'''
File: forms.py
Date: 2012-11
Author: Drew Verlee
Description: part of login infrastructure.
'''

from flask.ext.wtf import Form, TextField, BooleanField
from flask.ext.wtf import Required
from petalapp.database.models import User


#TODO: understand/better docs
class LoginForm(Form):
    """builds up login functionality"""
    openid = TextField('openid', validators=[Required()])
    remember_me = BooleanField('remember_me', default=False)

# because i don't have a profile,avatar,etc... possible not necessary?
#    def __init__(self, original_nickname, *args, **kwargs):
#        Form.__init__(self, *args, **kwargs)
#        self.original_nickname = original_nickname
#
#    #current not used as there are no profile pages
#    def validate(self):
#        if not Form.validate(self):
#            return False
#        if self.nickname.data == self.original_nickname:
#            return True
#        user = User.query.filter_by(nickname = self.nickname.data).first()
#        if user != None:
#            self.nickname.errors.append('This nickname is already in use. Please choose another one.')
#            return False
#        return True





