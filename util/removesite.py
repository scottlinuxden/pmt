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

import os
import sys
import string
import py_compile
import pmt_utils


print "Enter the name of the site to remove [ex. ifcs] : "
site_name=sys.stdin.readline()
site_name=string.lower(string.strip(site_name[:-1]))


# remove home directory
if os.path.exists('/home/%s' % site_name):
	os.system('rm -rf /home/%s' % site_name)

# remove database
os.system('dropdb %s -U postgres' % site_name)

# remove database users
# requires declarations file
print "You must manually remove this site's database user(s)"


# remove intro page at /var/www/html/[pmt_site].html
if os.path.exists('/var/www/html/%s.html' % site_name):
	os.system('rm -rf /var/www/html/%s.html' % site_name)

# remove template file from pmt in cvs
if os.path.exists('%s.template' % site_name):
	os.system('rm -rf %s.template' % site_name)

# remove passwd file from /var/www/admin/
if os.path.exists('/var/www/admin/%s.passwd' % site_name):
	os.system('rm -rf /var/www/admin/%s.passwd' % site_name)

# remove Counter dat file in /usr/local/etc/Counter/data/
if os.path.exists('/usr/local/etc/Counter/data/%s.dat' % site_name):
	os.system('rm -rf /usr/local/etc/Counter/data/%s.dat' % site_name)

# remove any aliases from /etc/aliases
# save aliases so people can still send emails

# remove site from the backup script
if os.path.exists('/usr/local/pmt/dump_db.py'):
	os.system('cp /usr/local/pmt/dump_db.py /usr/local/pmt/dump_db.py.bak')
	old=open('/usr/local/pmt/dump_db.py.bak','r')
	new=open('/usr/local/pmt/dump_db.py','w')

	# copy all lines except the one pertaining to the site to remove
	lines=old.readlines()
	for line in lines:
		if not string.strip(line)=="dump_db('%s')" % site_name:
			new.write(line)

	new.close()
	old.close()


# remove from /home/cvsroot/
if os.path.exists('/home/cvsroot/%s' % site_name):
	os.system('rm -rf /home/cvsroot/%s' % site_name)

# remove from /usr/local/mirror/mirror.py
if os.path.exists('/usr/local/mirror/mirror.py'):
	os.system('cp /usr/local/mirror/mirror.py /usr/local/mirror/mirror.py.bak')
	old=open('/usr/local/mirror/mirror.py.bak','r')
	new=open('/usr/local/mirror/mirror.py','w')

	# copy all lines except the one pertaining to the site to remove
	lines=old.readlines()
	for line in lines:
		if not string.strip(line)=="mirror_project('%s','%s')" % (site_name,site_name):
			new.write(line)

	new.close()
	old.close()

# remove viewcvs conf file from /usr/local/viewcvs-0.9.2/
if os.path.exists('/usr/local/viewcvs-0.9.2/viewcvs.conf.%s' % site_name):
	os.system('rm -rf /usr/local/viewcvs-0.9.2/viewcvs.conf.%s' % site_name)

# remove from httpd (then restart httpd)
# quite complicated - save this for another day
print "You must manually remove the site directories and aliases from httpd.conf"


