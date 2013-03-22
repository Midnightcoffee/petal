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

def most_recent_completed_uss():
    # user_survey_section_ids = [x.user_survey_sections.order_by(UserSurveySection.completed_date.desc().\
    # nullslast()).first().id if x.user_survey_sections.order_by(UserSurveySection.completed_date.desc().\
    # nullslast()).first() else None for x in user.organizations]
    # drew = User.query.filter_by(name='drew.verlee@gmail.com').first()

    # return db.session.query(UserSurveySection).\
    #     filter(User.name == 'drew.verlee@gmail.com').\
    #     order_by(UserSurveySection.completed_date.desc()).group_by(Organization.id).all()

    # return db.session.query(UserSurveySection.id).join(UserSurveySection.organization).\
    # group_by(UserSurveySection.id).having(func.count(Organization.id) == 1).all()
    # return db.session.query(UserSurveySection).order_by(UserSurveySection.id.desc()).all()

    # return UserSurveySection.query.filter(extract('year',
    #     UserSurveySection.completed_date) == 2013).all()

    # return db.session.query(func.max(UserSurveySection.completed_date)).all()
    # return db.session.query(UserSurveySection).\
    #         order_by(UserSurveySection.organization).group_by(UserSurveySection.organization).all()

    # for o, m in db.session.query(UserSurveySection,func.\
    #         max(UserSurveySection.)).group_by(UserSurveySection.).all():
    #     print("uss cd {0} : {1}".format(o, m))

    # return db.session.query(func.max(UserSurveySection.completed_date)).scalar()

    # for v in db.session.query(UserSurveySection.survey_section).distinct():
    #     print(v)

    # print(db.session.query(func.count(distinct(UserSurveySection.completed_date))).one())

    # for org, mc in db.session.query(SurveySection.name,
    #         func.max(UserSurveySection.completed_date)).group_by(SurveySection.name).all():
    #     print(" Orgs cm {0} : {1}".format(org, mc))

    # for u, a in db.session.query(SurveySection, UserSurveySection).\
    #     filter(SurveySection.id==UserSurveySection.survey_section_id).\
    #     filter(func.max(UserSurveySection.completed_date)).one():
    #     print(u,a)

    # for name, in db.session.query(User.name).\
    #         filter(User.organizations.any()):
    #             print(name)

    # for value, m in db.session.query(Organization.id, User.id).distinct().\
    #         filter(Organization.id == 1).all():
    #             print(value, m)
    count = 0
    for uss in db.session.query(UserSurveySection.completed_date).filter(
        (Organization.id == 1) | (Organization.id ==2)).filter(SurveyHeader.id == 1).\
        filter(SurveySection.id ==1).filter(UserSurveySection.completed_date != None).distinct():
        count+=1
        print(uss)
    print(count)



    # userSurveySection with most recent completed date
    # per section per organization




if __name__ == "__main__":
    from pprint import pprint as pp
    pp(most_recent_completed_uss())





