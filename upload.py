# -*-coding: utf-8-*-


import falcon
import json
from wsgiref import simple_server
import pymysql
from login_api import *
from config import *
import gunicorn
from query_project import *
from falcon_multipart.middleware import MultipartMiddleware
import io, os, re, uuid, mimetypes

app = falcon.API()
app.req_options.auto_parse_form_urlencoded = True
app.req_options.keep_blank_qs_values = True


class multipartupload(object):
    def __init__(self, image_store, path=None):
        self._image_store = image_store
        self.file_path = path

    def on_post(self, req, resp):
        data = req.params
        chunknumber = data["chunkNumber"]
        totalchunks = data["totalChunks"]
        chunksize = data["chunkSize"]
        currentchunksize = data["currentChunkSize"]
        totalsize = data["totalSize"]
        identifier = data["identitier"]
        filename = data["filename"]
        file = data["file"]
        print(file)
        print(filename)
        # relativepath = data["relativePath"]
        tmp = self._image_store(store_path=self.file_path, filename=filename)
        name = tmp.save(req.stream, req.content_type)
        resp._headers["Access-Control-Allow-Origin"] = "*"
        resp.status = falcon.HTTP_200

        resp.location = '/image/' + name

        # # image = req.get_param('image')
        # # filename = image.filename
        # # helpers.write_json(resp, falcon.HTTP_200,{
        # #                 'name': filename
        # #                 })
        # data = req.params
        # filename = data["fileName"]
        # filesize = data["fileSize"]
        # # isfirstupload = data["isfirstupload"]
        # """暂时先不需要判断是否最后的分片"""
        # upload = cgi.FieldStorage(fq=req.stream, environ=req.env)
        # data = upload["file"].file.read().decode('utf-8')
        # resp.body = json.dumps(dict(data=data))
        #
        #
        #
        # file_path = os.path.join(self.file_path, filename)
        # with open(file_path, "wb") as files:
        #     while True:
        #         chunk = req.stream.read(4096)
        #         if not chunk:
        #             break
        #         files.write(chunk)
        # resp.status = falcon.HTTP_200
        # resp.location = '/models/{}'.format(model.name)
        # resp._headers["Access-Control-Allow-Origin"] = "*"
        # resp.body = '{"success":true, "info":\"%s\"}' % data-


class ImageStore(object):
    _CHUNK_SIZE_BYTES = 4096

    def __init__(self, store_path, filename=None, open=io.open):
        self._storage_path = store_path
        self._filename = filename
        self._fopen = open

    def save(self, image_stream, image_content_type):
        ext = mimetypes.guess_extension(image_content_type)  #ext参数暂时用不上
        image_path = os.path.join(self._storage_path, self._filename)
        with self._open(image_path, 'wb') as image_file:
            while True:
                chunk = image_stream.read(self._CHUNK_SIZE_BYTES)
                if not chunk:
                    break
                image_file.write(chunk)
        return self._file_name

    def open(self, name):
        image_path = os.path.join(self._storage_path, name)
        stream = self._open(image_path, 'rb')
        stream_len = os.path.getsize(image_path)
        return stream, stream_len


def create_app(image_store):
    api = falcon.API()
    api.add_route('/upload', multipartupload(image_store))
    return api


def get_app():
    storage_path = os.environ.get('LOOK_STORAGE_PATH', '.')
    image_store = ImageStore(storage_path)
    return create_app(image_store)

# app=falcon.API(middleware=[MultipartMiddleware()])
# app.add_route("/upload", multipartupload())

httpd = simple_server.make_server("127.0.0.1", 8093, get_app())
httpd.serve_forever()

# from io import open
# import os
#
# import falcon
# from falcon_multipart.middleware import MultipartMiddleware
# import pytest
#
# application = falcon.API(middleware=MultipartMiddleware())
#
# @pytest.fixture
# def app():
#     return application
#
#
# def test_parse_form_as_params(client):
#     class Resource:
#         def on_post(self, req, resp, **kwargs):
#             assert req.get_param('simple') == 'ok'
#             assert req.get_param('afile').file.read() == b'filecontent'
#             assert req.get_param('afile').filename == 'afile.txt'
#             resp.body = 'parsed'
#             resp.content_type = 'text/plain'
#
#         application.add_route('/route', Resource())
#         resp = client.post('/route', data={
#             'simple': 'ok'}, files={'afile': ('filecontent', 'afile.txt')})
#         assert resp.status == falcon.HTTP_OK
#         assert resp.body == 'parsed'


