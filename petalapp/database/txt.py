commit 6f834aadc1ef3432daef9ff07e1be0007a9707fc
Author: Drew Verlee <Drew.verlee@gmail.com>
Date:   Thu Feb 7 01:08:17 2013 -0500

    cleaner code for storing info

diff --git a/petalapp/database/models.py b/petalapp/database/models.py
index 5879d6e..ac43a10 100644
--- a/petalapp/database/models.py
+++ b/petalapp/database/models.py
@@ -95,10 +95,10 @@ class SurveyHeader(db.Model):
     name = db.Column(db.String(80))
     instructions = db.Column(db.String(3000))
     other_info =  db.Column(db.String(250))
-    time_period = db.Column(db.String(200))
+    time_period = db.Column(db.Integer)
 
 
-    def __init__(self, name='',instructions='',other_info='', time_period=''):
+    def __init__(self, time_period, name='',instructions='',other_info='', ):
         self.name = name
         self.instructions = instructions
         self.other_info =other_info
@@ -135,7 +135,7 @@ class SurveySection(db.Model):
     """
     id = db.Column(db.Integer, primary_key=True)
     survey_header_id = db.Column(db.Integer, db.ForeignKey('survey_header.id'))
-    parent_id = Column(db.Integer, db.ForeignKey('surveysection.id'))
+    parent_id = db.Column(db.Integer, db.ForeignKey('survey_section.id'))
     user_survey_sections = db.relationship('UserSurveySection', backref="survey_section",
             lazy='dynamic')
     questions = db.relationship('Question', backref='survey_section', lazy='dynamic')
@@ -144,12 +144,12 @@ class SurveySection(db.Model):
     subheading = db.Column(db.String(1200))
     required_yn = db.Column(db.Boolean)
     time_period = db.Column(db.String(100))
-    children = db.relationship('SurveySection', backref='survey_section', lazy='dynamic')
+    children = db.relationship('SurveySection', lazy='dynamic')
 
 
 
     def __init__(self,name='',section_required_yn=False,order=0, time_period=''
-            ,subheading=''):
+            ,subheading='', ):
         self.name = name
         self.section_required_yn = section_required_yn
         self.order = order

commit ddf5efcb2fa90099eefffaa900e2592dd6ea0d53
Author: Drew Verlee <Drew.verlee@gmail.com>
Date:   Mon Jan 28 19:19:45 2013 -0500

    removed question.head,tail,etc.. replaced with name

diff --git a/petalapp/database/models.py b/petalapp/database/models.py
index d6930f4..5879d6e 100644
--- a/petalapp/database/models.py
+++ b/petalapp/database/models.py
@@ -141,17 +141,20 @@ class SurveySection(db.Model):
     questions = db.relationship('Question', backref='survey_section', lazy='dynamic')
     order = db.Column(db.Integer)
     name = db.Column(db.String(100))
+    subheading = db.Column(db.String(1200))
     required_yn = db.Column(db.Boolean)
     time_period = db.Column(db.String(100))
     children = db.relationship('SurveySection', backref='survey_section', lazy='dynamic')
 
 
 
-    def __init__(self,name='',section_required_yn=False,order=0, time_period=''):
+    def __init__(self,name='',section_required_yn=False,order=0, time_period=''
+            ,subheading=''):
         self.name = name
         self.section_required_yn = section_required_yn
         self.order = order
         self.time_period = time_period
+        self.subheading = subheading
 
     def __repr__(self):
         return '<survey name: %r>' % self.name
@@ -273,9 +276,7 @@ class Question(db.Model):
     question_options = db.relationship('QuestionOption', backref='question',lazy='dynamic')
 
     #TODO old look over
-    full = db.Column(db.String(1500))
-    tail = db.Column(db.String(750))
-    head = db.Column(db.String(1000))
+    name = db.Column(db.String(500))
     order = db.Column(db.Integer)
     value = db.Column(db.Integer)
     answer_required_yn =db.Column(db.Boolean)
@@ -287,14 +288,12 @@ class Question(db.Model):
     #answers = db.relationship('Answer', backref='question', lazy='dynamic')
 
     def __init__(
-            self, full='',tail='',head='',
+            self, name='',
             order=0, value=0, answer_required_yn=False, subtext='',
             allow_mult_options_answers_yn=False
                 ):
 
-        self.full = full
-        self.tail = tail
-        self.head = head
+        self.name = name
         self.value = value
         self.order = order
         self.answer_required_yn = answer_required_yn
@@ -302,7 +301,7 @@ class Question(db.Model):
         self.allow_mult_options_answers_yn = allow_mult_options_answers_yn
 
     def __repr__(self):
-        return '<Question full: %r>' % self.full
+        return '<Question name: %r>' % self.name
 
 
 class InputType(db.Model):

commit a20d66bac4173354934c3f730ca932a74b175cee
Author: Drew Verlee <Drew.verlee@gmail.com>
Date:   Sun Jan 27 21:34:09 2013 -0500

    creating adjacency list relationships

diff --git a/petalapp/database/models.py b/petalapp/database/models.py
index 8ff0a60..d6930f4 100644
--- a/petalapp/database/models.py
+++ b/petalapp/database/models.py
@@ -135,6 +135,7 @@ class SurveySection(db.Model):
     """
     id = db.Column(db.Integer, primary_key=True)
     survey_header_id = db.Column(db.Integer, db.ForeignKey('survey_header.id'))
+    parent_id = Column(db.Integer, db.ForeignKey('surveysection.id'))
     user_survey_sections = db.relationship('UserSurveySection', backref="survey_section",
             lazy='dynamic')
     questions = db.relationship('Question', backref='survey_section', lazy='dynamic')
@@ -142,6 +143,8 @@ class SurveySection(db.Model):
     name = db.Column(db.String(100))
     required_yn = db.Column(db.Boolean)
     time_period = db.Column(db.String(100))
+    children = db.relationship('SurveySection', backref='survey_section', lazy='dynamic')
+
 
 
     def __init__(self,name='',section_required_yn=False,order=0, time_period=''):

commit 481a0a1f01b4967865ca35036393ba686b6da05a
Author: Drew Verlee <Drew.verlee@gmail.com>
Date:   Sun Jan 27 20:42:15 2013 -0500

    before survey recursion

diff --git a/petalapp/database/models.py b/petalapp/database/models.py
index 9f3138b..8ff0a60 100644
--- a/petalapp/database/models.py
+++ b/petalapp/database/models.py
@@ -146,7 +146,6 @@ class SurveySection(db.Model):
 
     def __init__(self,name='',section_required_yn=False,order=0, time_period=''):
         self.name = name
-        self.name = name
         self.section_required_yn = section_required_yn
         self.order = order
         self.time_period = time_period
@@ -249,11 +248,9 @@ class OptionGroup(db.Model):
     option_choices = db.relationship('OptionChoice', backref='option_group',lazy='dynamic')
     questions = db.relationship('Question', backref ='option_group', lazy='dynamic')
     name = db.Column(db.String(50))
-    head = db.Column(db.String(300))
 
-    def __init__(self, name='',head=''):
+    def __init__(self, name=''):
         self.name = name
-        self.list_head = head
 
     def __repr__(self):
         return '<name: %r >' % self.name
@@ -275,6 +272,7 @@ class Question(db.Model):
     #TODO old look over
     full = db.Column(db.String(1500))
     tail = db.Column(db.String(750))
+    head = db.Column(db.String(1000))
     order = db.Column(db.Integer)
     value = db.Column(db.Integer)
     answer_required_yn =db.Column(db.Boolean)
@@ -286,12 +284,14 @@ class Question(db.Model):
     #answers = db.relationship('Answer', backref='question', lazy='dynamic')
 
     def __init__(
-            self, full='',tail='',
+            self, full='',tail='',head='',
             order=0, value=0, answer_required_yn=False, subtext='',
             allow_mult_options_answers_yn=False
                 ):
 
         self.full = full
+        self.tail = tail
+        self.head = head
         self.value = value
         self.order = order
         self.answer_required_yn = answer_required_yn
@@ -299,7 +299,7 @@ class Question(db.Model):
         self.allow_mult_options_answers_yn = allow_mult_options_answers_yn
 
     def __repr__(self):
-        return '<Question name: %r>' % self.name
+        return '<Question full: %r>' % self.full
 
 
 class InputType(db.Model):

commit 0b98b3394f9185e139e018995d59493ec7153422
Author: Drew Verlee <Drew.verlee@gmail.com>
Date:   Wed Jan 23 17:00:20 2013 -0500

    cleaning up files

diff --git a/petalapp/database/models.py b/petalapp/database/models.py
index 60799ec..9f3138b 100644
--- a/petalapp/database/models.py
+++ b/petalapp/database/models.py
@@ -139,20 +139,20 @@ class SurveySection(db.Model):
             lazy='dynamic')
     questions = db.relationship('Question', backref='survey_section', lazy='dynamic')
     order = db.Column(db.Integer)
-    title = db.Column(db.String(100))
+    name = db.Column(db.String(100))
     required_yn = db.Column(db.Boolean)
     time_period = db.Column(db.String(100))
 
 
-    def __init__(self,title='',section_required_yn=False,order=0, time_period=''):
-        self.title = title
-        self.title = title
+    def __init__(self,name='',section_required_yn=False,order=0, time_period=''):
+        self.name = name
+        self.name = name
         self.section_required_yn = section_required_yn
         self.order = order
         self.time_period = time_period
 
     def __repr__(self):
-        return '<survey title: %r>' % self.title
+        return '<survey name: %r>' % self.name
 
 class UserSurveySection(db.Model):
     """

commit 3d6e174c8d0513f7601e3e6c84af9194e5cc3083
Author: Drew Verlee <Drew.verlee@gmail.com>
Date:   Mon Jan 14 18:59:46 2013 -0500

    building pages dyamically based on user selection

diff --git a/petalapp/database/models.py b/petalapp/database/models.py
index 5b192a3..60799ec 100644
--- a/petalapp/database/models.py
+++ b/petalapp/database/models.py
@@ -41,6 +41,8 @@ class User(db.Model):
         user = User.query.filter_by(name=user_name).first()
         if not user:
             user = User(name=user_name)
+            db.session.add(user)
+            db.session.commit()
         return user
 
 
@@ -62,13 +64,6 @@ class Organization(db.Model):
     def __repr__(self):
         return '<Name: %r>' % self.name
 
-    def add_retrive(self, organization_name):
-        org = Organization.query.filter_by(name=organization_name).first()
-        if not org:
-            org = Organization(name=organization_name)
-        return org
-
-
 
 class Market(db.Model):
     """
@@ -84,11 +79,6 @@ class Market(db.Model):
     def __repr__(self):
         return '<name : %r >' % self.name
 
-    def add_retrive(self, market_name):
-        market = Market.query.filter_by(name=market_name).first()
-        if not market:
-            market = Market(name=market_name)
-        return market
 
 
 
@@ -325,12 +315,6 @@ class InputType(db.Model):
         return '<Input_type: %r>' % self.input_type
 
 
-    def add_retrive(self,input_name):
-        inpt = InputType.query.filter_by(name=input_name).first()
-        if not inpt:
-            inpt = InputType(Input_type=input_name)
-        return inpt
-
 
 
 

commit a7d7d2d6eed34edc8af3b0c1e234b25b4637f334
Author: Drew Verlee <Drew.verlee@gmail.com>
Date:   Mon Jan 14 11:20:53 2013 -0500

    created some uniqueness methods on classes

diff --git a/petalapp/database/models.py b/petalapp/database/models.py
index 6ac07b0..5b192a3 100644
--- a/petalapp/database/models.py
+++ b/petalapp/database/models.py
@@ -5,21 +5,7 @@ ROLE_CONTRIBUTER = 1
 ROLE_ADMIN = 2
 
 import datetime
-#hospitals = db.Table('hospitals',
-#    db.Column('hospital_id', db.Integer, db.ForeignKey('hospital.id', ondelete="CASCADE")),
-#    db.Column('user_id', db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"))
-#)
-#
-#organizations = db.Table('organizations',
-#    db.Column('organization_id', db.Integer, db.ForeignKey('organization.id',ondelete='cascade')),
-#    db.Column('user_id', db.Integer, db.ForeignKey('user.id', ondelete='cascade'))
-#)
-#
-##user_survey_sections = db.Table('user_survey_sections',
-##    db.Column('user_survey_section_id'), db.Integer, db.ForeignKey('user_survey_section.id'),
-##    db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
-##    )
-#
+
 class User(db.Model):
     """User has a many-to-many relationship with Organization"""
 
