#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pymysql
import json
import warnings


class MySQL():
    '''
    Use this module to connect to the MySQL database and do some tasks.
    '''

    def __init__(self, host, user, password, db, charset='utf8mb4'):
        self._host = host
        self._user = user
        self._password = password
        self._db_name = db
        self._charset = charset
        self._db = None
        self._connect()
        self._cursor = self._db.cursor()

    def _connect(self):
        self._db = pymysql.connect(
            host=self._host,
            user=self._user,
            password=self._password,
            db=self._db_name,
            charset=self._charset)
        print('connect OK!')

    def _query(self, sql):
        try:
            result = self._cursor.execute(sql)
        except Exception as e:
            print(e)
            result = None
        return result

    def creat_table_if_not_exist(self, name, data):
        # 提供表名及表内数据结构字典
        is_exist_sql = 'show tables like "{}"'.format(name)
        self._query(is_exist_sql)
        if self._cursor.fetchall():
            warn_message = 'Table Create Error. Table "{}" already Exists!'.format(
                name).center(70, '-')
            warnings.warn('\n' + warn_message)
            return
        try:
            sql = 'create table if not exists {name} ({table_content})'.format(
                name=name,
                table_content=','.join(
                    ['{} {}'.format(key, data[key]) for key in data]))
            self._cursor.execute(sql)
            self._db.commit()
            print('Table "{}" created success!'.format(name))
        except Exception as e:
            self._db.rollback()
            print(e)

    def drop_table(self, name):
        # drop指定表
        is_exist_sql = 'show tables like "{}"'.format(name)
        self._query(is_exist_sql)
        if not self._cursor.fetchall():
            warn_message = 'Table "{}" Not Exist!'.format(name).center(70, '-')
            warnings.warn('\n' + warn_message)
            return
        try:
            sql = 'drop table {name}'.format(name=name)
            self._cursor.execute(sql)
            self._db.commit()
            print('Table "{}" Droped Success!'.format(name))
        except Exception as e:
            self._db.rollback()
            print(e)

    def insert(self, table, data):
        # 插入数据到指定table
        try:
            sql = 'insert into {table} ({keys}) values ({values})'.format(
                table=table,
                keys=','.join([key for key in data]),
                values=','.join(['"{}"'.format(data[key]) for key in data]))
            self._cursor.execute(sql)
            self._db.commit()
            # print('Insert Success!')
            return self._cursor.lastrowid
        except Exception as e:
            self._db.rollback()
            print(e)

    def update(self, table, data, condition):
        # 更新table中的数据
        try:
            sql = 'update {table} set {update_data}'.format(
                table=table,
                update_data=','.join(
                    ['{}={}'.format(key, data[key]) for key in data]))
            if condition != 'all':
                sql += 'where {}'.format(condition)
            self._cursor.execute(sql)
            self._db.commit()
            return self._cursor.lastrowid
        except Exception as e:
            self._db.rollback()
            print(e)

    def select(self, table, column='*', condition=''):
        if condition:
            condition = 'where ' + condition
        sql = 'select {column} from {table} {condition}'.format(
            column=column, table=table, condition=condition)
        self._query(sql)
        return self._cursor.fetchall()

    def delete(self, table, condition):
        # 删除table中的数据, condition为'all'时删除全部数据
        try:
            sql = 'delete from {table} {condition}'.format(
                table=table,
                condition='where {}'.format(condition)
                if condition != 'all' else '')
            self._cursor.execute(sql)
            self._db.commit()
            print('Delete item success!')
            # 返回受影响的行数
            return self._cursor.rowcount
        except Exception as e:
            self._db.rollback()
            print(e)

    def close(self):
        self._cursor.close()
        self._db.close()

    @staticmethod
    def load_config(config_file='config.key'):
        """
        file: config.key -- example:
        {
            "host": "localhost",
            "user": "user",
            "password": "password",
            "db": "db"
        }
        """
        with open(config_file) as f:
            return json.loads('\n'.join(f.readlines()))


def main():
    conf = MySQL.load_config()
    db = MySQL(conf['host'], conf['user'], conf['password'], conf['db'])
    from table import jobs
    db.creat_table_if_not_exist(jobs.NAME, jobs.TABLE_CONTENT)
    job_data = {
        'CITY': '上海',
        'PositionName': 'python',
        'Salary': 10000,
        'CompanyName': '你好公司'
    }
    ins_res = db.insert('jobs', job_data)
    print(ins_res)
    # del_res = db.delete('jobs', 'all')
    # print(del_res)
    db.close()


if __name__ == "__main__":
    main()
