from app import app, db, models
from sqlalchemy.orm.attributes import flag_modified


"""ONLY USED TO UPDATE EXISTING DATABASE FROM CLI
Updates users and user_mods with new timetable format
"""

def patch_users_and_mods(): 
    mods = models.User_Mods.query.all()
    for mod in mods: 
        mod.sem = 2
        flag_modified(mod, "sem")
        print(mod.sem)
        mod.get_timings()
        print(mod.class_grp)
        flag_modified(mod, "class_grp")
        db.session.commit()

    users = models.User.query.all()
    for u in users: 
        u.get_busy_time()
        flag_modified(u, "timetable")
        db.session.commit()

if __name__ == "__main__":
    patch_users_and_mods()
    print("done")