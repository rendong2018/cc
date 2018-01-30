#!/usr/bin/env python
# coding=utf-8

import os,json, glob
from flask_cors import *
from flask import Flask, request, render_template as rt
import subprocess
from multiprocessing import *
import datetime
from login_api import *
from config import *

app_flask = Flask(__name__)
CORS(app_flask, supports_credentials=True)

@app_flask.route('/login', methods=['POST'])
def Login():
    if request.method == 'POST':
        """  firstName: '', lastName: '', passWord: '', email: '', liteLab: '', passWord2: '', email2: '', institutionName: """
        username = request.form.get("userName")
        password = request.form.get("passWord")
        db = Mysql(table_name="MYSQL")
        sql = """select * from register where email = \"%s\";""" % username
        data2 = db.fetch_one(sql)
        print(data2)
        # 跨域问题没有设置

        # resp.status = falcon.HTTP_200
        # resp._headers["Access-Control-Allow-Origin"] = "*"
        if data2:
            password_sql = data2[3]
            if password == password_sql:
                return_info = {"success":True, "info": "Log in success!" }
            else:
                return_info = {"success":False, "info": "Wrong passWord!" }
            # resp.body = return_info
        else:
            return_info= {"success":False, "info": "Wrong userName!"}
        db.commit()
        return json.dumps(return_info, ensure_ascii=False)

@app_flask.route('/register', methods=['POST'])
def Register():
        """  firstName: '', lastName: '', passWord: '', email: '', liteLab: '', passWord2: '', email2: '', institutionName: """
        firstName = request.form.get("firstName")
        lastName = request.form.get("lastName")
        passWord = request.form.get("passWord")
        email = request.form.get("email")
        liteLab = request.form.get("liteLab")
        passWord2 = request.form.get("passWord2")
        email2 = request.form.get("email2")
        institutionName = request.form.get("institutionName")
        print(firstName)
        db = Mysql(table_name="MYSQL")
        sql = """select * from register where email = \"%s\";""" % email
        data2 = db.fetch_one(sql)
        print(data2)
        # resp.status = falcon.HTTP_200
        # resp._headers["Access-Control-Allow-Origin"] = "*"
        if data2:
            return_info = {"success":False, "info":"%s exists!"%email }
        else:
            sql = ' insert into register values(UUID(), \"%s\", \"%s\", \"%s\",\"%s\", \"%s\", \"%s\"); ' % (firstName, lastName, passWord, email, liteLab, institutionName)
            db.execute(sql)
            sql = "select * from register where passWord=\"%s\" and email=\"%s\";" % (passWord, email)
            out = db.fetch_one(sql)
            register_id = out[0]
            try:
                sql_login = "insert into login values(\"%s\",\"%s\", UUID(), \"%s\");" % (email, passWord, register_id)
                db.execute(sql_login)
            except Exception:
                sql_login_create = "create table if not exists login (ID VARCHAR(60), REGISTER_ID VARCHAR(60), userName VARCHAR(20), passWord VARCHAR(20))DEFAULT CHARSET = UTF8;"
                db.execute(sql_login_create)
                sql_login = "insert into login values(\"%s\",\"%s\", UUID(), \"%s\");" % (email, passWord, register_id)
                db.execute(sql_login)
            return_info = {"success":True, "info":data}
        db.commit()
        return json.dumps(return_info, ensure_ascii=False)

