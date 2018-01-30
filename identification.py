# -*-coding: utf-8-*-

import falcon, json, re
from wsgiref import simple_server
import pymysql
from login_api import *
from config import *
import gunicorn
from query_project import *
import glob


app = falcon.API()
app.req_options.auto_parse_form_urlencoded = True
app.req_options.keep_blank_qs_values = True

class Identification(object):
    def __init__(self):
        self.id = []

    def on_post(self, req, resp):
        data = req.params
        """  firstName: '', lastName: '', passWord: '', email: '', liteLab: '', passWord2: '', email2: '', institutionName: """

        # tmp = data["userName"].decode('unicode_escape')
        # tmp = data["userName"]
        # username = tmp.encode('raw_unicode_escape')
        username = data['userName']
        print(username)
        useridcard = data["userIdCard"]
        usertel = data["userTel"]
        db = Mysql(table_name="GLORIA_MYSQL")
        sql = """select * from sample_mx where SUBJECT_SFZ=\"%s\" and SUBJECT_NAME=\"%s\" and S_TEL=\"%s\";""" % (useridcard, username, usertel)
        data2 = db.fetch_all(sql)
        resp.status = falcon.HTTP_200
        resp._headers["Access-Control-Allow-Origin"] = "*"
        if not data2:
            sql = """select * from sample_mx where SUBJECT_NAME=\"%s\" and SUBJECT_SFZ=\"%s\";""" % (username, useridcard)
            data2 = db.fetch_all(sql)
            if not data2:
                    sql = """select * from sample_mx where SUBJECT_NAME=\"%s\" and S_TEL=\"%s\";""" % (username, usertel)
                    data2 = db.fetch_all(sql)
                    if not data2:
                        sql = """select * from sample_mx where SUBJECT_NAME=\"%s\";""" % username
                        data2 = db.fetch_all(sql)
                        if not data2:
                            return_info = '{"success":false, "info": "Identification wrong!" }'
                            resp.body = return_info
                            db.commit()
                        else:
                            self.id = ["username"]
                    else:
                        self.id = ["username", "usertel"]
            else:
                self.id = ["username", "useridcard"]
        else:
            self.id = ["username", "useridcard", "usertel"]
        db_identification = Mysql(table_name="WECHAT_MYSQL")
        username_decode = username.encode('raw_unicode_escape')
        username_encode = username_decode.decode('unicode_escape')
        print(username_decode)
        print(username_encode)
        sql = """select * from identification where userName=\"%s\" and userIdCard=\"%s\" and userTel=\"%s\";""" % (username, useridcard, usertel)
        out = db_identification.fetch_one(sql)
        if not out:
            sql = """ insert into identification values(UUID(), \"%s\", \"%s\",\"%s\", now()); """ % (username_encode, useridcard, usertel)
            db_identification.execute(sql)
            db_identification.commit()
        return_info = '{"success":true, "info": "Identification success!" }'
        resp.body = return_info
        db.commit()
        # else:
        #     sql = """select * from sample_mx where SUBJECT_NAME=\"%s\" and S_TEL=\"%s\";""" % (username, usertel)
        #     data = db.fetch_one(sql)
        #     if data:
        #         if data[52] != useridcard:
        #             return_info = '{"success":false, "info": "userIdCard wrong!" }'
        #     else:
        #         return_info = '{"success":false, "info": "Identification wrong!" }'
        #     # return_info = '{"success":false, "info": "Identification wrong!" }'




