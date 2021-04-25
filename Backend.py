from flask import Flask,request,json
import pandas as pd 
from gensim.models import Word2Vec
from pythainlp.tokenize import word_tokenize
import pythainlp.corpus as st
import numpy as np
import pymongo
from bson.objectid import ObjectId
from datetime import datetime
import random
import requests 
import json

client = pymongo.MongoClient("mongodb+srv://tum123456:ttt123456@cluster0.cfjjb.mongodb.net/<dbname>?retryWrites=true&w=majority")
db = client.test
mydb = db["MyProject"]

class machine:
    def __init__(self,label,a=1,b=1):
        self.label = label
        self.a = a
        self.b = b
        
    def update1(self,_id):
        mycol = mydb["TestRec"]
        mycol.update_one({'_id' : _id , 'data.label':self.label} , {"$inc": {'data.$.b': 1}})
        
    def update2(self,_id):
        mycol = mydb["TestRec"]
        mycol.update_one({'_id' : _id , 'data.label':self.label} , {"$set": {'data.$.a': self.a + 1}})
        mycol.update_one({'_id' : _id , 'data.label':self.label} , {"$set": {'data.$.b': self.b }})
        
    def reset(self,_id):
        mycol = mydb["TestRec"]
        mycol.update_one({'_id' : _id , 'data.label':self.label} , {"$set": {'data.$.a': 1}})
        mycol.update_one({'_id' : _id , 'data.label':self.label} , {"$set": {'data.$.b': 1}})
        
typew = [{"label":"กฎหมาย", "value":"กฎหมาย"},{"label":"การตลาด", "value":"การตลาด"},{"label":"เกษตร/จัดสวน/ปศุสัตว์/ประมง/เหมืองแร่", "value":"เกษตร/จัดสวน/ปศุสัตว์/ประมง/เหมืองแร่"},
        {"label":"ขาย", "value":"ขาย"},{"label":"เขียนแบบ/งานDrawing/AutoCad/ออกแบบวิศวกรรม", "value":"เขียนแบบ/งานDrawing/AutoCad/ออกแบบวิศวกรรม"},
        {"label":"คอมพิวเตอร์/IT/โปรแกรมเมอร์", "value":"คอมพิวเตอร์/IT/โปรแกรมเมอร์"},{"label":"งานการเงิน-ธนาคาร", "value":"งานการเงิน-ธนาคาร"},{"label":"งานขนส่ง-คลังสินค้า", "value":"งานขนส่ง-คลังสินค้า"},{"label":"งานนำเข้า-ส่งออก", "value":"งานนำเข้า-ส่งออก"},{"label":"งานบริการลูกค้า-Call Center", "value":"งานบริการลูกค้า-Call Center"},{"label":"งานบัญชี", "value":"งานบัญชี"},{"label":"งานบันเทิง/นักแสดง/นางแบบ/นักร้อง/Stylist/Costume", "value":"งานบันเทิง/นักแสดง/นางแบบ/นักร้อง/Stylist/Costume"},{"label":"จัดซื้อ/ธุรการ/ประสานงานทั่วไป", "value":"จัดซื้อ/ธุรการ/ประสานงานทั่วไป"},{"label":"เจ้าหน้าที่ความปลอดภัย(จป.)/สิ่งแวดล้อม/ISO", "value":"เจ้าหน้าที่ความปลอดภัย(จป.)/สิ่งแวดล้อม/ISO"},{"label":"ช่างเทคนิค/อิเลคโทรนิค/ซ่อมบำรุง/ช่างพิมพ์", "value":"ช่างเทคนิค/อิเลคโทรนิค/ซ่อมบำรุง/ช่างพิมพ์"},{"label":"นักเขียน/บรรณาธิการ/พิสูจน์อักษร/Copywriter/นักแปลภาษา", "value":"นักเขียน/บรรณาธิการ/พิสูจน์อักษร/Copywriter/นักแปลภาษา"},{"label":"บุคคล/ฝึกอบรม", "value":"บุคคล/ฝึกอบรม"},{"label":"ผลิต/ควบคุมคุณภาพ/โรงงาน", "value":"ผลิต/ควบคุมคุณภาพ/โรงงาน"},{"label":"ผู้จัดการ/ผู้อำนวยการ/MD/CEO", "value":"ผู้จัดการ/ผู้อำนวยการ/MD/CEO"},{"label":"แผนกรักษาความปลอดภัย/งานอาคารจอดรถ", "value":"แผนกรักษาความปลอดภัย/งานอาคารจอดรถ"},{"label":"แพทย์/เภสัชกร/สาธารณสุข", "value":"แพทย์/เภสัชกร/สาธารณสุข"},{"label":"ภูมิศาสตร์/แผนที่/GIS/ผังเมือง", "value":"ภูมิศาสตร์/แผนที่/GIS/ผังเมือง"},{"label":"แม่บ้าน/พี่เลี้ยง/คนสวน", "value":"แม่บ้าน/พี่เลี้ยง/คนสวน"},{"label":"โยธา/สำรวจ/สถาปัตย์/มัณฑนากร/ประเมินราคา", "value":"โยธา/สำรวจ/สถาปัตย์/มัณฑนากร/ประเมินราคา"},{"label":"ล่าม/มัคคุเทศก์/จองห้อง/จองตั๋ว", "value":"ล่าม/มัคคุเทศก์/จองห้อง/จองตั๋ว"},{"label":"เลขานุการ", "value":"เลขานุการ"},{"label":"วิจัย/วิเคราะห์ (เศรษฐศาสตร์/หุ้น/ประกันภัย/ธนาคาร)", "value":"วิจัย/วิเคราะห์ (เศรษฐศาสตร์/หุ้น/ประกันภัย/ธนาคาร)"},{"label":"วิทยาศาสตร์/Lab/วิจัยพัฒนา", "value":"วิทยาศาสตร์/Lab/วิจัยพัฒนา"},{"label":"วิศวกร", "value":"วิศวกร"},{"label":"ศิลปะ/กราฟฟิค/ออกแบบ/ช่างภาพ", "value":"ศิลปะ/กราฟฟิค/ออกแบบ/ช่างภาพ"},{"label":"ส่งเอกสาร/ขับรถ/ส่งผลิตภัณฑ์", "value":"ส่งเอกสาร/ขับรถ/ส่งผลิตภัณฑ์"},{"label":"สื่อสารมวลชน/นักข่าว/งานวิทยุ/โทรทัศน์/หนังสือพิมพ์", "value":"สื่อสารมวลชน/นักข่าว/งานวิทยุ/โทรทัศน์/หนังสือพิมพ์"},{"label":"สุขภาพ/โภชนาการ/ความงาม/ฟิตเนส/สปา", "value":"สุขภาพ/โภชนาการ/ความงาม/ฟิตเนส/สปา"},{"label":"เสื้อผ้า/สิ่งทอ/ช่างแพทเทิร์น", "value":"เสื้อผ้า/สิ่งทอ/ช่างแพทเทิร์น"},{"label":"ออกแบบเว็บไซต์/Web", "value":"ออกแบบเว็บไซต์/Web"},{"label":"อัญมณีและเครื่องประดับ", "value":"อัญมณีและเครื่องประดับ"},{"label":"อาจารย์/ครู/งานวิชาการ", "value":"อาจารย์/ครู/งานวิชาการ"},{"label":"อาหาร/เครื่องดื่ม/กุ๊ก/บาร์เทนเดอร์/พนักงานเสิร์ฟ", "value":"อาหาร/เครื่องดื่ม/กุ๊ก/บาร์เทนเดอร์/พนักงานเสิร์ฟ"},{"label":"งาน Part-time/พนักงานชั่วคราว", "value":"งาน Part-time/พนักงานชั่วคราว"},{"label":"Freelance", "value":"Freelance"},{"label":"อื่นๆ", "value":"อื่นๆ"}
    ]

words = st.thai_stopwords()
data = pd.read_excel("Book1.xlsx",index_col=0) 
word_not_important = ['หา','รับ','งาน','ทำหน้าที่','หน้าที่','ซ่อม','(',')','/']
app = Flask(__name__)

def plus(_id,label):
    #Employee_An
    #Employer_An
    mycol = mydb["TestRec"]
    mycol.update_one({'_id' : _id , 'data.label':label} , {"$inc": {'data.$.num': 1}})
    
def minus(_id,label):
    #Employee_An
    #Employer_An
    mycol = mydb["TestRec"]
    mycol.update_one({'_id' : _id , 'data.label':label} , {"$inc": {'data.$.num': -1}})
    
