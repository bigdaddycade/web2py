# -*- coding: utf-8 -*-
#
#
######### ALL UUID VALUES FOR ID IN PROFILE ARE ACCOUNTKEY

apiVersion = '0.9'

from Media import Album, Media
from AccountUser import Account
accountObj = Account(db)
albumObj = Album(db)
mediaObj = Media(db)

from Profile import Profile
profileObj = Profile(db)

from SharMail import Message
messageObj = Message(db)

import gluon.contrib.simplejson as simplejson

@auth.requires_login()
def index():
	accountKey = request.vars.account_key or None
	account=False
	messages=False

	accountID = accountObj.get_account_id_by_user_id(session.auth.user.id)
	if accountID:
		account=accountObj.get(accountID)
		messages=messageObj.get_message_list_by_account_id(accountID)

	return dict(message='boob')

####################################################
####################################################
################### Message API ####################
####################################################
####################################################

@auth.requires_login()
def get_folder():
	response.view = 'generic.'+request.extension
	folder = request.vars.folder or None
	messages=False

	accountID = accountObj.get_account_id_by_user_id(session.auth.user.id)
	if accountID:
		messages=messageObj.get_message_list_for_folder_by_account_id(accountID, folder)

	return api_response(messages=messages)

@auth.requires_login()
def get_key():
	response.view = 'generic.'+request.extension
	accountKey = request.vars.account_key or None
	messages=False

	requestorID = accountObj.get_account_id_by_user_id(session.auth.user.id)
	accountID = accountObj.get_account_id_by_account_key(accountKey)
	if accountID:
		messages=messageObj.get_message_list_for_account_by_account_id(requestorID, accountID)

	return api_response(messages=messages)

@auth.requires_login()
def send_message():
	response.view = 'generic.'+request.extension
	jsonData = simplejson.loads(request.body.read()) if request.body else {}
	requestorID = accountObj.get_account_id_by_user_id(session.auth.user.id)

	if jsonData:
		accountID = accountObj.get_account_id_by_account_key(jsonData['key'])
		mSubject = jsonData['subject']
		mbody = jsonData['body']

		if messageObj.send_new_message(requestorID, accountID, mSubject, mbody):
			return api_response(message='message sent')

@auth.requires_login()
def get_message():
	response.view = 'generic.'+request.extension
	messageKey = request.vars.message_key or None
	message=False

	requestorID = accountObj.get_account_id_by_user_id(session.auth.user.id)
	if requestorID:
		message=messageObj.get_message_by_message_key(messageKey, requestorID)

	return api_response(message=message)

@auth.requires_login()
def delete_message():
	response.view = 'generic.'+request.extension
	messageKey = request.vars.message_key or None
	undo = request.vars.undo or None
	success = False

	requestorID = accountObj.get_account_id_by_user_id(session.auth.user.id)
	if requestorID:
		if undo:
			if messageObj.restore_message_by_message_key(messageKey, requestorID):
				success = True
		else:
			if messageObj.delete_message_by_message_key(messageKey, requestorID):
				success = True

	return api_response(success=success)

@auth.requires_login()
def get_basic():
	response.view = 'generic.'+request.extension
	accountKey = request.vars.account_key or None
	basics = ''

	accountID = accountObj.get_account_id_by_account_key(accountKey)
	if accountID:
		basics=accountObj.get_basic_data_by_account_id(accountID, True)

	return api_response(basics=basics)

####################################################
####################################################
#################### GENERICS ######################
####################################################
####################################################


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

