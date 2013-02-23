from petalapp import db
ROLE_VIEWER = 0
ROLE_CONTRIBUTER = 1
ROLE_ADMIN = 2

organizations = db.Table('organizations',
        db.Column('organization_id', db.Integer, db.ForeignKey('organization.id')),
        db.Column('user_id', db.Integer, db.ForeignKey('user.id')))

class User(db.Model):
    """User has a many-to-many relationship with Organization"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=True)
    role = db.Column(db.SmallInteger, default=ROLE_VIEWER)
    answers = db.relationship('Answer', backref='user',lazy='dynamic')
    survey_comments = db.relationship('SurveyComment', backref='user', lazy='dynamic')
    user_survey_sections = db.relationship('UserSurveySection', backref='user', lazy='dynamic')
    organizations = db.relationship('Organization',
            secondary=organizations,
        backref=db.backref('users', lazy='dynamic'))

    def __init__(self, name='', role=ROLE_VIEWER): #FIXME: redundant
        self.role = role
        self.name = name

    #TODO what information to show?
    def __repr__(self):
        return self.name

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)


    def add_retrive(self, name):
        user = User.query.filter_by(name=name).first()
        if not user:
            user = User(name=name)
            db.session.add(user)
            db.session.commit()
        return user




survey_headers = db.Table('survey_headers',
        db.Column('survey_header_id', db.Integer, db.ForeignKey('survey_header.id')),
        db.Column('organization_id', db.Integer, db.ForeignKey('organization.id')))



class Organization(db.Model):
    """
    Organization has a many-to-one relationship with Market
    Organization has a  one-to-many relationship with survey_headers
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    survey_headers = db.relationship('SurveyHeader',
            secondary=survey_headers,backref=db.backref('organizations',lazy='dynamic'))
    user_survey_sections = db.relationship('UserSurveySection', backref='organization',
            lazy='dynamic')
    market_id = db.Column(db.Integer, db.ForeignKey('market.id'))

    def __init__(self, name=''):
        self.name = name

    def __repr__(self):
        return self.name



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
        return self.name



