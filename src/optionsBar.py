import sys
import pmt_utils
import declarations

#--------------------------------------------------------------------------
# This functions adds the search box and the python logo to the optionsBar
def finishPage():

    print '<TABLE BORDER=0 COLS=1 WIDTH="100%">'
    print '  <TR ALIGN=CENTER>'
    print '    <TD><b><FONT COLOR="white" SIZE=-2><BR><BR>'
    print '        <A HREF="javascript:displaySearch()">Search:</A>'
    print '        </font></b></TD></TR>'
    print '<TR ALIGN=CENTER>'
    print '    <TD><FORM action="/cgi-bin/htsearch" method=post target="siteInfo">'
    print '         <INPUT type="text" size="7" name="words" MAXLENGTH="128" value="">'
    print '         <INPUT type=hidden name=method value=and>'
    print '         <INPUT type=hidden name=format value=builtin-long>'
    print '         <INPUT type=hidden name=config value="htdig.%s">' % db
    print '         <INPUT type=hidden name=restrict value="">'
    print '         <INPUT type=hidden name=exclude value="">'
    print '         </FORM></TD></TR></TABLE>'
    print '<BR><BR></CENTER>'
    print '<CENTER><FONT FACE="Garamond"><FONT COLOR="white"><FONT SIZE=-2>'
    print '<A HREF="javascript:displaySiteNotice()">Copyright'
    print '&copy; 1999, Linuxden.com, All rights reserved.</A>'
    print '</FONT></FONT></FONT></CENTER>'
    print '<BR><CENTER><A HREF="http://www.python.org" target="_top">'
    print '<IMG SRC="/icons/pypower.gif" BORDER=0></A></CENTER>'
    print '</body></html>'
#--------------------------------------------------------------------------


#--------------------------------------------------------------------------
# This function adds a login button
def simpleAdmin():
    print '<img src=/%s/icons/admin.gif>' % db
    print '<img src=/%s/icons/login.gif usemap="#login" border=0><br>' % db
    print '<map name=login>'
    loginPage="'/%s-cgi-bin/login.pyc?top=true'" % db
    java="return popup(%s,'Login',475,200)" % loginPage
    print '<area shape=rect coords="0,0,100,16" onClick="%s" ' % java
    print 'target="siteInfo"></map>'
#--------------------------------------------------------------------------

pmt_utils.htmlContentType()
db=declarations.pmt_info['db_name']

print """<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML//EN">
<html>
  <head>
        <script>
                supportsPreload =
                    (((navigator.appName == "Netscape") &&
            (parseInt(navigator.appVersion) >= 3 )) ||
            ((navigator.appName == "Microsoft Internet Explorer") &&
            (parseInt(navigator.appVersion) >= 4 )));

            if (supportsPreload) {
              capNormal = imagePreload('/icons/capButton.gif');
              capDepressed = imagePreload('/icons/capButtonDep.gif');
              programNormal = imagePreload('/icons/progButton.gif');
              programDepressed = imagePreload('/icons/progButtonDep.gif');
              travelNormal = imagePreload('/icons/travelButton.gif');
              travelDepressed = imagePreload('/icons/travelButtonDep.gif');
              employmentNormal = imagePreload('/icons/employButton.gif');
              employmentDepressed = imagePreload('/icons/employButtonDep.gif');
            }

            function imagePreload(img) {
              var a=new Image(); a.src=img; return a;
              }

        </script>
    <title>linuXden.com</title>

    <SCRIPT TYPE="text/javascript">
    window.name='options';
    </SCRIPT>


        <SCRIPT TYPE="text/javascript">
        function popup(mylink, windowname,w,h)
        {
        if (! window.focus)return true;
        var href;
        if (typeof(mylink) == 'string')
        href=mylink;
        else
        href=mylink.href;
        LeftPosition=(screen.width)?(screen.width-w)/2:100;
        TopPosition=(screen.height)?(screen.height-h)/2:100;
        settings='width='+ w + ',height='+ h + ',top=' + TopPosition + ',left=' + LeftPosition + ',scrollbars=yes'
        popWindow=window.open(href, windowname, settings);
        popWindow.focus()
        return false;
        }
        </SCRIPT>
  </head>
<SCRIPT LANGUAGE="JavaScript">
function displaySiteNotice() {
  window.open("/siteNotice.html","Site_Notice","scrollbars=yes,resizable=no,height=250,width=300");
}
function displaySearch() {
  window.open("/search.html","Search_Help","scrollbars=yes,resizable=no,height=200,width=300");
}
</script>"""

