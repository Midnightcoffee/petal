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
            oss = (uss.organization_id,
                    uss.period_id,
                    uss.survey_section.survey_header_id,
                    uss.survey_section_id)
            if oss not in r:
                r[oss] = uss
            else:
                if not r[oss].completed_date:
                    if uss.completed_date:
                        r[oss] = uss
                else:
                    if uss.completed_date and r[oss].completed_date < uss.completed_date:
                        r[oss] = uss

    return r
    result = []
    for k in r:
        result.append(r[k].id)
    result.sort() #FIXME i don't believe this will work
    return result

def uss_by_osh(usses):
    r = {}
    for k in usses:
        if k[0:3] not in r:
            r[k[0:3]] = [usses[k]]
        else:
            r[k[0:3]].append(usses[k])
    return r


def sort_uss(usses):
    for k in usses:
        usses[k].sort(key=lambda x: x.survey_section.order)
    return usses

def show_order(usses):
    for k in usses:
        print([x.survey_section.order for x in usses[k]])


def show_id(usses):
    for k in usses:
        print([x.id for x in usses[k]])

def return_ids(usses):
    r = []
    for x in usses:
        for i in usses[x]:
            r.append(i.id)
    return r

def chain(usses):
    return return_ids(sort_uss(uss_by_osh(most_recent_completed_uss(usses))))
    # userSurveySection with most recent completed date
    # per section per organization




if __name__ == "__main__":
    drew = User.query.filter_by(name='drew.verlee@gmail.com').one()
    usses = most_recent_completed_uss(drew)
    usses = uss_by_osh(usses)
    usses = sort_uss(usses)
    # show_order(usses)
    # show_id(usses)
    print(return_ids(usses))





