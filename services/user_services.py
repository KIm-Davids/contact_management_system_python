import flask
import pymongo
import json
from bson.objectid import ObjectId
from exceptions import mycustomexception
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from validations.user_validation import validations

validate = validations()

app = Flask(__name__)



try:
    mongo = pymongo.MongoClient(host="localhost", port=27017, serverSelectionTimeoutMS=1000)
    db = mongo.phonebook
    mongo.server_info()
except:
    print("Unable to connect to the MongoDB server !")


def create_user(first_name):
    try:
        last_name = request.form["lastname"]
        email = request.form["email"]
        password = request.form["password"]

        hashed_password = generate_password_hash(password)

        # if email["email"] == " ":
        #    return Response(response=)

        user = {
            "firstname:": first_name,
            "lastname": last_name,
            "email": email,
            "password": hashed_password,
            "login_status": "offline"
        }

        dbResponse = db.users.insert_one(user)
        print(dbResponse.inserted_id)
        return Response(response=json.dumps({"message": "Registered Successfully", "id": f"{dbResponse.inserted_id}"}),
                        status=200, mimetype="application/json")
    except Exception as ex:
        print(ex)
        return Response({"message": "Registration failed"}, status=500, mimetype="application/json")


@app.get("/get_users")
def get_users():
    try:
        data = list(db.users.find())
        for user in data:
            user["_id"] = str(user["_id"])
        return Response(
            json.dumps(data), status=200, mimetype="application/json"
        )
    except:
        return Response({"message": "Read Users failed"}, status=500, mimetype="application/json")


@app.patch("/login/user/")
def update_user():
    try:
        email = request.form["email"]
        password = request.form["password"]

        user = db.users.find_one({"email": email})

        if user and check_password_hash(user["password"], password):
            db.users.update_one({"email": email}, {"$set": {"login_status": "online"}})
            # dbResponse = db.users.find_one({"email": email}, {"$set": {"firstname": request.form["firstname"]}})
            return Response(response=json.dumps({"message": "login Successfully", "status": "online"}), status=200,
                            mimetype="application/json")

        else:
            return Response(response=json.dumps({"message": "Invalid email or password", "status": "Login failed"}),
                            status=200, mimetype="application/json")
        # return Response(response= json.dumps({"message": "Login Successful"}), status=200, mimetype="application/json")

    except Exception as ex:
        print(ex)
    return Response(response=json.dumps({"message": "Login failed"}), status=400, mimetype="application/json")


@app.route("/create-contact", methods=["PATCH"])
def create_contact():
    name = request.form["contact_name"]
    phone_number = request.form["contact_phonenumber"]

    contact_list = db.users
    contacts_found = contact_list.find()

    ids = [str(contact_id) for contact_id in contacts_found]
    return Response(response=json.dumps({"all_ids": ids}), status=200, mimetype="application/json")


def check_if_user_is_online(email):
    user = db.users.find_one({"email": email})

    if user["login_status"] == "online":
        return True
    else:
        return False


# def set_user_register_login_status(email):
#    if
#


# @app.route("/login/user", methods=["POST"])
# def login_user():
#    try:
#       user = {"email": request.form["email"], "password": request.form["password"]}
#       login_status = verifyuser(user)
#       is_logged_in = {"login_status": login_status}
#       dbResponse = db.users.insert_one(user, is_logged_in)
#       if login_status == True:
#          return Response(response= json.dumps({"User Logged in successfully"}, status=200, mimetype="application/json"))
#    except:
#       return Response(response={"message": "Failed to login"}, status=500, mimetype="application/json")
#

# def verifyuser(user):
#    data = list(db.users.find())
#    for user_from_database in data:
#       user_from_database["_id"] = str(user_from_database["_id"])
#       if user["email"] != user_from_database["email"]:
#          raise mycustomexception("Invalid details")
#       if user["password"] != user_from_database["password"]:
#          raise mycustomexception("Invalid details")
#    return True

if __name__ == "__main__":
    app.run(port=80, debug=True)
