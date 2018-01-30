# -*-coding: utf-8-*-

import falcon, json
from wsgiref import simple_server
import pymysql
# from login_api import *
# from config import *
import gunicorn
# from query_project import *

app = falcon.API()
app.req_options.auto_parse_form_urlencoded = True
app.req_options.keep_blank_qs_values = True


class upload(object):
    def on_post(self, req, resp):
        params = req.params
        data = req.stream.read()
        content_type = req.content_type
        import base64
        with open("D:/cc/falconUploadPng1.png",'wb') as f1:
            f1.write(data)
        # with open("D:/cc/falconUploadPng.png",'wb') as f1:
        #     data1 = str(data)
        #     data2 = data1.strip().split("\\r\\n")
        #     print(data2[0],data2[1],data2[2],data2[3])
        #     data3 = data2[5:-2]
        #     data4 = "\r\n".join(data3)
        #     data5 = bytes(data4, encoding='utf8')
        #     # print(data4)
        #     f1.write(data5)
            # tmp = base64.b64encode(data)
            # f1.write(tmp)

        # s1 = str(data).split("\\r\\n")
        # print("s1", s1)
        # for i in s1:
        #     print(i)
        # with open("D:/cc/testpdl1xml.xml",'w') as f1:
        #     s4 = s1[-3]
        #     for ss in s4.split("\\n"):
        #         print(ss)
        #         f1.write(ss+"\n")
        resp.status = falcon.HTTP_200
        resp._headers["Access-Control-Allow-Origin"] = "*"
        return_info = '{"success":true, "info": "upload success!" }'
        resp.body = return_info

app.add_route("/upload", upload())
httpd = simple_server.make_server("127.0.0.1", 8122, app)
httpd.serve_forever()