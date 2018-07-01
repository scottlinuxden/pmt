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

import os, string, sys
import cgi, glob
from pg import DB
import urllib
import os_utils
import pmt_utils
import declarations
import time_pkg
import time
import stat
import file_io
import db_authentication




#------------------------------------------------------------------------------
def addGoogle():
    print '<!-- SiteSearch Google -->'
    print '<FORM method=GET action="http://www.google.com/search">'
    print '<TABLE bgcolor="#FFFFFF"><tr><td>'
    print '<A HREF="http://www.google.com/">'
    print '<IMG SRC="http://www.google.com/logos/Logo_40wht.gif" '
    print 'border="0" ALT="Google"></A>'
    print '</td>'
    print '<td>'
    print '<INPUT TYPE=text name=q size=31 maxlength=255 value="">'
    print '<INPUT type=submit name=btnG VALUE="Google Search">'
    print '<font size=-1>'
    print '<input type=hidden name=domains value="www.isrparc.org"><br>'
    print '<input type=radio name=sitesearch value=""> WWW'
    print '<input type=radio name=sitesearch value="www.isrparc.org" checked>'
    print 'www.isrparc.org <br>'
    print '</font>'
    print '</td></tr></TABLE>'
    print '</FORM>'
    print '<!-- SiteSearch Google -->'
#------------------------------------------------------------------------------


#------------------------------------------------------------------------------
def displayLogin(form, alert=None):
    print "<HTML>"
    print "<HEAD>"
    pmt_utils.javaScript("list_docs")
    pmt_utils.title("Data Item Listing")
    print "</HEAD>"
    pmt_utils.bodySetup()
    pmt_utils.mainHeading('Data Item Listing')
    pmt_utils.subHeading('Login')
    java="return submitForm(document.list_docs)"
    pmt_utils.formSetup("list_docs",db_name,"list_docs",java)
    pmt_utils.usernamePasswordDisplay()
    if alert!=None:
        pmt_utils.alertsArea(form,alert)
    print "<hr><INPUT TYPE='submit' NAME='submit' value='Submit' >"
    if form.has_key('directory'):
        if string.find(form['directory'].value,'..')>=0:
            sys.exit()
        print "<INPUT TYPE='hidden' NAME='directory' "
        print "value='%s'>" % form['directory'].value
        

#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
def pageSetup():
    print "<HTML>"
    print "<HEAD>"
    print '<meta name="robots" content="noindex,follow">'
    pmt_utils.title("Document Listing")
    print '    <SCRIPT TYPE="text/javascript">'
    print '    <!--'
    print '    function popup(mylink, windowname,w,h)'
    print '    {'
    print '    if (! window.focus)return true;'
    print '    var href;'
    print "    if (typeof(mylink) == 'string')"
    print '    href=mylink;'
    print '    else'
    print '    href=mylink.href;'
    print '    LeftPosition=(screen.width)?(screen.width-w)/2:100;'
    print '     TopPosition=(screen.height)?(screen.height-h)/2:100;'
    settings="'width='+ w + ',height='+ h + ',top=' + TopPosition + "
    settings=settings+"',left=' + LeftPosition + ',scrollbars=yes'"
    print "    settings=%s" % settings
    print '    popWindow=window.open(href, windowname, settings);'
    print '    popWindow.focus()'
    print '    return false;'
    print '    }'
    print '     //-->'
    print '    </SCRIPT>'
    print "</HEAD>"
    pmt_utils.bodySetup()
    print '<Font Face="SerpentineSansICG,Arial">'
    #addGoogle()
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
def verifyUserPass(db):
    
    status, details = db_authentication.password_valid(db,
                                                       crypt_salt=db_name,
                                                       username=username,
                                                       password=password)
    if status != 'success':
        displayLogin(form,details)
        #pmt_utils.alertsArea(form, details)
        sys.exit(1)

    if pmt_utils.hasPriv(db, username, 'list_docs')!=1:
        message='User %s does not have access to view Data Items' % username
        displayLogin(form,message)
        sys.exit(1)
#------------------------------------------------------------------------------


#------------------------------------------------------------------------------
def emailButton(key,menu_name, help_pdf):
    link='/%s-cgi-bin/email.pyc' % declarations.pmt_info['db_name']
    link=link+'?table=spr&key=%s' % key
    print '<HR>'
    print '<TABLE>'
    print '<TR>'
    java="return goto_url('%s')" % menu_name
    html='<INPUT TYPE="button" NAME="return_to_menu" VALUE=" Listing " '
    html=html+'onClick="%s">' % java
    pmt_utils.tableColumn(html)
    java="return popup('%s','Email_Problem_Report',600,500)" % link
    html='<input type="button" name="email" value="Email" onClick="%s">' % java
    pmt_utils.tableColumn(html)
    java="return goto_url ('%s')" % help_pdf
    html='<INPUT TYPE="button" NAME="help" VALUE=" Help " onClick="%s">' % java
    pmt_utils.tableColumn(html)
    print '</TR>'
    print '</TABLE>'
