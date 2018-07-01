import os,string
import pmt_utils
import declarations

def dbInit():
    dbResult=pmt_utils.connectDB(declarations.pmt_info['browser_username'],
                                 declarations.pmt_info['browser_password'],
                                 declarations.pmt_info['db_name'])
    if dbResult['status']!='success':
        print "Error while connecting to database<BR>"
        return "error",None

    return 'success',dbResult['result']

def getAllUsers():
    # Connect to the database
    status,db=dbInit()
    if status!='success':
        print "Unable to get users from database"
        return 'error',None

    # Get all users in the project
    sql="select member_username from project_members;"
    result=pmt_utils.executeSQL(db,sql)
    if result['status']!='success':
        print "Unable to execute query for user list"
        return 'error',None

    # Build the list of usernames
    userList=[]
    for user in result['result']:
        userList.append(user['member_username'])

    return 'success',userList


def refuseAll():
    # Create an empty permissions file
    #file,ext=os.path.splitext(form['filename'].value)
    #permFilename="%s.perm" % file
    permFilename="%s.perm" % form['filename'].value
    permFile=open(permFilename,'r')
    owner=permFile.readline()
    if string.find(owner,':')>=0:
        owner=string.split(owner,':')[1]
        owner=string.strip(owner)
    else:
        owner="None"
    permFile.close()
    permFile=open(permFilename,'w')
    permFile.write("Owner:%s\n" % owner)
    permFile.close()

def allowAll():
    # Remove the permission file
    #file,ext=os.path.splitext(form['filename'].value)
    #permFilename="%s.perm" % file
    permFilename="%s.perm" % form['filename'].value
    permFile=os.remove(permFilename)

def updatePermissions():
    # Build the refuse and allow lists from the form data
    toRefuseList=[]
    toAllowList=[]
    if form.has_key('toRefuse'):
        toRefuseList=pmt_utils.formOptionListToList(form,'toRefuse')
    if form.has_key('toAllow'):
        toAllowList=pmt_utils.formOptionListToList(form,'toAllow')

    #file,ext=os.path.splitext(form['filename'].value)
    #permFilename="%s.perm" % file
    permFilename="%s.perm" % form['filename'].value


    # If add users to list of allowed users...
    if form.has_key('addAllowed'):
        # ... append list to names already in permissions file
        permFile=open(permFilename,'a')
        for user in toAllowList:
            if user=="(None)":
                refuseAll()
                return
            permFile.write("%s\n" % user)
        permFile.close()

    # Else if refuse users access to file...
    elif form.has_key('refuseAllowed'):

        if '(None)' in toRefuseList:
            allowAll()
            return
        
        # ... if the permissions file exists...
        if os.path.exists(permFilename):
            # ...get the names of the allowed users
            permFile=open(permFilename,'r')
            owner=permFile.readline()
            allowedUsers=permFile.readlines()
            permFile.close()
            if string.find(owner,':')>=0:
                owner=string.split(owner,':')[1]
                owner=string.strip(owner)
            else:
                allowedUsers.append(owner)
                owner="None"
            # Strip off the newline
            for i in xrange(0,len(allowedUsers)):
                allowedUsers[i]=allowedUsers[i][:-1]
        else:
            # ... otherwise, all users are allowed access
            status,allowedUsers=getAllUsers()
            owner="None"
            if status!='success':
                print "Unable to get user list from database"
                return 'error'

        # For each allowed user...
        permFile=open(permFilename,'w')
        permFile.write("Owner: %s\n" % owner)
        for user in allowedUsers:
            # ...if the user is not to be refused...
            if user not in toRefuseList:
                # ...write their username to the file
                permFile.write("%s\n" % user)
        permFile.close()
    else:
        print "No command"
        return 'error'

    return 'success'

