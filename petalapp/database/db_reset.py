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
# from pci_notes.storage.survey_headers.pci import survey_headers
# from pci_notes.storage.users import users
# from pci_notes.storage.market_organization import market_organization

# from petalapp.config import SQLALCHEMY_DATABASE_URI
# from pci_notes.storage.name_storage import input_types, option_groups,\
#    units_of_measurements
from pci_notes.survey import markets, users, survey_headers,\
    input_types, option_groups, units_of_measurements


def db_reset():
    db.drop_all()
    db.create_all()

    # units_of_measurements
    uoms = []
    for u_om in units_of_measurements:
        uom = UnitOfMeasurement(name=u_om.name)
        db.session.add(uom)
        uoms.append(uom)

    # input_types
    its = []
    for i_t in input_types:
        it = InputType(name=i_t.name)
        its.append(it)
        db.session.add(it)

    # option_group_choice
    ogs = {}
    ocs = []
    for o_g in option_groups:
        og = OptionGroup(name=o_g.name)
        for o_c in o_g.option_choices:
            oc = OptionChoice(name=o_c.name)
            ocs.append(oc)
            og.option_choices.append(oc)
        db.session.add(og)
        ogs[og] = ocs

    #survey_headers, survey_sections, questions, option_group, etc..
    shs = []
    for s_h in survey_headers:
        sh = SurveyHeader(name=s_h.name)
        for s_s in s_h.survey_sections:
            ss = SurveySection(name=s_s.name,subheading=s_s.subheading,
                order=s_s.order)
            for q_u in s_s.questions:
                q = Question(name=q_u.name, value=q_u.value, order=q_u.order,
                    answer_required_yn=q_u.answer_required_yn,
                        subtext=q_u.subtext,
                    allow_mult_options_answers_yn=q_u.allow_mult_options_answers_yn)
                for it in its:
                    if it.name ==  q_u.input_type.name:
                        it.questions.append(q)
                for og in ogs:
                    if og.name == q_u.option_group.name:
                        og.questions.append(q)
                    for oc in ogs[og]:
                        qo = QuestionOption()
                        q.question_options.append(qo)
                        oc.question_options.append(qo)
                ss.questions.append(q)
            sh.survey_sections.append(ss)
        db.session.add(sh)
        shs.append(sh)


    orgs = []
    for m in markets:
        market = Market(name=m.name)
        for o in m.organizations:
            org = Organization(name=o.name)
            for sh in shs:
                for osh in o.survey_headers:
                    if osh.name == sh.name:
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

if __name__ == "__main__":
    db_reset()
