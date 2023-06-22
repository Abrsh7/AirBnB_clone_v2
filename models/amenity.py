#!/usr/bin/python3
""" Amenity Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String

from models import storage_t


if storage_t == "db":
    class Amenity(BaseModel, Base):
        """ Amenity class to store amenity information """
        __tablename__ = 'amenities'
        name = Column(String(128), nullable=False)

        def __init__(self, *args, **kwargs):
            """initializes amenity"""
            super().__init__(*args, **kwargs)


else:
    class Amenity(BaseModel, Base):
        """ Amenity class to store amenity information """
        name = ""
