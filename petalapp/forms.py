'''
File: forms.py
Date: 2012-11
Author: Drew Verlee
Description: part of login infrastructure.
'''

from flask.ext.wtf import Form, TextField, BooleanField
from flask.ext.wtf import Required


#TODO: understand/better docs
class LoginForm(Form):
    """builds up login functionality"""

    openid = TextField('openid', validators=[Required()])
    remember_me = BooleanField('remember_me', default=False)
