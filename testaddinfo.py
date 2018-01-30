# -*-coding: utf-8-*-

import falcon, json, sys
from wsgiref import simple_server
import pymysql
from login_api import *
from config import *
from query_project import *
from docx import Document
from docx.shared import Inches
from query_sample_info import *
sys.getdefaultencoding()
import datetime
from addinfo import templateword


app = falcon.API()
app.req_options.auto_parse_form_urlencoded = True
app.req_options.keep_blank_qs_values = True

class reportInfo(object):
    def on_post(self, req, resp):
        params = req.params
        sample_code = params["sampleCode"]
        project = params["title"]
        report_name = params["reportName"]
        user_name = params["userName"]
        mysql = Mysql(table_name="MYSQL")
        sql = "select * from login where userName=\"%s\";" % user_name
        data1 = mysql.fetch_one(sql)
        if data1:
            usernameid = data1[-1]
            print(usernameid)
            # out_path = "/home/khl/web/dist/downloads/tmp"
            out_path = "C://inetpub/wwwroot"
            """这个地方存在bug还没有改"""
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

            db = Mysql(table_name="REPORT_MYSQL")
            sql = "select * from report where sampleName=\"%s\";" % sample_code
            data = db.fetch_one(sql)
            if data:
                tmp_pdfpath = data[-2]
                tmp_pdfurl = data[-1]
                new_pdfpath = os.path.join(out_path, report_name+".doc")
                new_pdfurl = os.path.join(out_path, report_name+".pdf")
                if os.path.exists(new_pdfpath):
                    os.remove(new_pdfpath)
                if os.path.exists(new_pdfurl):
                    os.remove(new_pdfurl)
                os.system("cp %s %s" % (tmp_pdfpath, new_pdfpath))
                os.system("cp %s %s" % (tmp_pdfurl, new_pdfurl))
                sql_tmp = "insert into report values(UUID(), \"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\")"
                #
                sql = sql_tmp % (data[1], data[2],data[3],data[4],datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),data[6],data[7],report_name,new_pdfpath,new_pdfurl,usernameid)
                print(sql)
                db.execute(sql)
                db.commit()
                return_info = '{"success":true, "info": "Report generation success!" }'
                resp.body = return_info
            else:
                sql = "select * from projectName where projectName=\"%s\" and type = \"%s\";" % (project_name, type)
                print(sql)
                data = db.fetch_one(sql)
                projectname_id = data[0]
                sql = "select * from template where projectId=\"%s\";" % projectname_id
                data = db.fetch_one(sql)
                if data:
                    # xml_path = os.path.join(data[-1], data[-2])
                    # print('xml_path', xml_path)
                    # xml_path = "/home/khl/web/word/15geneBlood.xml"
                    xml_path = "E:\\15geneBlood.xml"
                    pdfpath, pdfurl = templateword(xml_path, out_path, report_name, sample_code, project_name, usernameid, type)
                    return_info = '{"success":true, "info": "Report generation success!" }'
                    resp.body = return_info
                else:
                    return_info = '{"success":false, "info": "Report generation failure!" }'
                    resp.body = return_info
        else:
            resp.body = '{"success":false, "info": "Report generation failure!" }'
