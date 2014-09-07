# -*- coding: utf-8 -*-

apiVersion = '0.9'

import gluon.contrib.simplejson as simplejson

@auth.requires_login()
def edit_account_vg():
	response.view = 'generic.'+request.extension
	jsonData = simplejson.loads(request.body.read()) if request.body else {}
	
	from AccountUser import Account
	accountObj = Account(db)
	accountID = accountObj.get_account_id_by_user_id(session.auth.user.id)
	if accountID:
		account = accountObj.update_account_views_and_gender(accountID, jsonData['gender'], jsonData['albumLevel'], jsonData['friendLevel'], jsonData['blogLevel'])
		if account:
			return api_response(account=account)

####################################################
####################################################
##################### ALBUM ########################
####################################################
####################################################

@auth.requires_login()
def create_album():
	albums = {}
	response.view = 'generic.'+request.extension
	jsonData = simplejson.loads(request.body.read()) if request.body else {}

	from Media import Album
	albumObj = Album(db)
	if albumObj.create_album(jsonData['accountID'], jsonData['name'], jsonData['viewLevel'], jsonData['notes']):
		albums = albumObj.get_albums_by_account_id(jsonData['accountID'])

		return api_response(albums=albums)

@auth.requires_login()
def remove_album():
	response.view = 'generic.'+request.extension
	albumID = request.vars.album_id or None
	from Media import Album
	albumObj = Album(db)
	if albumObj.remove_album_by_id(albumID):

		return api_response(album='deleted')

@auth.requires_login()
def edit_album():
	response.view = 'generic.'+request.extension
	jsonData = simplejson.loads(request.body.read()) if request.body else {}

	from Media import Album
	albumObj = Album(db)
	album = albumObj.update_album(jsonData['albumId'], jsonData['name'], jsonData['viewLevel'], jsonData['description'], jsonData['update'])
	if album:
		return api_response(album=album)

####################################################
####################################################
##################### MEDIA ########################
####################################################
####################################################

@auth.requires_login()
def remove_media():
	album = {}
	response.view = 'generic.'+request.extension
	mediaID = request.vars.media_id or None
	albumID = request.vars.album_id or None
	from Media import Media
	mediaObj = Media(db)
	from Media import Album
	albumObj = Album(db)
	if mediaObj.remove_media_by_id(mediaID, albumID):
		album = albumObj.get(albumID)

	return api_response(album=album)

@auth.requires_login()
def edit_media():
	response.view = 'generic.'+request.extension
	jsonData = simplejson.loads(request.body.read()) if request.body else {}

	from Media import Media
	mediaObj = Media(db)
	if mediaObj.update_media(jsonData['mediaId'], jsonData['fileName'], jsonData['viewLevel'], jsonData['description']):

		return api_response(mediaId=jsonData['mediaId'])



@auth.requires_login()
@cache.action()
def image():
	"""
	it_is_ok = mediaObj.can_i_view_media(session.auth.user.id, request)
	if it_is_ok:
		return response.download(request, db)
	else:
		return False
	"""
	return response.download(request, db)

####################################################
####################################################
#################### PROFILE #######################
####################################################
####################################################

@auth.requires_login()
def edit_profile():
	response.view = 'generic.'+request.extension
	jsonData = simplejson.loads(request.body.read()) if request.body else {}

	from Profile import Profile
	profileObj = Profile(db)
	profile = profileObj.update_profile(jsonData['profileId'], jsonData['name'], jsonData['tagLine'], jsonData['viewLevel'])
	account = profileObj.get_account_data_for_profile_update(session.auth.user.id)
	albums = profileObj.get_albums_for_profile_update(jsonData['accountId'])
	return api_response(profile=profile, account=account, albums=albums)


@auth.requires_login()
def update_profile():
	response.view = 'generic.'+request.extension
	dataKey = request.vars.key or None
	dataValue = request.vars.value or None

	from Profile import Profile
	profileObj = Profile(db)
	if dataKey:
		if dataKey == 'newProfileImage':
			profileObj.edit_profile_images(session.auth.user.id, dataValue, 'profile')
		if dataKey == 'newBackGroundImage':
			profileObj.edit_profile_images(session.auth.user.id, dataValue, 'background')

	account = profileObj.get_account_data_for_profile_update(session.auth.user.id)
	profile = profileObj.get_profile_by_user_id_with_details(session.auth.user.id)
	albums = profileObj.get_albums_for_profile_update(profile['accountId'])
	return api_response(profile=profile, account=account, albums=albums)