@app_flask.route('/sample', methods=['POST'])
def query_sample():
        project_info = str(request.form.get("project"))
        sampletype = str(request.form.get("sampleType"))
        samplename = str(request.form.get("sampleName"))
        username = request.form.get("userName")
        size = int(request.form.get("size"))
        page = int(request.form.get('page'))

        # resp.status = falcon.HTTP_200
        # resp._headers["Access-Control-Allow-Origin"] = "*"

        sample_mysql = Mysql(table_name="PC_SAMPLE")
        register_mysql = Mysql(table_name="MYSQL")
        sql = "select * from register where email=\"%s\";" %  username
        out = register_mysql.fetch_one(sql)
        register_id = out[0]
        sql = "select * from sample where REGISTER_ID=\"%s\";" % register_id
        out_data = sample_mysql.fetch_all(sql)
        data = []
        if out_data:
            id = 0
            for out1 in out_data:
                sample_name = out1[2]
                sample_id = sample_name
                sample_detail = out1[3]
                project = out1[-5]
                sample_type = out1[-4]
                role = out1[-3]
                imported_by = out1[-2]
                imported_on = out1[-1]
                print(samplename == sample_id, project_info == project, sampletype == sample_type)
                if project_info and samplename and sampletype:
                    if samplename == sample_id and project_info == project and sampletype == sample_type:
                        return_json = {"sampleName": sample_id, "sampleDetail": sample_detail, "project": project,
                                       "sampleType": sample_type, "role": role, "importedBy": imported_by,
                                       "importedOn": imported_on}
                    else:
                        continue
                elif project_info and samplename and not sampletype:
                    if project_info == project and sample_id==samplename:
                        return_json = {"sampleName": sample_id, "sampleDetail": sample_detail, "project": project,
                                       "sampleType": sample_type, "role": role, "importedBy": imported_by,
                                       "importedOn": imported_on}
                    else:
                        continue
                elif project_info and not samplename and not sampletype:
                    if project_info == project:
                        return_json = {"sampleName": sample_id, "sampleDetail": sample_detail, "project": project,
                                       "sampleType": sample_type, "role": role, "importedBy": imported_by,
                                       "importedOn": imported_on}
                    else:
                        continue
                elif not project_info and samplename and sampletype:
                    if sample_id == samplename and sampletype == sample_type:
                        return_json = {"sampleName": sample_id, "sampleDetail": sample_detail, "project": project,
                                       "sampleType": sample_type, "role": role, "importedBy": imported_by,
                                       "importedOn": imported_on}
                    else:
                        continue
                elif not project_info and not samplename and sampletype:
                    if sampletype == sample_type:
                        return_json = {"sampleName": sample_id, "sampleDetail": sample_detail, "project": project,
                                       "sampleType": sample_type, "role": role, "importedBy": imported_by,
                                       "importedOn": imported_on}
                    else:
                        continue
                elif not project_info and samplename and not sampletype:
                    if sample_id == samplename:
                        return_json = {"sampleName": sample_id, "sampleDetail": sample_detail, "project": project,
                                       "sampleType": sample_type, "role": role, "importedBy": imported_by,
                                        "importedOn": imported_on}
                    else:
                        continue
                elif project_info and not samplename and sampletype:
                    if project_info == project and sampletype == sample_type:
                        return_json = {"sampleName": sample_id, "sampleDetail": sample_detail, "project": project,
                                       "sampleType": sample_type, "role": role, "importedBy": imported_by,
                                       "importedOn": imported_on}
                    else:
                        continue
                elif not project_info and not samplename and not sampletype:
                    return_json = {"sampleName": sample_id, "sampleDetail": sample_detail, "project": project,
                                   "sampleType": sample_type, "role": role, "importedBy": imported_by,
                                   "importedOn": imported_on}
                data.append(return_json)
            range_tmp = range(len(data))
            mod = len(data) % size  # 取余
            reminder = int(len(data) / size)
            if mod != 0:
                if page == 1:
                    range_id = range_tmp[0:size]
                elif page == (reminder - 1):
                    range_id = range_tmp[(size * (page-1)):len(values)]
                else:
                    range_id = range_tmp[(size * (page-1)):(size * page)]
            else:
                range_id = range_tmp[(size * (page-1)):(size * page)]
            out_json = []
            for index in range_id:
                out_json.append(data[index])
            length = str(len(out_json))
            total = str(len(data))
            # out_json可能需要用json.dumps包装一下
            return_info = {"success":True, "info": out_json, "length":length, "total":total}
        else:
            return_info = {"success":False, "info": "wrong!" }
        sample_mysql.commit()
        register_mysql.commit()
        return json.dumps(return_info, ensure_ascii=False)

