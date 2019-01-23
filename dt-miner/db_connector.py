#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pymysql


class MySQL_Connector():
    '''
    You can use this module to connect to the MySQL database and do some tasks.
    '''
    def __init__(self, host, user, password, db, charset='utf8mb4'):
        self._host = host
        self._user = user
        self._password = password
        self._db = db
        self._charset = charset

    def connect(self):
        pass

    def creat_table(self):
        pass

    def insert(self):
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
