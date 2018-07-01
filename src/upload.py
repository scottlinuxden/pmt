# $Id$
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

import sys,os,cgi,glob,string,shutil
import os_utils
import StringIO
import declarations
import db_authentication
import commands
import smtplib
import pmt_utils
import file_io
import time


#-------------------------------------------------------------------------------
def displayLogin(alert=None):
    print "<HTML>"
    print "<HEAD>"
    pmt_utils.javaScript("upload")
    pmt_utils.title("Upload")
    print "</HEAD>"
    pmt_utils.bodySetup()
    pmt_utils.mainHeading('Upload')
    pmt_utils.subHeading('Login')
    pmt_utils.formSetup("upload",declarations.pmt_info['db_name'],
    		    "upload","return submitForm(document.upload)")
    pmt_utils.usernamePasswordDisplay()
    if alert!=None:
        pmt_utils.alertsArea(form,alert)
    print "<hr><INPUT TYPE='submit' NAME='submit' value='Submit' >"
    if form.has_key('dest'):
        print '<INPUT TYPE=hidden NAME=dest value="%s">' % form['dest'].value
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
def verifyUserPass():
    db = pmt_utils.connectDB(declarations.pmt_info['browser_username'],
                             declarations.pmt_info['browser_password'],
                             declarations.pmt_info['db_name'])

    # could not connect to db
    if db['status'] != 'success':
        displayLogin("Can not connect to database,\n" + db['message'])
        sys.exit(1)

    status, details = db_authentication.password_valid(db['result'],
            				crypt_salt=db_name,
            				username=username,
            				password=password)
    if status != 'success':
        displayLogin(details)
        sys.exit(1)

    if pmt_utils.hasPriv(db['result'],username,'upload')==0:
        displayLogin('User %s does not have upload privileges' % username)
        sys.exit()

#------------------------------------------------------------------------------



#------------------------------------------------------------------------------
def send_email(mailserver, from_address, recipients, subject, content):

    recipient_list = ''
    for i in recipients:
        recipient_list = recipient_list + ', '

    recipient_list = recipient_list[:-2]

    out=StringIO.StringIO()
    out.write("Subject: %s\n" % subject)
    out.write("To: %s\n\n" % recipient_list)
    out.write(content)

    mail=smtplib.SMTP(mailserver)

    mail.sendmail(
        from_addr=from_address,
        to_addrs=recipients,
        msg=out.getvalue())
#------------------------------------------------------------------------------



#------------------------------------------------------------------------------
def upload_results(html_message, email_message, form):
    print "<HTML><HEAD><TITLE>Upload Results</TITLE></HEAD><BODY>"
    print '<body background="/%s/icons/circ_bg.jpg">' % (db_name)
    print '<h3>Upload Results</h3>'
    print '<BLINK><STRONG>NOTE: All uploads are logged.</STRONG></BLINK><BR>'
    print html_message
    print "</BODY></HTML>"

    email_header = 'Program Name: ' + declarations.pmt_info['db_name'] + '\n'
    email_header = email_header + 'Username: ' + username +'\n\n'
    mail_support(email_header + email_message)
#------------------------------------------------------------------------------



#------------------------------------------------------------------------------
def mail_support(msg=""):

    email=db_name + "_uploads@isrparc.org" # where to email reports
    #email="webmaster@isrparc.org"

    content = "---------------------------------------\n"
    content = content + msg + '\n\n'

    for x in [ 'REQUEST_URI','HTTP_USER_AGENT','REMOTE_ADDR','HTTP_FROM',
               'REMOTE_HOST','REMOTE_PORT','SERVER_SOFTWARE','HTTP_REFERER',
               'REMOTE_IDENT','REMOTE_USER','QUERY_STRING','DATE_LOCAL' ]:
        if os.environ.has_key(x):
            line = "%s: %s\n" % (x, os.environ[x])
            content = content + line

    content = content + "---------------------------------------\n"

    db_label=string.upper(db_name)
    if db_label=="SAVE":
        db_label="IFCS"
    elif db_label=="BUAV":
        db_label="FCST"
    elif db_label=="CUAB":
        db_label="PADV"
    subject="%s Upload Report" % db_label
    pmt_utils.send_email('www.isrparc.org',email,[email],subject,content)
#------------------------------------------------------------------------------



