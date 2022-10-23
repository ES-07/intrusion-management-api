from datetime import datetime, date
from pydantic import BaseModel
from sqlalchemy import Date
from app.enums import Notification_type, DeviceState




class PersonBase(BaseModel):
    email: str
    password: str
    id: int
    name: str
    address: str
    cellphone : int
    birthday: date 

class PersonRequest(PersonBase):
    pass

class PersonResponse(PersonBase):
    id_number: int
    class Config:
        orm_mode = True




## PROPERTY OWNER
class PropertyOwnerBase(PersonBase):
    contract_date: date 
    notification_type :Notification_type 

  
class PropertyOwnerRequest(PropertyOwnerBase):
    pass  

class PropertyOwnerResponse(PropertyOwnerBase):
    property_owner_id: int
    class Config:
        use_enum_values = True
        orm_mode = True



## SECURITY MANAGER

class SecurityManagerBase(BaseModel):
    pass

class SecurityManagerRequest(SecurityManagerBase):
    pass

class SecurityManagerResponse(SecurityManagerBase):
    id_number: int
    class Config:
        orm_mode = True
   

## BUILDINGS

class BuildingBase(BaseModel): 
    address:str
    name: str
    client : int 
    #devices: List[Device]
    #nao sei como meter aqui a pessoa

class BuildingRequest(BuildingBase):
    pass

class BuildingResponse(BuildingBase):
    building_id: int
    class Config:
        orm_mode = True 

class IntrusionBase(BaseModel):
    intrusion_time: datetime
    building_id: int

class IntrusionRequest(IntrusionBase):
    pass

class IntrusionResponse(IntrusionBase):
    intrusion_id: int
    class Config:
        orm_mode = True
