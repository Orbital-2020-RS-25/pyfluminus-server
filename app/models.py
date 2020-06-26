from app import db
from app.extra_api import get_timetable

from datetime import datetime  
from datetime import timedelta  

def get_dates(week, day_of_week, start, end):
    sem_start = datetime(year=2020, month=1, day=13, hour=0, minute=0, second=0) 
    day = {
        "Monday": 0,
        "Tuesday": 1, 
        "Wednesday": 2, 
        "Thursday": 3, 
        "Friday": 4, 
        "Saturday": 5, 
        "Sunday": 6
    }
    if week < 7: 
        week = week - 1 #offset recess week after week 6

    days_to_add = float(7 * week + day[day_of_week])
    start_time = sem_start + timedelta(days=days_to_add, hours=float(start[0:2]), minutes=float(start[2:3]))
    end_time = sem_start + timedelta(days=days_to_add, hours=float(end[0:2]), minutes=float(end[2:]))
    date_of_lesson = start_time.date()
    def makeStr(time): 
        return time.strftime("%Y-%m-%dT%H:%M:%S")

    return (makeStr(start_time), makeStr(end_time), date_of_lesson.strftime("%Y-%m-%d"))

class User(db.Model):
    """Database table for a user. Implemented with flask-SQLalchemy. 

    :param name: Name of student
    :type name: String, maximum size 64
    :param nus_net_id: NUSnet ID of the student, the EXXXXXXX number
    :type nus_net_id: String, maximum size 8
    """
    __tablename__ = 'users'
    #database id
    id = db.Column(db.Integer, primary_key=True)
    #name of user, not unique as people may have same names
    name = db.Column(db.String(64), index=True, unique=False)
    #NUSNET ID, the EXXXXXXX number
    nus_net_id = db.Column(db.String, index=True, unique=True)
    timetable = db.Column(db.JSON)
    mods = db.relationship('User_Mods', backref='student_taking')

    def add_friend(self, user_to_be_added):
        try: 
            user_id = User.query.filter_by(nus_net_id=user_to_be_added).first().id
        except: 
            raise ValueError("User not found")
        if Friends.query.filter_by(student=self.nus_net_id).filter_by(friend=user_to_be_added).first() != None: 
            new_friend = Friends(student=self.nus_net_id, friend=user_to_be_added)
            db.session.add(new_friend)
            db.commit()
            return True
        else: 
            return False
    
    def get_busy_time(self): 
        time_slots = {}
        mods = User_Mods.query.filter_by(student=self.id).all()
        for mod in mods:
            #mods are keys 
            code = mod.code
            mod_name = mod.name
            classes = mod.class_grp #array
            for lesson in classes: 
                #print(lesson)
                if not lesson: 
                    break
                lesson_timing = lesson['timing']
                if not lesson_timing: 
                    break
                lesson_timing = lesson_timing[0]
                day = lesson_timing['day']
                start = lesson_timing['startTime']
                end = lesson_timing['endTime']
                lesson_type = lesson['lessonType']
                venue = lesson_timing['venue']
                weeks = lesson_timing['weeks']
                for week in weeks: 
                    timing = get_dates(week, day, start, end)
                    calendar_item = {
                        'start': timing[0], 
                        'end': timing[1], 
                        'name': {
                            'code': code, 
                            'lessonType': lesson_type, 
                            'venue': venue, 
                            'name': mod_name
                        }
                    }
                    if timing[2] in time_slots: 
                        time_slots[timing[2]].append(calendar_item)
                    else: 
                        time_slots[timing[2]] = [calendar_item]
        self.timetable = time_slots

            
        
    def __repr__(self):
        return "<User {}, {}, {}>".format(self.name, self.nus_net_id, self.id)

class User_Mods(db.Model):
    """Represents mods taken by a user in the database. 

    :param code: Module code of the mod, i.e. CS2030, UTW1001R
    :type code: String, maximum size 8
    :param mod_id: Module id used by luminus
    :type mod_id: String, maximum size 64
    :param name: Name of the module
    :type name: String, maximum size 30
    :param class_grp: Class group of the student taking this module, defaults to T0 for now #TODO#
    :type class_grp: String, maximum size 6
    :param term: The semester which this module is taken in
    :type term: String, maximum size 6
    :param student: NUSnet ID of the student taking this module
    :type student: String, maximum size 8

    """
    __tablename__ = 'user_mods'
    id = db.Column(db.Integer, index=True, primary_key=True)
    code = db.Column(db.String(8), index=True, unique=False)
    mod_id = db.Column(db.String(64), index=True, unique=False)
    name = db.Column(db.String)
    class_grp = db.Column(db.JSON)
    #files = db.Column(db.JSON) #tree structure
    term = db.Column(db.String(6), index=True, unique=False)
    sem = db.Column(db.Integer)
    student = db.Column(db.Integer, db.ForeignKey('users.id'))
    student_taking_mod = db.relationship('User', backref='mod_taken_by')

    def get_timings(self): 
        timetable = get_timetable(self.code, self.term, self.sem)
        for grp in self.class_grp: 
            letter = grp['classNum'][0]
            if letter == 'L': 
                lesson = 'Lecture'
            elif letter == 'B': 
                lesson = "Laboratory"
            elif letter == 'T': 
                lesson = 'Tutorial'
            else: 
                lesson = "Sectional Teaching"

            grp['lessonType'] = lesson
            grp['timing'] = []

        if timetable != None: 
            for timing in timetable: 
                for grp in self.class_grp: 
                    if grp['lessonType'] == timing['lessonType'] and grp['classNum'][1:] == timing['classNo']: 
                        grp['timing'].append(timing)
                        break
        return self

    def __repr__(self):
        return "<Mod {} taken by {}>".format(self.code, self.student)

class Announcements(db.Model): 
    id = db.Column(db.Integer, index=True, primary_key=True)
    code = db.Column(db.String)
    contents = db.Column(db.JSON)
    def __repr__(self): 
        return "<Announcement {} under ()>".format(self.contents, self.code)

class Mod_files(db.Model):
    id = db.Column(db.Integer, index=True, primary_key=True)
    code = db.Column(db.String)
    contents = db.Column(db.JSON)

class Friends(db.Model): 
    id = db.Column(db.Integer, index=True, primary_key=True)
    student = db.Column(db.String)
    friend = db.Column(db.Integer)
    def __repr__(self): 
        return "<{} is a friend of {}>".format(self.friend, self, student)
#class Mod_Files(db.Model): 
#    __tablename__ = 'mod_files'
#    id = db.Column(db.Integer, index=True, primary_key=True)
#    mod_db_id = db.Column(db.Integer, db.ForeignKey('user_mods.id'))
#    filename = db.Column(db.String, index=True, unique=False)
#    file_path = db.Column(db.String, unique=True)
#    mod_belonging_to = db.relationship('User_Mods', backref='contained_files')
#    
#    def __repr__(self): 
#        return "<File {} with path {} under module {}>".format(self.filename, self.file_path, self.mod_belonging_to)
