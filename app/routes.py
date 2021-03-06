from pyfluminus.authorization import vafs_jwt
from pyfluminus.api import name, modules, get_announcements
from pyfluminus.structs import Module

from flask import Flask, request, jsonify, redirect, url_for, render_template
import sys
from app import app, db, util
from app.models import User, User_Mods, Announcements, Mod_files
from app.extra_api import get_class_grps
import json

from sqlalchemy.orm.attributes import flag_modified

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

@app.route('/get_class_grps', methods=['POST'])
def f(): 
    mod_id = request.get_json()['mod_id']
    auth = request.get_json()['auth']
    return get_class_grps(auth, mod_id)

# receives login info and returns auth token, login info must be sent as application/json
@app.route('/login', methods=['POST'])
def login():
    login_info = request.get_json()

    print(login_info['userName']+'\n')
    
    if login_info['userName'] == 'test': 
        auth = {'jwt' : 'test'}
        return util.response_json(True, 1, auth), HTTP_OK

    auth = vafs_jwt("nusstu\\" + login_info['userName'].upper(), login_info['password'])
    if "error" in auth:
        return util.response_json(False, 1, auth), HTTP_UNAUTHORISED
        
    user_id = login_info['userName'].upper()

    if User.query.filter_by(nus_net_id=user_id).first() == None: 
        uName = name(auth).data
        u = User(name = uName, nus_net_id = user_id)
        #mods = util.get_active_mods(auth)
        db.session.add(u)
        db.session.commit()
        uId = User.query.filter_by(nus_net_id=user_id).first().id
        util.add_mods(auth, uId)
        u = User.query.get(uId)
        u.get_busy_time()
        flag_modified(u, "timetable")
        db.session.commit()

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
    user_id = login_info['userName'].upper()
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

    u = User.query.filter_by(nus_net_id=user_id).first()
    u.get_busy_time()
    flag_modified(u, "timetable")
    db.session.commit()
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
                                "term" : mod.term}
        return util.response_json(True, len(mods), {
            "name" : user.name, 
            "mods" : mod_info, 
            "timetable" : user.timetable}), HTTP_OK
    except: 
        return util.response_json(False, 1, {"error" : "Not found"}), HTTP_NOT_FOUND

@app.route('/modules/filesAll', methods=['POST'])
def files_all(): 
    auth = request.get_json()
    files = util.get_mod_files(auth)
    return util.response_json(True, len(files), files), HTTP_OK

@app.route('/modules/files', methods=['POST'])
def files():
    auth = request.get_json()['auth']
    code = request.get_json()['code']
    files = json.dumps(util.get_single_mod_files(auth, code))
    f = Mod_files(code=code, contents=files)
    db.session.add(f)
    db.session.commit()
    return util.response_json(True, len(files), files), HTTP_OK

@app.route('/modules/announcements', methods=['POST'])
def announcements_single(): 
    auth = request.get_json()['auth']
    code = request.get_json()['code']
    mod_id = User_Mods.query.filter_by(code=code).first().mod_id
    msgs = util.get_single_mod_announcements(auth, mod_id)
    m = Announcements(code=code, contents=msgs)
    db.session.add(m)
    db.session.commit()
    return util.response_json(True, len(msgs), msgs), HTTP_OK

@app.route('/modules/announcementsTest', methods=['POST'])
def aTest():
    #code = request.get_json()['code']
    #reply = Announcements.query.filter_by(code=code).first().contents
    #return util.response_json(True, len(reply), reply), HTTP_OK
    auth = request.get_json()['auth']
    code = request.get_json()['code']
    mod_id = User_Mods.query.filter_by(code=code).first().mod_id
    msgs = util.get_single_mod_announcements(auth, mod_id)
    m = Announcements(code=code, contents=msgs)
    db.session.add(m)
    db.session.commit()
    return util.response_json(True, len(msgs), msgs), HTTP_OK

@app.route('/modules/modFileTest', methods=['POST'])
def fTest():
    #code = request.get_json()['code']
    #reply = Mod_files.query.filter_by(code=code).first().contents
    #return util.response_json(True, len(reply), reply), HTTP_OK
    auth = request.get_json()['auth']
    code = request.get_json()['code']
    files = json.dumps(util.get_single_mod_files(auth, code))
    f = Mod_files(code=code, contents=files)
    db.session.add(f)
    db.session.commit()
    return util.response_json(True, len(files), files), HTTP_OK 