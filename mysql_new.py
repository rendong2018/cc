# -*-coding: utf-8-*-

import falcon, json, re
import pymysql
from login_api import *
from config import *
from ftplib import FTP
import sys, os
from getftp import *
import glob

out_path = "/home/khl/web/wechat_data"
global out_path

def new_info():
    db = Mysql(table_name="GLORIA_MYSQL")
    #create table upload_sample (ID VARCHAR(80), usernameId VARCHAR(100), datetime VARCHAR(100), filename VARCHAR(200), filepath VARCHAR(200), oldname VARCHAR(200))DEFAULT CHARSET=UTF8;
    #sql = "create table ftp_download (ID VARCHAR(80), sample_code VARCHAR(60),status VARCHAR(100),datetime VARCHAR(100),file_name VARCHAR(200), path VARCHAR(200))DEFAULT CHARSET=UTF8;"
    sql = "select * from report_info;"
    data = db.fetch_all(sql)
    db.commit()
    report_name = []
    db1 = Mysql(table_name="REPORT_MYSQL")
    out_path = "/home/khl/web/wechat_data"
    for d in data:
        if d[11] and d[11] not in report_name:
            report_name.append(d[11])
            print(d[11])
            sample_code = d[17]
            sql = "insert into ftp_download values(UUID(),\"%s\",\"%s\",now(),\"%s\",\"%s\")" % (sample_code,"完成",d[11],out_path)
            print(sql)
            db1.execute(sql)
    db1.commit()
    with open(out_path+"/list.txt", 'w') as f1:
        f1.write("\n".join(report_name)+"\n")

def insert_info(sample_code, file_name):
    """插入文件信息"""
    db_144 = Mysql(table_name="REPORT_MYSQL")
    sql = "insert into ftp_download values(UUID(),\"%s\",\"%s\",now(),\"%s\",\"%s\")" % (sample_code, "完成", file_name, out_path)
    db_144 = db_144.execute(sql)
    db_144.commit()
    ret = True
    return ret


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
            file_path = os.path.join(tmp_data[-1], tmp_data[-2])
            file_name = i[11]
            filepath=file_path
            print(filepath, file_name)
            if os.path.exists(filepath) and 'pdf' in file_name:
                cmd = "convert -verbose -density 300 %s -quality 100 -depth 24 %s" % (file_path, file_name.split(".pdf")[0]+".png")
                print(cmd)
                os.system(cmd)
                files_list = glob.glob("%s/%s*.png" % (out_path, file_name.split('.pdf')[0]))
                print(files_list)
                tmp_path = os.path.join(out_path, file_name.split('.pdf')[0])
                print("tmp_path", tmp_path)
                for file in files_list:
                    cmd = "cp %s %s" % (file, tmp_path + "/"+os.path.basename(file))
                    print(cmd)
                    os.system(cmd)


def query_report_sample():
    sql = "select * from report_info;"
    db = Mysql(table_name="GLORIA_MYSQL")
    data = db.fetch_all(sql)
    report_list= []
    report_info = {}
    with open("D:/wechat/report_sample.txt", 'w') as f1:
        for d in data:
            report_tmp = d[11]
            if report_tmp and 'pdf' in report_tmp:
                if report_tmp not in report_list:
                    sample_id = d[16]
                    sql = "select * from sample_mx where ID=\"%s\";" % sample_id
                    data1 = db.fetch_one(sql)
                    if data1:
                        f1.write(sample_id+"\t"+data1[2]+"\t"+data1[3]+"\t"+data1[52]+"\t"+data1[59]+"\t"+data1[8]+"\n")


if __name__ == "__main__":
    # new_info()
    # backup_report()
    # query_report_sample()