def get_num(_id,label):
    mycol = mydb["TestRec"]
    myquery = {"_id": _id}
    mydoc = mycol.find(myquery)
    mydoc = list(mydoc)
    for i in mydoc[0]['data']:
        if(i['label'] == label):
            return i['num']
            break
        
def lower(x):
    return x.lower()

def concerned_sentence(search,allsentence):
    arr = []
    for i in search:
        for j in allsentence:
            if(i.lower() in j['position']):
                arr.append(j['position'])
    return arr

def concerned_sentence1(search,allsentence):
    arr = []
    for i in search:
        for j in allsentence:
            if(i.lower() in j['job']):
                arr.append(j['job'])
    return arr

def clear_space(s):
    s = s.lower()
    global words,word_not_important
    ss = ''
    for i in s:
        if(i != '/'):
            if(i != ' '):
                ss+=i
    b = word_tokenize(s)
    bb = []
    for i in b:
        if(i ==  ' '):
            None
        elif(i in words):
            None
        elif(i in word_not_important):
            None
        else:
            bb.append(i)
    return bb

def send_Notifi(token,title,msg):
    API_ENDPOINT = "https://exp.host/--/api/v2/push/send"

    message = {
        'to': token,
        'sound': 'default',
        'title': title,
        'body': msg,
    }
    header = {
          'Content-Type': 'application/json',
    }
    # sending post request and saving response as response object 
    r = requests.post(url = API_ENDPOINT, data = json.dumps(message), headers=header) 
    # extracting response text  
    pastebin_url = r.text 
    print(r) 
    
    
    
data['Title'] = data['Title'].apply(lower)
all_work = [clear_space(i) for i in data['Title'].tolist()]


@app.route('/')
def home():
    ###print("Hello World")
    return "This is home page "

@app.route('/login_employee')
def login_employee():
    if(request.method == 'GET'):
        try:
            param1 = request.args.get('name')
            param2 = request.args.get('pass')
            mycol = mydb["Employee_Account"]
            result = mycol.find({ "Email":param1})
            result = list(result)
            if(len(result) != 0):
                if(param2 == result[0]['Password']):
                    response = {
                         'response' : 'Pass',
                         'mimetype' : 'application/json',
                         'data': json.dumps(result[0], default=str)
                    }
                else:
                    response = {
                         'response' : 'Not Pass',
                         'mimetype' : 'application/json'     
                    }
                    
            else:
                response = {
                     'response' : 'Not Pass',
                     'mimetype' : 'application/json'     
                }
        except :
            response = {
                 'response' : 'Cannot',
                 'mimetype' : 'application/json'     
            }
        return response

@app.route('/login_employer')
def login_employer():
    if(request.method == 'GET'):
        try:
            param1 = request.args.get('name')
            param2 = request.args.get('pass')
            mycol = mydb["Employer_Account"]
            result = mycol.find({ "Email":param1})
            result = list(result)
            if(len(result) != 0):
                if(param2 == result[0]['Password']):
                    response = {
                         'response' : 'Pass',
                         'mimetype' : 'application/json',
                         'data': json.dumps(result[0], default=str)
                    }
                else:
                    response = {
                         'response' : 'Not Pass',
                         'mimetype' : 'application/json'     
                    }
                    
            else:
                response = {
                     'response' : 'Not Pass',
                     'mimetype' : 'application/json'     
                }
        except :
            response = {
                 'response' : 'Cannot',
                 'mimetype' : 'application/json'     
            }
        return response

@app.route('/forgotPassword', methods=['GET','POST'])
def forgotPassword():
    if(request.method == 'POST'):
        ###print(request.json)
        try:
            data = request.json
            if(data['mode'] == 'Employee'):
                mycol = mydb["Employee_Account"]
            else:
                mycol = mydb["Employer_Account"]
            result = mycol.find({ "Email":data["Email"]})
            result = list(result)
            print(result[0]['ID'] == data['ID'] )
            if(result[0]['ID'] == data['ID'] and result[0]['Question'] == data['Question'] and result[0]['Answer'] == data['Answer'] ):
                response = {
                     'response' : 'Pass',
                     'mimetype' : 'application/json'     
                }
            else:
                response = {
                     'response' : 'Not Pass',
                     'mimetype' : 'application/json'     
                }
        except:
            response = {
                 'response' : 'Cannot',
                 'mimetype' : 'application/json'     
            }
        return response

@app.route('/resetPassword', methods=['GET','POST'])
def resetPassword():
    if(request.method == 'POST'):
        ###print(request.json)
        try:
            data = request.json
            if(data['mode'] == 'Employee'):
                mycol = mydb["Employee_Account"]
                find = { '_id': data['id'] }
                newvalues = { "$set": { 'Password': data['Password1'] } } 
                mycol.update_one(find, newvalues)
                response = {
                     'response' : 'Pass',
                     'mimetype' : 'application/json'     
                }
            else:
                mycol = mydb["Employer_Account"]
                find = { '_id': data['email'] }
                newvalues = { "$set": { 'age': data['age'] } } 
                mycol.update_one(find, newvalues)
                response = {
                     'response' : 'Pass',
                     'mimetype' : 'application/json'     
                }
        except:
            response = {
                 'response' : 'Cannot',
                 'mimetype' : 'application/json'     
            }
        return response

@app.route('/search_job', methods=['GET','POST'])
def search_job():
    if(request.method == 'GET'):
        param = request.args.get('search')
        ###print(param)
        search_word = param
        search = clear_space(search_word)
        mycol = mydb["Employer_Annoucment"]
        result = mycol.find({})
        result = list(result)
        select_sentence = concerned_sentence(search,result)
        ####print(select_sentence)
        ####print(search)
        if(len(select_sentence) > 0):
            x = [clear_space(ss) for ss in select_sentence]
            ###print(x)
            model = Word2Vec(x, min_count=1,size = 500)
            ###print(model)
            ###print(model.wv.vocab)
            a = []
            a += search
            try:
                for t in search:
                    text = ''
                    if(t in model.wv.vocab):
                        text = t
                    else:
                        for ii in model.wv.vocab:
                            if(t in ii):
                                text = ii
                                break
                    aa=model.most_similar(text)
                    list_of_word = [i[0] for i in aa]
                    a += list_of_word
                        
                    a = np.array(a) 
                    a = np.unique(a)
                        
                    ###print("===== RESULT =====")
                    ###print(a)
                    ###print("===== RESULT =====")
                    lst = []
                    id_s = []
                    for i in a:
                        for j in result:
                            if(i in j['position']):
                                if(j['_id'] not in id_s):
                                    lst.append(j)
                                    id_s.append(j['_id'])
                    ###print(lst)
                    ###print("result = "+str(len(lst)))
                    ###print("all = "+str(len(result)))
                    lst =json.dumps(lst, default=str)
                    response = {
                        'response' : "find",
                        'data':lst,
                        'mimetype' : 'application/json'
                    }
            except:
                response = {
                 'response' : 'ไม่สามารถทำได้',
                 'mimetype' : 'application/json'
                }
        else:
            response = {
             'response' : 'ไม่มีงานอยุ่ในระบบ',
             'mimetype' : 'application/json'
            }
        
        return response

@app.route('/search_employee', methods=['GET','POST'])
def search_employee():
    if(request.method == 'GET'):
        param = request.args.get('search')
        ###print(param)
        search_word = param
        search = clear_space(search_word)
        mycol = mydb["Employee_Annoucment"]
        result = mycol.find({})
        result = list(result)
        select_sentence = concerned_sentence1(search,result)
        ####print(select_sentence)
        ####print(search)
        if(len(select_sentence) > 0):
            x = [clear_space(ss) for ss in select_sentence]
            ###print(x)
            model = Word2Vec(x, min_count=1,size = 500)
            ###print(model)
            ###print(model.wv.vocab)
            a = []
            a += search
            try:
                for t in search:
                    text = ''
                    if(t in model.wv.vocab):
                        text = t
                    else:
                        for ii in model.wv.vocab:
                            if(t in ii):
                                text = ii
                                break
                    aa=model.most_similar(text)
                    list_of_word = [i[0] for i in aa]
                    a += list_of_word
                        
                    a = np.array(a) 
                    a = np.unique(a)
                        
                    ###print("===== RESULT =====")
                    ###print(a)
                    ###print("===== RESULT =====")
                    lst = []
                    id_s = []
                    for i in a:
                        for j in result:
                            if(i in j['job']):
                                if(j['_id'] not in id_s):
                                    lst.append(j)
                                    id_s.append(j['_id'])
                    ###print(lst)
                    ###print("result = "+str(len(lst)))
                    ###print("all = "+str(len(result)))
                    lst =json.dumps(lst, default=str)
                    response = {
                        'response' : "find",
                        'data':lst,
                        'mimetype' : 'application/json'
                    }
            except:
                response = {
                 'response' : 'ไม่สามารถทำได้',
                 'mimetype' : 'application/json'
                }
        else:
            response = {
             'response' : 'ไม่มีงานอยุ่ในระบบ',
             'mimetype' : 'application/json'
            }
        
        return response

