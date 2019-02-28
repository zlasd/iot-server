
from datetime import datetime
import math


from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column,Integer,String,Text,DateTime, \
                ForeignKey,Table,Float,Enum,desc,Boolean,func
from sqlalchemy.orm import relationship,backref
from flask import url_for

from myapp import db

class Device(db.Model):
    __tablename__ = 'device'
    
    ID = Column(Integer, primary_key=True)
    name = Column(String(64), nullable=False, unique=True, index=True)
    type = Column(String(64))
    address = Column(String(256))
    passwd = Column(String(256), nullable=False)
    joinTime = Column(DateTime, default=datetime.now)
    live = Column(Boolean, nullable=False)
    
    def __init__(self, name, type, addr, passwd):
        self.name = name
        self.type = type
        self.address = addr
        self.passwd = passwd
        self.joinTime = datetime.now()
        self.live = True
        
    def __repr__(self):
        return '<Device#{}-{}>'.format(self.ID, self.name)
    

    
class Alert(db.Model):
    __tablename__ = 'alert'
    
    alertID = Column(Integer, primary_key=True)
    deviceID = Column(Integer, ForeignKey('device.ID'))
    time = Column(DateTime, default=datetime.now)
    personNo = Column(Integer)
    confidence = Column(Float)
    
    device = relationship('Device', backref=backref('alerts', order_by=desc(time)))
    
    def __init__(self, deviceID, personNo, confidence):
        self.deviceID = deviceID
        self.personNo = personNo
        self.confidence = confidence
        self.time = datetime.now()
    
    def __repr__(self):
        return '<Alert {}>'.format(self.alertID)
