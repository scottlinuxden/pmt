#!/usr/bin/env python
# $Id: user_administration.py,v 1.1 2003/12/30 17:21:42 lliabraa Exp $
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
#   Voice:  304.534.3031
#

import declarations
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

class user_administration:

    def __init__(self,
                 ignore_user_login=0,
                 prompt=1,
                 db_name=None,
                 postgres_username=None,
                 postgres_password=None):
        
        self.db_name = db_name
        self.postgres_username = postgres_username
        self.postgres_password = postgres_password
        self.prompt = prompt
        
        os.putenv("PGLIB", "/usr/lib/pgsql")
        
        os.putenv("PGDATA", "/var/lib/pgsql")

        if not ignore_user_login:

            if getpass.getuser() != 'postgres':
                print 'You must be logged in as user postgres to'
                print 'create a db. Exiting application.'
                return 'error'

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

        if prompt and postgres_username == None:
                
            while 1:
                print "Enter the postgres username: ",
                self.postgres_username = sys.stdin.readline()
                self.postgres_username = string.strip(self.postgres_username[:-1])
                if string.strip(self.postgres_username) != "":
                    break
                else:
                    print "You must enter a postgres username"
                        
        else:
            if postgres_username != None:
                self.postgres_username = string.strip(postgres_username)

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

    def delete_user(self,
                    username):

        self.username = username
        
        if self.prompt and username == None:
            while 1:
                
                print "Enter the new username: ",
                self.username = sys.stdin.readline()
                self.username = string.strip(self.username[:-1])
                if string.strip(self.username) != "":
                    break
                else:
                    print "You must enter a username"
                    
        else:
            if username != None:
                self.username = string.strip(username)
                os.system("/usr/bin/destroyuser " + self.username)

        if self.username == None and self.password == None:
            return 'error'

        else:
            return 'success'
        
    def add_user(self,
                 username,
                 password):

        self.username = username
        self.password = password
        
        if self.prompt and username == None:
            while 1:
                
                print "Enter the new username: ",
                self.username = sys.stdin.readline()
                self.username = string.strip(self.username[:-1])
                if string.strip(self.username) != "":
                    break
                else:
                    print "You must enter a username"
                    
        else:
            if username != None:
                self.username = string.strip(username)
				
        if self.prompt and self.password == None:
            while 1:
                
                self.password = getpass.getpass(prompt='Enter the password for the new user: ')
                
                if string.strip(self.password) != "":
                    break
                else:
                    print "You must enter a password"
                    
        else:
            if password != None:
                self.password = password

        if self.password == None and self.username == None:
            return 'error'

        dbResult = pmt_utils.connectDB(self.postgres_username, self.postgres_password, self.db_name)

        if dbResult['status'] != "success":
            print dbResult['message']
            return 'error'

        self.db = dbResult['result']

        queryResult = pmt_utils.executeSQL(self.db, "SELECT count(*) FROM pg_user WHERE usename = '%s'" % (self.username))

        result = queryResult['result']
        
        rows_which_match = result[0]["count"]

        if rows_which_match != 0:
            print 'User already exists'
            return 'Error'
            
        if queryResult["status"] != 'success':
            print queryResult["status"]
            return 'error'

        queryResult = pmt_utils.executeSQL(self.db, "SELECT MAX(usesysid) FROM pg_user")

        if queryResult["status"] != 'success':
            print queryResult["status"]
            return 'error'

        result = queryResult['result']

        user_id = result[0]['max']
        
        user_id = user_id + 1
        
        self.db.close()
                
        print "Answer NO to the next prompt"
        
        os.system("/usr/bin/createuser -i %d -D -U %s" % (user_id,self.username))
                        
        dbResult = pmt_utils.connectDB(self.postgres_username, self.postgres_password, self.db_name)
        
        if dbResult['status'] != "success":
            print dbResult['message']
            return 'error'

        self.db = dbResult['result']
        
        queryResult = pmt_utils.executeSQL(self.db, "ALTER USER %s WITH PASSWORD %s" % (self.username, self.password))

        if queryResult["status"] != 'success':
            print queryResult['message']
            return 'error'

        grantList = []

        privileges = declarations.table_privileges()
        
        for table_name in privileges.keys():

            for user_name in privileges[table_name].keys():

                grantStatement = "GRANT "
                for privilege in privileges[table_name][user_name]:
                    grantStatement = grantStatement + privilege + ", "
                    
                grantStatement = grantStatement[:-2] + " ON " + table_name + " TO " + self.username
                grantList.append(grantStatement)

        grantList.append("GRANT ALL ON pai_id_seq TO %s" % (self.username))
        grantList.append("GRANT ALL ON project_members_id_seq TO %s" % (self.username))
                
        queryResult = pmt_utils.executeSqlItemList(self.db, grantList, 1)

        if queryResult["status"] != 'success':
            print "Failed to execute all GRANTS"
            return 'error'

        self.db.close()
        
        return 'success'

if __name__ == "__main__":
    
    user_admin = user_administration(prompt=0,
                                     db_name='pmt',
                                     postgres_username='postgres',
                                     postgres_password='post1dba')
    user_admin.add_user(username='davis',password='ian2son')
    
