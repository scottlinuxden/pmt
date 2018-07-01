import sys
import os
import string
import smtplib
import time
import types
import file_io
import php_sess
from pg import DB
import _pg
from mod_python import apache,util

#username: www
#password: wkuapi
#database: scott needs changed to phoenix
#/srv/www/htdocs/phoenix directory

#item table
#nationalproduct = 4th column
#description = 5th column
#itempk = next key
#itempksk = 1
#itemtypelfk = 1
#threshholdreorder = 0
#frequencycount = -1
#frequencyperiod = 3
#unit = 69
#maxcount = 1
#dayofuse = 1
#unittext=cc

#lot table
#manufacturer = 3rd column
#lotpk=nextkey
#lotpksk = 1
#itemfk = itemkey inserted before the lot
#itemfksk = 1
#expirationdate = 10th column
#lotnum = 9th column
#manufacturer = 3rd column

#lotqty
#lotqty = next key
#lotpkfk = refers to lot table lotpk
#lotpkfksk =1
#qtyonhand=6th column

debugOn = 0
debugReq=None

def debug(output):
    global debugOn
    if debugOn:
        debugReq.write('DEBUG: %s<BR>' % (output))
    
def executeSQL(db, sqlStatement):
    """
    Execute a sql statement specified by sqlStatement for the already
    open db connection designate by db
    Returns a queryResult type, see above
    """

    try:
        pgqueryObject = db.query(sqlStatement)

    except TypeError:
        debug('type error')
        return {'status' : 'error', 'message' : "TypeError: Bad Argument type, or too many arguments", 'result' : None}
    except ValueError:
        debug('value error')
        return {'status' : 'error', 'message' : "ValueError: Empty SQL Query", 'result' : None}
    except _pg.ProgrammingError, message:
        debug('programming error: message = %s' % (message))
        return {'status' : 'error', 'message' : message, 'result' : None}

    # sql statement is not a select or insert
    if pgqueryObject == None:
        return {'status' : 'success', 'message' : "SQL Statement processed returning nothing", 'result' : None}

    # sql statement is an insert or update statement
    if type(pgqueryObject) is types.IntType:
        return {'status' : 'success', 'message' : "SQL Statement processed return number rows affected", 'result' : pgqueryObject}

    elif type(pgqueryObject) is types.LongType:
        return {'status' : 'success', 'message' : "SQL Statement processed return number rows affected", 'result' : pgqueryObject}

    result = pgqueryObject.dictresult()

    for row in xrange(0,len(result)):
        for column in result[row].keys():
            if result[row][column] == None:
                result[row][column] = ""

    return {'status' : 'success', 'message' : "SQL Query processed returning rows fetched", 'result' : result}

def sqlFieldFormat(fieldValue):
    isNumber=0
    checkForNumber = string.replace(fieldValue,",","")
    for i in [int,float]:
        try:
            b = i(checkForNumber)
            fieldValue = `b`
        except ValueError:
            pass
        else:
            isNumber = 1
            break

    if not isNumber:
        if string.strip(fieldValue) == '':
            fieldValue = "NULL"
        else:
            fieldValue = string.replace(fieldValue,"'","\\'")
            fieldValue = "'%s'" % (fieldValue)

    return fieldValue

def mainHeading(req,
                topic):
    """
    Generates the Main Header HTML
    """
    req.write('<FONT FACE="Verdana,Arial" SIZE="-1" COLOR="darkRed"><B>' + topic + '</B></FONT><BR>')

def connectDB(username, password, database):
    
    try:
        
        db = DB(database, 'localhost', 5432, None, None, username, password)
        
    except TypeError:
        return {'status' : 'error', 'message' : "Bad Argument type, or too many arguments", 'result' : None}
    
    except SyntaxError:
        return {'status' : 'error', 'message' : "Duplicate argument definition in connect", 'result' : None}
    
    except _pg.InternalError, message:
        return {'status' : 'error', 'message' : message, 'result' : None}
    
    return {'status' : 'success', 'message' : 'Database connection succeeded', 'result' : db}
    