@app.route('/Employee_Register', methods=['GET','POST'])
def Employee_Register():
    if(request.method == 'POST'):
        ###print(request.json)
        try:
            data = request.json
            mycol = mydb["Employee_Account"]
            result = mycol.find({ "Email":data["Email"]})
            result = list(result)
            result1 = mycol.find({"ID":data["ID"]})
            result1 = list(result1)
            if(len(result) == 0 and len(result1) == 0):
                js = request.json
                data = [{'label':typew[i]['label'],'a':1,'b':1} for i in range(41)]
                js['data'] = data
                print(js)
                mycol.insert_one(js)
                response = {
                     'response' : 'Pass',
                     'mimetype' : 'application/json'     
                }
            else:
                response = {
                     'response' : 'Not Pass',
                     'mimetype' : 'application/json'     
                }
        except:
            response = {
                 'response' : 'Cannot',
                 'mimetype' : 'application/json'     
            }
        return response

@app.route('/Employer_Register', methods=['GET','POST'])
def Employer_Register():
    if(request.method == 'POST'):
        try:
            data = request.json
            mycol = mydb["Employer_Account"]
            result = mycol.find({ "Email":data["Email"]})
            result = list(result)
            result1 = mycol.find({"ID":data["ID"]})
            result1 = list(result1)
            if(len(result) == 0 and len(result1) == 0):
                js = request.json
                data = [{'label':typew[i]['label'],'a':1,'b':1} for i in range(41)]
                js['data'] = data
                print(js)
                mycol.insert_one(js)
                response = {
                     'response' : 'Pass',
                     'mimetype' : 'application/json'     
                }
            else:
                response = {
                     'response' : 'Not Pass',
                     'mimetype' : 'application/json'     
                }
        except:
            response = {
                 'response' : 'Cannot',
                 'mimetype' : 'application/json'     
            }
        return response

@app.route('/Employee_StatusEdit', methods=['GET','POST'])
def Employee_StatusEdit():
    if(request.method == 'POST'):
        ###print(request.json)
        try:
            data = request.json
            mycol = mydb["Employee_Account"]
            find = { '_id': data['email'] }
            newvalues = { "$set": { 'age': data['age'] } } 
            mycol.update_one(find, newvalues)
            newvalues = { "$set": { 'sex': data['sex'] } } 
            mycol.update_one(find, newvalues)
            newvalues = { "$set": { 'nation': data['nation'] } } 
            mycol.update_one(find, newvalues)
            newvalues = { "$set": { 'religion': data['religion'] } } 
            response = {
                 'response' : 'Pass',
                 'mimetype' : 'application/json'     
            }
        except:
            response = {
                 'response' : 'Cannot',
                 'mimetype' : 'application/json'     
            }
        return response

@app.route('/Employee_Annoucment', methods=['GET','POST','DELETE'])
def Employee_Annoucment():
    if(request.method == 'POST'):
        ###print(request.json)
        try:
            data = request.json
            mycol = mydb["Employee_Annoucment"]
            mycol.insert_one(data)
            plus('Employee_An',data['jobType'])
            response = {
                 'response' : 'Pass',
                 'mimetype' : 'application/json'     
            }
        except:
            response = {
                 'response' : 'Cannot',
                 'mimetype' : 'application/json'     
            }
        return response
    elif(request.method == 'GET'):
        param = request.args.get('want')
        ###print(param)
        try:
            mycol = mydb["Employee_Annoucment"]
            if(param == 'all'):
                result = mycol.find({})
                result = list(result)
                ###print(result)
                response = {
                     'data': json.dumps(result, default=str),
                     'response' : 'Pass',
                     'mimetype' : 'application/json'     
                }
            else:
                result = mycol.find({ "owner":param})
                result = list(result)
                ###print(result)
                response = {
                     'data': json.dumps(result, default=str),
                     'response' : 'Pass',
                     'mimetype' : 'application/json'     
                }
        except:
            response = {
                 'response' : 'Cannot',
                 'mimetype' : 'application/json'     
            }
        return response
    elif(request.method == 'DELETE'):
        param = request.args.get('want')
        ###print(param)
        try:
            mycol = mydb["Employee_Annoucment"]
            myquery = { "_id": ObjectId(param) }
            result = mycol.find(myquery)
            result = list(result)[0]['jobType']
            minus('Employee_An',result)
            print(result)
            mycol.delete_one(myquery)
            response = {
                 'response' : 'Pass',
                 'mimetype' : 'application/json'     
            }
        except:
            response = {
                 'response' : 'Cannot',
                 'mimetype' : 'application/json'     
            }
        return response
    
@app.route('/Employer_Annoucment', methods=['GET','POST','DELETE'])
def Employer_Annoucment():
    if(request.method == 'GET'):
        param = request.args.get('want')
        ###print(param)
        try:
            mycol = mydb["Employer_Annoucment"]
            if(param == 'all'):
                result = mycol.find({})
                result = list(result)
                ###print(result)
                response = {
                     'data': json.dumps(result, default=str),
                     'response' : 'Pass',
                     'mimetype' : 'application/json'     
                }
            else:
                result = mycol.find({ "owner":param})
                result = list(result)
                ###print(result)
                response = {
                     'data': json.dumps(result, default=str),
                     'response' : 'Pass',
                     'mimetype' : 'application/json'     
                }
        except:
            response = {
                 'response' : 'Cannot',
                 'mimetype' : 'application/json'     
            }
        return response
    
    elif(request.method == 'POST'):
        ###print(request.json)
        try:
            data = request.json
            print(data)
            mycol = mydb["Employer_Annoucment"]
            mycol.insert_one(data)
            plus('Employer_An',data['jobType'])
            response = {
                 'response' : 'Pass',
                 'mimetype' : 'application/json'     
            }
        except:
            response = {
                 'response' : 'Cannot',
                 'mimetype' : 'application/json'     
            }
        return response
    elif(request.method == 'DELETE'):
        param = request.args.get('want')
        ###print(param)
        try:
            mycol = mydb["Employer_Annoucment"]
            myquery = { "_id": ObjectId(param) }
            result = mycol.find(myquery)
            result = list(result)[0]['jobType']
            print(result)
            minus('Employer_An',result)
            mycol.delete_one(myquery)
            response = {
                 'response' : 'Pass',
                 'mimetype' : 'application/json'     
            }
        except:
            response = {
                 'response' : 'Cannot',
                 'mimetype' : 'application/json'     
            }
        return response
 
@app.route('/Employer_Profile', methods=['GET'])
def Employer_Profile():
    if(request.method == 'GET'):
        param = request.args.get('want')
        ###print(param)
        try:
            mycol = mydb["Employer_Account"]
            if(param == 'all'):
                result = mycol.find({})
                result = list(result)
                ###print(result)
                response = {
                     'data': json.dumps(result, default=str),
                     'response' : 'Pass',
                     'mimetype' : 'application/json'     
                }
            else:
                result = mycol.find({ "_id":param})
                result = list(result)
                ###print(result)
                response = {
                     'data': json.dumps(result, default=str),
                     'response' : 'Pass',
                     'mimetype' : 'application/json'     
                }
        except:
            response = {
                 'response' : 'Cannot',
                 'mimetype' : 'application/json'     
            }
        return response

@app.route('/Company_Contact_Edit', methods=['GET','POST'])
def Company_Contact_Edit():
    if(request.method == 'GET'):
        param = request.args.get('want')
        ###print(param)
        try:
            mycol = mydb["Employer_Account"]
            if(param == 'all'):
                result = mycol.find({})
                result = list(result)
                ###print(result)
                response = {
                     'data': json.dumps(result, default=str),
                     'response' : 'Pass',
                     'mimetype' : 'application/json'     
                }
            else:
                result = mycol.find({ "_id":param})
                result = list(result)
                ###print(result)
                response = {
                     'data': json.dumps(result, default=str),
                     'response' : 'Pass',
                     'mimetype' : 'application/json'     
                }
        except:
            response = {
                 'response' : 'Cannot',
                 'mimetype' : 'application/json'     
            }
        return response
    
    elif(request.method == 'POST'):
        ###print(request.json)
        try:
            data = request.json
            ###print(data)
            mycol = mydb["Employer_Account"]
            find = { 'Email': data['Email'] }
            newvalues = { "$set": { 'contact': data['contact'] } } 
            mycol.update_one(find, newvalues)
            response = {
                 'response' : 'Pass',
                 'mimetype' : 'application/json'     
            }
        except:
            response = {
                 'response' : 'Cannot',
                 'mimetype' : 'application/json'     
            }
        return response
    
