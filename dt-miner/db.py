#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pymysql
import json


class MySQL():
    '''
    You can use this module to connect to the MySQL database and do some tasks.
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

    def creat_table(self, name, data):
        # 提供表名及表内数据结构字典
        try:
            table_content = ''
            for key in data:
                table_content += '{} {},'.format(key, data[key])
            sql = 'create table {name} ({table_content})'.format(
                name=name, table_content=table_content)
            self._cursor.execute(sql)
            self._db.commit()
        except Exception as e:
            self._db.rollback()
            print(e)

    def insert(self, table, data):
        # 插入数据到指定table
        try:
            sql = 'insert into {table} ({key}) values ({values})'.format(
                table=table,
                key=','.join([key for key in data]),
                values=','.join([data[key] for key in data]))
            self._cursor.execute(sql)
            self._db.commit()
            return self._cursor.lastrowid
        except Exception as e:
            self._db.rollback()
            print(e)

    def update(self):
        pass

    def query(self, sql):
        try:
            result = self._cursor.execute(sql)
        except Exception as e:
            print(e)
            result = None
        return result

    def select(self):
        pass

    def delete(self):
        pass

    def transact(self):
        pass

    def save(self):
        self._db.save()

    def close(self):
        self._connection.close()


def load_config(config_file='config.key'):
    with open(config_file) as f:
        return json.loads('\n'.join(f.readlines()))


def main():
    conf = load_config()
    db = MySQL(conf['host'], conf['user'], conf['password'], conf['db'])


if __name__ == "__main__":
    main()
