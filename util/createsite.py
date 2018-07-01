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
#   E-mail: rsdavis@linuxden.com
#

import os
import sys
import string
import py_compile
import pmt_utils
import shutil

# list of directories to add
directories = ['html', 'cgi-bin', 'icons', 'documents','images','viewcvs','cvs_exports']


#-------------------------------------------------------------------------------
def create_home_dir(site_name):

	# Create directory /home/new_site/.
	# Then create the subdirectories listed in global var 'directories'
	# Set ownership to nobody

	if os.path.exists('/home/%s' % site_name):
		print "Updating %s..." % site_name
	else:
		print "Creating %s..." % site_name
		os.mkdir('/home/%s' % site_name)

	for i in xrange(0,len(directories)):
		if not os.path.exists('/home/%s/%s' % (site_name,directories[i])):
			os.mkdir('/home/%s/%s' % (site_name,directories[i]))

	os.system('chown nobody.nobody /home/%s/*' % site_name)

#-------------------------------------------------------------------------------



#-------------------------------------------------------------------------------
def copy_pyc_files(site_name):

	# Copy all files listed in pmt_site.files to a temp directory.
	# Then compile the .py into .pyc files
	# Delete the .py files and copy what's left to cgi-bin
	# Set ownership and permissions

	print "	Copying source files"

	os.system('mkdir pmt_temp')

	fileptr=open('pmt_site.files','r')

	fileList=fileptr.readlines()
	for file in fileList:
		file=string.strip(file)
		shutil.copy('../src/%s' % file,'pmt_temp')
		py_compile.compile('pmt_temp/%s' % file)
		
	fileptr.close()

#	os.system('python compileall.py pmt_temp')
	os.system('rm -f pmt_temp/*.py')
	os.system('cp pmt_temp/* /home/%s/cgi-bin' % site_name)

	# Set owner to nobody and permissions to [rwxr--r--]
	os.system('chown nobody.nobody /home/%s/cgi-bin/*' % site_name)
	os.system('chmod 744 /home/%s/cgi-bin/*' % site_name)

	# Remove the temp directory
	os.system('rm -rf pmt_temp')
#-------------------------------------------------------------------------------



#-------------------------------------------------------------------------------
def copy_html_files(site_name, project_name):

	# Copy the default 'front page' to the /www/var/html directory
	# Copy the html files from the install directory to /home/new_site/html
	# Copy the images from install to /home/new_site/icons
	# Customize the html files with site_name and project_name
	# Set ownership and permission

	print "	Copying html and image files"

	shutil.copy('../install/pmt_site.html','/var/www/html/%s.html' % site_name)
	os.system('cp ../install/*.html /home/%s/html' % site_name)
	os.system('cp ../install/*.gif ../install/*.jpg /home/%s/icons' % site_name)

	# replace 'pmt_site' with site_name and "pmt_project" with project_name
	p_name=string.replace(project_name, ' ', '\ ')
	filelist=os.listdir('/home/%s/html' % site_name)
	for file in filelist:
		os.system('vi -c %s/pmt_site/%s/g -c wq /home/%s/html/%s' % ('%s',site_name,site_name,file))
		os.system('vi -c %s/pmt_project/%s/g -c wq /home/%s/html/%s' % ('%s',p_name,site_name,file))

	os.system('vi -c %s/pmt_site/%s/g -c wq /var/www/html/%s.html' % ('%s',site_name,site_name))
	os.system('vi -c %s/pmt_project/%s/g -c wq /var/www/html/%s.html' % ('%s',p_name,site_name))

	os.system('chown nobody.nobody /home/%s/html/*' % site_name)
	os.system('chown nobody.nobody /var/www/html/%s.html' % site_name)
	os.system('chown nobody.nobody /home/%s/icons/*' % site_name)

	os.system('chmod 644 /home/%s/html/*' % site_name)
	os.system('chmod 644 /home/%s/icons/*' % site_name)
	os.system('chmod 644 /var/www/html/%s.html' % site_name)


