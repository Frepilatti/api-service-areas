from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from geoalchemy2 import Geometry
from .database import Base

class Provider(Base):
    __tablename__ = 'providers'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)
    language = Column(String, nullable=False)
    currency = Column(String, nullable=False)

    service_areas = relationship("ServiceArea", back_populates="provider", cascade="all, delete-orphan")

class ServiceArea(Base):
    __tablename__ = 'service_areas'

    id = Column(Integer, primary_key=True, index=True)
    provider_id = Column(Integer, ForeignKey('providers.id', ondelete='CASCADE'), nullable=False)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    geojson = Column(Geometry('POLYGON', srid=4326), nullable=False)

    provider = relationship("Provider", back_populates="service_areas")
