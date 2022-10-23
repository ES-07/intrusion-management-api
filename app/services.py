from requests import delete
import app.database as _db

from app.models import *

from sqlalchemy.orm import Session


def _add_tables():
    return _db.Base.metadata.create_all(bind=_db.engine)

def get_db():
    db = _db.SessionLocal()
    try:
        yield db
    finally:
        db.close()

class SecurityManagerRepository:

    @staticmethod
    def get_all(db: Session):
        return db.query(SecurityManager).all()

    @staticmethod
    def find_by_id(db: Session, id: int):
        return db.query(SecurityManager).filter(SecurityManager.id == id).first()

    @staticmethod
    def save(db: Session, security_manager: SecurityManager):
        if security_manager.id_number:
            db.merge(security_manager)
        else:
            db.add(security_manager)
        db.commit()
        return security_manager

    @staticmethod
    def delete(db: Session, id: int):
        manager = SecurityManagerRepository.find_by_id(db=db, id=id)
        if manager is not None:
            db.delete(manager)
            db.commit
            return True
        return False

class PropertyOwnerRepository:

    @staticmethod
    def get_all(db: Session):
        return db.query(PropertyOwner).all()

    @staticmethod
    def find_by_id(db: Session, id: int):
        return db.query(PropertyOwner).filter(PropertyOwner.id == id).first()

    @staticmethod
    def save(db: Session, property_owner: PropertyOwner):
        if property_owner.id_number:
            db.merge(property_owner)
        else:
            db.add(property_owner)
        db.commit()
        return property_owner

    @staticmethod
    def delete(db: Session, id: int):
        owner = PropertyOwnerRepository.find_by_id(db=db, id=id)
        if owner is not None:
            db.delete(owner)
            db.commit
            return True
        return False

class BuildingRepository:

    @staticmethod
    def get_all(db: Session):
        return db.query(Building).all()

    @staticmethod
    def find_by_id(db: Session, id: int):
        return db.query(Building).filter(Building.id == id).first()

    @staticmethod
    def save(db: Session, building: Building):
        if building.id_number:
            db.merge(building)
        else:
            db.add(building)
        db.commit()
        return building

    @staticmethod
    def delete(db: Session, id: int):
        building = BuildingRepository.find_by_id(db=db, id=id)
        if building is not None:
            db.delete(building)
            db.commit
            return True
        return False


class IntrusionRepository:


    @staticmethod
    def find_by_id(db: Session, id: int):
        return db.query(Intrusion).filter(Intrusion.id == id).first()

    @staticmethod
    def save(db: Session, intrusion: Intrusion):
        if intrusion.id_number:
            db.merge(intrusion)
        else:
            db.add(intrusion)
        db.commit()
        return intrusion


    @staticmethod
    def get_all_by_building(db: Session, buildingId: int):
        lst = db.query(Intrusion).all()
        rtn_lst=[]
        
        for i in lst:
            if i.building_id == buildingId:
                rtn_lst.append(i)


        print(rtn_lst)
        return lst

    