@@ -30,13 +16,6 @@ class User(db.Model):
     role = db.Column(db.SmallInteger, default=ROLE_VIEWER)
     user_survey_sections = db.relationship('UserSurveySection', backref='user', lazy='dynamic')
 
-#    organizations = db.relationship('Organization', secondary=organizations,
-#        backref=db.backref('users', lazy='dynamic'))
-
-    #user_survey_sections = db.relationship('User_survey_section', seciondary=user_survey_sections,
-    #        backref=db.backref('users', lazy='dynamic'))
-
-
     def __init__(self, email, role=ROLE_VIEWER): #FIXME: redundant
         self.role = role
         self.email = email
@@ -45,15 +24,6 @@ class User(db.Model):
     def __repr__(self):
         return '<email: %r>' % (self.email)
 
-    #TODO maybe alter these to do the connection for us?
-#    def add_organization(self, organization):
-#        if not (organization in self.organizations):
-#            self.organizations.append(organization)
-#
-#    def remove_organization(self, organization):
-#        if not (organization in self.organization):
-#            self.organizations.remove(organization)
-
     def is_authenticated(self):
         return True
 
@@ -67,6 +37,13 @@ class User(db.Model):
         return unicode(self.id)
 
 
+    def add_retrive(self, user_name):
+        user = User.query.filter_by(name=user_name).first()
+        if not user:
+            user = User(name=user_name)
+        return user
+
+
 class Organization(db.Model):
     """
     Organization has a many-to-one relationship with Market
@@ -85,6 +62,14 @@ class Organization(db.Model):
     def __repr__(self):
         return '<Name: %r>' % self.name
 
+    def add_retrive(self, organization_name):
+        org = Organization.query.filter_by(name=organization_name).first()
+        if not org:
+            org = Organization(name=organization_name)
+        return org
+
+
+
 class Market(db.Model):
     """
     Market has a one-to-many relationship with Organization
@@ -99,6 +84,13 @@ class Market(db.Model):
     def __repr__(self):
         return '<name : %r >' % self.name
 
+    def add_retrive(self, market_name):
+        market = Market.query.filter_by(name=market_name).first()
+        if not market:
+            market = Market(name=market_name)
+        return market
+
+
 
 class SurveyHeader(db.Model):
     """
@@ -108,19 +100,22 @@ class SurveyHeader(db.Model):
     """
     id = db.Column(db.Integer, primary_key=True)
     organization_id = db.Column(db.Integer, db.ForeignKey('organization.id'))
-    sections = db.relationship('SurveySection', backref='survey_header',lazy='dynamic')
-    comments = db.relationship('SurveyComment', backref='survey_header',lazy='dynamic')
+    survey_sections = db.relationship('SurveySection', backref='survey_header',lazy='dynamic')
+    survey_comments = db.relationship('SurveyComment', backref='survey_header',lazy='dynamic')
     name = db.Column(db.String(80))
     instructions = db.Column(db.String(3000))
     other_info =  db.Column(db.String(250))
+    time_period = db.Column(db.String(200))
 
 
-    def __init__(self, name='',instructions='',other_info=''):
+    def __init__(self, name='',instructions='',other_info='', time_period=''):
         self.name = name
         self.instructions = instructions
         self.other_info =other_info
+        self.time_period = time_period
 
     def __repr__(self):
+
         return '<survey name: %r>' % self.name
 
 
@@ -156,16 +151,18 @@ class SurveySection(db.Model):
     order = db.Column(db.Integer)
     title = db.Column(db.String(100))
     required_yn = db.Column(db.Boolean)
+    time_period = db.Column(db.String(100))
 
 
-    def __init__(self,title='',section_required_yn=False,order=0):
+    def __init__(self,title='',section_required_yn=False,order=0, time_period=''):
         self.title = title
         self.title = title
         self.section_required_yn = section_required_yn
         self.order = order
+        self.time_period = time_period
 
     def __repr__(self):
-        return '<survey name: %r>' % self.name
+        return '<survey title: %r>' % self.title
 
 class UserSurveySection(db.Model):
     """
@@ -177,8 +174,9 @@ class UserSurveySection(db.Model):
     completed_date = db.Column(db.DateTime)
     user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
 
-    def __init__(self, completed_date=datetime.datetime.utcnow()):
+    def __init__(self, completed_date=None):
         self.completed_date = completed_date
+        #datetime.datetime.utcnow()
 
     def __repr__(self):
         return '<completed on: %r>' % self.completed_date
@@ -327,7 +325,11 @@ class InputType(db.Model):
         return '<Input_type: %r>' % self.input_type
 
 
-
+    def add_retrive(self,input_name):
+        inpt = InputType.query.filter_by(name=input_name).first()
+        if not inpt:
+            inpt = InputType(Input_type=input_name)
+        return inpt
 
 
 

commit 2b3e0ae43db955ee502b3208463159d2c8e242ac
Author: Drew Verlee <Drew.verlee@gmail.com>
Date:   Sun Jan 13 19:41:32 2013 -0500

    start place for altering pci form2

diff --git a/petalapp/database/models.py b/petalapp/database/models.py
index 6070fbf..6ac07b0 100644
--- a/petalapp/database/models.py
+++ b/petalapp/database/models.py
@@ -24,10 +24,11 @@ class User(db.Model):
     """User has a many-to-many relationship with Organization"""
 
     id = db.Column(db.Integer, primary_key=True)
-    survey_comments = db.relationship('Survey_comment', backref='user', lazy='dynamic')
+    survey_comments = db.relationship('SurveyComment', backref='user', lazy='dynamic')
     answers = db.relationship('Answer', backref='user',lazy='dynamic')
     email = db.Column(db.String(150), unique=True)
     role = db.Column(db.SmallInteger, default=ROLE_VIEWER)
+    user_survey_sections = db.relationship('UserSurveySection', backref='user', lazy='dynamic')
 
 #    organizations = db.relationship('Organization', secondary=organizations,
 #        backref=db.backref('users', lazy='dynamic'))
@@ -67,20 +68,37 @@ class User(db.Model):
 
 
 class Organization(db.Model):
-    """Organization's has a one-to-many relationship with answer and a
-    many-to-many relationship with User"""
+    """
+    Organization has a many-to-one relationship with Market
+    Organization has a  one-to-many relationship with survey_headers
+
+    """
 
     id = db.Column(db.Integer, primary_key=True)
     name = db.Column(db.String(80))
-    #answers = db.relationship('Answer', backref='organization', lazy = 'dynamic')
-    survey_headers = db.relationship('Survey_header', backref='organization', lazy='dynamic')
+    survey_headers = db.relationship('SurveyHeader', backref='organization', lazy='dynamic')
+    market_id = db.Column(db.Integer, db.ForeignKey('market.id'))
 
-    def __init__(self, name):
+    def __init__(self, name=''):
         self.name = name
 
     def __repr__(self):
         return '<Name: %r>' % self.name
 
+class Market(db.Model):
+    """
+    Market has a one-to-many relationship with Organization
+    """
+    id = db.Column(db.Integer, primary_key=True)
+    organizations = db.relationship('Organization', backref='market', lazy='dynamic')
+    name = db.Column(db.String(80))
+
+    def __init__(self, name=''):
+        self.name = name
+
+    def __repr__(self):
+        return '<name : %r >' % self.name
+
 
 class SurveyHeader(db.Model):
     """
@@ -90,20 +108,20 @@ class SurveyHeader(db.Model):
     """
     id = db.Column(db.Integer, primary_key=True)
     organization_id = db.Column(db.Integer, db.ForeignKey('organization.id'))
-    survey_sections = db.relationship('Survey_section', backref='survey_header',lazy='dynamic')
-    survey_comments = db.relationship('Survey_comment', backref='survey_header',lazy='dynamic')
-    survey_name = db.Column(db.String(80))
+    sections = db.relationship('SurveySection', backref='survey_header',lazy='dynamic')
+    comments = db.relationship('SurveyComment', backref='survey_header',lazy='dynamic')
+    name = db.Column(db.String(80))
     instructions = db.Column(db.String(3000))
     other_info =  db.Column(db.String(250))
 
 
-    def __init__(self, survey_name='',instructions='',other_info=''):
-        self.survey_name = survey_name
+    def __init__(self, name='',instructions='',other_info=''):
+        self.name = name
         self.instructions = instructions
         self.other_info =other_info
 
     def __repr__(self):
-        return '<survey name: %r>' % self.survey_name
+        return '<survey name: %r>' % self.name
 
 
 class SurveyComment(db.Model):
@@ -132,18 +150,19 @@ class SurveySection(db.Model):
     """
     id = db.Column(db.Integer, primary_key=True)
     survey_header_id = db.Column(db.Integer, db.ForeignKey('survey_header.id'))
