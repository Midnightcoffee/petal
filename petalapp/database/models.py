from petalapp import db

ROLE_VIEWER = 0
ROLE_CONTRIBUTER = 1
ROLE_ADMIN = 2

import datetime

class User(db.Model):
    """User has a many-to-many relationship with Organization"""

    id = db.Column(db.Integer, primary_key=True)
    survey_comments = db.relationship('SurveyComment', backref='user', lazy='dynamic')
    answers = db.relationship('Answer', backref='user',lazy='dynamic')
    email = db.Column(db.String(150), unique=True)
    role = db.Column(db.SmallInteger, default=ROLE_VIEWER)
    user_survey_sections = db.relationship('UserSurveySection', backref='user', lazy='dynamic')

    def __init__(self, email, role=ROLE_VIEWER): #FIXME: redundant
        self.role = role
        self.email = email

    #TODO what information to show?
    def __repr__(self):
        return '<email: %r>' % (self.email)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)


    def add_retrive(self, user_name):
        user = User.query.filter_by(name=user_name).first()
        if not user:
            user = User(name=user_name)
            db.session.add(user)
            db.session.commit()
        return user


class Organization(db.Model):
    """
    Organization has a many-to-one relationship with Market
    Organization has a  one-to-many relationship with survey_headers

    """

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    survey_headers = db.relationship('SurveyHeader', backref='organization', lazy='dynamic')
    market_id = db.Column(db.Integer, db.ForeignKey('market.id'))

    def __init__(self, name=''):
        self.name = name

    def __repr__(self):
        return '<Name: %r>' % self.name


class Market(db.Model):
    """
    Market has a one-to-many relationship with Organization
    """
    id = db.Column(db.Integer, primary_key=True)
    organizations = db.relationship('Organization', backref='market', lazy='dynamic')
    name = db.Column(db.String(80))

    def __init__(self, name=''):
        self.name = name

    def __repr__(self):
        return '<name : %r >' % self.name




class SurveyHeader(db.Model):
    """
    Survey_header has a many-to-one relationship with Organization
    Survey_header has a one-to-many relationship with survey section_name
    Survey_header has a one-to-many relationship with survey_comments
    """
    id = db.Column(db.Integer, primary_key=True)
    organization_id = db.Column(db.Integer, db.ForeignKey('organization.id'))
    survey_sections = db.relationship('SurveySection', backref='survey_header',lazy='dynamic')
    survey_comments = db.relationship('SurveyComment', backref='survey_header',lazy='dynamic')
    name = db.Column(db.String(80))
    instructions = db.Column(db.String(3000))
    other_info =  db.Column(db.String(250))
    time_period = db.Column(db.String(200))


    def __init__(self, name='',instructions='',other_info='', time_period=''):
        self.name = name
        self.instructions = instructions
        self.other_info =other_info
        self.time_period = time_period

    def __repr__(self):

        return '<survey name: %r>' % self.name


class SurveyComment(db.Model):
    """
    Survey_comments has a many-to-one relationship with Survey_header
    Survey_comments has a many-to-one relationship with Users
    """
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    survey_header_id = db.Column(db.Integer, db.ForeignKey('survey_header.id'))
    comments = db.Column(db.String(3000))


    def __init__(self, comments=''):
        self.comments = comments

    def __repr__(self):
        return '<comments: %r>' % self.comments


class SurveySection(db.Model):
    """
    Survey_section has a many-to-one relationship with Survey_header
    Survey_section has a one-to-many relationship with User_survey_section
    Survey_section has a one-to-many relationship with Question
    """
    id = db.Column(db.Integer, primary_key=True)
    survey_header_id = db.Column(db.Integer, db.ForeignKey('survey_header.id'))
    parent_id = Column(db.Integer, db.ForeignKey('surveysection.id'))
    user_survey_sections = db.relationship('UserSurveySection', backref="survey_section",
            lazy='dynamic')
    questions = db.relationship('Question', backref='survey_section', lazy='dynamic')
    order = db.Column(db.Integer)
    name = db.Column(db.String(100))
    subheading = db.Column(db.String(1200))
    required_yn = db.Column(db.Boolean)
    time_period = db.Column(db.String(100))
    children = db.relationship('SurveySection', backref='survey_section', lazy='dynamic')



    def __init__(self,name='',section_required_yn=False,order=0, time_period=''
            ,subheading=''):
        self.name = name
        self.section_required_yn = section_required_yn
        self.order = order
        self.time_period = time_period
        self.subheading = subheading

    def __repr__(self):
        return '<survey name: %r>' % self.name

class UserSurveySection(db.Model):
    """
    User_survey_section has a many-to-one relationship with Survey_section
    User_survey_section has a many-to-many relationship with User
    """
    id = db.Column(db.Integer, primary_key=True)
    survey_section_id = db.Column(db.Integer, db.ForeignKey('survey_section.id'))
    completed_date = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, completed_date=None):
        self.completed_date = completed_date
        #datetime.datetime.utcnow()

    def __repr__(self):
        return '<completed on: %r>' % self.completed_date



