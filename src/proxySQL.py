
import os
import pymysql
import sqlite3
from warnings import filterwarnings
from server.collectProxyList import ProxyIpInfo
from proxyMessage import CliMessage,Color

class proxySQL(object):
    def __init__(self):
        super().__init__()
    def connect_db(self):pass
    def create_database(self,database_name):pass
    def create_table(self,table_name):pass
    def insert(self,*args):pass
    def remove(self,*args):pass
    def update(self,*args):pass
    def execute_sql(self, sql,*args):pass
    def close(self):pass
    def is_closed(self):pass
    def select_table(self,table_name=None):pass
    def select_database(self,database_name=None):pass
    def fetch_one_row(self):pass
class proxySQLite(proxySQL):
    def __init__(self,database_path,table_name=None,table_field=None,overwrite=False):
        super().__init__()
        if database_path=='db/test.db':
            if not os.path.exists('db'):
                os.mkdir('db')
        self.database_path=database_path
        self.table_field=table_field
        self.table_name=table_name
        self.is_open=False
        self.unique_export=False
        self.overwrite=overwrite
        self.connect_db()
    def __del__(self):
        if self.is_open:
            self.close()
    def connect_db(self):
        if self.is_open:
            return False
        if self.overwrite:
            if os.path.exists(self.database_path):
                os.unlink(self.database_path)
        try:
            self.conn=sqlite3.connect(self.database_path)
        except Exception as e:
            CliMessage.print_with_status(e.args,Color.Red,Color.Bold,None,'failed')
            CliMessage.print_with_status(f"Failed to connect SQLite database...",Color.Red,Color.Bold,None,'failed')
            exit(-1)
        self.is_open=True
        self.cursor = self.conn.cursor()
    def select_table(self,table_name=None):
        if table_name:
            self.table_name=table_name
    def find_exist(self,proxy):
        self.execute_sql(f"SELECT * FROM {self.table_name} WHERE proxies='{proxy}';")
        if self.cursor.fetchone():
            return True
        else:
            return False
    def execute_sql(self,sql):
        try:
            self.cursor.execute(sql)
            self.conn.commit()
        except:
            self.row_count = -1
            self.conn.rollback()
            return False
        return True
    def create_table(self,table_name=None):
        # table_field => ['ID','proxies','location','log_time']
        if table_name:
            self.table_name=table_name
        _sql=f"CREATE TABLE IF NOT EXISTS {self.table_name} (" \
             f"ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,{' TEXT,'.join(self.table_field)} " \
             f"TEXT," \
             f"log_time TIMESTAMP default (datetime('now', 'localtime'))" \
             f");"
        return self.execute_sql(_sql)
    def insert(self,values):
        _fmt=','.join([f'\'{{{i}}}\'' for i in range(len(self.table_field))])
        _sql=f"INSERT INTO {self.table_name}(proxies,location) VALUES ({_fmt});".format(*values)
        return self.execute_sql(_sql)
    def remove(self,prefix='proxies',value=None):
        _sql=f"DELETE FROM {self.table_name} WHERE {prefix}=\'{value}\';"
        return self.execute_sql(_sql)
    def update(self,proxies=None,new_value=None):
        _sql=f"UPDATE {self.table_name} SET location=\'{new_value}\' WHERE proxies=\'{proxies}\';"
        return self.execute_sql(_sql)
    def is_closed(self):
        return not self.is_open
    def close(self):
        if not self.is_closed():
            self.cursor.close()
            self.conn.close()
            self.is_open = False
    def fetch_one_row(self):
        sql=f'SELECT * FROM {self.table_name};'
        if not self.execute_sql(sql):
            return None
        row = self.cursor.fetchone()
        while row:
            yield row
            row=self.cursor.fetchone()
