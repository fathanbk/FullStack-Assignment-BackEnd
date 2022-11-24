from flask import Flask, Response, request, make_response, jsonify
import pymongo
from flask_cors import CORS, cross_origin
from bson.objectid import ObjectId
import json

app = Flask(__name__)

CORS(app)

try:
    mongo = pymongo.MongoClient(
        host="mongodb://localhost:27017",
        serverSelectionTimeoutMS = 3000
    )
    db = mongo.fishapi
    mongo.server_info()
except:
    print("ERROR - Cannot connect to database")

@app.route('/register', methods=['POST'])
def pondRegister():
    try:
        data = {
            "name": request.json['name'],
            "location": request.json['location'],
            "shape": request.json['shape'],
            "material": request.json['material']
        }

        dbResponse = db.pond.insert_one(data)
        response = make_response(
                jsonify(
                    {"message": "Pond created successfully"}
                ),
                200,
            )
        response.headers["Content-Type"] = "application/json"
        
        return response
    except Exception as e: 
        response = make_response(jsonify({"error":str(e)}),500)
        response.headers["Content-Type"] = "application/json"
        return response
    
@app.route("/", methods=["GET"])
def getPond():
    try:
        data = list(db.pond.find())
        for pond in data:
            pond['_id'] = str(pond['_id'])

        response = make_response(
                jsonify(data,
                    {"message": "Pond fetched successfully"}
                ),
                200,
            )
        response.headers["Content-Type"] = "application/json"

        return response
    except Exception as e:
       response = make_response(jsonify({"error":str(e)}),500)
       response.headers["Content-Type"] = "application/json"
       return response

@app.route('/pond/<id>', methods=['PATCH'])
def pondUpdate(id):
    try:
        if request.method == 'PATCH':
            data = {
                "name": request.json['name'],
                "location": request.json['location'],
                "shape": request.json['shape'],
                "material": request.json['material'],
                }
            dbResponse = db.pond.update_one({'_id': ObjectId(id)}, {'$set': data})
            response = make_response(
                    jsonify(
                        {"message": "Pond updated successfully"}
                    ),
                    200,
                )
            response.headers["Content-Type"] = "application/json"
            
            return response
        return make_response(
            jsonify(
                {"message": "Pond already updated"}
            ),
            200,
        )
    except Exception as e:
        return Response(
            response=json.dumps({"message": "An error occurred", "error": str(e)}),
            status=500,
            mimetype="application/json"
        )
    
if __name__ == '__main__':
    app.run(debug=True)
