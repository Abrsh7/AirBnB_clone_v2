#!/usr/bin/python3
""" City Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship

from models import storage_t


class City(BaseModel, Base):
    """ The city class, contains state ID and name """
    if storage_t == "db":
        __tablename__ = 'cities'
        state_id = Column(String(60), ForeignKey('states.id'), nullable=False)
        name = Column(String(128), nullable=False)
        places = relationship(
            "Place",
            backref="city",
            cascade="all, delete"
        )
    else:
        state_id = ""
        name = ""

        @property
        def places(self):
            """Getter for list of place instances of the city"""
            from models import storage
            from models.place import Place
            city_places = []
            all_places = storage.all(Place)
            for place in all_places.values():
                if place.city_id == self.id:
                    city_places.append(place)
            return city_places

    def __init__(self, *args, **kwargs):
        """initializes city"""
        super().__init__(*args, **kwargs)
