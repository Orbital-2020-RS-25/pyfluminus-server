from app import db

class User(db.model):
    #database id
    id = db.Column(db.Integer, primary_key=True)
    #name of user, not unique as people may have same names
    name = db.Column(db.String(64), index=True, unique=False)
    #NUSNET ID, the EXXXXXXX number
    nus_net_id = db.Column(db.String(8), index=True, unique=True)

    def __repr__(self):
        return "<User {}>".format(self.name)