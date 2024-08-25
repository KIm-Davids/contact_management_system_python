from flask import Flask,Response, request
import pymongo
import json
from bson.objectid import ObjectId

app = Flask(__name__)

try:
   mongo = pymongo.MongoClient(host="localhost", port=27017, serverSelectionTimeoutMS = 1000)
   db =mongo.phonebook
   mongo.server_info()
except:
   print("Unable to connect to the MongoDB server !")

@app.route("/register/users", methods=['POST'])
def create_user():
   try:
      user = {"firstname":request.form["firstname"],"lastname":request.form["lastname"],"email":request.form["email"], "password":request.form["password"]}
      dbResponse = db.users.insert_one(user)
      print(dbResponse.inserted_id)
      return Response(response= json.dumps({"message": "Registered Successfully","id":f"{dbResponse.inserted_id}"}),status= 200, mimetype="application/json")
   except Exception as ex:
      print(ex)
      return Response({"message": "Registration failed"}, status= 500, mimetype="application/json")


@app.route("/get_users", methods=["GET"])
def get_users():
   try:

      return Response(
         json.dumps(data), status=200, mimetype="application/json"
      )
   except:
      return Response({"message": "Read Users failed"}, status= 500, mimetype="application/json")


@app.route("/login/user", methods=["POST"])
def login_user():
   try:
      user = {"email": request.form["email"], "password": request.form["password"]}
      dbResponse = db.users.insert_one(user)
      return Response(response= json.dumps({}))
   except:
      return Response({"message": "Failed to login"}, status=500, mimetype="application/json")



if __name__ == "__main__":
   app.run(port=80, debug=True)