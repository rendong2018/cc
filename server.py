#!/usr/bin/env python
# coding=utf-8

import os,json, glob
from flask_cors import *
from flask import Flask, request, render_template as rt
import subprocess
from multiprocessing import *
import datetime
from login_api import *
from config import *

app_flask = Flask(__name__)
CORS(app_flask, supports_credentials=True)


@app_flask.route('/upload', methods=['GET', 'POST'])
def index():  # 一个分片上传后被调用
    """前端传递给我的参数: chunkNumber, chunkSize, currentChunkSize, totalSize,
       identifier,filename,relativePath,totalChunks,"file"; filename="timg.jfif",
    """
    if request.method == 'POST':
        # upload_file = request.files['file']
        # task = request.form.get('iden')  # 获取文件唯一标识符
        chunkNumber = request.form.get('chunkNumber', 0)  # 获取该分片在所有分片中的序号
        chunkSize = request.form.get('chunkSize')
        currentChunkSize = request.form.get('currentChunkSize')
        totalSize = request.form.get('totalSize')
        identifier = request.form.get('identifier')
        filename = request.form.get('filename')
        relativePath = request.form.get('relativePath')
        totalChunks = request.form.get('totalChunks')
        file = request.files['file']

        print(chunkNumber,chunkSize,currentChunkSize,totalSize,identifier,filename,relativePath,totalChunks)
        print(file)
        if totalChunks:
            now_time = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename_date = "%s_%s" % (now_time, filename)
            filename_identifier = '%s_%s' % (filename, chunkNumber)  # 构成该分片唯一标识符
            file.save('/home/khl/web/upload/%s' % filename_identifier)  # 保存分片到本地
            if chunkNumber == totalChunks:
                file_list = glob.glob(r'/home/khl/web/upload/%s*' % filename)
                file_list_path = " ".join([os.path.join('/home/khl/web/upload/', i) for i in file_list])
                cmd = "cat %s > %s" % (file_list_path, "/home/khl/web/upload/%s" % filename_date)
                print('cmd', cmd)
                # p=subprocess.Popen(cmd, shell=True)
                os.system(cmd)
        else:
            print('heihei')
            filename = file.filename
            now_time = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename_date = "%s_%s" % (now_time, filename)
            file.save('/home/khl/web/upload/%s' % filename_date)
            # 保存分片到本地
        db = Mysql(table_name="REPORT_MYSQL")
        sql = """insert into png values(UUID(),"",now(),\"%s\","/home/khl/web/upload");""" % filename_date
        db.execute(sql)
        import json
        png_path = "/home/khl/web/upload/%s" % filename_date)
        if os.path.exists(png_path):
            png_url = png_path.replace('/home/khl/web/upload', 'http://192.168.1.144:8095')
            sql = """select * from png where filename=\"%s\";""" % filename_date
            data = db.fetch_one(sql)
            db.commit()
            if data:
                uuid = data[0]
            url_info = {"url": png_url, "uuid":uuid}
            print('url_info', url_info)
            result = {"success": True, "info": url_info}
        else:
            result = {"success": False, "info": "FALSE!"}
        return json.dumps(result, ensure_ascii=False)


@app_flask.route('/success', methods=['GET'])
def upload_success():  # 所有分片均上传完后被调用
    task = request.args.get('task_id')
    ext = request.args.get('ext', '')
    upload_type = request.args.get('type')
    if len(ext) == 0 and upload_type:
        ext = upload_type.split('/')[1]
    ext = '' if len(ext) == 0 else '.%s' % ext  # 构建文件后缀名
    chunk = 0
    with open('./upload/%s%s' % (task, ext), 'w') as target_file:  # 创建新文件
        while True:
            try:
                filename = './upload/%s%d' % (task, chunk)
                source_file = open(filename, 'r',encoding='utf-8')  # 按序打开每个分片
                target_file.write(source_file.read())  # 读取分片内容写入新文件
                source_file.close()
            except IOError:
                break
            chunk += 1
            os.remove(filename)  # 删除该分片，节约空间
    return rt('./index.html')


if __name__ == '__main__':
    # app.run(debug=False)
    app_flask.run(host='192.168.1.144', port=5000)

"""
------WebKitFormBoundary05HCxaIO4CLWEnIi
Content-Disposition: form-data; name="chunkNumber"

1
------WebKitFormBoundary05HCxaIO4CLWEnIi
Content-Disposition: form-data; name="chunkSize"

1048576
------WebKitFormBoundary05HCxaIO4CLWEnIi
Content-Disposition: form-data; name="currentChunkSize"

136826
------WebKitFormBoundary05HCxaIO4CLWEnIi
Content-Disposition: form-data; name="totalSize"

136826
------WebKitFormBoundary05HCxaIO4CLWEnIi
Content-Disposition: form-data; name="identifier"

136826-timgjfif
------WebKitFormBoundary05HCxaIO4CLWEnIi
Content-Disposition: form-data; name="filename"

timg.jfif
------WebKitFormBoundary05HCxaIO4CLWEnIi
Content-Disposition: form-data; name="relativePath"

timg.jfif
------WebKitFormBoundary05HCxaIO4CLWEnIi
Content-Disposition: form-data; name="totalChunks"

1
------WebKitFormBoundary05HCxaIO4CLWEnIi
Content-Disposition: form-data; name="file"; filename="timg.jfif"
Content-Type: image/jpeg


------WebKitFormBoundary05HCxaIO4CLWEnIi--
"""
