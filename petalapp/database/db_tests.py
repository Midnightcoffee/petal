
import unittest

from petalapp import db

from petalapp.database.models import User, Market, Organization, SurveyComment,\
    SurveyHeader, SurveySection, Question, Answer, QuestionOption, OptionChoice,\
    Question, InputType, UserSurveySection


from petalapp.database.db_functions import add_unique, number_of_organizations
from pci_notes.survey_to_database2 import build_survey, create_survey

#maybe useful later?


class TestUniqueColumns(unittest.TestCase):

    def setUp(self):
        db.drop_all()
        db.create_all()

        add_unique('amarket', Market)
        add_unique('amarket', Market)
        add_unique('aorg', Organization)
        add_unique('aorg', Organization)

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_unique_make_market(self):
        market_count = Market.query.count()
        message = 'expected size or market 1, actual size: ' + str(market_count)
        self.assertEqual(market_count, 1, message)

    def test_unique_make_organization(self):
        org_count = Organization.query.count()
        message = 'expected size of organization 1, actual size: ' + str(org_count)
        self.assertEqual(org_count, 1, message)




class test_actual_database_setup(unittest.TestCase):
    """
    Test just for instal setup,
    Number of organizations should be  18
    Markets should be 6
    Survey Headers 2
    """

    def setUp(self):
        db.drop_all()
        db.create_all()
        create_survey()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_unique_market_actual(self):
        market_count = Market.query.count()
        message = 'expected size or market 6, actual size: ' + str(market_count)
        self.assertEqual(market_count, 6, message)

    def test_unique_make_organization_actual(self):
        org_count = Organization.query.count()
        message = 'expected size of organization' + str(number_of_organizations) + ' actual number '  + str(org_count)
        self.assertEqual(org_count, number_of_organizations, message)

    def test_number_of_survey_headers(self):
        self.assertEqual(SurveyHeader.query.count(), 2*number_of_organizations, 'expected 2')

    def test_organization_to_survey_header_join(self):
        for organization in Organization.query.all():
            survey_per_org = organization.survey_headers.count()
            message ="expected num of surveys for " + str(organization.name) + \
                "2, actual size: " + str(survey_per_org)
            self.assertEqual(survey_per_org, 2, message)

if __name__ == "__main__":
    unittest.main()


