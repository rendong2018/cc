# -*-coding: utf-8-*-

import falcon, json, re
from wsgiref import simple_server
import pymysql
from login_api import *
from config import *
import gunicorn
from query_project import *

project_id = "18d34035-44be-4065-b8e1-cb0054f591ea"
db = Mysql(table_name="GLORIA_MYSQL")
sql = "select * from exp_result_mx where EX_SAMPLE_ID=\"%s\";" % project_id
db_out = db.fetch_one(sql)
print(db_out)