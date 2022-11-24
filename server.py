from flask import Flask, Response, request, make_response, jsonify
import pymongo
from flask_cors import CORS, cross_origin

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
    
if __name__ == '__main__':
    app.run(debug=True)