#------------------------------------------------------------------------------
def display_form():
    print "<html>"
    print "<head>"
    print "<title>Documentation Maintenance</title></head>"
    print '<body background="/%s/icons/circ_bg.jpg">' % (db_name)

    pmt_utils.mainHeading("Upload")
    pmt_utils.subHeading("Single File, Zip, or Tarfile upload:")

    print '<P><form action="/%s-cgi-bin/upload.pyc" method="POST" enctype="multipart/form-data">' % db_name
    print '<TABLE BORDER=0>'

    # display the name of the data item
    print "<TR><TD><B>Data Item Name</B>:</TD><TD>"
    pmt_utils.textbox(None, 'name',  "", '40', '80',  None,  None)
    print "</TD></TR>"

    # display the version field
    print "<TR><TD><B>Version:</B></TD><TD>"
    pmt_utils.textbox(None,  'version',  "",  '40',  '80',  None,  None)
    print "</TD></TR>"

    # display the description field
    print "<TR><TD><B>Description:</B></TD><TD>"
    pmt_utils.textarea(None,   'description',   "",   '5',   '40',   None,   None)
    print "</TD></TR>"

    print '<TR><TD><B>Filename</B>:</TD>'
    print '<TD><input name="archive" type="file" size="40" maxlength="100"></TD></TR>'
    if form.has_key('dest'):
        dest=form['dest'].value
    else: dest=''
    print '<TR><TD><B>Destination Folder</B>:</TD><TD>'
    print '<input name="folder" type="text" size="40" maxlength="100" value="%s">' % dest
    print '</TD></TR></TABLE>'
    
    print '<input name="permissions" type="checkbox" value="permissions">'
    print 'Set file permissions after upload<BR>'

    print '<input name="extract" type="checkbox" value="extract">'
    print 'Extract archive on server<BR>'
    print '<input name="submit" type="submit" value="Upload File">'
    print '</form>'

    print '<HR>'

    print '<H3>Introduction</H3>'
    print '<P>This maintenance function will allow authorized users to upload a single file or file archive to their website.  The tar file may be compressed with gzip.  The archive file size when extracted should not'
    print 'exceed your maximum allowable disk space allotment for your site which is %d MB (%d bytes).  If this happens all files that exceed the allotment will not be stored in your website.  It is therefore suggested that you maintain a complete copy of your site locally and change your local copy to how you would like it on www.isrparc.org, create the archive of your local copy and upload the archive to www.isrparc.org.  The archive filename should end with .zip, .tar.gz, or .tgz</P>' % (upload_ceiling/(1024*1024),upload_ceiling)

    print '<P>You may upgrade your disk space allotment via an e-mail request to the www.isrparc.org <A HREF="mailto:support@isrparc.org">support team</A>.</P>'
    print '<H3>Directions for Uploading Archives</H3>'
    print '<P>You may upload a winzip, gzip, or tar file to your website.'
#    print 'The contents of the archive should match the following directory tree structure, in other words the directories listed below should be the top level directories when the archive is created.</P>'
    print '<P>All files including files in zip and tar archive should not have spaces in their name.</P>'
    print '<P>Filenames can have mixed case and are not governed by an 8.3 filename name specification.'
#    print '<P>If the file you are uploading is not a zip or tar archive, the file will be placed in the documents directory for the website you specify.'
#    print '<P>Allowable subdirectories in your archive file</P>'
#    print '<UL>'
#    print '<LI>documents'
#    print '</UL>'
#    print '<P>NOTE: Do <b>NOT</B> put a subdirectory called cgi-bin in your archive file. This can damage the Documentation Management engine at your website, if installed.</P>'
#    print '<P>Example (Windows 9x Systems at MS-DOS prompt):</p>'
#    print 'cd C:\<BR>'
#    print 'mkdir website<BR>'
#    print 'cd C:\website<BR>'
#    print 'mkdir documents<BR>'
#    print '<P>Put all of your document files: MS Word, Excel, Power Point, Adobe Acrobat, ASCII text under the documents directory'
#    print '<p>zip all files under c:\website directory but do not zip the directory c:\website</p>'
#    print '<P>If your archive has other directories in it besides the above mentioned names, these directories will not be accessed by the www.isrparc.org server and will be merely wasting your websites disk space allotment.  This Site Maintenance Upload program does not check the integrity of your archive file so it is imperative that you specify your archive as mentioned above.  Future updates will verify the contents of the archive file you are uploading.</P>'
    print '<p align="right"><A HREF="mailto:support@isrparc.org">Contact Support Team</a>'


    print '</body>'
    print '</html>'