def getPermissionLists():
    filename=form['filename'].value
    status,db=dbInit()
    if status!='success':
        print "Initialization Error"
        return "error",None,None
    
    if not os.path.exists(filename):
        print "Specified file could not be found: %s" % filename
        return "error",None,None

    # Open the permission file and read the list of allowed users
    #file,ext=os.path.splitext(filename)
    relative_filename=os.path.split(filename)[1]
    if os.path.exists("%s.perm" % filename):
        print "<H2>Loading permissions for %s</H2>" % relative_filename
        new_permissions=0
    else:
        print "<H2>Creating permissions for %s</H2>" % relative_filename
        new_permissions=1

    # If this is the first time permissions have been set ...
    if new_permissions:
        # ... the allowedUsers list is empty
        owner="None"
        allowedUsers=[]
    else:
        # ... otherwise, read the list of allowed users from the file
        permFile=open("%s.perm" % filename,'r')
        owner=permFile.readline()
        allowedUsers=permFile.readlines()
        permFile.close()
        if string.find(owner,':')>=0:
            owner=string.split(owner,":")[1]
            owner=string.strip(owner)
        else:
            allowedUsers.append(owner)
            owner="None"
        # Strip off the newline
        for i in xrange(0,len(allowedUsers)):
            allowedUsers[i]=allowedUsers[i][:-1]
    

    print "<CENTER>Owner: %s</CENTER><BR>" % owner

    # Build list of refused users
    sql="select member_username from project_members;"
    result=pmt_utils.executeSQL(db,sql)
    if result['status']!='success':
        print "Error fetching user list"
        return "error",None,None

    # Add any users that are not in the permissions file to refusedUsers
    refusedUsers=[]
    for user in result['result']:
        if user['member_username'] not in allowedUsers:
            refusedUsers.append(user['member_username'])

    refusedUsers.sort()
    allowedUsers.sort()

    # if there is no permissions file, all users are allowed access
    if new_permissions:
        # but allowedUsers is empty and refusedUsers contains all users
        #  so return them swapped
        return "success", refusedUsers, allowedUsers
    else:
        return "success", allowedUsers, refusedUsers
    

def displayPermissions():
    
    # Get the list of allowed and refused users from the permissions file
    status,allowedUsers,refusedUsers=getPermissionLists()
    if status!='success':
        print "Error processing permissions file"
        return
    
    # Create a form with...
    print '<FORM ACTION="permission.pyc" METHOD="POST"  WIDTH="10">'

    # ... the current filename ...
    print '<INPUT NAME="filename" TYPE=hidden '
    print 'VALUE="%s">' % form['filename'].value
    print '<TABLE><TR>'

    # ... the list of users who have access ...
    print '<TD><SELECT NAME="toRefuse" SIZE="6" MULTIPLE>'
    if len(allowedUsers)==0:
        print '<OPTION>(None)'
    else:
        for user in allowedUsers:
            print '<OPTION>%s' % (user)
    print "</SELECT><BR>Allowed Users</TD>"

    # .. the command buttons (to add or refuse access) ...
    print '<TD><INPUT NAME="refuseAllowed" TYPE=submit VALUE="-->">'
    print '<BR><INPUT NAME="addAllowed"    TYPE=submit VALUE="<--"></TD>'

    # ... the list of users who are refused access
    print '<TD><FORM ACTION="permission.pyc" METHOD="POST" WIDHT="10">'
    print '<SELECT NAME="toAllow" SIZE="6" MULTIPLE>'
    if len(refusedUsers)==0:
        print '<OPTION>(None)'
    else:
        for user in refusedUsers:
            print '<OPTION>%s' % (user)
    print "</SELECT><BR>Refused Users</TD>"

    print '</TR></TABLE></FORM>'
    
        
    
# Initialize html output
pmt_utils.htmlContentType()
print "<HTML>"
print "<HEAD>"
pmt_utils.title("Permissions")

# Add javascript for the close window button
print '<SCRIPT TYPE="text/javascript">'
print '<!--'

print 'function closerefresh()'
print '{'
print '    if (! (window.focus && window.opener))'
print '        return true;'
print '    window.opener.focus();'
print '    window.close();'
print '    if (opener.top.location != opener.location) {'
print '        opener.location.reload();}'
print '    return false;'
print '}'

print 'function closewin()'
print '{'
print '    if (! (window.focus && window.opener))'
print '        return true;'
print '    window.opener.focus();'
print '    window.close();'
print '    return false;'
print '}'

print '//-->'
print '</SCRIPT>'
print "</HEAD>"
pmt_utils.bodySetup()
form=pmt_utils.getFormData()
db_name=declarations.pmt_info['db_name']

# If a filename has been specified...
if form.has_key('filename'):
    #print form['filename'].value
    # ...if the add or refuse buttons were pressed ...
    if form.has_key('addAllowed') or form.has_key('refuseAllowed'):
        # ...update the permissions
        updatePermissions()

    # Display the users who have permissions and those who do not
    print "<CENTER>"
    displayPermissions()
else:
    # ... otherwise no filename is specified so output an error
    print "No file specified"

# Display the close window button
print '<form method="POST" >'
print '<input type="button" value="Close Window" '
print 'onClick="return closewin()">'
print '</form>'
print "</CENTER>"

print "</BODY></HTML>"
