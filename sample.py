from petalapp.database.models import *

for org in Organization.query.all():
    for sh in org.survey_headers:
        for ss in sh.survey_sections:
            mco,mc = None,None
            for uss in ss.user_survey_sections:
                if uss.organization.id == org.id:
                    if uss.completed_date != None:
                        if mco < uss.completed_date.toordinal():
                            mco = uss.completed_date.toordinal()
                            mc = uss.completed_date
            print(mc)



