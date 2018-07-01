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

import os
import string
import commands
import sys

db_list=['save',
	 'c17',
	 'spyball',
	 'ivvnn',
	 'biometrics',
	 'usafsr',
	 'isr',
	 'buav',
	 'cuav',
	 'contact']

web_list=['save',
	  'c17',
	  'spyball',
	  'ivvnn',
	  'biometrics',
	  'usafsr',
	  'isr',
	  'buav',
	  'cuav']

def dump_db(db_name):

	status, output = commands.getstatusoutput('pg_dump %s -U postgres | gzip >  /home/lliabraa/backup/%s.db.dump.gz' % (db_name, db_name))
	#print db_name,status,output

def tar_web(web_name):

	os.system('tar zcf /home/lliabraa/backup/%s.web.gz --exclude documents --exclude cvs_exports -C /home/%s/ .' % (web_name,web_name))



if __name__ == "__main__":

	# Generate all the tar files
	for name in db_list:
		dump_db(name)

	for name in web_list:
		tar_web(name)

	#get the /var/www/ files too
	os.system('tar zcf /home/lliabraa/backup/home.web.gz --exclude manual -C /var/www/ .')

	# Tar all the archive files together
	os.system('tar cf /home/lliabraa/backup/pmt.backup -C /home/lliabraa/backup/ .')
