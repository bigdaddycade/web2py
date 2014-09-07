#!/usr/bin/env python
# coding: utf8
from gluon import *
import gluon.contrib.simplejson as simplejson
import datetime

class Message:
	def __init__(self, db):
		self.db = db

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

	def get(self, messageID='', accountID='', details=True):
		display = False
		if not messageID:
			messageID = self.messageID

		if messageID:
			query = self.db.message_table.id == messageID
			result = self.db(query).select().first()
			if result:
				if accountID == result.sender_id:
					if result.s_deleted:
						timeDelta = datetime.datetime.now() - result.s_deleted
						if timeDelta.days < 10:
							display = 'sender'
					else:
						display = 'sender'
				elif accountID == result.receiver_id:
					if result.r_deleted:
						timeDelta = datetime.datetime.now() - result.r_deleted
						if timeDelta.days < 10:
							display = 'receiver'
					else:
						display = 'receiver'

				if display:
					from AccountUser import Account
					accountObj = Account(self.db)
					message = {} ### MAYBE []
					message['key'] = result.message_id
					message['subject'] = result.m_subject
					message['hasRead'] = result.m_read
					message['whenSent'] = result.created
					message['deleted'] = False

					if display == 'sender':
						message['sender'] = 'self'
						message['receiver'] = accountObj.get_basic_data_by_account_id(result.receiver_id, True)
						if result.s_deleted:
							message['deleted'] = result.s_deleted
					elif display == 'receiver':
						message['receiver'] = 'self'
						message['sender'] = accountObj.get_basic_data_by_account_id(result.sender_id, True)
						if result.r_deleted:
							message['deleted'] = result.r_deleted
					else:
						message['sender'] = False
						message['receiver'] = False

					if details:
						message['mText'] = result.m_body

						if result.media_link:
							media=[]
							jsonData = simplejson.loads(result.media_link)
							for image in jsonData:
								media.append(image)
							message['attached'] = media
						else:
							message['attached'] = False

					display = message

		return display

	def get_message_list_by_account_id(self, accountID, hideDeleted=''):
		messages = {} ### MAYBE []
		messages['sent'] = []
		messages['received'] = []
		if not hideDeleted:
			messages['deleted'] = []
		queryS = self.db.message_table.sender_id == accountID
		queryR = self.db.message_table.receiver_id == accountID
		resultsS = self.db(queryS).select(self.db.message_table.id)
		resultsR = self.db(queryR).select(self.db.message_table.id)
		if resultsS:
			for result in resultsS:
				message = self.get(result.id, accountID, False)
				if message:
					if message['deleted']:
						if not hideDeleted:
							messages['deleted'].append(message)
					else:
						messages['sent'].append(message)

		if resultsR:
			for result in resultsR:
				message = self.get(result.id, accountID, False)
				if message:
					if message['deleted']:
						if not hideDeleted:
							messages['deleted'].append(message)
					else:
						messages['received'].append(message)
		if not hideDeleted:
			if (len(messages['sent']) > 0) or (len(messages['received']) > 0) or (len(messages['deleted']) > 0):
				return messages
			else:
				return False
		if hideDeleted:
			if (len(messages['sent']) > 0) or (len(messages['received']) > 0):
				return messages
			else:
				return False

	def get_message_list_for_account_by_account_id(self, requestorID, accountID):
		messages = []
		queryS = (self.db.message_table.sender_id == requestorID) & (self.db.message_table.receiver_id == accountID)
		queryR = (self.db.message_table.receiver_id == requestorID) & (self.db.message_table.sender_id == accountID)
		resultsS = self.db(queryS).select(self.db.message_table.id)
		resultsR = self.db(queryR).select(self.db.message_table.id)
		if resultsS:
			for result in resultsS:
				message = self.get(result.id, requestorID, False)
				if message:
					if not message['deleted']:
						messages.append(message)

		if resultsR:
			for result in resultsR:
				message = self.get(result.id, requestorID, False)
				if message:
					if not message['deleted']:
						messages.append(message)
		if len(messages) > 0:
			return messages
		else:
			return False

	def get_message_list_for_folder_by_account_id(self, requestorID, folder):
		messages = []
		if (folder == 'sent') or (folder == 'delete'):
			queryS = self.db.message_table.sender_id == requestorID
			resultsS = self.db(queryS).select(self.db.message_table.id)
			if resultsS:
				for result in resultsS:
					message = self.get(result.id, requestorID, False)
					if message:
						if folder == 'delete':
							if message['deleted']:
								messages.append(message)
						elif folder == 'sent':
							if not message['deleted']:
								messages.append(message)

		if (folder == 'inbox') or (folder == 'delete'):
			queryR = self.db.message_table.receiver_id == requestorID
			resultsR = self.db(queryR).select(self.db.message_table.id)
			if resultsR:
				for result in resultsR:
					message = self.get(result.id, requestorID, False)
					if message:
						if folder == 'delete':
							if message['deleted']:
								messages.append(message)
						elif folder == 'inbox':
							if not message['deleted']:
								messages.append(message)

		if len(messages) > 0:
			return messages
		else:
			return False

	def send_new_message(self, requestorID, accountID, mSubject, mBody):
		didItWork = False
		if requestorID:
			import uuid
			identifier = str(uuid.uuid1())
			if self.db.message_table.insert(
						message_id=identifier,
						sender_id=requestorID,
						receiver_id=accountID,
						m_subject=mSubject,
						m_body=mBody):
				didItWork=True

		return didItWork

	def get_message_by_message_key(self, messageKey, requestorID):
		message = False
		query = self.db.message_table.message_id == messageKey
		result = self.db(query).select().first()
		if result:
			message = self.get(result.id, requestorID)
			if message:
				if message['receiver'] == 'self':
					self.db(query).update(m_read=True)

		return message

	def delete_message_by_message_key(self, messageKey, requestorID):
		success = False
		query = self.db.message_table.message_id == messageKey
		result = self.db(query).select().first()
		if result:
			if result.sender_id == requestorID:
				success = self.db(query).update(s_deleted=datetime.datetime.now())
			if result.receiver_id == requestorID:
				success = self.db(query).update(r_deleted=datetime.datetime.now())

		return success

	def restore_message_by_message_key(self, messageKey, requestorID):
		success = False
		query = self.db.message_table.message_id == messageKey
		result = self.db(query).select().first()
		if result:
			if result.sender_id == requestorID:
				success = self.db(query).update(s_deleted=None)
			if result.receiver_id == requestorID:
				success = self.db(query).update(r_deleted=None)

		return success

	def get_new_messages_by_auth_id(self, userID):
		messages = []
		query = self.db.user_data.user_id == userID
		result = self.db(query).select().first()
		if result:
			accountID = result.account_key
			queryR = (self.db.message_table.receiver_id == accountID) & (self.db.message_table.m_read == False)
			resultsR = self.db(queryR).select(self.db.message_table.id, limitby=(0, 5))
			if resultsR:
				for result in resultsR:
					message = self.get(result.id, accountID, False)
					if message:
						messages.append(message)

		if len(messages) > 0:
			return messages
		else:
			return False

	def get_unread_message_count_by_auth_id(self, userID):
		count = 0
		query = self.db.user_data.user_id == userID
		result = self.db(query).select().first()
		if result:
			queryR = (self.db.message_table.receiver_id == result.account_key) & (self.db.message_table.m_read == False)
			count = self.db(queryR).count()

		return count

