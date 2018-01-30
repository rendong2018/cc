#-*-coding: utf-8 -*-

import pymysql
from config import Config

class Mysql(object):
    def __init__(self, table_name):
        self._config = Config(table_name=table_name)
        self._con = self.__get_con()
        print(self._con)
        self._cursor = self._con.cursor()

    def __get_con(self):
        print(type(self._config.host))
        print(self._config.host, self._config.user, self._config.password, self._config.db_name, self._config.port)
        db = pymysql.connect(host=self._config.host, user=self._config.user, passwd=self._config.password,
                             db=self._config.db_name, port=int(self._config.port), charset="utf8",  use_unicode=True)
        return db

    # def __del__(self):
    #     # self._cursor.close()
    #     self._con.close()

    def cursor(self):
        return self._cursor

    def commit(self):
        try:
            self._con.commit()
        except Exception as e:
            print(e)
            self._con.rollback()
        finally:
            self._con.close()

    def fetch_one(self, sql, params=None):
        """params 参数暂时先用不上"""
        try:
            self._cursor.execute(sql)
            result = self._cursor.fetchone()
            if result:
                return result
            else:
                result = False
                return result
        except Exception as e:
            raise(e)

    def fetch_many(self,sql):
        try:
            self._cursor.execute(sql)
            results = self._cursor.fetchmany()
            return results
        except Exception as e:
            raise(e)

    def fetch_all(self,sql):
        try:
            self._cursor.execute(sql)
            results = self._cursor.fetchall()
            return results
        except Exception as e:
            raise(e)

    def execute(self, sql):
        print(sql)

        self._cursor.execute(sql)
        # try:
        #     self._cursor.execute(sql)
        # except Exception as e:
        #     raise(e)


def main():
    db = Mysql(table_name = "")
    # db = Mysql(table_name="MYSQL")
    # """  firstName: '', lastName: '', passWord: '', email: '', liteLab: '', passWord2: '', email2: '', institutionName: """
    # sql = "create table if not exists register (firstName VARCHAR(20), lastName VARCHAR(20), passWord VARCHAR(20), email VARCHAR(20), liteLab VARCHAR(20), institutionName VARCHAR(20));"
    # db.execute(sql)
    # db.commit()




if __name__ == "__main__":
    main()

# """  firstName: '', lastName: '', passWord: '', email: '', liteLab: '', passWord2: '', email2: '', institutionName: '' """
#
# execute(cur_tmp= cur, sql_tmp= sql)
# execute(cur_tmp=cur, sql_tmp=sql)
# execute(cur_tmp = cur, sql_tmp=sql)
# execute(cur_tmp = cur, sql_tmp=sql)
# execute(cur_tmp = cur, sql_tmp=sql)
#
# commit(db)





