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
        self._connection = None
        self._connect()
        self._cursor = self._connection.cursor()

    def _connect(self):
        self._connection = pymysql.connect(
            host=self._host,
            user=self._user,
            password=self._password,
            db=self._db_name,
            charset=self._charset)

    def creat_table(self):
        pass

    def insert(self, table, data):
        pass

    def update(self):
        pass

    def query(self):
        pass

    def delete(self):
        pass

    def delete(self):
        pass

    def transact(self):
        pass

    def save(self):
        pass

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
