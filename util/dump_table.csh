#! /bin/tcsh -f
echo -n "Enter database name to dump: "; set db_name=$<
echo -n "Enter table name to dump: "; set table_name=$<
echo "Enter Postgres username/password to logging into db as"
/usr/bin/pg_dump $db_name -t $table_name -D -a -u -f ${db_name}.${table_name}.table_dump