#-------------------------------------------------------------------------------




#-------------------------------------------------------------------------------
def createDetails(filename, full_path, extracted=0):


    if extracted==1:
        itemname=filename
        date=time.strftime('%m/%d/%y',time.localtime(time.time()))
        file_name=filename
        version=form['version'].value
        index=string.find(full_path,'documents')
        location=full_path[index+10:]
        description='None'

    else:
        itemname=form['name'].value
        date=time.strftime('%m/%d/%y',time.localtime(time.time()))
        file_name=form['archive'].filename
        version=form['version'].value
        location=form['folder'].value
        description=form['description'].value
    if location=='': location='/'

    # write detail info in HTML format
    lines = []
    lines.append('<HTML><HEAD><TITLE>Data Item Details for: %s</TITLE></HEAD><BODY>' % (filename))
    lines.append('<body background="/%s/icons/circ_bg.jpg">' % (declarations.pmt_info['db_name']))
    lines.append('<CENTER><B><FONT COLOR="#000099">Data Item Details Page</FONT></B><HR SIZE=1 NOSHADE WIDTH=100%>')
    lines.append('<TABLE border=0>')
    lines.append('<TR><TD><B>Data Item Name:</B></TD><TD> %s <BR>' % (itemname))
    lines.append('<TR><TD><B>Date Entered:</B></TD><TD> %s <BR>' % date)
    lines.append('<TR><TD><B>Filename:</B></TD><TD> %s <BR>' % file_name)
    lines.append('<TR><TD><B>Version:</B></TD><TD> %s <BR>' % version)
    lines.append('<TR><TD><B>Location:</B></TD><TD> %s <BR>' % location)
    lines.append('<TR><TD><B>Description:</B></TD><TD> %s <BR>' % description)
    lines.append('</TABLE>')
    lines.append('</BODY></HTML>')

    # if the filename has more than 1 period in it replace them with _
    if string.count(filename,".") > 1:
        filename = string.replace(filename,".","_")

    # create html file with detail info
    status, details = file_io.writeToFile(full_path + filename + '.html', lines)
    if status != 'success':
        html_msg = details
        upload_results(html_msg,'Could not generate html details file for %s' % (filename),form)
        sys.exit()
#------------------------------------------------------------------------------



#-----------------------------------------------------------------------------
def pageEnd(table_data,db):
    print "</FORM>"
    pmt_utils.trailer(table_data, db)
    db.close()
    print "</BODY>"
    print "</HTML>"    
#-----------------------------------------------------------------------------


#----------------------------------------------------------------------------
def exit(messagetable_data=None,db=None,display_login=1):

    if display_login:
        pmt_utils.usernamePasswordDisplay(username)
    pmt_utils.alertsArea(form, message);

    if username!=None and db!=None:
        create_priv=pmt_utils.hasPriv(db,username,'create_spr')
    else:
        create_priv=0

    url='/%s/html/sprsum.html' % db_name
    pmt_utils.queryFunctionButtons(create_priv, url)

    pmt_utils.textbox(None, 'key_id', '', '10', '10', None, None, 'hidden')
    pmt_utils.textbox(None, 'action', '', '10', '10', None, None, 'hidden')
    pmt_utils.textbox(None, 'item_no', '', '8', '8', None, None, 'hidden')
    
    if table_data!=None and db!=None:
        pageEnd(table_data,db)
    sys.exit()
#-----------------------------------------------------------------------------


