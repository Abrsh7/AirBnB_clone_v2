#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Table, Column, String, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship

from models import storage_t

place_amenity = Table('place_amenity', Base.metadata,
    Column(
        'place_id', String(60),
        ForeignKey('places.id'), primary_key=True, nullable=False
    ),
    Column(
        'amenity_id', String(60),
        ForeignKey('amenities.id'), primary_key=True, nullable=False
    )
)


if storage_t == "db":
    class Place(BaseModel, Base):
        """ A place to stay """
        __tablename__ = 'places'
        city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
        user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
        name = Column(String(128), nullable=False)
        description = Column(String(1024), nullable=True)
        number_rooms = Column(Integer, nullable=False, default=0)
        number_bathrooms = Column(Integer, nullable=False, default=0)
        max_guest = Column(Integer, nullable=False, default=0)
        price_by_night = Column(Integer, nullable=False, default=0)
        latitude = Column(Float, nullable=True)
        longitude = Column(Float, nullable=True)
        reviews = relationship(
            "Review",
            backref="place",
            cascade="all, delete"
        )
        amenities = relationship(
            "Amenity",
            secondary=place_amenity,
            backref="place_amenities",
            viewonly=False
        )

        def __init__(self, *args, **kwargs):
            """initializes place"""
            super().__init__(*args, **kwargs)


else:
    class Place(BaseModel):
        """ A place to stay """
        city_id = ""
        user_id = ""
        name = ""
        description = ""
        number_rooms = 0
        number_bathrooms = 0
        max_guest = 0
        price_by_night = 0
        latitude = 0.0
        longitude = 0.0
        amenity_ids = []

        @property
        def reviews(self):
            """Getter for list of review instances of the place"""
            from models import storage
            from models.review import Review
            place_reviews = []
            all_reviews = storage.all(Review)
            for review in all_reviews.values():
                if review.place_id == self.id:
                    place_reviews.append(review)
            return place_reviews

        @property
        def amenities(self):
            """Getter for list of amenity instances of the place"""
            from models import storage
            place_amenities = []
            for amenity_id in self.amenity_ids:
                amenity_key = "Amenity." + amenity_id
                place_amenities.append(storage.all()[amenity_key])
            return place_amenities
        
        @amenities.setter
        def append(self, amenity):
            from models.amenity import Amenity
            if not isinstance(amenity, Amenity):
                return
            self.amenity_ids.append(amenity.id)
