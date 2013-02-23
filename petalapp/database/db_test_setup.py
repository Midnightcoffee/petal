import unittest
from petalapp import db
# from pci_notes.name_storage import market_organization
from petalapp.database.db_functions import add_unique, number_of_organizations
from petalapp.database.models import User, Market, Organization, SurveyComment,\
    SurveyHeader, SurveySection, Question, Answer, QuestionOption, OptionChoice,\
    Question, InputType, UserSurveySection


class test_live_db(unittest.TestCase):

    def test_unique_market_actual(self):
        market_count = Market.query.count()
        message = 'expected size or market 6, actual size: ' + str(market_count)
        self.assertEqual(market_count, 6, message)

    def test_unique_make_organization_actual(self):
        org_count = Organization.query.count()
        message = 'expected size of organization' + str(number_of_organizations) + ' actual number '  + str(org_count)
        self.assertEqual(org_count, number_of_organizations, message)

    def test_organization_to_survey_header_join(self):
        for organization in Organization.query.all():
            survey_per_org = organization.survey_headers.count()
            message ="expected num of surveys for " + str(organization.name) + \
                "2, actual size: " + str(survey_per_org)
            self.assertEqual(survey_per_org, 2, message)

# if __name__ == "__main__":
#     unittest.main()
