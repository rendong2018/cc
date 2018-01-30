# coding:utf-8

import falcon
import json
import uuid
import pymysql
from login_api import *
from config import *

from wsgiref import simple_server

app = falcon.API()

app.req_options.auto_parse_form_urlencoded = True
app.req_options.keep_blank_qs_values = True

#from .common import *

import sys
reload(sys)
sys.setdefaultencoding('utf8')

# import MySQLdb

#连接数据库
# def linkDB():
#     conn=MySQLdb.connect(host='192.168.1.144',user='khl',passwd='121121',db='report',port=3306,charset='utf8')
#     return conn

#查询数据到字典
def my_query_sql(db,sql):


    # 数据修改操作——提交要求
    #cursor.execute(sql)
    #transaction.commit_unless_managed()

    # 数据检索操作,不需要提交
    # db.execute(sql)
    rawData = db.fetch_all(sql)
    col_names = [desc[0] for desc in db._cursor.description]
    print(col_names)
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
    def on_post(self, req, resp):
        params = req.params
        user_name = params["userName"]
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
            page = 0
        if params.has_key('version'):
            queryversion += params["version"].strip()
        if params.has_key('filter'):
            filter += params["filter"].strip()
        if params.has_key('type'):
            ngs_type += params["type"].strip()

        #连接数据库
        try:
            # conn = linkDB()
            conn = Mysql(table_name="REPORT_MYSQL")
        except:
            conn =None

        #返回状态码
        resp.status = falcon.HTTP_200
        #设置允许跨域请求
        resp._headers["Access-Control-Allow-Origin"] = "*"

        if conn:
            #创建游标
            # cursor = conn.cursor()
            #查询总数
            sql = 'SELECT count(1) AS total FROM projectName'
            foo = my_query_sql(conn,sql)
            result["total"] = foo[0]['total']
            #查询版本
            sql = 'SELECT GROUP_CONCAT(DISTINCT version) as totalVersion FROM projectName '
            foo = my_query_sql(conn, sql)
            result["totalVersion"] = (foo[0]['totalVersion']).split(',')

            sql = 'SELECT projectName AS "description",projectName AS "application",`version`,`datetime` AS "date",author,' \
                  ' REPLACE(templateWord,"/home/khl/web/word","http://192.168.1.144:8094") AS url FROM projectName WHERE 1=1 '

            if queryversion != '':
                sql += ' AND version="%s" '%(queryversion)

            if ngs_type != '':
                sql += ' AND ngs_type="%s" '%(ngs_type)

            if filter != '':
                sql += ' AND projectName LIKE "%'+filter.strip().replace('"','\\"')+'%" '

            # sql += ' LIMIT %d,%d' % ((page - 1) * size, size)
            # print('sql',sql)
            info = int(result["total"])
            print('total',info)
            range_tmp = range(info)
            mod = info % size  # 取余
            reminder = int(info / size)
            if mod != 0:
                if page == (reminder-1):
                    range_id = range_tmp[(size * (page - 1)):info]
                else:
                    range_id = range_tmp[(size * page):(size * (page + 1))]
                # if page == 1:
                #     range_id = range_tmp[0:size]
                # elif page == (reminder - 1):
                #     range_id = range_tmp[(size * (page - 1)):info]
                # else:
                #     print('haha', size * page, size * (page + 1))
                #     range_id = range_tmp[(size * page):(size * (page + 1))]
            else:
                range_id = range_tmp[(size * (page)):(size * (page+1))]
            sql += ' LIMIT %d,%d' % (range_id[0],(range_id[-1]+1))
            print('sql',sql)
            print('haha, range_id',range_id)
            result["info"] = my_query_sql(conn,sql)
            # sql = """select * from projectName;"""
            # result['total'] = len(db.fetch_all(sql))
            result["length"] = len(result["info"])
            result["success"] = True

            #关闭连接
            # conn.close()
            conn.commit()

        else:
            result["info"] = "Connect failure!"

        resp.body = json.dumps(result, ensure_ascii=False)


app.add_route('/analysis',Analysis())

if __name__ == '__main__':
    httpd = simple_server.make_server('192.168.1.144', 8111, app)
    httpd.serve_forever()
