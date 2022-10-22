import app.schemas as _schemas
import sqlalchemy.orm as _orm
import app.services as _services
import fastapi as _fastapi


from time import time
from urllib import response
from fastapi import HTTPException
from starlette.responses import Response
from app.redis import init_redis_pool
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from sqlalchemy.orm import Session


app = _fastapi.FastAPI()
# incluir router mais tarde3



@app.on_event("startup")
async def startup_event():
    app.state.redis = await init_redis_pool()
    # criar repositório bd



@app.post("/api/intrusion", response_model=_schemas._BaseIntrusion)
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
