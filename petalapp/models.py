from petalapp import db

ROLE_USER = 0
ROLE_ADMIN = 1

hospitals = db.Table('hospitals',
    db.Column('hospital_id', db.Integer, db.ForeignKey('hospital.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    #mail = db.Column(db.String(150), unique=True)
    #role = db.Column(db.SmallInteger, default=ROLE_USER)
    hospitals = db.relationship('Hospital', secondary=hospitals,
        backref=db.backref('users', lazy='dynamic'))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Name %r>' % self.name

class Hospital(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    data = db.relationship('Data', backref='hospital', lazy='dynamic')

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Name %r>' % self.name


class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    PC = db.Column(db.Integer)
    hospital_id = db.Column(db.Integer, db.ForeignKey('hospital.id'))

    def __init__(self, name):
        self.PC = pc

    def __repr__(self):
        return '<pc %r>' % self.PC