#-------------------------------------------------------------------------------



#-------------------------------------------------------------------------------
def create_declarations_file(site_name, domain, db_user, db_pass):

	# Copy from pmt_site.template into a new file declarations.py using custom data
	# Compile the .py file and copy the .pyc file to /home/new_site/cgi_bin
	# Set ownership and permissions


	print "Creating %s declarations file" % site_name

	shutil.copy('pmt_site.template','%s.template' % site_name)
	os.system('mkdir pmt_temp')
	template=open('pmt_site.template','r')
	declarations=open('pmt_temp/declarations.py','w')

	content=template.readlines()
	for line in content:
		words=string.split(line)
		if len(words)<3:
			declarations.write(line)
			continue

		if words[2]=="'{{{DB_NAME}}}'":
			declarations.write(words[0]+' '+words[1]+" '"+site_name + "'\n")
		elif words[2] == "'{{{DOMAIN_NAME}}}'":
			declarations.write(words[0]+' '+words[1]+" '"+domain + "'\n")
		elif words[2] == "'{{{BROWSER_USERNAME}}}'":
			declarations.write(words[0]+' '+words[1]+" '"+db_user + "'\n")
		elif words[2] == "'{{{BROWSER_PASSWORD}}}'":
			declarations.write(words[0]+' '+words[1]+" '"+db_pass + "'\n")
		elif words[2] == "'{{{HELP_URL}}}'":
			declarations.write(words[0]+' '+words[1]+" 'help.html'\n")
		else:
			declarations.write(line)

	template.close()
	declarations.close()

	py_compile.compile('pmt_temp/declarations.py')
	shutil.copy('pmt_temp/declarations.pyc', '/home/%s/cgi-bin' % site_name)
	shutil.copy('pmt_temp/declarations.pyc', '.')
	shutil.copy('pmt_temp/declarations.py', '.')

	os.system('chown nobody.nobody /home/%s/cgi-bin/*' % site_name)
	os.system('chmod 744 /home/%s/cgi-bin/*' % site_name)

	# Remove the temp directory
	os.system('rm -rf pmt_temp')


#-------------------------------------------------------------------------------


#-------------------------------------------------------------------------------
def create_database(site_name, pg_password):

	# Import the new declarations file
	# Create the database
	# Create the db user and set password
	# Connect to the database as the new user and create the tables
	# Set permissions
	# Customize and run pmt_site.tables file

	print "Creating %s database" % site_name

	import declarations

	db_name =declarations.pmt_info['db_name']
	username=declarations.pmt_info['browser_username']
	password=declarations.pmt_info['browser_password']


	os.system('createdb -U postgres -q %s >> log.txt 2>> log.txt' % db_name)
	os.system('createuser -U postgres -q -D -A %s >> log.txt 2>> log.txt' % username)

	db=pmt_utils.connectDB('postgres', pg_password, db_name)
	sqlStatement="ALTER USER %s WITH PASSWORD '%s'" % (username,password)
	pmt_utils.executeSQL(db['result'],sqlStatement)

	db=pmt_utils.connectDB(username, password, db_name)
	if db['status']!='success':
		print dbResult['message']
		sys.exit(1)

	db=db['result']

	dbCreate = pmt_utils.create_tables(db, declarations.define_tables(), 0)
	if dbCreate['status']!='success':
		print 'Could not create DB'
		sys.exit()

	# Create sequences
	seqList=['project','pai','task','spr','ecp','project_members']
	for seq in seqList:
		 sqlStatement="CREATE SEQUENCE %s_id_seq START 1" % seq
		 pmt_utils.executeSQL(db,sqlStatement)

	# Grant privileges specified in declarations
	privs=declarations.table_privileges()
	for table_name in privs.keys():
		sqlStatement="GRANT "
		for user in privs[table_name].keys():
			for privilege in privs[table_name][user]:
				sqlStatement=sqlStatement+privilege+', '

			sqlStatement=sqlStatement[:-2] + ' ON ' + table_name + ' TO ' + user
			#print sqlStatement
			pmt_utils.executeSQL(db,sqlStatement)
			
	# Customize file, run it, then change it back
	os.system('vi -c %s/pmt_usr/%s/g -c wq pmt_site.tables' % ('%s',username))
	os.system("psql %s %s -f 'pmt_site.tables' >> log.txt" % (db_name,username))
	#pmt_utils.exec_sql_file(db,'pmt_site.tables')
	os.system('vi -c %s/%s/pmt_usr/g -c wq pmt_site.tables' % ('%s',username))

	return db

