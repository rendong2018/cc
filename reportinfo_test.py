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

class reportInfo(object):
    def on_post(self, req, resp):
        params = req.params
        sample_code = params["sampleCode"]   # 样本编号
        project = params["title"]  # 报告模板
        report_name = params["reportName"]   # 文件名
        user_name = params["userName"]
        workflow_name = params["workflowName"]  # 报告结果名称
        print(sample_code,project,report_name,user_name,workflow_name)

        tumorInfiltrating = params["tumorInfiltrating"]
        pd28Tumor = params["pd28Tumor"]
        pd28Lymph = params["pd28Lymph"]
        pd142Tumor = params["pd142Tumor"]
        pd142Lymph = params["pd142Lymph"]
        cd8 = params["cd8"]
        tumorPercent = params["tumorPercent"]
        tumorLevel = params["tumorLevel"]  #msi稳定性判断

        msiStable = params["msiStable"]  #判断稳定或者不稳定
        # uid= params['uid']
        filenameLeft = params['filenameLeft']
        filenameRight = params['filenameRight']
        uidleft = params['uidLeft']
        uidright = params['uidRight']
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
        msi_list = {"NR21":None,"NR24":None,"NR27":None,
                    "BAT25":None,"BAT26":None,"MONO27":None,"PentaC":None,"PentaD":None}
        print('msiStable', msiStable)
        if msiStable:
            for item in msi_list.keys():
                if item in msiStable.split("_"):
                    msi_list[item] = "稳定"
                else:
                    msi_list[item] = "不稳定"
            print('msi_list', msi_list)
        reportStable = params["reportStable"]

        resp.status = falcon.HTTP_200
        resp._headers["Access-Control-Allow-Origin"] = "*"

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
            resp.status = falcon.HTTP_200
            resp._headers["Access-Control-Allow-Origin"] = "*"

            if type:
                sql = "select * from projectName where projectName=\"%s\" and type = \"%s\";" % (project_name, type)
            else:
                sql = "select * from projectName where projectName=\"%s\";" % project_name
            data = db.fetch_one(sql)
            projectname_id = data[0]
            analysis_name = data[1]
            xml_path = data[8]
            if data:
                print('xml_path', xml_path)
                if project_name == "普晟惠-PD-L1及CD8蛋白表达检测":
                    tumor_infiltrating = get_tumor_infiltrating(tumorInfiltrating, pd28Tumor, pd28Lymph,
                                            pd142Tumor,pd142Lymph, cd8,tumorPercent, tumorLevel)
                    msi_info = None
                elif project_name == "普晟惠-MSI微卫星不稳定性检测":
                    msi_info = get_msi_info(NR21=msi_list['NR21'], NR24=msi_list['NR24'],
                                            NR27=msi_list['NR27'], BAT25=msi_list['BAT25'], BAT26=msi_list['BAT26'],
                                            MONO27=msi_list['MONO27'], PentaC=msi_list['PentaC'],
                                            PentaD=msi_list['PentaD'],reportStable=reportStable)
                    print('msi_info', msi_info)
                    tumor_infiltrating = None
                else:
                    tumor_infiltrating = None
                    msi_info = None
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
                resp.body = return_info
            else:
                return_info = '{"success":false, "info": "Report generation failure!" }'
                resp.body = return_info
        else:
            resp.body = '{"success":false, "info": "Report generation failure!" }'

app.add_route("/reportinfo", reportInfo())

httpd = simple_server.make_server("192.168.1.144", 8100, app)
httpd.serve_forever()

# app_flask.run(host='192.168.1.144', port=8100)
