import sys
from flask import Flask, flash, redirect, render_template, request, url_for
sys.path.append("/home/ndririchard/Documents/IDU4/INFO834/PROJECT_/")

from Server.mongo.mongo import *
from Server.redis.redis_ import *

app = Flask(__name__, template_folder="templates", static_folder="static")


@app.route("/")
def home():
    return render_template("home.html")

@app.route("/newUser")
def getNewUserPage():
    data = {
        "title" : "New User",
        "isSignIn" : True
    }
    return render_template("signinAndLogin.html", data = data)


@app.route("/user", methods=["POST"])
def verication():
    form = request.form
    ret = None
    isSignin = True

    if (form["IsSignin"] == "True"):
        ret = createUser(form["nkname"], form["nkpassword"])
        if (ret == -1):
            return render_template("error.html", msg = "This user already exist")

    else :
        ret = logUser(form["nkname"], form["nkpassword"])
        if (ret == -1):
            return render_template("error.html", msg = "Wrong credentials")

    return render_template("user.html", data = form["nkname"], message = "Welcom bro", rooms = getRoom())


@app.route("/login")
def getloginPage():
    data = {
        "title" : "Login",
        "isSignIn" : False
    }
    return render_template("signinAndLogin.html", data = data)


@app.route("/newRoom")
def CreateRoom_():
    return render_template("createRoom.html")


@app.route("/createRoomProcess", methods=["POST"])
def createRoomProcess():
    if not(isAbleToCreate(request.form["username"]) == 0):
       return render_template("user.html", data = request.form["username"], 
                                message = "You are not able to create a room :(", rooms = getRoom())

    ret = createRoom(request.form["username"], request.form["name"], request.form["pswd"])
    createItem(request.form["username"], ret)
    return render_template("user.html", data = request.form["username"], 
                                message = "Your room is created youpiii :)", rooms = getRoom())


@app.route("/room", methods=["POST"])
def room():
    roomObj = {"name" : request.form["room"], "password" : request.form["psswd"]}
    if (checkIfExist(roomObj)):
        return render_template("user.html", data = request.form["user"], 
                                message = "Invalid password", rooms = getRoom())
    for r in getRoom(roomObj):
        roomObj = r
        if request.form["user"] not in r.get("members"):
            joinRoom(request.form["user"], r.get("_id"))
    return render_template("room.html", room = roomObj, user = request.form["user"])
    
@app.route("/send", methods = ["POST"])
def send():
    newMessage(request.form["user"], getRoomId(request.form["room"]), request.form["msg"])
    return render_template("room.html", 
                           room = getRoomFromCursor(getRoom({"name" : request.form["room"]})), 
                           user = request.form["user"])

if __name__ == "__main__":
    app.run(debug=True)