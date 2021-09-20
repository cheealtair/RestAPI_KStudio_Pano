'''
Requirements:
conda install flask
conda install flask-restplus

'''


from flask import Flask, request
from flask_restplus import Api, Resource, fields
import json
import SWA_DeployedModel as swam
import pandas as pd

# defining app using flask_restplus.API
flask_app = Flask(__name__)
app = Api(app=flask_app,
          version="1.0",
          title="my main",
          description="my first app")
# namespace root 'main' will appear in Swagger doc
# access via: http://127.0.0.1/main
name_space = app.namespace('main', description='Main APIs')


# define apps under the namespace

# Usage: http://127.0.0.1:5000/main/   The trailing "/" is needed
@name_space.route("/")
class MainClass(Resource):
    def get(self):
        return {
            "status": "Got new data"
        }

    def post(self):
        return {
            "status": "Posted new1 data" 
        }

# Usage: http://127.0.0.1:5000/main/array_2col    No trailing "/" is required
@name_space.route("/array_2col")
class Array2colClass(Resource):

    def post(self):
        data = request.json['data']
        out_data = "{'typename': " + str(type(data)) + "}"
        #out_data =  { "status": "Posted new4 data" }
        print(type(out_data))
        print(type(data))
        print(data)
        # for using {table-data}
        
        table = []
        for arow in data:
            data1 = arow[0]
            data2 = arow[1]
            table.append({'age': str(data1), 'rel': data2})
        print(table)
        
        # end for using {table-data}
        '''
        # for using {table}        
        table = []
        for arow in data:
            data1 = arow["ProductIds"] * 3.14159
            data2 = arow["rel"] + arow["rel"] + arow["rel"]  
            table.append({'age': str(data1), 'rel': data2})
        print(table)
        
        # end for using {table}
        '''
        data = table
        print(json.dumps(data))
        return data


# Usage: http://127.0.0.1:5000/main/swa_model    No trailing "/" is required
@name_space.route("/swa_model")
class swaModelClass(Resource):

    def post(self):
        data = request.json['data']

        # Scoring using SWA deployed model
        in_header = ["age","relationship"]        
        mytoken = swam.getToken()
        myresults = swam.getModelResults(mytoken, in_header, data)
        dict_predicted = myresults.json()
        list_predicted = dict_predicted['data']['ndarray'] 
        #print(list_predicted)

        # for using {table-data}
        table = []
        for arow, brow in zip(data, list_predicted):
            data1 = arow[0]
            data2 = arow[1]
            table.append({'age': str(data1), 'rel': data2, 'predicted':brow[0]})
        #print(table)
        # end for using {table-data}
        
        data = table
        #print(json.dumps(data))
        return data

# Usage: http://127.0.0.1:5000/main/streams_simple    No trailing "/" is required
@name_space.route("/streams_simple")
class swaModelStreamsClass(Resource):

    def post(self):
        #data = request.json['data']
        df = pd.DataFrame([{'c1': 10, 'c2': 100}, {'c1': 11, 'c2': 110}, {'c1': 12, 'c2': 120}])
        table = [{'c1': 10, 'c2': 100}, {'c1': 11, 'c2': 110}, {'c1': 12, 'c2': 120}]
        #return json.dumps(table)
        return table

# Usage: http://127.0.0.1:5000/main/swa_model_streams    No trailing "/" is required
@name_space.route("/swa_model_streams")
class swaModelStreamsClass(Resource):

    def post(self):
        
        
        data = request.json['data']
        # Scoring using SWA deployed model
        in_header = ["age", "relationship"]
        mytoken = swam.getToken()
        myresults = swam.getModelResults(mytoken, in_header, data)
        dict_predicted = myresults.json()
        list_predicted = dict_predicted['data']['ndarray']
        # print(list_predicted)

        # for using {table-data}
        table = []
        for arow, brow in zip(data, list_predicted):
            data1 = arow[0]
            data2 = arow[1]
            table.append({'age': str(data1), 'rel': data2, 'predicted': brow[0]})
        #print(table)
        # end for using {table-data}

        data = table
        # print(json.dumps(data))
        return data
        
        '''
        print(type(request.json))
        data = request.json['data']
        print(type(data))
        for aa in data:
            print(aa)
        
        table = [{'c1': 10, 'c2': 100}, {'c1': 11, 'c2': 110}, {'c1': 12, 'c2': 120}]
        # return json.dumps(table)
        return data
        '''


if __name__ == '__main__':
    app.app.run(debug=True)

"""
To use in Pano.
1. Run this server
2. On Pano select this:
Datasources: Text
3. Under Transform Settings
Auth TYpe: Basic
URL: http://localhost:5000/main/
TimeoutL 10
Http Method: POST
Content Type: application/json
Request Body: empty
Response Type: json
"""