@app_flask.route('/project', methods=['POST'])
def project_name():
        type = request.form.get("type")   # ngs 和 noNgs类型判断
        version = request.form.get("version")   # 版本号判断
        db = Mysql(table_name="REPORT_MYSQL")
        sql = """select * from projectName;"""
        project_tmp = db.fetch_all(sql)
        data = []
        total_version = []
        reserved_project = ["普晟惠-PD-L1及CD8蛋白表达检测", "普晟惠-MSI微卫星不稳定性检测","普晟畅-结直肠癌靶向用药12基因检测","普晟朗-肺癌靶向用药15基因检测", "普晟和-肿瘤靶向化疗用药83基因检测","普益康-肿瘤个体化诊疗620基因检测"]
        if type == "非ngs":
            filter_type = "noNgs"
        else:
            filter_type = type
        if project_tmp:
            for d in project_tmp:
                if d[1] in reserved_project and filter_type == d[5]:
                    if not version:
                        tmp = {"title": d[1], "text": "", "url": "",'type':d[5], "version":d[3]}
                        data.append(tmp)
                    elif version == d[3]:
                        tmp = {"title": d[1], "text": "", "url": "", 'type': d[5], "version": d[3]}
                        data.append(tmp)
                    if d[3] not in total_version:
                        total_version.append(d[3])
        # resp.status = falcon.HTTP_200
        # resp._headers["Access-Control-Allow-Origin"] = "*"
        return_info = {"success":True, "info": data, "version":total_version}
        return json.dumps(return_info, ensure_ascii=False)

@app_flask.route('/sampleinfo', methods=['POST'])
def GetSampleInfo():
        """根据样本的编写获得样本的其他信息"""
        samplename = request.form.get("sampleName")
        db = Mysql(table_name="GLORIA_MYSQL")
        sql = """select * from sample_mx where S_MCODE = \"%s\";""" % samplename
        data = db.fetch_all(sql)
        # resp.status = falcon.HTTP_200
        # resp._headers["Access-Control-Allow-Origin"] = "*"
        if data:
            result = {"success":True, "info": "样本存在!" }
        else:
            result = {"success":False, "info": "样本不存在!" }
        # resp.body = result
        return json.dumps(return_info, ensure_ascii=False)


@app_flask.route('/reportinfo', methods=['POST'])
def reportInfo():
        sample_code = request.form.get("sampleCode")   # 样本编号
        project = request.form.get("title")  # 报告模板
        report_name = request.form.get("reportName")   # 文件名
        user_name = request.form.get("userName")
        workflow_name = request.form.get("workflowName")  # 报告结果名称
        tumorInfiltrating = request.form.get("tumorInfiltrating")
        pd28Tumor = request.form.get("pd28Tumor")
        pd28Lymph = request.form.get("pd28Lymph")
        pd142Tumor = request.form.get("pd142Tumor")
        pd142Lymph = request.form.get("pd142Lymph")
        cd8 = request.form.get("cd8")
        tumorPercent = request.form.get("tumorPercent")
        tumorLevel = request.form.get("tumorLevel")
        msiStable = request.form.get("msiStable")
        uid= request.form.get('uid')
        filenameLeft = request.form.get('filenameLeft')
        filenameRight = request.form.get('filenameRight')

        msi_list = {"NR21":None,"NR24":None,"NR27":None,
                    "BAT25":None,"BAT26":None,"MONO27":None,"PentaC":None,"PentaD":None}
        if msiStable:
            for item in msiStable.split("_"):
                if item in msi_list.keys():
                    msi_list[item] = "稳定"
                else:
                    msi_list[item] = "不稳定"
        reportStable = request.form.get("reportStable")

        # resp.status = falcon.HTTP_200
        # resp._headers["Access-Control-Allow-Origin"] = "*"

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
            # resp.status = falcon.HTTP_200
            # resp._headers["Access-Control-Allow-Origin"] = "*"

            db = Mysql(table_name="REPORT_MYSQL")
            sql = "select * from report where sampleName=\"%s\" and analysisName=\"%s\";" % (sample_code, project_name)
            data_batch = db.fetch_all(sql)
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
                        resp.body = return_info
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
                    return_info = {"success":True, "info": "Report generation success!" }
                else:
                    return_info = {"success":False, "info": "Report generation failure!" }
        else:
            return_info = {"success":False, "info": "Report generation failure!" }
        return json.dumps(return_info, ensure_ascii=False)

