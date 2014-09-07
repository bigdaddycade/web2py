# -*- coding: utf-8 -*-
#
#
######### ALL UUID VALUES FOR ID IN PROFILE ARE ACCOUNTKEY

from Media import Album, Media
from AccountUser import Account
accountObj = Account(db)
albumObj = Album(db)
mediaObj = Media(db)

from Profile import Profile
profileObj = Profile(db)

@auth.requires_login()
def index():
	accountKey = request.vars.account_key or None
	angularData = {}

	if accountKey:
		editButton = XML('<div class="pointer" ng-click=""><i class="fa fa-users fa-2x"></i><br>Add to Friend List</div>')
		angularData['profile']=profileObj.get_profile_by_account_key(accountKey)
		angularData['albums'] = albumObj.get_albums_by_account_key(accountKey)
	else:
		editButton = XML('<div class="pointer" ng-click="viewContent(\'editProfile\')"><i class="fa fa-cogs fa-2x"></i><br>Edit Profile</div>')
		angularData['profile']=profileObj.get_profile_by_user_id(session.auth.user.id)
		angularData['albums'] = albumObj.get_albums_by_user_id(session.auth.user.id)

	###ADD VIEW PERMISSIONS###
	

	return dict(angularData=angularData, editButton=editButton)

@auth.requires_login()
def edit():
	angularData = {}
	angularData['account']=profileObj.get_account_data_for_profile_update(session.auth.user.id)
	if angularData['account']:
		angularData['profile']=profileObj.get_profile_by_user_id_with_details(session.auth.user.id)
		angularData['albums']=profileObj.get_albums_for_profile_update(angularData['profile']['accountId'])

	return dict(angularData=angularData)

@auth.requires_login()
def about():
	accountKey = request.vars.account_key or None
	profile = {}
	photoCount = 0
	friendCount = 0
	messageButton = False
	isFriend = False
	iAmAFriend = False

	if accountKey:
		if accountObj.check_account_key(session.auth.user.id, accountKey):
			redirect(URL('profile', 'about'))
		isFriend = accountObj.get_friend_level(session.auth.user.id, accountKey)
		if isFriend == 6:
			redirect(URL('profile', 'broken', vars=dict(account_key=accountKey)))
		viewLevel = accountObj.am_i_a_friend(session.auth.user.id, accountKey)
		if viewLevel == 6:
			redirect(URL('profile', 'broken'))
		elif viewLevel <= 4:
			iAmAFriend = True
		
		messageButton = XML('<li><a href="messages.html?lang=en"><i class="fa fa-fw icon-envelope-fill-1"></i> <span> Send Message</span></a></li>')
		profile = profileObj.get_profile_by_account_key(accountKey, viewLevel)
		friendCount = profileObj.get_friend_count_by_account_key(accountKey)
		photoCount = albumObj.get_photo_count_by_account_key(accountKey, viewLevel)

	else:
		iAmAFriend = 'self'
		profile = profileObj.get_profile_by_user_id(session.auth.user.id)
		friendCount = profileObj.get_friend_count_by_user_id(session.auth.user.id)
		photoCount = albumObj.get_photo_count_by_user_id(session.auth.user.id)
	

	if not isFriend:
		isFriend = 'false'
	return dict(profile=profile,
		photoCount=photoCount,
		friendCount=friendCount,
		isFriend=isFriend,
		iAmAFriend=iAmAFriend,
		messageButton=messageButton)

@auth.requires_login()
def albums():
	accountKey = request.vars.account_key or None
	albumKey = request.vars.album_key or None
	view = {}
	profile = {}
	albums = False
	album = False
	photoCount = 0
	friendCount = 0
	messageButton = False
	isFriend = False
	comments = False
	iAmAFriend = False

	if accountKey:
		if accountObj.check_account_key(session.auth.user.id, accountKey):
			redirect(URL('profile', 'albums'))
		isFriend = accountObj.get_friend_level(session.auth.user.id, accountKey)
		if isFriend == 6:
			redirect(URL('profile', 'broken', vars=dict(account_key=accountKey)))
		viewLevel = accountObj.am_i_a_friend(session.auth.user.id, accountKey)
		if viewLevel == 6:
			redirect(URL('profile', 'broken'))
		elif viewLevel <= 4:
			iAmAFriend = True
		view['home']=False
		messageButton = XML('<li><a href="messages.html?lang=en"><i class="fa fa-fw icon-envelope-fill-1"></i> <span> Send Message</span></a></li>')
		profile = profileObj.get_profile_by_account_key(accountKey, viewLevel)
		friendCount = profileObj.get_friend_count_by_account_key(accountKey)
		photoCount = albumObj.get_photo_count_by_account_key(accountKey, viewLevel)
		albums = albumObj.get_albums_by_account_key(accountKey, viewLevel, session.auth.user.id)
	else:
		iAmAFriend = 'self'
		view['home']=True
		profile = profileObj.get_profile_by_user_id(session.auth.user.id)
		friendCount = profileObj.get_friend_count_by_user_id(session.auth.user.id)
		photoCount = albumObj.get_photo_count_by_user_id(session.auth.user.id)
		albums = albumObj.get_albums_by_user_id(session.auth.user.id)

	if albumKey:
		for rawAlbum in albums:
			if rawAlbum['albumKey'] == albumKey:
				album = rawAlbum
				view['main'] = 'images'
				if accountKey:
					comments = accountObj.get_comments('album', albumKey, accountKey, session.auth.user.id)
				else:
					comments = accountObj.get_comments('album', albumKey, 'self', session.auth.user.id)
	else:
		view['main'] = 'albums'


	if not isFriend:
		isFriend = 'false'
	return dict(profile=profile,
		photoCount=photoCount,
		friendCount=friendCount,
		messageButton=messageButton,
		albums=albums,
		album=album,
		isFriend=isFriend,
		comments=comments,
		iAmAFriend=iAmAFriend,
		view=view)

