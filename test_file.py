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

class workflow(object):
    def on_post(self, req, resp):
        params = req.params
        user_name = params["userName"]
        size = int(params["size"])
        page = int(params['page'])
        queryversion = params["version"]
        filter = params["filter"]
        i = 0
        resp.status = falcon.HTTP_200
        resp._headers["Access-Control-Allow-Origin"] = "*"
        outversion = []  # 列表，嵌套字典
        totalversion = []  # 列表 存储unique version信息
        mysql = Mysql(table_name="MYSQL")
        sql = "select * from login where userName=\"%s\";" % user_name
        data = mysql.fetch_one(sql)
        result = {}
        if data:
            usernameid = data[-1]
            db = Mysql(table_name="REPORT_MYSQL")
            """{title: '分析名称',key: 'analysisName'},
                {title: '样本名称',key: 'sampleName'},
                {title: '流程名称',key: 'flowName'},
                {title: '版本',key: 'version'},
                {title: '日期',key: 'date'},
                {title: '状态',key: 'status'},"""
            sql = "select * from report where userNameId=\"%s\";" % usernameid
            info = []
            data = db.fetch_all(sql)
            print(len(data))
            # print(len(data))
            if data:
                for tmp in data:
                    print(tmp[0])
                    analysisName=tmp[2]
                    sampleName=tmp[3]
                    flowName=tmp[4]
                    projectid = tmp[1]
                    sql = "select * from projectName where ID=\"%s\";" % projectid
                    projectinfo=db.fetch_one(sql)
                    if projectinfo:
                        version = projectinfo[3]
                        date = tmp[5]
                        status = tmp[6]
                        oldpdfpath = tmp[-3]
                        oldpdfurl = tmp[-2]
                        pdfpath = oldpdfpath.replace('/home/khl/web/dist', "http://192.168.1.144:8096")
                        pdfurl = oldpdfurl.replace('/home/khl/web/dist', "http://192.168.1.144:8096")
                        if version not in totalversion:
                            tmp_data = {"key": version, "value": version}
                            totalversion.append(version)
                            outversion.append(tmp_data)
                            i += 1
                        if filter and queryversion:
                            if ((filter in analysisName  or filter in sampleName) and version == queryversion):
                                aaaa = {"analysisName": analysisName, "sampleName":sampleName ,
                                        "flowName": flowName, "version": version, "date": date, "status": status,
                                        "pdfpath": pdfpath, "pdfurl": pdfurl, "uniqueId": tmp[0]}
                                info.append(aaaa)
                        elif filter and not queryversion:
                            if filter in analysisName  or filter in sampleName:
                                aaaa = {"analysisName": analysisName, "sampleName": sampleName,
                                        "flowName": flowName, "version": version, "date": date, "status": status,
                                        "pdfpath": pdfpath, "pdfurl": pdfurl, "uniqueId": tmp[0]}
                                info.append(aaaa)
                        elif not filter and queryversion:
                            if version == queryversion:
                                aaaa = {"analysisName": analysisName, "sampleName": sampleName,
                                        "flowName": flowName, "version": version, "date": date, "status": status,
                                        "pdfpath": pdfpath, "pdfurl": pdfurl, "uniqueId": tmp[0]}
                                info.append(aaaa)
                        elif not filter and not queryversion:
                            aaaa = {"analysisName": analysisName, "sampleName": sampleName,
                                    "flowName": flowName, "version": version, "date": date, "status": status,
                                    "pdfpath": pdfpath, "pdfurl": pdfurl, "uniqueId": tmp[0]}
                            print(aaaa)
                            info.append(aaaa)
                    else:
                        result["success"] = False
                        result["info"] = "Report failure!"
                        resp.body = json.dumps(result, ensure_ascii=False)
                        # resp.body = '{"success":false, "info": "Report failure!" }'
                print(type(info))
                range_tmp = range(len(info))
                mod = len(info) % size  # 取余
                reminder = int(len(info) / size)
                if mod != 0:
                    if page == 1:
                        range_id = range_tmp[0:size]
                    elif page == (reminder - 1):
                        range_id = range_tmp[(size * (page - 1)):len(info)]
                    else:
                        range_id = range_tmp[(size * (page - 1)):(size * page)]
                else:
                    range_id = range_tmp[(size * (page - 1)):(size * page)]
                out_json = []
                for index in range_id:
                    out_json.append(info[index])
                result["success"] = True
                result["info"] = out_json
                result["length"] = str(len(out_json))
                result["total"] = str(len(info))
                result["totalVersion"] = outversion
                resp.body = json.dumps(result, ensure_ascii=False)
            else:
                result["success"] = False
                result["info"] = "Report failure!"
                resp.body = json.dumps(result, ensure_ascii=False)