@app_flask.route('/workflow', methods=['POST'])
def workflow():
        user_name = request.form.get("userName")
        size = int(request.form.get("size"))
        page = int(request.form.get('page'))
        queryversion = request.form.get("version")
        filter = request.form.get("filter")
        i = 0
        # resp.status = falcon.HTTP_200
        # resp._headers["Access-Control-Allow-Origin"] = "*"

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
                        author = projectinfo[6]  #添加模板作者名称
                        date = tmp[5]
                        status = tmp[6]
                        oldpdfpath = tmp[-3]
                        oldpdfurl = tmp[-2]
                        pdfpath = oldpdfpath.replace('/home/khl/web/dist', "http://192.168.1.144:8096")
                        pdfurl = oldpdfurl.replace('/home/khl/web/dist', "http://192.168.1.144:8096")
                        sample_code = tmp[3]  # 样本编号
                        report_name = os.path.basename(oldpdfpath)
                        if version not in totalversion:
                            tmp_data = {"key": version, "value": version}
                            totalversion.append(version)
                            outversion.append(tmp_data)
                            i += 1
                        if filter and queryversion:
                            if ((filter in analysisName  or filter in sampleName) and version == queryversion):
                                aaaa = {"title": analysisName, "sampleName":sampleName ,"author":author,
                                        "reportName":report_name, "sampleCode":sample_code,
                                        "workflowName": flowName, "version": version, "date": date, "status": status,
                                        "pdfpath": pdfpath, "pdfurl": pdfurl, "uniqueId": tmp[0]}
                                info.append(aaaa)
                        elif filter and not queryversion:
                            if filter in analysisName  or filter in sampleName:
                                aaaa = {"title": analysisName, "sampleName": sampleName,"author":author,
                                        "reportName": report_name, "sampleCode": sample_code,
                                        "workflowName": flowName, "version": version, "date": date, "status": status,
                                        "pdfpath": pdfpath, "pdfurl": pdfurl, "uniqueId": tmp[0]}
                                info.append(aaaa)
                        elif not filter and queryversion:
                            if version == queryversion:
                                aaaa = {"title": analysisName, "sampleName": sampleName, "author":author,
                                        "reportName": report_name, "sampleCode": sample_code,
                                        "workflowName": flowName, "version": version, "date": date, "status": status,
                                        "pdfpath": pdfpath, "pdfurl": pdfurl, "uniqueId": tmp[0]}
                                info.append(aaaa)
                        elif not filter and not queryversion:
                            aaaa = {"title": analysisName, "sampleName": sampleName,"author":author,
                                    "reportName": report_name, "sampleCode": sample_code,
                                    "workflowName": flowName, "version": version, "date": date, "status": status,
                                    "pdfpath": pdfpath, "pdfurl": pdfurl, "uniqueId": tmp[0]}
                            print(aaaa)
                            info.append(aaaa)
                    else:
                        result["success"] = False
                        result["info"] = "Report failure!"
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
                        # range_id = range_tmp[(size * page):mod]
                        range_id = range_tmp[(size * (page )):(size * (page+1))]
                else:
                    range_id = range_tmp[(size * (page - 1)):(size * page)]
                out_json = []
                print('range_id',range_id)
                for index in range_id:
                    out_json.append(info[index])
                result["success"] = True
                result["info"] = out_json
                result["length"] = str(len(out_json))
                result["total"] = str(len(info))
                result["totalVersion"] = outversion
            else:
                result["success"] = False
                result["info"] = "Report failure!"
        return json.dumps(result, ensure_ascii=False)


