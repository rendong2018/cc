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
    #ftp.encoding('gbk')
    #ftp.encoding('gbk')
    ftp.set_debuglevel(2)
    ftp.connect(conf.host, int(conf.port))
    ftp.login(conf.user, conf.password)
    out_path = "/home/khl/web/png/data"
    # 会先暂时假定文件在tempupfile文件夹下面

    bufsize = 1024
    ss=0
    ftp.cwd("workspace")
    ftp.cwd("reportfile")
    listing = []
    ftp.retrlines("LIST", listing.append)
    #print(listing)
    with open(out_path+"/list.txt",'w') as f1:
        for ftp_name_tmp in listing:
            ftp_name = ftp_name_tmp.split(" ")[-1]
            ss += 1
            filename = os.path.join(out_path, ftp_name)
            localfilename = filename
            #localfilename = filename.encode(code)
            # localfilename = filename.decode('unicode_escape').encode('utf-8')
            #localfilename = filename
            file_handle = open(localfilename, "wb")
            print(ftp_name)
            remotefilename = ftp_name.decode('utf-8').encode('gbk')
            # try:
            #     remotefilename = ftp_name.encode(code)
            #remotefilename = ftp_name.decode('unicode_escape').encode('utf-8')
            ftp.retrbinary("RETR " + "%s" % remotefilename, file_handle.write)
                #print(code)
            # except Exception:
            #    print(ss)
            #    pass
            # finally:
            f1.write(ftp_name + "\n")
            file_handle.close()
    # remotefilename = ftp_name
    ret = True
    # 暂时不用try 方法来捕获错误   错误直接输出
    ftp.set_debuglevel(0)
    ftp.quit()
    return ret

if __name__ == "__main__":
    # encode = ['utf-8','gbk','GB2312','GB18030','Big5','HZ']
    # for i in encode:
    connect_ftp()