@app.route('/Company_Information_Edit', methods=['GET','POST'])
def Company_Information_Edit():
    if(request.method == 'GET'):
        param = request.args.get('want')
        ###print(param)
        try:
            mycol = mydb["Employer_Account"]
            if(param == 'all'):
                result = mycol.find({})
                result = list(result)
                ###print(result)
                response = {
                     'data': json.dumps(result, default=str),
                     'response' : 'Pass',
                     'mimetype' : 'application/json'     
                }
            else:
                result = mycol.find({ "_id":param})
                result = list(result)
                ###print(result)
                response = {
                     'data': json.dumps(result, default=str),
                     'response' : 'Pass',
                     'mimetype' : 'application/json'     
                }
        except:
            response = {
                 'response' : 'Cannot',
                 'mimetype' : 'application/json'     
            }
        return response
    
    elif(request.method == 'POST'):
        ###print(request.json)
        try:
            data = request.json
            ###print(data)
            mycol = mydb["Employer_Account"]
            find = { 'Email': data['Email'] }
            newvalues = { "$set": { 'information': data['information'] } } 
            mycol.update_one(find, newvalues)
            find = { 'Email': data['Email'] }
            newvalues = { "$set": { 'companyName': data['companyName'] } } 
            mycol.update_one(find, newvalues)
            response = {
                 'response' : 'Pass',
                 'mimetype' : 'application/json'     
            }
        except:
            response = {
                 'response' : 'Cannot',
                 'mimetype' : 'application/json'     
            }
        return response

@app.route('/Job_Description', methods=['GET'])
def Job_Description():
    if(request.method == 'GET'):
        param = request.args.get('want')
        try:
            mycol = mydb["Employer_Annoucment"]
            if(param == 'all'):
                result = mycol.find({})
                result = list(result)
                ###print(result)
                response = {
                     'data': json.dumps(result, default=str),
                     'response' : 'Pass',
                     'mimetype' : 'application/json'     
                }
            else:
                result = mycol.find({ "_id": ObjectId(param) })
                result = list(result)
                ###print(result)
                response = {
                     'data': json.dumps(result, default=str),
                     'response' : 'Pass',
                     'mimetype' : 'application/json'     
                }
        except:
            response = {
                 'response' : 'Cannot',
                 'mimetype' : 'application/json'     
            }
        return response

@app.route('/Job_Annoucement_Edit', methods=['GET','POST'])
def Job_Annoucement_Edit():
    if(request.method == 'GET'):
        param = request.args.get('want')
        try:
            mycol = mydb["Employer_Annoucment"]
            if(param == 'all'):
                result = mycol.find({})
                result = list(result)
                ###print(result)
                response = {
                     'data': json.dumps(result, default=str),
                     'response' : 'Pass',
                     'mimetype' : 'application/json'     
                }
            else:
                result = mycol.find({ "_id": ObjectId(param) })
                result = list(result)
                ###print(result)
                response = {
                     'data': json.dumps(result, default=str),
                     'response' : 'Pass',
                     'mimetype' : 'application/json'     
                }
        except:
            response = {
                 'response' : 'Cannot',
                 'mimetype' : 'application/json'     
            }
        return response

    elif(request.method == 'POST'):
        try:
            mycol = mydb["Employer_Annoucment"]
            data = request.json
            find = { '_id': ObjectId(data['objID']) }
            newvalues = { "$set": { 'position': data['position'] } }       
            mycol.update_one(find, newvalues)
            newvalues = { "$set": { 'location': data['location'] } }
            mycol.update_one(find, newvalues)
            newvalues = { "$set": { 'workingAge': data['workingAge'] } }
            mycol.update_one(find, newvalues)
            newvalues = { "$set": { 'Description': data['Description'] } }
            mycol.update_one(find, newvalues)
            newvalues = { "$set": { 'jobType': data['jobType'] } }
            mycol.update_one(find, newvalues)
            newvalues = { "$set": { 'Compensation': data['Compensation'] } }
            mycol.update_one(find, newvalues)
            newvalues = { "$set": { 'Properties': data['Properties'] } }
            mycol.update_one(find, newvalues)
            newvalues = { "$set": { 'Benefits': data['Benefits'] } }
            mycol.update_one(find, newvalues)
            newvalues = { "$set": { 'experience': data['experience'] } }
            mycol.update_one(find, newvalues)


            ###print(result)
            response = {
                'response' : 'Pass',
                'mimetype' : 'application/json'     
            }
        except:
            response = {
                 'response' : 'Cannot',
                 'mimetype' : 'application/json'     
            }
        return response

@app.route('/Application', methods=['GET'])
def Application():
    if(request.method == 'GET'):
        param = request.args.get('want')
        ###print(param)
        try:
            mycol = mydb["Employer_Annoucment"]
            if(param == 'all'):
                result = mycol.find({})
                result = list(result)
                ###print(result)
                response = {
                     'data': json.dumps(result, default=str),
                     'response' : 'Pass',
                     'mimetype' : 'application/json'     
                }
            else:
                result = mycol.find({ "_id": ObjectId(param) })
                result = list(result)
                ###print(result)
                response = {
                     'data': json.dumps(result, default=str),
                     'response' : 'Pass',
                     'mimetype' : 'application/json'     
                }
        except:
            response = {
                 'response' : 'Cannot',
                 'mimetype' : 'application/json'     
            }
        return response

@app.route('/Employee_Profile', methods=['GET'])
def Employee_Profile():
    if(request.method == 'GET'):
        param = request.args.get('want')
        try:
            mycol = mydb["Employee_Account"]
            if(param == 'all'):
                result = mycol.find({})
                result = list(result)
                ####print(result)
                response = {
                     'data': json.dumps(result, default=str),
                     'response' : 'Pass',
                     'mimetype' : 'application/json'     
                }
            else:
                result = mycol.find({ "_id":param})
                result = list(result)
                ####print(result)
                response = {
                     'data': json.dumps(result, default=str),
                     'response' : 'Pass',
                     'mimetype' : 'application/json'     
                }
        except:
            response = {
                 'response' : 'Cannot',
                 'mimetype' : 'application/json'     
            }
        return response

@app.route('/Hiring', methods=['GET'])
def Hiring():
    if(request.method == 'GET'):
        param = request.args.get('want')
        ####print(param)
        try:
            mycol = mydb["Employer_Account"]
            if(param == 'all'):
                result = mycol.find({})
                result = list(result)
                ####print(result)
                response = {
                     'data': json.dumps(result, default=str),
                     'response' : 'Pass',
                     'mimetype' : 'application/json'     
                }
            else:
                result = mycol.find({ "_id":param})
                result = list(result)
                ####print(result)
                response = {
                     'data': json.dumps(result, default=str),
                     'response' : 'Pass',
                     'mimetype' : 'application/json'     
                }
        except:
            response = {
                 'response' : 'Cannot',
                 'mimetype' : 'application/json'     
            }
        return response

@app.route('/Application_Profile', methods=['GET'])
def Application_Profile():
    if(request.method == 'GET'):
        param = request.args.get('want')
        ####print("param = " + param)
        try:
            mycol = mydb["Employee_Account"]
            if(param == 'all'):
                result = mycol.find({})
                result = list(result)
                ####print(result)
                response = {
                     'data': json.dumps(result, default=str),
                     'response' : 'Pass',
                     'mimetype' : 'application/json'     
                }
            else:
                result = mycol.find({ "_id":param})
                result = list(result)
                ####print(result)
                response = {
                     'data': json.dumps(result, default=str),
                     'response' : 'Pass',
                     'mimetype' : 'application/json'     
                }
        except:
            response = {
                 'response' : 'Cannot',
                 'mimetype' : 'application/json'     
            }
        return response

