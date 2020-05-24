from pyfluminus.authorization import vafs_jwt
from pyfluminus.api import name, modules, get_announcements
from pyfluminus.structs import Module
from flask import Flask, request, jsonify
import sys
from app import app, db, util
from app.models import User, User_Mods

#TODO add get class grps api with https://luminus.azure-api.net/user/Resource/{ResourceID}/Group[?sortby][&offset][&limit][&where]
HTTP_OK = 200
HTTP_NO_CONTENT = 204
HTTP_BAD_REQUEST = 400
HTTP_UNAUTHORISED = 401
HTTP_NOT_FOUND = 404

@app.route('/')
def index():
    return 'Main page'

# a simple page that says hello
@app.route('/hello')
def hello():
    return 'Hello, World!'

# receives login info and returns auth token, login info must be sent as application/json
@app.route('/login', methods=['POST'])
def login():
    login_info = request.get_json()
    auth = vafs_jwt("nusstu\\" + login_info['userName'], login_info['password'])
    if "error" in auth:
        return util.response_json(False, 1, auth), HTTP_UNAUTHORISED
    if User.query.get(login_info['userName']) == None: 
        uName = name(auth).data
        u = User(name = uName, nus_net_id = login_info['userName'])
        mods = util.get_active_mods(auth)
        for key in mods: 
            m = User_Mods(code=key, mod_id=mods[key]["id"], name=mods[key]["name"], term=mods[key]["term"], student=login_info['userName'])
            db.session.add(m)
            db.session.commit()
        db.session.add(u)
        db.session.commit()
    return util.response_json(True, 1, auth), HTTP_OK

@app.route('/name', methods=['POST'])
def userName(): 
    try: 
        auth = request.get_json()
        return util.response_json(True, 1, name(auth).data), HTTP_OK
    except: 
        return util.response_json(False, 1, {"error" : "Invalid"}), HTTP_NOT_FOUND

@app.route('/activeModules', methods=['POST'])
def active_mods():
    try: 
        auth = request.get_json()
        return util.get_active_mods(auth)
    except: 
        return util.response_json(False, 1, {"error" : "Invalid"}), HTTP_NOT_FOUND

@app.route('/announcementsAll', methods = ['POST'])
def announcements():
    try:
        auth = request.get_json()
        return util.get_all_announcement
    except: 
        return util.response_json(False, 1, {"error" : "Invalid"}), HTTP_NOT_FOUND

@app.route('/profile/<nusNetId>')
def profile(nusNetId):
    try: 
        user = User.query.get(nusNetId)
        mods = User_Mods.query.filter_by(student=nusNetId).all()
        mod_info = {}
        for mod in mods:
            mod_info[mod.code] = {"id" : mod.mod_id,
                                "name" : mod.name,
                                "term" : mod.term}
        return {"name" : user.name, 
                "mods" : mod_info}
    except: 
        return util.response_json(False, 1, {"error" : "Not found"}), HTTP_NOT_FOUND