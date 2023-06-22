#!/usr/bin/python3
""" Review module for the HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey

from models import storage_t


if storage_t == "db":
    class Review(BaseModel, Base):
        """ Review class to store review information """
        __tablename__ = 'reviews'
        place_id = Column(String(60), ForeignKey('places.id'), nullable=False)
        user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
        text = Column(String(1024), nullable=False)

        def __init__(self, *args, **kwargs):
            """initializes review"""
            super().__init__(*args, **kwargs)


else:
    class Review(BaseModel, Base):
        """ Review class to store review information """
        place_id = ""
        user_id = ""
        text = ""
