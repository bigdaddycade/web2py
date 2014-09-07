#!/usr/bin/env python
# coding: utf8
from gluon import *

class Search:
	def __init__(self, db):
		self.db = db

	def get_most_popular(self, userID):
		greatest = []
		count = self.db.media_likes.media_key.count()
		results = self.db().select(self.db.media_likes.id, count, groupby = self.db.media_likes.media_key, orderby = ~count)
		if results:
			from AccountUser import Account
			accountObj = Account(self.db)
			for result in results:
				likeData = self.db(self.db.media_likes.id == result.media_likes.id).select().first()
				mediaData = self.db(self.db.upload_media.id == likeData.media_key).select().first()
				accountKey = self.get_account_key_by_album_id(mediaData.album_key)
				if mediaData.view_level >= accountObj.am_i_a_friend(userID, accountKey):
					media = {}
					media['likes'] = self.db(self.db.media_likes.media_key == likeData.media_key).count()
					media['thumb'] = mediaData.thumbnail
					media['album'] = self.get_album_key_by_album_id(mediaData.album_key)
					if accountObj.check_account_key(userID, accountKey):
						media['account'] = ""
					else:
						media['account'] = accountKey
					greatest.append(media)

			return greatest
		else:
			return False

	def get_newest_media(self, userID):
		newest = []
		results = self.db().select(self.db.upload_media.id, groupby = self.db.upload_media.album_key, orderby = ~self.db.upload_media.up_date)
		if results:
			from AccountUser import Account
			accountObj = Account(self.db)
			for result in results:
				mediaData = self.db(self.db.upload_media.id == result.id).select().first()
				accountKey = self.get_account_key_by_album_id(mediaData.album_key)
				if mediaData.view_level >= accountObj.am_i_a_friend(userID, accountKey):
					media = {}
					media['thumb'] = mediaData.thumbnail
					media['album'] = self.get_album_key_by_album_id(mediaData.album_key)
					if accountObj.check_account_key(userID, accountKey):
						media['account'] = ""
					else:
						media['account'] = accountKey
					newest.append(media)

			return newest
		else:
			return False

	def get_album_key_by_album_id(self, albumID):
		query = self.db.account_albums.id == albumID
		result = self.db(query).select().first()
		if result:
			return result.album_id
		else:
			return False

	def get_account_key_by_album_id(self, albumID):
			query = self.db.account_albums.id == albumID
			result = self.db(query).select().first()
			if result:
				query = self.db.account.id == result.account_key
				newResult = self.db(query).select().first()
				if newResult:
					return newResult.account_id
				else:
					return False