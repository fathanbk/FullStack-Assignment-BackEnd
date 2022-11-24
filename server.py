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
        return jsonify({"error":str(e)})
    
@app.route("/", methods=["GET"])
def getPond():
    try:
        data = list(db.pond.find())
        for pond in data:
            pond['_id'] = str(pond['_id'])

        return Response(
            response= json.dumps(data),
            status=200, 
            mimetype="application/json")
    except Exception as e:
        return Response(
            response=json.dumps({"message": "An error occurred", "error": str(e)}),
            status=500,
            mimetype="application/json"
        )
    
if __name__ == '__main__':
    app.run(debug=True)