-    user_survey_sections = db.relationship('User_survey_section', backref="survey_section",
+    user_survey_sections = db.relationship('UserSurveySection', backref="survey_section",
             lazy='dynamic')
     questions = db.relationship('Question', backref='survey_section', lazy='dynamic')
-    name = db.Column(db.String(45))
-    title = db.Column(db.String(45))
+    order = db.Column(db.Integer)
+    title = db.Column(db.String(100))
     required_yn = db.Column(db.Boolean)
 
 
-    def __init__(self, name='',title='',section_required_yn=False):
-        self.name = name
+    def __init__(self,title='',section_required_yn=False,order=0):
+        self.title = title
         self.title = title
         self.section_required_yn = section_required_yn
+        self.order = order
 
     def __repr__(self):
         return '<survey name: %r>' % self.name
@@ -156,6 +175,7 @@ class UserSurveySection(db.Model):
     id = db.Column(db.Integer, primary_key=True)
     survey_section_id = db.Column(db.Integer, db.ForeignKey('survey_section.id'))
     completed_date = db.Column(db.DateTime)
+    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
 
     def __init__(self, completed_date=datetime.datetime.utcnow()):
         self.completed_date = completed_date
@@ -220,7 +240,7 @@ class OptionChoice(db.Model):
     Option_choice has a one-to-many relationship with Question_option
     """
     id = db.Column(db.Integer, primary_key=True)
-    question_options = db.relationship('Question_option', backref='option_choice',lazy='dynamic')
+    question_options = db.relationship('QuestionOption', backref='option_choice',lazy='dynamic')
     option_group_id = db.Column(db.Integer, db.ForeignKey('option_group.id'))
 
     name = db.Column(db.String(200))
@@ -238,12 +258,14 @@ class OptionGroup(db.Model):
     Option_group has a one-to-many relationship with Question
     """
     id = db.Column(db.Integer, primary_key=True)
-    option_choices = db.relationship('Option_choice', backref='option_group',lazy='dynamic')
+    option_choices = db.relationship('OptionChoice', backref='option_group',lazy='dynamic')
     questions = db.relationship('Question', backref ='option_group', lazy='dynamic')
     name = db.Column(db.String(50))
+    head = db.Column(db.String(300))
 
-    def __init__(self, name=''):
+    def __init__(self, name='',head=''):
         self.name = name
+        self.list_head = head
 
     def __repr__(self):
         return '<name: %r >' % self.name
@@ -260,14 +282,13 @@ class Question(db.Model):
     survey_section_id = db.Column(db.Integer, db.ForeignKey('survey_section.id'))
     inputtype_id = db.Column(db.Integer, db.ForeignKey('input_type.id'))
     option_group_id = db.Column(db.Integer, db.ForeignKey('option_group.id'))
-    question_options = db.relationship('Question_option', backref='question',lazy='dynamic')
+    question_options = db.relationship('QuestionOption', backref='question',lazy='dynamic')
 
     #TODO old look over
-    full_text = db.Column(db.String(1500))
-    head_text = db.Column(db.String(750))
-    tail_text = db.Column(db.String(750))
+    full = db.Column(db.String(1500))
+    tail = db.Column(db.String(750))
     order = db.Column(db.Integer)
-    point = db.Column(db.Integer)
+    value = db.Column(db.Integer)
     answer_required_yn =db.Column(db.Boolean)
     subtext = db.Column(db.String(500))
     allow_mult_options_answers_yn = db.Column(db.Boolean)
@@ -276,17 +297,14 @@ class Question(db.Model):
 
     #answers = db.relationship('Answer', backref='question', lazy='dynamic')
 
-
-
     def __init__(
-            self, full_text='',  head_text='',tail_text='',
-            order=0, point=0, answer_required_yn=False, subtext='',
+            self, full='',tail='',
+            order=0, value=0, answer_required_yn=False, subtext='',
             allow_mult_options_answers_yn=False
                 ):
 
-        self.full_text = full_text
-        self.head_text = head_text
-        self.point = point
+        self.full = full
+        self.value = value
         self.order = order
         self.answer_required_yn = answer_required_yn
         self.subtext = subtext

commit 5ab192f312622ebb22d4e056da6d08a3563b4dbc
Author: Drew Verlee <Drew.verlee@gmail.com>
Date:   Sun Jan 13 11:58:30 2013 -0500

    style change to db

diff --git a/petalapp/database/models.py b/petalapp/database/models.py
index 6f05178..6070fbf 100644
--- a/petalapp/database/models.py
+++ b/petalapp/database/models.py
@@ -5,22 +5,36 @@ ROLE_CONTRIBUTER = 1
 ROLE_ADMIN = 2
 
 import datetime
-
-#TODO:rename?
-hospitals = db.Table('hospitals',
-    db.Column('hospital_id', db.Integer, db.ForeignKey('hospital.id')),
-    db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
-)
-
+#hospitals = db.Table('hospitals',
+#    db.Column('hospital_id', db.Integer, db.ForeignKey('hospital.id', ondelete="CASCADE")),
+#    db.Column('user_id', db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"))
+#)
+#
+#organizations = db.Table('organizations',
+#    db.Column('organization_id', db.Integer, db.ForeignKey('organization.id',ondelete='cascade')),
+#    db.Column('user_id', db.Integer, db.ForeignKey('user.id', ondelete='cascade'))
+#)
+#
+##user_survey_sections = db.Table('user_survey_sections',
+##    db.Column('user_survey_section_id'), db.Integer, db.ForeignKey('user_survey_section.id'),
+##    db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
+##    )
+#
 class User(db.Model):
-    """User has a many-to-many relationship with Hospital"""
+    """User has a many-to-many relationship with Organization"""
 
     id = db.Column(db.Integer, primary_key=True)
+    survey_comments = db.relationship('Survey_comment', backref='user', lazy='dynamic')
+    answers = db.relationship('Answer', backref='user',lazy='dynamic')
     email = db.Column(db.String(150), unique=True)
     role = db.Column(db.SmallInteger, default=ROLE_VIEWER)
 
-    hospitals = db.relationship('Hospital', secondary=hospitals,
-        backref=db.backref('users', lazy='dynamic'))
+#    organizations = db.relationship('Organization', secondary=organizations,
+#        backref=db.backref('users', lazy='dynamic'))
+
+    #user_survey_sections = db.relationship('User_survey_section', seciondary=user_survey_sections,
+    #        backref=db.backref('users', lazy='dynamic'))
+
 
     def __init__(self, email, role=ROLE_VIEWER): #FIXME: redundant
         self.role = role
@@ -30,13 +44,14 @@ class User(db.Model):
     def __repr__(self):
         return '<email: %r>' % (self.email)
 
-    def add_hospital(self, hospital):
-        if not (hospital in self.hospitals):
-            self.hospitals.append(hospital)
-
-    def remove_hospital(self, hospital):
-        if not (hospital in self.hospital):
-            self.hospitals.remove(hospital)
+    #TODO maybe alter these to do the connection for us?
+#    def add_organization(self, organization):
+#        if not (organization in self.organizations):
+#            self.organizations.append(organization)
+#
+#    def remove_organization(self, organization):
+#        if not (organization in self.organization):
+#            self.organizations.remove(organization)
 
     def is_authenticated(self):
         return True
@@ -51,13 +66,14 @@ class User(db.Model):
         return unicode(self.id)
 
 
-class Hospital(db.Model):
-    """Hospital's has a one-to-many relationship with answer and a
+class Organization(db.Model):
+    """Organization's has a one-to-many relationship with answer and a
     many-to-many relationship with User"""
 
     id = db.Column(db.Integer, primary_key=True)
     name = db.Column(db.String(80))
-    answers = db.relationship('Answer', backref='hospital', lazy = 'dynamic')
+    #answers = db.relationship('Answer', backref='organization', lazy = 'dynamic')
+    survey_headers = db.relationship('Survey_header', backref='organization', lazy='dynamic')
 
     def __init__(self, name):
         self.name = name
@@ -65,86 +81,233 @@ class Hospital(db.Model):
     def __repr__(self):
         return '<Name: %r>' % self.name
 
-class Answer(db.Model):
-    """Answers has a many to one relationship with Hospital, a one to
-    many relationship with Question and a many to one relationship with survey"""
 
+class SurveyHeader(db.Model):
+    """
+    Survey_header has a many-to-one relationship with Organization
+    Survey_header has a one-to-many relationship with survey section_name
+    Survey_header has a one-to-many relationship with survey_comments
+    """
     id = db.Column(db.Integer, primary_key=True)
-    value = db.Column(db.Integer)
-    hospital_id = db.Column(db.Integer, db.ForeignKey('hospital.id'))
-    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))
-    survey_id = db.Column(db.Integer, db.ForeignKey('survey.id'))
+    organization_id = db.Column(db.Integer, db.ForeignKey('organization.id'))
+    survey_sections = db.relationship('Survey_section', backref='survey_header',lazy='dynamic')
+    survey_comments = db.relationship('Survey_comment', backref='survey_header',lazy='dynamic')
+    survey_name = db.Column(db.String(80))
+    instructions = db.Column(db.String(3000))
+    other_info =  db.Column(db.String(250))
 
-    def __init__(self, value=0):
-        self.value = value
+
+    def __init__(self, survey_name='',instructions='',other_info=''):
+        self.survey_name = survey_name
+        self.instructions = instructions
+        self.other_info =other_info
 
     def __repr__(self):
-        return '<Answer: %r>' % self.value
+        return '<survey name: %r>' % self.survey_name
 
 
-class Question(db.Model):
-    """Question has a one to many to one relationship with Answer"""
+class SurveyComment(db.Model):
+    """
+    Survey_comments has a many-to-one relationship with Survey_header
+    Survey_comments has a many-to-one relationship with Users
+    """
     id = db.Column(db.Integer, primary_key=True)
-    key = db.Column(db.String(300))
-    point = db.Column(db.Integer)
-    answers = db.relationship('Answer', backref='question', lazy='dynamic')
-    header_id = db.Column(db.Integer, db.ForeignKey('header.id'))
-    inputtype_id = db.Column(db.Integer, db.ForeignKey('inputtype.id'))
-    order = db.Column(db.Integer)
+    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
+    survey_header_id = db.Column(db.Integer, db.ForeignKey('survey_header.id'))
+    comments = db.Column(db.String(3000))
 
 
-    def __init__(self, key, point, order):
-        self.key = key
-        self.point = point
-        self.order = order
+    def __init__(self, comments=''):
+        self.comments = comments
 
     def __repr__(self):
-        return '<Question: %r>' % self.key
+        return '<comments: %r>' % self.comments
 
 
-class Inputtype(db.Model):
-    """Inputtype has a one to many relationship with Question"""
+class SurveySection(db.Model):
+    """
+    Survey_section has a many-to-one relationship with Survey_header
+    Survey_section has a one-to-many relationship with User_survey_section
+    Survey_section has a one-to-many relationship with Question
+    """
     id = db.Column(db.Integer, primary_key=True)
-    questions = db.relationship('Question', backref='inputtype', lazy='dynamic')
-    input_type = db.Column(db.String(50))
+    survey_header_id = db.Column(db.Integer, db.ForeignKey('survey_header.id'))
+    user_survey_sections = db.relationship('User_survey_section', backref="survey_section",
+            lazy='dynamic')
+    questions = db.relationship('Question', backref='survey_section', lazy='dynamic')
+    name = db.Column(db.String(45))
+    title = db.Column(db.String(45))
+    required_yn = db.Column(db.Boolean)
 
-    def __init__(self, input_type):
-        self.input_type = input_type
+
+    def __init__(self, name='',title='',section_required_yn=False):
+        self.name = name
+        self.title = title
+        self.section_required_yn = section_required_yn
 
     def __repr__(self):
-        return '<Inputtype: %r>' % self.input_type
+        return '<survey name: %r>' % self.name
 
-class Header(db.Model):
-    """header has a one to many relationship with question"""
+class UserSurveySection(db.Model):
+    """
+    User_survey_section has a many-to-one relationship with Survey_section
+    User_survey_section has a many-to-many relationship with User
+    """
     id = db.Column(db.Integer, primary_key=True)
-    header = db.Column(db.String(600))
-    questions = db.relationship('Question', backref='header',lazy='dynamic')
-    order = db.Column(db.Integer)
+    survey_section_id = db.Column(db.Integer, db.ForeignKey('survey_section.id'))
+    completed_date = db.Column(db.DateTime)
 
-    def __init__(self, header,order):
-        self.header = header
-        self.order = order
+    def __init__(self, completed_date=datetime.datetime.utcnow()):
+        self.completed_date = completed_date
 
     def __repr__(self):
-        return '<header: %r>' % self.header
+        return '<completed on: %r>' % self.completed_date
+
+
+
+class Answer(db.Model):
+    """
+    Answer has a many-to-one relationship with User
+    Answer has a many-to-one relationship with Question_options
+    Answer has a many-to-one relationship with Unit_of_measurement
+    """
+    id = db.Column(db.Integer, primary_key=True)
+    numeric = db.Column(db.Integer)
+    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
+    question_option_id = db.Column(db.Integer, db.ForeignKey('question_option.id'))
+    unit_of_measurement_id = db.Column(db.Integer, db.ForeignKey('unit_of_measurement.id'))
+    #organization_id = db.Column(db.Integer, db.ForeignKey('organization.id'))
+    #question_id = db.Column(db.Integer, db.ForeignKey('question.id'))
+    #survey_id = db.Column(db.Integer, db.ForeignKey('survey.id'))
+
+    def __init__(self, numeric=0):
+        self.numeric = numeric
+
+    #TODO a dynamic one?
+    def __repr__(self):
+        return '<Answer numeric: %r>' % self.numeric
+
 
+class UnitOfMeasurement(db.Model):
+    """
+    Unit_of_measurement has a one-to-many relationship with Answer
+    """
+    id = db.Column(db.Integer, primary_key=True)
+    answers = db.relationship('Answer', backref='unit_of_measurement', lazy='dynamic')
+    name = db.Column(db.String(80))
 
+    def __init__(self, name):
+        self.name = name
 
-class Survey(db.Model):
-    """survey has a one to may relationship with  answer"""
+    def __repr__(self):
+        return '<name: %r>' % self.name
+
+
+class QuestionOption(db.Model):
+    """
+    Question_option has a many-to-one relationship with Option_choice
+    Question_option has a many-to-one relationship with Question
+    Question_option has a one-to-many relationship with Answer
+    """
     id = db.Column(db.Integer, primary_key=True)
-    answers = db.relationship('Answer', backref='survey', lazy='dynamic')
-    release  = db.Column(db.String(50))
-    timestamp = db.Column(db.DateTime)
+    answers = db.relationship('Answer', backref='question_option',lazy='dynamic')
+    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))
+    Option_choice_id = db.Column(db.Integer, db.ForeignKey('option_choice.id'))
+
+class OptionChoice(db.Model):
+    """
+    Option_choice has a many-to-one relationship with Option_group
+    Option_choice has a one-to-many relationship with Question_option
+    """
+    id = db.Column(db.Integer, primary_key=True)
+    question_options = db.relationship('Question_option', backref='option_choice',lazy='dynamic')
+    option_group_id = db.Column(db.Integer, db.ForeignKey('option_group.id'))
+
+    name = db.Column(db.String(200))
+
+    def __init__(self, name=''):
+        self.name = name
+
+    def __repr__(self):
+        return '<option choice name: %r >' % self.name
+
+
+class OptionGroup(db.Model):
+    """
+    Option_group has a one-to-many relationship with Option_choice
+    Option_group has a one-to-many relationship with Question
+    """
+    id = db.Column(db.Integer, primary_key=True)
+    option_choices = db.relationship('Option_choice', backref='option_group',lazy='dynamic')
+    questions = db.relationship('Question', backref ='option_group', lazy='dynamic')
+    name = db.Column(db.String(50))
+
+    def __init__(self, name=''):
+        self.name = name
+
+    def __repr__(self):
+        return '<name: %r >' % self.name
+
+
+class Question(db.Model):
+    """
+    Question has a many-to-one relationship with Survey_section
+    Question has a many-to-one relationship with Input_type
+    Question has a many-to-one relationship with Option_group
+    Question has a one-to-many relationship with Question_option
+    """
+    id = db.Column(db.Integer, primary_key=True)
+    survey_section_id = db.Column(db.Integer, db.ForeignKey('survey_section.id'))
+    inputtype_id = db.Column(db.Integer, db.ForeignKey('input_type.id'))
+    option_group_id = db.Column(db.Integer, db.ForeignKey('option_group.id'))
+    question_options = db.relationship('Question_option', backref='question',lazy='dynamic')
+
+    #TODO old look over
+    full_text = db.Column(db.String(1500))
+    head_text = db.Column(db.String(750))
+    tail_text = db.Column(db.String(750))
     order = db.Column(db.Integer)
+    point = db.Column(db.Integer)
+    answer_required_yn =db.Column(db.Boolean)
+    subtext = db.Column(db.String(500))
+    allow_mult_options_answers_yn = db.Column(db.Boolean)
 
-    def __init__(self, release, order, timestamp=datetime.datetime.utcnow()):
-        self.release = release
-        self.timestamp = timestamp
+
+
+    #answers = db.relationship('Answer', backref='question', lazy='dynamic')
+
+
+
+    def __init__(
+            self, full_text='',  head_text='',tail_text='',
+            order=0, point=0, answer_required_yn=False, subtext='',
+            allow_mult_options_answers_yn=False
+                ):
+
+        self.full_text = full_text
+        self.head_text = head_text
+        self.point = point
         self.order = order
+        self.answer_required_yn = answer_required_yn
+        self.subtext = subtext
+        self.allow_mult_options_answers_yn = allow_mult_options_answers_yn
 
     def __repr__(self):
-        return '<Release: %r>' % self.release
+        return '<Question name: %r>' % self.name
+
+
+class InputType(db.Model):
+    """Input_type has a one to many relationship with Question"""
+    id = db.Column(db.Integer, primary_key=True)
+    questions = db.relationship('Question', backref='input_type', lazy='dynamic')
+    input_type = db.Column(db.String(50))
+
+    def __init__(self, input_type):
+        self.input_type = input_type
+
+    def __repr__(self):
+        return '<Input_type: %r>' % self.input_type
+
 
 
 

commit 09a09739a4b39ba64332d0475746a2f93f539f63
Author: Drew Verlee <Drew.verlee@gmail.com>
Date:   Sat Jan 12 13:12:21 2013 -0500

    building from to db amazon logic up

diff --git a/petalapp/database/models.py b/petalapp/database/models.py
index eee9452..6f05178 100644
--- a/petalapp/database/models.py
+++ b/petalapp/database/models.py
@@ -143,8 +143,8 @@ class Survey(db.Model):
         self.timestamp = timestamp
         self.order = order
 
-def __repr__(self):
-    return '<Release: %r>' % self.release
+    def __repr__(self):
+        return '<Release: %r>' % self.release
 
 
 

commit 98d009585edbdcf42d5300b8ece021b852f55ab8
Author: Drew Verlee <Drew.verlee@gmail.com>
Date:   Sat Jan 12 00:39:44 2013 -0500

    added input type model

diff --git a/petalapp/database/models.py b/petalapp/database/models.py
index afa1402..eee9452 100644
--- a/petalapp/database/models.py
+++ b/petalapp/database/models.py
@@ -88,7 +88,8 @@ class Question(db.Model):
     key = db.Column(db.String(300))
     point = db.Column(db.Integer)
     answers = db.relationship('Answer', backref='question', lazy='dynamic')
-    question_header_id = db.Column(db.Integer, db.ForeignKey('question_header.id'))
+    header_id = db.Column(db.Integer, db.ForeignKey('header.id'))
+    inputtype_id = db.Column(db.Integer, db.ForeignKey('inputtype.id'))
     order = db.Column(db.Integer)
 
 
@@ -101,12 +102,23 @@ class Question(db.Model):
         return '<Question: %r>' % self.key
 
 
+class Inputtype(db.Model):
+    """Inputtype has a one to many relationship with Question"""
+    id = db.Column(db.Integer, primary_key=True)
+    questions = db.relationship('Question', backref='inputtype', lazy='dynamic')
+    input_type = db.Column(db.String(50))
+
+    def __init__(self, input_type):
+        self.input_type = input_type
+
+    def __repr__(self):
+        return '<Inputtype: %r>' % self.input_type
 
-class Question_header(db.Model):
-    """Question_header has a one to many relationship with question"""
+class Header(db.Model):
+    """header has a one to many relationship with question"""
     id = db.Column(db.Integer, primary_key=True)
     header = db.Column(db.String(600))
-    questions = db.relationship('Question', backref='question_header',lazy='dynamic')
+    questions = db.relationship('Question', backref='header',lazy='dynamic')
     order = db.Column(db.Integer)
 
     def __init__(self, header,order):

commit 4d93aef375d6ca1cf58b8f97addd14e988cffa9b
Author: Drew Verlee <Drew.verlee@gmail.com>
Date:   Fri Jan 11 22:23:32 2013 -0500

    loads of stuff, made a table in my survey

diff --git a/petalapp/database/models.py b/petalapp/database/models.py
index 8581a17..afa1402 100644
--- a/petalapp/database/models.py
+++ b/petalapp/database/models.py
@@ -57,7 +57,7 @@ class Hospital(db.Model):
 
     id = db.Column(db.Integer, primary_key=True)
     name = db.Column(db.String(80))
-    answer = db.relationship('Answer', backref='hospital', lazy = 'dynamic')
+    answers = db.relationship('Answer', backref='hospital', lazy = 'dynamic')
 
     def __init__(self, name):
         self.name = name
@@ -75,7 +75,7 @@ class Answer(db.Model):
     question_id = db.Column(db.Integer, db.ForeignKey('question.id'))
     survey_id = db.Column(db.Integer, db.ForeignKey('survey.id'))
 
-    def __init__(self, value):
+    def __init__(self, value=0):
         self.value = value
 
     def __repr__(self):
@@ -89,11 +89,13 @@ class Question(db.Model):
     point = db.Column(db.Integer)
     answers = db.relationship('Answer', backref='question', lazy='dynamic')
     question_header_id = db.Column(db.Integer, db.ForeignKey('question_header.id'))
+    order = db.Column(db.Integer)
 
 
-    def __init__(self, key, point):
+    def __init__(self, key, point, order):
         self.key = key
         self.point = point
+        self.order = order
 
     def __repr__(self):
         return '<Question: %r>' % self.key
@@ -105,9 +107,11 @@ class Question_header(db.Model):
     id = db.Column(db.Integer, primary_key=True)
     header = db.Column(db.String(600))
     questions = db.relationship('Question', backref='question_header',lazy='dynamic')
+    order = db.Column(db.Integer)
 
-    def __init__(self, header):
+    def __init__(self, header,order):
         self.header = header
+        self.order = order
 
     def __repr__(self):
         return '<header: %r>' % self.header
@@ -120,10 +124,12 @@ class Survey(db.Model):
     answers = db.relationship('Answer', backref='survey', lazy='dynamic')
     release  = db.Column(db.String(50))
     timestamp = db.Column(db.DateTime)
+    order = db.Column(db.Integer)
 
-    def __init__(self, release,timestamp=datetime.datetime.utcnow()):
+    def __init__(self, release, order, timestamp=datetime.datetime.utcnow()):
         self.release = release
         self.timestamp = timestamp
+        self.order = order
 
 def __repr__(self):
     return '<Release: %r>' % self.release

commit 1535d933ba2c7763bcb484ed6239c9a4b781bed4
Author: Drew Verlee <Drew.verlee@gmail.com>
Date:   Thu Jan 10 01:12:11 2013 -0500

    updated survey to db

diff --git a/petalapp/database/models.py b/petalapp/database/models.py
index 20c2596..8581a17 100644
--- a/petalapp/database/models.py
+++ b/petalapp/database/models.py
@@ -86,11 +86,14 @@ class Question(db.Model):
     """Question has a one to many to one relationship with Answer"""
     id = db.Column(db.Integer, primary_key=True)
     key = db.Column(db.String(300))
+    point = db.Column(db.Integer)
     answers = db.relationship('Answer', backref='question', lazy='dynamic')
     question_header_id = db.Column(db.Integer, db.ForeignKey('question_header.id'))
 
-    def __init__(self, key):
+
+    def __init__(self, key, point):
         self.key = key
+        self.point = point
 
     def __repr__(self):
         return '<Question: %r>' % self.key

commit 6c098b1bd454a9e09a7300d236a83dc31c2ebaad
Author: Drew Verlee <Drew.verlee@gmail.com>
Date:   Wed Jan 9 16:32:46 2013 -0500

    reloaded sslify to get logs

diff --git a/petalapp/database/models.py b/petalapp/database/models.py
index 1335cd5..20c2596 100644
--- a/petalapp/database/models.py
+++ b/petalapp/database/models.py
@@ -22,7 +22,7 @@ class User(db.Model):
     hospitals = db.relationship('Hospital', secondary=hospitals,
         backref=db.backref('users', lazy='dynamic'))
 
-    def __init__(self, email, role=ROLE_VIEWER): #FIXME: redundant 
+    def __init__(self, email, role=ROLE_VIEWER): #FIXME: redundant
         self.role = role
         self.email = email
 
@@ -120,7 +120,7 @@ class Survey(db.Model):
 
     def __init__(self, release,timestamp=datetime.datetime.utcnow()):
         self.release = release
-        self.timestamp = timestamp 
+        self.timestamp = timestamp
 
 def __repr__(self):
     return '<Release: %r>' % self.release

commit d5bf8a949c1938de4755160250ea6f2570fdcca8
Author: Drew Verlee <Drew.verlee@gmail.com>
Date:   Wed Jan 9 16:18:13 2013 -0500

    changes made to build forms queing from db

diff --git a/petalapp/database/models.py b/petalapp/database/models.py
index 5d70293..1335cd5 100644
--- a/petalapp/database/models.py
+++ b/petalapp/database/models.py
@@ -4,6 +4,7 @@ ROLE_VIEWER = 0
 ROLE_CONTRIBUTER = 1
 ROLE_ADMIN = 2
 
+import datetime
 
 #TODO:rename?
 hospitals = db.Table('hospitals',
@@ -27,7 +28,7 @@ class User(db.Model):
 
     #TODO what information to show?
     def __repr__(self):
-        return '<email : %r>' % (self.email)
+        return '<email: %r>' % (self.email)
 
     def add_hospital(self, hospital):
         if not (hospital in self.hospitals):
@@ -62,7 +63,7 @@ class Hospital(db.Model):
         self.name = name
 
     def __repr__(self):
-        return '<Name %r>' % self.name
+        return '<Name: %r>' % self.name
 
 class Answer(db.Model):
     """Answers has a many to one relationship with Hospital, a one to
@@ -74,19 +75,41 @@ class Answer(db.Model):
     question_id = db.Column(db.Integer, db.ForeignKey('question.id'))
     survey_id = db.Column(db.Integer, db.ForeignKey('survey.id'))
 
+    def __init__(self, value):
+        self.value = value
+
+    def __repr__(self):
+        return '<Answer: %r>' % self.value
+
 
 class Question(db.Model):
     """Question has a one to many to one relationship with Answer"""
     id = db.Column(db.Integer, primary_key=True)
     key = db.Column(db.String(300))
     answers = db.relationship('Answer', backref='question', lazy='dynamic')
+    question_header_id = db.Column(db.Integer, db.ForeignKey('question_header.id'))
+
+    def __init__(self, key):
+        self.key = key
+
+    def __repr__(self):
+        return '<Question: %r>' % self.key
+
 
 
 class Question_header(db.Model):
     """Question_header has a one to many relationship with question"""
     id = db.Column(db.Integer, primary_key=True)
     header = db.Column(db.String(600))
-    questions = db.relationship('Queston', backref='question_header',lazy='dynamic')
+    questions = db.relationship('Question', backref='question_header',lazy='dynamic')
+
+    def __init__(self, header):
+        self.header = header
+
+    def __repr__(self):
+        return '<header: %r>' % self.header
+
+
 
 class Survey(db.Model):
     """survey has a one to may relationship with  answer"""
@@ -95,6 +118,15 @@ class Survey(db.Model):
     release  = db.Column(db.String(50))
     timestamp = db.Column(db.DateTime)
 
+    def __init__(self, release,timestamp=datetime.datetime.utcnow()):
+        self.release = release
+        self.timestamp = timestamp 
+
+def __repr__(self):
+    return '<Release: %r>' % self.release
+
+
+
 
 
 

commit 5b2c3e47b09f6f0edbc4babc8e567b0bb714c5b4
Author: Drew Verlee <Drew.verlee@gmail.com>
Date:   Wed Jan 9 13:46:42 2013 -0500

    added question header
    to db models

diff --git a/petalapp/database/models.py b/petalapp/database/models.py
index f208b9d..5d70293 100644
--- a/petalapp/database/models.py
+++ b/petalapp/database/models.py
@@ -78,10 +78,16 @@ class Answer(db.Model):
 class Question(db.Model):
     """Question has a one to many to one relationship with Answer"""
     id = db.Column(db.Integer, primary_key=True)
-    key = db.Column(db.String(500))
+    key = db.Column(db.String(300))
     answers = db.relationship('Answer', backref='question', lazy='dynamic')
 
 
+class Question_header(db.Model):
+    """Question_header has a one to many relationship with question"""
+    id = db.Column(db.Integer, primary_key=True)
+    header = db.Column(db.String(600))
+    questions = db.relationship('Queston', backref='question_header',lazy='dynamic')
+
 class Survey(db.Model):
     """survey has a one to may relationship with  answer"""
     id = db.Column(db.Integer, primary_key=True)

commit 3512ed01f10c84594da2239b2aff6c34850f2947
Author: Drew Verlee <Drew.verlee@gmail.com>
Date:   Sun Jan 6 21:36:23 2013 -0500

    created permissions heirarchy

diff --git a/petalapp/database/models.py b/petalapp/database/models.py
index fc7d7e5..f208b9d 100644
--- a/petalapp/database/models.py
+++ b/petalapp/database/models.py
@@ -21,7 +21,7 @@ class User(db.Model):
     hospitals = db.relationship('Hospital', secondary=hospitals,
         backref=db.backref('users', lazy='dynamic'))
 
-    def __init__(self, email, role=ROLE_VIEWER): #FIXME: redundent 
+    def __init__(self, email, role=ROLE_VIEWER): #FIXME: redundant 
         self.role = role
         self.email = email
 

commit 337c4f5700670f8e0da72baa0455925a7ee8368d
Author: Drew Verlee <Drew.verlee@gmail.com>
Date:   Sun Jan 6 21:12:18 2013 -0500

    created new pci html forms

diff --git a/petalapp/database/models.py b/petalapp/database/models.py
index bc61296..fc7d7e5 100644
--- a/petalapp/database/models.py
+++ b/petalapp/database/models.py
@@ -1,8 +1,8 @@
 from petalapp import db
 
-ROLE_VIEWER = 'viewer'
-ROLE_CONTRIBUTER = 'contributer'
-ROLE_ADMIN = 'admin'
+ROLE_VIEWER = 0
+ROLE_CONTRIBUTER = 1
+ROLE_ADMIN = 2
 
 
 #TODO:rename?
@@ -21,7 +21,7 @@ class User(db.Model):
     hospitals = db.relationship('Hospital', secondary=hospitals,
         backref=db.backref('users', lazy='dynamic'))
 
-    def __init__(self, email, role=ROLE_VIEWER):
+    def __init__(self, email, role=ROLE_VIEWER): #FIXME: redundent 
         self.role = role
         self.email = email
 

commit 9b20d8a73db922e96a00439f26a5c5928ee0e58e
Author: Drew Verlee <Drew.verlee@gmail.com>
Date:   Sun Jan 6 17:48:08 2013 -0500

    app using BroswerID functionality

diff --git a/petalapp/database/models.py b/petalapp/database/models.py
index 59cfaa8..bc61296 100644
--- a/petalapp/database/models.py
+++ b/petalapp/database/models.py
@@ -1,8 +1,8 @@
 from petalapp import db
 
-ROLE_VIEWER = 0
-ROLE_CONTRIBUTER = 1
-ROLE_ADMIN = 2
+ROLE_VIEWER = 'viewer'
+ROLE_CONTRIBUTER = 'contributer'
+ROLE_ADMIN = 'admin'
 
 
 #TODO:rename?
@@ -21,13 +21,13 @@ class User(db.Model):
     hospitals = db.relationship('Hospital', secondary=hospitals,
         backref=db.backref('users', lazy='dynamic'))
 
-    def __init__(self, nickname, email, password="OpenID",role=ROLE_VIEWER):
+    def __init__(self, email, role=ROLE_VIEWER):
         self.role = role
         self.email = email
 
     #TODO what information to show?
     def __repr__(self):
-        return '<Name : %r>' % (self.nickname)
+        return '<email : %r>' % (self.email)
 
     def add_hospital(self, hospital):
         if not (hospital in self.hospitals):
@@ -37,6 +37,18 @@ class User(db.Model):
         if not (hospital in self.hospital):
             self.hospitals.remove(hospital)
 
+    def is_authenticated(self):
+        return True
+
+    def is_active(self):
+        return True
+
+    def is_anonymous(self):
+        return False
+
+    def get_id(self):
+        return unicode(self.id)
+
 
 class Hospital(db.Model):
     """Hospital's has a one-to-many relationship with answer and a
@@ -44,7 +56,7 @@ class Hospital(db.Model):
 
     id = db.Column(db.Integer, primary_key=True)
     name = db.Column(db.String(80))
-    answer = db.relationship('answer', backref='hospital', lazy = 'dynamic')
+    answer = db.relationship('Answer', backref='hospital', lazy = 'dynamic')
 
     def __init__(self, name):
         self.name = name
@@ -67,13 +79,13 @@ class Question(db.Model):
     """Question has a one to many to one relationship with Answer"""
     id = db.Column(db.Integer, primary_key=True)
     key = db.Column(db.String(500))
-    answers = db.relationship('answer', backref='question', lazy='dynamic')
+    answers = db.relationship('Answer', backref='question', lazy='dynamic')
 
 
 class Survey(db.Model):
     """survey has a one to may relationship with  answer"""
     id = db.Column(db.Integer, primary_key=True)
-    answers = db.relationship('answer', backref='survey', lazy='dynamic')
+    answers = db.relationship('Answer', backref='survey', lazy='dynamic')
     release  = db.Column(db.String(50))
     timestamp = db.Column(db.DateTime)
 

commit 1fd051625e8a825721829198edd4069675e20915
Author: Drew Verlee <Drew.verlee@gmail.com>
Date:   Sun Jan 6 02:48:30 2013 -0500

    database changed

diff --git a/petalapp/database/models.py b/petalapp/database/models.py
index cfce664..59cfaa8 100644
--- a/petalapp/database/models.py
+++ b/petalapp/database/models.py
@@ -1,27 +1,27 @@
 from petalapp import db
-from datetime import datetime
-ROLE_USER = 0
-ROLE_ADMIN = 1
+
+ROLE_VIEWER = 0
+ROLE_CONTRIBUTER = 1
+ROLE_ADMIN = 2
+
 
 #TODO:rename?
 hospitals = db.Table('hospitals',
     db.Column('hospital_id', db.Integer, db.ForeignKey('hospital.id')),
     db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
 )
-# tags bmarks time
+
 class User(db.Model):
     """User has a many-to-many relationship with Hospital"""
 
     id = db.Column(db.Integer, primary_key=True)
-    nickname = db.Column(db.String(64), unique = True)
     email = db.Column(db.String(150), unique=True)
-    role = db.Column(db.SmallInteger, default=ROLE_USER)
+    role = db.Column(db.SmallInteger, default=ROLE_VIEWER)
 
     hospitals = db.relationship('Hospital', secondary=hospitals,
         backref=db.backref('users', lazy='dynamic'))
 
-    def __init__(self, nickname, email, password="OpenID",role=ROLE_USER):
-        self.nickname= nickname
+    def __init__(self, nickname, email, password="OpenID",role=ROLE_VIEWER):
         self.role = role
         self.email = email
 
@@ -29,18 +29,6 @@ class User(db.Model):
     def __repr__(self):
         return '<Name : %r>' % (self.nickname)
 
-    def is_authenticated(self):
-        return True
-
-    def is_active(self):
-        return True
-
-    def is_anonymous(self):
-        return False
-
-    def get_id(self):
-        return unicode(self.id)
-
     def add_hospital(self, hospital):
         if not (hospital in self.hospitals):
             self.hospitals.append(hospital)
@@ -50,26 +38,13 @@ class User(db.Model):
             self.hospitals.remove(hospital)
 
 
-    @staticmethod
-    def make_unique_nickname(nickname):
-        if User.query.filter_by(nickname = nickname).first() == None:
-            return nickname
-        version = 2
-        while True:
-            new_nickname = nickname + str(version)
-            if User.query.filter_by(nickname = new_nickname).first() == None:
-                break
-            version += 1
-        return new_nickname
-
-
 class Hospital(db.Model):
-    """Hospital's has a one-to-many relationship with DATA and a
+    """Hospital's has a one-to-many relationship with answer and a
     many-to-many relationship with User"""
 
     id = db.Column(db.Integer, primary_key=True)
     name = db.Column(db.String(80))
-    data = db.relationship('Data', backref='hospital', lazy = 'dynamic')
+    answer = db.relationship('answer', backref='hospital', lazy = 'dynamic')
 
     def __init__(self, name):
         self.name = name
@@ -77,92 +52,31 @@ class Hospital(db.Model):
     def __repr__(self):
         return '<Name %r>' % self.name
 
+class Answer(db.Model):
+    """Answers has a many to one relationship with Hospital, a one to
+    many relationship with Question and a many to one relationship with survey"""
+
+    id = db.Column(db.Integer, primary_key=True)
+    value = db.Column(db.Integer)
+    hospital_id = db.Column(db.Integer, db.ForeignKey('hospital.id'))
+    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))
+    survey_id = db.Column(db.Integer, db.ForeignKey('survey.id'))
 
