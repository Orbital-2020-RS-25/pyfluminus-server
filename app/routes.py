from pyfluminus.authorization import vafs_jwt
from pyfluminus.api import name, modules, get_announcements
from pyfluminus.structs import Module

from flask import Flask, request, jsonify, redirect, url_for, render_template
import sys
from app import app, db, util
from app.models import User, User_Mods
from app.extra_api import get_class_grps

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
        
    user_id = login_info['userName']

    if User.query.filter_by(nus_net_id=user_id).first() == None: 
        uName = name(auth).data
        u = User(name = uName, nus_net_id = user_id)
        #mods = util.get_active_mods(auth)
        db.session.add(u)
        db.session.commit()
        uId = User.query.filter_by(nus_net_id=user_id).first().id
        util.add_mods(auth, uId)

    return util.response_json(True, 1, auth), HTTP_OK

@app.route('/name', methods=['POST'])
def userName(): 
    try: 
        auth = request.get_json()
        return util.response_json(True, 1, name(auth).data), HTTP_OK
    except: 
        return util.response_json(False, 1, {"error" : "Invalid"}), HTTP_NOT_FOUND

@app.route('/updateProfile', methods=['POST'])
def updateProfile(): 
    login_info = request.get_json()
    auth = vafs_jwt("nusstu\\" + login_info['userName'], login_info['password'])
    user_id = login_info['userName']
    if "error" in auth:
        return util.response_json(False, 1, auth), HTTP_UNAUTHORISED

    if User.query.filter_by(nus_net_id=user_id).first() != None:
        uName = name(auth).data
        db.update(User).where(User.nus_net_id==user_id).values(name=uName)
        db.session.commit()
    else: 
        uName = name(auth).data
        u = User(name = uName, nus_net_id = user_id)
        db.session.add(u)
        db.session.commit()
    
    if User.query.filter_by(nus_net_id=user_id).first().mods == []: 
        uId = User.query.filter_by(nus_net_id=user_id).first().id
        util.add_mods(auth, uId)
    else: 
        uId = User.query.filter_by(nus_net_id=user_id).first().id
        util.update_mods(auth, uId)

    return redirect(url_for('profile', nusNetId=user_id))

@app.route('/activeModules', methods=['POST'])
def active_mods():
    try: 
        auth = request.get_json()
        mods = util.get_active_mods(auth)
        return util.response_json(True, len(mods), mods), HTTP_OK
    except: 
        return util.response_json(False, 1, {"error" : "Invalid"}), HTTP_NOT_FOUND

@app.route('/announcementsAll', methods = ['POST'])
def announcements():
    try:
        auth = request.get_json()
        msgs = util.get_all_announcement(auth)
        return util.response_json(True, len(msgs), msgs), HTTP_OK
    except: 
        return util.response_json(False, 1, {"error" : "Invalid"}), HTTP_NOT_FOUND

@app.route('/profile/<nusNetId>')
def profile(nusNetId):
    try: 
        user = User.query.filter_by(nus_net_id=nusNetId).first()
        uId = user.id
        mods = User_Mods.query.filter_by(student=uId).all()
        mod_info = {}
        for mod in mods:
            mod_info[mod.code] = {"id" : mod.mod_id,
                                "name" : mod.name,
                                "term" : mod.term, 
                                "class_grps" : mod.class_grp}
        return util.response_json(True, len(mods), {"name" : user.name, 
                "mods" : mod_info}), HTTP_OK
    except: 
        return util.response_json(False, 1, {"error" : "Not found"}), HTTP_NOT_FOUND

@app.route('/modules/filesAll', methods=['POST'])
def files_all(): 
    auth = request.get_json()
    files = util.get_mod_files(auth)
    return util.response_json(True, len(files), files), HTTP_OK