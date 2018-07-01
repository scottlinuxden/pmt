# $Id$
#
# COPYRIGHT:
#   Copyright (C) 1999 LinuXden, All Rights Reserved
#   Copright Statement at http://www.linuxden.com/copyrighted_apps.html
#
# AUTHOR: 
#   R. Scott Davis
#
# CONTACT:
#   R. Scott Davis
#   E-mail: scott.davis@linuxden.com
#

import string
import os
import crypt
import pmt_utils
import sha

#----------------------------------------------------------------------------
def username_exists(db, username):

	sql="SELECT count(*) FROM project_members "
	sql=sql+"WHERE member_username = '%s'" % (username)
	dbResult = pmt_utils.executeSQL(db, sql)

	if dbResult['status'] != 'success':
		return ('error', 'Username not found')

	else:
		result = dbResult['result']
		if result[0]['count'] > 0:
			return ('success', 'Username found')
		else:
			return ('error', 'Username not found')
#----------------------------------------------------------------------------

			
#----------------------------------------------------------------------------
def encrypt_password(crypt_salt, password):

	return crypt.crypt(password, crypt_salt[:2])
#----------------------------------------------------------------------------

		
#----------------------------------------------------------------------------
def password_valid(db, crypt_salt, username, password):

	status, details = username_exists(db, username)

	if status == 'success':

		sql="SELECT member_password FROM project_members "
		sql=sql+"WHERE member_username = '%s'" % (username)
		dbResult = pmt_utils.executeSQL(db, sql)

		if dbResult['status'] != 'success':
			return ('error', 'Username/password not valid')
		else:
			result = dbResult['result']
			hash=sha.new(result[0]['member_password']).digest()

			if  hash == password:
				return ('success', 'Username/password valid')
			else:
				return ('error', 'Invalid password')

	else:
		return ('error', 'Username not found')
#----------------------------------------------------------------------------


#----------------------------------------------------------------------------
def update_username_password(db, username, password, crypt_salt):

	sql="UPDATE project_members SET member_password = '%s' " % (password)
	sql=sql+"WHERE member_username = '%s'" % (username)
	dbResult = pmt_utils.executeSQL(db, sql)

	if dbResult['status'] != 'success':
		return ('error', 'Username not found')
	else:
		return ('success', 'Password updated')
#----------------------------------------------------------------------------
