#!/bin/bash
source .credentials
python phpmyadmin_sql_backup.py ${SQLURL} ${SQLUSER} ${SQLPASS} -o data -q ${SQLOPTIONS}
