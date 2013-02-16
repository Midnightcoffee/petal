
from petalapp.database.models import User, Organization, SurveyHeader,\
    SurveyComment, Market,SurveySection, UserSurveySection, Answer, \
    UnitOfMeasurement, QuestionOption, OptionChoice, Question,OptionGroup, \
    InputType

from pprint import pprint as pp
tables = (User, Organization, SurveyHeader,SurveyComment, Market,SurveySection, UserSurveySection, 
Answer, UnitOfMeasurement, QuestionOption, OptionChoice, Question,OptionGroup, 
    InputType)
if __name__ == "__main__":
    for table in tables:
        pp("Table Name: {0} ::{1}".format(table.__name__,table.query.all()))
