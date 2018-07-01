# $Id$
# Copyright (C) 1999 LinuXden, All Rights Reserved
# Copright Statement at http://www.linuxden.com/copyrighted_apps.html
#

import sys,os,cgi,glob,string
import os_utils
import db_authentication
import commands
import declarations
import pmt_utils
from passwdCookie import *

def display_form(form, alerts):

    username = ''
    current_password = ''
    new_password = ''
    verify_password = ''

    if form.has_key('username'):
        username = form['username'].value
    if form.has_key('current_password'):
        current_password = form['current_password'].value

    if form.has_key('new_password'):
        new_password = form['new_password'].value

    if form.has_key('verify_password'):
        verify_password = form['verify_password'].value
    
    print '<html><head><title>Password Maintenance</title></head>'
#    print '<body bgcolor="#B7BAB7" TEXT="#000000">
    print '<body background="/%s/icons/circ_bg.jpg">' % (declarations.pmt_info['db_name'])
#    print '<H1>Password Maintenance</H1>'
    pmt_utils.mainHeading('Maintenance')
    pmt_utils.subHeading('Change Password')

    print '<form action="/%s-cgi-bin/passwd_admin.pyc" method="POST" enctype="application/x-www-form-urlencoded">' % (declarations.pmt_info['db_name'])

    print '<TABLE BORDER=0>'

    print '<TR><TD><B>Username</B>:</TD><TD><input name="username" type="text" size="9" maxlength="9" value="%s"></TD></TR>' % (username)
    
    print '<TR><TD><B>Current Password:</B></TD><TD><input name="current_password" type="password" size="8" maxlength="8" value="%s"></TD></TR>' % (current_password)
    
    print '<TR><TD><B>New Password:</B></TD><TD><input name="new_password" type="password" size="8" maxlength="8" value="%s"></TD></TR>' % (new_password)
    
    print '<TR><TD><B>Verify Password:</B></TD><TD><input name="verify_password" type="password" size="8" maxlength="8" value="%s"></TD></TR>' % (verify_password)

    print '<TR><TD COLSPAN=2>'
    pmt_utils.alertsArea(form, alerts)
    print '</TD></TR>'

    print """</TABLE>
    <HR>
    <input name="submit" type="submit" value="Update Password">
    <p align="right"><A HREF="mailto:support@isrparc.org">Contact Support Team</a>"""

    print """</form>
    </body>
    </html>"""

#print "content-type: text/html\n"

form = cgi.FieldStorage()


if form.has_key('new_password'):

    dbResult = pmt_utils.connectDB(declarations.pmt_info['browser_username'], declarations.pmt_info['browser_password'], declarations.pmt_info['db_name'])

    # could not connect to db
    if dbResult['status'] != 'success':
        pmt_utils.htmlContentType()
        display_form(form, 'Password could not be updated. Can not connect to database.')
        sys.exit(1)

    else:


        db = dbResult['result']

        status, details = db_authentication.password_valid(db,
                                                           crypt_salt=declarations.pmt_info['db_name'],
                                                           username=form['username'].value,
                                                           password=form['current_password'].value)

        if status != 'success':
            pmt_utils.htmlContentType()
            display_form(form, details)
            sys.exit(1)

        if form['new_password'].value != form['verify_password'].value:
            pmt_utils.htmlContentType()
            display_form(form,'Can not verify your password, your new password does not match your entry for the verify password.')
            sys.exit(1)

        status, details = db_authentication.update_username_password(db=db,
                                                                     crypt_salt=declarations.pmt_info['db_name'],
                                                                     username=form['username'].value,
                                                                     password=form['new_password'].value)

        if status != 'success':
            pmt_utils.htmlContentType()
            display_form(form, 'Password not updated. Reason: %s' % (details))
            sys.exit(1)

        else:

            status, output = commands.getstatusoutput('/usr/bin/htpasswd -b /var/www/admin/%s.passwd %s %s' % (declarations.pmt_info['db_name'], form['username'].value, form['new_password'].value,))

            if status != 0:
                pmt_utils.htmlContentType()
                display_form(form, 'Password not updated. Reason: %s' % (output))

            else:
                loginCookie=authCookie()
                loginCookie.set(form['username'].value,form['new_password'].value)
		loginCookie.outputToBrowser(genHeader=1)

                display_form(form, 'Password updated.')

else:
    pmt_utils.htmlContentType()
    display_form(form, '')
