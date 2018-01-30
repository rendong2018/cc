#-*-coding: utf-8-*-

import falcon, json, re
from wsgiref import simple_server
import pymysql
from login_api import *
from config import *
import gunicorn
#from query_project import *
from ftplib import FTP
import sys, os
from pdftopng import *

def connect_ftp():
    conf = Config(table_name="FTP")
    print(conf.host, conf.port,conf.user,conf.password)
    ftp = FTP()
    ftp.set_debuglevel(2)
    ftp.connect(conf.host, int(conf.port))
    ftp.login(conf.user, conf.password)
    # out_path = "/home/khl/web/png/data"
    out_path = "/home/khl/web/new_data"
    # 会先暂时假定文件在tempupfile文件夹下面

    bufsize = 1024
    ss=0
    ftp.cwd("workspace")
    ftp.cwd("reportfile")
    listing = []
    ftp.retrlines("LIST", listing.append)
    with open(out_path+"/list.txt",'w') as f1:
        for ftp_name_tmp in listing:
            ftp_name = ftp_name_tmp.split(" ")[-1]
            tmp_ftp_name = ftp_name.decode('gbk')
            print(tmp_ftp_name)
            ss += 1
            filename = os.path.join(out_path, tmp_ftp_name)
            localfilename = filename
            #localfilename = filename.encode(code)
            # localfilename = filename.decode('unicode_escape').encode('utf-8')
            #localfilename = filename
            file_handle = open(localfilename, "wb")
            print(ftp_name)
            remotefilename = ftp_name
            print(remotefilename)
            ftp.retrbinary("RETR " + "%s" % remotefilename, file_handle.write)
            f1.write(ftp_name + "\n")
            file_handle.close()
    # remotefilename = ftp_name
    ret = True
    ftp.set_debuglevel(0)
    ftp.quit()
    return ret

if __name__ == "__main__":
    # encode = ['utf-8','gbk','GB2312','GB18030','Big5','HZ']
    # for i in encode:
    connect_ftp()
