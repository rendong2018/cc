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

class analysis(object):
    def on_post(self, req, resp):
        params = req.params
        result = {}
        user_name = params["userName"]
        size = int(params["size"])
        page = int(params['page'])
        queryversion = params["version"]
        filter = params["filter"]
        ngs_type = params["type"]   # 添加过滤参数  all ngs noNgs
        db = Mysql(table_name="REPORT_MYSQL")
        sql = "select * from projectName;"
        outversion = []  # 列表，嵌套字典
        totalversion = []  # 列表 存储unique version信息
        i = 0
        data=db.fetch_all(sql)
        resp.status = falcon.HTTP_200
        resp._headers["Access-Control-Allow-Origin"] = "*"
        print('data', data)
        if data:
            result["success"] = True
            info = []
            for d in data:
                description = d[1]
                application = d[1]
                version = d[-4]
                date = d[-5]
                if version not in totalversion:
                    if ngs_type == "ngs" or ngs_type == "noNgs":
                        if d[-2] == ngs_type:
                            tmp = {"key":version,"value":version}
                            totalversion.append(version)
                            outversion.append(tmp)
                            i += 1
                        else:
                            continue
                    else:
                        tmp = {"key": version, "value": version}
                        totalversion.append(version)
                        outversion.append(tmp)
                        i += 1
                if filter and queryversion:
                    if filter in application and version == queryversion:
                        if ngs_type == "ngs" or ngs_type == "noNgs":
                            if ngs_type == d[-2]:
                                info_tmp = {"description":description,"application":application,
                                    "version":version,"date":date}
                                info.append(info_tmp)
                            else:
                                continue
                        else:
                            info_tmp = {"description": description, "application": application,
                                        "version": version, "date": date}
                            info.append(info_tmp)
                elif filter and not queryversion:
                    if filter in application:
                        if ngs_type == "ngs" or ngs_type == "noNgs":
                            if ngs_type == d[-2]:
                                info_tmp = {"description": description, "application": application,
                                            "version": version, "date": date}
                                info.append(info_tmp)
                            else:
                                continue
                        else:
                            info_tmp = {"description": description, "application": application,
                                        "version": version, "date": date}
                            info.append(info_tmp)
                elif not filter and queryversion:
                    if version == queryversion:
                        if ngs_type == "ngs" or ngs_type == "noNgs":
                            if ngs_type == d[-2]:
                                info_tmp = {"description": description, "application": application,
                                            "version": version, "date": date}
                                info.append(info_tmp)
                            else:
                                continue
                        else:
                            info_tmp = {"description": description, "application": application,
                                        "version": version, "date": date}
                            info.append(info_tmp)
                elif not filter and not queryversion:
                    if ngs_type == "ngs" or ngs_type == "noNgs":
                        if ngs_type == d[-2]:
                            info_tmp = {"description": description, "application": application,
                                        "version": version, "date": date}
                            info.append(info_tmp)
                        else:
                            continue
                    else:
                        info_tmp = {"description": description, "application": application,
                                    "version": version, "date": date}
                        info.append(info_tmp)
            print('info', info)
            range_tmp = range(len(info))
            mod = len(info) % size  # 取余
            reminder = int(len(info) / size)
            if mod != 0:
                if page == 1:
                    range_id = range_tmp[0:size]
                elif page == (reminder - 1):
                    range_id = range_tmp[(size * (page - 1)):len(info)]
                else:
                    range_id = range_tmp[(size*page):mod]
                    #range_id = range_tmp[(size * (page - 1)):(size * page)]
            else:
                range_id = range_tmp[(size * (page - 1)):(size * page)]
            out_json = []
            for index in range_id:
                out_json.append(info[index])
            result["info"] = out_json
            result["length"] = str(len(out_json))
            result["total"] = str(len(info))
            result["totalVersion"] = outversion
            resp.body = json.dumps(result, ensure_ascii=False)
        else:
            result["success"] = Falseapp.add_route("/analysis", analysis())

httpd = simple_server.make_server("192.168.1.144", 8100, app)
httpd.serve_forever()
            result["info"] = "Report failure!"
            resp.body = json.dumps(result, ensure_ascii=False)


