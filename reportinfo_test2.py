# -*-coding: utf-8-*-

import falcon, json, sys
from wsgiref import simple_server
import pymysql
from login_api import *
from config import *
import gunicorn
from query_project import *
from docx import Document
from docx.shared import Inches
from query_sample_info import *
sys.getdefaultencoding()
import datetime
from addinfo import templateword
from project_conf import *
from falcon_multipart.middleware import MultipartMiddleware
from flask import Flask, request, render_template as rt
from server import *

# app = falcon.API()

app = falcon.API(middleware=[MultipartMiddleware()])
app.req_options.auto_parse_form_urlencoded = True
app.req_options.keep_blank_qs_values = True


params= {}
params["sampleCode"] = "YHB1720537"
params['title'] = '普晟朗-肺癌靶向用药15基因检测'
params["reportName"] = 'testtrue'
params["userName"] = 'I'
params['workflowName'] = "aaaaaaa"

sample_code = params["sampleCode"]   # 样本编号
project = params["title"]  # 报告模板
report_name = params["reportName"]   # 文件名
user_name = params["userName"]
workflow_name = params["workflowName"]  # 报告结果名称
uidleft=None
uidright=None
db = Mysql(table_name="REPORT_MYSQL")
if not uidleft:
    uidLeft = None
else:
    sql = """select * from png where ID=\"%s\";""" % uidleft
    data = db.fetch_one(sql)
    uidLeft = os.path.join(data[-1], data[-2])
if not uidright:
    uidRight = None
else:
    sql = """select * from png where ID=\"%s\";""" % uidright
    data = db.fetch_one(sql)
    uidRight = os.path.join(data[-1], data[-2])

mysql = Mysql(table_name="MYSQL")
sql = "select * from login where userName=\"%s\";" % user_name
data1 = mysql.fetch_one(sql)
print('data1', data1)
if data1:
    usernameid = data1[-1]
    print(usernameid)
    out_path = "/home/khl/web/dist/downloads/tmp"
    if "组织版" in project:
        project_name = project.split('-组织版')[0]
        type = "组织版"
    elif "血液版" in project:
        project_name = project.split('-血液版')[0]
        type = "血液版"
    else:
        project_name = project
        type = None

    if type:
        sql = "select * from projectName where projectName=\"%s\" and type = \"%s\";" % (project_name, type)
    else:
        sql = "select * from projectName where projectName=\"%s\";" % project_name
    data = db.fetch_one(sql)
    projectname_id = data[0]
    analysis_name = data[1]
    sql = "select * from template where projectId=\"%s\";" % projectname_id
    data = db.fetch_one(sql)
    if data:
        xml_path = os.path.join(data[-1], data[-2])
        # xml_path = "/home/khl/web/word/msi.xml"
        print('xml_path', xml_path)

        if project_name == "普晟惠-PD-L1及CD8蛋白表达检测":
            tumor_infiltrating = get_tumor_infiltrating(tumorInfiltrating, pd28Tumor, pd28Lymph,
                                    pd142Tumor,pd142Lymph, cd8,tumorPercent, tumorLevel)
            msi_info = None
        if project_name == "普晟惠-MSI微卫星不稳定性检测":
            msi_info = get_msi_info(NR21=msi_list['NR21'], NR24=msi_list['NR24'],
                                    NR27=msi_list['NR27'], BAT25=msi_list['BAT25'], BAT26=msi_list['BAT26'],
                                    MONO27=msi_list['MONO27'], PentaC=msi_list['PentaC'],
                                    PentaD=msi_list['PentaD'],reportStable=reportStable)
            print('msi_info', msi_info)
            tumor_infiltrating = None

        pdfpath, pdfurl = templateword(xml_path, out_path, report_name, sample_code, project_name, usernameid, type, tumor_infiltrating=tumor_infiltrating, msi_info=msi_info, image_left=uidLeft,image_right=uidRight)
        ###ID,templateID,analysisName,sampleName,workflowName,DATETIME,STATUS,path,reportName,pdfPath,pdfUrl,userNameId)
        #sql_tmp = "insert into report(ID,templateID,analysisName,sampleName,workflowName,DATETIME,STATUS,path,reportName,pdfPath,pdfUrl,userNameId) values(UUID(), \"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\")"
        sql_tmp = "insert into report values(UUID(), \"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\")"
        sql = sql_tmp % (
        projectname_id, analysis_name, sample_code, workflow_name, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "完成", "/home/khl/web/dist/", report_name, pdfpath, pdfurl, usernameid)

        print(sql)
        db.execute(sql)
        db.commit()
        return_info = '{"success":true, "info": "Report generation success!" }'

    else:
        return_info = '{"success":false, "info": "Report generation failure!" }'

else:
    pass
