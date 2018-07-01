#! /bin/tcsh -f
create_db pmt
gunzip -c pmt.db.dump.gz | psql pmt
exit 0
