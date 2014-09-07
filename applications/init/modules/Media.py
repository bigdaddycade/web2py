#!/usr/bin/env python
# coding: utf8
from gluon import *

import os
try:
	from PIL import Image, ImageOps
except:
	import Image, ImageOps

class Album:
	def __init__(self, db, albumID=''):
		self.db = db
		self.albumID = albumID

	def get(self, albumID='', viewLevel=1, requestorID='self'):
		if requestorID != 'self':
			query = self.db.user_data.user_id == requestorID
			result = self.db(query).select().first()
			if result:
				accountID = result.account_key
		if not albumID:
			albumID = self.albumID

		if albumID:
			query = self.db.account_albums.id == albumID
			results = self.db(query).select().first()

			if results:
				album = {}
				album['albumKey'] = results.album_id
				album['albumId'] = results.id
				album['viewLevel'] = results.view_level
				album['name'] = results.name
				album['description'] = results.description
				album['created'] = results.created
				album['modified'] = results.modified

				query = (self.db.upload_media.album_key == albumID) & (self.db.upload_media.view_level >= viewLevel)
				m_results = self.db(query).select()
				if m_results:
					album['media'] = []
					for m_result in m_results:
						media = {}
						media['mediaId'] = m_result.id
						media['mediaType'] = m_result.media_type
						media['uploadDate'] = m_result.up_date
						media['viewLevel'] = m_result.view_level
						media['description'] = m_result.notes
						media['fileName'] = m_result.file_name
						media['media_data'] = m_result.up_file
						media['thumb_data'] = m_result.thumbnail
						media['banner_data'] = m_result.banner
						queryC = self.db.media_likes.media_key == m_result.id
						media['likes'] = self.db(queryC).count()
						media['isLiked'] = False
						if requestorID != 'self':
							queryL = (self.db.media_likes.media_key == m_result.id) & (self.db.media_likes.account_key == accountID)
							if self.db(queryL).select().first():
								media['isLiked'] = True
						else:
							media['isLiked'] = 'self'

						album['media'].append(media)

				else:
					album['media'] = False


			else:
				album = False
		else:
			album = False

		return album

	def get_albums_by_account_key(self, accountKey, viewLevel=5, requestorID='self'):
		query = self.db.account.account_id == accountKey
		result = self.db(query).select(self.db.account.id).first()
		if result:
			albums = self.get_albums_by_account_id(result.id, viewLevel, requestorID)

			return albums
		else:
			return False

	def get_albums_by_user_id(self, userID):
		query = self.db.user_data.user_id == userID
		result = self.db(query).select(self.db.user_data.account_key).first()
		if result:
			albums = self.get_albums_by_account_id(result.account_key, 1, 'self')

			return albums
		else:
			return False

	def get_albums_by_account_id(self, accountID, viewLevel=1, requestorID='self'):
		albums = []
		query = (self.db.account_albums.account_key == accountID) & (self.db.account_albums.view_level >= viewLevel)
		results = self.db(query).select(self.db.account_albums.id)
		if results:
			for result in results:
				albums.append(self.get(result, viewLevel, requestorID))

			return albums

		return False

	def get_albums_by_album_key(self, albumKey):
		query = self.db.account_albums.album_id == albumKey
		result = self.db(query).select(self.db.account_albums.id).first()
		if result:
			return self.get(result)

		return False


	def create_album(self, accountID, name, viewLevel, notes):
		import uuid
		identifier = str(uuid.uuid1())
		from datetime import datetime
		if self.db.account_albums.insert(
			account_key=accountID,
			album_id=identifier,
			view_level=viewLevel,
			name=name,
			description=notes):
			return True
		else:
			return False

	def remove_album_by_id(self, albumID, accountID=''):
		if not accountID:
			query = self.db.account_albums.id == albumID
			album = self.db(query).select().first()
			if album:
				accountID = album.account_key

		if accountID:
			query1 = self.db.upload_media.album_key == albumID
			results = self.db(query1).select()
			if results:
				for result in results:
					self.db.deleted_media.insert(
						account_id=accountID,
						album_id=albumID,
						media_id=result.id,
						media_type=result.media_type,
						up_file=result.up_file)

			self.db(query).delete()
			return True
		else:
			return False

	def remove_album_by_key(self, albumKey):
		query = self.db.account_albums.album_id == albumKey
		album = self.db(query).select().first()
		if album:
			accountID = album.account_key
			albumID = album.id

		if accountID:
			query1 = self.db.upload_media.album_key == albumID
			results = self.db(query1).select()
			if results:
				for result in results:
					self.db.deleted_media.insert(
						account_id=accountID,
						album_id=albumID,
						media_id=result.id,
						media_type=result.media_type,
						up_file=result.up_file)

			self.db(query).delete()
			return True
		else:
			return False

	def update_album(self, albumID, name, viewLevel, notes, updateFlag=''):
		if albumID:
			query = self.db.account_albums.id == albumID
			if self.db(query).update(name=name, view_level=viewLevel, description=notes):
				if updateFlag:
					query1 = self.db.upload_media.album_key == albumID
					results = self.db(query1).select()
					if results:
						for result in results:
							query2 = self.db.upload_media.id == result.id
							self.db(query2).update(view_level=viewLevel)

				return self.get(albumID)

	def get_photo_count_by_account_key(self,accountKey, viewLevel=5):
		mediaCount = 0
		query = self.db.account.account_id == accountKey
		result = self.db(query).select(self.db.account.id).first()
		if result:
			mediaCount = self.get_photo_count_by_account_id(result.id, viewLevel)
		
		return mediaCount

	def get_photo_count_by_user_id(self, userID):
		mediaCount = 0
		query = self.db.user_data.user_id == userID
		account = self.db(query).select(self.db.user_data.account_key).first()
		if account:
			mediaCount = self.get_photo_count_by_account_id(account.account_key)
		
		return mediaCount

	def get_photo_count_by_account_id(self, accountID, viewLevel=1):
		mediaCount = 0
		if accountID:
			query = (self.db.account_albums.account_key == accountID) & (self.db.account_albums.view_level >= viewLevel)
			results = self.db(query).select(self.db.account_albums.id)
			if results:
				for result in results:
					query = (self.db.upload_media.album_key == result.id) & (self.db.upload_media.view_level >= viewLevel) 
					mediaCount = mediaCount + self.db(query).count()
		
		return mediaCount