#------------------------------------------------------------------------------


#------------------------------------------------------------------------------
def setupTable(dir_name,form):
    print '<CENTER>'

    if db_name == 'save':
        print '<FONT SIZE="4"><B>IFC Program Data Items</B></FONT>'
    else:
        print '<FONT SIZE="4">'
        print '<B>%s Program Data Items</B></FONT>' % (string.upper(db_name))

    if dir_name == '':
        dir_name = '/'
    else:
        last_slash = string.rfind(dir_name[:-1], '/')
        if last_slash == 0:
            parent_name = '/'
        else:
            parent_name = dir_name[:last_slash]

        print '<form method=post action=/%s-cgi-bin/list_docs.pyc ' % db_name
        print 'enctype="application/x-www-form-urlencoded">'
        print '<FONT SIZE="4"><b>Parent Folder:</b>'
        print '<button type=submit name=parentlink value="Parent_Folder">'
        print '<IMG SRC="/icons/upone.gif">'
        print '<input type=submit value="Parent Folder" name=oldParLink>'
        print '</button>'
        print '<input type=hidden name=directory '
        print 'value="%s">' % parent_name
        print '</form>'


    print '<BR><FONT SIZE="4">'
    print '<B>Folder Name: %s</B></FONT>' % (string.upper(dir_name))
    print '<TABLE WIDTH=80%>'
    print '<TR>'
    print '<TH ALIGN=CENTER>Name</TH><TH>Details</TH><TH>Version</TH>'
    print '<TH>Type</TH><TH>Date Entered</TH><TH>Size</TH></TR>'
#------------------------------------------------------------------------------


#------------------------------------------------------------------------------
def havePermission(username,filename):
    file,ext=os.path.splitext(filename)

    # Don't display permissions files
    if ext=='.perm':
        return 0
    
    permFilename="%s.perm" % filename

    #print permFilename
    #print os.path.exists(permFilename)

    # If the permissions file exists...
    if os.path.exists(permFilename):
        # ..open it and get the list of allowed users
        permFile=open(permFilename,'r')
        owner=permFile.readline()
        allowedUsers=permFile.readlines()
        permFile.close()

        if string.find(owner,':')>=0:
            owner=string.split(owner,':')[1]
            owner=string.strip(owner)
            if username==owner:
                #print "owner=user"
                return 1
        else:
            allowedUsers.append(owner)
            owner="None"

        # Strip the newline
        for i in xrange(0,len(allowedUsers)):
            allowedUsers[i]=allowedUsers[i][:-1]

        # If the given username is in the list...
        if username in allowedUsers:
            # return true
            #print "user in allowed list"
            return 1
        else:
            # else the user is not in the permissions file so return false
            return 0
        
    else:
        # ...otherwise there is no permissions file so everyone has access
        #print "no perm file"
        return 1

#------------------------------------------------------------------------------


#------------------------------------------------------------------------------
def getOwner(filename):
    # Build the permissions filename
    permFilename="%s.perm" % filename

    # If the permissions file does not exist...
    if not os.path.exists(permFilename):
        # ... then there is no owner, return None
        return None

    # Read the first line from the permissions file
    permFile=open(permFilename,'r')
    ownerLine=permFile.readline()
    permFile.close()
    # If it specifies an owner...
    if len(ownerLine)>5:
        if string.upper(ownerLine[:5])=="OWNER":
            # ... return the owner's username
            owner=string.split(ownerLine,":")[1]
            owner=string.strip(owner)
            return owner

    # Since we got here there is no owner specified
    return None
#------------------------------------------------------------------------------


