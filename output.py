
Traceback (most recent call last):
  File "pci_notes/transfer/survey_to_database3.py", line 108, in <module>
    create_init_database()
  File "pci_notes/transfer/survey_to_database3.py", line 26, in create_init_database
    db.drop_all()
  File "/home/drew/.virtualenvs/staging/local/lib/python2.7/site-packages/flask_sqlalchemy.py", line 830, in drop_all
    self._execute_for_all_tables(app, bind, 'drop_all')
  File "/home/drew/.virtualenvs/staging/local/lib/python2.7/site-packages/flask_sqlalchemy.py", line 814, in _execute_for_all_tables
    op(bind=self.get_engine(app, bind), tables=tables)
  File "/home/drew/.virtualenvs/staging/local/lib/python2.7/site-packages/sqlalchemy/schema.py", line 2598, in drop_all
    tables=tables)
  File "/home/drew/.virtualenvs/staging/local/lib/python2.7/site-packages/sqlalchemy/engine/base.py", line 2302, in _run_visitor
    conn._run_visitor(visitorcallable, element, **kwargs)
  File "/home/drew/.virtualenvs/staging/local/lib/python2.7/site-packages/sqlalchemy/engine/base.py", line 1972, in _run_visitor
    **kwargs).traverse_single(element)
  File "/home/drew/.virtualenvs/staging/local/lib/python2.7/site-packages/sqlalchemy/sql/visitors.py", line 106, in traverse_single
    return meth(obj, **kw)
  File "/home/drew/.virtualenvs/staging/local/lib/python2.7/site-packages/sqlalchemy/engine/ddl.py", line 130, in visit_metadata
    self.traverse_single(table, drop_ok=True)
  File "/home/drew/.virtualenvs/staging/local/lib/python2.7/site-packages/sqlalchemy/sql/visitors.py", line 106, in traverse_single
    return meth(obj, **kw)
  File "/home/drew/.virtualenvs/staging/local/lib/python2.7/site-packages/sqlalchemy/engine/ddl.py", line 173, in visit_table
    self.connection.execute(schema.DropTable(table))
  File "/home/drew/.virtualenvs/staging/local/lib/python2.7/site-packages/sqlalchemy/engine/base.py", line 1449, in execute
    params)
  File "/home/drew/.virtualenvs/staging/local/lib/python2.7/site-packages/sqlalchemy/engine/base.py", line 1542, in _execute_ddl
    compiled
  File "/home/drew/.virtualenvs/staging/local/lib/python2.7/site-packages/sqlalchemy/engine/base.py", line 1698, in _execute_context
    context)
  File "/home/drew/.virtualenvs/staging/local/lib/python2.7/site-packages/sqlalchemy/engine/base.py", line 1691, in _execute_context
    context)
  File "/home/drew/.virtualenvs/staging/local/lib/python2.7/site-packages/sqlalchemy/engine/default.py", line 331, in do_execute
    cursor.execute(statement, parameters)
sqlalchemy.exc.InternalError: (InternalError) cannot drop table organization because other objects depend on it
DETAIL:  constraint survey_header_organization_id_fkey on table survey_header depends on table organization
HINT:  Use DROP ... CASCADE to drop the dependent objects too.
 '\nDROP TABLE organization' {}
Traceback (most recent call last):
  File "pci_notes/transfer/survey_to_database3.py", line 109, in <module>
    create_init_database()
  File "pci_notes/transfer/survey_to_database3.py", line 27, in create_init_database
    db.drop_all()
  File "/home/drew/.virtualenvs/staging/local/lib/python2.7/site-packages/flask_sqlalchemy.py", line 830, in drop_all
    self._execute_for_all_tables(app, bind, 'drop_all')
  File "/home/drew/.virtualenvs/staging/local/lib/python2.7/site-packages/flask_sqlalchemy.py", line 814, in _execute_for_all_tables
    op(bind=self.get_engine(app, bind), tables=tables)
  File "/home/drew/.virtualenvs/staging/local/lib/python2.7/site-packages/sqlalchemy/schema.py", line 2598, in drop_all
    tables=tables)
  File "/home/drew/.virtualenvs/staging/local/lib/python2.7/site-packages/sqlalchemy/engine/base.py", line 2302, in _run_visitor
    conn._run_visitor(visitorcallable, element, **kwargs)
  File "/home/drew/.virtualenvs/staging/local/lib/python2.7/site-packages/sqlalchemy/engine/base.py", line 1972, in _run_visitor
    **kwargs).traverse_single(element)
  File "/home/drew/.virtualenvs/staging/local/lib/python2.7/site-packages/sqlalchemy/sql/visitors.py", line 106, in traverse_single
    return meth(obj, **kw)
  File "/home/drew/.virtualenvs/staging/local/lib/python2.7/site-packages/sqlalchemy/engine/ddl.py", line 130, in visit_metadata
    self.traverse_single(table, drop_ok=True)
  File "/home/drew/.virtualenvs/staging/local/lib/python2.7/site-packages/sqlalchemy/sql/visitors.py", line 106, in traverse_single
    return meth(obj, **kw)
  File "/home/drew/.virtualenvs/staging/local/lib/python2.7/site-packages/sqlalchemy/engine/ddl.py", line 173, in visit_table
    self.connection.execute(schema.DropTable(table))
  File "/home/drew/.virtualenvs/staging/local/lib/python2.7/site-packages/sqlalchemy/engine/base.py", line 1449, in execute
    params)
  File "/home/drew/.virtualenvs/staging/local/lib/python2.7/site-packages/sqlalchemy/engine/base.py", line 1542, in _execute_ddl
    compiled
  File "/home/drew/.virtualenvs/staging/local/lib/python2.7/site-packages/sqlalchemy/engine/base.py", line 1698, in _execute_context
    context)
  File "/home/drew/.virtualenvs/staging/local/lib/python2.7/site-packages/sqlalchemy/engine/base.py", line 1691, in _execute_context
    context)
  File "/home/drew/.virtualenvs/staging/local/lib/python2.7/site-packages/sqlalchemy/engine/default.py", line 331, in do_execute
    cursor.execute(statement, parameters)
sqlalchemy.exc.InternalError: (InternalError) cannot drop table organization because other objects depend on it
DETAIL:  constraint survey_header_organization_id_fkey on table survey_header depends on table organization
HINT:  Use DROP ... CASCADE to drop the dependent objects too.
 '\nDROP TABLE organization' {}
Traceback (most recent call last):
  File "petalapp/database/models.py", line 10, in <module>
    db.Column('user_id', db.Integer, db.ForeignKey('user.id', ondelete='cascade')))
  File "/home/drew/.virtualenvs/staging/local/lib/python2.7/site-packages/flask_sqlalchemy.py", line 65, in _make_table
    return sqlalchemy.Table(*args, **kwargs)
  File "/home/drew/.virtualenvs/staging/local/lib/python2.7/site-packages/sqlalchemy/schema.py", line 305, in __new__
    "existing Table object." % key)
sqlalchemy.exc.InvalidRequestError: Table 'organizations' is already defined for this MetaData instance.  Specify 'extend_existing=True' to redefine options and columns on an existing Table object.
