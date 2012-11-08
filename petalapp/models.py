from petalapp import db

ROLE_USER = 0
ROLE_ADMIN = 1

hospitals = db.Table('Hospital',
        db.Column('hospital_id', db.Integer, db.ForeignKey('hospitals.id')),
        db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
        )

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    #name = db.Column(db.String(80))
    #mail = db.Column(db.String(150), unique=True)
    #role = db.Column(db.SmallInteger, default=ROLE_USER)

    hospitals = db.relationship('Hospital', secondary=hospitals,
            backref=db.backref('users', lazy='dynamic'))

    #def __repr__(self):
    #    return '<Name %r>' % self.name

class Hospital(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    #Data = db.relationship('Data', backref = 'H_backref', lazy = 'dynamic')

    #def __repr__(self):
    #    return '<Hospital %r>' % self.name

#class Data(db.Model):
#    id = db.Column(db.Integer, primary_key=True)
#    hospital_id = db.Column(db.Integer, db.ForeignKey('Hospital.id'))
#    PC = db.Column(db.Integer)
#
#    def __repr__(self):
#        return '<Pc Well %r>' % self.PC
#    #and so on...
#

# labels for Categories.
#    labels = ["PC team wellness", "Interdisciplinary Team", "Coverage/Ability",
#        "Standard Form", "Initial PC evaluation", "Hospital PC screening",
#        "PC follow up", "Post Discharge Services", "Bereavement Contacts",
#        "Marking and Education","Marking and Education", "Care coordination",
#        "Availability", "Family Centerdness", "PC Networking",
#        "Education and training", "Certification"]



