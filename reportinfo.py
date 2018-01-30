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
        workflow_name = params["workflowName"]
        mysql = Mysql(table_name="MYSQL")
        sql = "select * from login where userName=\"%s\";" % user_name
        data1 = mysql.fetch_one(sql)
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

            db = Mysql(table_name="REPORT_MYSQL")
            sql = "select * from report where sampleName=\"%s\";" % sample_code
            data_batch = db.fetch_all(sql)
            if data_batch:
                for data in data_batch:
                    tmp_pdfpath = data[-2]
                    tmp_pdfurl = data[-1]
                    new_pdfpath = os.path.join(out_path, report_name+".doc")
                    new_pdfurl = os.path.join(out_path, report_name+".pdf")
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
                        resp.body = return_info
                    else:
                        continue
            else:
                if type:
                    sql = "select * from projectName where projectName=\"%s\" and type = \"%s\";" % (project_name, type)
                else:
                    sql = "select * from projectName where projectName=\"%s\";" % project_name
                print(sql)
                data = db.fetch_one(sql)
                projectname_id = data[0]
                analysis_name = data[1]
                sql = "select * from template where projectId=\"%s\";" % projectname_id
                data = db.fetch_one(sql)
                if data:
                    xml_path = os.path.join(data[-1], data[-2])
                    print('xml_path', xml_path)
                    # xml_path = "/home/khl/web/word/15geneBlood.xml"
                    pdfpath, pdfurl = templateword(xml_path, out_path, report_name, sample_code, project_name, usernameid, type)
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

#-*-coding: utf-8 -*-

import pymysql
from config import Config

class Mysql(object):
    def __init__(self, table_name):
        self._config = Config(table_name=table_name)
        self._con = self.__get_con()
        print(self._con)
        self._cursor = self._con.cursor()

    def __get_con(self):
        print(type(self._config.host))
        print(self._config.host, self._config.user, self._config.password, self._config.db_name, self._config.port)
        db = pymysql.connect(host=self._config.host, user=self._config.user, passwd=self._config.password,
                             db=self._config.db_name, port=int(self._config.port), charset="utf8",  use_unicode=True)
        return db

    # def __del__(self):
    #     # self._cursor.close()
    #     self._con.close()

    def cursor(self):
        return self._cursor

    def commit(self):
        try:
            self._con.commit()
        except Exception as e:
            print(e)
            self._con.rollback()
        finally:
            self._con.close()

    def fetch_one(self, sql, params=None):
        """params 参数暂时先用不上"""
        try:
            self._cursor.execute(sql)
            result = self._cursor.fetchone()
            if result:
                return result
            else:
                result = False
                return result
        except Exception as e:
            raise(e)

    def fetch_many(self,sql):
        try:
            self._cursor.execute(sql)
            results = self._cursor.fetchmany()
            return results
        except Exception as e:
            raise(e)

    def fetch_all(self,sql):
        try:
            self._cursor.execute(sql)
            results = self._cursor.fetchall()
            return results
        except Exception as e:
            raise(e)

    def execute(self, sql):
        print(sql)

        self._cursor.execute(sql)
        # try:
        #     self._cursor.execute(sql)
        # except Exception as e:
        #     raise(e)