class proxyMySQL(proxySQL):
    def __init__(self,user,pwd,table_field=None,
                 table_name=None,database_name=None,
                 host='localhost',port=3306,overwrite=False):
        super().__init__()
        filterwarnings('ignore',category=pymysql.Warning)
        self.overwrite=overwrite
        self.database_name=database_name
        self.table_name=table_name
        self.is_open=False
        self.host=host
        self.port=port
        self.user=user
        self.pwd=pwd
        self.table_field=table_field
        self.unique_export=False
        self.connect_db()
    def __del__(self):
        if self.is_open:
            self.close()
    def connect_db(self):
        if self.is_open:
            return False
        try:
            self.conn = pymysql.Connection(host=self.host,user=self.user, password=self.pwd,port=self.port,charset='utf8')
        except pymysql.MySQLError as e:
            CliMessage.print_with_status(e.args,Color.Red,Color.Bold,None,'failed')
            CliMessage.print_with_status(f"Failed to connect MySQL Server...",Color.Red,Color.Bold,None,'failed')
            exit(-1)
        self.is_open=True
        self.cursor = self.conn.cursor()
        return True
    def execute_sql(self, sql,*args):
        try:
            self.cursor.execute(sql,*args)
            self.conn.commit()
        except:
            self.conn.rollback()
            return False
        return True
    def select_database(self,database_name=None):
        if database_name:
            self.database_name = database_name
        self.conn.select_db(database_name)
    def select_table(self,table_name=None):
        if table_name:
            self.table_name = table_name
    def create_database(self,database_name=None):
        if database_name:
            self.database_name=database_name
        if self.overwrite==True:
            sql_drop_db=f"DROP DATABASE IF EXISTS {self.database_name};"
            self.execute_sql(sql_drop_db)
        sql=f"CREATE DATABASE IF NOT EXISTS {self.database_name};"
        return self.execute_sql(sql)
    def create_table(self,table_name=None):
        self.conn.select_db(self.database_name)
        if table_name:
            self.table_name=table_name
        if self.overwrite:
            sql_drop_tb=f"DROP TABLE IF EXISTS {self.database_name}.{self.table_name}"
            self.execute_sql(sql_drop_tb)
        _tbs=' VARCHAR(50),'.join(self.table_field)
        sql=f"""
            CREATE TABLE IF NOT EXISTS {self.database_name}.{self.table_name}(
                ID INT AUTO_INCREMENT NOT NULL,
                {_tbs} VARCHAR(50),
                log_time DATETIME DEFAULT NOW(),
                CONSTRAINT {self.table_name}_PK PRIMARY KEY (ID)
                )ENGINE=InnoDB
                DEFAULT CHARSET=utf8mb4
                COLLATE=utf8mb4_unicode_ci;"""
        return self.execute_sql(sql)
    def find_exist(self,proxy):
        self.execute_sql(f"SELECT * FROM {self.database_name}.{self.table_name} WHERE proxies='{proxy}';")
        if self.cursor.fetchone():
            return True
        else:
            return False
    def insert(self,values):
        _field=','.join(self.table_field)
        _fmt=','.join(['%s']*len(self.table_field))
        sql=f"INSERT INTO {self.database_name}.{self.table_name}({_field}) VALUES({_fmt});"
        return self.execute_sql(sql,tuple(values))
    def remove(self,value=None):
        _sql=f"DELETE FROM {self.database_name}.{self.table_name} WHERE proxies='{value}';"
        return self.execute_sql(_sql)
    def update(self,proxies=None,new_value=None):
        _sql=f"UPDATE {self.database_name}.{self.table_name} SET location=\'{new_value}\' WHERE proxies=\'{proxies}\';"
        return self.execute_sql(_sql)
    def is_closed(self):
        try:
            self.conn.ping(False)
            return False
        except:
            return True
    def close(self):
        if not self.is_closed():
            self.cursor.close()
            self.conn.close()
            self.is_open=False
    def fetch_one_row(self):
        sql=f'SELECT * FROM {self.database_name}.{self.table_name};'
        if not self.execute_sql(sql):
            return None
        row = self.cursor.fetchone()
        while row:
            yield row
            row=self.cursor.fetchone()