-class Data(db.Model):
-    """Data has a many-to-one relationship with Hospital"""
 
+class Question(db.Model):
+    """Question has a one to many to one relationship with Answer"""
     id = db.Column(db.Integer, primary_key=True)
+    key = db.Column(db.String(500))
+    answers = db.relationship('answer', backref='question', lazy='dynamic')
 
-    standard_form = db.Column(db.Integer)
-    marketing_education = db.Column(db.Integer)
-    record_availability = db.Column(db.Integer)
-    family_centerdness = db.Column(db.Integer)
-    pc_networking = db.Column(db.Integer)
-    education_and_training = db.Column(db.Integer)
-    team_funding = db.Column(db.Integer)
-    coverage = db.Column(db.Integer)
-    pc_for_expired_pts = db.Column(db.Integer)
-    hospital_pc_screening  = db.Column(db.Integer)
-    pc_follow_up = db.Column(db.Integer)
-    post_discharge_services = db.Column(db.Integer)
-    bereavement_contacts = db.Column(db.Integer)
-    certification = db.Column(db.Integer)
-    team_wellness = db.Column(db.Integer)
-    care_coordination = db.Column(db.Integer)
 
+class Survey(db.Model):
+    """survey has a one to may relationship with  answer"""
+    id = db.Column(db.Integer, primary_key=True)
+    answers = db.relationship('answer', backref='survey', lazy='dynamic')
+    release  = db.Column(db.String(50))
     timestamp = db.Column(db.DateTime)
 