print '<BODY LINK="white" bgcolor="#000080">'
print "<TABLE BORDER=0 CELLPADDING=1 CELLSPACING=0></TABLE>"
print "<TABLE CELLPADDING=1 CELLSPACING=0></TABLE>"

print '<center>'
print '<A HREF="/%s/html/siteInfo.html" target="siteInfo">' % db
print '<img src="/%s/icons/%s.jpg" width=125></A></center>' % (db,db)
print '<center>'


username,password=pmt_utils.getUserPass(None)
if username!=None and password!=None:


    dbResult = pmt_utils.connectDB(declarations.pmt_info['browser_username'],
                                   declarations.pmt_info['browser_password'],
                                   declarations.pmt_info['db_name'])

    if dbResult['status'] != 'success':
        pmt_utils.alertsArea(None,dbResult['message'])
        sys.exit()
    else:
        DB=dbResult['result']

    print '<img src=/%s/icons/top.gif        usemap="#top" border=0><br>' % db

    #print db
    if db=="usafsr":
        form=pmt_utils.getFormData()
        #print form
        if form.has_key('public'):
            print '<img src=/%s/icons/downloads.gif usemap="#file_exchange" border=0><br>' % db
            simpleAdmin()
            print '<img src=/%s/icons/logout.gif        usemap="#logout" border=0><br>' % db
            print '<map name=file_exchange>'
            print '   <area shape=rect coords="0,0,100,16" href="/%s-cgi-bin/list_docs.pyc" target="siteInfo"></map>' % db
            print '<map name=top>'
            print '   <area shape=rect coords="0,23,100,39" href="http://www.linuxden.com" target="_top">'
            print '   <area shape=rect coords="0,40,100,56" href="http://www.linuxden.com" target="_top">'
            print '   <area shape=rect coords="0,57,100,73" href="/index.html" target="_top"></map>'
            print '<map name=logout>'
            parms="'/%s-cgi-bin/login.pyc?logout=1','LogOut',475,200" % db
            print '''<area shape=rect coords="0,0,100,16" onClick="return popup(%s)" target="siteInfo"></map>''' % parms
            finishPage()
            sys.exit()
            
    print '<img src=/%s/icons/contact_list.gif    usemap="#contact_list" border=0><br>' % db
    if db=='pmtdemo':
        if pmt_utils.hasPriv(DB,username,'cust_admin')==1:
            print '<img src=/%s/icons/customers.gif        usemap="#customers" border=0><br>' % db
    
    if db in ['pmtdemo']:
        if pmt_utils.hasPriv(DB,username, 'view_wiki')==1:
            print '<img src=/%s/icons/data_items.gif usemap="#data_items" border=0><br>' % db


    if pmt_utils.hasPriv(DB,username,'cvs_web')==1 or pmt_utils.hasPriv(DB,username,'cvs_export')==1:
        print '<img src=/%s/icons/dev_lib.gif        usemap="#dev_lib" border=0><br>' % db

    print '<img src=/%s/icons/action_items.gif    usemap="#action_items" border=0><br>' % db
    print '<img src=/%s/icons/problem_reports.gif    usemap="#problem_reports" border=0><br>' % db
    print '<img src=/%s/icons/change_props.gif    usemap="#change_props" border=0><br>' % db
    
    if pmt_utils.hasPriv(DB, username, 'view_task')==1:
        print '<img src=/%s/icons/task_list.gif     usemap="#task_list" border=0><br>' % db

    if pmt_utils.hasPriv(DB, username, 'create_po')==1:
        print '<img src=/%s/icons/purchasing.gif       usemap="#purchasing" border=0><br>' % db
    if pmt_utils.hasPriv(DB, username, 'create_inv')==1:
        print '<img src=/%s/icons/inventory.gif       usemap="#inventory" border=0><br>' % db

    print '<img src=/%s/icons/maillist.gif        usemap="#maillist" border=0><br>' % db


    if pmt_utils.hasPriv(DB,username,'list_docs')==1:
            if db=="usafsr":
                print '<img src=/%s/icons/downloads.gif  usemap="#file_exchange" border=0><br>' % db
            else:
                print '<img src=/%s/icons/file_exchange.gif    usemap="#file_exchange" border=0><br>' % db

    print '<img src=/%s/icons/downloads.gif        usemap="#downloads" border=0><br>' % db

    if db=='company':
        print '<img src=/%s/icons/timesheet.gif usemap="#timesheet" border=0><br>' % db
        print '<img src=/%s/icons/mail.gif        usemap="#mail" border=0><br>' % db
    print '<img src=/%s/icons/admin.gif>' % db
    print '<img src=/%s/icons/login.gif        usemap="#login" border=0><br>' % db
    print '<img src=/%s/icons/change_passwd.gif    usemap="#change_passwd" border=0><br>' % db


    if pmt_utils.hasPriv(DB,username,'upload')==1:
        print '<img src=/%s/icons/upload.gif        usemap="#upload" border=0><br>' % db
    if pmt_utils.hasPriv(DB,username,'folder_admin')==1:
        print '<img src=/%s/icons/doc_maint.gif        usemap="#doc_maint" border=0><br>' % db
    if pmt_utils.hasPriv(DB,username,'user_admin')==1:
        print '<img src=/%s/icons/user_admin.gif    usemap="#user_admin" border=0><br>' % db
    if pmt_utils.hasPriv(DB,username,'project_data')==1:
        print '<img src=/%s/icons/project_info.gif    usemap="#project_info" border=0><br>' % db
        print '<img src=/%s/icons/edit_options.gif    usemap="#edit_options" border=0><br>' % db


    print '<map name=contact_list>    <area shape=rect coords="0,0,100,16" href="/%s-cgi-bin/contact_list.pyc" target="siteInfo"></map>' % db
    print '<map name=timesheet>     <area shape=rect coords="0,0,100,16" href="http://63.163.164.10:7001/DeltekTC/welcome.msv" target="_top"></map>'
    print '<map name=customers>    <area shape=rect coords="0,0,100,16" href="/isr/html/cust_home.html" target="siteInfo"></map>'
    print '<map name=file_exchange>    <area shape=rect coords="0,0,100,16" href="/%s-cgi-bin/list_docs.pyc" target="siteInfo"></map>' % db
    print '<map name=dev_lib>    <area shape=rect coords="0,0,100,24" href="/%s-cgi-bin/cvsweb.pyc" target="siteInfo"></map>' % db
    print '<map name=action_items>    <area shape=rect coords="0,0,100,16" href="/%s-cgi-bin/pai_admin.pyc" target="siteInfo"></map>' % db
    print '<map name=problem_reports><area shape=rect coords="0,0,100,24" href="/%s-cgi-bin/spr_admin.pyc" target="siteInfo"></map>' % db
    print '<map name=change_props>    <area shape=rect coords="0,0,100,24" href="/%s-cgi-bin/ecp_admin.pyc" target="siteInfo"></map>' % db
    print '<map name=task_list>    <area shape=rect coords="0,0,100,16" href="/%s-cgi-bin/task_admin.pyc" target="siteInfo"></map>' % db
    print '<map name=purchasing>   <area shape=rect coords="0,0,100,16" href="/%s-cgi-bin/po_admin.pyc" target="siteInfo"></map>' % db
    print '<map name=inventory>   <area shape=rect coords="0,0,100,16" href="/%s-cgi-bin/inv_admin.pyc" target="siteInfo"></map>' % db
    if db=='aam':
        wikiName='AAM'
        print '<map name=data_items> <area shape=rect coords="0,0,100,16" href="https://www.isrparc.org/twiki/bin/view/%s/WebHome" target="_blank"></map>' % wikiName
    elif db=='buav':
        wikiName='MMS'
        print '<map name=data_items> <area shape=rect coords="0,0,100,16" href="https://www.isrparc.org/twiki/bin/view/%s/WebHome" target="_blank"></map>' % wikiName
    elif db=='save':
        wikiName="IFCS"
        print '<map name=data_items> <area shape=rect coords="0,0,100,16" href="https://www.isrparc.org/save-cgi-bin/twiki/view/%s/" target="_blank"></map>' % (wikiName)
    else:
        wikiName="Unknown"
        print '<map name=data_items> <area shape=rect coords="0,0,100,16" href="http://www.isrparc.org/twiki/bin/view/%s/WebHome" target="_blank"></map>' % wikiName
    print '<map name=downloads> <area shape=rect coords="0,0,100,16" href="/downloads.html" target="siteInfo"></map>'
    print '<map name=change_passwd>    <area shape=rect coords="0,0,100,24" href="/%s-cgi-bin/passwd_admin.pyc" target="siteInfo"></map>' % db
    print '<map name=upload>    <area shape=rect coords="0,0,100,16" href="/%s-cgi-bin/upload.pyc" target="siteInfo"></map>' % db
    print '<map name=doc_maint>    <area shape=rect coords="0,0,100,24" href="/%s-cgi-bin/doc_maintenance.pyc" target="siteInfo"></map>' % db
    print '<map name=user_admin>    <area shape=rect coords="0,0,100,16" href="/%s-cgi-bin/project_members_admin.pyc" target="siteInfo"></map>' % db
    print '<map name=project_info>    <area shape=rect coords="0,0,100,16" href="/%s-cgi-bin/project_admin.pyc" target="siteInfo"></map>' % db
    print '<map name=edit_options>    <area shape=rect coords="0,0,100,16" href="/%s-cgi-bin/options.pyc" target="siteInfo"></map>' % db




