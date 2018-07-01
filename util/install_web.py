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

import install
import sys

def main():
	install_engine = install.install(ignore_user_login=1,prompt=0,db_name=sys.argv[1])
	install_engine.pmt_utils_web()

if __name__ == "__main__":
	main()
