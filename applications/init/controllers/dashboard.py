# -*- coding: utf-8 -*-


from Media import Album, Media
from AccountUser import Account
accountObj = Account(db)
albumObj = Album(db)
mediaObj = Media(db)

from Profile import Profile
profileObj = Profile(db)

@auth.requires_login()
def index():

	account={}
	users={}
	title = {}
	albums = {}
	albums['blocked']=[]
	albums['public']=[]
	albums['friends']=[]
	albums['goodFriends']=[]
	albums['innerCircle']=[]
	albums['private']=[]
	title['set4'] = 'Profile Settings'
	title['subtitle4'] = 'Set profile name, tag line, and view settings. WARNING-you can only search profiles of equal or greater view setting:'
	
	
	accountID = accountObj.get_account_id_by_user_id(session.auth.user.id)
	if not accountID:
		accountID = accountObj.create_account_and_add_user_data_and_profile(session.auth.user.id)
		if accountID:
			redirect(URL('dashboard', 'index'))

	if accountID:
		account=accountObj.get(accountID)
		users=accountObj.get_user_by_account(accountID)
		rawAlbums=albumObj.get_albums_by_account_id(accountID)
		if rawAlbums:
			for album in rawAlbums:
				if album['viewLevel'] == 1:
					albums['private'].append(album)
				elif album['viewLevel'] == 2:
					albums['innerCircle'].append(album)
				if album['viewLevel'] == 3:
					albums['goodFriends'].append(album)
				elif album['viewLevel'] == 4:
					albums['friends'].append(album)
				if album['viewLevel'] == 5:
					albums['public'].append(album)
				elif album['viewLevel'] == 6:
					albums['blocked'].append(album)

	
	return dict(
		account=account,
		albums=albums,
		users=users,
		title=title)



@auth.requires_login()
def account():

	account={}
	albums = {}
	profile={}
	albums = {}
	title = {}
	title['main'] = 'Account Settings'
	
	accountID = accountObj.get_account_id_by_user_id(session.auth.user.id)
	if not accountID:
		accountID = accountObj.create_account_and_add_user_data_and_profile(session.auth.user.id)
		if accountID:
			redirect(URL('dashboard', 'index'))

	if accountID:
		account=accountObj.get(accountID, True)
		albums=albumObj.get_albums_by_account_id(accountID)
		profile = profileObj.get_profile_by_user_id(session.auth.user.id)

	title['form2'] = 'Location Information'
	title['subtitle2'] = 'You can not search by location till this is set, but this information is not public till you allow it in "profile settings":'
	query2 = db.account(db.account.id==accountID)
	form2 = SQLFORM(db.account, query2, submit_button = 'Update Location', deletable=False, showid=False, fields=[
		'phone',
		'address',
		'city',
		'state_id',
		'zip_code',
		'country_id'
	])

	if form2.process().accepted:
		redirect(URL('dashboard', 'index'))
	elif form2.errors:
		response.flash = 'The form contains errors.'

	title['form4'] = 'Profile Settings'
	title['subtitle4'] = 'Set profile name, tag line, and view settings. WARNING-you can only search profiles of equal or greater view setting:'
	query4 = db.account_profile(db.account_profile.account_key==accountID)
	form4 = SQLFORM(db.account_profile, query4, submit_button = 'Update Profile', deletable=False, showid=False, fields=[
		'name',
		'tag_line',
		'view_level'
	])

	if form4.process().accepted:
		redirect(URL('dashboard', 'account'))
	elif form4.errors:
		response.flash = 'The form contains errors.'

	return dict(
		account=account,
		profile=profile,
		albums=albums,
		title=title,
		form2=form2,
		form4=form4)


@auth.requires_login()
def album():
	albumID = request.vars.album_id or None
	angularData = {}

	if albumID:
		angularData['album']=albumObj.get(albumID)

		form = FORM(LABEL("Add image(s) to album:"), INPUT(_name='up_files', _type='file', _multiple='', _accept='image/*', requires=IS_NOT_EMPTY()),  BR(),INPUT(_type='submit', _value='Add to Album'))
		if form.accepts(request.vars, formname="form"):
			files = request.vars['up_files']
			if not isinstance(files, list):
				files = [files]
			for f in files:
				print f.filename
				up_file = db.upload_media.up_file.store(f, f.filename)
				i = db.upload_media.insert(
					notes=request.vars.notes,
					up_file=up_file,
					file_name=f.filename,
					album_key=albumID,
					view_level=angularData['album']['viewLevel'],
					media_type='image')
				db.commit()
			redirect(URL('dashboard', 'album', vars=dict(album_id=albumID)))
		return dict(form=form, angularData=angularData)