-    hospital_id = db.Column(db.Integer, db.ForeignKey('hospital.id'))
 
-    def __init__(self, standard_form=0,
-            marketing_education=0, record_availability=0, family_centerdness=0,
-        pc_networking=0, education_and_training=0, team_funding=0,
-        coverage=0, pc_for_expired_pts=0, hospital_pc_screening=0,
-        pc_follow_up=0, post_discharge_services=0, bereavement_contacts=0,
-        certification=0, team_wellness=0, care_coordination=0, timestamp=datetime.utcnow()):
-
-            self.standard_form = standard_form
-            self.marketing_education =  marketing_education
-            self.record_availability = record_availability
-            self.family_centerdness =  family_centerdness
-            self.pc_networking =  pc_networking
-            self.education_and_training =  education_and_training
-            self.team_funding =  team_funding
-            self.coverage =  coverage
-            self.pc_for_expired_pts =  pc_for_expired_pts
-            self.hospital_pc_screening  =  hospital_pc_screening
-            self.pc_follow_up =  pc_follow_up
-            self.post_discharge_services =  post_discharge_services
-            self.bereavement_contacts =  bereavement_contacts
-            self.certification =  certification
-            self.team_wellness =  team_wellness
-            self.care_coordination = care_coordination
-            self.timestamp = timestamp
 
