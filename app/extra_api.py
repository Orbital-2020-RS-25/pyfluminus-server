from pyfluminus.api import api

def get_class_grps(auth, mod_id): 
    api_path = "user/Resource/" + mod_id + "/Group"
    response = api(auth, api_path)
    data = response[data]
    class_grps = {}
    for grp in data: 
        if 'classNo' in grp: 
            classNum = grp['classNo']
            classId = grp['id']
            class_grps['classNum'] = classNum
            class_grps['id'] = classId
    return class_grps