def test1():
    # params = {"sampleCode":"YHB1720517","title":"普晟和-肿瘤靶向化疗用药83基因检测",
    #           "reportName":"mnmnmn","userName":"I"}
    "YHB1721079"
    params = {"sampleCode":"YHB1721079","title":"普晟安-肿瘤全外显子组检测",
              "reportName":"wes","userName":"I"}
    # params = {"sampleCode":"YHB1720537","title":"普晟朗-肺癌靶向用药15基因检测",
    #           "reportName":"mnmnmn","userName":"I"}
    sample_code = params["sampleCode"]
    project = params["title"]
    report_name = params["reportName"]
    user_name = params["userName"]
    mysql = Mysql(table_name="MYSQL")
    sql = "select * from login where userName=\"%s\";" % user_name
    data1 = mysql.fetch_one(sql)
    if data1:
        usernameid = data1[-1]
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
        sql = "select * from report where sampleName=\"%s\";" % sample_code
        data_batch = db.fetch_all(sql)
        print(data_batch)
        if data_batch:
            for data in data_batch:
                tmp_pdfpath = data[-2]
                tmp_pdfurl = data[-1]
                print(tmp_pdfpath,tmp_pdfurl)
                print(os.path.exists(tmp_pdfpath))
                print('hahahahah')
                new_pdfpath = os.path.join(out_path, report_name + ".doc")
                new_pdfurl = os.path.join(out_path, report_name + ".pdf")

                if os.path.exists(tmp_pdfpath):
                    print("cp %s %s" % (tmp_pdfpath, new_pdfpath))
                    os.system("cp %s %s" % (tmp_pdfpath, new_pdfpath))
                    if os.path.exists(tmp_pdfurl):
                        os.system("cp %s %s" % (tmp_pdfurl, new_pdfurl))
                    sql_tmp = "insert into report(ID,templateID,analysisName,sampleName,workflowName,DATETIME,STATUS,path,reportName,pdfPath,pdfUrl,userNameId) values(UUID(), \"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\")"
                    sql = sql_tmp % (
                        data[1], data[2], data[3], data[4], datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                        data[6], data[7], report_name, new_pdfpath, new_pdfurl, usernameid)
                    print(sql)
                    db.execute(sql)
                    db.commit()
                    return_info = '{"success":true, "info": "Report generation success!" }'
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
            sql = "select * from template where projectId=\"%s\";" % projectname_id
            data = db.fetch_one(sql)
            if data:
                xml_path = os.path.join(data[-1], data[-2])
                print('xml_path', xml_path)
                # xml_path = "/home/khl/web/word/15geneBlood.xml"
                pdfpath, pdfurl = templateword(xml_path, out_path, report_name, sample_code, project_name, usernameid,
                                               type)
                return_info = '{"success":true, "info": "Report generation success!" }'
            else:
                return_info = '{"success":false, "info": "Report generation failure!" }'
    else:
        print("error!")

def main():
    info = ['1']
    size = 10
    page = 0
    range_tmp = range(len(info))
    mod = len(info) % size  # 取余
    reminder = int(len(info) / size)
    if mod != 0:
        if page == 1:
            range_id = range_tmp[0:size]
        elif page == (reminder - 1):
            range_id = range_tmp[(size * (page - 1)):len(info)]
        else:
            range_id = range_tmp[(size * (page - 1)):(size * page)]
    else:
        range_id = range_tmp[(size * (page - 1)):(size * page)]

    print(range_id)

def test2():
    db = Mysql(table_name="MYSQL")
    sql = "select * from register;"
    data = db.fetch_all(sql)
    print(data)
    for i in range(len(data)):
        sql_tmp = "insert into register1 values(\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\")"
        sql = sql_tmp % (data[i][0],data[i][1],data[i][2],data[i][3],data[i][4],data[i][5],data[i][6])
        db.execute(sql)
    db.commit()

if __name__ == "__main__":
    # main()
    test2()