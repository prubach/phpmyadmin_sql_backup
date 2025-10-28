#!/bin/bash
source .credentials
python phpmyadmin_sql_backup.py ${SQLURL} ${SQLUSER} ${SQLPASS} -c gzip -o data -q ${SQLOPTIONS}
