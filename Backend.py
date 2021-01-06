from flask import Flask,request,json
import pandas as pd 
from gensim.models import Word2Vec
from pythainlp.tokenize import word_tokenize
import pythainlp.corpus as st
import numpy as np
import pymongo
from bson.objectid import ObjectId

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
            if(i.lower() in j):
                arr.append(j)
    return arr

def clear_space(s):
    s = s.lower()
    global words,word_not_important
    ss = ''
    for i in s:
        if(i != '/'):
            if(i != ' '):
                ss+=i
    b = word_tokenize(ss)
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
        select_sentence = concerned_sentence(search,all_work)
        if(len(select_sentence) > 0):
            model = Word2Vec(select_sentence, min_count=1,size = 500)
            a = []
            try:
                for t in search:
                    aa=model.most_similar(t)
                    list_of_word = [i[0] for i in aa]
                    a += list_of_word
                    
                    a = np.array(a) 
                    a = np.unique(a)
                    
                    print("===== RESULT =====")
                    print(a)
                    print("===== RESULT =====")
                    
                    result = []
                    for i in a:
                        for j in range(len(all_work)):
                            if(i in all_work[j]):
                                result.append(j)
                                
                    result = np.array(result)
                    result = np.unique(result)
                    print("===== SEARCH RESULT =====")
                    print(result)
                    lst = []
                    for z in result:
                        da = [
                                data.iloc[z]['Title'],
                                data.iloc[z]['Company'],
                                data.iloc[z]['Location'],
                                data.iloc[z]['Property']
                        ]
                        lst.append(da)
                        #print(data.iloc[z])
                    #lst = json.dumps(lst ,ensure_ascii=False)
                    print(lst)
                    response = {
                         'response' : lst,
                         'mimetype' : 'application/json'
                    }
                    print("===== SEARCH RESULT =====")
            except:
                b = select_sentence
                
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
    
@app.route('/Employer_Annoucment', methods=['GET','POST'])
def Employer_Annoucment():
    if(request.method == 'GET'):
        param = request.args.get('want')
        print(param)
        try:
            mycol = mydb["Employer_Annoucment"]
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
    
    if(request.method == 'POST'):
        print(request.json)
        try:
            data = request.json
            print(data)
            """
            mycol = mydb["Employer_Annoucment"]
            mycol.insert_one(data)"""
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

@app.route('/getAllEmployee',methods=['GET','POST'])
def getAllEmployee():
    if(request.method == 'GET'):
        try:
            mycol = mydb["Employee_Account"]
            result = mycol.find({},{ "Password": 0, "Question": 0, "Answer": 0 })
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
if __name__ == '__main__':
    app.run(debug=True)
    