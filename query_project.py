# -*-coding: utf-8-

from config import *
from login import *
from collections import Counter, OrderedDict
from project_conf import *
import pymysql
import sys
reload(sys)
sys.setdefaultencoding('utf8')
project_list = new_wechat_project()

def queryProject(useridcard, username, usertel):
    db=Mysql(table_name="GLORIA_MYSQL")
    """先从样本管理开始分析"""
    # sql = """select * from sample_mx where SUBJECT_SFZ=\"%s\" and SUBJECT_NAME=\"%s\" and STORAGE_STAGE=\"%s\" and S_TYPE=\"%s\";""" % (useridcard, username, "收样".decode('utf-8'), "血液(Blood)".decode("utf-8"))
    # sql = """select * from sample_mx where SUBJECT_SFZ=\"%s\" and SUBJECT_NAME=\"%s\" and S_TEL=\"%s\" and (STORAGE_STAGE<>"收样" OR ISNULL(STORAGE_STAGE));""" % (useridcard, username, usertel)
    sql = """select * from sample_mx where SUBJECT_SFZ=\"%s\" and SUBJECT_NAME=\"%s\" and S_TEL=\"%s\"""" % (useridcard, username, usertel)
    data = db.fetch_all(sql)
    if not data:
        sql = """select * from sample_mx where SUBJECT_SFZ=\"%s\" and SUBJECT_NAME=\"%s\" and (STORAGE_STAGE<>"收样" OR ISNULL(STORAGE_STAGE));""" % (useridcard, username)
        # sql = """select * from sample_mx where SUBJECT_SFZ=\"%s\" and SUBJECT_NAME=\"%s\";""" % (useridcard, username)
        data = db.fetch_all(sql)
        print('data',data)
        if not data:
            sql = """select * from sample_mx where SUBJECT_NAME=\"%s\" and S_TEL=\"%s\" and (STORAGE_STAGE<>"收样" OR ISNULL(STORAGE_STAGE));""" % (username, usertel)
            data = db.fetch_all(sql)
            if not data:
                sql = """select * from sample_mx where SUBJECT_NAME=\"%s\" and (STORAGE_STAGE<>"收样" OR ISNULL(STORAGE_STAGE));""" % (username)
                data = db.fetch_all(sql)
                if not data:
                    sql = """select * from sample_mx where SUBJECT_NAME=\"%s\";""" % username
                    data = db.fetch_all(sql)
                    if not data:
                        raise Exception("username:%s, useridcard:%s,usertel:%s没有查询到!" % (username,useridcard,usertel))
    project_info = {}
    sample_code_list = {}
    project_id_list = []
    data_tmp = []
    data_info = {}
    num = 0
    rm_sample_code = None
    # 先判断是否有YHB、YHT  或者YHB、YHF 配对
    for i in data:
        sample_code_tmp = i[3]
        if sample_code_tmp not in sample_code_list.keys():
            sample_code_list[sample_code_tmp] = i
            if sample_code_tmp[2] == "B":
                num += 1
                rm_sample_code = sample_code_tmp
        else:
            pass
    print('sample_code_list', sample_code_list)
    if num == 1 and len(sample_code_list.keys()) > 1:
        # sample_code_list.pop(rm_sample_code)
        pass
    else:
        # 如果有2个YHB  判断哪个是'gDNA'
        if num == 2:
            new_values = []
            for keys, values in sample_code_list.items():
                if 'gDNA' in values[15]:
                    new_values.append(keys)
            for ss in new_values:
                sample_code_list.pop(ss)

    for q in sample_code_list.values():
        sql = "select * from h_sample_item where SAMPLE_ID=\"%s\"" % q[0]
        h_sample_item_id_list = db.fetch_all(sql)
        for h_sample_item_id in h_sample_item_id_list:
            item = h_sample_item_id[6]
            sql = 'select * from h_clinic_project where ID=\"%s\"' % item
            h_clinical_project_info = db.fetch_all(sql)
            print(h_clinical_project_info)
            if h_clinical_project_info:
                    project_tmp = h_clinical_project_info[0][1]
                    #目前先用'gDNA'作为条件筛选判断 此判断条件不行 换一个判断条件
                    # if 'gDNA' in project_tmp:
                    #     continue
                    # else:
                    # 修改替换project信息 和现在的产品名称对应一致
                    project = None
                    for keys,values in project_list.items():
                        if values in project_tmp:
                            project = keys
                            break
                    # 如果产品没有对应的产品名称列表  那么就会默认用原来的产品
                    if not project:
                        project = project_tmp
                    # 保证project现在是非空值才可以
                    if project:
                        if project in project_id_list:
                            continue
                        else:
                            project_id_list.append(project)
                            type = h_clinical_project_info[0][-4]
                            if username not in project_info.keys():
                                project_info[username] = {"project": ["%s" % project], "main_id": [q[0]], "type": [type], "reportId": [q[0]]}
                            else:
                                value = project_info[username]["project"]
                                value.append("%s" % project)
                                project_info[username]["project"] = value
                                main_id = project_info[username]["main_id"]
                                main_id.append(q[0])
                                project_info[username]["main_id"] = main_id
                                type_value = project_info[username]["type"]
                                type_value.append(type)
                                project_info[username]["type"] = type_value
                                reportid_value = project_info[username]["reportId"]
                                reportid_value.append(q[0])
                                project_info[username]["reportId"] = reportid_value

    print("project_info", project_info)
    return project_info