#-------------------------------------------------------------------------------


#-------------------------------------------------------------------------------
def create_admin(db, site_name, admin_user, admin_pass):
	
	# Insert a new user into the project_members table
	# Insert the new user into the privileges table and grant them user_admin privs
	# Update the project_member_id_seq

	print "Creating %s admin..." % site_name

	sqlStatement="INSERT INTO project_members (id, member_username, member_password) VALUES ('1','%s','%s')" % (admin_user, admin_pass)
	result=pmt_utils.executeSQL(db, sqlStatement)

	sqlStatement="INSERT INTO priviledges (member_username, user_admin) VALUES ('%s','%s')" % (admin_user, 't')
	result=pmt_utils.executeSQL(db, sqlStatement)

	queryResult = pmt_utils.executeSQL(db, "SELECT NEXTVAL('project_members_id_seq')")

#-------------------------------------------------------------------------------




#-------------------------------------------------------------------------------
def populate_db(db):
	
	# Make temp files for each table and copy the data into the database
	
	import declarations

	print 'Populating database...'

	try:
		datfile=open('pmt_site.dat','r')
	except:
		print "Couldn't find .dat file with project data"
		return
	
	data=datfile.readlines()
	datfile.close()
	datfile=open('temp.dat','w')
	for line in data:
		datfile.write(string.replace(line,'{PWD}',os.environ.get("PWD")))
	datfile.close()

	db_name =declarations.pmt_info['db_name']
	username=declarations.pmt_info['browser_username']

	os.system('psql %s %s -f %s' % (db_name,'postgres','temp.dat'))

	#Add permissions for usr

	#sql="grant all on ecp_id_seq to %s" % username
	#pmt_utils.executeSQL(db,sql)
	#sql="grant all on pai_id_seq to %s" % username
	#pmt_utils.executeSQL(db,sql)
	#sql="grant all on project_members_id_seq to %s" % username
	#pmt_utils.executeSQL(db,sql)
	#sql="grant all on project_id_seq to %s" % username
	#pmt_utils.executeSQL(db,sql)
	#sql="grant all on spr_id_seq to %s" % username
	#pmt_utils.executeSQL(db,sql)
	#sql="grant all on task_id_seq to %s" % username
	#pmt_utils.executeSQL(db,sql)

	#for line in data:
	#	words=string.split(line)
	#	if len(words)==0:
	#		continue
	#	if words[0]=='#':
	#		if words[1]=='END':
	#			tempfile.close()
	#			psqlcommand="\COPY %s from 'temp.dat' USING DELIMITERS ','" % table_name
	#			os.system('''psql %s %s -c "%s" >> log.txt 2>> log.txt''' % (db_name,username,psqlcommand))
	#		else:
	#			table_name=words[1]
	#			tempfile=open('temp.dat','w')
	#	else:
	#		tempfile.write(line)

	#datfile.close()
	#tempfile.close()
	os.system('rm -rf temp.dat')
#-------------------------------------------------------------------------------



