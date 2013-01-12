from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
question_header = Table('question_header', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('header', String(length=600)),
    Column('order', Integer),
)

question = Table('question', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('key', String(length=300)),
    Column('point', Integer),
    Column('question_header_id', Integer),
    Column('order', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['question_header'].columns['order'].create()
    post_meta.tables['question'].columns['order'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['question_header'].columns['order'].drop()
    post_meta.tables['question'].columns['order'].drop()
