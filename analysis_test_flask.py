# coding:utf-8

import falcon
import json
import uuid

from wsgiref import simple_server

app = falcon.API()

app.req_options.auto_parse_form_urlencoded = True
app.req_options.keep_blank_qs_values = True

#from .common import *

import sys
reload(sys)
sys.setdefaultencoding('utf8')

import MySQLdb

#连接数据库
def linkDB():
    conn=MySQLdb.connect(host='127.0.0.1',user='root',passwd='xy2017',db='report',port=3306,charset='utf8')
    return conn

#查询数据到字典
def my_query_sql(cursor,sql):


    # 数据修改操作——提交要求
    #cursor.execute(sql)
    #transaction.commit_unless_managed()

    # 数据检索操作,不需要提交
    cursor.execute(sql)
    rawData = cursor.fetchall()
    col_names = [desc[0] for desc in cursor.description]

    result = []
    for row in rawData:
        objDict = {}
        # 把每一行的数据遍历出来放到Dict中
        for index, value in enumerate(row):
            #objDict[col_names[index]] = str(value)
            objDict[col_names[index]] = str(value) if value else None

        result.append(objDict)

    return result


class Analysis(object):
    def on_get(self, req, resp):
        params = req.params
        result = {}
        result["success"] = False

        queryversion = ''
        filter = ''
        ngs_type = ''

        if params.has_key('size'):
            size = int(params["size"])
        else:
            size = 10
        if params.has_key('page'):
            page = int(params["page"])
        else:
            page = 1
        if params.has_key('version'):
            queryversion += params["version"].strip()
        if params.has_key('filter'):
            filter += params["filter"].strip()
        if params.has_key('type'):
            ngs_type += params["type"].strip()

        #连接数据库
        try:
            conn = linkDB()
        except:
            conn =None

        #返回状态码
        resp.status = falcon.HTTP_200
        #设置允许跨域请求
        resp._headers["Access-Control-Allow-Origin"] = "*"

        if conn:
            #创建游标
            cursor = conn.cursor()
            #查询总数
            sql = 'SELECT count(1) AS total FROM projectname'
            foo = my_query_sql(cursor,sql)
            result["total"] = foo[0]['total']
            #查询版本
            sql = 'SELECT GROUP_CONCAT(DISTINCT version) as totalVersion FROM projectname '
            foo = my_query_sql(cursor, sql)
            result["totalVersion"] = (foo[0]['totalVersion']).split(',')

            sql = 'SELECT projectName AS "description",projectName AS "application",`version`,`datetime` AS "date",author,' \
                  ' REPLACE(templateWord,"/home/khl/web/word","http://192.168.1.144:8094") AS url FROM projectname WHERE 1=1 '

            if queryversion != '':
                sql += ' AND version="%s" '%(queryversion)

            if ngs_type != '':
                sql += ' AND ngs_type="%s" '%(ngs_type)

            if filter != '':
                sql += ' AND projectName LIKE "%'+filter.strip().replace('"','\\"')+'%" '

            sql += ' LIMIT %d,%d' % ((page - 1) * size, size)

            result["info"] = my_query_sql(cursor,sql)

            result["length"] = len(result["info"])
            result["success"] = True

            #关闭连接
            conn.close()

        else:
            result["info"] = "Connect failure!"

        resp.body = json.dumps(result, ensure_ascii=False)


app.add_route('/analysis',Analysis())

if __name__ == '__main__':
    httpd = simple_server.make_server('127.0.0.1', 8080, app)
    httpd.serve_forever()