-    def __repr__(self):
-        return """
-    <standard_form : %r>\n
-    <marketing_education : %r>\n
-    <record_availability : %r>\n
-    <family_centerdness : %r>\n
-    <pc_networking : %r>\n
-    <education_and_training : %r>\n
-    <team_funding : %r>\n
-    <coverage : %r>\n
-    <pc_for_expired_pts : %r>\n
-    <hospital_pc_screening  : %r>\n
-    <pc_follow_up : %r>\n
-    <post_discharge_services : %r>\n
-    <bereavement_contacts : %r>\n
-    <certification : %r>\n
-    <team_wellness : %r>\n
-    <care_coordination : %r>\n
-    <datetime_utc  : %r>""" % (
-    self.standard_form,
-    self.marketing_education,
-    self.record_availability,
-    self.family_centerdness,
-    self.pc_networking,
-    self.education_and_training,
-    self.team_funding,
-    self.coverage,
-    self.pc_for_expired_pts,
-    self.hospital_pc_screening ,
-    self.pc_follow_up,
-    self.post_discharge_services,
-    self.bereavement_contacts,
-    self.certification,
-    self.team_wellness,
-    self.care_coordination,
-    self.timestamp)
 

commit 3d6aef337301a91157a27ac8e1b031a60cdafba5
Author: Drew Verlee <Drew.verlee@gmail.com>
Date:   Sun Jan 6 02:04:15 2013 -0500

    removed password

diff --git a/petalapp/database/models.py b/petalapp/database/models.py
index 1c9acc6..cfce664 100644
--- a/petalapp/database/models.py
+++ b/petalapp/database/models.py
@@ -16,7 +16,6 @@ class User(db.Model):
     nickname = db.Column(db.String(64), unique = True)
     email = db.Column(db.String(150), unique=True)
     role = db.Column(db.SmallInteger, default=ROLE_USER)
-    password = db.Column(db.String(250), unique=True)
 
     hospitals = db.relationship('Hospital', secondary=hospitals,
         backref=db.backref('users', lazy='dynamic'))

commit 3da77422b424d94aa1b467ebc2a5185e9cc316e7
Author: Drew Verlee <Drew.verlee@gmail.com>
Date:   Thu Jan 3 22:24:58 2013 -0500

    removed my email from login

diff --git a/petalapp/database/models.py b/petalapp/database/models.py
index 3039361..1c9acc6 100644
--- a/petalapp/database/models.py
+++ b/petalapp/database/models.py
@@ -16,11 +16,12 @@ class User(db.Model):
     nickname = db.Column(db.String(64), unique = True)
     email = db.Column(db.String(150), unique=True)
     role = db.Column(db.SmallInteger, default=ROLE_USER)
+    password = db.Column(db.String(250), unique=True)
 
     hospitals = db.relationship('Hospital', secondary=hospitals,
         backref=db.backref('users', lazy='dynamic'))
 
-    def __init__(self, nickname, email, role=ROLE_USER):
+    def __init__(self, nickname, email, password="OpenID",role=ROLE_USER):
         self.nickname= nickname
         self.role = role
         self.email = email

commit cf52c6e200ddb6c3e2634e1bf629d2b651304209
Author: Drew Verlee <Drew.verlee@gmail.com>
Date:   Tue Jan 1 19:45:32 2013 -0500

    added new relic, hopefully didnt alter app

diff --git a/petalapp/database/models.py b/petalapp/database/models.py
index 4ae370a..3039361 100644
--- a/petalapp/database/models.py
+++ b/petalapp/database/models.py
@@ -50,7 +50,6 @@ class User(db.Model):
             self.hospitals.remove(hospital)
 
 
-
     @staticmethod
     def make_unique_nickname(nickname):
         if User.query.filter_by(nickname = nickname).first() == None:

commit f02ce9530ece73771b3c135c7857db0893a5e677
Author: Drew Verlee <Drew.verlee@gmail.com>
Date:   Fri Dec 28 16:22:59 2012 -0500

    added methods to models.User

diff --git a/petalapp/database/models.py b/petalapp/database/models.py
index 24000bf..4ae370a 100644
--- a/petalapp/database/models.py
+++ b/petalapp/database/models.py
@@ -3,7 +3,7 @@ from datetime import datetime
 ROLE_USER = 0
 ROLE_ADMIN = 1
 
-#TODO:rename
+#TODO:rename?
 hospitals = db.Table('hospitals',
     db.Column('hospital_id', db.Integer, db.ForeignKey('hospital.id')),
     db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
@@ -41,6 +41,16 @@ class User(db.Model):
     def get_id(self):
         return unicode(self.id)
 
+    def add_hospital(self, hospital):
+        if not (hospital in self.hospitals):
+            self.hospitals.append(hospital)
+
+    def remove_hospital(self, hospital):
+        if not (hospital in self.hospital):
+            self.hospitals.remove(hospital)
+
+
+
     @staticmethod
     def make_unique_nickname(nickname):
         if User.query.filter_by(nickname = nickname).first() == None:

commit 88cb13e79f9401cb1f533ca0f325011f5a79a0cb
Author: Drew Verlee <Drew.verlee@gmail.com>
Date:   Thu Dec 27 17:23:30 2012 -0500

    handled duplicate nicnames, skipped profile avatar setup

diff --git a/petalapp/database/models.py b/petalapp/database/models.py
index 4288c4e..24000bf 100644
--- a/petalapp/database/models.py
+++ b/petalapp/database/models.py
@@ -41,7 +41,7 @@ class User(db.Model):
     def get_id(self):
         return unicode(self.id)
 
-    @stacticmethod
+    @staticmethod
     def make_unique_nickname(nickname):
         if User.query.filter_by(nickname = nickname).first() == None:
             return nickname

commit 96a680221d22d0b6e2c0b231645c846dda547c6d
Author: Drew Verlee <Drew.verlee@gmail.com>
Date:   Thu Dec 27 17:07:59 2012 -0500

    handling errors

diff --git a/petalapp/database/models.py b/petalapp/database/models.py
index dfaefd7..4288c4e 100644
--- a/petalapp/database/models.py
+++ b/petalapp/database/models.py
@@ -41,6 +41,19 @@ class User(db.Model):
     def get_id(self):
         return unicode(self.id)
 
+    @stacticmethod
+    def make_unique_nickname(nickname):
+        if User.query.filter_by(nickname = nickname).first() == None:
+            return nickname
+        version = 2
+        while True:
+            new_nickname = nickname + str(version)
+            if User.query.filter_by(nickname = new_nickname).first() == None:
+                break
+            version += 1
+        return new_nickname
+
+
 class Hospital(db.Model):
     """Hospital's has a one-to-many relationship with DATA and a
     many-to-many relationship with User"""

commit ad8bb379f7f5ce1d93d68a3db71031c57355db11
Author: Drew Verlee <Drew.verlee@gmail.com>
Date:   Thu Dec 27 14:10:42 2012 -0500

    trying to test app

diff --git a/petalapp/database/models.py b/petalapp/database/models.py
index 4251d36..dfaefd7 100644
--- a/petalapp/database/models.py
+++ b/petalapp/database/models.py
@@ -126,7 +126,6 @@ class Data(db.Model):
     <team_wellness : %r>\n
     <care_coordination : %r>\n
     <datetime_utc  : %r>""" % (
-
     self.standard_form,
     self.marketing_education,
     self.record_availability,

commit 4e9975fffa820af2a5c5b26b671fad9fe19b08d4
Author: Drew Verlee <Drew.verlee@gmail.com>
Date:   Thu Dec 27 13:09:16 2012 -0500

    application not running

diff --git a/petalapp/database/models.py b/petalapp/database/models.py
index 1e27268..4251d36 100644
--- a/petalapp/database/models.py
+++ b/petalapp/database/models.py
@@ -82,7 +82,7 @@ class Data(db.Model):
 
     hospital_id = db.Column(db.Integer, db.ForeignKey('hospital.id'))
 
-    def __init__(self, standard_form=0, 
+    def __init__(self, standard_form=0,
             marketing_education=0, record_availability=0, family_centerdness=0,
         pc_networking=0, education_and_training=0, team_funding=0,
         coverage=0, pc_for_expired_pts=0, hospital_pc_screening=0,

commit 6bf6883ab2285832974a9986a10cf517b674e861
Author: Drew Verlee <Drew.verlee@gmail.com>
Date:   Thu Dec 27 12:46:03 2012 -0500

    models updated with datetime

diff --git a/petalapp/database/models.py b/petalapp/database/models.py
index b3c04cf..1e27268 100644
--- a/petalapp/database/models.py
+++ b/petalapp/database/models.py
@@ -1,5 +1,5 @@
 from petalapp import db
-
+from datetime import datetime
 ROLE_USER = 0
 ROLE_ADMIN = 1
 
@@ -60,6 +60,7 @@ class Data(db.Model):
     """Data has a many-to-one relationship with Hospital"""
 
     id = db.Column(db.Integer, primary_key=True)
+
     standard_form = db.Column(db.Integer)
     marketing_education = db.Column(db.Integer)
     record_availability = db.Column(db.Integer)
@@ -77,14 +78,16 @@ class Data(db.Model):
     team_wellness = db.Column(db.Integer)
     care_coordination = db.Column(db.Integer)
 
+    timestamp = db.Column(db.DateTime)
+
     hospital_id = db.Column(db.Integer, db.ForeignKey('hospital.id'))
 
-    def __init__(self, standard_form=0, marketing_education=0,
-        record_availability=0, family_centerdness=0,
+    def __init__(self, standard_form=0, 
+            marketing_education=0, record_availability=0, family_centerdness=0,
         pc_networking=0, education_and_training=0, team_funding=0,
         coverage=0, pc_for_expired_pts=0, hospital_pc_screening=0,
         pc_follow_up=0, post_discharge_services=0, bereavement_contacts=0,
-        certification=0, team_wellness=0, care_coordination=0):
+        certification=0, team_wellness=0, care_coordination=0, timestamp=datetime.utcnow()):
 
             self.standard_form = standard_form
             self.marketing_education =  marketing_education
@@ -102,25 +105,28 @@ class Data(db.Model):
             self.certification =  certification
             self.team_wellness =  team_wellness
             self.care_coordination = care_coordination
+            self.timestamp = timestamp
 
     def __repr__(self):
         return """
-    {standard_form : %r}
-    {marketing_education : %r}
-    {record_availability : %r}
-    {family_centerdness : %r}
-    {pc_networking : %r}
-    {education_and_training : %r}
-    {team_funding : %r}
-    {coverage : %r}
-    {pc_for_expired_pts : %r}
-    {hospital_pc_screening  : %r}
-    {pc_follow_up : %r}
-    {post_discharge_services : %r}
-    {bereavement_contacts : %r}
-    {certification : %r}
-    {team_wellness : %r}
-    {care_coordination : %r}""" % (
+    <standard_form : %r>\n
+    <marketing_education : %r>\n
+    <record_availability : %r>\n
+    <family_centerdness : %r>\n
+    <pc_networking : %r>\n
+    <education_and_training : %r>\n
+    <team_funding : %r>\n
+    <coverage : %r>\n
+    <pc_for_expired_pts : %r>\n
+    <hospital_pc_screening  : %r>\n
+    <pc_follow_up : %r>\n
+    <post_discharge_services : %r>\n
+    <bereavement_contacts : %r>\n
+    <certification : %r>\n
+    <team_wellness : %r>\n
+    <care_coordination : %r>\n
+    <datetime_utc  : %r>""" % (
+
     self.standard_form,
     self.marketing_education,
     self.record_availability,
@@ -136,5 +142,6 @@ class Data(db.Model):
     self.bereavement_contacts,
     self.certification,
     self.team_wellness,
-    self.care_coordination)
+    self.care_coordination,
+    self.timestamp)
 

