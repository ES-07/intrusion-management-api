from typing import TYPE_CHECKING
from fastapi import HTTPException

from pyparsing import List

import app.database as _db
import app.models as _models
import app.schemas as _schemas

if TYPE_CHECKING:
    from sqlalchemy.orm import Session


def _add_tables():
    return _db.Base.metadata.create_all(bind=_db.engine)

def get_db():
    db = _db.SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def create_intrusion(
    intrusion: _schemas._BaseIntrusion, 
    db: "Session"
)-> _schemas._BaseIntrusion:
    intrusion = _models.Intrusion(**intrusion.dict())
    db.add(intrusion)
    db.commit()
    db.refresh(intrusion)
    return _schemas._BaseIntrusion.from_orm(intrusion)



async def get_all_intrusions(
    db: "Session"
)-> List[_schemas._BaseIntrusion]:
    intrusions = db.query(_models.Intrusion).all()
    return list(map(_schemas._BaseIntrusion.from_orm, intrusions))




async def get_intrusion(
    intrusion_id: int, 
    db: "Session"
)-> _models.Intrusion:
    intrusion = db.query(_models.Intrusion).filter(_models.Intrusion.id == intrusion_id).first()
    if intrusion is None:
        raise HTTPException(status_code=404, detail="Intrusion not found")
    return intrusion


async def delete_intrusion(
    intrusion: _models.Intrusion, 
    db: "Session"
):
    db.delete(intrusion)
    db.commit()


async def update_intrusion(
    intrusion_id: _schemas._BaseIntrusion,
    intrusion: _models.Intrusion,
    db: "Session",
)-> _schemas._BaseIntrusion:
    

    intrusion.timestamp = intrusion_id.timestamp 
    db.commit()
    db.refresh(intrusion)

    return _schemas._BaseIntrusion.from_orm(intrusion)