#-------------------------------------------------------------------------------
def setup_htaccess(site_name, admin_user, admin_pass):

	# Create the .htaccess file in the html and cgi-bin directories
	# Create the passwd file, add the admin user and set ownership on it

	htaccess=open('/home/%s//.htaccess' % site_name,'w')

	htaccess.write('AuthType Basic\n')
	htaccess.write('AuthName "%s Project Access"\n' % string.upper(site_name))
	htaccess.write('AuthUserFile /var/www/admin/%s.passwd\n' % site_name)
	htaccess.write('require valid-user\n')

	htaccess.close()

	#os.system('cp /home/%s/cgi-bin/.htaccess /home/%s/html' % (site_name,site_name))

	if not os.path.exists('/var/www/admin'):
		os.mkdir('/var/www/admin')
	os.system('/usr/bin/htpasswd -c -b /var/www/admin/%s.passwd %s %s' % (site_name, admin_user, admin_pass))
	
	os.system('chown nobody.nobody /var/www/admin/%s.passwd' % site_name)

#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
def setup_counter(site_name):

	# Create the Counter data file and set ownership and permissions

	count=open('/usr/local/etc/Counter/data/%s.dat' % site_name,'w')
	count.write('0\n')
	count.close()

	os.system('chown nobody.nobody /usr/local/etc/Counter/data/%s.dat' % site_name)
	os.system('chmod 666 /usr/local/etc/Counter/data/%s.dat' % site_name)

#-------------------------------------------------------------------------------



#-------------------------------------------------------------------------------
def add_alias(site_name):

	# Get an admin email address
	# Add [site_name]_uploads alias to /etc/aliases
	# Run newaliases

	print "Enter the email address for the webmaster of this site:"
	email=sys.stdin.readline()
	email=string.lower(string.strip(email[:-1]))

	uploadsFound=0
	docMaintFound=0
	if os.path.exists('/etc/aliases'):
		alias_file=open('/etc/aliases','r')
		lines=alias_file.readlines()
		for line in lines:
			words=string.split(line)
			if words==[]:
				continue
			if words[0]=='%s_uploads:' % site_name:
				uploadsFound=1

			if words[0]=='%s_document_maintenance' % site_name:
				docMaintFound=1

			if uploadsFound and docMaintFound:
				print '\tSite already in alias file.'
				alias_file.close()
				return
				
		alias_file.close()

		alias_file=open('/etc/aliases','a')
		if not uploadsFound:
			line='\n%s_uploads: %s\n' % (site_name,email)
			alias_file.write(line)
		if not docMaintFound:
			line='%s_document_maintenance: %s\n'%(site_name,email)
			alias_file.write(line)
		alias_file.close()

		os.system('/usr/bin/newaliases >> log.txt 2>> log.txt')
	else:
		print "Cannot find alias file."



#-------------------------------------------------------------------------------


#-------------------------------------------------------------------------------
def add_backup(site_name):

	# Add line to dump_db.py so this site will be backed up every night
	
	print "Adding site to nightly backup."

	if not os.path.exists('/usr/local/pmt'):
		os.mkdir('/usr/local/pmt')

	if not os.path.exists('/usr/local/pmt/dump_db.py'):
		shutil.copy('dump_db.py','/usr/local/pmt')
		
	backup=open('/usr/local/pmt/dump_db.py','r')
	lines=backup.readlines()
	found='false'
	for line in lines:
		words=string.split(line)
		if words==[]:
			continue
		if words[0]=="dump_db('%s')" % site_name:
			found='true'
	backup.close()

	if found=='true':
		print "\tSite is already in dump_db.py"
	else:
		backup=open('/usr/local/pmt/dump_db.py','a')
		backup.write("\n\tdump_db('%s')\n" % site_name)
		backup.close()
		os.system('touch /usr/local/pmt/%s.db.dump.gz' % site_name)
		os.system('chown postgres.postgres /usr/local/pmt/%s.db.dump.gz' % site_name)

