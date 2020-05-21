from pyfluminus.authorization import vafs_jwt
from pyfluminus.api import name, modules, get_announcements
from pyfluminus.structs import Module
from flask import Flask, request, jsonify
import sys
from app import app

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
    print(login_info, file=sys.stderr)
    return vafs_jwt(login_info['userName'], login_info['password'])

@app.route('/name', methods=['POST'])
def userName(): 
    auth = request.get_json()
    return name(auth).data

@app.route('/activeModules', methods=['POST'])
def active_mods():
    auth = request.get_json()
    mods = modules(auth).data
    mods_dict = {}
    for mod in mods:
        mods_dict[mod.code] = {"name" : mod.name, "id" : mod.id}
    return mods_dict
    
@app.route('/annoucementsAll', methods = ['POST'])
def announcements():
    auth = request.get_json()
    mods = modules(auth).data
    announcements_list = {}
    for mod in mods:
        announcements_list[mod.code] = get_announcements(auth, mod.id, False).data
    return announcements_list