class Report(object):
    def on_post(self, req, resp):
        data = req.params
        username = data["userName"]
        useridcard = data["userIdCard"]
        usertel = data["userTel"]
        size = int(data['size'])
        page = int(data['page'])
        queryinfo = QUERY(username=username, useridcard=useridcard, usertel=usertel)
        obj = []
        resp.status = falcon.HTTP_200
        resp._headers["Access-Control-Allow-Origin"] = "*"
        for keys, values in queryinfo.items():
            range_tmp = range(len(values))
            mod =len(values) % size  #取余
            reminder = int(len(values)/size)
            if mod != 0:
                if page == 0:
                    range_id = range_tmp[0:size]
                elif page == (reminder-1):
                        range_id = range_tmp[(size * page):(len(values)+1)]
                else:
                        range_id = range_tmp[(size*page):(size*(page+1))]
            else:
                range_id = range_tmp[(size * page):(size * (page + 1))]
            for index in range_id:
                values_info = values[index]
                values1 = values_info["info"]
                step = {}
                "type为True表示pipeline有5个步骤, type为False表示pipeline有4个步骤"
                if re.search('NGS', values_info["type"]):
                    step["type"] = True
                else:
                    step["type"] = False
                # tmp = b'%s' % keys1
                # reportName = tmp.decode('utf-8')
                step["reportName"] = values_info["project"]
                step["reportId"] = values_info["reportId"]
                if step["type"]:
                    if values1["report"]:
                        step["step"] = 4
                    elif values1["analysis"]:
                        step["step"] = 3
                    elif values1["outmanager"] or values1["datapcr"] or values1["ngs"] or values1["pcr"]:
                        step["step"] = 2
                    elif values1["extractrqc"]:
                        step["step"] = 1
                    else:
                        step["step"] = 0
                else:
                    if values1["report"]:
                        step["step"] = 3
                    elif values1["outmanager"] or values1["datapcr"] or values1["pcr"]:
                        step["step"] = 2
                    elif values1["extractrqc"]:
                        step["step"] = 1
                    else:
                        step["step"] = 0
                if step["type"]:
                    if step["step"] == 4:
                        step["end"] = True
                    else:
                        step["end"] = False
                else:
                    if step["step"] == 3:
                        step['end'] = True
                    else:
                        step["end"] = False
                obj.append(step)
        if obj:
            length = len(obj)
            #暂时先把参数end改成这个样子,此处是有一个bug存在的
            return_info = {"success":True, "obj": obj, "length": str(length)}
        else:
            return_info = {"success":False, "obj": "wrong!" }
        print(type(return_info))
        print(type(obj))
        print(json.dumps(return_info, ensure_ascii=False))
        resp.body = json.dumps(return_info, ensure_ascii=False)


class GetReport(object):
    def on_post(self, req, resp):
        data = req.params
        project_id = data["reportId"]
        db = Mysql(table_name="GLORIA_MYSQL")
        resp.status = falcon.HTTP_200
        resp._headers["Access-Control-Allow-Origin"] = "*"
        # select * from sample_qc qc，sample_mx mx where qc.old_sample_mx_id=mx.id and mx.S_MCODE='YHT1730028';
        sql = "select * from report_info where RP_SAMPLE_ID=\"%s\";" % project_id
        db_out_tmp = db.fetch_all(sql)
        db_out = None
        # db_out = db.fetch_one(sql)
        # 加了小的限制条件 不知道会不会报错
        print("db_out_tmp", db_out_tmp)
        if db_out_tmp:
            for i in db_out_tmp:
                if i[11]:
                    if 'gDNA' in i[11]:
                        continue
                    else:
                        db_out = i
                        break
                else:
                    continue
            if not db_out:
                db_out = db.fetch_one(sql)
            if not db_out:
                return_info = {"success": False, "obj": "报告正在生成中!"}
            else:
                # if db_out:
                path = "/home/khl/web/wechat_data"  #文件存放的路径
                new_path = "http://192.168.1.144:8097"
                from collections import defaultdict
                import urllib
                print('db_out', db_out)
                png_list = []
                if db_out:
                    report_name = db_out[11]
                    if report_name and 'pdf' in report_name:
                        png_path = path+"/"+report_name.split(".pdf")[0]
                        if os.path.exists(png_path):
                            png_report_name_list = os.listdir(png_path)
                            if png_report_name_list:
                                png_num = len(os.listdir(png_path))
                                # png_tmp_list = glob.glob("%s/%s*.png" % (png_path, report_name.split(".pdf")[0]))
                                for i in range(png_num):
                                    png_tmp = os.path.join(png_path, "%s-%s.png" % (report_name.split(".pdf")[0], str(i)))
                                    png_list.append({"url":png_tmp.replace(path, new_path)})
                                    return_info = {"success":True, "obj": png_list}
                            else:
                                return_info = {"success": False, "obj": "报告正在生成中!"}
                        else:
                            return_info = {"success": False, "obj": "报告正在生成中!"}
                    else:
                        return_info = {"success": False, "obj": "报告正在生成中!"}
                else:
                    return_info = {"success": False, "obj": "报告正在生成中!"}
        else:
            return_info = {"success": False, "obj": "报告正在生成中!"}
        resp.body = json.dumps(return_info, ensure_ascii=False)


app.add_route("/identification", Identification())
app.add_route("/report", Report())
app.add_route("/getreport", GetReport())


# httpd = simple_server.make_server("127.0.0.1", 8123, app)
# httpd.serve_forever()
