from pyfluminus.api import api
import requests

def get_class_grps(auth, mod_id): 
    print(auth)
    api_path = "user/Resource/" + mod_id + "/Group"
    response = api(auth, api_path)
    #print("\n")
    #print(mod_id)
    #print(response)
    #print("\n")
    try: 
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
    except KeyError: 
        print ("Not found")

def get_timetable(code, term, sem): 
    #print(term)
    term_year = term[:2]
    term_year_end = int(term_year) + 1
    #print(term_year)
    #print(term_year_end)
    term = "20{}-20{}".format(term_year, term_year_end)
    print(term)
    url = "https://api.nusmods.com/v2/{}/modules/{}.json".format(term, code)

    payload  = {}
    headers = {}
    response = requests.request("GET", url, headers=headers, data = payload)
    #print(response)
    if response.status_code == 404: 
        return None
    else: 
        contents = response.json()['semesterData'][sem - 1]['timetable']
        return contents