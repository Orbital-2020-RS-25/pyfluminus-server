from app import db

class User(db.Model):
    #database id
    id = db.Column(db.Integer)
    #name of user, not unique as people may have same names
    name = db.Column(db.String(64), index=True, unique=False)
    #NUSNET ID, the EXXXXXXX number
    nus_net_id = db.Column(db.String(8), index=True, unique=True, primary_key=True)
    mods = db.relationship('User_Mods', backref='student_taking', lazy='dynamic')

    def __repr__(self):
        return "<User {}>".format(self.name)

class User_Mods(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(8), index=True, unique=False)
    mod_id = db.Column(db.String(64), index=True, unique=False)
    name = db.Column(db.String(30))
    class_grp = db.Column(db.String(6), index=True, unique=False, default="T0")
    term = db.Column(db.String(6), index=True, unique=False)
    student = db.Column(db.Integer, db.ForeignKey('user.nus_net_id'))

    def __repr__(self):
        return "<Mod {} taken by {}>".format(self.code, self.student)