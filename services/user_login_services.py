def verifyUser(self,user):
    data = list(db.users.find())
    for user_from_database in data:
        user_from_database["_id"] = str(user_from_database["_id"])
        if user["email"] != user_from_database["email"]:
