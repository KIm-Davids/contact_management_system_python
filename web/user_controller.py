from flask import Flask, request
# from mongo.services import user_services

app = Flask(__name__)


@app.post("/register/users")
def register_user():
    user_services.create_user(request.form["first_name"])
