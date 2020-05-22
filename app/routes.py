from pyfluminus.authorization import vafs_jwt
from pyfluminus.api import name, modules, get_announcements
from pyfluminus.structs import Module
from flask import Flask, request, jsonify
import sys
from app import app, db, util
from app.models import User, User_Mods

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
    return auth

@app.route('/name', methods=['POST'])
def userName(): 
    auth = request.get_json()
    return name(auth).data

@app.route('/activeModules', methods=['POST'])
def active_mods():
    auth = request.get_json()
    return util.get_active_mods(auth)
    
@app.route('/annoucementsAll', methods = ['POST'])
def announcements():
    auth = request.get_json()
    return util.get_all_annoucements

@app.route('/profile/<nusNetId>')
def profile(nusNetId):
    user = User.query.get(nusNetId)
    mods = User_Mods.query.filter_by(student=nusNetId).all()
    mod_info = {}
    for mod in mods:
        mod_info[mod.code] = {"id" : mod.mod_id,
                              "name" : mod.name,
                              "term" : mod.term}
    return {"name" : user.name, 
            "mods" : mod_info}
