from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
data = Table('data', pre_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('standard_form', Integer),
    Column('marketing_education', Integer),
    Column('record_availability', Integer),
    Column('family_centerdness', Integer),
    Column('pc_networking', Integer),
    Column('education_and_training', Integer),
    Column('team_funding', Integer),
    Column('coverage', Integer),
    Column('pc_for_expired_pts', Integer),
    Column('hospital_pc_screening', Integer),
    Column('pc_follow_up', Integer),
    Column('post_discharge_services', Integer),
    Column('bereavement_contacts', Integer),
    Column('certification', Integer),
    Column('team_wellness', Integer),
    Column('care_coordination', Integer),
    Column('timestamp', DateTime),
    Column('hospital_id', Integer),
)

answer = Table('answer', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('value', Integer),
    Column('hospital_id', Integer),
    Column('question_id', Integer),
    Column('survey_id', Integer),
)

question = Table('question', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('key', String(length=500)),
)

survey = Table('survey', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('release', String(length=50)),
    Column('timestamp', DateTime),
)

user = Table('user', pre_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('nickname', String),
    Column('email', String),
    Column('role', SmallInteger),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['data'].drop()
    post_meta.tables['answer'].create()
    post_meta.tables['question'].create()
    post_meta.tables['survey'].create()
    pre_meta.tables['user'].columns['nickname'].drop()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['data'].create()
    post_meta.tables['answer'].drop()
    post_meta.tables['question'].drop()
    post_meta.tables['survey'].drop()
    pre_meta.tables['user'].columns['nickname'].create()
