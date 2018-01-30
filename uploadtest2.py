# -*-coding: utf-8-*-

import falcon, json
from wsgiref import simple_server
import pymysql
# from login_api import *
# from config import *
import gunicorn
# from query_project import *
from falcon_multipart.middleware import MultipartMiddleware

app = falcon.API(middleware=[MultipartMiddleware()])
app.req_options.auto_parse_form_urlencoded = True
app.req_options.keep_blank_qs_values = True


class upload(object):
    def on_post(self, req, resp):
        params = req.params
        # image = req.get_param('file')
        file = params['file']
        filename=params['filename']
        # print('image', image)
        filename = image.filename
        print('filename',filename)
        png_path = '/home/khl/web/upload/%s' % filename
        with open(png_path, 'wb') as temp_file:
            temp_file.write(image.file.read())
        resp.status = falcon.HTTP_200
        resp._headers["Access-Control-Allow-Origin"] = "*"
        if os.path.exists(png_path):
            url_path = png_path.replace('/home/khl/web/upload', 'http://192.168.1.144:8095')
            url_info = {"url":url_path}
            return_info = {"success":True, "info": url_info }
        else:
            return_info = {"success": False, "info": "FALSE!"}
        resp.body = json.dumps(return_info, ensure_ascii=False)

app.add_route("/upload", upload())
httpd = simple_server.make_server("192.168.1.144", 5000, app)
httpd.serve_forever()