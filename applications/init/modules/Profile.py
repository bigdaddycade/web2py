#!/usr/bin/env python
# coding: utf8
from gluon import *

class Profile:
	def __init__(self, db, profileID=''):
		self.db = db
		self.profileID = profileID

	def get(self, profileID='', details='', viewLevel=1):
		if not profileID:
			profileID = self.profileID

		if profileID:
			query = (self.db.account_profile.id == profileID) & (self.db.account_profile.view_level >= viewLevel)
			results = self.db(query).select().first()

			if results:
				profile = {}
				profile['tagLine'] = results.tag_line
				profile['viewLevel'] = results.view_level
				profile['name'] = results.name
				profile['profileImg'] = results.profile_img
				profile['backgroundImg'] = results.background_img

				if details:
					profile['profileId'] = results.id
					profile['accountId'] = results.account_key

				query = self.db.profile_data.profile_key == profileID
				p_results = self.db(query).select()
				if p_results:
					profile['data'] = []
					for p_result in p_results:
						p_data = {}
						p_data[p_result.data_type] = p_result.data_value
						p_data['viewLevel'] = p_result.view_level
						p_data['profileDataId'] = p_result.id

						profile['data'].append(p_data)

				else:
					profile['data'] = False


			else:
				profile = False
		else:
			profile = False

		return profile

	def get_profile_by_account_key(self, accountKey, viewLevel=5):
		query = self.db.account.account_id == accountKey
		result = self.db(query).select(self.db.account.id).first()
		if result:
			profile = self.get_profile_by_account_id(result.id, viewLevel)
			return profile
		else:
			return False

	def get_profile_by_account_id(self, accountID, viewLevel=1):
		profile = False
		query = self.db.account_profile.account_key == accountID
		result = self.db(query).select(self.db.account_profile.id).first()
		if result:
			profile = self.get(result.id, "", viewLevel)

		return profile

	def get_profile_by_account_id_with_details(self, accountID):
		query = self.db.account_profile.account_key == accountID
		result = self.db(query).select(self.db.account_profile.id).first()
		if result:
			details = True
			profile = self.get(result.id, details)

			return profile
		else:
			return False

	def get_profile_by_user_id(self, userID):
		query = self.db.user_data.user_id == userID
		result = self.db(query).select(self.db.user_data.account_key).first()
		if result:
			profile = self.get_profile_by_account_id(result.account_key)

			return profile
		else:
			return False

	def get_profile_by_user_id_with_details(self, userID):
		query = self.db.user_data.user_id == userID
		result = self.db(query).select(self.db.user_data.account_key).first()
		if result:
			profile = self.get_profile_by_account_id_with_details(result.account_key)

			return profile
		else:
			return False

	def edit_profile_images(self, userID, thumb, key):
		query = self.db.user_data.user_id == userID
		result = self.db(query).select(self.db.user_data.account_key).first()
		if result:
			query1 = self.db.account_profile.account_key == result.account_key
			if key == 'profile':
				self.db(query1).update(profile_img=thumb)
			elif key == 'background':
				self.db(query1).update(background_img=thumb)

			return True
		else:
			return False

	def get_account_data_for_profile_update(self, userID):
		account = {}
		query = self.db.user_data.user_id == userID
		accountID = self.db(query).select(self.db.user_data.account_key).first()
		if accountID:
			from AccountUser import Account
			accountObj = Account(self.db)
			result = accountObj.get(accountID.account_key)
			if result:
				account['gender'] = result['gender']
				account['eMail'] = result['eMail']
				account['phone'] = result['phone']
				account['address'] = result['address']
				account['city'] = result['city']
				account['state'] = result['state']
				account['zip_code'] = result['zip_code']
				account['country'] = result['country']

		return account

	def get_albums_for_profile_update(self, accountID):
		albums = []
		query = self.db.account_albums.account_key == accountID
		results = self.db(query).select()
		if results:
			for result in results:
				album = {}
				album['name']=result.name
				album['viewLevel']=result.view_level
				album['media'] = []
				query1 = self.db.upload_media.album_key == result.id
				dataList = self.db(query1).select()
				if dataList:
					for data in dataList:
						media={}
						media['ID']=data.id
						media['fileName']=data.file_name
						media['thumbnail']=data.thumbnail
						album['media'].append(media)
				else:
					album['media']=False

				albums.append(album)

			return albums
		else:
			return False

	def update_profile(self, profileID, name, tagLine, viewLevel):
		if profileID:
			query = self.db.account_profile.id == profileID
			if self.db(query).update(name=name, tag_line=tagLine, view_level=viewLevel):
				details = True
				return self.get(profileID, details)

	def add_profile_data(self, profileID, dataType, dataValue, viewLevel):
		if profileID:
			if self.db.profile_data.insert(
				profile_key=accountID,
				data_type=identifier,
				view_level=viewLevel,
				data_value=name):
				return True
			else:
				return False

	def add_a_friend(self, userID, friendAccount, viewLevel):
		success = False
		if userID:
			query = self.db.user_data.user_id == userID
			result = self.db(query).select(self.db.user_data.account_key).first()
			if result:
				query1 = self.db.account.account_id == friendAccount
				friendID = self.db(query1).select().first()
				if friendID:
					query2 = (self.db.friend_list.account_key == result.account_key) & (self.db.friend_list.friend_key == friendID.id)
					friend = self.db(query2).select().first()
					if friend:
						if viewLevel == '9':
							if self.db(query2).delete():
								success = True
						else:
							if self.db(query2).update(view_level=viewLevel):
								success = True
					else:
						if viewLevel != '9':
							if self.db.friend_list.insert(account_key=result.account_key, friend_key=friendID.id, view_level=viewLevel):
								success = True

		return success

	def get_friend_count_by_account_key(self, accountKey):
		friendCount = 0
		query = self.db.account.account_id == accountKey
		result = self.db(query).select(self.db.account.id).first()
		if result:
			friendCount = self.get_friend_count_by_account_id(result.id)
		
		return friendCount

	def get_friend_count_by_user_id(self, userID):
		friendCount = 0
		query = self.db.user_data.user_id == userID
		account = self.db(query).select(self.db.user_data.account_key).first()
		if account:
			friendCount = self.get_friend_count_by_account_id(account.account_key)
		
		return friendCount

	def get_friend_count_by_account_id(self, accountID):
		if accountID:
			query = self.db.friend_list.account_key == accountID
			results = self.db(query).count()
		
		return self.db(query).count()

	def get_friends_by_account_key(self, accountKey, userID=''):
		query = self.db.account.account_id == accountKey
		result = self.db(query).select(self.db.account.id).first()
		if result:
			myFriends = self.get_friends_by_account_id(result.id, True, userID)
		
		return myFriends

	def get_friends_by_user_id(self, userID):
		query = self.db.user_data.user_id == userID
		accountID = self.db(query).select(self.db.user_data.account_key).first()
		if accountID:
			myFriends = self.get_friends_by_account_id(accountID.account_key)
			return myFriends
		else:
			return False


	def get_friends_by_account_id(self, accountID, hideView=False, userID=''):
		myFriends = []
		if accountID:
			query = self.db.friend_list.account_key == accountID
			rawFriends =  self.db(query).select()
			if rawFriends:
				from Media import Album
				albumObj = Album(self.db)
				if userID:
					query = self.db.user_data.user_id == userID
					currentUserID = self.db(query).select(self.db.user_data.account_key).first()
				for friend in rawFriends:
					newfriend = {}
					query1 = self.db.account_profile.account_key == friend.friend_key
					query2 = self.db.account.id == friend.friend_key
					profile = self.db(query1).select().first()
					account = self.db(query2).select().first()
					newfriend['profileName'] = profile.name
					newfriend['profileImg'] = profile.profile_img
					newfriend['tag'] = profile.tag_line
					newfriend['images'] = albumObj.get_photo_count_by_account_key(account.account_id)
					if userID:
						if friend.friend_key == currentUserID.account_key:
							newfriend['key'] = ''
						else:
							newfriend['key'] = account.account_id
					else:
						newfriend['key'] = account.account_id
					if not hideView:
						newfriend['viewLevel'] = friend.view_level
					myFriends.append(newfriend)
				return myFriends
			else:
				return False