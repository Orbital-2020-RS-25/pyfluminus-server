from app import db

class User:
    def __init__(self, netId, name, mods, term):
        self.netId = netId
        self.name = name
        self.mods = mods
        self.term = term

    