class Answer(db.Model):
    """
    Answer has a many-to-one relationship with User
    Answer has a many-to-one relationship with Question_options
    Answer has a many-to-one relationship with Unit_of_measurement
    """
    id = db.Column(db.Integer, primary_key=True)
    numeric = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    question_option_id = db.Column(db.Integer, db.ForeignKey('question_option.id'))
    unit_of_measurement_id = db.Column(db.Integer, db.ForeignKey('unit_of_measurement.id'))
    #organization_id = db.Column(db.Integer, db.ForeignKey('organization.id'))
    #question_id = db.Column(db.Integer, db.ForeignKey('question.id'))
    #survey_id = db.Column(db.Integer, db.ForeignKey('survey.id'))

    def __init__(self, numeric=0):
        self.numeric = numeric

    #TODO a dynamic one?
    def __repr__(self):
        return '<Answer numeric: %r>' % self.numeric


class UnitOfMeasurement(db.Model):
    """
    Unit_of_measurement has a one-to-many relationship with Answer
    """
    id = db.Column(db.Integer, primary_key=True)
    answers = db.relationship('Answer', backref='unit_of_measurement', lazy='dynamic')
    name = db.Column(db.String(80))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<name: %r>' % self.name


class QuestionOption(db.Model):
    """
    Question_option has a many-to-one relationship with Option_choice
    Question_option has a many-to-one relationship with Question
    Question_option has a one-to-many relationship with Answer
    """
    id = db.Column(db.Integer, primary_key=True)
    answers = db.relationship('Answer', backref='question_option',lazy='dynamic')
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))
    Option_choice_id = db.Column(db.Integer, db.ForeignKey('option_choice.id'))

class OptionChoice(db.Model):
    """
    Option_choice has a many-to-one relationship with Option_group
    Option_choice has a one-to-many relationship with Question_option
    """
    id = db.Column(db.Integer, primary_key=True)
    question_options = db.relationship('QuestionOption', backref='option_choice',lazy='dynamic')
    option_group_id = db.Column(db.Integer, db.ForeignKey('option_group.id'))

    name = db.Column(db.String(200))

    def __init__(self, name=''):
        self.name = name

    def __repr__(self):
        return '<option choice name: %r >' % self.name


class OptionGroup(db.Model):
    """
    Option_group has a one-to-many relationship with Option_choice
    Option_group has a one-to-many relationship with Question
    """
    id = db.Column(db.Integer, primary_key=True)
    option_choices = db.relationship('OptionChoice', backref='option_group',lazy='dynamic')
    questions = db.relationship('Question', backref ='option_group', lazy='dynamic')
    name = db.Column(db.String(50))

    def __init__(self, name=''):
        self.name = name

    def __repr__(self):
        return '<name: %r >' % self.name


class Question(db.Model):
    """
    Question has a many-to-one relationship with Survey_section
    Question has a many-to-one relationship with Input_type
    Question has a many-to-one relationship with Option_group
    Question has a one-to-many relationship with Question_option
    """
    id = db.Column(db.Integer, primary_key=True)
    survey_section_id = db.Column(db.Integer, db.ForeignKey('survey_section.id'))
    inputtype_id = db.Column(db.Integer, db.ForeignKey('input_type.id'))
    option_group_id = db.Column(db.Integer, db.ForeignKey('option_group.id'))
    question_options = db.relationship('QuestionOption', backref='question',lazy='dynamic')

    #TODO old look over
    name = db.Column(db.String(500))
    order = db.Column(db.Integer)
    value = db.Column(db.Integer)
    answer_required_yn =db.Column(db.Boolean)
    subtext = db.Column(db.String(500))
    allow_mult_options_answers_yn = db.Column(db.Boolean)



    #answers = db.relationship('Answer', backref='question', lazy='dynamic')

    def __init__(
            self, name='',
            order=0, value=0, answer_required_yn=False, subtext='',
            allow_mult_options_answers_yn=False
                ):

        self.name = name
        self.value = value
        self.order = order
        self.answer_required_yn = answer_required_yn
        self.subtext = subtext
        self.allow_mult_options_answers_yn = allow_mult_options_answers_yn

    def __repr__(self):
        return '<Question name: %r>' % self.name


class InputType(db.Model):
    """Input_type has a one to many relationship with Question"""
    id = db.Column(db.Integer, primary_key=True)
    questions = db.relationship('Question', backref='input_type', lazy='dynamic')
    input_type = db.Column(db.String(50))

    def __init__(self, input_type):
        self.input_type = input_type

    def __repr__(self):
        return '<Input_type: %r>' % self.input_type