def verifyUserPass(req,
                   form,
                   username,
                   password,
                   db_name):

    db = connectDB(username,
                   password,
                   db_name)

    # could not connect to db
    if db['status'] != 'success':
        sys.exit(1)

def contentType(req):

    req.content_type = 'text/html'
    req.send_http_header()

def insertLot(db,
              itemfk,
              itemfksk,
              manufacturer,
              expirationdate,
              number):

    sqlStatement = "SELECT NEXTVAL('public.lot_lotpk_seq'::text)"
    
    result = executeSQL(db,sqlStatement)
    
    if result['status'] == 'success':
        
        lotpk = result['result'][0]['nextval']
        lotpksk = 1
        
        sqlStatement = "INSERT INTO lot (lotpk,lotpksk,itemfk,itemfksk,expirationdate,lotnum,manufacturer) VALUES (%s, %s, %s, %s, %s, %s, %s)" % (lotpk, lotpksk, itemfk, itemfksk, expirationdate, number, manufacturer)

        debug("sqlStatement = %s" % (sqlStatement))
        result = executeSQL(db,sqlStatement)
        
        if result['status'] == 'success':
            return {'status' : 'success', 'lotpk' : lotpk, 'lotpksk' : lotpksk}
        else:
            return {'status' : 'error', 'lotpk' : None, 'lotpksk' : None}
            
    else:
        return {'status' : 'error', 'lotpk' : None, 'lotpksk' : None}

def insertLotQty(db,
                 lotpkfk,
                 lotpkfksk,
                 qtyonhand):

    sqlStatement = "INSERT INTO lotqty (lotpkfk,lotpkfksk,qtyonhand) VALUES (%s,%s,%s)" % (lotpkfk,lotpkfksk,qtyonhand)
    
    debug("sqlStatement = %s" % (sqlStatement))
    result = executeSQL(db,sqlStatement)
    
    if result['status'] == 'success':
        return {'status' : 'success', 'lotqty' : None}
    else:
        return {'status' : 'error', 'lotqty' : None}
    
def insertItem(db,
               item_national_product,
               item_description,
               thresholdreorder,
               frequencycount,
               maxcount,
               daysofuse,
               unittext):
    
    frequencyperiod = 3
    unit = 69
    itemtypelfk = 1
    
    sqlStatement = "SELECT NEXTVAL('public.item_itempk_seq'::text)"
    
    result = executeSQL(db,sqlStatement)
    
    if result['status'] == 'success':
        
        itempk = result['result'][0]['nextval']
        itempksk = 1
        
        sqlStatement = "INSERT INTO item (itempk,itempksk,itemtypefk,nationalproduct,description,thresholdreorder,frequencycount,frequencyperiodfk,unit) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)" % (itempk, itempksk, itemtypelfk, item_national_product, item_description, thresholdreorder, frequencycount, frequencyperiod, unit)
        
        debug('sqlStatement = %s' % (sqlStatement))
        
        result = executeSQL(db,sqlStatement)
        
        if result['status'] == 'success':
            return {'status' : 'success', 'itempk' : itempk, 'itempksk' : itempksk}
        
        else:
            return {'status' : 'error', 'itempk' : None, 'itempksk' : None}
        
    else:
        return {'status' : 'error', 'itempk' : None, 'itempksk' : None}
        
def upload_results(req,
                   html_message):
            
    req.write("<HTML><HEAD><TITLE>Inventory Importer</TITLE></HEAD>")
    req.write('<body bgcolor=#bacb91>')
    mainHeading(req,"Inventory Importer")
    req.write('<HR>')

    req.write('<FONT FACE="Verdana,Arial" Size=-1>')
    req.write('<b>Results</b><br>')
    req.write(html_message)
    req.write('</font>')
    req.write('<hr><form method="post"><input type="button" value="Ok" onClick="self.close();"> </form>')
    req.write("</BODY></HTML>")
    
