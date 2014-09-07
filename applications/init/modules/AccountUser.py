#!/usr/bin/env python
# coding: utf8
from gluon import *

class Account:
	def __init__(self, db, accountID=''):
		self.db = db
		self.accountID = accountID

	def check_account_key(self, userID, accountKey):
		matched = False
		userAccount = self.get_account_id_by_user_id(userID)
		viewAccount = self.get_account_id_by_account_key(accountKey)
		if userAccount == viewAccount:
			matched = True

		return matched



	def get(self, accountID='', coded=''):
		if not accountID:
			accountID = self.accountID

		if accountID:
			query = self.db.account.id == accountID
			results = self.db(query).select().first()

			if results:
				account = {}
				account['ID'] = results.id
				account['accountId'] = results.account_id
				account['eMail'] = results.email
				account['address'] = results.address
				account['city'] = results.city
				account['zip_code'] = results.zip_code
				account['phone'] = results.phone
				account['created'] = results.created
				account['modified'] = results.modified
				account['status'] = results.status

				query1 = self.db.states.id == results.state_id
				stateHolder = self.db(query1).select().first()
				account['state'] = stateHolder.state_name
				query2 = self.db.countries.id == results.country_id
				countryHolder = self.db(query2).select().first()
				account['country'] = countryHolder.country_name

				if coded:
					account['gender'] = results.gender
					account['album'] = results.default_album
					account['friend'] = results.default_friend
					account['blog'] = results.default_blog

				else:
					query3 = self.db.gender_types.id == results.gender
					genderHolder = self.db(query3).select().first()
					account['gender'] = genderHolder.types
					query4 = self.db.friend_types.id > 0
					friends = self.db(query4).select()
					for friend in friends:
						if results.default_album == friend.id:
							account['album'] = friend.types
						if results.default_friend == friend.id:
							account['friend'] = friend.types
						if results.default_blog == friend.id:
							account['blog'] = friend.types


			else:
				account = False
		else:
			account = False

		return account

	def get_user_by_account(self, accountID=''):
		if not accountID:
			accountID = self.accountID

		if accountID:
			query = self.db.user_data.account_key == accountID
			results = self.db(query).select()

			if results:
				users = []
				for result in results:
					user = {}
					user['ID'] = result.id
					user['isPrimary'] = result.is_primary
					user['nickName'] = result.nick_name
					user['birthDay'] = result.birthday
					user['created'] = result.created
					user['lastLog'] = result.last_log
					user['status'] = result.status
					user['gender'] = result.gender

					users.append(user)

			else:
				users = False
		else:
			users = False

		return users

	def get_account_id_by_user_id(self, userID=''):
		if userID:
			query = self.db.user_data.user_id == userID
			result = self.db(query).select().first()
			if result:
				return result.account_key
			else:
				return False
		else:
			return False

	def get_account_id_by_account_key(self, accountKey=''):
		if accountKey:
			query = self.db.account.account_id == accountKey
			result = self.db(query).select().first()
			if result:
				return result.id
			else:
				return False
		else:
			return False

	def get_account_key_by_account_id(self, accountID=''):
		if accountID:
			query = self.db.account.id == accountID
			result = self.db(query).select().first()
			if result:
				return result.account_id
			else:
				return False
		else:
			return False

	def get_account_key_by_user_id(self, userID=''):
		winner = False
		if userID:
			query = self.db.user_data.user_id == userID
			result = self.db(query).select().first()
			if result:
				accountID = result.account_key
				if accountID:
					query = self.db.account.id == accountID
					result = self.db(query).select().first()
					if result:
						winner = result.account_id
		return winner

	def get_account_defaults(self, accountID=''):
		if accountID:
			query = self.db.account.id == accountID
			results = self.db(query).select().first()

			if results:
				account = {}
				account['album'] = results.default_album
				account['friend'] = results.default_friend
				account['blog'] = results.default_blog

				return account
		else:
			return False


	def create_account_and_add_user_data_and_profile(self, userID=''):
		account = False

		if userID:
			query = self.db.auth_user.id == userID
			data = self.db(query).select().first()

			if data:
				import uuid
				identifier = str(uuid.uuid1())
				from datetime import datetime
				if (data.first_name) or (data.last_name):
					screenName = data.first_name + data.last_name
				else:
					screenName=data.email
				
				accountID = self.db.account.insert(
					account_id=identifier,
					email=data.email,
					last_log=datetime.now())

				if accountID:
					dataID = self.db.user_data.insert(
						user_id=data.id,
						nick_name=screenName,
						account_key=accountID,
						is_primary=1,
						last_log=datetime.now())
					profileID = self.db.account_profile.insert(
						account_key=accountID,
						name=screenName,
						view_level=5,
						tag_line='Bask in this awesomeness')

					if dataID:
						account = accountID

		return account

	def get_basic_data_by_auth_id(self, userID=''):
		if userID:
			accountID = self.get_account_id_by_user_id(userID)
			if accountID:
				theBasics = self.get_basic_data_by_account_id(accountID, False, userID)

				return theBasics

			else:
				return False
		else:
			return False

	def get_basic_data_by_account_id(self, accountID='', simple='', userID=''):
		theBasics = {}
		if accountID:
			from Profile import Profile
			profileObj = Profile(self.db)
			profile = profileObj.get_profile_by_account_id(accountID)
			if not simple:
				query = self.db.user_data.user_id == userID
				nickName = self.db(query).select().first()
				query1 = self.db.account.id == accountID
				defaults = self.db(query1).select().first()
				if nickName:
					theBasics['name'] = nickName.nick_name
				if defaults:
					theBasics['friend'] = defaults.default_friend
					theBasics['blog'] = defaults.default_blog
				if profile:
					theBasics['backgroundImg'] = profile['backgroundImg']
					theBasics['profileTag'] = profile['tagLine']

			if profile:
				theBasics['profileName'] = profile['name']
				theBasics['profileImg'] = profile['profileImg']
				theBasics['accountKey'] = self.get_account_key_by_account_id(accountID)

			return theBasics

		else:
			return False

	def update_account_views_and_gender(self, accountID, gender, album, friend, blog):
		if accountID:
			query = self.db.account.id == accountID
			if self.db(query).update(gender=gender, default_album=album, default_friend=friend, default_blog=blog):
				return self.get(accountID, True)

	def get_available_accounts(self, userID):
		accounts = []
		if userID:
			accountID = self.get_account_id_by_user_id(userID)
			if accountID:
				query = self.db.account.id != accountID
				results = self.db(query).select(self.db.account.id, self.db.account.account_id)
				if results:
					for result in results:
						dataset = {}
						dataset['key'] = result.account_id
						from Profile import Profile
						profileObj = Profile(self.db)
						profile = profileObj.get_profile_by_account_id(result.id)
						if profile:
							dataset['profileName'] = profile['name']
							dataset['profileTag'] = profile['tagLine']
							dataset['profileImg'] = profile['profileImg']
							dataset['backgroundImg'] = profile['backgroundImg']

						accounts.append(dataset)

		return accounts

	def get_friend_level(self, userID, friendAccount):
		viewLevel = False
		if userID:
			accountID = self.get_account_id_by_user_id(userID)
			if accountID:
				friendID = self.get_account_id_by_account_key(friendAccount)
				if friendID:
					query = (self.db.friend_list.account_key == accountID) & (self.db.friend_list.friend_key == friendID)
					friend = self.db(query).select().first()
					if friend:
						viewLevel = friend.view_level

		return viewLevel

	def am_i_a_friend(self, userID, friendAccount):
		viewLevel = 5
		if userID:
			accountID = self.get_account_id_by_user_id(userID)
			if accountID:
				friendID = self.get_account_id_by_account_key(friendAccount)
				if friendID:
					query = (self.db.friend_list.account_key == friendID) & (self.db.friend_list.friend_key == accountID)
					friend = self.db(query).select().first()
					if friend:
						viewLevel = friend.view_level

		return viewLevel

	def create_comment(self, cType, key, commentT, mediaLink, userID):
		created=False
		if userID:
			accountID = self.get_account_id_by_user_id(userID)
			if accountID:
				album = ''
				media = ''
				status = ''
				if cType == 'album':
					query = self.db.account_albums.album_id == key
					aKey = self.db(query).select().first()
					album = aKey.id
				elif cType == 'media':
					media = key
				elif cType == 'status':
					status = key
				if self.db.comment_table.insert(
						album_key=album,
						media_key=media,
						status_key=status,
						poster_id=accountID,
						comment_text=commentT,
						media_link=mediaLink):
					created=True
		return created

	def get_comments(self, cType, key, accountKey, userID):
		comments = []
		if userID:
			accountID = self.get_account_id_by_user_id(userID)

		if accountKey == 'self':
			viewLevel = 1
		else:
			viewLevel = self.am_i_a_friend(userID, accountKey)

		if cType == 'album':
			query1 = self.db.account_albums.album_id == key
			aKey = self.db(query1).select().first()
			query = self.db.comment_table.album_key == aKey.id
		elif cType == 'media':
			query = self.db.comment_table.media_key == key
		elif cType == 'status':
			query = self.db.comment_table.status_key == key

		results = self.db(query).select()
		if results:
			for result in results:
				comment = {}
				if result.media_link:
					query = (self.db.upload_media.id == result.media_link) & (self.db.upload_media.view_level >= viewLevel)
					m_result = self.db(query).select().first()
					if m_result:
						comment['mediaLink'] = m_result.up_file
					else:
						comment['mediaLink'] = ''
				else:
					comment['mediaLink'] = ''
				basics = self.get_basic_data_by_account_id(result.poster_id, True)
				comment['posterKey'] = self.get_account_key_by_account_id(result.poster_id)
				comment['posterName'] = basics['profileName']
				comment['posterImg'] = basics['profileImg']
				comment['id'] = result.id
				comment['commentText'] = result.comment_text
				comment['created'] = result.created
				if result.album_key:
					comment['type'] = 'album'
					comment['key'] = result.album_key
				elif result.media_key:
					comment['type'] = 'media'
					comment['key'] = result.media_key
				elif result.status_key:
					comment['type'] = 'status'
					comment['key'] = result.status_key

				if (result.poster_id == accountID) or (accountKey == 'self'):
					comment['edit'] = True
				else:
					comment['edit'] = False

				comments.append(comment)

			return comments
		return False

	def edit_comment(self, commentID, commentT, mediaLink, userID):
		if userID:
			accountID = self.get_account_id_by_user_id(userID)
			if accountID:
				query = self.db.comment_table.id == commentID
				poster = self.db(query).select().first()
				if poster.poster_id == accountID:
					if self.db(query).update(comment_text=commentT, media_link=mediaLink):
						return True
				else:
					return False
			else:
				return False
		else:
			return False

	def delete_comment(self, commentID, userID, accountKey):
		if userID:
			accountID = self.get_account_id_by_user_id(userID)
			if accountID:
				query = self.db.comment_table.id == commentID
				poster = self.db(query).select().first()
				if (poster.poster_id == accountID) or (accountKey == 'self'):
					if self.db(query).delete():
						return True
				else:
					return False
			else:
				return False
		else:
			return False






