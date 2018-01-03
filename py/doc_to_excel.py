#  -*- coding: utf-8 -*-

import pandas as pd
from pandas.io.json import json_normalize
from pymongo import MongoClient

'''
说明: 将存储在mongo中的json文档转换成二维的excel文档, 主要用到了json_normalize函数
'''


def normalize_doc(doc):
    if doc['data'] == "":
        normalized = pd.DataFrame([[0, 0, 0]], columns=["_id", "userId", "error_code"])
    else:
        normalized = json_normalize(doc['data'])

    normalized["_id"] = doc["_id"]
    normalized["userId"] = doc["userId"]
    normalized["error_code"] = doc["error_code"]

    return normalized

if __name__ == "__main__":
    client = MongoClient("mongodb://dev:123456@192.168.1.100:8078/bfm")
    db = client['bfm']
    collection = db['lending']
    all_doc = collection.find().limit(300)
    one_doc = collection.find_one({"userId": 7200})

    result = normalize_doc(one_doc)
    for doc in all_doc:
        if len(doc['data']) > 1:
            print(doc)

        normalized = normalize_doc(doc)
        result = result.append(normalized, ignore_index=True)
    result.to_csv("data_analysis.csv", index=False)

