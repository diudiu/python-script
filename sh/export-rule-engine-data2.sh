#!/bin/bash
:<<BLOCK
说明: 用于从mysql中备份指定的表;
BLOCK

RULE_CONF_DATA_FILE=./sql.d/`date +%Y%m%d%H%M`-rule-engine-data.sql
TABLES="$(mysql -h$1 -u$2 -p$3 $4 -Bse 'show tables;')"

if [ $# -lt 3 ];then
   echo "[USAGE] sh export-rule-engine-data.sh <host> <user> <password>"
   exit
fi

for tname in $TABLES;do
    if [ $tname = "do_loan_manager_info" ]; then
        continue
    fi
    #echo $tname
    mysqldump -h$1 -u$2 -p$3  $4  ${tname} >> ${RULE_CONF_DATA_FILE}
done