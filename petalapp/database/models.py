from petalapp import db

ROLE_USER = 0
ROLE_ADMIN = 1

#TODO:rename
hospitals = db.Table('hospitals',
    db.Column('hospital_id', db.Integer, db.ForeignKey('hospital.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
)

#FIXME unsure about init
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    mail = db.Column(db.String(150), unique=True)
    role = db.Column(db.SmallInteger, default=ROLE_USER)
    hospitals = db.relationship('Hospital', secondary=hospitals,
        backref=db.backref('users', lazy='dynamic'))

    def __init__(self, name, role, mail="NONE", hospitals="NONE"):
        self.name = name
        self.role = role
        self.mail = mail
        self.hospitals = hospitals

    def __repr__(self):
        return '<Name %r>' % self.name

class Hospital(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    data = db.relationship('Data', backref='hospital', lazy='dynamic')

    def __init__(self, name, data):
        self.name = name
        self.date = data

    def __repr__(self):
        return '<Name %r>' % self.name


class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pc = db.Column(db.Integer)
    hospital_id = db.Column(db.Integer, db.ForeignKey('hospital.id'))

    def __init__(self, pc, hospital_id):
        self.pc = pc
        self.hospital_id = hospital_id

    def __repr__(self):
        return '<pc %r>' % self.pc


