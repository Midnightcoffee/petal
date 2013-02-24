'''
File: db_functions.py
Date: 2013-02-22
Author: Drew Verlee
Description: contains some useful functions run against the database
'''
from collections import namedtuple
from petalapp.database.models import UserSurveySection,SurveySection


SurveyTable = namedtuple('Survey_Table',['organization','organization_id','survey_header',
    'survey_section','survey_section_id','user_survey_section_id','completed','period_name',
    'period_start', 'period_end','assigned','due','questions'])

# FIXME pitfually slow!
import datetime
def most_recent_completed_uss(user):
    lids = []
    for o in user.organizations:
        for sh in o.survey_headers:
            for ss in sh.survey_sections:
                l = datetime.datetime(1,1,1)
                lid = None
                for uss in ss.user_survey_sections:
                    if o.id == uss.organization.id:
                        if l == datetime.datetime(1,1,1):
                            lid = uss.id
                        if (uss.completed_date and uss.completed_date >= l):
                            l = uss.completed_date
                            lid = uss.id
                lids.append(lid)
    return lids

def unpack(user_survey_section_ids):
    """given a list of ids return he labels i need to populate my views"""
    survey_tables = []
    # new = [int(x) for x in user_survey_section_ids if not type(x) == int]
    for user_survey_section_id in user_survey_section_ids:
        if user_survey_section_id:
            uss = UserSurveySection.query.get(user_survey_section_id)
            organization = uss.organization.name
            organization_id = uss.organization.id
            ss_id = uss.survey_section.id
            ss = SurveySection.query.get(ss_id)
            ss_name = ss.name
            sh_name = ss.survey_header.name
            survey_header = sh_name
            if uss.completed_date:
                completed = uss.completed_date.strftime("%Y-%d-%m")
            else:
                completed = uss.completed_date
            period_name = uss.period.name
            period_start = uss.period.start.strftime("%Y-%d-%m")
            period_end = uss.period.end.strftime("%Y-%d-%m")
            assigned = uss.assigned_due.assigned.strftime("%Y-%d-%m")
            due = uss.assigned_due.due.strftime("%Y-%d-%m")
            survey_table = SurveyTable(
                    organization=organization,
                    organization_id=organization_id,
                    survey_header=survey_header,
                    survey_section=ss_name,
                    survey_section_id=ss_id,
                    user_survey_section_id=user_survey_section_id,
                    period_name=period_name,
                    completed=completed,
                    period_start=period_start,
                    period_end=period_end,
                    assigned=assigned,
                    due=due,
                    questions=[]
                    )

            survey_tables.append(survey_table)
    return survey_tables

