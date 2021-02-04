from flask import Flask,request,json
import pandas as pd 
from gensim.models import Word2Vec
from pythainlp.tokenize import word_tokenize
import pythainlp.corpus as st
import numpy as np
import pymongo
from bson.objectid import ObjectId
from datetime import datetime

client = pymongo.MongoClient("mongodb+srv://tum123456:ttt123456@cluster0.cfjjb.mongodb.net/<dbname>?retryWrites=true&w=majority")
db = client.test
mydb = db["MyProject"]


words = st.thai_stopwords()
data = pd.read_excel("Book1.xlsx",index_col=0) 
word_not_important = ['หา','รับ','งาน','ทำหน้าที่','หน้าที่','ซ่อม','(',')','/']
app = Flask(__name__)

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

data['Title'] = data['Title'].apply(lower)
all_work = [clear_space(i) for i in data['Title'].tolist()]


@app.route('/')
def home():
    print("Hello World")
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

@app.route('/search_job', methods=['GET','POST'])
def search_job():
    if(request.method == 'GET'):
        param = request.args.get('search')
        print(param)
        search_word = param
        search = clear_space(search_word)
        mycol = mydb["Employer_Annoucment"]
        result = mycol.find({})
        result = list(result)
        select_sentence = concerned_sentence(search,result)
        #print(select_sentence)
        #print(search)
        if(len(select_sentence) > 0):
            x = [clear_space(ss) for ss in select_sentence]
            print(x)
            model = Word2Vec(x, min_count=1,size = 500)
            print(model)
            print(model.wv.vocab)
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
                        
                    print("===== RESULT =====")
                    print(a)
                    print("===== RESULT =====")
                    lst = []
                    id_s = []
                    for i in a:
                        for j in result:
                            if(i in j['position']):
                                if(j['_id'] not in id_s):
                                    lst.append(j)
                                    id_s.append(j['_id'])
                    print(lst)
                    print("result = "+str(len(lst)))
                    print("all = "+str(len(result)))
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
        print(param)
        search_word = param
        search = clear_space(search_word)
        mycol = mydb["Employee_Annoucment"]
        result = mycol.find({})
        result = list(result)
        select_sentence = concerned_sentence1(search,result)
        #print(select_sentence)
        #print(search)
        if(len(select_sentence) > 0):
            x = [clear_space(ss) for ss in select_sentence]
            print(x)
            model = Word2Vec(x, min_count=1,size = 500)
            print(model)
            print(model.wv.vocab)
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
                        
                    print("===== RESULT =====")
                    print(a)
                    print("===== RESULT =====")
                    lst = []
                    id_s = []
                    for i in a:
                        for j in result:
                            if(i in j['job']):
                                if(j['_id'] not in id_s):
                                    lst.append(j)
                                    id_s.append(j['_id'])
                    print(lst)
                    print("result = "+str(len(lst)))
                    print("all = "+str(len(result)))
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
        print(request.json)
        try:
            data = request.json
            mycol = mydb["Employee_Account"]
            result = mycol.find({ "Email":data["Email"]})
            result = list(result)
            result1 = mycol.find({"ID":data["ID"]})
            result1 = list(result1)
            if(len(result) == 0 and len(result1) == 0):
                mycol.insert_one(request.json)
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
                mycol.insert_one(request.json)
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
        print(request.json)
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
            mycol.update_one(find, newvalues)
            newvalues = { "$set": { 'degree': data['degree'] } } 
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

@app.route('/Employee_Annoucment', methods=['GET','POST','DELETE'])
def Employee_Annoucment():
    if(request.method == 'POST'):
        print(request.json)
        try:
            data = request.json
            mycol = mydb["Employee_Annoucment"]
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
    elif(request.method == 'GET'):
        param = request.args.get('want')
        print(param)
        try:
            mycol = mydb["Employee_Annoucment"]
            if(param == 'all'):
                result = mycol.find({})
                result = list(result)
                print(result)
                response = {
                     'data': json.dumps(result, default=str),
                     'response' : 'Pass',
                     'mimetype' : 'application/json'     
                }
            else:
                result = mycol.find({ "owner":param})
                result = list(result)
                print(result)
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
        print(param)
        try:
            mycol = mydb["Employee_Annoucment"]
            myquery = { "_id": ObjectId(param) }
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
        print(param)
        try:
            mycol = mydb["Employer_Annoucment"]
            if(param == 'all'):
                result = mycol.find({})
                result = list(result)
                print(result)
                response = {
                     'data': json.dumps(result, default=str),
                     'response' : 'Pass',
                     'mimetype' : 'application/json'     
                }
            else:
                result = mycol.find({ "owner":param})
                result = list(result)
                print(result)
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
        print(request.json)
        try:
            data = request.json
            print(data)
            mycol = mydb["Employer_Annoucment"]
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
    elif(request.method == 'DELETE'):
        param = request.args.get('want')
        print(param)
        try:
            mycol = mydb["Employer_Annoucment"]
            myquery = { "_id": ObjectId(param) }
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

@app.route('/chat', methods=['GET','POST','DELETE'])
def chat():
    if(request.method == 'GET'):
        try:
            param = request.args.get('want')
            print(param)
            myquery = { "id": param }
            mycol = mydb["chat"]
            mydoc = mycol.find(myquery)
            mydoc = list(mydoc)
            print(mydoc)
            mydoc.sort(reverse=True,key=lambda x:x['date'])
            print(mydoc)
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
            now = datetime.now()
            if(data["u1"] < data["u2"]):
                doc_id = data["u2"]+":"+data["u1"]
            else:
                doc_id = data["u1"]+":"+data["u2"]
            print(doc_id)
            print(datetime.fromtimestamp(int(datetime.timestamp(now))))
            datapackage = {
                'id':doc_id,
                'text': data["text"],
                'own': data["own"],
                'date': datetime.fromtimestamp(int(datetime.timestamp(now))),
                'type': data["type"]
            }
            print(datapackage)
            #print(datetime.fromtimestamp(datapackage['date']))
            mycol = mydb["chat"]
            mycol.insert_one(datapackage)
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
    