#!/usr/bin/env python
import authentication, sys, getpass, os

# password_file names
# upload_passwd - documentation upload password filename

def adduser(project_name, username, password, password_file):
    if not os.path.exists(os.path.join('/home', project_name, 'admin')):
        os.mkdir(os.path.join('/home', project_name, 'admin'))

    (status, message) = authentication.add_pwd_entry('/home/%s/admin/%s' % (project_name,password_file),project_name,username,password)

    print 'The status of the add is %s' % (status)
    print 'The details of the add is %s' % (message)
    
if __name__ == "__main__":
    print 'Enter the project name for user: ',
    project_name = sys.stdin.readline()[:-1]
    sys.stdin.flush()

    print 'Enter the password file for user: ',
    password_file = sys.stdin.readline()[:-1]

    print 'Enter the username of user to add: ',
    username = sys.stdin.readline()[:-1]

    password = getpass.getpass(prompt='Enter the password for the user: ')

    adduser(project_name,username,password,password_file)