def display_form(req,alert=None):
        
    req.write("<html>")
    req.write("<head>")
    req.write("<title>Inventory Importer</title></head>")
    req.write('<body bgcolor=#bacb91>')
    
    mainHeading(req,"Inventory Importer")

    req.write('<HR>')

    req.write('<FONT FACE="Verdana,Arial" Size=-1><b>Directions for Importing</B><br>')
    req.write('Enter the name of a valid import file in the <b>Filename</b> text field<br>')
    req.write('by manually typing in the name or by selecting the <b>Browse...</B><br>')
    req.write('button and navigating to the file location via a file browser dialog.<br>')
    req.write('The file must be a supported CDC file format.<br>')
    req.write('</font>')

    req.write('<form action="/phoenix/importer.pyc/importer" method="POST" enctype="multipart/form-data">')

    req.write('<TABLE BORDER=0>')

    req.write('<TR><TD><FONT FACE="Verdana,Arial" Size=-1><B>Filename</B></font>:</TD>')
    req.write('<TD><input name="archive" type="file" size="40" maxlength="100"></TD></TR>')

    req.write("</TABLE>")
    if alert:
        req.write('<FONT FACE="verdana,arial" color=black size=-1"><b>Alerts:</b></FONT><br><FONT FACE="Verdana,Arial" color=red Size=-1><b>%s</B><br>' % (alert))

    req.write('<hr><input name="submit" type="submit" value="Import"></p>')
    req.write('</form>')

    req.write('</body>')
    req.write('</html>')

def doUpload(req,
             form,
             username,
             password,
             db_name):

    verifyUserPass(req,
                   form,
                   username,
                   password,
                   db_name)

    html_msg = ''

    if form.has_key('archive'):

        # check for filesize is within allowable range
        archive_size = len(form['archive'].value)

        if archive_size == 0:
            msg="Suspicious import file size of 0. Import aborted."
            html_msg=html_msg+msg+"<BR>"
            upload_results(req,html_msg)
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

        full_path='/home/phoenix/importer/'
        full_path_name=full_path + archive_name

        # write the archive to the website
        try:
            archive_file = open(full_path_name, "wb")

        except IOError, exception_details:
            html_msg = "No permissions to import file to the website %s. " % db_name
            html_msg = html_msg+"Import aborted.<BR>"
            html_msg = html_msg + 'File: '+full_path_name
            upload_results(req,html_msg)
            sys.exit()
            
        archive_file.write(form['archive'].value)
        archive_file.close()

        fileSize=os.stat(full_path_name)[6]

        html_msg = html_msg + '<b>Import Filename: </b>'
        html_msg = html_msg + '%s<BR>' % (archive_name)
        html_msg = html_msg + '<b>File Size (bytes): </b>'
        html_msg = html_msg + '%s<BR>' % (fileSize)

        # item table presets
        thresholdreorder = 0
        frequencycount = 0
        maxcount = 0
        daysofuse = 0.0

        # lot table presets
        # lotpk=nextkey
        # itemfk = itemkey inserted before the lot

        # lotqty
        # lotqty = next key
        # lotpkfk = refers to lot table lotpk

        debugReq = req
        dbResult = connectDB(username,
                       password,
                       db_name)
        
        # could not connect to db
        if dbResult['status'] != 'success':
            sys.exit(1)

        db = dbResult['result']

        no_errors = 1
        itemsInserted = 0
        linesProcessed = 0

        html_msg = html_msg + "<b>Alerts:</B><br>"
        status, lines = file_io.readFromFile(full_path_name)

        if status == 'success':

            for i in xrange(0,len(lines)):

                if string.strip(lines[i]) == '':
                    continue

                debug('curline = :%s:' % (lines[i]))
                fields = string.split(lines[i],'|')

                for j in xrange(0,len(fields)):
                    fields[j] = sqlFieldFormat(fields[j])

                    debug('fields[%d] = :%s:' % (j,fields[j]))

                try:
                    item_national_product = fields[3]
                    item_description = fields[4]
                    lot_manufacturer = fields[2]
                    lot_expirationdate = fields[10]
                    lot_num = fields[9]
                    lotqty_qtyonhand = fields[5]
                    unittext = fields[6]
                except:
                    no_errors = 0
                    html_msg = html_msg + 'Error invalid importer file format.<BR>'
                    os.remove(full_path_name)
                    break
                
                result = executeSQL(db,"BEGIN")

                result = insertItem(db,item_national_product,item_description,
                                    thresholdreorder,frequencycount,maxcount,daysofuse,unittext)
                
                if result['status'] == 'success':

                    result = insertLot(db,result['itempk'],result['itempksk'],lot_manufacturer,
                                       lot_expirationdate,lot_num)

                    if result['status'] == 'success':

                        result = insertLotQty(db,result['lotpk'],result['lotpksk'],lotqty_qtyonhand)

                        if result['status'] == 'success':
                            result = executeSQL(db,"COMMIT");
                            itemsInserted += 1
                            
                        else:
                            result = executeSQL(db,"ROLLBACK")
                            no_errors = 0
                            html_msg = html_msg + 'Error inserting lot quantity table from data on line %d of import file.<BR>' % (i)

                    else:
                        result = executeSQL(db,"ROLLBACK")
                        no_errors = 0
                        html_msg = html_msg + 'Error inserting lot table from data on line %d of import file.<BR>' % (i)

                else:
                    result = executeSQL(db,"ROLLBACK")
                    no_errors = 0
                    html_msg = html_msg + 'Error inserting item table from data on line %d of import file.<BR>' % (i)

                linesProcessed += 1

            html_msg = html_msg + '%d lines processed, %d items have been successfully imported.<BR>' % (linesProcessed,itemsInserted)

            if no_errors:
                pass
            else:
                html_msg = html_msg + 'The import file could not be imported in its entirety.<BR>'

        else:
            html_msg = html_msg + "Can not read import file %s<br>" % (archive_name)
            
    else:
        html_msg = html_msg + "No import filename was specified, import aborted<BR>"

    upload_results(req,html_msg)

