'''
File: db_query.py
Date: 2013-03-20
Author: Drew Verlee
Description: temp location for function
'''
from petalapp.database.models import UserSurveySection,SurveySection, User,\
    Organization, SurveyHeader
from petalapp import db
from sqlalchemy import func, extract, distinct

def most_recent_completed_uss(user):
    r = {}
    os = [o.id for o in user.organizations]
    for uss in UserSurveySection.query.all():
        if uss.organization_id in os:
            oss = (uss.organization_id, uss.survey_section_id)
            if oss not in r:
                r[oss] = uss
            else:
                if not r[oss].completed_date:
                    if uss.completed_date:
                        r[oss] = uss
                else:
                    if uss.completed_date and r[oss].completed_date < uss.completed_date:
                        r[oss] = uss

    result = []
    for k in r:
        result.append(r[k].id)
    result.sort() #FIXME i don't believe this will work
    return result[0:10]








    # userSurveySection with most recent completed date
    # per section per organization




if __name__ == "__main__":
    from pprint import pprint as pp
    drew = User.query.filter_by(name='drew.verlee@gmail.com').one()
    pp(most_recent_completed_uss(drew))





