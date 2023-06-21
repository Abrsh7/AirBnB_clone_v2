#!/usr/bin/python3
""" Amenity Module for HBNB project """
from models.base_model import BaseModel, Base
from models.place import place_amenity
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from models import storage_t


class Amenity(BaseModel, Base):
    """ Amenity class to store amenity information """
    if storage_t == "db":
        __tablename__ = 'amenities'
        name = Column(String(128), nullable=False)
        amenities = relationship(
            "Place",
            secondary=place_amenity,
            viewonly=False
        )
    else:
        name = ""