@auth.requires_login()
def media_edit():
	albumKey = request.vars.album_key or None
	flag = request.vars.flag or None

	users={}
	title = {}
	albums = {}
	album = False
	view = {}
	#prevents delete if account and album dont match
	match = False
	albums['blocked']=[]
	albums['public']=[]
	albums['friends']=[]
	albums['goodFriends']=[]
	albums['innerCircle']=[]
	albums['private']=[]

	import uuid
	identifier = str(uuid.uuid1())
	
	
	accountID = accountObj.get_account_id_by_user_id(session.auth.user.id)
	if accountID:
		account=accountObj.get(accountID, True)
		users=accountObj.get_user_by_account(accountID)
		rawAlbums=albumObj.get_albums_by_account_id(accountID)
		if rawAlbums:
			for thisalbum in rawAlbums:
				if albumKey:
					if albumKey == thisalbum['albumKey']:
						#validates the account to the album for delete pruposes
						match = True
				if thisalbum['viewLevel'] == 1:
					albums['private'].append(thisalbum)
				elif thisalbum['viewLevel'] == 2:
					albums['innerCircle'].append(thisalbum)
				if thisalbum['viewLevel'] == 3:
					albums['goodFriends'].append(thisalbum)
				elif thisalbum['viewLevel'] == 4:
					albums['friends'].append(thisalbum)
				if thisalbum['viewLevel'] == 5:
					albums['public'].append(thisalbum)
				elif thisalbum['viewLevel'] == 6:
					albums['blocked'].append(thisalbum)

	if albumKey:
		view = 'images'
		album = albumObj.get_albums_by_album_key(albumKey)
		if flag == 'deleteMe':
			if match:
				if albumObj.remove_album_by_key(albumKey):
					redirect(URL('dashboard', 'media_edit', vars=dict(flag='deleted')))
				else:
					redirect(URL('dashboard', 'media_edit', vars=dict(album_key=albumKey, flag='wrong')))
			else:
				redirect(URL('dashboard', 'media_edit', vars=dict(album_key=albumKey, flag='mismatch')))

		query = db.account_albums(db.account_albums.album_id==albumKey)
		form = SQLFORM(db.account_albums, query, submit_button = 'Update Album', deletable=False, showid=False, fields=[
			'name',
			'description',
			'view_level'
		])
		form.element(_id="account_albums_description", replace=TEXTAREA(
			_class="text",
			_id="account_albums_description",
			value=album['description'],
			_name="description",
			_rows="4"))
		
		if form.process().accepted:
			if form.vars.view_level != album['viewLevel']:
				mediaObj.reset_media_view_level_to_album(album['albumId'], form.vars.view_level)
			redirect(URL('dashboard', 'media_edit', vars=dict(album_key=albumKey, flag='updated')))
		elif form.errors:
			response.flash = 'The form contains errors.'


		if album['albumId']:

			form1 = FORM(INPUT(_name='up_files', _type='file', _multiple='', _accept='image/*', requires=IS_NOT_EMPTY()),  BR(),INPUT(_type='submit', _value='Add to Album'))
			if form1.accepts(request.vars, formname="form1"):
				files = request.vars['up_files']
				if not isinstance(files, list):
					files = [files]
				for f in files:
					print f.filename
					up_file = db.upload_media.up_file.store(f, f.filename)
					i = db.upload_media.insert(
						notes=request.vars.notes,
						up_file=up_file,
						file_name=f.filename,
						album_key=album['albumId'],
						view_level=album['viewLevel'],
						media_type='image')
					db.commit()
				redirect(URL('dashboard', 'media_edit', vars=dict(album_key=albumKey, flag='media')))

		return dict(
			albums=albums,
			thisalbum=album,
			view=view,
			users=users,
			form=form,
			form1=form1)
	else:
		view = 'albums'

		form = SQLFORM(db.account_albums, submit_button = 'Create New Album', fields=[
			'name',
			'description',
			'view_level'
		])
		form.vars.view_level = account['album']
		form.vars.account_key = accountID
		form.vars.album_id = identifier
		if form.process().accepted:
			redirect(URL('dashboard', 'media_edit', vars=dict(album_key=identifier, flag='created')))
		elif form.errors:
			response.flash = 'The form contains errors.'

		return dict(
			albums=albums,
			thisalbum=album,
			view=view,
			users=users,
			form=form)

@auth.requires_login()
def media_advanced():
	accountKey = request.vars.account_key or None
	albumKey = request.vars.album_key or None
	flag = request.vars.flag or 'edit'
	view = {}
	albums = False
	album = False
	
	if accountKey:
		view['home']=False
		albums = albumObj.get_albums_by_account_key(accountKey)
	else:
		view['home']=True
		albums = albumObj.get_albums_by_user_id(session.auth.user.id)

	if albumKey:
		view['main'] = 'images'
		album = albumObj.get_albums_by_album_key(albumKey)
	else:
		view['main'] = 'albums'


	return dict(albums=albums,
		album=album,
		view=view,
		flag=flag)
