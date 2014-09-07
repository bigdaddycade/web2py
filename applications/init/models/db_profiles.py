# coding: utf8

db.define_table('account_profile',
				Field('account_key', 'reference account'),
				Field('name', 'string', writable=True, label='Profile Name'),
				Field('view_level', 'reference friend_types', default='5', requires=IS_IN_DB(db, db.friend_types.id, '%(types)s', zero=None), label='Profile View Level'),
				Field('tag_line', 'string', writable=True, label='Profile Tag Line'),
				Field('profile_img', 'string', writable=True, label='Profile Image'),
				Field('background_img', 'string', writable=True, label='Profile Background'))

db.define_table('profile_data_types',
				Field('types', 'string', writable=False))

db.define_table('profile_data',
				Field('profile_key', 'reference account_profile'),
				Field('data_type', 'string', writable=False),
				Field('data_value', 'text'),
				Field('view_level', 'reference friend_types'))

db.define_table('comment_table',
				Field('album_key', 'reference account_albums', label='album comment'),
				Field('media_key', 'reference upload_media', label='media comment'),
				Field('status_key', 'integer', label='status update comment'),
				Field('poster_id', 'reference account', label='account making the comment'),
                Field('comment_text', 'text', writable=True),
				Field('media_link', 'reference upload_media'),
				Field('created', 'datetime', default=request.now, writable=False, label='Creation Date/Time'))

if auth.is_logged_in():
	from AccountUser import Account
	accountObj = Account(db)
	from Profile import Profile
	profileObj = Profile(db)

	basicData = accountObj.get_basic_data_by_auth_id(session.auth.user.id)
	if basicData:
		basicData['friends'] = profileObj.get_friends_by_user_id(session.auth.user.id)
		currentKey = accountObj.get_account_key_by_user_id(session.auth.user.id)
	else:
		basicData = {}
		basicData['friends'] = False