commit 87c52c3be63b6d819a01090ade5cc731d335d39a
Author: Drew Verlee <Drew.verlee@gmail.com>
Date:   Wed Dec 26 23:49:33 2012 -0500

    nickname change in modles

diff --git a/petalapp/database/models.py b/petalapp/database/models.py
index b79a528..b3c04cf 100644
--- a/petalapp/database/models.py
+++ b/petalapp/database/models.py
@@ -27,7 +27,7 @@ class User(db.Model):
 
     #TODO what information to show?
     def __repr__(self):
-        return '<Name : %r, %r >' % (self.last_name ,self.first_name)
+        return '<Name : %r>' % (self.nickname)
 
     def is_authenticated(self):
         return True

commit 6e4f9a8ea719e9e64ed900937199d325373f23ca
Author: Drew Verlee <Drew.verlee@gmail.com>
Date:   Wed Dec 26 23:00:33 2012 -0500

    changed from first name to nickname in models

diff --git a/petalapp/database/models.py b/petalapp/database/models.py
index 1343dac..b79a528 100644
--- a/petalapp/database/models.py
+++ b/petalapp/database/models.py
@@ -13,17 +13,15 @@ class User(db.Model):
     """User has a many-to-many relationship with Hospital"""
 
     id = db.Column(db.Integer, primary_key=True)
-    last_name = db.Column(db.String(80))
-    first_name = db.Column(db.String(80))
+    nickname = db.Column(db.String(64), unique = True)
     email = db.Column(db.String(150), unique=True)
     role = db.Column(db.SmallInteger, default=ROLE_USER)
 
     hospitals = db.relationship('Hospital', secondary=hospitals,
         backref=db.backref('users', lazy='dynamic'))
 
-    def __init__(self, last_name, first_name, email, role=ROLE_USER):
-        self.last_name = last_name
-        self.first_name = first_name
+    def __init__(self, nickname, email, role=ROLE_USER):
+        self.nickname= nickname
         self.role = role
         self.email = email
 

commit 9de995979ab20d238087c74e324bc4f0f4c3ecc7
Author: Drew Verlee <Drew.verlee@gmail.com>
Date:   Wed Dec 26 14:45:20 2012 -0500

    app not running with gunicorn

diff --git a/petalapp/database/models.py b/petalapp/database/models.py
index ad814cc..1343dac 100644
--- a/petalapp/database/models.py
+++ b/petalapp/database/models.py
@@ -31,6 +31,18 @@ class User(db.Model):
     def __repr__(self):
         return '<Name : %r, %r >' % (self.last_name ,self.first_name)
 
+    def is_authenticated(self):
+        return True
+
+    def is_active(self):
+        return True
+
+    def is_anonymous(self):
+        return False
+
+    def get_id(self):
+        return unicode(self.id)
+
 class Hospital(db.Model):
     """Hospital's has a one-to-many relationship with DATA and a
     many-to-many relationship with User"""

commit e808fc32214cc2c62464f78c194599da77016aa3
Author: Drew Verlee <Drew.verlee@gmail.com>
Date:   Wed Dec 26 13:11:08 2012 -0500

    edited models

diff --git a/petalapp/database/models.py b/petalapp/database/models.py
index 35dd7c4..ad814cc 100644
--- a/petalapp/database/models.py
+++ b/petalapp/database/models.py
@@ -21,10 +21,7 @@ class User(db.Model):
     hospitals = db.relationship('Hospital', secondary=hospitals,
         backref=db.backref('users', lazy='dynamic'))
 
-
-
-    def __init__(self, last_name="NONE", first_name="NONE", role=ROLE_USER,
-            email="NONE"):
+    def __init__(self, last_name, first_name, email, role=ROLE_USER):
         self.last_name = last_name
         self.first_name = first_name
         self.role = role

commit f62b9f853b852fcc4ab5c635281d7630c46660e9
Author: Drew Verlee <Drew.verlee@gmail.com>
Date:   Wed Dec 26 12:28:10 2012 -0500

    create build_docs folder to house all documents

diff --git a/petalapp/database/models.py b/petalapp/database/models.py
index 2a8c1f7..35dd7c4 100644
--- a/petalapp/database/models.py
+++ b/petalapp/database/models.py
@@ -1,10 +1,9 @@
 from petalapp import db
-from werkzeug.security import generate_password_hash, check_password_hash
 
 ROLE_USER = 0
 ROLE_ADMIN = 1
 
