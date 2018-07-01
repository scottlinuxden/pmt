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
import declarations, pmt_utils, sys

def db_table_to_data_file(filename):
    
    dbResult = pmt_utils.connectDB(declarations.pmt_info['browser_username'], declarations.pmt_info['browser_password'], declarations.pmt_info['db_name'])
    
    # could not connect to db
    if dbResult['status'] != 'success':
        
        print 'Could not connect to database',
        sys.exit(1)
        
    pmt_utils.exec_sql_file(db, filename)

if __name__ == "__main__":
    db_table_to_data_file('pmt_tables.backup')
