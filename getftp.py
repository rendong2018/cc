# -*-coding: utf-8-*-

import falcon, json, re
from wsgiref import simple_server
import pymysql
from login_api import *
from config import *
import gunicorn
from query_project import *
from ftplib import FTP
import sys, os
from pdftopng import *


reload(sys)
sys.setdefaultencoding("utf-8")

def connect_ftp(ftp_name):
    conf = Config(table_name="FTP")
    print(conf.host, conf.port,conf.user,conf.password)
    ftp = FTP()
    # ftp.encoding('gbk')
    ftp.set_debuglevel(2)
    ftp.connect(conf.host, int(conf.port))
    ftp.login(conf.user, conf.password)
    out_path = "/home/khl/web/wechat_data"
    # 会先暂时假定文件在tempupfile文件夹下面

    bufsize = 1024
    filename = os.path.join(out_path, ftp_name)
    # localfilename = filename.encode('gbk')
    localfilename=filename
    file_handle = open(localfilename, "wb")
    ftp.cwd("workspace")
    ftp.cwd("reportfile")
    listing = []
    ftp.retrlines("LIST", listing.append)
    print(listing)
    # remotefilename = ftp_name
    remotefilename = ftp_name.encode('gbk')
    ftp.retrbinary("RETR " + "%s" % remotefilename, file_handle.write)
    ret = True
    # 暂时不用try 方法来捕获错误   错误直接输出
    ftp.set_debuglevel(0)
    file_handle.close()
    ftp.quit()
    return ret, filename

def outJpeg(ftp_name):
    ret, input_file = connect_ftp(ftp_name)
    out_path = "/home/khl/web/png"
    figure_path = "/home/khl/web/wechat/static/img"


    # file_name = ftp_name.split(".pdf")[0] + ".jpeg"
    # # file_name = os.path.basename(ftp_name)
    # if ret:
    #     if ftp_name.endswith("pdf"):
    #         ret = pdfConvertJpeg(input_file, out_path, file_name)
    #         if ret:
    #             out_file = os.path.join(figure_path, file_name)
    #             cmd = "cp %s %s" % (os.path.join(out_path, file_name), out_file)
    #             os.system(cmd)
    #             out_ret = True
    #         else:
    #             out_ret = False
    # else:
    #     out_ret = False
    # return out_ret

#"20180103013659899.xls"
# 1221云健康_20180102100834603.zip
#YHB1720642_20171226051139504.pdf
if __name__ == "__main__":
    # ftp_name = "MD20171109-2胡合珍_20171120050409003.pdf"
    # db = Mysql(table_name="GLORIA_MYSQL")
    # project_id = "5f6a0760-4bb9-409b-abc5-83ccd1a21560"
    # sql = "select * from report_info where RP_SAMPLE_ID=\"%s\";" % project_id
    # db_out = db.fetch_one(sql)
    # print(db_out)
    # if db_out[-4] == "不通过" or db_out[-4] == "通过":
    #     pass
    # else:
    #     if db_out:
    #         print(db_out[11])
    #         ftp_name = db_out[11]
    # ftp_name = "YHB1720642_20171226051139504.pdf"
    # ftp_name = "YHF1710519-陈文永-普晟惠（Personal-Benefit）-靶向药物伴随检测-20180103_20180103105753304.pdf"
    # ftp_name = "YHT1730028-杨锋-普晟和-肿瘤靶向化疗用药83基因检测-gDNA-20180112.doc"
    # connect_ftp(ftp_name)
    with open("/home/khl/web/wechat_data/list.txt",'r') as f1:
        files = f1.readlines()
        files_list = [i.strip()for i in files]
        for i in files_list:
            connect_ftp(i)
    # outJpeg(ftp_name)
    #"姜木兰_20171205112227679.pdf"