from petalapp import db

ROLE_USER = 0
ROLE_ADMIN = 1

#TODO:rename
hospitals = db.Table('hospitals',
    db.Column('hospital_id', db.Integer, db.ForeignKey('hospital.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
)
# tags bmarks time
#FIXME unsure about init
#FIXME tablename is already set unless overridden
class User(db.Model):
    """User has a many-to-many relationship with Hospital"""

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    mail = db.Column(db.String(150), unique=True)
    role = db.Column(db.SmallInteger, default=ROLE_USER)

    hospitals = db.relationship('Hospital', secondary=hospitals,
        backref=db.backref('users', lazy='dynamic'))



    def __init__(self, name="NONE", role=ROLE_USER, mail="NONE"):
        self.name = name
        self.role = role
        self.mail = mail

    def __repr__(self):
        return '<Name %r>' % self.name

class Hospital(db.Model):
    """Hospital's has a one-to-many relationship with DATA and a 
    many-to-many relationship with User"""

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    data = db.relationship('Data', backref='hospital', lazy = 'dynamic')

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Name %r>' % self.name


class Data(db.Model):
    """Data has a many-to-one relationship with Hospital"""

    id = db.Column(db.Integer, primary_key=True)
    pc = db.Column(db.Integer)
    hospital_id = db.Column(db.Integer, db.ForeignKey('hospital.id'))

    def __init__(self, pc):
        self.pc = pc

    def __repr__(self):
        return '<pc %r>' % self.pc