#------------------------------------------------------------------------------
def displayDataItem(form,username,details,serverpath,
                    full_path_name,filename, del_priv, admin_priv):

    # Allow folder admin to see all files, regardless of permissions
    #print username,serverpath
    if not havePermission(username,serverpath):
        return

    # Don't display permissions files
    file,ext=os.path.splitext(filename)
    if ext=='.perm':
        return 
    
    print '<TD ALIGN=CENTER CELLPADDING=5>'

    # print item name and link to download document
    if os.path.isdir(serverpath):
        link="/%s-cgi-bin/list_docs.pyc" % db_name
        link=link+"?project_name=%s&directory=%s" % (db_name,full_path_name)
        print '<a href="%s">%s</a>' % (link,details['item_name'])

    else:
        url="/%s/documents" % urllib.quote(db_name)
        url=url+"/%s" %  urllib.quote(full_path_name)
        print '<a href="%s">%s</a>' % (url, details['item_name'])

    print '</TD>'
    print '<TD ALIGN=CENTER>'

    if details['priv']=='None':
        print 'N/A'
    else:
        print '<form method="POST" action=%s>' % details['description']
        java="return popup('%s','File_Details',600,500)"%details['description']
        print '<input type="button" value="%s" ' % details['priv']
        print 'onClick="%s">' % (java)
        print '</form>'
    print '</TD>'

    print '<TD ALIGN=CENTER>'
    print details['version']
    print '</TD>'

    # figure out file type
    print '<TD ALIGN=CENTER>'
    if not os.path.isdir(serverpath):
        status, type, icon = os_utils.file_type(serverpath)
        if icon == None:
            print type
        else:
            print '<IMG SRC="/icons/%s" BORDER=0">' % (icon)
    else:
        url="/%s-cgi-bin/list_docs.pyc" % db_name
        print '<form method=post method=POST action=%s >' % url
        print '<input type=image src="/icons/folder.gif" border=0>'
        print '<input type=hidden name=directory value="%s">' % full_path_name
        print '</form>'
    print '</TD>'
    
    print '<TD ALIGN=CENTER>'
    print details['date']
    print '</TD>'

    print '<TD ALIGN=CENTER NOWRAP>'
    unit='B'
    full_file_name='/home/%s/documents/%s' % (db_name,full_path_name)
    size=os.stat(full_file_name)[stat.ST_SIZE]
    while size>=1024.0:
        size=size/1024.0
        if unit=='B': unit='KB'
        elif unit=='KB': unit='MB'
        elif unit=='MB': unit='GB'
        elif unit=='GB': unit='TB'
    print '%.2f %s' % (size,unit)
    print '</TD>'

    print '<td>'
    print '<TD Align=CENTER>'
    formData="?project=%s&fullpath=%s" % (db_name, serverpath)
    formData=formData+"&username=%s&name=%s" % (username, details['item_name'])
    poplink="/%s-cgi-bin/email.pyc%s" % (db_name, formData)
    if db_name!='usafsr':
        print '<form method="POST" action=poplink>'
        java="return popup('%s','Email_Data_Item',600,500)" % poplink
        print '<input type="button" value="Email" onClick="%s">' % java
        print '</form>'
    print '</td>'

    print '<TD Align=CENTER>'
    if del_priv==1 :#and (not os.path.isdir(serverpath)):
        formData='?project=%s&fullpath=%s&popup=1' % (db_name,serverpath)
        poplink="/%s-cgi-bin/delete.pyc%s" % (db_name, formData)
        print '<form method="POST" action=poplink>'
        java="return popup('%s','Confirm_File_Deletion',600,200)" % poplink
        print '<input type="button" value="Delete" onClick="%s">' % java
        print '</form>'
    print '</TD>'

    if admin_priv or username==getOwner(serverpath):
        print '<TD Align=CENTER>'
        print '<FORM method=post action=/%s-cgi-bin/permission.pyc>' % db_name
        url='/%s-cgi-bin/permission.pyc?filename=%s' % (db_name,serverpath)
        java="return popup('%s','Permissions',500,300)" % url
        print '<INPUT TYPE=button name=addlink value="Permissions" '
        print 'onClick="%s">' % java
        print '</form></TD>'


    print '</TR>'
#------------------------------------------------------------------------------


