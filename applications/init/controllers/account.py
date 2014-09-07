# -*- coding: utf-8 -*-

apiVersion = '0.9'


@auth.requires_login()
def index():

	view = request.vars.view or None

	account={}
	user={}
	title = 'Account Settings'

	from AccountUser import Account
	accountObj = Account(db)
	accountID = accountObj.get_account_id_by_user_id(session.auth.user.id)
	if not accountID:
		accountID = accountObj.create_account_and_add_user_data_and_profile(session.auth.user.id)
		if accountID:
			redirect(URL('account', 'index'))

	if not view:

		if accountID:
			account=accountObj.get(accountID)
			users=accountObj.get_user_by_account(accountID)

		return dict(
			view=view,
			account=account,
			users=users,
			title=title)

	if view == 'default':

		query = db.account(db.account.id==accountID)
		form = SQLFORM(db.account, query, submit_button = 'Update Account', deletable=False, showid=False, fields=[
			'default_friend',
			'default_blog',
			'default_album'
		])

		if form.process().accepted:
			redirect(URL('account', 'index'))
		elif form.errors:
			response.flash = 'The form contains errors.'

		return dict(
			view=view,
			title=title,
			form=form)

	if view == 'location':

		query = db.account(db.account.id==accountID)
		form = SQLFORM(db.account, query, submit_button = 'Update Account', deletable=False, showid=False, fields=[
			'phone',
			'address',
			'city',
			'state_id',
			'zip_code',
			'country_id'
		])

		if form.process().accepted:
			redirect(URL('account', 'index'))
		elif form.errors:
			response.flash = 'The form contains errors.'

		return dict(
			view=view,
			title=title,
			form=form)

	if view == 'personal':

		query = db.account(db.account.id==accountID)
		form = SQLFORM(db.account, query, submit_button = 'Update Account', deletable=False, showid=False, fields=[
			'gender',
			'email',
			'show_me_filter'
		])

		if form.process().accepted:
			redirect(URL('account', 'index'))
		elif form.errors:
			response.flash = 'The form contains errors.'

		return dict(
			view=view,
			title=title,
			form=form)

	if view == 'moderator':

		return dict(
			view=view,
			title=title)