@app.route('/bookmark', methods=['GET','POST'])
def bookmark():
    if(request.method == 'GET'):
        param = request.args.get('want')
        try:
            mycol = mydb["Employee_Account"]
            if(param == 'all'):
                result = mycol.find({})
                result = list(result)
                ####print(result)
                response = {
                     'data': json.dumps(result, default=str),
                     'response' : 'Pass',
                     'mimetype' : 'application/json'     
                }
            else:
                result = mycol.find({ "_id":param})
                result = list(result)
                ####print(result)
                response = {
                     'data': json.dumps(result, default=str),
                     'response' : 'Pass',
                     'mimetype' : 'application/json'     
                }
        except:
            response = {
                 'response' : 'Cannot',
                 'mimetype' : 'application/json'     
            }
        return response
    if(request.method == 'POST'):
        try:
            data = request.json
            ####print(data['Email'])
            ####print(data['Employee_Email'])
            ####print(data)
            mycol = mydb["Employer_Account"]
            if(data['checkBookmark'] == False):
                mycol.update(
                    { '_id' : data['Email'] },
                    { '$push' : {'bookmark' : data['Employee_Email']} }
                )
            else:
                mycol.update(
                    { '_id' : data['Email'] },
                    { '$pull' : {'bookmark' : data['Employee_Email']} }
                )
            response = {
                'response' : 'Pass',
                    'mimetype' : 'application/json'     
            }
        except:
            response = {
                 'response' : 'Cannot',
                 'mimetype' : 'application/json'     
            }
            
        return response

@app.route('/bookmark_Employer', methods=['GET'])
def bookmark_Employer():
    if(request.method == 'GET'):
        param = request.args.get('want')
        try:
            mycol = mydb["Employer_Account"]
            if(param == 'all'):
                result = mycol.find({})
                result = list(result)
                ####print(result)
                response = {
                     'data': json.dumps(result, default=str),
                     'response' : 'Pass',
                     'mimetype' : 'application/json'     
                }
            else:
                result = mycol.find({ "_id":param})
                result = list(result)
                ####print(result)
                response = {
                     'data': json.dumps(result, default=str),
                     'response' : 'Pass',
                     'mimetype' : 'application/json'     
                }
        except:
            response = {
                 'response' : 'Cannot',
                 'mimetype' : 'application/json'     
            }
        return response

@app.route('/Education_Edit', methods=['GET','POST'])
def Education_Edit():
    if(request.method == 'GET'):
        param = request.args.get('want')
        ####print(param)
        try:
            mycol = mydb["Employee_Account"]
            if(param == 'all'):
                result = mycol.find({})
                result = list(result)
                ####print(result)
                response = {
                     'data': json.dumps(result, default=str),
                     'response' : 'Pass',
                     'mimetype' : 'application/json'     
                }
            else:
                result = mycol.find({ "_id":param})
                result = list(result)
                ####print(result)
                response = {
                     'data': json.dumps(result, default=str),
                     'response' : 'Pass',
                     'mimetype' : 'application/json'     
                }
        except:
            response = {
                 'response' : 'Cannot',
                 'mimetype' : 'application/json'     
            }
        return response
    
    elif(request.method == 'POST'):
        ####print(request.json)
        try:
            data = request.json
            ####print(data)
            mycol = mydb["Employee_Account"]
            find = { 'Email': data['Email'] }
            newvalues = { "$set": { 'university': data['university'] } } 
            mycol.update_one(find, newvalues)
            newvalues = { "$set": { 'degree': data['degree'] } } 
            mycol.update_one(find, newvalues)
            newvalues = { "$set": { 'major': data['major'] } } 
            mycol.update_one(find, newvalues)
            newvalues = { "$set": { 'year': data['year'] } } 
            mycol.update_one(find, newvalues)
            newvalues = { "$set": { 'grade': data['grade'] } }             
            mycol.update_one(find, newvalues)

            response = {
                 'response' : 'Pass',
                 'mimetype' : 'application/json'     
            }
        except:
            response = {
                 'response' : 'Cannot',
                 'mimetype' : 'application/json'     
            }
        return response

@app.route('/Annoucement_Profle', methods=['GET'])
def Annoucement_Profle():
    if(request.method == 'GET'):
        param = request.args.get('want')
        try:
            mycol = mydb["Employee_Annoucment"]
            if(param == 'all'):
                result = mycol.find({})
                result = list(result)
                ####print(result)
                response = {
                     'data': json.dumps(result, default=str),
                     'response' : 'Pass',
                     'mimetype' : 'application/json'     
                }
            else:
                result = mycol.find({ "_id": ObjectId(param) })
                result = list(result)
                ####print(result)
                response = {
                     'data': json.dumps(result, default=str),
                     'response' : 'Pass',
                     'mimetype' : 'application/json'     
                }
        except:
            response = {
                 'response' : 'Cannot',
                 'mimetype' : 'application/json'     
            }
        return response

@app.route('/Annoucement_Edit', methods=['GET'])
def Annoucement_Edit():
    if(request.method == 'GET'):
        param = request.args.get('want')
        try:
            mycol = mydb["Employee_Annoucment"]
            if(param == 'all'):
                result = mycol.find({})
                result = list(result)
                ####print(result)
                response = {
                     'data': json.dumps(result, default=str),
                     'response' : 'Pass',
                     'mimetype' : 'application/json'     
                }
            else:
                result = mycol.find({ "_id": ObjectId(param) })
                result = list(result)
                ####print(result)
                response = {
                     'data': json.dumps(result, default=str),
                     'response' : 'Pass',
                     'mimetype' : 'application/json'     
                }
        except:
            response = {
                 'response' : 'Cannot',
                 'mimetype' : 'application/json'     
            }
        return response

@app.route('/Currenting_Job', methods=['GET'])
def Currenting_Job():
    if(request.method == 'GET'):
        param = request.args.get('want')
        try:
            mycol = mydb["Employee_Account"]
            if(param == 'all'):
                result = mycol.find({})
                result = list(result)
                ####print(result)
                response = {
                     'data': json.dumps(result, default=str),
                     'response' : 'Pass',
                     'mimetype' : 'application/json'     
                }
            else:
                result = mycol.find({ "_id": param })
                result = list(result)
                ####print(result)
                response = {
                     'data': json.dumps(result, default=str),
                     'response' : 'Pass',
                     'mimetype' : 'application/json'     
                }
        except:
            response = {
                 'response' : 'Cannot',
                 'mimetype' : 'application/json'     
            }
        return response

@app.route('/getJobAnnoucement', methods=['GET'])
def getJobAnnoucement():
    if(request.method == 'GET'):
        param = request.args.get('want')
        try:
            mycol = mydb["Employer_Annoucment"]
            if(param == 'all'):
                result = mycol.find({})
                result = list(result)
                ####print(result)
                response = {
                     'data': json.dumps(result, default=str),
                     'response' : 'Pass',
                     'mimetype' : 'application/json'     
                }
            else:
                result = mycol.find({ "_id": ObjectId(param) })
                result = list(result)
                ####print(result)
                response = {
                     'data': json.dumps(result, default=str),
                     'response' : 'Pass',
                     'mimetype' : 'application/json'     
                }
        except:
            response = {
                 'response' : 'Cannot',
                 'mimetype' : 'application/json'     
            }
        return response

@app.route('/getAllApply', methods=['GET'])
def getAllApply():
    if(request.method == 'GET'):
        param = request.args.get('want')
        try:
            mycol = mydb["Employee_Account"]
            if(param == 'all'):
                result = mycol.find({})
                result = list(result)
                ####print(result)
                response = {
                     'data': json.dumps(result, default=str),
                     'response' : 'Pass',
                     'mimetype' : 'application/json'     
                }
            else:
                result = mycol.find({ "_id": param })
                result = list(result)
                ####print(result)
                response = {
                     'data': json.dumps(result, default=str),
                     'response' : 'Pass',
                     'mimetype' : 'application/json'     
                }
        except:
            response = {
                 'response' : 'Cannot',
                 'mimetype' : 'application/json'     
            }
        return response

@app.route('/getJobAnnoucementByObj', methods=['GET'])
def getJobAnnoucementByObj():
    if(request.method == 'GET'):
        param = request.args.get('want')
        try:
            mycol = mydb["Employer_Annoucment"]
            if(param == 'all'):
                result = mycol.find({})
                result = list(result)
                ####print(result)
                response = {
                     'data': json.dumps(result, default=str),
                     'response' : 'Pass',
                     'mimetype' : 'application/json'     
                }
            else:
                result = mycol.find({ "_id": ObjectId(param) })
                result = list(result)
                ####print(result)
                response = {
                     'data': json.dumps(result, default=str),
                     'response' : 'Pass',
                     'mimetype' : 'application/json'     
                }
        except:
            response = {
                 'response' : 'Cannot',
                 'mimetype' : 'application/json'     
            }
        return response

