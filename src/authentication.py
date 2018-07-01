# $Id: authentication.py,v 1.1 2004/03/18 21:51:12 lliabraa Exp $
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
import file_io
import crypt
		     
def username_in_passwd(passwd_filename, username):

	status, lines = file_io.readFromFile(passwd_filename)

	username_found = 0
	
	for line_index in xrange(0, len(lines)):
		
		line_field = string.splitfields(lines[line_index],':')
		
		if username == line_field[0]:
			username_found = 1
			break

	if username_found:
		return 1
	else:
		return 0

def add_pwd_entry(passwd_filename, crypt_salt, username, password):

	# salt can be at max 2 chars.
	crypt_salt = crypt_salt[:2]
	
	status, lines = file_io.readFromFile(passwd_filename)

	# if files does not exist
	if status == 'error':
		del lines
		lines = []

	if lines != []:
		if username_in_passwd(passwd_filename, username):
			return('error', 'username already in passwd file, can not add')

	# add new pw entry to lines 
	lines.append(username + ':' + crypt.crypt(password, crypt_salt))

	status, output = file_io.writeToFile(passwd_filename,lines)
	
	return (status, 'username added')

def delete_pwd_entry(passwd_filename, username):

	status, lines = file_io.readFromFile(passwd_filename)
	
	username_found = 0
	
	for line_index in xrange(0, len(lines)):
		
		line_field = string.splitfields(lines[line_index],':')
		
		if username == line_field[0]:
			del lines[line_index]
			username_found = 1
			break

	if username_found:
		status, output = file_io.writeToFile(passwd_filename,lines)
		return ('success','username deleted')
	else:
		return ('error','username not found')
		
def password_valid(passwd_filename, crypt_salt, username, password):

	# salt can be at max 2 chars.
	crypt_salt = crypt_salt[:2]
	
	status, lines = file_io.readFromFile(passwd_filename)

	if status == 'error':
		return ('error', 0)

	for line_index in xrange(0, len(lines)):
		
		line_field = string.splitfields(lines[line_index],':')
		
		if (username == line_field[0]) and (crypt.crypt(password, crypt_salt) == line_field[1]):
			return ('success', 1)

	# username/password not found
	return ('success', 0)

def modify_password(passwd_filename,crypt_salt,username,password):

	# salt can be at max 2 chars.
	crypt_salt = crypt_salt[:2]
	
	status, lines = file_io.readFromFile(passwd_filename)
	
	if status == 'error':
		return ('error', 0)
	
	for line_index in xrange(0, len(lines)):
		
		line_field = string.splitfields(lines[line_index],':')
		
		if (username == line_field[0]):
			lines[line_index] = line_field[0] + ':' + crypt.crypt(password, crypt_salt)
			break
		
	status, output = file_io.writeToFile(passwd_filename,lines)
			
	# username/password not found
	return ('success', 0)

