# coding: utf8

db.define_table('message_table',
				Field('message_id', 'string', unique=True, writable=False, label='Account ID'),
				Field('sender_id', 'reference account'),
				Field('receiver_id', 'reference account'),
				Field('m_subject', 'string', writable=True, label='Subject'),
				Field('m_body', 'text', writable=True, label='Subject'),
				Field('media_link', 'string', writable=True, label='list of media from'),
				Field('m_read', 'boolean', writable=False, default=False),
				Field('created', 'datetime', default=request.now, writable=False, label='Creation Date/Time'),
				Field('s_deleted', 'datetime', writable=False, label='Deleted Date/Time'),
				Field('r_deleted', 'datetime', writable=False, label='Deleted Date/Time'))

db.define_table('group_table',
				Field('group_id', 'string', unique=True, writable=False, label='Account ID'),
				Field('owner_id', 'reference account'),
				Field('g_name', 'string', writable=True, label='Group Name'),
				Field('created', 'datetime', default=request.now, writable=False, label='Creation Date/Time'),
				Field('deleted', 'datetime', writable=False, label='Last Log In Date/Time'))

db.define_table('group_members',
				Field('group_key', 'reference account'),
				Field('member_id', 'reference account'))