#-----------------------------------------------------------------------------
def extract(type_of_archive,
            full_path_name,full_path,
            email_msg,html_msg):

    if type_of_archive == 'TAR':
        os.chdir(full_path)
        status, archive_output = os_utils.tar_extract(full_path_name)
        filelist=string.split(archive_output)

    elif type_of_archive == 'ZIP' or type_of_archive == 'GZIP':

        os.chdir(full_path)

        if type_of_archive == 'ZIP':
            status,archive_output=os_utils.unzip(full_path_name,echoOnError=1)
            filelist=string.split(archive_output)

        elif type_of_archive == 'GZIP':
            # copy the original uploaded file under a pseudonym
            i=1
            pseudo=full_path_name+'%d' % i
            while os.path.exists(pseudo):
                i=i+1
                pseudo=full_path_name+'%d' % i
            pseudo_file = open(pseudo, "wb")
            pseudo_file.write(form['archive'].value)
            pseudo_file.close()


            # unzip the gzip file
            status, archive_output = os_utils.gunzip(full_path_name,
                                                     force=1,
                                                     echoOnError=1)
            filelist=string.split(archive_output)

            # if file was *.gz, unzip it and strip .gz form archive_name
            truncate=string.rfind(full_path_name,".gz")
            if truncate == -1:
                truncate=len(full_path_name)

            #archive_name = tar_archive_name
            tarName=full_path_name[:truncate]
            status,type_of_archive,icon=os_utils.file_type(tarName)

            # restore the name of the original upload
            os.rename(pseudo, full_path_name)
            
            # extract the tar file inside the gzip archive
            if type_of_archive == 'TAR':
                status, archive_output = os_utils.tar_extract(tarName)
                filelist=string.split(archive_output)
                os.remove(full_path_name[:truncate])

            else:
                html_msg = 'Invalid archive file type.  Upload aborted.'
                email_msg='Attempted upload to %s ' % db_name
                email_msg=email_msg+'failed since archive is an invalid type.'
                upload_results(html_msg,email_msg,form)
                sys.exit()
        else:
            os.rename(full_path_name, full_path_name)
            archive_name = archive_name
            status = 'success'
            archive_output = ''
            filelist=[]

        # create details file for each extracted file
        for file in filelist:
            realpath='/home/%s/documents/%s' % (db_name,file)
            if os.path.exists(realpath):
                if realpath[-1]=='/':
                    realpath=realpath[:-1]
                file_path, filename = os.path.split(realpath)
                file_path=file_path+'/'
                createDetails(filename,file_path,extracted=1)

    return archive_output

#-----------------------------------------------------------------------------