# else no username or password in cookie
else:
    print '<img src=/%s/icons/top.gif        usemap="#top" border=0><br>' % db
    if db!="usafsr":
        print '<img src=/%s/icons/contact_list.gif    usemap="#contact_list" border=0><br>' % db
#    if db=='isr':
#        print '<img src=/%s/icons/customers.gif        usemap="#customers" border=0><br>' % db
    #print '<img src=/%s/icons/file_exchange.gif    usemap="#file_exchange" border=0><br>' % db
    #print '<img src=/%s/icons/dev_lib.gif        usemap="#dev_lib" border=0><br>' % db
        print '<img src=/%s/icons/action_items.gif    usemap="#action_items" border=0><br>' % db
        print '<img src=/%s/icons/problem_reports.gif    usemap="#problem_reports" border=0><br>' % db
        print '<img src=/%s/icons/change_props.gif    usemap="#change_props" border=0><br>' % db
    #print '<img src=/%s/icons/task_list.gif     usemap="#task_list" border=0><br>' % db
    #if db!="usafsr":
    if db!="usafsr":
        print '<img src=/%s/icons/purchasing.gif usemap="#purchasing" border=0><br>' % db
        print '<img src=/%s/icons/inventory.gif usemap="#inventory" border=0><br>' % db
        if db=='isr':
            print '<img src=/%s/icons/timesheet.gif usemap="#timesheet" border=0><br>' % db
            print '<img src=/%s/icons/mail.gif    usemap="#mail" border=0><br>' % db
    print '<img src=/%s/icons/downloads.gif        usemap="#downloads" border=0><br>' % db
    print '<img src=/%s/icons/admin.gif><br>' % db
    print '<img src=/%s/icons/login.gif        usemap="#login" border=0><br>' % db
    if db!='usafsr':
        print '<img src=/%s/icons/change_passwd.gif    usemap="#change_passwd" border=0><br>' % db

    print """<map name=contact_list>    <area shape=rect coords="0,0,100,16" onClick="return popup('/%s-cgi-bin/login.pyc?page=contact_list.pyc','Contact_List',475,200)" target="siteInfo"></map>""" % db
    print '<map name=customers>    <area shape=rect coords="0,0,100,16" href="/isr/html/cust_home.html" target="siteInfo"></map>'
    print """<map name=file_exchange>        <area shape=rect coords="0,0,100,16" onClick="return popup('/%s-cgi-bin/login.pyc?page=list_docs.pyc','File_exchange',475,200)" target="siteInfo"></map>""" % db
    print """<map name=dev_lib>        <area shape=rect coords="0,0,100,24" onClick="return popup('/%s-cgi-bin/login.pyc?page=cvsweb.pyc','CVS_Web_Access',475,200)" target="siteInfo"></map>""" % db
    print """<map name=action_items>    <area shape=rect coords="0,0,100,16" onClick="return popup('/%s-cgi-bin/login.pyc?page=pai_admin.pyc','Action_Items',475,200)" target="siteInfo"></map>""" % db
    print """<map name=problem_reports>    <area shape=rect coords="0,0,100,24" onClick="return popup('/%s-cgi-bin/login.pyc?page=spr_admin.pyc','Problem_Reports',475,200)" target="siteInfo"></map>""" % db
    print """<map name=change_props>    <area shape=rect coords="0,0,100,24" onClick="return popup('/%s-cgi-bin/login.pyc?page=ecp_admin.pyc','Change_Proposals',475,200)" target="siteInfo"></map>""" % db
    print """<map name=task_list>        <area shape=rect coords="0,0,100,16" onClick="return popup('/%s-cgi-bin/login.pyc?page=task_admin.pyc','Task_List',475,200)" target="siteInfo"></map>""" % db
    print """<map name=purchasing>     <area shape=rect coords="0,0,100,16" onClick="return popup('/%s-cgi-bin/login.pyc?page=po_admin.pyc','Purchasing',475,200)" target="siteInfo"></map>""" % db
    print """<map name=inventory>     <area shape=rect coords="0,0,100,16" onClick="return popup('/%s-cgi-bin/login.pyc?page=inv_admin.pyc','Inventory',475,200)" target="siteInfo"></map>""" % db
    if db=="usafsr":
        print '<map name=downloads>    <area shape=rect coords="0,0,100,16" href="/%s-cgi-bin/list_docs.pyc?username=public&password=public" target="siteInfo"></map>' % db
    else:
        print """<map name=downloads> <area shape=rect coords="0,0,100,24" href="/downloads/downloads.html" target="siteInfo"></map>"""
    print """<map name=change_passwd>    <area shape=rect coords="0,0,100,24" onClick="return popup('/%s-cgi-bin/login.pyc?page=passwd_admin.pyc','Change_Password',475,200)" target="siteInfo"></map>""" % db
    print '<map name=timesheet>     <area shape=rect coords="0,0,100,16" href="http://63.163.164.10:7001/DeltekTC/welcome.msv" target="_top"></map>'

