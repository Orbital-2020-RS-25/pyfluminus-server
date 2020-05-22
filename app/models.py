from app import db

class User(db.Model):
    #database id
    id = db.Column(db.Integer, primary_key=True)
    #name of user, not unique as people may have same names
    name = db.Column(db.String(64), index=True, unique=False)
    #NUSNET ID, the EXXXXXXX number
    nus_net_id = db.Column(db.String(8), index=True, unique=True)

    def __repr__(self):
        return "<User {}>".format(self.name)

class User_Mods(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(8), index=True, unique=False)
    mod_id = db.Column(db.String(64), index=True, unique=False)
    class_grp = db.Column(db.String(6), index=True, unique=False, default="T0")
    term = db.Column(db.String(6), index=True, unique=False)
    student = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return "<Mod {} taken by {}>".format(self.code, self.student)