#-----------------------------------------------------------------------------
def doUpload():

    email_msg=html_msg=''
    
    dbResult = pmt_utils.connectDB(declarations.pmt_info['browser_username'],
                                   declarations.pmt_info['browser_password'],
                                   declarations.pmt_info['db_name'])

    # could not connect to db
    if dbResult['status'] != 'success':
        upload_results('Can not verify you as a valid user<BR>',
                       'Can not verify you as a valid user', form)
        sys.exit()

    db = dbResult['result']

    # check for valid login
    status, details =db_authentication.password_valid(db,
    						  crypt_salt=db_name,
    						  username=username,
    						  password=password)

    if status != 'success':
        pmt_utils.bodySetup()
        pmt_utils.alerts(form, 'Can not verify username/password')
        print '<hr><form method=post action=/%s-cgi-bin/upload.pyc>' % db_name
        print '<input name=back value="Back to Upload" type=submit>'
        print '</body>'
        sys.exit()

    if pmt_utils.hasPriv(db, username, 'upload')!=1:
        pmt_utils.bodySetup()
        pmt_utils.alerts(form, 'User %s does not have upload privileges' % username)
        print '<hr><form method=post action=/%s-cgi-bin/upload.pyc>' % db_name
        print '<input name=back value="Back to Upload" type=submit>'
        print '</body>'
        sys.exit()

    # check for valid upload site
    if not os.path.exists('/home/%s' % db_name):

        html_msg=html_msg+"Upload site %s does not exist.<BR>" % db_name
        html_msg=html_msg+"No archive file was uploaded.<BR>"
        email_msg=email_msg+"Upload site %s does not exist.\n" % db_name
        email_msg=email_msg+"No archive file was uploaded.\n"

        upload_results(html_msg, email_msg, form)
        sys.exit()

    # format destination for upload
    if not form.has_key('folder'):
        destination = ''
    else:
        if form['folder'].value == '/':
            destination = ''
        else:
            destination = form['folder'].value + '/'

    if form.has_key('archive'):

        # check for filesize is within allowable range
        archive_size = len(form['archive'].value)

        if archive_size == 0:
            msg="Suspicious archive file size of 0. Upload aborted."
            email_msg=email_msg+msg 
            html_msg=html_msg+msg+"<BR>"
            upload_results(html_msg,email_msg,form)
            sys.exit()
                        
        if archive_size > upload_ceiling:
            html_msg = 'Archive file size exceeds maximum upload limit '
            html_msg = html_msg + 'of %d bytes.<BR>' % (upload_ceiling)
            html_msg = html_msg + 'Archive file size is %d bytes.<BR>' % (archive_size)
            html_msg = html_msg + 'No archive file was uploaded.<BR>'
            email_msg=string.replace(html_msg,"<BR>",'\n')

            upload_results(html_msg, email_msg,form)
            sys.exit()
                        
        archive_name = form['archive'].filename
        archive_name = string.strip(archive_name)

        # strip off leading \\,/,:
        if string.rfind(archive_name,"\\") >= 0:
            archive_name = archive_name[string.rfind(archive_name,"\\")+1:]
        if string.rfind(archive_name,"/") >= 0:
            archive_name = archive_name[string.rfind(archive_name,"/")+1:]
        if string.rfind(archive_name,":") >= 0:
            archive_name = archive_name[string.rfind(archive_name,":")+1:]

        full_path='/home/' + db_name + '/documents/' + destination
        full_path_name=full_path + archive_name

        # write the archive to the website
        try:
            archive_file = open(full_path_name, "wb")

        except IOError, exception_details:
            html_msg = "No permissions to upload file to the website %s. " % db_name
            html_msg = html_msg+"Uploaded aborted.<BR>"
            html_msg = html_msg + 'File: '+full_path_name
            email_msg=string.replace(html_msg,"<BR>",'\n')
            email_msg=email_msg+'\nReason: ' + exception_details[1] + '\n\n'
            upload_results(html_msg,email_msg,form)
            sys.exit()
            
        archive_file.write(form['archive'].value)
        archive_file.close()

        status, type_of_archive, icon = os_utils.file_type(full_path_name)

        createDetails(archive_name, full_path)

        # extract archive
        if form.has_key('extract'):
            if status == 'success':
                archive_output=extract(type_of_archive,
                                       full_path_name,full_path,
                                       email_msg,html_msg)

            else:
                html_msg = 'Uploading unknown file type, in most cases this'
                html_msg = html_msg+'is alright but the file should be checked'
                email_msg='Upload to %s of an unknown file type.' % db_name
                upload_results(html_msg,email_msg,form)
                sys.exit()
        else:
            archive_output=''
            status='success'

        html_msg = '<TABLE BORDER=0>'

        if os.environ.has_key('REMOTE_ADDR'):
            html_msg = html_msg +'<TR><TD>Your IP Address:</TD>'
            html_msg = html_msg +'<TD>%s</TD></TR>'%(os.environ['REMOTE_ADDR'])

        html_msg = html_msg + '<TR><TD>Your browser I.D.:</TD>'
        html_msg = html_msg + '<TD><B>%s</B></TD></TR>' % (browser)

        fileSize=os.stat(full_path_name)[6]
        if type_of_archive == 'TAR' or type_of_archive == 'ZIP':
            html_msg = html_msg + '<TR><TD>Archive name is: </TD>'
            html_msg = html_msg + '<TD>%s</TD></TR>' % (archive_name)
            html_msg = html_msg + '<TR><TD>Archive file size (bytes): </TD>'
            html_msg = html_msg + '<TD>%d</TD></TR></TABLE>' %(fileSize)
        else:
            html_msg = html_msg + '<TR><TD>Filename is: </TD>'
            html_msg = html_msg + '<TD>%s</TD></TR>' % (archive_name)
            html_msg = html_msg + '<TR><TD>File size (bytes): </TD>'
            html_msg = html_msg + '<TD>%s</TD></TR></TABLE>' %(fileSize)

        if type_of_archive == 'TAR' or type_of_archive == 'ZIP':
            html_msg = html_msg + '<PRE>'
            html_msg = html_msg + archive_output
            html_msg = html_msg + '</PRE>'

        if form.has_key('extract'):
            html_msg=html_msg+'<CENTER><B>Your archive file has been uploaded '
            html_msg = html_msg + 'and extracted successfully.</B></CENTER>'
        else:
            html_msg = html_msg + '<CENTER><B>Your file has been successfully '
            html_msg = html_msg + 'uploaded.</B></CENTER>'

        html_msg = html_msg+'<HR><CENTER><FONT SIZE="-1">'
        html_msg = html_msg+"<form method=post action=/%s-cgi-bin/list_docs.pyc>" %db_name
        html_msg=html_msg+'<input name=project_name type=hidden value="%s">'%db_name
        html_msg = html_msg+"<input name=directory type=hidden "
        html_msg = html_msg+'value="%s">' % form['folder'].value
        html_msg = html_msg+'<input name=submit type=submit value="View Data Items">'
        html_msg = html_msg+"</form>"

        link = "http://%s" % (declarations.pmt_info['domain_name'])

        html_msg = html_msg+'<CENTER><FONT SIZE="-1"><A HREF="%s">' % link
        html_msg = html_msg+'%s</A></FONT></CENTER>'% declarations.pmt_info['domain_name']

        if type_of_archive == 'TAR' or type_of_archive == 'ZIP':
            email_msg=email_msg+'Archive file was uploaded to %s.\n' % db_name
            email_msg=email_msg+'Archive file size (bytes): %d'%os.stat(full_path_name)[6]
            email_msg=email_msg+'\nArchive file location: %s' % form['folder'].value
            email_msg=email_msg+'\nArchive filename: %s\n' % archive_name
            email_msg=email_msg+archive_output + '\n'
        else:
            email_msg = email_msg+'File was uploaded to %s.\n' % db_name
            email_msg = email_msg+'File size (bytes): %d\n' % os.stat(full_path_name)[6]
            email_msg = email_msg+'Filename: %s\n' % archive_name
            email_msg = email_msg+"File location: %s\n" % form['folder'].value
            email_msg = email_msg+archive_output + '\n'

        if form.has_key('extract'):
            os.remove(full_path_name)


    else:
        html_msg = html_msg+"No file was received.  No archive filename was specified<BR>"
        email_msg=email_msg+'Attempted upload to %s.\n' % db_name
        email_msg=email_msg+'Failed since archive filename was not specified.'

    #if form.has_key('permissions'):
    #    doPermissions(full_path_name)

        
    upload_results(html_msg, email_msg, form)
    print "</BODY></HTML>"