print '<img src=/%s/icons/logout.gif        usemap="#logout" border=0><br>' % db

if declarations.pmt_info['db_name']=='save':
    mail_page='ifcs'
else:    mail_page=db

print '<map name=maillist>    <area shape=rect coords="0,0,100,16" href="/mailman/listinfo/%s" target="siteInfo"></map>' % mail_page
    
#print '<map name=mail>        <area shape=rect coords="0,0,100,16" href="/cgi-bin/bobomail.cgi" target="siteInfo"></map>'
print '''<map name=login>    <area shape=rect coords="0,0,100,16" onClick="return popup('/%s-cgi-bin/login.pyc?top=true','Login',475,200)" target="siteInfo"></map>''' % db
print '''<map name=logout>    <area shape=rect coords="0,0,100,16" onClick="return popup('/%s-cgi-bin/login.pyc?logout=1','LogOut',475,200)" target="siteInfo"></map>''' % db

print '<map name=top>'
print '                <area shape=rect coords="0,23,100,39" href="http://www.linuxden.com" target="_top">'
print '                <area shape=rect coords="0,40,100,56" href="http://www.wavefish.org" target="_top">'
print '                <area shape=rect coords="0,57,100,73" href="/index.html" target="_top"></map>'
print '</center>'

finishPage()
