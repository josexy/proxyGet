#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

import os
import random
import sqlite3
import pymysql
import proxy_config
from flask import Flask,request,session,render_template,g

app = Flask(__name__)
app.config.from_object('proxy_config')

def connect_sqlite3():
    if not os.path.exists(app.config['DATABASE_PATH']):
        g.db=None
        return g.db
    if not hasattr(g,'db'):
        try:
            g.db = sqlite3.connect(app.config['DATABASE_PATH'])
        except Exception as e:
            return None
    return g.db
def connect_mysql():
    if not hasattr(g,'db'):
        try:
            g.db = pymysql.Connection(
                host=app.config['MYSQL_HOST'],
                port=app.config['MYSQL_PORT'],
                user=app.config['MYSQL_USER'],
                password=app.config['MYSQL_PWD']
            )
        except Exception as e:
            return None
        g.db.select_db(app.config['DATABASE'])
    return g.db

@app.before_request
def connect_database():
    if app.config['SQL_TYPE']=='mysql':
        g.db=connect_mysql()
    else:
        g.db=connect_sqlite3()

@app.teardown_request
def close_database(exception):
    db = getattr(g,'db')
    if db is not None:
        db.close()

@app.route('/')
def index():
    session.pop('datas',None)
    return 'Welcome back'

@app.route('/ips')
def get_proxy():
    try:
        cursor = g.db.cursor()
        cursor.execute(f"select *from {app.config['TABLE']};")
        table_field = [x[0] for x in cursor.description]
        datas=[]
        row = cursor.fetchone()
        while row:
            datas.append(row)
            row = cursor.fetchone()
        session['datas']=datas
        return render_template('index.html',title='PROXY',table_field=table_field,datas=datas)
    except:
        return 'Error'

@app.route('/ip')
def get_per_random_ip():
    session.pop('datas',None)
    get_proxy()
    try:
        ip_tuple = random.choice(session['datas'])
    except:
        return 'Error'
    return '('+','.join([ip_tuple[1],ip_tuple[2]])+')'

def main(host=app.config['LISTEN_HOST'], port=app.config['LISTEN_PORT'], debug=app.config['DEBUG']):
    app.run(host, port, debug)

if __name__=='__main__':
    main()
