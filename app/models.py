from app import db
from app.extra_api import get_timetable

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
    free_time = db.Column(db.JSON)
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

    def set_free_time(self): 
        time_slots = []
        
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
        if timetable != None: 
            for timing in timetable: 
                for grp in self.class_grp: 
                    if grp['lessonType'] == timing['lessonType'] and grp['classNum'][1:] == timing['classNo']: 
                        grp['timing'] = timing
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
