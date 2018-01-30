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
import time
import os.path
# from doc2pdf import *
# import comtypes.client

def doc2pdf(in_file, out_file):
    wdFormatPDF = 17
    word = comtypes.client.CreateObject('Word.Application')
    doc = word.Documents.Open(in_file)
    doc.SaveAs(out_file, FileFormat=wdFormatPDF)
    doc.Close()
    word.Quit()

def templateword(xml_path, out_path, sample_name, sample_code, project_name, usernameid, type=None,tumor_infiltrating=None,msi_info=None,image_left=None,image_right=None):
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
    if type:
        project = project_name + '-' + type
    else:
        project = project_name
    reportData = query_sample_filter(sample_code=sample_code, project=project)
    print('reportData', reportData)
    # print('reportData', reportData)
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
    if tumor_infiltrating:
        for keys, values in tumor_infiltrating.items():
            new_reportdata[keys] = values
    if msi_info:
        for keys, values in msi_info.items():
            new_reportdata[keys] = values
    import base64
    if image_left:
        f = open(r'%s' % image_left, 'rb')  # 二进制方式打开图文件
        imageLeft = base64.b64encode(f.read())  # 读取文件内容，转换为base64编码
        f.close()
        new_reportdata['IMAGE_LEFT'] = imageLeft
    if image_right:
        f = open(r'%s' % image_right, 'rb')  # 二进制方式打开图文件
        imageRight = base64.b64encode(f.read())  # 读取文件内容，转换为base64编码
        f.close()
        new_reportdata['IMAGE_RIGHT'] = imageRight
    contents = contents.format(**new_reportdata)
    # print("new_reportdata", new_reportdata)

    # 4.1  "<<" 替换成 "{"  / ">>" 替换成 "}"
    contents = contents.replace('<<', '{').replace('>>', '}')

    contents1 = contents.encode('utf-8')
    # print(contents1)
    date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # print(date)
    #此处文件的命名感觉有点问题  重复命名可能会报错
    path = os.path.join(out_path, sample_code)
    try:
        if not os.path.exists(path):
            os.mkdir(path)
    except Exception:
        os.mkdir(path)

    #储存文件信息更加完整

    pdfpath = os.path.join(path, "%s_%s.doc" % (sample_name, datetime.datetime.now().strftime("%Y%m%d_%H%M%S")))
    pdfurl = os.path.join(path, "%s_%s.pdf" % (sample_name, datetime.datetime.now().strftime("%Y%m%d_%H%M%S")))
    print(pdfpath)
    with open(pdfpath, 'wb') as f1:
        tmp_data = contents1.decode("utf-8")
        f1.write(contents1)

    db = Mysql(table_name="REPORT_MYSQL")
    # 暂时先考虑我做的事情
    if type:
        sql = "select * from projectName where projectName=\"%s\" and type = \"%s\";" % (project_name, type)
    else:
        sql = "select * from projectName where projectName=\"%s\";" % project_name
    print(sql)
    data = db.fetch_one(sql)
    projectname_id = data[0]

    # sq1_tmp = "insert into report values(UUID(), \"%s\", \"%s\", \"%s\", \"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\")"
    # sql = sq1_tmp % (projectname_id, project, sample_code,"",datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),"完成", '/home/khl/web/word/report/',sample_name,pdfpath,pdfurl,usernameid)
    # db.execute(sql)
    db.commit()
    return pdfpath, pdfurl


if __name__ == "__main__":
    # sample_code = "YHB1721079"
    # project_name = "普益康-肿瘤个体化诊疗620基因检测"
    # xml_path = "/home/khl/web/word/620geneTissue.xml"
    # xml_path = "/home/khl/web/word/12geneTissue.xml
    # sample_code = "YHF1810005"
    # project_name = "普晟惠-PD-L1及CD8蛋白表达检测"
    # sample_code = "YHF1810005"
    # project_name = "普晟惠-MSI微卫星不稳定性检测"
    sample_code ="YHB1720537"
    project_name = "普晟朗-肺癌靶向用药15基因检测"
    # xml_path = "/home/khl/web/word/pd-l1.xml"
    # xml_path = "/home/khl/web/word/msi.xml"
    xml_path = "/home/khl/web/word/15gene.xml"
    sample_name = "YHF1810005_msi"
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
    tumorLevel = "aaa"
    NR21="稳定"
    NR24="稳定"
    NR27="稳定"
    BAT25="稳定"
    BAT26="稳定"
    MONO27="稳定"
    PentaC="稳定"
    PentaD="稳定"
    reportStable="稳定"
    # msi_info = get_msi_info(NR21, NR24, NR27, BAT25, BAT26, MONO27, PentaC, PentaD, reportStable)
    # tumor_infiltrating = get_tumor_infiltrating(tumorInfiltrating, pd28Tumor, pd28Lymph, pd142Tumor, pd142Lymph, cd8,
    #                                             tumorPercent, tumorLevel)
    # # print(tumor_infiltrating)
    image_left="/home/khl/web/upload/pdl1figure1.png"
    image_right="/home/khl/web/upload/pdl1figure1.png"
    templateword(xml_path, out_path, sample_name, sample_code, project_name, usernameid, type=None, tumor_infiltrating=None,msi_info=None,image_left=None,image_right=None)



