from sqlalchemy import Table, Column, ForeignKey, Integer, MetaData, Text, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import dataTypes
import json

Base = declarative_base()

class PlayerSave(Base):
    __tablename__ = "PlayerSave"
    name =  Column(Text, primary_key=True, unique=True)
    userdata = Column(Text)# saved as json string

    def __repr__(self):
        return "<PlayerSave name=%s stats=%s>" % (self.name, self.userdata)

engine = create_engine("sqlite:///database.db")
Base.metadata.create_all(engine)
DBSession = sessionmaker(bind=engine)

class DBInterface():
    def __init__(self):
        self.session = DBSession()

    #db functions like write read
    #create new save with user data passed
    def newSave(self, name, userdata):
        self.session.add(PlayerSave(name=name, userdata=json.dumps(userdata)))
        self.session.commit()

    #save userdata passed
    def save(self, name, userdata):
        userRef = self.session.query(PlayerSave).filter_by(name=name).first()
        if userRef:
            userRef.userdata = json.dumps(userdata)
            self.session.commit()
        else:
            print("Error saving to DB")

    #return save data of player
    def checkSave(self, name):
        userRef = self.session.query(PlayerSave).filter_by(name=name).first()
        if userRef:
            return userRef
        else:
            print("Save not found")
            return None
    #return all save data
    def returnAllSaves(self):
        return self.session.query(PlayerSave).all()
