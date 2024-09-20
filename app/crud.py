from sqlalchemy.orm import Session
from . import models, schemas
from geoalchemy2.shape import from_shape
from shapely.geometry import shape
import json

def get_provider(db: Session, provider_id: int):
    return db.query(models.Provider).filter(models.Provider.id == provider_id).first()

def get_providers(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Provider).offset(skip).limit(limit).all()

def create_provider(db: Session, provider: schemas.ProviderCreate):
    db_provider = models.Provider(**provider.dict())
    db.add(db_provider)
    db.commit()
    db.refresh(db_provider)
    return db_provider

def update_provider(db: Session, provider_id: int, provider: schemas.ProviderCreate):
    db_provider = get_provider(db, provider_id)
    if db_provider is None:
        return None
    for key, value in provider.dict().items():
        setattr(db_provider, key, value)
    db.commit()
    db.refresh(db_provider)
    return db_provider

def delete_provider(db: Session, provider_id: int):
    db_provider = get_provider(db, provider_id)
    if db_provider is None:
        return None
    db.delete(db_provider)
    db.commit()
    return db_provider

def get_service_area(db: Session, service_area_id: int):
    return db.query(models.ServiceArea).filter(models.ServiceArea.id == service_area_id).first()

def get_service_areas(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.ServiceArea).offset(skip).limit(limit).all()

def create_service_area(db: Session, service_area: schemas.ServiceAreaCreate, provider_id: int):
    try:
        geo_shape = shape(json.loads(service_area.geojson))
    except (ValueError, TypeError, json.JSONDecodeError):
        raise ValueError("Invalid GeoJSON format")
    db_service_area = models.ServiceArea(
        name=service_area.name,
        price=service_area.price,
        provider_id=provider_id,
        geojson=from_shape(geo_shape, srid=4326)
    )
    db.add(db_service_area)
    db.commit()
    db.refresh(db_service_area)
    return db_service_area

def update_service_area(db: Session, service_area_id: int, service_area: schemas.ServiceAreaCreate):
    db_service_area = get_service_area(db, service_area_id)
    if db_service_area is None:
        return None
    for key, value in service_area.dict().items():
        if key == 'geojson':
            try:
                geo_shape = shape(json.loads(value))
                setattr(db_service_area, 'geojson', from_shape(geo_shape, srid=4326))
            except (ValueError, TypeError, json.JSONDecodeError):
                raise ValueError("Invalid GeoJSON format")
        else:
            setattr(db_service_area, key, value)
    db.commit()
    db.refresh(db_service_area)
    return db_service_area

def delete_service_area(db: Session, service_area_id: int):
    db_service_area = get_service_area(db, service_area_id)
    if db_service_area is None:
        return None
    db.delete(db_service_area)
    db.commit()
    return db_service_area
