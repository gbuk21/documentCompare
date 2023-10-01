import flask
from flask import Flask
from flask import request,  jsonify, render_template, url_for , make_response
import json,os,re
import requests

import db_ops as dops

import functools

app = Flask(__name__)

app.secret_key="sight_words 1107"

from flask_paginate import Pagination, get_page_parameter

conn=dops.connect()
# files replace

    
@app.route('/<int:page>')
@app.route('/index/<int:page>')
@app.route('/index/')
@app.route('/')
def main_index(page=1):

    search = False
    q = request.args.get('q')
    if q:
        search = True
    documents=dops.get_distinct_documents(conn,"")

    if page is  None:
       page = request.args.get(get_page_parameter(), type=int, default=1)	
    pagination = Pagination(page=page, total=len(documents), search=search, record_name='documents',per_page=8)
    print(documents)

    return render_template('temp_index.html',  documents=documents,message_sent="All Documents",name="kiran",pagination=pagination)
    

@app.route('/get_document/<document_name>',methods=['GET'])
def show_version(document_name):
    
    versions=dops.get_distinct_document_versions(conn,"",document_name)
    print(versions)
    flask.session.pop('version1', None)
    flask.session.pop('version2', None)
    return render_template('choose_version.html',  document_name=document_name,versions=versions, message_sent='Document versions to compare',name="kiran")
   

@app.route('/compare_document_versions/<document_name>/<int:page>',methods=['POST','GET'])
@app.route('/compare_document_versions/<document_name>/',methods=['POST','GET'])
def show_compare(document_name,page=1):
    search = False
    q = request.args.get('q')
    if q:
        search = True

    print('i am here')
    try:
       version1=request.form['version1']
       flask.session['version1']=version1
    except:
       version1=flask.session['version1']
    print(version1)
    try:
       version2=request.form['version2'] 
       flask.session['version2']=version2
    except:
       version2=flask.session['version2']
    if page==1:
       doc_dff=dops.get_doc_differences(conn,"",document_name,version1, version2)
       flask.session['doc_dff']=doc_dff
    else:
       doc_dff=flask.session['doc_dff']
    print(doc_dff)
    try:
      for doc_dff_item in doc_dff:
          print(doc_dff_item['LineNumber'])
          for i in range(20):
              if (request.form['check'+str(i+1)])
    except:
      pass
    if page is  None:
       page = request.args.get(get_page_parameter(), type=int, default=1)	
    pagination = Pagination(page=page, total=len(doc_dff), search=search, record_name='doc_dff',per_page=1)

    return render_template('version_compare.html',  document_name=document_name,doc_dff=doc_dff, CurrentVersion=version1, previousversion=version2, message_sent='Document versions to compare',name="kiran",pagination=pagination)    

    
if __name__ == "__main__":
    app.run()
    
