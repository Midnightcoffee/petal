#TODO: probable move aws tools and this to a more sensible location


from database.models import User
from petalapp import db

def get_user_by_id(user_id):
    '''Given an id returns the user'''
    user = User.query.filter_by(id=user_id).first() # no need for unicode
    if user:
        return user
    else:
        return None

def create_broswerid_user(kwargs):
    ''' takes browserid response and creates a user'''
    if kwargs['status'] == 'okay':
        user = User(kwargs['email']) # i don't need to create an id?
        db.session.add(user)
        db.session.commit()
        return user
    else:
        return None


def get_user(kwargs):
    '''
    Given the response from BrowserID, finds or creates a user.
    If a user can neither be found nor created, returns None.
    '''
    #maybe a better way to do this?

    user = User.query.filter((User.email==kwargs.get('email'))|(User.id==kwargs.get('id'))).first()
    if user:
        return user
    return create_broswerid_user(kwargs)
