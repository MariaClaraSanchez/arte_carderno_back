from flask import Flask, Response, request
from bson.objectid import ObjectId

import pymongo
import json

# Iniciando a aplicação
app = Flask("__name__")


try:
    mongo = pymongo.MongoClient(
        host="localhost",
        port = 27017,
        serverSelectionTimeoutMS = 1000
    )
    db = mongo.company
    mongo.server_info() # trigger execpetion if cannot connect to db
except:
    print("ERROR - Canoot connect to db")


#Criação rotas

# ************** GET ************** 
@app.route("/users", methods=["GET"])
def get_some_users():
    try:
        data = list(db.users.find())
        
        for user in data: user["_id"] = str(user["_id"])

        return Response(
            response= json.dumps([
                data
                ]),
            status= 200,
            mimetype= "application/json"
        )
    except Exception as ex:
        print(ex)
        return Response(response= json.dumps({"message": "Cannot read users"}),status= 500,mimetype= "application/json")


# ************** POST ************** 
@app.route("/users", methods=["POST"])
def create_user():
    try:
        user = {
            "name": request.form['name'], 
            "lastName": request.form['lastName']
            }
        dbResponse = db.users.insert_one(user)
        print(dbResponse.inserted_id)

        return Response(
            response= json.dumps({
                "message": "User created", 
                "id": f"{dbResponse.inserted_id}"
                }),
            status= 200,
            mimetype= "application/json"
        )
    except Exception as ex:
        print(ex)


# ************** PATCH ************** 
@app.route("/users/<id>", methods=["PATCH"])
def update_users(id):
    try:
        dbResponse = db.users.update_one(
            {"_id":ObjectId(id)},
            {"$set": {"name": request.form["name"]}}
        )

        if dbResponse.modified_count == 1:
            return Response(
                response= json.dumps({"message": "User update"}),
                status= 200,
                mimetype= "application/json"
            )

        return Response(
                response= json.dumps({"message": "Nothing to update"}),
                status= 500,
                mimetype= "application/json"
            )
    except Exception as ex:
        print(ex)
        return Response(response= json.dumps({"message": "Sorry cannot update user"}),status= 500,mimetype= "application/json")


# ************** DELETE ************** 
@app.route("/users/<id>", methods=["DELETE"])
def delete_users(id):
    try:
        dbResponse = db.users.delete_one({"_id":ObjectId(id)})

        if dbResponse.deleted_count == 1:
            return Response(
                response= json.dumps({"message": "User delete", "id":f"{id}"}),
                status= 200,
                mimetype= "application/json"
            )
        return Response(
                response= json.dumps({"message": "User not found", "id":f"{id}"}),
                status= 200,
                mimetype= "application/json"
            )
    except Exception as ex:
        print(ex)
        return Response(response= json.dumps({"message": "Sorry cannot delete this user"}),status= 500,mimetype= "application/json")

# Conexão
if __name__ == "__main__":
    app.run(port=80, debug=True)

print("a")