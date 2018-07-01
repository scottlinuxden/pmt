import declarations
import pmt_utils
import db_authentication
import sys
from passwdCookie import *
import sha

def printJavascript():
    # Print Javascript for targetopener, and finish functions
    print '<SCRIPT TYPE="text/javascript">'
    print '<!--'
    # targetopener closes the popup and redirects the opener
    print 'function targetopener(mylink, closeme, closeonly)'
    print '{' 

    if form.has_key('top'):
        if form['top'].value=='true':
            print 'if (closeme)window.close();'
            print 'if (window.opener.top.location != window.opener.location) {'
            print '    window.opener.top.location.href = mylink ;'
            print '    window.opener.location.reload();'
            print '  }'
            print 'else {'
            print 'opener.location=mylink;}'
            
            
        elif form['top'].value=='other':
            print 'if (! closeonly)window.opener.top.location.href=mylink;'
            print 'if (closeme)window.close();'
            print 'if (opener.top.location != opener.location)    {'
            print 'opener.location=mylink;}'
        else:
            print 'if (! closeonly)window.opener.top.siteInfo.location.href=mylink;'
            print 'if (closeme)window.close();'
            print 'if (opener.top.location != opener.location)    {'
            print '    opener.top.siteInfo.location.href = mylink ;'
            print '    opener.location.reload();                  }'

    else:
        print 'if (! closeonly)window.opener.top.siteInfo.location.href=mylink;'
        print 'if (closeme)window.close();'
        print 'if (opener.top.location != opener.location)    {'
        print '    opener.top.siteInfo.location.href = mylink ;'        
        print '    opener.location.reload();                  }'
    print 'return false;'
    print '}'

    # finish closes the popup and refreshed the opener
    print 'function finish()  {'
    print '  opener.location.reload();'
    print '  window.close();'
    print '  return false;  }'
    print '//-->'
    print '</SCRIPT>'


def printUserPass():
    print '  <form method=post action=/%s-cgi-bin/login.pyc>' % db_name
    print '  <center><table>'
    print '  <tr><td><font color=white><b>Username:</b></font></td>'
    print '      <td><input type=text name=username size=8 maxlength=8></td></tr>'
    print '  <tr><td><font color=white><b>Password:</b></font></td>'
    print '      <td><input type=password name=password size=8 maxlength=8></td></tr>'
    print '  </table>'
    print '  <input type=submit name=submit value=submit>'

    # Retain old form data
    if form.has_key('page'):
        print '<input type=hidden name=page value="%s">' % form['page'].value
    if form.has_key('top'):
        print '<input type=hidden name=top value="%s">'%form['top'].value
                
    print '  </center>'
    print '  </form>'
   
def validUserPass(username,password):
     dbResult=pmt_utils.connectDB(declarations.pmt_info['browser_username'],
                                  declarations.pmt_info['browser_password'],
                                  declarations.pmt_info['db_name'])

     # could not connect to db
     if dbResult['status'] != 'success':
         pmt_utils.htmlContentType()
         print '<html>'
         pmt_utils.alertsArea(form, "Can not connect to database")
         sys.exit(1)
     else:
         db = dbResult['result']
         
     status, details = db_authentication.password_valid(db,
                                                        crypt_salt=db_name,
                                                        username=username,
                                                        password=password)

     return status
    

def processLogin():
    # Store username and password in a cookie
    loginCookie = authCookie()

    # If the username in the form is none...
    if form['username'].value=='none':
        # ... get the user/pass from the cookie
        pmt_utils.htmlContentType()
        print '<html>'
        username,password=loginCookie.get()
        
    else:
        # otherwise see if the user/pass entered into the from is valid
        hash=sha.new(form['password'].value).digest()
        status=validUserPass(form['username'].value,hash)

        # if the given user/pass is not valid...
        if status!='success':
            # ...display an error message and redraw the login prompt
            pmt_utils.htmlContentType()
            print '<html>'
            print ' <body bgcolor="#000080">'
            print '  <img src="/%s/icons/header.gif">' % db_name
            print '  <center>'
            print '  <font color=white><b>'
	    print 'Invalid username/password'
            print '  </b></font>'
            print '  </center>'
            printUserPass()
            sys.exit(1)

        # since we got here, the user/pass must be valid, so store them in a cookie...
        loginCookie.set(form['username'].value,form['password'].value)
        loginCookie.outputToBrowser(genHeader=1)
        print '<html>'
        formData=''
        if form.has_key('page'):
            formData='&page='+form['page'].value
        if form.has_key('top'):
            formData=formData+'&top='+form['top'].value
        # ... and refresh the page
        print '<head><meta http-equiv="refresh" content="0; '
	print 'url=/%s-cgi-bin/login.pyc?username=none%s" />' % (db_name,
                                                                 formData)
	print '</head>'

    print '<body bgcolor="#000080">'
    print '<img src="/%s/icons/header.gif">' % db_name

    printJavascript()

    print '<font color=white><b>'

    # If the cookie was not stored...
    username,password=loginCookie.get()
    if username==None:
        # ... output and error ...
        print 'Your browser is blocking cookies.  '
	print 'You will be required to login at each page unless you'
	print 'allow cookies from www.isrparc.org.'
        print '<BR><BR><CENTER>Please Wait...</CENTER>'
    else:
        # ... otherwise output the cookie information
        print 'A cookie has been stored on your computer.  '
	print 'It will expire in 100 days.'

    # Retain the old form data ... 
    print '<form method=post action=/%s-cgi-bin/login.pyc>' % db_name
    if form.has_key('page'):
        page=form['page'].value
    else:
        if db_name=='usafsr':
            page='/%s-cgi-bin/index.pyc?username=%s' % (db_name,username)
        else:
            page='/%s/html/index.html' % db_name

    # ... and add a button to close the window and redirect the opener
    java="return targetopener('%s',true)" % (page)
    print '<center><input type=submit name=submit value=OK onClick="%s">' %java
    print '</center></form></b></font>'



def checkCookie():
    # See if the test cookie actually retained the information
    testCookie=authCookie()
    username,password=testCookie.get()

    pmt_utils.htmlContentType()
    print '<html>'

    # If the cookie was not created
    if username==None and password==None:

        # Print the script for closing the window
        printJavascript()

        # Wait three seconds and then close window and redirect the opener
        if form.has_key('page'):
            java="targetopener('%s',true)" % (form['page'].value)
	    print '<body onLoad=setTimeout("%s",3000) bgcolor="#000080">' %java
        else:
            java="setTimeout(window.close, 3000)"
	    print '<BODY onLoad="%s" bgcolor="#000080">' % java

        # Display error message
        print '<img src="/%s/icons/header.gif">' % db_name
        print '<font color=white><b>'
        print 'Your browser is blocking cookies.  '
	print 'You wil be required to login at each page unless you '
	print 'allow cookies from www.isrparc.org.'
        print '<BR><BR><CENTER>Please Wait...</CENTER></b></font>'

    else:
        # Otherwise, cookies are working so draw the login prompt
        print '<body bgcolor="#000080">'
        print '<img src="/%s/icons/header.gif">' % db_name
        printUserPass()
   
def logout():
    # Get rid of the current cookie
    killCookie=authCookie()
    killCookie.logout()
    killCookie.outputToBrowser(genHeader=1)

    # Print the javascript to close the window
    print '<html><head>'
    printJavascript()
    print '</head>'

    # Display a message and a button to close the window
    print '<body bgcolor="#000080">'
    print '<img src="/%s/icons/header.gif">' % db_name
    print '<center><font color=white><b>'
    print 'Your cookie has been removed.</b></font>'
    print '<form>'
    print '<input type=button value="Close Window" name=close '
    print 'onClick="return finish()">'
    print '</form></center>'
    

def initLogin():

    # Check for a valid cookie
    loginCookie = authCookie()
    username,password=loginCookie.get()
    # If there is a valid cookie present...
    if validUserPass(username,password)=='success':
        # ...close the login popup and redirect the opener
        pmt_utils.htmlContentType()
        print '<html>'
        print '<head>'
        printJavascript()
        print '</head>'
        if form.has_key('page'):
            link=form['page'].value
            print '<body onLoad=targetopener("%s",true,false)>' % link
        else:
            print '<body onLoad=finish()>'
        
    else:
        # ...otherwise there was no valid cookie

        # create a test cookie to see if cookies are enabled
        testCookie=authCookie()
        testCookie.set('test','test')
        testCookie.outputToBrowser(genHeader=1)

        # retain the form data
        formData=''
        if form.has_key('page'):
            formData='&page=' + form['page'].value
        if form.has_key('top'):
            formData=formData+'&top=' + form['top'].value

        # refresh the page
        print '<html>'
        print '<head><meta http-equiv="refresh" content="0; '
        print 'url=/%s-cgi-bin/login.pyc?cookietest=none%s" />' %(db_name,formData)
        print '</head><body>'
    

form = pmt_utils.getFormData()
db_name=declarations.pmt_info['db_name']


if form.has_key('username'):
    # Check if the login is valid and store the cookie
    processLogin()

elif form.has_key('cookietest'):
    # Check if the test cookie was created
    checkCookie()
    
elif form.has_key('logout'):
    # Remove the current cookie
    logout()

else:
    # Check for a valid cookie and create a test cookie
    initLogin()

print '</body></html>'
