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
    #
    # normalized["_id"] = doc["_id"]
    # normalized["userId"] = doc["userId"]
    # normalized["error_code"] = doc["error_code"]

    return normalized

if __name__ == "__main__":
    username = urllib.parse.quote_plus('featrage')
    password = urllib.parse.quote_plus('feat46660N')
    # client = MongoClient("mongodb://dev:123456@192.168.1.100:8078/feature_storage_v2")
    client = MongoClient("mongodb://%s:%s@116.62.42.89:27017" % (username, password))
    db = client['feature_storage_v2']
    collection = db['apply_base']
    all_doc = collection.find().limit(5)
    one_doc = collection.find_one({"apply_id": "APPLY20171116161838612550209"})

    result = normalize_doc(one_doc)

    meta = []
    for doc in all_doc:
        if len(doc['data']) > 1:
            print(doc)

        normalized = normalize_doc(doc)
        result = result.append(normalized, ignore_index=True)
    result.to_csv("data_analysis.csv", index=False)

