from app.models import Intrusion
import app.schemas as _schemas
import app.services as _services
import app.database as _db
import fastapi as _fastapi


from time import time
from urllib import response
from fastapi import HTTPException
from starlette.responses import Response
from app.redis import init_redis_pool
from typing import TYPE_CHECKING, List
from sqlalchemy.orm import Session


app = _fastapi.FastAPI()



@app.on_event("startup")
async def startup_event():
    app.state.redis = await init_redis_pool()
    # criar repositório bd


@app.post("/intrusion/{building_id}", response_model=_schemas.IntrusionResponse)
def create_intrusion(
                    building_id: int, # id do edificio
                    intrusion: _schemas.IntrusionBase.building_id, 
                    db: Session = _fastapi.Depends(_services.get_db), 
                    time:int = time() #timestamp
                    ):

    
    intrusion = _services.IntrusionRepository.save(db=db, intrusion=intrusion)
    return intrusion

@app.get("/intrusion/{buildingId}", response_model=List[_schemas.IntrusionResponse])
def get_intrusion(buildingId: int, db: Session = _fastapi.Depends(_services.get_db)):
    """Get all intrusions from a building"""
    return _services.IntrusionRepository.get_all_by_building(db=db, buildingId=buildingId)


@app.get("/buildings", response_model=List[_schemas.BuildingResponse])
def get_buildings(db: Session = _fastapi.Depends(_services.get_db)):
    """Get all buildings"""
    return _services.BuildingRepository.get_all(db=db) 


""" @app.post("/api/intrusion", response_model=_schemas._BaseIntrusion)
async def create_intrusion(
    intrusion: _schemas._BaseIntrusion, 
    db: _orm.Session = _fastapi.Depends(_services.get_db)
):
    return await _services.create_intrusion(intrusion=intrusion, db=db)




@app.get("/api/intrusions/", response_model=List[_schemas._BaseIntrusion])
async def get_intrusions(db: _orm.Session = _fastapi.Depends(_services.get_db)):
    return await _services.get_all_intrusions(db=db)





@app.get("/api/intrusions/{intrusion_id}", response_model=_schemas._BaseIntrusion)
async def get_intrusion(
    intrusion_id: int, 
    db: _orm.Session = _fastapi.Depends(_services.get_db)
):
    return await _services.get_intrusion(intrusion_id=intrusion_id, db=db)




@app.delete("/api/intrusions/{intrusion_id}")
async def delete_intrusion(
    intrusion_id: int, 
    db: _orm.Session = _fastapi.Depends(_services.get_db)
):
    intrusion = await _services.get_intrusion(intrusion_id=intrusion_id, db=db)
    if intrusion is None:
        return _fastapi.HTTPException(status_code=404, detail="Intrusion not found")
    await _services.delete_intrusion(intrusion=intrusion, db=db)
    return "Intrusion deleted!"





@app.put("/api/intrusions/{intrusion_id}")
async def update_intrusion(
    intrusion_id: int,
    intrusion: _schemas._BaseIntrusion,
    db: _orm.Session = _fastapi.Depends(_services.get_db),
):
    intrusion_data = await _services.get_intrusion(intrusion_id=intrusion_id, db=db) #model
    if intrusion_data is None:
        return _fastapi.HTTPException(status_code=404, detail="Intrusion not found")
  
    return await _services.update_intrusion(intrusion_id=intrusion, intrusion=intrusion_data ,db=db)
 





@app.get("/hello")
def hello():
    return {"message": "Hello world. O projeto está feito meus caros"}


@app.get("/intrusion")
def getIntrusionData():
    return {"message": "get all data from cameras"}

@app.post("/newIntrusion")
def getIntrusionData(timestamp: str, num_humans: int):
    return {"message": f"New intrusion detected at {timestamp} with {num_humans} humans"}


@app.put("/videoClips")
def storeVideoClips():
    return {"message": "send video clips to AWS S3"}
"""
