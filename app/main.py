from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from geoalchemy2.functions import ST_Contains
from . import crud, models, schemas
from .database import engine, get_db
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import func

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Service Area API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/providers/", response_model=schemas.Provider)
def create_provider(provider: schemas.ProviderCreate, db: Session = Depends(get_db)):
    return crud.create_provider(db=db, provider=provider)

@app.get("/providers/", response_model=List[schemas.Provider])
def read_providers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    providers = crud.get_providers(db, skip=skip, limit=limit)
    return providers

@app.get("/providers/{provider_id}", response_model=schemas.Provider)
def read_provider(provider_id: int, db: Session = Depends(get_db)):
    db_provider = crud.get_provider(db, provider_id=provider_id)
    if db_provider is None:
        raise HTTPException(status_code=404, detail="Provider not found")
    return db_provider

@app.put("/providers/{provider_id}", response_model=schemas.Provider)
def update_provider(provider_id: int, provider: schemas.ProviderCreate, db: Session = Depends(get_db)):
    db_provider = crud.update_provider(db, provider_id=provider_id, provider=provider)
    if db_provider is None:
        raise HTTPException(status_code=404, detail="Provider not found")
    return db_provider

@app.delete("/providers/{provider_id}", response_model=schemas.Provider)
def delete_provider(provider_id: int, db: Session = Depends(get_db)):
    db_provider = crud.delete_provider(db, provider_id=provider_id)
    if db_provider is None:
        raise HTTPException(status_code=404, detail="Provider not found")
    return db_provider

@app.post("/providers/{provider_id}/service_areas/", response_model=schemas.ServiceArea)
def create_service_area_for_provider(
    provider_id: int, service_area: schemas.ServiceAreaCreate, db: Session = Depends(get_db)
):
    try:
        return crud.create_service_area(db=db, service_area=service_area, provider_id=provider_id)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))

@app.get("/service_areas/", response_model=List[schemas.ServiceArea])
def read_service_areas(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    service_areas = crud.get_service_areas(db, skip=skip, limit=limit)
    return service_areas

@app.get("/service_areas/{service_area_id}", response_model=schemas.ServiceArea)
def read_service_area(service_area_id: int, db: Session = Depends(get_db)):
    db_service_area = crud.get_service_area(db, service_area_id=service_area_id)
    if db_service_area is None:
        raise HTTPException(status_code=404, detail="Service Area not found")
    return db_service_area

@app.put("/service_areas/{service_area_id}", response_model=schemas.ServiceArea)
def update_service_area(service_area_id: int, service_area: schemas.ServiceAreaCreate, db: Session = Depends(get_db)):
    try:
        db_service_area = crud.update_service_area(db, service_area_id=service_area_id, service_area=service_area)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    if db_service_area is None:
        raise HTTPException(status_code=404, detail="Service Area not found")
    return db_service_area

@app.delete("/service_areas/{service_area_id}", response_model=schemas.ServiceArea)
def delete_service_area(service_area_id: int, db: Session = Depends(get_db)):
    db_service_area = crud.delete_service_area(db, service_area_id=service_area_id)
    if db_service_area is None:
        raise HTTPException(status_code=404, detail="Service Area not found")
    return db_service_area

@app.get("/search/")
@app.get("/search/")
def search_service_areas(lat: float, lng: float, db: Session = Depends(get_db)):
    point_wkt = f'POINT({lng} {lat})'
    point_geom = func.ST_SetSRID(func.ST_GeomFromText(point_wkt), 4326)
    
    query = db.query(models.ServiceArea, models.Provider).join(models.Provider).filter(
        ST_Contains(models.ServiceArea.geojson, point_geom)
    )
    results = []
    for service_area, provider in query.all():
        results.append({
            'service_area_name': service_area.name,
            'provider_name': provider.name,
            'price': service_area.price
        })
    return results