#------------------------------------------------------------------------------
def getDetails(form,html_filename,filename,priv):
    details={'item_name':'',
             'version':'',
             'date':'',
             'description':'',
             'priv':'View'}

    dir, file = os.path.split(html_filename)
    path='/home/%s/documents/%s/%s' % (db_name, dir, filename)
    serverpath='/home/%s/documents/%s' % (db_name, html_filename + '.html')
    status, lines = file_io.readFromFile(serverpath)

    if form.has_key('directory'):
        if string.find(form['directory'].value,'..')>=0:
            sys.exit()
        directory=form['directory'].value
    else: directory='/'

    noFile=0
    # if can't read file
    if status != 'success':
        details['item_name'] = filename
        details['version'] = "N/A"
        mod_time=time.localtime(os.stat(path)[stat.ST_MTIME])
        details['date'] = time.strftime('%m/%d/%y',mod_time)
        noFile=1
    else:
        # parse the details file for item_name, version, and date entered
        for line in lines:
            word=string.split(line)
            if len(word)==0:
                continue
            else:   end_index=len(word)-1
            if string.find(word[0],'Data')!=-1:
                details['item_name'] = string.join(word[3:end_index])
            elif string.find(word[0],'Version')!=-1:
                details['version'] = string.join(word[1:end_index])
            elif string.find(word[0],'Date')!=-1:
                if word[2][0]=='[':
                    mod_time=time.localtime(os.stat(path)[stat.ST_MTIME])
                    details['date'] = time.strftime('%m/%d/%y',mod_time)
                else:
                    details['date'] = string.join(word[2:end_index])
                    details['date'] = string.split(details['date'],'@')[0]


    if priv==1:
        details['priv']='Edit'
        link="/%s-cgi-bin/edit.pyc" % declarations.pmt_info['db_name']
        if noFile==1:
            details['priv']='Create'
            link="/%s-cgi-bin/edit.pyc" % declarations.pmt_info['db_name']
    else:
        if noFile==1:
            details['priv']='None'
            link=''
        else:
            details['priv']='View'
            link="/%s-cgi-bin/view.pyc" % declarations.pmt_info['db_name']
    link=link+'?project=%s&directory=%s' % (db_name,directory)
    link=link+'&filename=%s' % filename
    details['description']=link

    return details
#------------------------------------------------------------------------------


#------------------------------------------------------------------------------
def display_links(username,dir_name,edit_priv, del_priv):

    abs_filename='/home/%s/documents/%s/b00kmarkz' % (db_name, dir_name)

    if os.path.exists(abs_filename):
        bookmarks=open(abs_filename)
    else:
        return
    
    lines=bookmarks.readlines()
    
    for line in lines:
        if line==None:
            continue
        words=string.split(line)
        id=words[0]
        name=words[2]
        i=3
        while words[i]!='|':
            name=name+' '+words[i]
            i=i+1
        href=words[i+1]
        date=words[i+3]
        if href[:7]!='http://' and href[:6]!='ftp://':
            href='http://'+href
        print '<tr><td align=center><a href="%s">%s</a><br></td>' % (href,name)

        print '<TD ALIGN=CENTER>'
        if edit_priv==1:
            print '<form method="POST" action=/%s-cgi-bin/edit.pyc>' % db_name
            url='/%s-cgi-bin/edit.pyc?link=%s' % (db_name,id)
            url=url+'&file=%s' % (abs_filename)
            java="return popup('%s','File_Details',600,500)" % url
            print '<input type="button" value="Edit" onClick="%s">' % java
        else:
            print '<form method="POST" action=/%s-cgi-bin/view.pyc>' % db_name
            url="/%s-cgi-bin/view.pyc?link=%s" % (db_name,id)
            url=url+"&file=%s" % abs_filename
            java="return popup('%s','File_Details',600,500)" % url
            print '<input type="button" value="View" onClick="%s">' % java
        print '</form>'
        print '</TD>'

        print '<td align=center>Link</td>'
        print '<td align=center><img src=/icons/world1.gif></td>'
        print '<td align=center>%s</td>' % date
        print '<td align=center>Link</td><td></td>'

        formData="?project=%s&fullpath=%s" % (db_name,abs_filename)
        formData=formData+"&username=%s&name=%s&id=%s" % (username, name, id)
        poplink="/%s-cgi-bin/email.pyc%s" % (db_name,formData)
       
        if db_name!='usafsr':
            print '<td ALIGN=CENTER><form method="POST" action=poplink>'
            java="return popup('%s','Email_Data_Item',600,500)" % poplink
            print '<input type="button" value="Email" onClick="%s">' % java
            print '</form></td>'

        if del_priv==1:
            print '<TD Align=CENTER>'
            formData="?project=%s&fullpath=%s" % (db_name, abs_filename)
            formData=formData+"&name=%s&id=%s&popup=1" % (name, id)
            poplink="/%s-cgi-bin/delete.pyc%s" % (db_name, formData)
            print '<form method="POST" action=poplink>'
            java="return popup('%s','Confirm_File_Deletion',600,200)" % poplink
            print '<input type="button" value="Delete" onClick="%s">' % java
            print '</form></td>'

        print '</tr>'

    bookmarks.close()
#------------------------------------------------------------------------------


