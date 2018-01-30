# -*-coding: utf-8-*-

import falcon, json, re
import pymysql
from login_api import *
from config import *
from ftplib import FTP
import sys, os
from getftp import *
import glob

def backup_report():
    """查询数据  定时备份  每三个小时备份一次"""
    db = Mysql(table_name="GLORIA_MYSQL")
    sql = "select * from report_info;"
    db_144 = Mysql(table_name="REPORT_MYSQL")
    data = db.fetch_all(sql)
    db.commit()
    out_path = "/home/khl/web/wechat_data/"

    for i in data:
        sample_code = i[17]
        if not i[11]:
            continue
        else:
            sql = "select * from ftp_download where sample_code=\"%s\";" % sample_code
            tmp_data = db_144.fetch_one(sql)
            file_path = os.path.join(out_path, i[11])
            if tmp_data:
                continue
                # if os.path.exists(file_path):
                #     "判断数据库里面是否有信息  如果已经存储信息  则忽略"
                #     if 'pdf' in i[11]:
                #         tmp_png_path = os.path.join(out_path, i[11].split(".pdf")[0])
                #         if not os.path.exists(tmp_png_path):
                #             os.mkdir(tmp_png_path)
                #         if os.listdir(tmp_png_path):
                #             #暂时先这样考虑吧 可能还会有错误
                #             continue
                #         else:
                #             file_list = glob.glob(r'%s/%s*.png' % (out_path,i[11].split('.pdf')[0]))
                #             for file in file_list:
                #                 cmd = "mv %s %s" % (file, os.path.join(tmp_png_path,os.path.basename(file)))
                #                 os.system(cmd)
            else:
                file_name = i[11]
                ret, filename1 = connect_ftp(file_name)
                if ret:
                    if os.path.exists(file_path) and 'pdf' in file_name:
                        cmd = "convert -verbose -density 300 %s -quality 100 -depth 24 %s" % (file_path, file_name.split(".pdf")[0]+".png")
                        print(cmd)
                        os.system(cmd)
                        files_list = glob.glob("%s/%s*.png" % (out_path, file_name.split('.pdf')[0]))
                        print(files_list)
                        tmp_path = os.path.join(out_path, file_name.split('.pdf')[0])
                        if not os.path.exists(tmp_path):
                            os.mkdir(tmp_data)

                        print("tmp_path", tmp_path)
                        for file in files_list:
                            cmd = "mv %s %s" % (file, tmp_path + "/"+os.path.basename(file))
                            print(cmd)
                            os.system(cmd)
                        sql = """insert into ftp_download values(UUID(),\"%s\","完成",now(),\"%s\","/home/khl/web/wechat_data")""" % (sample_code, file_name)
                        db_144.execute(sql)
    db_144.commit()

if __name__ == "__main__":
    backup_report()