class Analysis:
    def __init__(self, id):
        self.db = Mysql(table_name="GLORIA_MYSQL")
        self.id = id

    def report(self):
        # 关于样本是否走到最后report这一步 是否出报告还需要进行最后一步的检查
        sql = "select * from report_info where RP_SAMPLE_ID=\"%s\";"% self.id
        out1 = self.db.fetch_one(sql)
        # 判断样本
        sql1 = "select * from EXP_RESULT_MX where EX_SAMPLE_ID=\"%s\";" % self.id
        out2 = self.db.fetch_one(sql1)
        if out1 or out2:
            return True
        else:
            return False

    def analysis(self):
        sql = "select * from k_infoanalysis_mx where SAMPLE_ID=\"%s\"" % self.id
        out = self.db.fetch_all(sql)
        if not out:
            return False
        else:
            return True

    def outmanager(self):
        sql = "select * from k_epiboly_manage_mx where SAMPLE_MX_ID=\"%s\"" % self.id
        out = self.db.fetch_all(sql)
        if out:
            return True
        else:
            return False

    def datapcr(self):
        sql = "select * from expresult_mx where SAMPLE_MX_ID=\"%s\";" % self.id
        out1 = self.db.fetch_all(sql)
        sql = "select * from rp_numpcr_result where SAMPLE_ID=\"%s\";" % self.id
        out2 = self.db.fetch_all(sql)
        if out1 or out2:
            return True
        else:
            return False

    def ngs(self):
        sql = "select * from sample_index where MY_SAMPLE_ID=\"%s\";" % self.id
        out1 = self.db.fetch_all(sql)
        sql = "select * from quacontrol_sample_mx where QCS_SAMPLE_ID=\"%s\";" % self.id
        out2 = self.db.fetch_all(sql)
        # 此处可能会有bug
        sql = "select * from mixed_sample_mx where MS_QC_SAMPLEID=\"%s\";" % self.id
        out3 = self.db.fetch_all(sql)
        if out1 or out2 or out3:
            return True
        else:
            return False

    def extractrqc(self):
        sql = "select * from sample_separate_mx where OLD_SAMPLE_MX_ID=\"%s\"" % self.id
        out1 = self.db.fetch_all(sql)
        sql = "select * from k_sample_tq_mx where SAMPLE_ID=\"%s\"" % self.id
        out2 = self.db.fetch_all(sql)
        sql = "select * from sample_qc where OLD_SAMPLE_MX_ID=\"%s\";" % self.id
        out3 = self.db.fetch_all(sql)
        sql = "select * from k_sample_tq_pool where K_SAMPLE_ID=\"%s\";" % self.id
        out4 = self.db.fetch_all(sql)
        sql = "select * from sample_qc where SAMPLE_MX_ID=\"%s\";" % self.id
        out5 = self.db.fetch_all(sql)
        if out1 or out2 or out3 or out4 or out5:
            return True
        else:
            return False

    def pcr(self):
        sql = "select * from k_lgc_sample_mx where SAMPLE_MX_ID=\"%s\"" % self.id
        out1 = self.db.fetch_all(sql)
        sql = "select * from k_result_summary where SAMPLE_MX_ID=\"%s\";" % self.id
        out2 = self.db.fetch_all(sql)
        if out1 or out2:
            return True
        else:
            return False

    def close(self):
        self.db.commit()

def queryinfo(id):
    data = Analysis(id)
    report_info = data.report()
    analysis_info = data.analysis()
    outmanager_info = data.outmanager()
    datapcr_info = data.datapcr()
    ngs_info = data.ngs()
    extractrqc_info = data.extractrqc()
    pcr_info = data.pcr()
    data.close()

    print("report:%s,analysis:%s,outmanager:%s,datapcr:%s,ngs:%s,extractrqc:%s,pcr:%s" % (report_info, analysis_info,
                        outmanager_info, datapcr_info, ngs_info, extractrqc_info, pcr_info))
    return_info = OrderedDict()
    return_info = {"report": report_info, "analysis": analysis_info, "outmanager": outmanager_info,
                   "datapcr": datapcr_info, "ngs": ngs_info, "extractrqc": extractrqc_info, "pcr": pcr_info}
    return return_info


def get_project_info(projectInfo):
    get_project_info_result = {}
    for keys, values in projectInfo.items():
        mainId = values["main_id"]
        project = values["project"]
        type = values["type"]
        reportid = values["reportId"]
        get_project_info_result[keys] = []
        for index in range(len(mainId)):
            queryInfoOut = queryinfo(mainId[index])
            get_project_info_result[keys].append({"project": project[index], "info": queryInfoOut, "type": type[index], "reportId":reportid[index]})
    return get_project_info_result


def QUERY(username, useridcard, usertel):
    Queryinfo = queryProject(useridcard, username, usertel)
    out = get_project_info(projectInfo=Queryinfo)
    return out


def main():
    data = queryProject(useridcard="420121196307261516", username="毛诗泉", usertel="13886199270")
    print(data)

if __name__ == "__main__":
    # main()
    # useridcard="350521195410278526"
    # username="林宝珠"
    # usertel="13959207769"
    # 310222195011210412	谢龙法	13918315927
    useridcard = "350521195410278526"
    username="林宝珠"
    usertel="13671051120"
    # data = QUERY(username,useridcard,usertel)
    # print(data)
    # data = queryProject(useridcard, username, usertel)
    # print(data)
    # "362fa49b-de5a-4e8e-90aa-0c3c67607b7a"
    # data = Analysis("362fa49b-de5a-4e8e-90aa-0c3c67607b7a")
    # print(data.report())
    db = Mysql(table_name="REPORT_MYSQL")
    sql = """insert into template values(UUID(), "1ff9a202-ffe5-11e7-952a-3cf724cf9faf",now(),"msi.xml","/home/khl/web/word")"""
    db.execute(sql)
    db.commit()

    "create table identification (ID VAR" \
    "CHAR(60), userName VARCHAR(20), userIdCard VARCHAR(50), userTel VARCHAR(20))DEFAULT CHARSET = UTF8;"