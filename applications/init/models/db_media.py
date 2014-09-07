# coding: utf8

db.define_table('account_albums',
				Field('account_key', 'reference account'),
				Field('album_id', 'string', unique=True, writable=False, label='Album ID'),
				Field('view_level', 'reference friend_types', default='4', requires=IS_IN_DB(db, db.friend_types.id, '%(types)s', zero=None)),
				Field('name', 'string', label='Album Name'),
                Field('description', 'text', writable=True),
				Field('created', 'datetime', default=request.now, writable=False, label='Creation Date/Time'),
				Field('modified', 'datetime', writable=False, default=request.now, update=request.now))


Album_image = db.define_table('upload_media',
				Field('album_key', 'reference account_albums'),
				Field('media_type', 'string', label='Media Type'),
				Field('file_name', represent = lambda x, row: "None" if x == None else x[:45]),
				Field('up_file', 'upload', uploadseparate=True, requires=IS_NOT_EMPTY()),
				Field('up_date', 'datetime', default=request.now),
				Field('view_level', 'reference friend_types'),
				Field('notes', 'text'),
				Field('thumbnail', 'upload', autodelete=True),
				Field('banner', 'upload', autodelete=True))

from Media import thumbnail_generator, banner_generator
box = (200, 200)
bannerbox = (450, 260)
Album_image.thumbnail.compute = lambda row: thumbnail_generator(row.up_file, box)
Album_image.banner.compute = lambda row: banner_generator(row.up_file, bannerbox)


db.define_table('deleted_media',
				Field('account_id', 'integer'),
				Field('album_id', 'integer'),
				Field('media_id', 'integer'),
				Field('media_type', 'string'),
				Field('up_file', 'string'),
				Field('delete_date', 'datetime', default=request.now))

db.define_table('media_likes',
				Field('account_key', 'reference account'),
				Field('media_key', 'reference upload_media'),
				Field('like_date', 'datetime', default=request.now))
