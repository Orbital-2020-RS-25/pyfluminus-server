from pyfluminus.api import name, modules, get_announcements, current_term
from pyfluminus.structs import Module

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