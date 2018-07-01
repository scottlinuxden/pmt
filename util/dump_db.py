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

def dump_db(db_name):

    status, output = commands.getstatusoutput('su postgres -c "/usr/bin/pg_dump %s | gzip >  /usr/local/pmt/%s.db.dump.gz"' % (db_name, db_name))

if __name__ == "__main__":
    dump_db('name of db')