#------------------------------------------------------------------------------

#-----------------------------------------------------------------------------
def doPermissions(filename):
    print '<html>'
    print '<head>'
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
    print '</head>'

    permFile=open(filename+".perm",'w')
    permFile.write("Owner: %s\n" % username)
    permFile.close()

    
    java="return popup('/%s-cgi-bin/permission.pyc?filename=%s','Permissions',500,300)" % (db_name, filename)
    print '<body onLoad="%s">' % java


    #print '<BR>'
    #print filename
    #print '<BR>'

    #print "Handle Permissions now"

#-----------------------------------------------------------------------------


#------------------------------------------------------------------------------

pmt_utils.htmlContentType()
form=pmt_utils.getFormData()
db_name=declarations.pmt_info['db_name']
username,password=pmt_utils.getUserPass(form)

if os.environ.has_key("HTTP_USER_AGENT"):
    browser = os.environ["HTTP_USER_AGENT"]
else:
    browser = "No Known Browser"

if os.environ.has_key("SCRIPT_NAME"):
    posturl = os.environ["SCRIPT_NAME"]
else:
    posturl = ""
    
upload_ceiling = 100 * 1024 * 1024 # 100 megabytes


if form.has_key("permissions"):
    if form.has_key('archive'):
        archive_name=form['archive'].filename
        archive_name=string.strip(archive_name)
        # strip off leading \\,/,:
        if string.rfind(archive_name,"\\") >= 0:
            archive_name = archive_name[string.rfind(archive_name,"\\")+1:]
        if string.rfind(archive_name,"/") >= 0:
            archive_name = archive_name[string.rfind(archive_name,"/")+1:]
        if string.rfind(archive_name,":") >= 0:
            archive_name = archive_name[string.rfind(archive_name,":")+1:]
        path="/home/%s/documents/%s/" % (db_name,form['folder'].value)
        doPermissions(path+archive_name)

if form.has_key("archive"):
    doUpload()
    
else:
    pmt_utils.bodySetup()
    verifyUserPass()
    display_form()


