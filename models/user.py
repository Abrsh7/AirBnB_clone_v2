#!/usr/bin/python3
"""This module defines a class User"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from models import storage_t


if storage_t == "db":
    class User(BaseModel, Base):
        """This class defines a user by various attributes"""
        __tablename__ = 'users'
        email = Column(String(128), nullable=False)
        password = Column(String(128), nullable=False)
        first_name = Column(String(128), nullable=True)
        last_name = Column(String(128), nullable=True)
        places = relationship(
            "Place",
            backref="user",
            cascade="all, delete"
        )
        reviews = relationship(
            "Review",
            backref="user",
            cascade="all, delete"
        )

        def __init__(self, *args, **kwargs):
            """initializes user"""
            super().__init__(*args, **kwargs)


else:
    class User(BaseModel):
        """This class defines a user by various attributes"""
        email = ''
        password = ''
        first_name = ''
        last_name = ''

        @property
        def places(self):
            """Getter for list of place instances of the user"""
            from models import storage
            from models.place import Place
            user_places = []
            all_places = storage.all(Place)
            for place in all_places.values():
                if place.user_id == self.id:
                    user_places.append(place)
            return user_places

        @property
        def reviews(self):
            """Getter for list of review instances of the user"""
            from models import storage
            from models.review import Review
            user_reviews = []
            all_reviews = storage.all(Review)
            for review in all_reviews.values():
                if review.user_id == self.id:
                    user_reviews.append(review)
            return user_reviews
