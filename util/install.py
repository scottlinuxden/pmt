#!/usr/bin/env python
# $Id$
#
# COPYRIGHT:
#   Copyright (C) 1999 LinuXden, All Rights Reserved
#   Copright Statement at http://www.linuxden.com/copyrighted_apps.html
#
# AUTHOR: 
#   Scott Davis
#
# CONTACT:
#   R. Scott Davis
#   E-mail: scott.davis@linuxden.com
#

import stat
import glob
import string
import compileall
import os_utils
import shutil
import os, string, sys
import cgi
import types
import commands
import getpass
import file_io
import pmt_utils
from pg import DB

class install:
	
	def __init__(self,
		     ignore_user_login=0,
		     prompt=1,
		     db_name=None,
		     domain_name=None,
		     postgres_username=None,
		     postgres_password=None,
		     db_admin_username=None,
		     db_admin_password=None,
		     visitor_username=None,
		     visitor_password=None,
		     help_url=None):
		
		self.db_name = db_name
		self.domain_name = domain_name
		self.postgres_username = postgres_username
		self.postgres_password = postgres_password
		self.db_admin_username = db_admin_username
		self.db_admin_password = db_admin_password
		self.visitor_username = visitor_username
		self.visitor_password = visitor_password
		self.help_url = help_url

		os.putenv("PGLIB", "/usr/lib/pgsql")

		os.putenv("PGDATA", "/var/lib/pgsql")

		if not ignore_user_login:

			if getpass.getuser() != 'postgres':
				print 'You must be logged in as user postgres to'
				print 'create a db. Exiting application.'
				sys.exit(1)

		if prompt and db_name == None:

			while 1:
				print 'Enter the database name to manipulate: ',
				self.db_name = sys.stdin.readline()
				self.db_name = string.lower(string.strip(self.db_name[:-1]))
				if string.strip(self.db_name) != "":
					break
				else:
					print "You must enter a database name to manipulate"
					
		else:
			if db_name != None:
				self.db_name = string.lower(string.strip(db_name))

		if prompt and domain_name == None:

			while 1:
				print 'Enter the domain name [EX. www.softwareresearch.org]: ',
				self.domain_name = sys.stdin.readline()
				self.domain_name = string.lower(string.strip(self.domain_name[:-1]))
				if string.strip(self.domain_name) != "":
					break
				else:
					print "You must enter a domain name"
					
		else:
			if domain_name != None:
				self.domain_name = string.lower(string.strip(domain_name))

		if prompt and postgres_username == None:

			while 1:
				print "Enter the postgres username: ",
				self.postgres_username = sys.stdin.readline()
				self.postgres_username = string.lower(string.strip(self.postgres_username[:-1]))
				if string.strip(self.postgres_username) != "":
					break
				else:
					print "You must enter a postgres username"

		else:
			if postgres_username != None:
				self.postgres_username = string.lower(string.strip(postgres_username))

		if prompt and postgres_password == None:

			while 1:
				self.postgres_password = getpass.getpass(prompt='Enter the password for the postgres user: ')
				
				if string.strip(self.postgres_password) != "":
					os.putenv("PGPASSWORD", self.postgres_password)
					break
				else:
					print "You must enter a password"

		else:
			if postgres_password != None:
				self.postgres_password = postgres_password

		if prompt and db_admin_username == None:
			while 1:
				
				print "Enter the db admin username: ",
				self.db_admin_username = sys.stdin.readline()
				self.db_admin_username = string.lower(string.strip(self.db_admin_username[:-1]))
				if string.strip(self.db_admin_username) != "":
					break
				else:
					print "You must enter a username"

		else:
			if db_admin_username != None:
				self.db_admin_username = string.lower(string.strip(db_admin_username))
				
		if prompt and db_admin_password == None:
			
			while 1:
				self.db_admin_password = getpass.getpass(prompt='Enter the password for the db admin: ')
				
				if string.strip(self.db_admin_password) != "":
					break
				else:
					print "You must enter a password"
					
		else:
			if db_admin_password != None:
				self.db_admin_password = db_admin_password
				
		if prompt and visitor_username == None:
			while 1:
				
				print "Enter the site visitor username: ",
				self.visitor_username = sys.stdin.readline()
				self.visitor_username = string.lower(string.strip(self.visitor_username[:-1]))
				if string.strip(self.visitor_username) != "":
					break
				else:
					print "You must enter a username"
					
		else:
			if visitor_username != None:
				self.visitor_username = string.lower(string.strip(visitor_username))
				
		if prompt and visitor_password == None:
			while 1:
				
				self.visitor_password = getpass.getpass(prompt='Enter the password for the site visitor: ')
				
				if string.strip(self.visitor_password) != "":
					break
				else:
					print "You must enter a password"
					
		else:
			if visitor_password != None:
				self.visitor_password = visitor_password
				
		if prompt and help_url == None:
			while 1:
				
				print "Enter the URL for pmt help documentation: ",
				self.help_url = sys.stdin.readline()
				self.help_url = string.lower(string.strip(self.help_url[:-1]))
				if string.strip(self.help_url) != "":
					break
				else:
					print "You must enter a URL for pmt help documentation"
					
		else:
			if help_url != None:
				self.help_url = string.lower(string.strip(help_url))

	def create_declarations(self):

		status, declaration_template_lines = file_io.readFromFile('%s.template' % (self.db_name))
		
		line_index = 0
		
		for line in declaration_template_lines:
			
			field = string.split(line)

			if len(field) < 3:
				line_index = line_index + 1
				continue

			if field[0][:8] == "pmt_info":

				if field[1] == '=':

					if field[2] == "'{{{DB_NAME}}}'":

						declaration_template_lines[line_index] = field[0] + ' ' + field[1] + " '" + self.db_name + "'"

					elif field[2] == "'{{{DOMAIN_NAME}}}'":
						declaration_template_lines[line_index] = field[0] + ' ' + field[1] + " '" + self.domain_name + "'"
						
					elif field[2] == "'{{{BROWSER_USERNAME}}}'":
						declaration_template_lines[line_index] = field[0] + ' ' + field[1] + " '" + self.visitor_username + "'"
						
					elif field[2] == "'{{{BROWSER_PASSWORD}}}'":
						declaration_template_lines[line_index] = field[0] + ' ' + field[1] + " '" + self.visitor_password + "'"
						
					elif field[2] == "'{{{HELP_URL}}}'":
						declaration_template_lines[line_index] = field[0] + ' ' + field[1] + " '" + self.help_url + "'"
						
			line_index = line_index + 1

		status, output = file_io.writeToFile('declarations.py', declaration_template_lines)
		
	def create_db(self):

		import declarations

		dbResult = pmt_utils.connectDB(self.postgres_username, self.postgres_password, self.db_name)
		
		# could not connect to db
		if dbResult['status'] != 'success':

			# database does not exist so we do not have to backup
			# table data from previous version of this database
			print 'Could not connect to %s database, no db backup to perform.' % (self.db_name),

		else:
			# else there is a database that exists with this name
			db = dbResult['result']

			# backup all tables to dat files
			#pmt_utils.exec_sql_file(db, '%s_tables.backup' % (self.db_name))

			db.close()

			# destroy the previous version of this database
			os.system('dropdb %s' % (self.db_name))

		# connect to template database to get maximum user
		# id in use at this time
		dbResult = pmt_utils.connectDB(self.postgres_username, self.postgres_password, 'template1')

		if dbResult['status'] != "success":
			print dbResult['message']
			sys.exit(1)

		db = dbResult['result']

		queryResult = pmt_utils.executeSQL(db, "SELECT MAX(usesysid) FROM pg_user")

		if queryResult["status"] != 'success':
			print queryResult["status"]
			sys.exit(1)

		result = queryResult['result']

		user_id = result[0]['max']
		
		user_id = user_id + 1
		
		db.close()
		
		# create database
		os.system("createdb %s" % (self.db_name))
		
		os.system("/usr/bin/destroyuser " + self.db_admin_username)

		# print "Answer NO to the next prompt"
		
		os.system("/usr/bin/createuser -D -A %s" % (self.db_admin_username))

		user_id = user_id + 1
		
		os.system("/usr/bin/destroyuser " + self.visitor_username)
		
		# print "Answer NO to the next prompt"
		
		os.system("/usr/bin/createuser -D -A %s" % (self.visitor_username))
		
		dbResult = pmt_utils.connectDB(self.postgres_username, self.postgres_password, self.db_name)
				
		if dbResult['status'] != "success":
			print dbResult['message']
			sys.exit(1)

		db = dbResult['result']


		# queryResult = pmt_utils.executeSQL(db, "DELETE FROM pg_group WHERE groname = 'admins'")
		
		# queryResult = pmt_utils.executeSQL(db, "INSERT INTO pg_group (groname, grosysid, grolist) VALUES ('admins', '1', '{1000}')")
		
		#if queryResult["status"] != 'success':
		#	print queryResult["status"]
		#	sys.exit(1)
	
		# queryResult = pmt_utils.executeSQL(db, "DELETE FROM pg_group WHERE groname = 'users'")
	
		# queryResult = pmt_utils.executeSQL(db, "INSERT INTO pg_group (groname, grosysid, grolist) VALUES ('users', '2', '{2000}')")
		
		# if queryResult["status"] != 'success':
		#	print queryResult["status"]
		#	sys.exit(1)

		queryResult = pmt_utils.executeSQL(db, "ALTER USER postgres WITH PASSWORD '%s'" % (self.postgres_password))

		if queryResult["status"] != 'success':
			print queryResult['message']
			sys.exit(1)

		queryResult = pmt_utils.executeSQL(db, "ALTER USER %s WITH PASSWORD '%s'" % (self.db_admin_username, self.db_admin_password))

		if queryResult["status"] != 'success':
			print queryResult['message']
			sys.exit(1)

		queryResult = pmt_utils.executeSQL(db, "ALTER USER %s WITH PASSWORD '%s'" % (self.visitor_username, self.visitor_password))

		if queryResult["status"] != 'success':
			print queryResult['message']
			sys.exit(1)

		queryResult = pmt_utils.create_tables(db, declarations.define_tables(), 1)

		if queryResult["status"] != 'success':
			print queryResult['message']
			sys.exit(1)

		pmt_utils.exec_sql_file(db, self.db_name + '.tables')
		
		grantList = []

		privileges = declarations.table_privileges()
		
		for table_name in privileges.keys():
			for user_name in privileges[table_name].keys():
				grantStatement = "GRANT "
				for privilege in privileges[table_name][user_name]:
					grantStatement = grantStatement + privilege + ", "
					
				grantStatement = grantStatement[:-2] + " ON " + table_name + " TO " + user_name
				grantList.append(grantStatement)
								
			# grant all privileges to the db admin
			grantList.append("GRANT ALL ON " + table_name + " TO " + self.db_admin_username)

		queryResult = pmt_utils.executeSqlItemList(db, grantList, 1)

		if queryResult["status"] != 'success':
			print "Failed to execute all GRANTS"
			sys.exit(1)

	def pmt_utils_web(self):

		project_name = self.db_name
	    
		status, dist_list = file_io.readFromFile(os.path.expandvars(os.path.join('${PWD}', self.db_name + '.files')))
		
		if not os.path.exists(os.path.join('/home', project_name)):
			os.mkdir(os.path.join('/home', project_name))

		if not os.path.exists(os.path.join('/home', project_name, 'html')):
			os.mkdir(os.path.join('/home', project_name, 'html'))

		if not os.path.exists(os.path.join('/home', project_name, 'cgi-bin')):
			os.mkdir(os.path.join('/home', project_name, 'cgi-bin'))

		if not os.path.exists(os.path.join('/home', project_name, 'images')):
			os.mkdir(os.path.join('/home', project_name, 'images'))

		if not os.path.exists(os.path.join('/home', project_name, 'admin')):
			os.mkdir(os.path.join('/home', project_name, 'admin'))

		if os.path.exists(os.path.join('.', 'staging')):
			os_utils.super_remove(os.path.join('.', 'staging'))

		os.mkdir(os.path.join('.', 'staging'))

		for curfile in dist_list:
			shutil.copy(curfile,os.path.join('.','staging'))

		os.chdir(os.path.join('.','staging'))

		compileall.compile_dir('.',0,None,0)
		
		os.chdir(os.path.join('..'))
		
		for curfile in glob.glob(os.path.join('.','staging','*.pyc')):
			shutil.copy(curfile,os.path.join('/home',project_name,'cgi-bin'))

		shutil.copy(os.path.join('images','imageMissing.gif'),os.path.join('/home',project_name,'images'))

		os_utils.set_file_mode(filename = os.path.join('/home',project_name),
							   user = ['r','w','x'])

		os_utils.set_file_mode(filename = os.path.join('/home',project_name,'html'),
							   user = ['r','w','x'])
		
		for curfile in glob.glob(os.path.join('/home',project_name,'html','*')):
			os_utils.set_file_mode(filename = curfile,
								   user = ['r','w'])

		os_utils.set_file_mode(filename = os.path.join('/home',project_name,'cgi-bin'),
							   user = ['r','w','x'])

		for curfile in glob.glob(os.path.join('/home',project_name,'cgi-bin','*')):
			os_utils.set_file_mode(filename = curfile,
								   user = ['r','w','x'])

		os_utils.set_file_mode(filename = os.path.join('/home',project_name,'images'),
							   user = ['r','w','x'])

		for curfile in glob.glob(os.path.join('/home',project_name,'images','*')):
			os_utils.set_file_mode(filename = curfile,
								   user = ['r','w'])

		os_utils.set_file_mode(filename = os.path.join('/home',project_name,'admin'),
							   user = ['r','w','x'])
				
		for curfile in glob.glob(os.path.join('/home',project_name,'admin','*')):
			os_utils.set_file_mode(
				filename = curfile,
				user = ['r','w'])

		status, output = os_utils.super_chown(
			directory_name=os.path.join('/home',project_name),
			username='nobody',
			groupname='nobody')

		if status != 'success':
			print 'Ownership settings of directory tree %s failed.' % (os.path.join('/home',project_name))

	def su_exec_pmt_utils_web(self):
		os_utils.su_exec(command = 'python install_web.py %s' % (self.db_name))
				
