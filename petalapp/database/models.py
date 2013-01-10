from petalapp import db

ROLE_VIEWER = 0
ROLE_CONTRIBUTER = 1
ROLE_ADMIN = 2

import datetime

#TODO:rename?
hospitals = db.Table('hospitals',
    db.Column('hospital_id', db.Integer, db.ForeignKey('hospital.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
)

class User(db.Model):
    """User has a many-to-many relationship with Hospital"""

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    role = db.Column(db.SmallInteger, default=ROLE_VIEWER)

    hospitals = db.relationship('Hospital', secondary=hospitals,
        backref=db.backref('users', lazy='dynamic'))

    def __init__(self, email, role=ROLE_VIEWER): #FIXME: redundant
        self.role = role
        self.email = email

    #TODO what information to show?
    def __repr__(self):
        return '<email: %r>' % (self.email)

    def add_hospital(self, hospital):
        if not (hospital in self.hospitals):
            self.hospitals.append(hospital)

    def remove_hospital(self, hospital):
        if not (hospital in self.hospital):
            self.hospitals.remove(hospital)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)


class Hospital(db.Model):
    """Hospital's has a one-to-many relationship with answer and a
    many-to-many relationship with User"""

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    answer = db.relationship('Answer', backref='hospital', lazy = 'dynamic')

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Name: %r>' % self.name

class Answer(db.Model):
    """Answers has a many to one relationship with Hospital, a one to
    many relationship with Question and a many to one relationship with survey"""

    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Integer)
    hospital_id = db.Column(db.Integer, db.ForeignKey('hospital.id'))
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))
    survey_id = db.Column(db.Integer, db.ForeignKey('survey.id'))

    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return '<Answer: %r>' % self.value


class Question(db.Model):
    """Question has a one to many to one relationship with Answer"""
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(300))
    point = db.Column(db.Integer)
    answers = db.relationship('Answer', backref='question', lazy='dynamic')
    question_header_id = db.Column(db.Integer, db.ForeignKey('question_header.id'))


    def __init__(self, key, point):
        self.key = key
        self.point = point

    def __repr__(self):
        return '<Question: %r>' % self.key



class Question_header(db.Model):
    """Question_header has a one to many relationship with question"""
    id = db.Column(db.Integer, primary_key=True)
    header = db.Column(db.String(600))
    questions = db.relationship('Question', backref='question_header',lazy='dynamic')

    def __init__(self, header):
        self.header = header

    def __repr__(self):
        return '<header: %r>' % self.header



class Survey(db.Model):
    """survey has a one to may relationship with  answer"""
    id = db.Column(db.Integer, primary_key=True)
    answers = db.relationship('Answer', backref='survey', lazy='dynamic')
    release  = db.Column(db.String(50))
    timestamp = db.Column(db.DateTime)

    def __init__(self, release,timestamp=datetime.datetime.utcnow()):
        self.release = release
        self.timestamp = timestamp

def __repr__(self):
    return '<Release: %r>' % self.release






