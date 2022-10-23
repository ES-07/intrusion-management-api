from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Date, Enum
from sqlalchemy.orm import relationship

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import datetime as _dt
from app.enums import Notification_type, DeviceState

from app.database import Base


class Person(Base):
    __tablename__ = "person"

    id_number = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String, unique=True)
    hashed_password = Column(String)
    address = Column(String)
    cellphone = Column(Integer, unique=True)
    birthday = Column(Date)

    property_owners = relationship("PropertyOwner", back_populates="person")
    security_managers = relationship("SecurityManager", back_populates="person")

#acho que bastava um enum para distinguir

class SecurityManager(Person):
    __tablename__ = "securitymanager"

    person = relationship("Person", back_populates="security_managers")
    worker_id = Column(Integer, ForeignKey("person.id_number"), primary_key=True)

class PropertyOwner(Person):
    __tablename__ = "propertyowner"

    property_owner_id = Column(Integer, ForeignKey("person.id_number"), primary_key=True)
    contract_date = Column(Date)
    notification_type = Column(Enum(Notification_type, default=Notification_type.TXT_MSG))
    person = relationship("Person", back_populates="property_owners")
    
    
    buildings = relationship("Building", back_populates="owner")




class Building(Base):
    __tablename__ = "buildings"

    id = Column(Integer, primary_key=True, index=True)
    address = Column(String(100), index=True)
    
    # Foreign Keys
    client_id = Column(Integer, ForeignKey("propertyowner.property_owner_id"))
    security_manager_id = Column(Integer, ForeignKey("securitymanager.worker_id"))


    # Relationships
    client = relationship("PropertyOwner", back_populates="buildings")
    security_manager = relationship("SecurityManager", back_populates="buildings")
    intrusions = relationship("Intrusion", back_populates="building")


class Intrusion(Base):
    __tablename__ = "intrusions"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, default=_dt.datetime.utcnow)

    building_id = Column(Integer, ForeignKey("buildings.id"))
    building = relationship("Building", back_populates="intrusions")


"""class User(_database.Base):
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
        return f"Intrusion('{self.camera_id}', '{self.timestamp}')"""