#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
def setup_webcvs(site_name,project_name):
	
	# Make temporary [site_name].modules file
	if not os.path.exists('/home/cvsroot/%s/' % site_name):
		os.makedirs('/home/cvsroot/%s/' % site_name)
		os.system('chown nobody.nobody /home/cvsroot/%s' % site_name)
		os.mkdir('/home/cvsroot/%s/%s/' % (site_name,site_name))
		os.system('chown nobody.nobody /home/cvsroot/%s/%s' % (site_name,site_name))
		os.mkdir('/home/cvsroot/%s/CVSROOT' % (site_name))
		os.system('chown nobody.nobody /home/cvsroot/%s/CVSROOT' % (site_name))
		modules=open('/home/cvsroot/%s/CVSROOT/%s.modules' % (site_name,site_name),'w')
		modules.write('%s %s\n' % (site_name,site_name))
		modules.close()
		os.system('chown nobody.nobody /home/cvsroot/%s/CVSROOT/%s.modules' % (site_name,site_name))
		print "A temporary .modules file has been created."
	print "!! YOU MUST MANUALLY CREATE THE %s.modules FILE ON GAMEPC !!" % site_name

	# Add line to mirror.py so this project can be copied
	shutil.copy('/usr/local/mirror/mirror.py /usr/local/mirror/mirror.py.bak')
	print "Backup of mirror.py created: /usr/local/mirror/mirror.py.bak"
	old=open('/usr/local/mirror/mirror.py.bak','r')
	new=open('/usr/local/mirror/mirror.py','w')
	lines=old.readlines()

	inserted='false'
	for line in lines:
		if line[:28]=='# END MIRROR_PROJECT LINES #' and inserted=='false':
			new.write("try:\n\tmirror_project('%s','%s')\n" % (site_name,site_name))
			new.write("except:\n\tpass\n")
		if string.strip(line)=="mirror_project('%s','%s')" % (site_name,site_name):
			print "\tThis site is already in mirror.py"
			inserted='already'
		new.write(line)
	new.close()
	old.close()		

	# Make viewcvs conf file
	old=open('/usr/local/viewcvs-0.9.2/viewcvs.conf.pmt_site','r')
	new=open('/usr/local/viewcvs-0.9.2/viewcvs.conf.%s' % site_name,'w')
	lines=old.readlines()
	for line in lines:
		if string.strip(line)=='# PMT DEVELOPMENT LINE':
			new.write('\tDevelopment : /home/cvsroot/%s/%s\n' % (site_name,site_name))
		if string.strip(line)=='# PMT MAIN TITLE LINE':
			new.write('main_title = %s CVS Repository\n' % project_name)
		new.write(line)
	old.close()
	new.close()
	os.system('chown nobody.nobody /usr/local/viewcvs-0.9.2/viewcvs.conf.%s' % site_name)
	
	# Copy cgi files to viewcvs directory
	if os.path.exists('/home/%s/viewcvs/' % site_name):
		shutil.copy('query.cgi.bak /home/%s/viewcvs/' % site_name)
		oldcvs=open('../src/viewcvs.cgi','r')
		newcvs=open('/home/%s/viewcvs/viewcvs.cgi' % site_name,'w')
		lines=oldcvs.readlines()
		for line in lines:
			words=string.split(line)
			if words==[]:
				continue
			if words[0]=='CONF_PATHNAME':
				line='CONF_PATHNAME = "/usr/local/viewcvs-0.9.2/viewcvs.conf.%s"\n' % site_name
			newcvs.write(line)

		oldcvs.close()
		newcvs.close()
		os.system('chown nobody.nobody /home/%s/viewcvs/*' % site_name)
		os.system('chmod u+x /home/%s/viewcvs/*' % site_name)
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
def configure_httpd(site_name):
	
	# Make a backup and copy data from it to the new version
	# Insert the necessary lines for the new site

	print "Updating http.conf"

	os.system('mv /etc/httpd/conf/httpd.conf /etc/httpd/conf/httpd.conf.backup')
	print "Backup of httpd.conf created: /etc/httpd/conf/httpd.conf.backup"
	oldconf=open("/etc/httpd/conf/httpd.conf.backup",'r')
	newconf=open("/etc/httpd/conf/httpd.conf", 'w')

	oldlines=oldconf.readlines()

	# TBD This code only works if # END DIRECTORY SECTION is in the file
	# which is not the case for an initial install
	# Insert <Directory> blocks
	inserted='false'
	for line in oldlines:
		if line[:25]=="# END DIRECTORY SECTION #" and inserted=='false':
			inserted='true'
			newconf.write('\n<Directory /home/%s>\n' % site_name)
			config_string='  Options None\n  AllowOverride All\n  order allow,deny\n  allow from all\n</Directory>\n'
			newconf.write(config_string)

			for i in xrange(0,len(directories)):
				newconf.write('\n<Directory /home/%s/%s>\n' % (site_name,directories[i]))
				newconf.write(config_string)

		if string.strip(line)=="<Directory /home/%s>" % site_name:
			print "	The site is already in httpd.conf"
			inserted='already'

		newconf.write(line)

	# Insert aliases
	if inserted=='true':
		newconf.write('\nScriptAlias /%s-cgi-bin/ "/home/%s/cgi-bin/"' % (site_name,site_name))
		newconf.write('\nScriptAlias /%s-cvs-web/ "/home/%s/viewcvs/"' % (site_name,site_name))
		newconf.write('\nAlias /%s/ "/home/%s/"' % (site_name, site_name))
		newconf.write('\nAlias /%s-cvs-exports/ "/home/%s/cvs_exports/"\n' % (site_name,site_name))
	
	oldconf.close()
	newconf.close()


