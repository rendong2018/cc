# -*-coding: utf-8-*-

import falcon, json, sys
from wsgiref import simple_server
import pymysql
from login_api import *
from config import *
import gunicorn
# from query_project import *
from docx import Document
from docx.shared import Inches
import datetime
from falcon_multipart.middleware import MultipartMiddleware
from flask import Flask, request, render_template as rt
from project_conf import *

db = Mysql(table_name="REPORT_MYSQL")
info = {"普晟朗-肺癌靶向用药15基因检测":["/home/khl/web/word/15gene.xml","/home/khl/web/word/15gene.doc"],
        "普晟畅-结直肠癌靶向用药12基因检测": ["/home/khl/web/word/12gene.xml", "/home/khl/web/word/12gene.doc"],
        "普晟和-肿瘤靶向化疗用药83基因检测": ["/home/khl/web/word/83gene.xml", "/home/khl/web/word/83gene.doc"],
        "普益康-肿瘤个体化诊疗620基因检测": ["/home/khl/web/word/620gene.xml", "/home/khl/web/word/620gene.doc"],
        "普晟惠-PD-L1及CD8蛋白表达检测": ["/home/khl/web/word/pdl1.xml", "/home/khl/web/word/pdl1.doc"],
        "普晟惠-MSI微卫星不稳定性检测": ["/home/khl/web/word/msi.xml", "/home/khl/web/word/msi.doc"]}
for keys,values in info.items():
    sql = """update projectName set templateWord=\"%s\" and templateXml=\"%s\" where projectName=\"%s\";""" % (values[1],values[0],keys)
    print(sql)
    db.execute(sql)
db.commit()

# project = new_wechat_project()
# sql = "select * from projectName;"
# data = db.fetch_all(sql)
# project_list= []
# for i in data:
#     if i[1] not in project_list:
#         project_list.append(i[1])
# print('project_list', project_list)

# for keys,values in project.items():
#     if keys not in project_list:
#         sql = """insert into projectName(ID,projectName,datetime,version,type,ngs_type,author) values(UUID(),\"%s\",now(),"1.0","","ngs","何霞清");""" % keys
#         db.execute(sql)
# db.commit()


#
# sql = "select * from template;"
# data = db.fetch_all(sql)
# info = {}
# for i in data:
#     id = i[1]
#     url = i[4]+"/"+i[3]
#     info[id] = url
# print('info',info)

# sql = "select * from projectName;"
# d = db.fetch_all(sql)
# for item in d:
#     if item[0] in info.keys():
#         tmp_xml = info[item[0]]
#         name = tmp_xml.split('.xml')
#         word = name+".doc"
#         sql = "insert into projectName(templateWord, templateXml) values(%s,%s) where ID=\"%s\";" % (word, tmp_xml,item[0])
#         db.execute(sql)
# db.commit()
