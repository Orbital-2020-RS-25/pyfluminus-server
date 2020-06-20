from pyfluminus.api import api

def get_class_grps(auth, mod_id): 
    api_path = "user/Resource/" + mod_id + "/Group"
    response = api(auth, api_path)
    data = response['ok']['data']
    print(data)
    class_grps = []
    for grp in data: 
        if 'classNo' in grp: 
            classNum = grp['classNo']
            classId = grp['id']
            class_grp = {
                'classNum': classNum, 
                'id': classId
            }
            class_grps.append(class_grp)
    return class_grps
