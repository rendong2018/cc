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

class deleteWorkflow(object):
    def on_post(self, req, resp):
        params = req.params
        uniqueid = params["id"]
        resp.status = falcon.HTTP_200
        resp._headers["Access-Control-Allow-Origin"] = "*"
        db = Mysql(table_name="REPORT_MYSQL")
        sql = "select * from report where ID=\"%s\";" % uniqueid
        data = db.fetch_one(sql)
        if data:
            sql = "delete from report where ID=\"%s\"" % uniqueid
            try:
                db.execute(sql)
                db.commit()
                result = {"success":True,"info":"删除成功"}
            except Exception:
                result = {"success":True,"info":"删除失败"}
        else:
            result = {"success": True, "info": "删除成功"}
        resp.body = json.dumps(result, ensure_ascii=False)

app.add_route("/delete", deleteWorkflow())

httpd = simple_server.make_server("192.168.1.144", 8100, app)
httpd.serve_forever()