@app.route('/bookmark_Employee', methods=['GET','POST'])
def bookmark_Employee():
    if(request.method == 'GET'):
        param = request.args.get('want')
        try:
            mycol = mydb["Employee_Account"]
            if(param == 'all'):
                result = mycol.find({})
                result = list(result)
                ####print(result)
                response = {
                     'data': json.dumps(result, default=str),
                     'response' : 'Pass',
                     'mimetype' : 'application/json'     
                }
            else:
                result = mycol.find({ "_id":param})
                result = list(result)
                ###print(result)
                response = {
                     'data': json.dumps(result, default=str),
                     'response' : 'Pass',
                     'mimetype' : 'application/json'     
                }
        except:
            response = {
                 'response' : 'Cannot',
                 'mimetype' : 'application/json'     
            }
        return response
    if(request.method == 'POST'):
        try:
            data = request.json
            ###print(data['Email'])
            ###print(data['Employee_Email'])
            ###print(data)
            mycol = mydb["Employer_Account"]
            if(data['checkBookmark'] == False):
                mycol.update(
                    { '_id' : data['Email'] },
                    { '$push' : {'bookmark' : data['Employee_Email']} }
                )
            else:
                mycol.update(
                    { '_id' : data['Email'] },
                    { '$pull' : {'bookmark' : data['Employee_Email']} }
                )
            response = {
                'response' : 'Pass',
                    'mimetype' : 'application/json'     
            }
        except:
            response = {
                 'response' : 'Cannot',
                 'mimetype' : 'application/json'     
            }
            
        return response

@app.route('/bookmark2', methods=['GET','POST'])
def bookmark2():
    if(request.method == 'GET'):
        param = request.args.get('want')
        try:
            mycol = mydb["Employee_Account"]
            if(param == 'all'):
                result = mycol.find({})
                result = list(result)
                ###print(result)
                response = {
                     'data': json.dumps(result, default=str),
                     'response' : 'Pass',
                     'mimetype' : 'application/json'     
                }
            else:
                result = mycol.find({ "_id":param})
                result = list(result)
                ###print(result)
                response = {
                     'data': json.dumps(result, default=str),
                     'response' : 'Pass',
                     'mimetype' : 'application/json'     
                }
        except:
            response = {
                 'response' : 'Cannot',
                 'mimetype' : 'application/json'     
            }
        return response
    if(request.method == 'POST'):
        try:
            data = request.json
            ###print(data['Email'])
            ###print(data['jobObj'])
            ###print(data)
            mycol = mydb["Employee_Account"]
            if(data['checkBookmark'] == False):
                mycol.update(
                    { '_id' : data['Email'] },
                    { '$push' : {'bookmark' :data['jobObj']} }
                )
            else:
                mycol.update(
                    { '_id' : data['Email'] },
                    { '$pull' : {'bookmark' : data['jobObj']} }
                )
            response = {
                'response' : 'Pass',
                    'mimetype' : 'application/json'     
            }
        except:
            response = {
                 'response' : 'Cannot',
                 'mimetype' : 'application/json'     
            }
            
        return response

@app.route('/Annoucement_by_objId', methods=['GET'])
def Annoucement_by_objId():
    if(request.method == 'GET'):
        param = request.args.get('want')
        try:
            mycol = mydb["Employee_Annoucment"]
            if(param == 'all'):
                result = mycol.find({})
                result = list(result)
                ###print(result)
                response = {
                     'data': json.dumps(result, default=str),
                     'response' : 'Pass',
                     'mimetype' : 'application/json'     
                }
            else:
                result = mycol.find({ "_id": ObjectId(param) })
                result = list(result)
                ###print(result)
                response = {
                     'data': json.dumps(result, default=str),
                     'response' : 'Pass',
                     'mimetype' : 'application/json'     
                }
        except:
            response = {
                 'response' : 'Cannot',
                 'mimetype' : 'application/json'     
            }
        return response

@app.route('/Employee_Annoucement_Edit', methods=['POST'])
def Employee_Annoucement_Edit():
    if(request.method == 'POST'):
        try:
            data = request.json
            ###print(data['objId'])
            ###print(data)
            mycol = mydb["Employee_Annoucment"]
            find = { '_id': ObjectId(data['objId']) }
            newvalues = { "$set": { 'job': data['job'] } } 
            mycol.update_one(find, newvalues)
            newvalues = { "$set": { 'location': data['location'] } } 
            mycol.update_one(find, newvalues)
            newvalues = { "$set": { 'experience': data['experience'] } } 
            mycol.update_one(find, newvalues)
            newvalues = { "$set": { 'type': data['jobType'] } }             
            mycol.update_one(find, newvalues)
            newvalues = { "$set": { 'Compensation': data['Compensation'] } }             
            mycol.update_one(find, newvalues)
            newvalues = { "$set": { 'aboutMe': data['aboutMe'] } }             
            mycol.update_one(find, newvalues)

            response = {
                 'response' : 'Pass',
                 'mimetype' : 'application/json'     
            }
        except:
            response = {
                 'response' : 'Cannot',
                 'mimetype' : 'application/json'     
            }
            
        return response

@app.route('/addPending', methods=['POST'])
def addPending():
    if(request.method == 'POST'):
        try:
            data = request.json
            mycol = mydb["Employer_Annoucment"]
            mycol.update(
                { '_id' : ObjectId(data['objId']) },
                { '$push' : {'applyList' : data['email']} }
            )
            mycol = mydb["Employee_Account"]
            mycol.update(
                { '_id' : data['email'] },
                { '$push' : {'allApply' : data['objId']} }
            )

            mycol = mydb["PushToken"]
            token_id = data['employerEmail']+'_'+data['mode'] 
            print(token_id)
            token = mycol.find({'_id':token_id})
            token = list(token)[0]['token']
            send_Notifi(token,'You Have a new notification','มีผู้สมัครงานเข้ามาใหม่')

            response = {
                'response' : 'Pass',
                    'mimetype' : 'application/json'     
            }
        except:
            response = {
                 'response' : 'Cannot',
                 'mimetype' : 'application/json'     
            }
            
        return response

@app.route('/addHiring', methods=['POST'])
def addHiring():
    if(request.method == 'POST'):
        try:
            data = request.json
            mycol = mydb["Employer_Account"]
            mycol.update(
                { '_id' : data['employer'] },

                { '$push' : {'hiringList' : data['email']} }
            )
            mycol = mydb["Employer_Annoucment"]
            mycol.update(
                { '_id' : ObjectId(data['objId']) },

                { '$pull' : {'applyList' : data['email']} }
            )
            mycol = mydb["Employee_Account"]
            mycol.update(
                { '_id' : data['email'] },

                { '$pull' : {'allApply' : data['objId']} }
            )
            response = {
                'response' : 'Pass',
                    'mimetype' : 'application/json'     
            }
        except:
            response = {
                 'response' : 'Cannot',
                 'mimetype' : 'application/json'     
            }
            
        return response

@app.route('/finishWork', methods=['POST'])
def finishWork():
    if(request.method == 'POST'):
        try:
            data = request.json
            ###print(data)
            mycol = mydb["Employer_Account"]
            mycol.update(
                { '_id' : data['employer'] },
                { '$pull' : {'hiringList' : data['email']} }
            )
            mycol.update(
                { '_id' : data['employer'] },
                { '$pull' : {'EmployeeOfJob' : data['EmployeeOfJob']} }
            )
            #set new rating
            ###print('set new rate')
            mycol = mydb["Employee_Account"]
            find = { '_id': data['email'] }
            newvalues = { "$set": { 'rating': data['rating'] } }       
            mycol.update_one(find, newvalues)
            newvalues = { "$set": { 'countJob': data['countJob'] } }       
            mycol.update_one(find, newvalues)
            mycol.update(
                { '_id' : data['email'] },
                { '$push' : {'allRate' : data['allRate']} }
            )
            mycol.update(
                { '_id' : data['email'] },
                { '$pull' : {'Currenting' : data['jobID']} }
            )
            #set jobDone in Areement
            ###print('set jobdone')
            mycol = mydb["Agreement"]
            find = { '_id': ObjectId(data['agreementId']) }
            newvalues = { "$set": { 'jobDone': data['jobDone'] } }       
            mycol.update_one(find, newvalues)

            myquery = { "_id": ObjectId(data['agreementId']) }
            mycol.delete_one(myquery)

            response = {
                'response' : 'Pass',
                    'mimetype' : 'application/json'     
            }
        except:
            response = {
                 'response' : 'Cannot',
                 'mimetype' : 'application/json'     
            }
            
        return response

