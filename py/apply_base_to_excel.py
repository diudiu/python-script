#  -*- coding: utf-8 -*-

import pandas as pd
from pandas.io.json import json_normalize
from pymongo import MongoClient
import urllib.parse

'''
说明: 将存储在mongo中的json文档转换成二维的excel文档, 主要用到了json_normalize函数
'''


def normalize_doc(doc):
    normalized = json_normalize(doc)
    return normalized


if __name__ == "__main__":
    username = urllib.parse.quote_plus('dev')
    password = urllib.parse.quote_plus('123456')
    # client = MongoClient("mongodb://dev:123456@192.168.1.100:8078/feature_storage_v2")
    # client = MongoClient("mongodb://%s:%s@116.62.42.89:27017" % (username, password))
    # client = MongoClient("mongodb://%s:%s@de.digcredit.com:2717" % (username, password))
    client = MongoClient("mongodb://de.digcredit.com:2717")
    db = client['feature_storage']
    db.authenticate(username, password, mechanism='SCRAM-SHA-1')
    collection1 = db['apply_base_v1']  # 1.0
    collection12 = db['apply_base_v12']  # 并行2.0
    collection2 = db['apply_base']     # 2.0

    all_doc1 = collection1.find()
    all_doc12 = collection12.find()
    all_doc2 = collection2.find()

    result = pd.DataFrame()
    # for doc in all_doc1:
    #     normalized = json_normalize(doc)
    #     result = result.append(normalized, ignore_index=True)
    for doc in all_doc12:
        normalized = json_normalize(doc)
        result = result.append(normalized, ignore_index=True)
    for doc in all_doc2:
        normalized = json_normalize(doc)
        result = result.append(normalized, ignore_index=True)

    del result["_id"]
    del result["data.operator_dig_upload.call_list.wd_api_mobilephone_getdata_response.data.data_list"]
    del result["data.operator_dig_upload.call_pay_list"]
    del result["data.operator_dig_upload.phone_list"]

    # result.to_csv("data_analysis_v2.csv", index=False)  # 2.0
    result.to_excel("flatten_apply_base_v2.xls", index=False)
    # result.to_csv("data_analysis_v1.csv", index=False)   # 1.0