@auth.requires_login()
def add_friend():
	response.view = 'generic.'+request.extension
	jsonData = simplejson.loads(request.body.read()) if request.body else {}

	from Profile import Profile
	profileObj = Profile(db)
	if profileObj.add_a_friend(session.auth.user.id, jsonData['accountKey'], jsonData['viewLevel']):
		if jsonData['viewLevel'] == '9':
			message = "no longer friends"
		else:
			message="now friends"
		return api_response(message=message)

####################################################
####################################################
#################### COMMENTS ######################
####################################################
####################################################

@auth.requires_login()
def fetch_comments():
	response.view = 'generic.'+request.extension
	jsonData = simplejson.loads(request.body.read()) if request.body else {}
	comments = False

	from AccountUser import Account
	accountObj = Account(db)
	comments = accountObj.get_comments(jsonData['cType'], jsonData['key'], jsonData['accountKey'], session.auth.user.id)
	
	return api_response(comments=comments)

@auth.requires_login()
def create_comment():
	response.view = 'generic.'+request.extension
	jsonData = simplejson.loads(request.body.read()) if request.body else {}

	from AccountUser import Account
	accountObj = Account(db)
	if accountObj.create_comment(jsonData['cType'], jsonData['key'], jsonData['commentT'], jsonData['mediaLink'], session.auth.user.id):
		comments = accountObj.get_comments(jsonData['cType'], jsonData['key'], jsonData['accountKey'], session.auth.user.id)
		return api_response(message='comment added', comments=comments)

@auth.requires_login()
def edit_comment():
	response.view = 'generic.'+request.extension
	jsonData = simplejson.loads(request.body.read()) if request.body else {}

	from AccountUser import Account
	accountObj = Account(db)
	if accountObj.edit_comment(jsonData['comment_id'], jsonData['commentT'], jsonData['mediaLink'], session.auth.user.id):
		return api_response(message='deleted')

@auth.requires_login()
def delete_comment():
	response.view = 'generic.'+request.extension
	commentId = request.vars.comment_id or None
	accountKey = request.vars.account_key or None

	from AccountUser import Account
	accountObj = Account(db)
	if accountObj.delete_comment(commentId, session.auth.user.id, accountKey):
		return api_response(message='deleted')

####################################################
####################################################
#################### GENERICS ######################
####################################################
####################################################

@auth.requires_login()
def basic_data():
	response.view = 'generic.'+request.extension
	from AccountUser import Account
	accountObj = Account(db)
	from Profile import Profile
	profileObj = Profile(db)
	basicData = {}
	basicData = accountObj.get_basic_data_by_auth_id(session.auth.user.id)
	basicData['friends'] = profileObj.get_friends_by_user_id(session.auth.user.id)
	return api_response(basicData=basicData)


@auth.requires_login()
def new_messages():
	response.view = 'generic.'+request.extension
	from SharMail import Message
	messageObj = Message(db)
	messages = messageObj.get_new_messages_by_auth_id(session.auth.user.id)
	return api_response(messages=messages)


@auth.requires_login()
def message_count():
	response.view = 'generic.'+request.extension
	from SharMail import Message
	messageObj = Message(db)
	count = messageObj.get_unread_message_count_by_auth_id(session.auth.user.id)
	return api_response(count=count)


@auth.requires_login()
def like_media():
	response.view = 'generic.'+request.extension
	reply = False
	mediaID = request.vars.media_id or None
	likeType = request.vars.l_type or None
	from Media import Media
	mediaObj = Media(db)
	if likeType == 'like':
		if mediaObj.like_media(mediaID, session.auth.user.id):
			reply = True;
	else:
		if mediaObj.like_media(mediaID, session.auth.user.id, True):
			reply = True;

	return api_response(success=reply)
	

def api_response(**kwargs) :
	resp = dict(**kwargs)

	resp.update({
		'version': apiVersion,
		'success': True,
	})

	return resp


def api_error(code, message='', info='') :
	from SHARError import Error
	errorHandler = Error()
	errorHandler.set_error(code, message, info)

	error_response = {
		'version': apiVersion,
		'success': False,
		'error': errorHandler.code,
		'reason': errorHandler.reason,
		'info': errorHandler.info,
	}