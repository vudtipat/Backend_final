from flask import Flask,request,json,Response
import psycopg2
from psycopg2.extras import RealDictCursor

       
def insert(table,data):
    try:
        connection = psycopg2.connect(user = "ppociznxzknvfz",
                                      password = "e7e5d5872f97e341660c93d04ea2682a3d9f892c450b1ec8c5679903e6387162",
                                      host = "ec2-34-234-185-150.compute-1.amazonaws.com",
                                      port = "5432",
                                      database = "d8965kg37dlmdu")
        cursor = connection.cursor()
        cursor.execute('''INSERT INTO '''+table+''' (username, password) VALUES ('''+"'"+data['user']+"'"+','+"'"+data['pass']+"'"+')')
        connection.commit()
        connection.close()
        print("PostgreSQL connection is closed")
        return "SUCCESS"
    except (Exception, psycopg2.Error) as error :
        print ("Error while connecting to PostgreSQL", error)
        
def select_all(table,data):
    try:
        connection = psycopg2.connect(user = "ppociznxzknvfz",
                                      password = "e7e5d5872f97e341660c93d04ea2682a3d9f892c450b1ec8c5679903e6387162",
                                      host = "ec2-34-234-185-150.compute-1.amazonaws.com",
                                      port = "5432",
                                      database = "d8965kg37dlmdu")
        cursor = connection.cursor(cursor_factory= RealDictCursor)
        cursor.execute('select * from '+table+' where username = '+"'"+data['user']+"'")
        result = json.dumps(cursor.fetchone())
        connection.close()
        print("PostgreSQL connection is closed")
        return result
    except (Exception, psycopg2.Error) as error :
        print ("Error while connecting to PostgreSQL", error)

def update(table,data):
    
    try:
        connection = psycopg2.connect(user = "ppociznxzknvfz",
                                      password = "e7e5d5872f97e341660c93d04ea2682a3d9f892c450b1ec8c5679903e6387162",
                                      host = "ec2-34-234-185-150.compute-1.amazonaws.com",
                                      port = "5432",
                                      database = "d8965kg37dlmdu")
        cursor = connection.cursor()
        cursor.execute('update '+table+' set email = '+"'"+data['user']+"'"+','+' password = '+ "'"+data['pass']+"'"+ ' where username = '+"'"+data['user']+"'")
        connection.commit()
        connection.close()
        print("PostgreSQL connection is closed")
        return "SUCCESS"
    except (Exception, psycopg2.Error) as error :
        print ("Error while connecting to PostgreSQL", error)
        
app = Flask(__name__)

@app.route('/')
def home():
    print("Hello World")
    return "This is home page "


@app.route('/api/tests', methods=['GET','POST'])
def tests():
    if(request.method == 'GET'):
        list_x = [{
          "name": "JohnSon",
          "age": 30,
          "city": "New York"
        },{
          "name": "JOOO",
          "age": 30,
          "city": "New York"
        },{
          "name": "BOBY",
          "age": 30,
          "city": "New York"
        },{
          "name": "TERWA",
          "age": 30,
          "city": "New York"
        }]
        response = app.response_class(
        response=json.dumps(list_x),
        mimetype='application/json'
        )
        return response
    
    if(request.method == 'POST'):
        print("Success11111!!")
        param = request.json
        print(param)
        response1 = insert('accounts',param)
        return Response(response=response1, status=200, mimetype="application/json") #return json string
        
@app.route('/api/param', methods=['GET','POST'])
def param():
    if(request.method == 'GET'):
        param1 = request.args.get('name')
        param2 = request.args.get('pass')
        data = {'user':param1,'pass':param2}
        print(param1+' '+param2)
        response = app.response_class(
                response=select_all('accounts',data),
                mimetype='application/json'
        )
        return response
    
    if(request.method == 'POST'):
        param1 = request.args.get('name')
        param2 = request.args.get('pass')
        data = {'user':param1,'pass':param2}
        print(param1+' '+param2)
        response = app.response_class(
                response=update('accounts',data),
                mimetype='application/json'
        )
        return response
 

if __name__ == '__main__':
    app.run(debug=True)
    