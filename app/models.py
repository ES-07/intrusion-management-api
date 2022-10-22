from operator import index
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import datetime as _dt


import app.database as _database


Base  = declarative_base()


class User(_database.Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), index=True)
    email = Column(String(50), unique=True)

    properties = relationship('Property', back_populates='owner')

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

class Property(_database.Base):
    __tablename__ = 'properties'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True)
    location = Column(String(50), unique=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    
    # N relationship with User
    owner = relationship('User', back_populates='properties')

    
    cameras = relationship('Camera', back_populates='property')
    intrusion = relationship('Intrusion', back_populates='property')

    def __repr__(self):
        return f"Property('{self.name}', '{self.location}', '{self.price}')"

class Camera(_database.Base):
    __tablename__ = 'cameras'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True)
    location = Column(String(50), unique=True)

    property_id = Column(Integer, ForeignKey('properties.id'))
    property = relationship('Property', back_populates='cameras')

    def __repr__(self):
        return f"Camera('{self.name}', '{self.location}')"

class Intrusion(_database.Base):
    __tablename__ = 'intrusions'

    id = Column(Integer, primary_key=True, index=True)
    
    timestamp = Column(DateTime(timezone=True), default=_dt.datetime.utcnow)
    
    property_id = Column(Integer, ForeignKey('properties.id'))
    property = relationship('Property', back_populates='intrusion')

    def __repr__(self):
        return f"Intrusion('{self.camera_id}', '{self.timestamp}')"