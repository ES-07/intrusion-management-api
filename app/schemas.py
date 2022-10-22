import datetime as _dt
import pydantic as _pydantic


class _BaseUser(_pydantic.BaseModel):
    name: str
    email: str

class _BaseProperty(_pydantic.BaseModel):
    name: str
    location: str

class _BaseCamera(_pydantic.BaseModel):
    name: str
    location: str

class _BaseIntrusion(_pydantic.BaseModel):
    timestamp: _dt.datetime

    class Config:
        orm_mode = True