#!/usr/bin/env python
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
#

import os, string, commands, sys
import save_declarations
import spyball_declarations
import ivvnn_declarations
import usafsr_declarations
import c17_declarations
import biometrics_declarations
import isr_declarations

def dump_db_tables(db_name, table_data):

    table_name_keys = table_data.keys()
	
    table_name_keys.sort()

    for table_name in table_name_keys:

        status, output = commands.getstatusoutput('su postgres -c "/usr/bin/pg_dump %s -t %s -D -a -f /usr/local/pmt/%s.%s.table_dump"' % (db_name, table_name, db_name, table_name))

if __name__ == "__main__":
        dump_db_tables('save', save_declarations.define_tables())
        dump_db_tables('c17', c17_declarations.define_tables())
	dump_db_tables('spyball',spyball_declarations.define_tables())
	dump_db_tables('ivvnn', ivvnn_declarations.define_tables())
	dump_db_tables('biometrics', biometrics_declarations.define_tables())
	dump_db_tables('usafsr', usafsr_declarations.define_tables())
	dump_db_tables('isr', isr_declarations.define_tables())







