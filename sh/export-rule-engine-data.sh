#!/bin/bash
:<<BLOCK
说明: 用于从mysql中备份指定的表;
主要使用了awk解析列表 awk '{for( i=1;i<=NF;i++) print $i}'
BLOCK

RULE_ENGINE_TABLES="rule
                    rule_set
                    flow_chart
                    policy_set
                    rn_credit_card_option_config
                    rn_credit_card_feature_config
                    rn_credit_card_model_config
                    result_code
                    fic_city_code_field
                    fic_client_overview
                    fic_data_source_info
                    fic_feature_card_type
                    fic_feature_code_mapping
                    fic_feature_common_conf
                    fic_feature_process_info
                    fic_feature_relevance_conf
                    fic_feature_rule_type
                    fic_feature_shunt_conf
                    fic_feature_type
                    fic_func_lib
                    fic_interface_info
                    fic_pre_field_info
                    menu
                    role
                    role_menu
                    account
                    company"

RULE_CONF_DATA_FILE=./`date +%Y%m%d%H%M`-init-rule-engine-data.sql

if [ $# -lt 3 ];then
   echo "[USAGE] sh export-rule-engine-data.sh <host> <user> <password>"
   exit
fi

for tname in `echo ${RULE_ENGINE_TABLES} | awk '{for( i=1;i<=NF;i++) print $i}'`;do
    mysqldump -h$1 -u$2 -p$3  featurefactory ${tname} >> ${RULE_CONF_DATA_FILE}
done
