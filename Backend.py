from flask import Flask,request,json,Response

app = Flask(__name__)
x="Hello World"

@app.route('/')
def home():
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
        print("Success!!")
        param = request.json
        print(param)
        return Response(response='success', status=200, mimetype="application/json") #return json string
        
@app.route('/api/param', methods=['GET','POST'])
def param():
    if(request.method == 'GET'):
        param1 = request.args.get('name')
        param2 = request.args.get('pass')
        print(param1+' '+param2)
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
 

if __name__ == '__main__':
    app.run(debug=True)
    