-#TODO: possible rename
+#TODO:rename
 hospitals = db.Table('hospitals',
     db.Column('hospital_id', db.Integer, db.ForeignKey('hospital.id')),
     db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
@@ -19,27 +18,19 @@ class User(db.Model):
     email = db.Column(db.String(150), unique=True)
     role = db.Column(db.SmallInteger, default=ROLE_USER)
 
-    #passwords
-
     hospitals = db.relationship('Hospital', secondary=hospitals,
         backref=db.backref('users', lazy='dynamic'))
 
-    def __init__(self, password, last_name="NONE", first_name="NONE", role=ROLE_USER,
-            email="NONE"):
 
+
+    def __init__(self, last_name="NONE", first_name="NONE", role=ROLE_USER,
+            email="NONE"):
         self.last_name = last_name
         self.first_name = first_name
         self.role = role
         self.email = email
-        self.set_password(password)
-
-    def set_password(self, password):
-        self.pw_hash = generate_password_hash(self.pw_hash, password)
-
-    def check_password(self, password):
-        return check_password_hash(self.pw_hash, password)
 
-    #TODO what information should i show?
+    #TODO what information to show?
     def __repr__(self):
         return '<Name : %r, %r >' % (self.last_name ,self.first_name)
 

commit a8707ccf52e299dfae618b68c4eb7fdffab86e96
Author: Drew Verlee <Drew.verlee@gmail.com>
Date:   Sat Dec 22 12:27:38 2012 -0500

    small commit before merge

diff --git a/petalapp/database/models.py b/petalapp/database/models.py
index 9757721..2a8c1f7 100644
--- a/petalapp/database/models.py
+++ b/petalapp/database/models.py
@@ -4,7 +4,7 @@ from werkzeug.security import generate_password_hash, check_password_hash
 ROLE_USER = 0
 ROLE_ADMIN = 1
 
-#TODO:rename
+#TODO: possible rename
 hospitals = db.Table('hospitals',
     db.Column('hospital_id', db.Integer, db.ForeignKey('hospital.id')),
     db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
@@ -21,14 +21,9 @@ class User(db.Model):
 
     #passwords
 
-
-
-
     hospitals = db.relationship('Hospital', secondary=hospitals,
         backref=db.backref('users', lazy='dynamic'))
 
-
-
     def __init__(self, password, last_name="NONE", first_name="NONE", role=ROLE_USER,
             email="NONE"):
 
@@ -44,7 +39,7 @@ class User(db.Model):
     def check_password(self, password):
         return check_password_hash(self.pw_hash, password)
 
-    #TODO what information to show?
+    #TODO what information should i show?
     def __repr__(self):
         return '<Name : %r, %r >' % (self.last_name ,self.first_name)
 

commit d535b0641ffee63fb05123db7355ad225dc7c573
Author: Drew Verlee <Drew.verlee@gmail.com>
Date:   Mon Dec 10 13:58:34 2012 -0500

    petalapp/database/models added salted security not sure if correct

diff --git a/petalapp/database/models.py b/petalapp/database/models.py
index 35dd7c4..9757721 100644
--- a/petalapp/database/models.py
+++ b/petalapp/database/models.py
@@ -1,4 +1,5 @@
 from petalapp import db
+from werkzeug.security import generate_password_hash, check_password_hash
 
 ROLE_USER = 0
 ROLE_ADMIN = 1
@@ -18,17 +19,30 @@ class User(db.Model):
     email = db.Column(db.String(150), unique=True)
     role = db.Column(db.SmallInteger, default=ROLE_USER)
 
+    #passwords
+
+
+
+
     hospitals = db.relationship('Hospital', secondary=hospitals,
         backref=db.backref('users', lazy='dynamic'))
 
 
 
-    def __init__(self, last_name="NONE", first_name="NONE", role=ROLE_USER,
+    def __init__(self, password, last_name="NONE", first_name="NONE", role=ROLE_USER,
             email="NONE"):
+
         self.last_name = last_name
         self.first_name = first_name
         self.role = role
         self.email = email
+        self.set_password(password)
+
+    def set_password(self, password):
+        self.pw_hash = generate_password_hash(self.pw_hash, password)
+
+    def check_password(self, password):
+        return check_password_hash(self.pw_hash, password)
 
     #TODO what information to show?
     def __repr__(self):

commit 1ca9af28d2d449e5ca463312bac6d1ff299d7192
Author: Drew Verlee <Drew.verlee@gmail.com>
Date:   Thu Dec 6 17:59:08 2012 -0500

    working with database

diff --git a/petalapp/database/models.py b/petalapp/database/models.py
index 4beac6c..35dd7c4 100644
--- a/petalapp/database/models.py
+++ b/petalapp/database/models.py
@@ -72,12 +72,12 @@ class Data(db.Model):
 
     hospital_id = db.Column(db.Integer, db.ForeignKey('hospital.id'))
 
-    def __init__(self, standard_form, marketing_education,
-        record_availability, family_centerdness,
-        pc_networking, education_and_training, team_funding,
-        coverage, pc_for_expired_pts, hospital_pc_screening,
-        pc_follow_up, post_discharge_services, bereavement_contacts,
-        certification, team_wellness, care_coordination):
+    def __init__(self, standard_form=0, marketing_education=0,
+        record_availability=0, family_centerdness=0,
+        pc_networking=0, education_and_training=0, team_funding=0,
+        coverage=0, pc_for_expired_pts=0, hospital_pc_screening=0,
+        pc_follow_up=0, post_discharge_services=0, bereavement_contacts=0,
+        certification=0, team_wellness=0, care_coordination=0):
 
             self.standard_form = standard_form
             self.marketing_education =  marketing_education

commit 89eb250669bcdce5705febf4f6b7ca938ed41d8f
Author: Drew Verlee <Drew.verlee@gmail.com>
Date:   Thu Dec 6 17:44:17 2012 -0500

    shell script push

diff --git a/petalapp/database/models.py b/petalapp/database/models.py
index 63f6deb..4beac6c 100644
--- a/petalapp/database/models.py
+++ b/petalapp/database/models.py
@@ -9,14 +9,13 @@ hospitals = db.Table('hospitals',
     db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
 )
 # tags bmarks time
-#FIXME unsure about init
-#FIXME tablename is already set unless overridden
 class User(db.Model):
     """User has a many-to-many relationship with Hospital"""
 
     id = db.Column(db.Integer, primary_key=True)
-    name = db.Column(db.String(80))
-    mail = db.Column(db.String(150), unique=True)
+    last_name = db.Column(db.String(80))
+    first_name = db.Column(db.String(80))
+    email = db.Column(db.String(150), unique=True)
     role = db.Column(db.SmallInteger, default=ROLE_USER)
 
     hospitals = db.relationship('Hospital', secondary=hospitals,
@@ -24,16 +23,19 @@ class User(db.Model):
 
 
 
-    def __init__(self, name="NONE", role=ROLE_USER, mail="NONE"):
-        self.name = name
+    def __init__(self, last_name="NONE", first_name="NONE", role=ROLE_USER,
+            email="NONE"):
+        self.last_name = last_name
+        self.first_name = first_name
         self.role = role
-        self.mail = mail
+        self.email = email
 
+    #TODO what information to show?
     def __repr__(self):
-        return '<Name %r>' % self.name
+        return '<Name : %r, %r >' % (self.last_name ,self.first_name)
 
 class Hospital(db.Model):
-    """Hospital's has a one-to-many relationship with DATA and a 
+    """Hospital's has a one-to-many relationship with DATA and a
     many-to-many relationship with User"""
 
     id = db.Column(db.Integer, primary_key=True)
@@ -51,13 +53,81 @@ class Data(db.Model):
     """Data has a many-to-one relationship with Hospital"""
 
     id = db.Column(db.Integer, primary_key=True)
-    pc = db.Column(db.Integer)
+    standard_form = db.Column(db.Integer)
+    marketing_education = db.Column(db.Integer)
+    record_availability = db.Column(db.Integer)
+    family_centerdness = db.Column(db.Integer)
+    pc_networking = db.Column(db.Integer)
+    education_and_training = db.Column(db.Integer)
+    team_funding = db.Column(db.Integer)
+    coverage = db.Column(db.Integer)
+    pc_for_expired_pts = db.Column(db.Integer)
+    hospital_pc_screening  = db.Column(db.Integer)
+    pc_follow_up = db.Column(db.Integer)
+    post_discharge_services = db.Column(db.Integer)
+    bereavement_contacts = db.Column(db.Integer)
+    certification = db.Column(db.Integer)
+    team_wellness = db.Column(db.Integer)
+    care_coordination = db.Column(db.Integer)
+
     hospital_id = db.Column(db.Integer, db.ForeignKey('hospital.id'))
 
-    def __init__(self, pc):
-        self.pc = pc
+    def __init__(self, standard_form, marketing_education,
+        record_availability, family_centerdness,
+        pc_networking, education_and_training, team_funding,
+        coverage, pc_for_expired_pts, hospital_pc_screening,
+        pc_follow_up, post_discharge_services, bereavement_contacts,
+        certification, team_wellness, care_coordination):
+
+            self.standard_form = standard_form
+            self.marketing_education =  marketing_education
+            self.record_availability = record_availability
+            self.family_centerdness =  family_centerdness
+            self.pc_networking =  pc_networking
+            self.education_and_training =  education_and_training
+            self.team_funding =  team_funding
+            self.coverage =  coverage
+            self.pc_for_expired_pts =  pc_for_expired_pts
+            self.hospital_pc_screening  =  hospital_pc_screening
+            self.pc_follow_up =  pc_follow_up
+            self.post_discharge_services =  post_discharge_services
+            self.bereavement_contacts =  bereavement_contacts
+            self.certification =  certification
+            self.team_wellness =  team_wellness
+            self.care_coordination = care_coordination
 
     def __repr__(self):
-        return '<pc %r>' % self.pc
-
+        return """
+    {standard_form : %r}
+    {marketing_education : %r}
+    {record_availability : %r}
+    {family_centerdness : %r}
+    {pc_networking : %r}
+    {education_and_training : %r}
+    {team_funding : %r}
+    {coverage : %r}
+    {pc_for_expired_pts : %r}
+    {hospital_pc_screening  : %r}
+    {pc_follow_up : %r}
+    {post_discharge_services : %r}
+    {bereavement_contacts : %r}
+    {certification : %r}
+    {team_wellness : %r}
+    {care_coordination : %r}""" % (
+    self.standard_form,
+    self.marketing_education,
+    self.record_availability,
+    self.family_centerdness,
+    self.pc_networking,
+    self.education_and_training,
+    self.team_funding,
+    self.coverage,
+    self.pc_for_expired_pts,
+    self.hospital_pc_screening ,
+    self.pc_follow_up,
+    self.post_discharge_services,
+    self.bereavement_contacts,
+    self.certification,
+    self.team_wellness,
+    self.care_coordination)
 

commit 16ff19656dbc64c63af414b3944158f0109eeadc
Author: Drew Verlee <Drew.verlee@gmail.com>
Date:   Thu Dec 6 13:02:10 2012 -0500

    small db change

diff --git a/petalapp/database/models.py b/petalapp/database/models.py
index 12308be..63f6deb 100644
--- a/petalapp/database/models.py
+++ b/petalapp/database/models.py
@@ -24,11 +24,10 @@ class User(db.Model):
 
 
 
-    def __init__(self, name="NONE", role=ROLE_USER, mail="NONE", hospitals="NONE"):
+    def __init__(self, name="NONE", role=ROLE_USER, mail="NONE"):
         self.name = name
         self.role = role
         self.mail = mail
-        self.hospitals = hospitals
 
     def __repr__(self):
         return '<Name %r>' % self.name

commit c89d19739da6a3506bd426acc84553ac52459a7e
Author: Drew Verlee <Drew.verlee@gmail.com>
Date:   Thu Dec 6 12:55:59 2012 -0500

    create petalapp/database/db_test_many.py to build a test model of the db

diff --git a/petalapp/database/models.py b/petalapp/database/models.py
index 9f8385c..12308be 100644
--- a/petalapp/database/models.py
+++ b/petalapp/database/models.py
@@ -8,17 +8,23 @@ hospitals = db.Table('hospitals',
     db.Column('hospital_id', db.Integer, db.ForeignKey('hospital.id')),
     db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
 )
-
+# tags bmarks time
 #FIXME unsure about init
+#FIXME tablename is already set unless overridden
 class User(db.Model):
+    """User has a many-to-many relationship with Hospital"""
+
     id = db.Column(db.Integer, primary_key=True)
     name = db.Column(db.String(80))
     mail = db.Column(db.String(150), unique=True)
     role = db.Column(db.SmallInteger, default=ROLE_USER)
+
     hospitals = db.relationship('Hospital', secondary=hospitals,
         backref=db.backref('users', lazy='dynamic'))
 
-    def __init__(self, name, role, mail="NONE", hospitals="NONE"):
+
+
+    def __init__(self, name="NONE", role=ROLE_USER, mail="NONE", hospitals="NONE"):
         self.name = name
         self.role = role
         self.mail = mail
@@ -28,26 +34,29 @@ class User(db.Model):
         return '<Name %r>' % self.name
 
 class Hospital(db.Model):
+    """Hospital's has a one-to-many relationship with DATA and a 
+    many-to-many relationship with User"""
+
     id = db.Column(db.Integer, primary_key=True)
     name = db.Column(db.String(80))
-    data = db.relationship('Data', backref='hospital', lazy='dynamic')
+    data = db.relationship('Data', backref='hospital', lazy = 'dynamic')
 
-    def __init__(self, name, data):
+    def __init__(self, name):
         self.name = name
-        self.date = data
 
     def __repr__(self):
         return '<Name %r>' % self.name
 
 
 class Data(db.Model):
+    """Data has a many-to-one relationship with Hospital"""
+
     id = db.Column(db.Integer, primary_key=True)
     pc = db.Column(db.Integer)
     hospital_id = db.Column(db.Integer, db.ForeignKey('hospital.id'))
 
-    def __init__(self, pc, hospital_id):
+    def __init__(self, pc):
         self.pc = pc
-        self.hospital_id = hospital_id
 
     def __repr__(self):
         return '<pc %r>' % self.pc

commit 9726d7489ef518c83dde6879e43574501e424bb2
Author: Drew Verlee <Drew.verlee@gmail.com>
Date:   Wed Nov 28 21:08:19 2012 -0500

    changes to db_migrate

diff --git a/petalapp/database/models.py b/petalapp/database/models.py
index e20ffe8..9f8385c 100644
--- a/petalapp/database/models.py
+++ b/petalapp/database/models.py
@@ -9,6 +9,7 @@ hospitals = db.Table('hospitals',
     db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
 )
 
+#FIXME unsure about init
 class User(db.Model):
     id = db.Column(db.Integer, primary_key=True)
     name = db.Column(db.String(80))
@@ -17,8 +18,11 @@ class User(db.Model):
     hospitals = db.relationship('Hospital', secondary=hospitals,
         backref=db.backref('users', lazy='dynamic'))
 
-    def __init__(self, name):
+    def __init__(self, name, role, mail="NONE", hospitals="NONE"):
         self.name = name
+        self.role = role
+        self.mail = mail
+        self.hospitals = hospitals
 
     def __repr__(self):
         return '<Name %r>' % self.name
@@ -28,8 +32,9 @@ class Hospital(db.Model):
     name = db.Column(db.String(80))
     data = db.relationship('Data', backref='hospital', lazy='dynamic')
 
-    def __init__(self, name):
+    def __init__(self, name, data):
         self.name = name
+        self.date = data
 
     def __repr__(self):
         return '<Name %r>' % self.name
@@ -40,8 +45,9 @@ class Data(db.Model):
     pc = db.Column(db.Integer)
     hospital_id = db.Column(db.Integer, db.ForeignKey('hospital.id'))
 
-    def __init__(self, pc):
+    def __init__(self, pc, hospital_id):
         self.pc = pc
+        self.hospital_id = hospital_id
 
     def __repr__(self):
         return '<pc %r>' % self.pc

commit 092a8f7ce06ee0414fa0a29654209b809b58dc21
Author: Drew Verlee <Drew.verlee@gmail.com>
Date:   Wed Nov 28 20:17:27 2012 -0500

    small db change'

diff --git a/petalapp/database/models.py b/petalapp/database/models.py
index eb651bb..e20ffe8 100644
--- a/petalapp/database/models.py
+++ b/petalapp/database/models.py
@@ -12,8 +12,8 @@ hospitals = db.Table('hospitals',
 class User(db.Model):
     id = db.Column(db.Integer, primary_key=True)
     name = db.Column(db.String(80))
-    #mail = db.Column(db.String(150), unique=True)
-    #role = db.Column(db.SmallInteger, default=ROLE_USER)
+    mail = db.Column(db.String(150), unique=True)
+    role = db.Column(db.SmallInteger, default=ROLE_USER)
     hospitals = db.relationship('Hospital', secondary=hospitals,
         backref=db.backref('users', lazy='dynamic'))
 

commit 11f755da857310f6beebe6c82a3bc994c86b6368
Author: Drew Verlee <Drew.verlee@gmail.com>
Date:   Fri Nov 23 09:52:50 2012 -0500

    some refactoring moving deleting ect.. no changes to app function

diff --git a/petalapp/database/models.py b/petalapp/database/models.py
new file mode 100644
index 0000000..eb651bb
--- /dev/null
+++ b/petalapp/database/models.py
@@ -0,0 +1,49 @@
+from petalapp import db
+
+ROLE_USER = 0
+ROLE_ADMIN = 1
+
+#TODO:rename
+hospitals = db.Table('hospitals',
+    db.Column('hospital_id', db.Integer, db.ForeignKey('hospital.id')),
+    db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
+)
+
+class User(db.Model):
+    id = db.Column(db.Integer, primary_key=True)
+    name = db.Column(db.String(80))
+    #mail = db.Column(db.String(150), unique=True)
+    #role = db.Column(db.SmallInteger, default=ROLE_USER)
+    hospitals = db.relationship('Hospital', secondary=hospitals,
+        backref=db.backref('users', lazy='dynamic'))
+
+    def __init__(self, name):
+        self.name = name
+
+    def __repr__(self):
+        return '<Name %r>' % self.name
+
+class Hospital(db.Model):
+    id = db.Column(db.Integer, primary_key=True)
+    name = db.Column(db.String(80))
+    data = db.relationship('Data', backref='hospital', lazy='dynamic')
+
+    def __init__(self, name):
+        self.name = name
+
+    def __repr__(self):
+        return '<Name %r>' % self.name
+
+
+class Data(db.Model):
+    id = db.Column(db.Integer, primary_key=True)
+    pc = db.Column(db.Integer)
+    hospital_id = db.Column(db.Integer, db.ForeignKey('hospital.id'))
+
+    def __init__(self, pc):
+        self.pc = pc
+
+    def __repr__(self):
+        return '<pc %r>' % self.pc
+
+
