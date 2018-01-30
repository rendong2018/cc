# coding:utf-8

import falcon
import json
import uuid
import sys
from config import *
sys.getdefaultencoding()
import datetime
import time
import os.path
from query_sample_info import *

# from doc2pdf import *
# import comtypes.client


def templateword(xml_path, out_path, sample_name, sample_code, project_name, reportData=None,tumor_infiltrating=None):
    """
    :param xml_path: 模板的路径信息
    :param out_path: 生成报告文档的路径
    :param sample_name: 样本名字
    :param sample_code: 样本编号
    :param project_name: 项目名字
    :param usernameid: 用户存在login数据库的信息
    :param type: 组织版还是血液版, 默认为None
    :return:
    """
    # out_path = "D:/cc"
    f = open(xml_path, 'rb')
    contents_tmp = f.read()
    f.close()
    if isinstance(contents_tmp, bytes):
        # contents = str(contents_tmp, 'utf-8')
        contents = str(contents_tmp)
    project = project_name
    # if type:
    #     project = project_name + '-' + type
    # else:
    #     project = project_name
    # reportData = query_sample_filter(sample_code=sample_code, project=project)
    """
    {'ClientName': '费远锋', 'ReportNo': 'YHB1720537', 'SampleHospital': '新桥医院', 
    'ReportDate': '2017.12.28', 'ClientSex': '男', 'ClientID': '512328194612051873', 
    'ClientAge': '1946.12.05', 'ClientPhone': '13370792222', 'ClientInfo': '肺鳞癌', 
    'ClientHistory': '使用化疗药物2疗程，药物询医', 'SampleNo': 'YHB1720537', 
    'SampleType': '血液blood（B）', 
    'SampleDNA': '7ml', 'SampleDateRecieved': '2017.12.05'}
    """

    # print(reportData)


    contents = contents.replace('{', '<<').replace('}', '>>')
    # 4.2  "<<<<" 替换成 "{"  / ">>>>" 替换成 "}"
    contents = contents.replace('<<<<', '{').replace('>>>>', '}')
    # 4.3 使用 format函数替换
    # print(reportData)
    new_reportdata = {}
    for keys, values in reportData.items():
        new_reportdata[keys] = values
    for keys, values in tumor_infiltrating.items():
        new_reportdata[keys] = values
    contents = contents.format(**new_reportdata)
    print("new_reportdata", new_reportdata)
    # if tumor_infiltrating:
    #     contents = contents.format(**tumor_infiltrating)
    # contents = contents.format()
    # 4.1  "<<" 替换成 "{"  / ">>" 替换成 "}"
    contents = contents.replace('<<', '{').replace('>>', '}')

    contents1 = contents.encode('utf-8')
    # print(contents1)
    # print(date)
    #此处文件的命名感觉有点问题  重复命名可能会报错


    #储存文件信息更加完整




if __name__ == "__main__":
    # sample_code = "YHB1721079"
    # project_name = "普益康-肿瘤个体化诊疗620基因检测"
    # xml_path = "/home/khl/web/word/620geneTissue.xml"
    # xml_path = "/home/khl/web/word/12geneTissue.xml
    sample_code = "YHF1810005"
    project_name = "普晟惠-PD-L1及CD8蛋白表达检测"
    xml_path = "/home/khl/web/word/pd-l1.xml"
    sample_name = "YHF1810005_pd_l1"
    # project_name = "普晟畅（Personal-CRC）-结直肠癌靶向用药12基因检测-组织版"
    usernameid = "09f7600c-de52-11e7-85d7-eef2f2e6a896"
    out_path = "/home/khl/web/dist/downloads/tmp"
    tumorInfiltrating = "活跃"
    pd28Tumor = "阴性"
    pd28Lymph = "阴性"
    pd142Tumor = "阴性"
    pd142Lymph = "阴性"
    cd8 = "8%阳性"
    tumorPercent = "50%"
    tumorLevel = "中等"
    tumor_infiltrating = get_tumor_infiltrating(tumorInfiltrating, pd28Tumor, pd28Lymph, pd142Tumor, pd142Lymph, cd8,
                                                tumorPercent, tumorLevel)
    print(tumor_infiltrating)
    reportData1 = {'ReportDate': '2018.1.23', 'SampleType': '\xe7\x9f\xb3\xe8\x9c\xa1\xe5\x8c\x85\xe5\x9f\x8b\xe7\xbb\x84\xe7\xbb\x87FFPE\xef\xbc\x88F\xef\xbc\x89', 'ClientSex': '\xe7\x94\xb7', 'ClientInfo': '\xe4\xb8\x8b\xe5\x92\xbd\xe7\x99\x8c', 'SampleHospital': '\xe6\xb5\xb7\xe5\x86\x9b\xe6\x80\xbb\xe5\x8c\xbb\xe9\x99\xa2', 'ClientName': '\xe7\x89\x9b\xe6\x99\xaf\xe5\x8d\x8e', 'SampleNo': 'YHF1810005', 'ClientPhone': '18754909008', 'ClientHistory': '/', 'ClientID': '372830195009050013', 'ReportNo': 'YHF1810005', 'DateRecieved': '2018.01.15', 'ClientAge': '1950.09.05', 'SampleDNA': '1\xe5\x9d\x97'}
    # def templateword(xml_path, out_path, sample_name, sample_code, project_name, reportData=None,tumor_infiltrating=None):

    templateword(xml_path, out_path, sample_name, sample_code, project_name, reportData=reportData1, tumor_infiltrating=tumor_infiltrating)



