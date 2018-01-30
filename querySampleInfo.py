# coding:utf-8

import falcon
import json
import uuid
import sys
from query_sample_info import *
from login_api import *
from config import *
sys.getdefaultencoding()
import datetime


db = Mysql(table_name="GLORIA_MYSQL")
#project_id = "31ab7f93-2034-4ad7-a8aa-29a72adbd95b"  #12gene
# project_id = "03e2e538-b099-4ed8-b402-efdb960f2f43" #620gene
# project_id = "03fb8015-0f24-4bac-b36b-034fb0d61482" # 83gene
project_id = "ad2e61a8-d85a-4baa-9e0a-d3d83431f98e"  #15gene

sql = "select * from h_sample_item where item_id=\"%s\";" % project_id
data = db.fetch_all(sql)
sample_code = []
for d in data:
    sample_id = d[5]
    sql = "select * from sample_mx where ID=\"%s\";" % sample_id
    tmp = db.fetch_one(sql)
    try:
        print(tmp[3])
        if tmp[3] not in sample_code:
            sample_code.append(tmp[3])
    except Exception:
        print("tmp3",tmp)

with open("D:/cc/%s" % "15geneCode.txt",'w') as f1:
    for i in sample_code:
        f1.write(i+"\n")

print(len(sample_code))