@app_flask.route('/delete', methods=['POST'])
def delete():
    def on_post(self, req, resp):
        uniqueid = request.form.get("id")
        # resp.status = falcon.HTTP_200
        # resp._headers["Access-Control-Allow-Origin"] = "*"
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
                result = {"success":False,"info":"删除失败"}
        else:
            result = {"success": True, "info": "删除成功"}
        return json.dumps(result, ensure_ascii=False)
        # resp.body = json.dumps(result, ensure_ascii=False)

@app_flask.route('/analysis', methods=['POST'])
def analysis():
        result = {}
        user_name = request.form.get("userName")
        size = int(request.form.get("size"))
        page = int(request.form.get('page'))
        queryversion = request.form.get("version")
        filter = request.form.get("filter")
        ngs_type = request.form.get("type")   # 添加过滤参数  all ngs noNgs
        db = Mysql(table_name="REPORT_MYSQL")
        sql = "select * from projectName;"
        outversion = []  # 列表，嵌套字典
        totalversion = []  # 列表 存储unique version信息
        i = 0
        data=db.fetch_all(sql)
        # resp.status = falcon.HTTP_200
        # resp._headers["Access-Control-Allow-Origin"] = "*"
        print('data', data)
        if data:
            result["success"] = True
            info = []
            for d in data:
                description = d[1]
                application = d[1]
                version = d[3]
                date = d[2]
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
                    # range_id = range_tmp[(size*page):mod]
                    #range_id = range_tmp[(size * (page - 1)):(size * page)]
                    range_id = range_tmp[(size * (page)):(size * (page + 1))]
            else:
                range_id = range_tmp[(size * (page - 1)):(size * page)]
            out_json = []
            for index in range_id:
                out_json.append(info[index])
            result["info"] = out_json
            result["length"] = str(len(out_json))
            result["total"] = str(len(info))
            result["totalVersion"] = outversion
            # resp.body = json.dumps(result, ensure_ascii=False)
        else:
            result["success"] = False
            result["info"] = "Report failure!"
            # resp.body = json.dumps(result, ensure_ascii=False)
        return json.dumps(result, ensure_ascii=False)

@app_flask.route('/upload', methods=['POST'])
def upload():
        image = request.form.get('file')
        filename = image.filename
        png_path = '/home/khl/web/upload/%s' % filename
        with open(png_path, 'wb') as temp_file:
            temp_file.write(image.file.read())
        # resp.status = falcon.HTTP_200
        # resp._headers["Access-Control-Allow-Origin"] = "*"
        if os.path.exists(png_path):
            url_path = png_path.replace('/home/khl/web/upload', 'http://192.168.1.144:8095')
            url_info = {"url":url_path}
            return_info = {"success":True, "info": url_info }
        else:
            return_info = {"success": False, "info": "FALSE!"}
        return json.dumps(return_info, ensure_ascii=False)

@app_flask.route('/analysisquery', methods=['POST'])
def analysisquery():
        result = {}
        user_name = request.form.get("userName")
        size = int(request.form.get("size"))
        page = int(request.form.get('page'))
        queryversion = request.form.get("version")
        filter = request.form.get("filter")
        db = Mysql(table_name="REPORT_MYSQL")
        sql = "select * from projectName;"
        print(sql)
        outversion = []  # 列表，嵌套字典
        totalversion = []  # 列表 存储unique version信息
        i = 0
        data=db.fetch_all(sql)
        # resp.status = falcon.HTTP_200
        # resp._headers["Access-Control-Allow-Origin"] = "*"
        if data:
            result["success"] = True
            info = []
            for d in data:
                description = d[1]
                application = d[1]
                version = d[3]
                date = d[2]
                if version not in totalversion:
                    tmp = {}
                    tmp[str(i)] = version
                    outversion.append(tmp)
                    i += 1
                if filter and queryversion:
                    if filter in application and version == queryversion:
                        info_tmp = {"description":description,"application":application,
                            "version":version,"date":date}
                        info.append(info_tmp)
                elif filter and not queryversion:
                    if filter in application:
                        info_tmp = {"description": description, "application": application,
                                    "version": version, "date": date}
                        info.append(info_tmp)
                elif not filter and queryversion:
                    if version == queryversion:
                        info_tmp = {"description": description, "application": application,
                                    "version": version, "date": date}
                        info.append(info_tmp)
                elif not filter and not queryversion:
                    info_tmp = {"description": description, "application": application,
                                "version": version, "date": date}
                    info.append(info_tmp)

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
            print(info)
            for index in range_id:
                out_json.append(info[index])
            result["info"] = out_json
            result["length"] = str(len(out_json))
            result["total"] = str(len(info))
            result["totalVersion"] = outversion
        else:
            result["success"] = False
            result["info"] = "Report failure!"
        return json.dumps(result, ensure_ascii=False)