def importer(
    req):

    #global debugReq
    #debugReq = req
    form = req.form
    db_name='phoenix'
    username='www'
    password='wkuapi'

    contentType(req)

    #php_session = php_sess.setupSession(req)

    #if not php_session.has_key('userPK'):
    #    util.redirect(req,"/phoenix/permatslogon.php")

    #if not php_session.has_key():
    #    util.redirect(req,"/phoenix/main.php")
    #else:
    #    if php_session['fulladmin'] == 'f':
    #        util.redirect(req,"/phoenix/main.php")

    if form.has_key('archive'):
        archive_name=form['archive'].filename
        archive_name=string.strip(archive_name)

        if len(archive_name) != 0:

           if len(form['archive'].value) == 0:
                alert = 'Specified file does not exist.'

                verifyUserPass(req,
                               form,
                               username,
                               password,
                               db_name)
                
                display_form(req,alert)
           else:
 
               # strip off leading \\,/,:
               if string.rfind(archive_name,"\\") >= 0:
                   archive_name = archive_name[string.rfind(archive_name,"\\")+1:]
               if string.rfind(archive_name,"/") >= 0:
                   archive_name = archive_name[string.rfind(archive_name,"/")+1:]
               if string.rfind(archive_name,":") >= 0:
                   archive_name = archive_name[string.rfind(archive_name,":")+1:]
                        
               doUpload(req,
                        form,
                        username,
                        password,
                        db_name)
        else:
            alert = 'No import filename specified.'

            verifyUserPass(req,
                           form,
                           username,
                           password,
                           db_name)

            display_form(req,alert)
            
    else:
        verifyUserPass(req,
                       form,
                       username,
                       password,
                       db_name)

        display_form(req)
        
        
