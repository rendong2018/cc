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

sample_code = "YHF1810005"
# project_name = "普晟惠-MSI微卫星不稳定性检测"
project_name = "普晟惠-PD-L1及CD8蛋白表达检测"
xml_path = "/home/khl/web/word/pd-l1.xml"
# xml_path = "/home/khl/web/word/msi.xml"
# xml_path = "D:/cc/msi.xml"
sample_name = "YHF1810005_pdl1"
# project_name = "普晟畅（Personal-CRC）-结直肠癌靶向用药12基因检测-组织版"
usernameid = "09f7600c-de52-11e7-85d7-eef2f2e6a896"
# out_path = "/home/khl/web/dist/downloads/tmp"
out_path = "/home/khl/web/dist/downloads/tmp"
tumorInfiltrating = "活跃"
pd28Tumor = "阴性"
pd28Lymph = "阴性"
pd142Tumor = "阴性"
pd142Lymph = "阴性"
cd8 = "8%阳性"
tumorPercent = "50%"
tumorLevel = "aaa"
msiStable = "NR21_NR24_MONO27"
reportStable = "稳定"
user_name = "I"
project = project_name
report_name = "aaaamsi"
workflow_name = "aaaaaaaamsi"


msi_list = {"NR21":None,"NR24":None,"NR27":None,
                    "BAT25":None,"BAT26":None,"MONO27":None,"PentaC":None,"PentaD":None}

for item in msiStable.split("_"):
    if item in msi_list.keys():
        msi_list[item] = "稳定"
    else:
        msi_list[item] = "不稳定"
print(msiStable, reportStable)

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
    db = Mysql(table_name="REPORT_MYSQL")
    sql = "select * from report where sampleName=\"%s\" and analysisName=\"%s\";" % (sample_code, project_name)
    data_batch = db.fetch_all(sql)
    print('data_batch', data_batch)
    if data_batch:
        for data in data_batch:
            tmp_pdfpath = data[-3]
            tmp_pdfurl = data[-2]
            print(tmp_pdfpath,tmp_pdfurl)
            tmp_path = os.path.join(out_path, sample_code)
            if not os.path.exists(tmp_path):
                os.mkdir(tmp_path)
            new_pdfpath = os.path.join(tmp_path, report_name+".doc")
            new_pdfurl = os.path.join(tmp_path, report_name+".pdf")
            if os.path.exists(tmp_pdfpath):
                print("cp %s %s" % (tmp_pdfpath, new_pdfpath))
                os.system("cp %s %s" % (tmp_pdfpath, new_pdfpath))
                if os.path.exists(tmp_pdfurl):
                    os.system("cp %s %s" % (tmp_pdfurl, new_pdfurl))
                sql_tmp = "insert into report(ID,templateID,analysisName,sampleName,workflowName,DATETIME,STATUS,path,reportName,pdfPath,pdfUrl,userNameId) values(UUID(), \"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\")"
                sql = sql_tmp % (data[1], data[2], data[3], workflow_name, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    data[6], data[7], report_name, new_pdfpath, new_pdfurl, usernameid)
                print(sql)
                db.execute(sql)
                db.commit()
                return_info = '{"success":true, "info": "Report generation success!" }'
                break
            else:
                continue
    else:
        if type:
            sql = "select * from projectName where projectName=\"%s\" and type = \"%s\";" % (project_name, type)
        else:
            sql = "select * from projectName where projectName=\"%s\";" % project_name
        data = db.fetch_one(sql)
        projectname_id = data[0]
        analysis_name = data[1]
        sql = "select * from template where projectId=\"%s\";" % projectname_id
        data = db.fetch_one(sql)
        print('datahaha',data)
        if data:
            # xml_path = os.path.join(data[-1], data[-2])
            xml_path = "/home/khl/web/word/msi.xml"
            print('xml_path', xml_path)
            # xml_path = "/home/khl/web/word/15geneBlood.xml"
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
            pdfpath, pdfurl = templateword(xml_path, out_path, report_name, sample_code, project_name, usernameid, type, tumor_infiltrating=tumor_infiltrating, msi_info=msi_info)
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