#------------------------------------------------------------------------------
def writeTable(form,username,
               edit_priv,      # edit data item details
               del_priv,       # delete data items (and folders)
               up_priv,        # upload data items
               private_priv,   # view private data items
               admin_priv): # change permissions and add folders

    if form.has_key('directory'):
        if form['directory'].value != '/':
            if string.find(form['directory'].value,'..')>=0:
                sys.exit()
            dir_name = form['directory'].value + '/'
        else:
            dir_name = '/'
    else:
        dir_name = '/'

    if dir_name[0]!='/':
        dir_name='/'+dir_name

    setupTable(dir_name,form)

    # List each file and info
    files = os.listdir("/home/%s/documents%s" % (db_name, dir_name))
    files.sort()
    for filename in files:

        if dir_name != '':
            full_path_name = dir_name + filename
        else:
            full_path_name = filename

        serverpath='/home/%s/documents/%s' % (db_name, full_path_name)

        if not os.path.exists(serverpath):
            continue

        if filename=='b00kmarkz' or filename=='b00kmarkz.backup':
            continue

        base, ext = os.path.splitext(full_path_name)

        # skip html details files
        if ext == '.html':
            status, lines = file_io.readFromFile(serverpath)
            if status != 'success':
                continue

            word = string.split(lines[0])

            if len(word) > 4:
                # skip over processing data item details html file
                if word[0] == '<HTML><HEAD><TITLE>Data' and \
                       word[1] == 'Item' and \
                       word[2] == 'Details' and word[3] == 'for:':
                    continue

        html_filename = full_path_name
        if string.count(filename,".") > 1:
            # replace multiple periods with underscores
            html_filename = string.replace(filename,".","_")
            html_filename = dir_name+html_filename

        details=getDetails(form, html_filename, filename,edit_priv)
        if filename=="private":
            if private_priv:
                displayDataItem(form,username,details,serverpath,
                                full_path_name,filename,del_priv,admin_priv)
        else:
            displayDataItem(form,username,details,serverpath,
                            full_path_name,filename,del_priv,admin_priv)
        
    display_links(username,dir_name,edit_priv,del_priv)

    print '</TABLE>'
    print '<hr>'

    print "<TABLE><TR>"

    if admin_priv:
        print '<TD><CENTER><FONT SIZE="-1">'
        print '<FORM method=post action=/%s-cgi-bin/add.pyc>' % db_name
        url='/%s-cgi-bin/add.pyc?location=%s' % (db_name,dir_name)
        java="return popup('%s','Add_Folder',500,300)" % url
        #print '<INPUT TYPE=hidden name=location value="%s">' % (dir_name)
        print '<INPUT TYPE=button name=addlink value="Add Folder" '
        print 'onClick="%s">' % java
        print '</form></CENTER></TD>'
        
    
    if db_name!='usafsr':
        print '<TD><CENTER><FONT SIZE="-1">'
        print '<FORM method=post action=/%s-cgi-bin/addlink.pyc>' % db_name
        url='/%s-cgi-bin/addlink.pyc?dest=%s' % (db_name,dir_name)
        java="return popup('%s','Add_Link',500,300)" % url
        print '<INPUT TYPE=button name=addlink value="Add Link" '
        print 'onClick="%s">' % java
        print '</form></CENTER></TD>'

    if up_priv==1:
        print '<TD><CENTER><FONT SIZE="-1">'
        print '<FORM method=post action=/%s-cgi-bin/upload.pyc>' % (db_name)
        print '<INPUT TYPE=submit name=uplink value="Upload File">'
        print '<INPUT TYPE=hidden name=dest value="%s">' % dir_name
        print '</form></CENTER><TD>'

    print "<TR></TABLE>"
#------------------------------------------------------------------------------



#------------------------------------------------------------------------------
pmt_utils.htmlContentType()
form = pmt_utils.getFormData()
db_name=declarations.pmt_info['db_name']
username,password=pmt_utils.getUserPass(form)

if username==None:
    displayLogin(form)

else:
    pageSetup()

    db = pmt_utils.connectDB(declarations.pmt_info['browser_username'],
                             declarations.pmt_info['browser_password'],
                             declarations.pmt_info['db_name'])

    # could not connect to db
    if db['status'] != 'success':
        message="Can not connect to database,\n" + db['message']
        pmt_utils.alertsArea(form,)
        sys.exit(1)

    verifyUserPass(db['result'])

    edit_priv    = pmt_utils.hasPriv(db['result'],username,'edit_details')
    del_priv     = pmt_utils.hasPriv(db['result'],username,'del_docs')
    up_priv      = pmt_utils.hasPriv(db['result'],username,'upload')
    private_priv = pmt_utils.hasPriv(db['result'],username,'private_data')
    admin_priv   = pmt_utils.hasPriv(db['result'],username,'folder_admin')
    writeTable(form,username,
               edit_priv,
               del_priv,
               up_priv,
               private_priv,
               admin_priv)

print '</BODY>'
print '</HTML>'
#------------------------------------------------------------------------------
