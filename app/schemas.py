from pydantic import BaseModel, EmailStr, Field, validator
from typing import List
from geoalchemy2.elements import WKBElement
from geoalchemy2.shape import to_shape
import json

class ServiceAreaBase(BaseModel):
    name: str
    price: float
    geojson: str

class ServiceAreaCreate(ServiceAreaBase):
    pass

class ServiceArea(ServiceAreaBase):
    id: int
    provider_id: int

    @validator('geojson', pre=True)
    def geojson_to_string(cls, v):
        if isinstance(v, WKBElement):
            shape = to_shape(v)
            geojson_dict = shape.__geo_interface__
            return json.dumps(geojson_dict)
        return v

    class Config:
        orm_mode = True

class ProviderBase(BaseModel):
    name: str
    email: EmailStr
    phone_number: str
    language: str
    currency: str

class ProviderCreate(ProviderBase):
    pass

class Provider(ProviderBase):
    id: int
    service_areas: List[ServiceArea] = []

    class Config:
        orm_mode = True
