from petalapp.database.models import *

def get_drew():
    drew = User.query.filter_by(email='drew.verlee@gmail.com').first()
    drews_sections = drew.user_survey_sections.all()
    print("drews sections: {0}".format(drews_sections))
    print(drews_sections)

#query where the organization's, survey_header's user_survey_section.id is the 
# same as the user's survey section id

for org in Organization.query.all():
    print(org)
    