@app.route('/postAgreement', methods=['POST'])
def postAgreement():
    if(request.method == 'POST'):
        try:
            data = request.json
            mycol = mydb["Agreement"]
            mycol.insert_one(data)
            mycol = mydb["PushToken"]
            if(data['mode'] == 'Employee'):
                token_id = data['EmployeeID']+'_'+data['mode'] 
                print(token_id)
                token = mycol.find({'_id':token_id})
                token = list(token)[0]['token']
                send_Notifi(token,'You Have a new notification','นายจ้างทำสัญญาเรียบร้อยแล้ว')

            response = {
                 'response' : 'Pass',
                 'mimetype' : 'application/json'     
            }
        except:
            response = {
                 'response' : 'Cannot',
                 'mimetype' : 'application/json'     
            }
            
        return response

@app.route('/checkAgreement', methods=['POST'])
def checkAgreement():
    if(request.method == 'POST'):
        data = request.json
        ###print(data['jobID'])
        ###print(data['EmployeeID'])
        ###print(data['EmployerID'])
        try:
            mycol = mydb["Agreement"]
            result = mycol.find({ "jobID":data['jobID'], "EmployeeID":data['EmployeeID'], "EmployerID":data['EmployerID']})
            result = list(result)
            ###print(result)
            response = {
                'data': json.dumps(result, default=str),
                'response' : 'Pass',
                'mimetype' : 'application/json'     
            }
        except:
            response = {
                 'response' : 'Cannot',
                 'mimetype' : 'application/json'     
            }
        return response

@app.route('/employeeUpdateAgreement', methods=['POST'])
def employeeUpdateAgreement():
    if(request.method == 'POST'):
        data = request.json
        ###print(data)
        try:
            mycol = mydb["Agreement"]
            find = { '_id': ObjectId(data['agreementID']) }
            newvalues = { "$set": { 'EmployeeStatus': data['EmployeeStatus'] } }       
            mycol.update_one(find, newvalues)

            mycol = mydb["Employee_Account"]
            mycol.update(
                { '_id' : data['employeeEmail'] },
                { '$pull' : {'allApply' : data['objId']} }
            )
            mycol.update(
                { '_id' : data['employeeEmail'] },
                { '$push' : {'Currenting' : data['objId']} }
            )

            mycol = mydb["Employer_Account"]
            mycol.update(
                { '_id' : data['employerEmail'] },
                { '$push' : {'hiringList' : data['employeeEmail']} }
            )
            mycol.update(
                { '_id' : data['employerEmail'] },
                { '$push' : {'EmployeeOfJob' : data['EmployeeOfJob']} }
            )


            mycol = mydb["Employer_Annoucment"]
            mycol.update(
                { '_id' : ObjectId(data['objId']) },
                { '$pull' : {'applyList' : data['employeeEmail']} }
            )

            mycol = mydb["PushToken"]
            token_id = data['employerEmail']+'_'+data['mode'] 
            print(token_id)
            token = mycol.find({'_id':token_id})
            token = list(token)[0]['token']
            send_Notifi(token,'You Have a new notification','ลูกจ้างทำสัญญาเรียบร้อยแล้ว')

            response = {
                'response' : 'Pass',
                'mimetype' : 'application/json'     
            }
            
        except:
            response = {
                 'response' : 'Cannot',
                 'mimetype' : 'application/json'     
            }
        return response

@app.route('/getAgreement', methods=['POST'])
def getAgreement():
    if(request.method == 'POST'):
        data = request.json
        try:
            mycol = mydb["Agreement"]
            result = mycol.find({ 'EmployeeID': data['email'], 'jobID': data['jobID'], 'EmployerID':data['employer'] })
            result = list(result)
            ###print(result)
            response = {
                'data': json.dumps(result, default=str),
                'response' : 'Pass',
                'mimetype' : 'application/json'     
            }
        except:
            response = {
                 'response' : 'Cannot',
                 'mimetype' : 'application/json'     
            }
        return response

@app.route('/chat', methods=['GET','POST','DELETE'])
def chat():
    if(request.method == 'GET'):
        try:
            param = request.args.get('want')
            ###print(param)
            if(request.args.get('u1') < request.args.get('u2')):
                doc_id = request.args.get('u2')+":"+request.args.get('u1')
            else:
                doc_id = request.args.get('u1')+":"+request.args.get('u2')
            myquery = { "_id": doc_id }
            mycol = mydb["chat"]
            mydoc = mycol.find(myquery,{'data':1,'_id':0})
            mydoc = list(mydoc)
            mydoc = mydoc[0]['data']
            mydoc.sort(reverse=True,key=lambda x:x['date'])
            ###print(mydoc)
            response = {
                 'data': json.dumps(mydoc, default=str),
                 'response' : 'Pass',
                 'mimetype' : 'application/json'     
            }
        except:
            response = {
                 'response' : 'Cannot',
                 'mimetype' : 'application/json'     
            }
        return response
    
    elif(request.method == 'POST'):
        print(request.json)
        try:
            data = request.json
            if(data['mode'] == 'Employee'):
                mode = 'Employer'
            else:
                mode = 'Employee'
            if(data['u1'] == data['own']):
                m = data['u2']
            else:
                m = data['u1']
            token_id = m+'_'+mode 
            print(token_id)
            mycol = mydb["PushToken"]
            token = mycol.find({'_id':token_id})
            token = list(token)[0]['token']
            print(token)
            now = datetime.now()
            mycol = mydb["chat"]
            if(data["u1"] < data["u2"]):
                doc_id = data["u2"]+":"+data["u1"]
            else:
                doc_id = data["u1"]+":"+data["u2"]
            re = mycol.find({'_id':doc_id})
            if(len(list(re)) == 0):
                mycol.insert_one({'_id':doc_id,
                                  'data':[]
                                }) 
            datapackage = {
                'text': data["text"],
                'own': data["own"],
                'date': datetime.fromtimestamp(int(datetime.timestamp(now))),
                'type': data["type"]
            }
            mycol.update(
               { '_id': doc_id },
               { '$push': {'data': datapackage} }
            )
            send_Notifi(token,'You Have a new message','ํคุณได้รับข้อความใหม่')
            response = {
                 'response' : 'Pass',
                 'mimetype' : 'application/json'     
            }
        except:
            response = {
                 'response' : 'Cannot',
                 'mimetype' : 'application/json'     
            }
        return response

@app.route('/getJobIdFromAgreement', methods=['POST'])
def getJobIdFromAgreement():
    if(request.method == 'POST'):
        data = request.json
        ###print(data)
        try:
            mycol = mydb["Agreement"]
            result = mycol.find({ 'EmployeeID': data['EmployeeID'], 'EmployerID':data['EmployerID'], 
                                  'EmployeeStatus':data['EmployeeStatus'], 'EmployerStatus':data['EmployerStatus'], 
                                  'jobDone':data['jobDone'] })
            result = list(result)
            ###print(result)
            response = {
                'data': json.dumps(result, default=str),
                'response' : 'Pass',
                'mimetype' : 'application/json'     
            }
        except:
            response = {
                 'response' : 'Cannot',
                 'mimetype' : 'application/json'     
            }
        return response

@app.route('/getChatList', methods=['POST'])
def getChatList():
    if(request.method == 'POST'):
        data = request.json
        print(data['email'])
        try:
            mycol = mydb["chat"]
            result = mycol.find({"_id": {'$regex': '.*'+data['email']+'*'}},{'_id':1})
            result = list(result)
            print(result)
            result = [i['_id'].split(':') for i in result]
            print(result)
            for i in result:
                i.remove(data['email'])
            print(result)
            result = [i[0] for i in result]
            print(result)
            if(data['mode'] == 'Employee'):
                mycol = mydb["Employer_Account"]
            else:
                mycol = mydb["Employee_Account"]
            data = []
            result = np.unique(result)
            for i in result:
                r = mycol.find({"_id": i})
                r = list(r)
                if(r != []):
                    data.append((r[0]))
            response = {
                'data': json.dumps(data, default=str),
                'response' : 'Pass',
                'mimetype' : 'application/json'     
            }
        except:
            response = {
                 'response' : 'Cannot',
                 'mimetype' : 'application/json'     
            }
        return response


@app.route('/postAboutMe', methods=['POST'])
def postAboutMe():
    if(request.method == 'POST'):
        try:
            data = request.json
            mycol = mydb["AboutMe"]
            mycol.insert_one(data)
            response = {
                 'response' : 'Pass',
                 'mimetype' : 'application/json'     
            }
        except:
            response = {
                 'response' : 'Cannot',
                 'mimetype' : 'application/json'     
            }
            
        return response

