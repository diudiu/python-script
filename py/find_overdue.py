#  -*- coding: utf-8 -*-
import pandas as pd
from pymongo import MongoClient

"""
说明: 根据excel中指定的apply_id,从mongo中查询数据,并填充excel中缺失的数据
主要用到了 data.loc[data['apply_id'] == appliy_id, 'name'] = one_doc["lineal_name"]
"""
if __name__ == "__main__":
    data = pd.read_excel('overdue.xlsx')
    appliy_ids = data['apply_id']

    client = MongoClient("mongodb://dev:123456@192.168.1.198:27017/riskcontrol_core")
    db = client['riskcontrol_core']
    collection = db['apply_base']

    for appliy_id in appliy_ids:
        one_doc = collection.find_one({"apply_id": appliy_id})
        if one_doc:
            data.loc[data['apply_id'] == appliy_id, 'name'] = one_doc["lineal_name"]
            data.loc[data['apply_id'] == appliy_id, 'pid'] = one_doc["card_id"]
            data.loc[data['apply_id'] == appliy_id, 'mobile'] = one_doc["lineal_mobile"]
    data.to_csv("result.csv", index=False)