if __name__ == "__main__":

	print 'Enter the database name to install: ',
	db_name = sys.stdin.readline()
	db_name = string.lower(string.strip(db_name[:-1]))

	if db_name == 'save':
		install_engine = install(prompt=0,
					 db_name='save',
					 domain_name='www.isrparc.org',
					 postgres_username='postgres',
					 postgres_password='post1dba',
					 db_admin_username='admsve',
					 db_admin_password='adm1sve',
					 visitor_username='usrsve',
					 visitor_password='usr1sve',
					 help_url='help.html')
		
	elif db_name == 'spyball':
		install_engine = install(prompt=0,
					 db_name='spyball',
					 domain_name='www.isrparc.org',
					 postgres_username='postgres',
					 postgres_password='post1dba',
					 db_admin_username='admspy',
					 db_admin_password='adm1spy',
					 visitor_username='usrspy',
					 visitor_password='usr1spy',
					 help_url='help.html')

	elif db_name == 'c17':
		install_engine = install(prompt=0,
					 db_name='c17',
					 domain_name='www.isrparc.org',
					 postgres_username='postgres',
					 postgres_password='post1dba',
					 db_admin_username='admc17',
					 db_admin_password='adm1c17',
					 visitor_username='usrc17',
					 visitor_password='usr1c17',
					 help_url='help.html')
		
	elif db_name == 'biometrics':
		install_engine = install(prompt=0,
					 db_name='biometrics',
					 domain_name='www.isrparc.org',
					 postgres_username='postgres',
					 postgres_password='post1dba',
					 db_admin_username='admbio',
					 db_admin_password='adm1bio',
					 visitor_username='usrbio',
					 visitor_password='usr1bio',
					 help_url='help.html')

	elif db_name == 'ivvnn':
		install_engine = install(prompt=0,
					 db_name='ivvnn',
					 domain_name='www.isrparc.org',
					 postgres_username='postgres',
					 postgres_password='post1dba',
					 db_admin_username='admivv',
					 db_admin_password='adm1ivv',
					 visitor_username='usrivv',
					 visitor_password='usr1ivv',
					 help_url='help.html')
		

	elif db_name == 'isr':
		install_engine = install(prompt=0,
					 db_name='isr',
					 domain_name='www.isrparc.org',
					 postgres_username='postgres',
					 postgres_password='post1dba',
					 db_admin_username='admisr',
					 db_admin_password='adm1isr',
					 visitor_username='usrisr',
					 visitor_password='usr1isr',
					 help_url='help.html')

	elif db_name == 'cave':
		install_engine = install(prompt=0,
					 db_name='cave',
					 domain_name='www.isrparc.org',
					 postgres_username='postgres',
					 postgres_password='post1dba',
					 db_admin_username='admcve',
					 db_admin_password='adm1cve',
					 visitor_username='usrcve',
					 visitor_password='usr1cve',
					 help_url='help.html')

	elif db_name == 'gisstr':
		install_engine = install(prompt=0,
					 db_name='gisstr',
					 domain_name='www.isrparc.org',
					 postgres_username='postgres',
					 postgres_password='post1dba',
					 db_admin_username='admgis',
					 db_admin_password='adm1gis',
					 visitor_username='usrgis',
					 visitor_password='usr1gis',
					 help_url='help.html')

	elif db_name == 'pmt':
		install_engine = install(prompt=0,
					 db_name='pmt',
					 domain_name='www.isrparc.org',
					 postgres_username='postgres',
					 postgres_password='post1dba',
					 db_admin_username='admpmt',
					 db_admin_password='adm1pmt',
					 visitor_username='usrpmt',
					 visitor_password='usr1pmt',
					 help_url='help.html')

	elif db_name == 'pmis':
		install_engine = install(prompt=0,
					 db_name='pmis',
					 domain_name='www.isrparc.org',
					 postgres_username='postgres',
					 postgres_password='post1dba',
					 db_admin_username='pmisadm',
					 db_admin_password='pmis1ad',
					 visitor_username='usrpms',
					 visitor_password='usr1pms',
					 help_url='help.html')

	elif db_name == 'usafsr':
		install_engine = install(prompt=0,
					 db_name='usafsr',
					 domain_name='www.isrparc.org',
					 postgres_username='postgres',
					 postgres_password='post1dba',
					 db_admin_username='admafs',
					 db_admin_password='adm1afs',
					 visitor_username='usrafs',
					 visitor_password='usr1afs',
					 help_url='help.html')

	elif db_name == 'buav':
		install_engine = install(prompt=0,
					 db_name='buav',
					 domain_name='www.isrparc.org',
					 postgres_username='postgres',
					 postgres_password='post1dba',
					 db_admin_username='admbuv',
					 db_admin_password='adm1buv',
					 visitor_username='usrbuv',
					 visitor_password='usr1buv',
					 help_url='help.html')
	else:
		install_engine = install(prompt=1)
	
	install_engine.create_declarations()
	install_engine.create_db()
	install_engine.su_exec_pmt_utils_web()
		
