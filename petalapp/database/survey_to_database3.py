'''
File: survey_to_database3.py
Date: 2013-02-06
Author: Drew Verlee
Description: contains the transfer script for initial setup
'''
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

#TODO move me
def in_database(instance, table):
    return table.query.filter_by(name=instance.name).first()


def create_init_database():
    db.drop_all()
    db.create_all()
    for user_package in users:
        user = User.query.filter_by(name=user_package.name).first()
        if not user:
            user = User(
                    name = user_package.name,
                    role = user_package.role,
                    )
        # markets
        for market_key in user_package.market_organization:
            m = Market.query.filter_by(name=market_key).first()
            if not m:
                m =  Market(name=market_key)
            # organizations
            for organization_name in user_package.market_organization[market_key]:
                org = Organization.query.filter_by(name=organization_name).first()
                if not org:
                    org = Organization(name = organization_name)
                # join
                user.organizations.append(org)
                m.organizations.append(org)
                db.session.add(m)
                # Survey_head
                for survey_header_package in survey_headers:
                    #survey_header = in_database(survey_header_package, SurveyHeader)
                    survey_header = SurveyHeader.query.filter_by(name=survey_header_package.name).first()
                    if not survey_header:
                        survey_header = SurveyHeader(
                                name = survey_header_package.name
                                                    )
                    # join
                    org.survey_headers.append(survey_header)
                    db.session.add(org)
                    #survey_sections
                    for survey_section_package in survey_header_package.survey_sections:
                        survey_section = in_database(survey_section_package, SurveySection)
                        if not survey_section:
                            survey_section = SurveySection(
                                    name = survey_section_package.name,
                                    subheading = survey_section_package.subheading,
                                    order= survey_section_package.order,
                                    section_required_yn = survey_section_package.section_required_yn
                                    )
                        #join survey header with survey sections
                        survey_header.survey_sections.append(survey_section)
                        # questions
                        for question_package in survey_section_package.questions:
                            question = in_database(question_package, Question)
                            if not question:
                                question = Question(
                                        name = question_package.name,
                                        value = question_package.value,
                                        order = question_package.order,
                                        answer_required_yn = question_package.answer_required_yn,
                                        subtext = question_package.subtext,
                                        )
                            # question section merge
                            survey_section.questions.append(question)
                            #input types
                            input_type = InputType.query.filter_by(name=question_package.input_type).first()
                            if not input_type:
                                input_type = InputType( name = question_package.input_type)
                            #merge question input type
                            input_type.questions.append(question)
                            db.session.add(input_type)
                            # OptionGroup
                            option_group = OptionGroup.query.filter_by(name=question_package.option_group_name).first()
                            if not option_group:
                                option_group = OptionGroup(
                                        name=question_package.option_group_name
                                        )
                            option_group.questions.append(question)
                            db.session.add(option_group)
                            #option choices
                            for choice in question_package.option_choice:
                                option_choice = OptionChoice.query.filter_by(name=choice).first()
                                if not option_choice:
                                    option_choice = OptionChoice(name=choice)
                                #merge option group and choice
                                option_group.option_choices.append(option_choice)
                                # question options
                                db.session.add(option_choice)
                                question_option = db.session.query(QuestionOption).\
                                        filter((QuestionOption.question == question)
                                                & (QuestionOption.option_choice == option_choice)).first()
                                if not question_option:
                                    question_option = QuestionOption()
                                    question.question_options.append(question_option)
                                    option_choice.question_options.append(question_option)
                                db.session.add(option_choice)
                                db.session.flush()
    points = UnitOfMeasurement('points')
    db.session.add(points)
    db.session.add(user)
    db.session.commit()

if __name__ == "__main__":
    create_init_database()
