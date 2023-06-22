#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from models import storage_t


if storage_t == "db":
    class State(BaseModel, Base):
        """ State class """
        __tablename__ = 'states'
        name = Column(String(128), nullable=False)
        cities = relationship(
            "City",
            backref="state",
            cascade="all, delete"
        )

        def __init__(self, *args, **kwargs):
            """initializes state"""
            super().__init__(*args, **kwargs)


else:
    class State(BaseModel, object):
        """ State class """
        name = ""

        @property
        def cities(self):
            """Getter for list of city instances of the state"""
            from models import storage
            from models.city import City
            state_cities = []
            all_cities = storage.all(City)
            for city in all_cities.values():
                if city.state_id == self.id:
                    state_cities.append(city)
            return state_cities
