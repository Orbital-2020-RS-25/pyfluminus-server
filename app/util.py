from pyfluminus.api import name, modules, get_announcements, current_term
from pyfluminus.structs import Module
from pyfluminus.fluminus import get_links_for_module

from app import db
from app.models import User, User_Mods
from app.extra_api import get_class_grps

def get_active_mods(auth):
    """Gets all active mods taken by authenticated student. 

    :param auth: Authentication token issued from Luminus
    :type auth: dict
    :return: Mods and their details in a dictionary
            e.g.: {CS2030 : {"name" : Module name, 
                             "id"   : Module id, 
                             "term" : Term this module is taken in}}
    :rtype: dict
    """
    mods = modules(auth).data
    mods_dict = {}
    for mod in mods:
        mods_dict[mod.code] = {"name" : mod.name, "id" : mod.id, "term" : mod.term}
    return mods_dict

def get_all_announcement(auth):
    """Gets all announcements the current authenticated user has. 

    :param auth: Authentication token issued from Luminus
    :type auth: dict
    :return: Dictionary of all announcements the user has, grouped by modules
    :rtype: dict
    """
    mods = modules(auth).data
    announcements_list = {}
    for mod in mods:
        announcements_list[mod.code] = get_announcements(auth, mod.id, False).data
    return announcements_list

def get_current_term(auth):
    """Gets the current semester this student is in. 

    :param auth: Authentication token issued by Luminus
    :type auth: dict
    :return: Current term of the student
    :rtype: dict
    """
    return current_term(auth).data

def response_json(status, count, data): 
    """Generates JSON for http responses

    :param status: True if data is valid and there are no errors, False otherwise
    :type valid: boolean
    :param code: http response code
    :type code: int
    :param count: Total number of fields in data
    :type count: int
    :param data: json structure for the actual data
    :type data: dict
    :return: Dictionary comprising of all the params to be sent to client as JSON
    :rtype: dict
    """
    return {
        "status" : status, 
        #"code"  : code, 
        "count" : count,
        "data"  : data
    }

def add_mods(auth, uId): 
    mods = get_active_mods(auth)
    for key in mods: 
        mod_id = mods[key]["id"]
        class_grp = get_class_grps(auth, mod_id)
        m = User_Mods(code=key, mod_id=mod_id, name=mods[key]["name"], class_grp=class_grp, term=mods[key]["term"], student=uId)
        db.session.add(m)
        db.session.commit()

def update_mods(auth, uId): 
    mods = get_active_mods(auth)
    old_mods = User.query.get(uId).mods
    for mod in old_mods: 
        db.session.delete(mod)
        db.session.commit()
    add_mods(auth, uId)

def get_mod_files(auth): 
    mods = modules(auth).data
    files = []
    for module in mods:
        if module is None:
            continue
        data = get_links_for_module(auth, module)
        files.append(data)
    return files

def get_single_mod_files(auth, code): 
    mods = modules(auth).data
    for mod in mods: 
        if mod is None: 
            continue
        if mod.code == code: 
            return get_links_for_module(auth, mod)
    return None

def get_single_mod_announcements(auth, mod_id):
    return get_announcements(auth, mod_id, False).data