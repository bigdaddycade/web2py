# -*- coding: utf-8 -*-


from Media import Album, Media
from AccountUser import Account
accountObj = Account(db)
albumObj = Album(db)
mediaObj = Media(db)

from Profile import Profile
profileObj = Profile(db)

from Search import Search
searchObj = Search(db)

@auth.requires_login()
def new():

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
		greatest=searchObj.get_most_popular(session.auth.user.id),
		newest=searchObj.get_newest_media(session.auth.user.id),
		account=account,
		albums=albums,
		users=users,
		title=title)