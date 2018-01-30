# coding:utf-8

import falcon

import json
import uuid
import sys
from query_sample_info import *
from login_api import *
from config import *
sys.getdefaultencoding()
import datetime

def templateword(xml_path, out_path, sample_name, sample_code, project_name, usernameid, type=None):
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
    f = open(xml_path, 'rb')
    contents_tmp = f.read()
    f.close()
    if isinstance(contents_tmp, bytes):
        # contents = str(contents_tmp, 'utf-8')
        contents = str(contents_tmp)
    if type:
        project = project_name + '-' + type
    else:
        project = project_name
    reportData = query_sample_filter(sample_code=sample_code, project=project)
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
    contents = contents.format(**reportData)
    # 4.1  "<<" 替换成 "{"  / ">>" 替换成 "}"
    contents = contents.replace('<<', '{').replace('>>', '}')

    contents1 = contents.encode('utf-8')
    # print(contents1)
    date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # print(date)
    #此处文件的命名感觉有点问题  重复命名可能会报错
    pdfpath = os.path.join(out_path,"%s.doc" % sample_name)
    pdfurl = os.path.join(out_path, "%s.pdf" % sample_name)
    print(contents1.decode("utf-8"))
    with open(pdfpath, 'wb') as f1:
        tmp_data = contents1.decode("utf-8")
        f1.write(contents1)


if __name__ == "__main__":
    # pass
    # xml_path = "D:/cc/12gene_template.xml"
    # xml_path = "D:/cc/15gene_20180109temp.xml"
    # out_path = "D:/cc/"
    # xml_path = "/home/khl/web/word/12gene_template.xml"
    xml_path = "/home/khl/web/word/83geneTissue.xml"
    out_path = "/home/khl/web/word"
    sample_name = "aaaaaaaa83gene"
    # sample_code = "YHB1720537"
    # sample_code = "YHB1720312"
    # project_name = "普晟畅（Personal-CRC）-结直肠癌靶向用药12基因检测-组织版"

    sample_code = "YHB1720517"
    project_name = "普晟和-肿瘤靶向化疗用药83基因检测"
    usernameid = "09f7600c-de52-11e7-85d7-eef2f2e6a896"
    templateword(xml_path, out_path, sample_name, sample_code, project_name, usernameid, type=None)
