'''
File: db_reset.py
Date: 2013-02-23
Author: Drew Verlee
Description: used to bulk load our database
'''
from sqlalchemy import create_engine
from petalapp.database.models import User, Organization, SurveyHeader,\
    SurveyComment, SurveySection, UserSurveySection, Answer, \
    UnitOfMeasurement, QuestionOption, OptionChoice, Question,OptionGroup, \
    InputType, ROLE_VIEWER, ROLE_CONTRIBUTER, ROLE_ADMIN, Market
from petalapp import db
from petalapp.database.models import User, Organization, SurveyHeader,\
    SurveyComment, SurveySection, UserSurveySection, Answer, \
    UnitOfMeasurement, QuestionOption, OptionChoice, Question,OptionGroup, \
    InputType, ROLE_VIEWER, ROLE_CONTRIBUTER, ROLE_ADMIN, Market
from pci_notes.storage.survey_headers.pci import survey_headers
from pci_notes.storage.users import users
from pci_notes.storage.market_organization import market_organization
from petalapp.config import SQLALCHEMY_DATABASE_URI
from pci_notes.storage.name_storage import input_types, option_group_choice,\
   units_of_measurements


def deb_reset():
    db.drop_all()
    db.create_all()

    uoms = []
    for u_om in units_of_measurements:
        uom = UnitOfMeasurement(name=u_om.name)
        db.ession.add(uom)
        uoms.append(uom)

    its = []
    for i_t in input_types:
        it = InputType(name=i_t)
        its.append(it)
        db.session.add(it)

    ogs = []
    for o_g in option_group_choice:
        og = OptionGroup(name=o_g)
        db.session.add(og)
        for o_c in option_group_choice[o_g]:
            oc = OptionChoice(name = o_c)
            og.option_choices.append(oc)
        db.session.add(og)
        ogs.append(og)

    shs = []
    for s_h in survey_headers:
        sh = SurveyHeader(name=s_h.name)
        for s_s in s_h.survey_sections:
            ss = SurveySection(name=s_s.name,subheading=s_s.subheading,
                order=s_s.order,children=s_s.children)
            for q_u in s_s.questions:
                q = Question(name=q_u.name, value=q_u.value, order=q_u.order,
                    answer_required_yn=q_u.answer_required_yn, subtext=q_u.subtext,
                    allow_mult_options_answers_yn=q_u.allow_mult_options_answers_yn)
                for it in its:
                    if it.name ==  q_u.input_type:
                        it.append(q)
                for og in ogs:
                    if og.name == q_u.option_group_name:
                        og.questions.append(q)
            ss.questions.append(q)
        sh.survey_sections.append(ss)
        shs.append(sh)

    #TODO FIX ME currently were ignoring the idea that organizations might
    # not have every survey_header
    orgs = []
    for m in market_organization:
        market = Market(name=m)
        for o in market_organization[m]:
            org = Organization(name=o)
            for sh in shs:
                org.survey_headers.append(sh)
            orgs.append(org)
            market.organizations.append(org)
        db.session.add(market)


    for u in users:
        user = User(name=u.name, role=u.role)
        for org in orgs:
            user.organizations.append(org)
        db.session.add(user)

    db.session.commit()


# SQL LANGUAGE EXPRESSION
# def db_reset():
#     # lets reset it
#     db.drop_all()
#     db.create_all()

#     # establish our connection
#     engine = create_engine(SQLALCHEMY_DATABASE_URI)
#     conn = engine.connect()


#     # load in our users
#     user_insert = User.__table__insert()
#     for user in users: # users is a list of namedtuples
#         conn.execute(user_insert, name=user.name, role=user.role)

#     # load in the organizations
#     organization_insert = Organization.__table__insert()
#     for organization in organizations:
#         conn.execute(organization_insert, name=organization.name)

#     con.execute(organization_insert(), [
#         {'

if __name__ == "__main__":
    db_reset()
