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
import shutil
from subprocess import *

# path = "/home/khl/web/png/data"

def batchpdfconvertpng(path):
    for files in os.listdir(path):
        if files.endswith('pdf'):
            file_path = os.path.join(path, files)
            file_name = files.split(".pdf")[0]
            tmp_path = os.path.join(path, file_name)
            if not os.path.exists(tmp_path):
                os.mkdir(tmp_path)
            else:
                shutil.rmtree(tmp_path)
            # png_path = os.path.join(tmp_path, "%s.png" % file_name)
            cmd = "convert -verbose -density 1200 %s -quality 100 -depth 24 %s " % (file_path, "%s.png" % file_name)
            os.system(cmd)
            files_list = glob.glob("%s/%s*.png" % (tmp_path,file_name))
            [os.system("cp %s %s" % (path+"/"+i, tmp_path+"/"+i))for i in files_list]

            # p = subprocess.Popen(cmd, shell = True)

if __name__ == "__main__":
    path = "/home/khl/web/png/data"
    batchpdfconvertpng(path)