@auth.requires_login()
def browse():
	profiles = []

	profiles = accountObj.get_available_accounts(session.auth.user.id)
	
	return dict(profiles=profiles)

@auth.requires_login()
def broken():
	accountKey = request.vars.account_key or None
	profile = {}
	photoCount = 0
	friendCount = 0
	messageButton = False
	isFriend = False
	comments = False
	iAmAFriend = False

	if accountKey:
		isFriend = accountObj.get_friend_level(session.auth.user.id, accountKey)
		if not isFriend:
			redirect(URL('profile', 'about', vars=dict(account_key=accountKey)))
		viewLevel = accountObj.am_i_a_friend(session.auth.user.id, accountKey)
		if viewLevel == 6:
			redirect(URL('profile', 'broken'))
		profile = profileObj.get_profile_by_account_key(accountKey, viewLevel)
		friendCount = profileObj.get_friend_count_by_account_key(accountKey)
		photoCount = albumObj.get_photo_count_by_account_key(accountKey, viewLevel)
	else:	
		profile = profileObj.get_profile_by_user_id(session.auth.user.id)
		friendCount = profileObj.get_friend_count_by_user_id(session.auth.user.id)
		photoCount = albumObj.get_photo_count_by_user_id(session.auth.user.id)

	if not isFriend:
		isFriend = 'false'
	return dict(profile=profile,
		photoCount=photoCount,
		friendCount=friendCount,
		messageButton=messageButton,
		comments=comments,
		iAmAFriend=iAmAFriend,
		isFriend=isFriend)

@auth.requires_login()
def friends():
	accountKey = request.vars.account_key or None
	profile = {}
	photoCount = 0
	friendCount = 0
	messageButton = False
	isFriend = False
	friends = False
	comments = False
	iAmAFriend = False

	if accountKey:
		if accountObj.check_account_key(session.auth.user.id, accountKey):
			redirect(URL('profile', 'friends'))
		isFriend = accountObj.get_friend_level(session.auth.user.id, accountKey)
		if isFriend == 6:
			redirect(URL('profile', 'broken', vars=dict(account_key=accountKey)))
		viewLevel = accountObj.am_i_a_friend(session.auth.user.id, accountKey)
		if viewLevel == 6:
			redirect(URL('profile', 'broken'))
		elif viewLevel <= 4:
			iAmAFriend = True
		messageButton = XML('<li><a href="messages.html?lang=en"><i class="fa fa-fw icon-envelope-fill-1"></i> <span> Send Message</span></a></li>')
		profile = profileObj.get_profile_by_account_key(accountKey, viewLevel)
		friendCount = profileObj.get_friend_count_by_account_key(accountKey)
		photoCount = albumObj.get_photo_count_by_account_key(accountKey, viewLevel)
		friends = profileObj.get_friends_by_account_key(accountKey, session.auth.user.id)
	else:
		iAmAFriend = 'self'
		profile = profileObj.get_profile_by_user_id(session.auth.user.id)
		friendCount = profileObj.get_friend_count_by_user_id(session.auth.user.id)
		photoCount = albumObj.get_photo_count_by_user_id(session.auth.user.id)
	

	if not isFriend:
		isFriend = 'false'
	return dict(profile=profile,
		photoCount=photoCount,
		friendCount=friendCount,
		isFriend=isFriend,
		friends=friends,
		comments=comments,
		iAmAFriend=iAmAFriend,
		messageButton=messageButton)