@app.route('/getAboutMe', methods=['POST'])
def getAboutMe():
    if(request.method == 'POST'):
        data = request.json
        ###print(data)
        try:
            mycol = mydb["AboutMe"]
            result = mycol.find({ 'objId': data['objId'], 'email':data['email'] })
            result = list(result)
            ###print(result)
            response = {
                'data': json.dumps(result, default=str),
                'response' : 'Pass',
                'mimetype' : 'application/json'     
            }
        except:
            response = {
                 'response' : 'Cannot',
                 'mimetype' : 'application/json'     
            }
        return response

@app.route('/Employee_Interesting', methods=['POST'])
def Employee_Interesting():
    if(request.method == 'POST'):
        ###print(request.json)
        try:
            data = request.json
            mycol = mydb["Employee_Account"]
            find = { '_id': data['email'] }
            newvalues = { "$set": { 'interest': data['interest'] } } 
            mycol.update_one(find, newvalues)
            response = {
                 'response' : 'Pass',
                 'mimetype' : 'application/json'     
            }
        except:
            response = {
                 'response' : 'Cannot',
                 'mimetype' : 'application/json'     
            }
        return response

@app.route('/Employee_Image', methods=['POST'])
def Employee_Image():
    if(request.method == 'POST'):
        ###print(request.json)
        try:
            data = request.json
            mycol = mydb["Employee_Account"]
            find = { '_id': data['email'] }
            newvalues = { "$set": { 'image': data['image'] } } 
            mycol.update_one(find, newvalues)
            response = {
                 'response' : 'Pass',
                 'mimetype' : 'application/json'     
            }
        except:
            response = {
                 'response' : 'Cannot',
                 'mimetype' : 'application/json'     
            }
        return response

@app.route('/Employer_Image', methods=['POST'])
def Employer_Image():
    if(request.method == 'POST'):
        ###print(request.json)
        try:
            data = request.json
            mycol = mydb["Employer_Account"]
            find = { '_id': data['email'] }
            newvalues = { "$set": { 'image': data['image'] } } 
            mycol.update_one(find, newvalues)
            response = {
                 'response' : 'Pass',
                 'mimetype' : 'application/json'     
            }
        except:
            response = {
                 'response' : 'Cannot',
                 'mimetype' : 'application/json'     
            }
        return response

@app.route('/insertChat', methods=['POST'])
def insertChat():
    if(request.method == 'POST'):
        try:
            data = request.json
            mycol = mydb["chat"]
            mycol.insert_one(data)
            response = {
                 'response' : 'Pass',
                 'mimetype' : 'application/json'     
            }
        except:
            response = {
                 'response' : 'Cannot',
                 'mimetype' : 'application/json'     
            }
            
        return response

@app.route('/Emplyee_Rec', methods=['POST','GET'])
def Emplyee_Rec(): 
    if(request.method == 'GET'):
        param = request.args.get('want')
        print(param)
        mycol = mydb["TestRec"]
        myquery = {"_id": 'Employer_An'}
        mydoc = mycol.find(myquery)
        mydoc = list(mydoc)
        mydoc = mydoc[0]['data']
        mydoc1 = [i['label'] for i in mydoc if (i['num']>0)]
        print(mydoc1)
        mycol = mydb["Employee_Account"]
        mydoc = mycol.find({'_id':param})
        mydoc = list(mydoc)
        mydoc = mydoc[0]['data']
        mydoc = [i for i in mydoc if i['label'] in mydoc1]
        Mymc = [machine(i['label'],i['a'],i['b']) for i in mydoc]
        index = np.argmax([np.random.beta(m.a, m.b) for m in Mymc])
        label = Mymc[index].label
        print(index,label)
        mycol = mydb["Employer_Annoucment"]
        myquery = {"jobType": label}
        mydoc = mycol.find(myquery,{'_id':1})
        mydoc = list(mydoc)
        if(len(mydoc) >= 10):
            mydoc = random.sample(mydoc[0],10)
        print(mydoc)
        results = []
        for i in mydoc:
            result = mycol.find({ "_id":i['_id']})
            result = list(result)
            results.append(result[0])
        print(results)
        mycol = mydb["Employee_Account"]
        mycol.update_one({'_id' : param , 'data.label':label} , {"$inc": {'data.$.b': 1}})
        response = {
                'data': json.dumps(results, default=str),
                'response' : 'Pass',
                'mimetype' : 'application/json'     
        }
        return response
    if(request.method == 'POST'):
        data = request.json
        id_u = data['id_u']
        id_j = data['id_j']
        print(data)
        mycol = mydb["Employer_Annoucment"]
        myquery = {"_id": ObjectId(id_j)}
        mydoc = mycol.find(myquery,{'jobType':1})
        mydoc = list(mydoc)
        label = mydoc[0]['jobType']
        print(label)
        mycol = mydb["Employee_Account"]
        mycol.update_one({'_id' : id_u , 'data.label':label} , {"$inc": {'data.$.b': -1}})
        mycol.update_one({'_id' : id_u , 'data.label':label} , {"$inc": {'data.$.a': 1}})
        response = {
                'response' : 'Pass',
                'mimetype' : 'application/json'     
        }
        return response

@app.route('/Emplyer_Rec', methods=['POST','GET'])
def Emplyer_Rec():
    if(request.method == 'GET'):
        param = request.args.get('want')
        print(param)
        mycol = mydb["TestRec"]
        myquery = {"_id": 'Employee_An'}
        mydoc = mycol.find(myquery)
        mydoc = list(mydoc)
        mydoc = mydoc[0]['data']
        mydoc1 = [i['label'] for i in mydoc if (i['num']>0)]
        print(mydoc1)
        mycol = mydb["Employer_Account"]
        mydoc = mycol.find({'_id':param})
        mydoc = list(mydoc)
        mydoc = mydoc[0]['data']
        mydoc = [i for i in mydoc if i['label'] in mydoc1]
        Mymc = [machine(i['label'],i['a'],i['b']) for i in mydoc]
        index = np.argmax([np.random.beta(m.a, m.b) for m in Mymc])
        label = Mymc[index].label
        print(index,label)
        mycol = mydb["Employee_Annoucment"]
        myquery = {"jobType": label}
        mydoc = mycol.find(myquery,{'_id':1})
        mydoc = list(mydoc)
        if(len(mydoc) >= 10):
            mydoc = random.sample(mydoc[0],10)
        print(mydoc)
        results = []
        for i in mydoc:
            result = mycol.find({ "_id":i['_id']})
            result = list(result)
            results.append(result[0])
        print(results)
        mycol = mydb["Employer_Account"]
        mycol.update_one({'_id' : param , 'data.label':label} , {"$inc": {'data.$.b': 1}})
        response = {
                'data': json.dumps(results, default=str),
                'response' : 'Pass',
                'mimetype' : 'application/json'     
        }
        return response
    if(request.method == 'POST'):
        data = request.json
        id_u = data['id_u']
        id_j = data['id_j']
        print(data)
        mycol = mydb["Employee_Annoucment"]
        myquery = {"_id": ObjectId(id_j)}
        mydoc = mycol.find(myquery,{'jobType':1})
        mydoc = list(mydoc)
        label = mydoc[0]['jobType']
        print(label)
        mycol = mydb["Employer_Account"]
        mycol.update_one({'_id' : id_u , 'data.label':label} , {"$inc": {'data.$.b': -1}})
        mycol.update_one({'_id' : id_u , 'data.label':label} , {"$inc": {'data.$.a': 1}})
        response = {
                'response' : 'Pass',
                'mimetype' : 'application/json'     
        }
        return response

@app.route('/set_Token', methods=['POST'])
def set_Token():
    if(request.method == 'POST'):
        print(request.json)
        try:
            data = request.json
            mycol = mydb["PushToken"]
            fi = mycol.find({'_id':data['email']+'_'+data['mode']})
            fi = list(fi)
            print(fi)
            if(len(fi) == 0):
                data = {
                    '_id':data['email']+'_'+data['mode'],
                    'token':data['token']
                }
                mycol.insert_one(data)
            else:
                data = request.json
                find = { '_id': data['email']+'_'+data['mode'] }
                newvalues = { "$set": { 'token': data['token'] } } 
                mycol.update_one(find, newvalues)
            response = {
                 'response' : 'Pass',
                 'mimetype' : 'application/json'     
            }
        except:
            response = {
                 'response' : 'Cannot',
                 'mimetype' : 'application/json'     
            }
        return response

if __name__ == '__main__':
    app.run(debug=True)
    