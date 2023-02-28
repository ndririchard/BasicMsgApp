# imports
import datetime as dt
import pymongo as pmg
from bson.objectid import ObjectId

# create a mongo client
clt = pmg.MongoClient("localhost", 27017)

# Api's functions

def checkIfExist(Obj, isRoom=True, clt=clt):
    if (isRoom):
        return 0 == clt.App["Rooms"].count_documents(Obj)
    else : 
        return 0 == clt.App["Users"].count_documents(Obj)

# Users

def createUser(nkname, passwd, clt=clt):
    user = {"nickname" : nkname, "password" : passwd}
    if (checkIfExist({"nickname" : nkname}, False)):
        user_id = clt.App["Users"].insert_one(user).inserted_id
        return user_id
    else : 
        return -1

def logUser(nkname, passwd, clt=clt):
    user = {"nickname" : nkname, "password" : passwd}
    if not(checkIfExist(user, False)):
        return 0
    return -1

def deleteUser(nkname, clt=clt):
    user = {"nickname" : nkname}
    if not(checkIfExist(user, False)):
        clt.App["Users"].delete_one(user)
        return 0
    else :
        return -1

def joinRoom(user, room, clt=clt):
    if not(checkIfExist({"nickname" : user}, False)) and not(checkIfExist({"_id" : ObjectId(room)})):
        clt.App.Rooms.update_one(
            {"_id" : ObjectId(room)},
            {"$push" : {"members" : user}}
        )
        return 0
    else:
        return -1

# Rooms

def createRoom(user, name, passwd, clt=clt):
    room = {
        "author" : user,
        "name" : name,
        "password" : passwd,
        "creation_date" : dt.datetime.utcnow(),
        "members" : [],
        "messages" : []
    }
    if not(checkIfExist({"nickname" : user}, False)):
        if (checkIfExist({"name" : name})):
            room_id = clt.App["Rooms"].insert_one(room).inserted_id
            joinRoom(user, ObjectId(room_id))
            return room_id
        else:
            return -1
    else:
        return -1


def getRoom(filter_=None, clt=clt):
    if filter_ == None:
        return clt.App.Rooms.find({})
    return clt.App.Rooms.find(filter_)


def deleteRoom(room_id, clt=clt):
    if not(checkIfExist({"_id" : ObjectId(room_id)})):
        clt.App["Rooms"].delete_one({"_id" : ObjectId(room_id)})
        return 0
    return -1

# Messages
def newMessage(sd_user, room_id, text, clt=clt):
    if not(checkIfExist({"_id" : ObjectId(room_id)})):
        if sd_user in clt.App.Rooms.find_one({"_id" : ObjectId(room_id)}).get("members"):
            clt.App.Rooms.update_one(
                {"_id" : ObjectId(room_id)},
                {"$push" : {"messages" : {"from" : sd_user, "msg" : text}}}
            )
            return 0
    return -1

def getRoomId(name):
    r = None
    rooms = getRoom({"name" : name})
    for room in rooms:
        r = room.get("_id")
    return r


def getRoomFromCursor(r):
    for ro in r:
        return ro

if __name__ == "__main__":
    newMessage("Ana", "63f76c743e582b77eafdac15", "Hello guys")
    newMessage("Ana", "63f76c743e582b77eafdac15", "How are you?")