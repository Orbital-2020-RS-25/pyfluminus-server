from pyfluminus.api import name, modules, get_announcements, current_term
from pyfluminus.structs import Module

def get_active_mods(auth):
    mods = modules(auth).data
    mods_dict = {}
    for mod in mods:
        mods_dict[mod.code] = {"name" : mod.name, "id" : mod.id, "term" : mod.term}
    return mods_dict

def get_all_annoucements(auth):
    mods = modules(auth).data
    announcements_list = {}
    for mod in mods:
        announcements_list[mod.code] = get_announcements(auth, mod.id, False).data
    return announcements_list

def get_current_term(auth):
    """returns current term data in dict
        e.g.: {term: "1820", description: "2018/2019 Semester 2"}
    """
    return current_term(auth).data