class Media:
	def __init__(self, db, mediaID=''):
		self.db = db
		self.mediaID = mediaID

	def like_media(self, mediaID, userID, delete=False):
		reply = False
		if userID:
			query = self.db.user_data.user_id == userID
			result = self.db(query).select().first()
			if result:
				accountID = result.account_key
				if not delete:
					if self.db.media_likes.insert(account_key=accountID, media_key=mediaID):
						reply = True
				if delete:
					queryD = (self.db.media_likes.media_key == mediaID) & (self.db.media_likes.account_key == accountID)
					if self.db(queryD).delete():
						reply = True

		return reply

	def remove_media_by_id(self, mediaID, albumID, accountID=''):
		if not accountID:
			query = self.db.account_albums.id == albumID
			album = self.db(query).select().first()
			if album:
				accountID = album.account_key

		if accountID:
			query1 = self.db.upload_media.id == mediaID
			result = self.db(query1).select().first()
			if result:
				self.db.deleted_media.insert(
					account_id=accountID,
					album_id=albumID,
					media_id=mediaID,
					media_type=result.media_type,
					up_file=result.up_file)

			self.db(query1).delete()
			return True
		else:
			return False

	def update_media(self, mediaID, fileName, viewLevel, notes):
		if mediaID:
			query = self.db.upload_media.id == mediaID
			self.db(query).update(file_name=fileName, view_level=viewLevel, notes=notes)

			return True

	def reset_media_view_level_to_album(self, albumID, newViewLevel):
		if albumID:
			query = self.db.upload_media.album_key == albumID
			results = self.db(query).select()
			if results:
				for result in results:
					query1 = self.db.upload_media.id == result.id
					self.db(query1).update(view_level=newViewLevel)

			return True

"""
this if for image security...maybe needless
	def can_i_view_media(self, userID, theRequest):
		query = self.db.user_data.user_id == userID
		result = self.db(query).select(self.db.user_data.account_key).first()
		if result:
			accountID = result.account_key
			queryI = self.db.upload_media.up_file == theRequest
			queryT = self.db.upload_media.thumbnail == theRequest
			queryB = self.db.upload_media.banner == theRequest
			resultI = self.db(query).select().first()
			resultT = self.db(query).select().first()
			resultB = self.db(query).select().first()
"""


def thumbnail_generator(file_name, box, fit=True, name="thumb"):
	'''Downsample the image.
	@param img: Image - an Image-object
	@param box: tuple(x, y) - the bounding box of the result image
	@param fit: boolean - crop the image to fill the box
	'''
	if file_name:
		request = current.request
		image_dir = __find_image_dir__(file_name, os.path.join(request.folder, 'uploads'))
		img = Image.open(os.path.join(image_dir, file_name))# Convert to RGB if necessary
		if img.mode not in ('L', 'RGB'):
			img = img.convert('RGB')
		if fit:
			img = ImageOps.fit(img, box, Image.ANTIALIAS)
		else:
			img.thumbnail(box, Image.ANTIALIAS)
		root, ext = os.path.splitext(file_name)
		# I use PNG since there is no lost of quality with it way of compression
		thumb = '%s_%s%s' % (root, name, '.png')
		img.save(os.path.join(image_dir, thumb), 'PNG')
	return thumb

def banner_generator(file_name, box, fit=True, name="banner"):
	'''Downsample the image.
	@param img: Image - an Image-object
	@param box: tuple(x, y) - the bounding box of the result image
	@param fit: boolean - crop the image to fill the box
	'''
	if file_name:
		request = current.request
		image_dir = __find_image_dir__(file_name, os.path.join(request.folder, 'uploads'))
		img = Image.open(os.path.join(image_dir, file_name))# Convert to RGB if necessary
		if img.mode not in ('L', 'RGB'):
			img = img.convert('RGB')
		if fit:
			img = ImageOps.fit(img, box, Image.ANTIALIAS)
		else:
			img.thumbnail(box, Image.ANTIALIAS)
		root, ext = os.path.splitext(file_name)
		# I use PNG since there is no lost of quality with it way of compression
		banner = '%s_%s%s' % (root, name, '.png')
		img.save(os.path.join(image_dir, banner), 'PNG')
	return banner

def __find_image_dir__(name, path):
	for root, dirs, files in os.walk(path):
		if name in files:
			return root