#-------------------------------------------------------------------------------





#-------------------------------------------------------------------------------
def restart_httpd():
	
	# Do it twice to be sure

	print "Restarting httpd service..."
	os.system('/etc/rc.d/init.d/httpd restart')
	os.system('/etc/rc.d/init.d/httpd restart')
#-------------------------------------------------------------------------------



#-------------------------------------------------------------------------------
if __name__ == "__main__":
	print "Enter the name of the new project [ex. Intelligent Flight Control System] : "
	project_name=sys.stdin.readline()
	project_name=string.strip(project_name[:-1])

	print "Enter a name for the new site [ex. ifcs] : "
	site_name=sys.stdin.readline()
	site_name=string.lower(string.strip(site_name[:-1]))

	# Create the home directory and copy the pyc and html files to the appropriate directory
	create_home_dir(site_name)
	copy_pyc_files(site_name)
	copy_html_files(site_name,project_name)

	print "Enter the domain name of the site [ex. www.isrparc.org] : "
	domain=sys.stdin.readline()
	domain=string.lower(string.strip(domain[:-1]))

	print "Enter a username for the database: "
	db_user=sys.stdin.readline()
	db_user=string.lower(string.strip(db_user[:-1]))

	print "Enter a password for the database: "
	db_pass=sys.stdin.readline()
	db_pass=string.strip(db_pass[:-1])

	print "Enter password for user postgres: "
	pg_password=sys.stdin.readline()
	pg_password=string.strip(pg_password[:-1])

	# Create the declarations file and create the database and tables based on that
	create_declarations_file(site_name, domain, db_user, db_pass)
	db=create_database(site_name, pg_password)

	print "Enter a username for site admin: "
	admin_user=sys.stdin.readline()
	admin_user=string.lower(string.strip(admin_user[:-1]))

	print "Enter a password for site admin: "
	admin_pass=sys.stdin.readline()
	admin_pass=string.strip(admin_pass[:-1])

	# Add the first user to the system and give them user_admin privileges
	create_admin(db, site_name, admin_user, admin_pass)

	# Add project info and option menu data to the database
	populate_db(db)

	# Add .htaccess functionality
	setup_htaccess(site_name,admin_user,admin_pass)

	# Add a .dat file for the counter
	setup_counter(site_name)
	
	# Add a new alias
	add_alias(site_name)

	# Add the site to the backup program
	add_backup(site_name)

	# TBD removed 01-29-2006 since we can not mirror with only one machine
	#setup_webcvs(site_name,project_name)

	# Add httpd aliases and access to the home directory and then restart the httpd service
	configure_httpd(site_name)
	restart_httpd()

	print "Installation Complete.  See log.txt for more information"
#-------------------------------------------------------------------------------
