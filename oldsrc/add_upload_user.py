#!/usr/bin/env python
# $Id: add_upload_user.py,v 1.1 2003/12/30 17:21:42 lliabraa Exp $
#
# COPYRIGHT:
#   Copyright (C) 1999 LinuXden, All Rights Reserved
#   Copright Statement at http://www.linuxden.com/copyrighted_apps.html
#
# AUTHOR: 
#   Lane LiaBraaten
#
# CONTACT:
#   R. Scott Davis
#   E-mail: rsdavis@linuxden.com
#   Voice:  304.534.3031
#
import authentication, sys, getpass, os

def adduser(project_name, username, password):
    if not os.path.exists(os.path.join('/home', project_name, 'admin')):
        os.mkdir(os.path.join('/home', project_name, 'admin'))
    (status, message) = authentication.add_pwd_entry('/home/%s/admin/upload_passwd' % (project_name),project_name,username,password)

    
if __name__ == "__main__":
    print 'Enter the project name to add user: ',
    project_name = sys.stdin.readline()[:-1]
    sys.stdin.flush()
    print 'Enter the username of person to add: ',
    username = sys.stdin.readline()[:-1]
    password = getpass.getpass(prompt='Enter the password for the user: ')
    adduser(project_name,username,password)