class SurveyHeader(db.Model):
    """
    Survey_header has a many-to-one relationship with Organization
    Survey_header has a one-to-many relationship with survey section_name
    Survey_header has a one-to-many relationship with survey_comments
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    other_info =  db.Column(db.String(250))

    survey_sections = db.relationship('SurveySection', backref='survey_header',lazy='dynamic')
    survey_comments = db.relationship('SurveyComment', backref='survey_header',lazy='dynamic')
    instructions = db.Column(db.String(3000))



    def __init__(self, name='',instructions='',other_info='' ):
        self.name = name
        self.instructions = instructions
        self.other_info =other_info


    def __repr__(self):

        return self.name


class SurveyComment(db.Model):
    """
    Survey_comments has a many-to-one relationship with Survey_header
    Survey_comments has a many-to-one relationship with Users
    """
    id = db.Column(db.Integer, primary_key=True)
    comments = db.Column(db.String(3000))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    survey_header_id = db.Column(db.Integer, db.ForeignKey('survey_header.id'))

    def __init__(self, comments=''):
        self.comments = comments

    def __repr__(self):
        return self.comments


class SurveySection(db.Model):
    """
    Survey_section has a many-to-one relationship with Survey_header
    Survey_section has a one-to-many relationship with User_survey_section
    Survey_section has a one-to-many relationship with Question
    """
    id = db.Column(db.Integer, primary_key=True)
    order = db.Column(db.Integer)
    name = db.Column(db.String(100),unique=True)
    subheading = db.Column(db.String(1200))
    required_yn = db.Column(db.Boolean)
    user_survey_sections = db.relationship('UserSurveySection', backref="survey_section",
            lazy='dynamic')
    questions = db.relationship('Question', backref='survey_section', lazy='dynamic')
    children = db.relationship('SurveySection', lazy='dynamic')
    survey_header_id = db.Column(db.Integer, db.ForeignKey('survey_header.id'))
    parent_id = db.Column(db.Integer, db.ForeignKey('survey_section.id'))



    def __init__(self,name='',section_required_yn=False,order=0,subheading='', ):
        self.name = name
        self.section_required_yn = section_required_yn
        self.order = order
        self.subheading = subheading

    def __repr__(self):
        return self.name

class Period(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    start = db.Column(db.DateTime)
    end = db.Column(db.DateTime)
    name = db.Column(db.String(100), unique=True)
    user_survey_sections = db.relationship('UserSurveySection', backref='period',
            lazy='dynamic')

    def __init__(self, name=None, start=None, end=None):
        self.name = name
        self.start = start
        self.end = end

    def __repr__(self):
        return '<name: %r\n start: %r\n end:%r>' % (self.name,self.start,self.end)

class AssignedDue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    due = db.Column(db.DateTime )
    assigned = db.Column(db.DateTime)
    user_survey_sections = db.relationship('UserSurveySection', backref='assigned_due',
            lazy='dynamic')

    def __init__(self, assigned=None, due=None):
        self.assigned = assigned
        self.due = due

    def __repr__(self):
        return '<assigned: %r\n due: %r >' % (self.assigned, self.due)



class UserSurveySection(db.Model):
    """
    User_survey_section has a many-to-one relationship with Survey_section
    User_survey_section has a many-to-many relationship with User
    """
    id = db.Column(db.Integer, primary_key=True)
    completed_date = db.Column(db.DateTime)
    answers = db.relationship('Answer', backref='user_survey_section',
            lazy='dynamic')
    survey_section_id = db.Column(db.Integer, db.ForeignKey('survey_section.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    data_id = db.Column(db.Integer, db.ForeignKey('data.id'))
    organization_id = db.Column(db.Integer, db.ForeignKey('organization.id'))
    period_id = db.Column(db.Integer, db.ForeignKey('period.id'))
    assigned_due_id = db.Column(db.Integer, db.ForeignKey('assigned_due.id'))


    def __init__(self, completed=None): #datetime.datetime.utcnow())
        self.completed = completed

    def __repr__(self):
        return "<completed date: %r>" % self.completed_date






class Answer(db.Model):
    """
    Answer has a many-to-one relationship with User
    Answer has a many-to-one relationship with Question_options
    Answer has a many-to-one relationship with Unit_of_measurement
    """
    id = db.Column(db.Integer, primary_key=True)
    numeric = db.Column(db.Integer)
    text = db.Column(db.String(500))
    tf = db.Column(db.Boolean)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    question_option_id = db.Column(db.Integer, db.ForeignKey('question_option.id'))
    unit_of_measurement_id = db.Column(db.Integer, db.ForeignKey('unit_of_measurement.id'))
    user_survey_section_id = db.Column(db.Integer, db.ForeignKey('user_survey_section.id'))


    def __init__(self, numeric=None, text=None, tf=None):
        self.numeric = numeric
        self.tf = tf
        self.text = text

class UnitOfMeasurement(db.Model):
    """
    Unit_of_measurement has a one-to-many relationship with Answer
    """
    id = db.Column(db.Integer, primary_key=True)
    answers = db.relationship('Answer', backref='unit_of_measurement', lazy='dynamic')
    name = db.Column(db.String(80),unique=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name


class QuestionOption(db.Model):
    """
    Question_option has a many-to-one relationship with Option_choice
    Question_option has a many-to-one relationship with Question
    Question_option has a one-to-many relationship with Answer
    """
    id = db.Column(db.Integer, primary_key=True)
    answers = db.relationship('Answer', backref='question_option',lazy='dynamic')
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))
    option_choice_id = db.Column(db.Integer, db.ForeignKey('option_choice.id'))

class OptionChoice(db.Model):
    """
    Option_choice has a many-to-one relationship with Option_group
    Option_choice has a one-to-many relationship with Question_option
    """
    id = db.Column(db.Integer, primary_key=True)
    question_options = db.relationship('QuestionOption', backref='option_choice',lazy='dynamic')
    option_group_id = db.Column(db.Integer, db.ForeignKey('option_group.id'))
    name = db.Column(db.String(200), unique=True)

    def __init__(self, name=''):
        self.name = name

    def __repr__(self):
        return self.name


class OptionGroup(db.Model):
    """
    Option_group has a one-to-many relationship with Option_choice
    Option_group has a one-to-many relationship with Question
    """
    id = db.Column(db.Integer, primary_key=True)
    option_choices = db.relationship('OptionChoice', backref='option_group',lazy='dynamic')
    questions = db.relationship('Question', backref ='option_group', lazy='dynamic')
    name = db.Column(db.String(50), unique=True)

    def __init__(self, name=''):
        self.name = name

    def __repr__(self):
        return self.name


class Question(db.Model):
    """
    Question has a many-to-one relationship with Survey_section
    Question has a many-to-one relationship with Input_type
    Question has a many-to-one relationship with Option_group
    Question has a one-to-many relationship with Question_option
    """
    id = db.Column(db.Integer, primary_key=True)
    question_options = db.relationship('QuestionOption', backref='question',lazy='dynamic')
    survey_section_id = db.Column(db.Integer, db.ForeignKey('survey_section.id'))
    inputtype_id = db.Column(db.Integer, db.ForeignKey('input_type.id'))
    option_group_id = db.Column(db.Integer, db.ForeignKey('option_group.id'))


    #TODO old look over
    name = db.Column(db.String(500),unique=True)
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
        return self.name


class InputType(db.Model):
    """Input_type has a one to many relationship with Question"""
    id = db.Column(db.Integer, primary_key=True)
    questions = db.relationship('Question', backref='input_type', lazy='dynamic')
    name = db.Column(db.String(50),unique=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<name: %r>' % self.name



class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    standard_form = db.Column(db.Integer)
    marketing_education = db.Column(db.Integer)
    record_availability = db.Column(db.Integer)
    family_centerdness = db.Column(db.Integer)
    pc_networking = db.Column(db.Integer)
    education_and_training = db.Column(db.Integer)
    team_funding = db.Column(db.Integer)
    coverage = db.Column(db.Integer)
    pc_for_expired_pts = db.Column(db.Integer)
    hospital_pc_screening  = db.Column(db.Integer)
    pc_follow_up = db.Column(db.Integer)
    post_discharge_services = db.Column(db.Integer)
    bereavement_contacts = db.Column(db.Integer)
    certification = db.Column(db.Integer)
    team_wellness = db.Column(db.Integer)
    care_coordination = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime)
    url = db.Column(db.String(300))

    user_survey_sections = db.relationship('UserSurveySection', backref='data',
            lazy='dynamic')
    def __init__(self, standard_form=0,
            marketing_education=0, record_availability=0, family_centerdness=0,
        pc_networking=0, education_and_training=0, team_funding=0,
        coverage=0, pc_for_expired_pts=0, hospital_pc_screening=0,
        pc_follow_up=0, post_discharge_services=0, bereavement_contacts=0,
        certification=0, team_wellness=0, care_coordination=0, timestamp=None):

            self.standard_form = standard_form
            self.marketing_education =  marketing_education
            self.record_availability = record_availability
            self.family_centerdness =  family_centerdness
            self.pc_networking =  pc_networking
            self.education_and_training =  education_and_training
            self.team_funding =  team_funding
            self.coverage =  coverage
            self.pc_for_expired_pts =  pc_for_expired_pts
            self.hospital_pc_screening  =  hospital_pc_screening
            self.pc_follow_up =  pc_follow_up
            self.post_discharge_services =  post_discharge_services
            self.bereavement_contacts =  bereavement_contacts
            self.certification =  certification
            self.team_wellness =  team_wellness
            self.care_coordination = care_coordination
            self.timestamp = timestamp

    def __repr__(self):
        return """ %r, %r, %r, %r, %r, %r, %r, %r, %r, %r, %r, %r, %r, %r, %r, %r, %r  %r""" % (self.standard_form,
    self.marketing_education,
    self.record_availability,
    self.family_centerdness,
    self.pc_networking,
    self.education_and_training,
    self.team_funding,
    self.coverage,
    self.pc_for_expired_pts,
    self.hospital_pc_screening ,
    self.pc_follow_up,
    self.post_discharge_services,
    self.bereavement_contacts,
    self.certification,
    self.team_wellness,
    self.care_coordination,
    self.timestamp,
    self.url)
        # """
    # <standard_form : %r>\n
    # <marketing_education : %r>\n
    # <record_availability : %r>\n
    # <family_centerdness : %r>\n
    # <pc_networking : %r>\n
    # <education_and_training : %r>\n
    # <team_funding : %r>\n
    # <coverage : %r>\n
    # <pc_for_expired_pts : %r>\n
    # <hospital_pc_screening  : %r>\n
    # <pc_follow_up : %r>\n
    # <post_discharge_services : %r>\n
    # <bereavement_contacts : %r>\n
    # <certification : %r>\n
    # <team_wellness : %r>\n
    # <care_coordination : %r>\n
    # <datetime_utc  : %r>""" % (

# @event.listens_for(Session, 'after_flush')
# def delete_many_to_many(session, ctx):
#     session.query(SurveyHeader).filter(SurveyHeader.organizations.any()).delete(synchronize_session=False)
#     session.query(Organization).filter(Organization.users.any()).delete(synchronize_session=False)

