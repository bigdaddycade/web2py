# coding: utf8

db.define_table('friend_types',
				Field('types', 'string', writable=False, label='friend type key'))

db.define_table('gender_types',
				Field('types', 'string', writable=False, label='Gender'))

db.define_table('countries',
				Field('country_name', 'string', writable=False, label='Country Name'))

db.define_table('states',
				Field('state_name', 'string', writable=False, label='State Name'),
				Field('country_id', 'reference countries', default='1'))

db.define_table('account',
				Field('account_id', 'string', unique=True, writable=False, label='Account ID'),
				Field('email', 'string', requires=IS_EMAIL()),
				Field('default_friend', 'reference friend_types', default='4', requires=IS_IN_DB(db, db.friend_types.id, '%(types)s', zero=None), label='Default New Friends'),
				Field('default_blog', 'reference friend_types', default='5', requires=IS_IN_DB(db, db.friend_types.id, '%(types)s', zero=None), label='Default New Blog'),
				Field('default_album', 'reference friend_types', default='4', requires=IS_IN_DB(db, db.friend_types.id, '%(types)s', zero=None), label='Default New Album'),
				Field('show_me', 'boolean', label='Show me as logged in'),
				Field('show_me_filter', 'reference friend_types', default='5', requires=IS_IN_DB(db, db.friend_types.id, '%(types)s', zero=None), label='Filter who sees me logged in'),
				Field('gender', 'reference gender_types', requires=IS_IN_DB(db, db.gender_types.id, '%(types)s', zero=None), default='10', label='Gender'),
				Field('address', 'string', writable=True, label='Street Address'),
				Field('city', 'string', writable=True, label='City'),
				Field('state_id', 'reference states', requires=IS_IN_DB(db, db.states.id, '%(state_name)s', zero=None), default='53', label='State'),
				Field('zip_code', 'integer', label='Zip Code'),
				Field('country_id', 'reference countries', requires=IS_IN_DB(db, db.countries.id, '%(country_name)s', zero=None), default='249', label='Country'),
				Field('phone', 'string', label='Phone Number'),
				Field('created', 'datetime', default=request.now, writable=False, label='Creation Date/Time'),
				Field('modified', 'datetime', writable=False, default=request.now, update=request.now, label='Last Updated Date/Time'),
				Field('last_log', 'datetime', writable=False, label='Last Log In Date/Time'),
				Field('status', requires=IS_IN_SET(['Active', 'Disabled']), default='Active'))

db.define_table('user_data',
				Field('user_id', 'reference auth_user'),
				Field('account_key', 'reference account'),
				Field('is_primary', requires=IS_IN_SET([0, 1]), default=0, label='Account Administrator'),
				Field('nick_name', 'string', label='Nick Name'),
				Field('birthday', 'datetime', label='Day Month Year of your birth'),
				Field('gender', requires=IS_IN_SET(['Male', 'Female', 'TS/TV/TG', 'undeclared']), default='undeclared', label='Gender'),
				Field('created', 'datetime', default=request.now, writable=False, label='Creation Date/Time'),
				Field('last_log', 'datetime', writable=False, label='Last Log In Date/Time'),
				Field('status', requires=IS_IN_SET(['Active', 'Disabled']), default='Active', label='Can this user log in'))

db.define_table('friend_list',
				Field('account_key', 'reference account'),
				Field('friend_key', 'reference account'),
				Field('view_level', 'reference friend_types'))