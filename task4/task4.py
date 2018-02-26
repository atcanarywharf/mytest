import os
import requests
import sys
import json
import detectlanguage
import sqlite3 as sql
import matplotlib.pyplot as plt
import numpy as np
import shutil
from os.path import exists
from urllib.parse import quote
from flask import Flask, request, redirect, url_for, send_from_directory, render_template
from werkzeug.utils import secure_filename

mc_url = "http://api.meaningcloud.com/lang-2.0"
mc_keyvalue = "0d67b1a032357fccd83a37bc90db94bf"
ld_keyvalue = "83d7446cfd76915af8c948826baef0d6"



UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def read_file():
    if not exists('count.txt'):
        return 0
    f = open('count.txt')
    text = f.read()
    f.closed
    return int(text.rstrip())
    
n = read_file()

@app.route('/')
def welcome():
    conn = sql.connect('database.db')
    print("Opened database successfully")
    conn.execute('CREATE TABLE IF NOT EXISTS compare (mc TEXT, ld TEXT)')
    print("Table created successfully")
    conn.close()
    return render_template('welcome.html')

@app.route('/text', methods=['GET', 'POST'])
def input_text():
    if request.method == 'POST':
      text = request.form['content']
      return redirect(url_for('identified_text',text=text))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Input text</h1>
    <form action = "" id = "form" method = "post">
      <p><textarea rows="6" cols="50" name="content" form="form">Enter text here...</textarea></p>
      <p><input type = submit value = submit></p>      
    </form>   
    '''

def mc_identify(text):
    text = quote(text)
    payload = "key=" + mc_keyvalue + "&txt=" + text
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.request("POST", mc_url, data=payload, headers=headers)
    data = json.loads(response.text)
    languages = []
    for language in data['language_list']:
        languages.append(language['name'])
    if len(languages) == 0:
        return ""
    result = ", ".join(languages)
    return result

def ld_identify(text):
    detectlanguage.configuration.api_key = ld_keyvalue
    code = ""
    try:
        code = detectlanguage.simple_detect(text)
    except:
        return ""
    lanlist = detectlanguage.languages()
    result = ""
    for landict in lanlist:
        if landict['code'] == code:
            result = landict['name']
            break
    return result
    
@app.route('/textresult/<text>')
def identified_text(text):
    mc_result = mc_identify(text)
    ld_result = ld_identify(text)
    if mc_result == "" or ld_result == "":
        return "No language identified"
    return render_template("result.html",mc_result = mc_result, ld_result = ld_result)
    
    
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/uploads', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            return 'No file part'
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            return 'No selected file'
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file',
                                    filename=filename))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''

@app.route('/fileresult/<filename>')
def uploaded_file(filename):
    f = open(UPLOAD_FOLDER + '/' + filename)
    text = f.read()
    f.closed
    mc_result = mc_identify(text)
    ld_result = ld_identify(text)
    if mc_result == "" or ld_result == "":
        return "No language identified"
    return render_template("result.html",mc_result = mc_result, ld_result = ld_result)
    
@app.route('/db_op',methods = ['POST', 'GET'])
def db_op():
     
   con = sql.connect("database.db")
   if request.method == 'POST':
      global n 
      n = n + 1
      try:
         mc = request.form['mc']
         ld = request.form['ld']
         
         cur = con.cursor()           
         cur.execute("INSERT INTO compare (mc,ld) VALUES (?,?)",(mc,ld) )            
         con.commit()
      except:
         con.rollback()      
      finally:
         con.row_factory = sql.Row  
         cur = con.cursor()
         cur.execute("select count(*) from compare where mc = \'right\'")
         mc_row = cur.fetchone()
         mc_count = mc_row[0]
         cur.execute("select count(*) from compare where ld = \'right\'")
         ld_row = cur.fetchone()
         ld_count = ld_row[0]
         con.close()
         objects = ('MeanCloud', 'LanguageDetection')
         y_pos = np.arange(len(objects))
         performance = [mc_count, ld_count] 
         plt.bar(y_pos, performance, align='center', alpha=0.5)
         plt.xticks(y_pos, objects)
         plt.ylabel('The number of right times')
         plt.title('Compare performance of two services')
         if exists('static'):
            shutil.rmtree('static')         
         os.mkdir('static')
         plt.savefig('static/compare' + str(n) + '.png')
         write_file(n)
   return render_template("compare.html", n = n)

def write_file(n):
    f = open("count.txt", "w")
    f.write(str(n))
    f.close
   
if __name__ == "__main__":
   
   app.run(debug = True)