@app_flask.route('/upload', methods=['POST'])
def index():  # 一个分片上传后被调用
    """前端传递给我的参数: chunkNumber, chunkSize, currentChunkSize, totalSize,
       identifier,filename,relativePath,totalChunks,"file"; filename="timg.jfif",
    """
    if request.method == 'POST':
        # upload_file = request.files['file']
        # task = request.form.get('iden')  # 获取文件唯一标识符
        chunkNumber = request.form.get('chunkNumber', 0)  # 获取该分片在所有分片中的序号
        chunkSize = request.form.get('chunkSize')
        currentChunkSize = request.form.get('currentChunkSize')
        totalSize = request.form.get('totalSize')
        identifier = request.form.get('identifier')
        filename = request.form.get('filename')
        relativePath = request.form.get('relativePath')
        totalChunks = request.form.get('totalChunks')
        file = request.files['file']

        print(chunkNumber,chunkSize,currentChunkSize,totalSize,identifier,filename,relativePath,totalChunks)
        print(file)
        if totalChunks:
            now_time = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename_date = "%s_%s" % (now_time, filename)
            filename_identifier = '%s_%s' % (filename, chunkNumber)  # 构成该分片唯一标识符
            file.save('/home/khl/web/upload/%s' % filename_identifier)  # 保存分片到本地
            if chunkNumber == totalChunks:
                file_list = glob.glob(r'/home/khl/web/upload/%s*' % filename)
                file_list_path = " ".join([os.path.join('/home/khl/web/upload/', i) for i in file_list])
                cmd = "cat %s > %s" % (file_list_path, "/home/khl/web/upload/%s" % filename_date)
                print('cmd', cmd)
                # p=subprocess.Popen(cmd, shell=True)
                os.system(cmd)
        else:
            print('heihei')
            filename = file.filename
            now_time = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename_date = "%s_%s" % (now_time, filename)
            file.save('/home/khl/web/upload/%s' % filename_date)
            # 保存分片到本地
        db = Mysql(table_name="REPORT_MYSQL")
        sql = """insert into png values(UUID(),"",now(),\"%s\","/home/khl/web/upload");""" % filename_date
        db.execute(sql)
        import json
        png_path = "/home/khl/web/upload/%s" % filename_date)
        if os.path.exists(png_path):
            png_url = png_path.replace('/home/khl/web/upload', 'http://192.168.1.144:8095')
            sql = """select * from png where filename=\"%s\";""" % filename_date
            data = db.fetch_one(sql)
            db.commit()
            if data:
                uuid = data[0]
            url_info = {"url": png_url, "uuid":uuid}
            print('url_info', url_info)
            result = {"success": True, "info": url_info}
        else:
            result = {"success": False, "info": "FALSE!"}
        return json.dumps(result, ensure_ascii=False)

# app.add_route("/login", Login())
# app.add_route("/register", Register())
# app.add_route("/sample", query_sample())
# app.add_route("/project", project_name())
# app.add_route("/sampleinfo", GetSampleInfo())
# app.add_route("/reportinfo", reportInfo())
# app.add_route("/upload", upload())
# app.add_route("/workflow", workflow())
# app.add_route("/delete", deleteWorkflow())
# app.add_route("/analysis", analysis())
# app.add_route("/analysisquery", analysisquery())