#!/usr/bin/python3
"""This module defines a class to manage DB storage for hbnb clone"""
from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from models.base_model import Base
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


class DBStorage:
    """This class manages storage of hbnb models in a MySQL database"""
    __engine = None
    __session = None    # Pool of sessions

    def __init__(self):
        """Instantiates the Database storage"""
        HBNB_MYSQL_USER = getenv('HBNB_MYSQL_USER')
        HBNB_MYSQL_PWD = getenv('HBNB_MYSQL_PWD')
        HBNB_MYSQL_HOST = getenv('HBNB_MYSQL_HOST')
        HBNB_MYSQL_DB = getenv('HBNB_MYSQL_DB')
        HBNB_ENV = getenv('HBNB_ENV')
        self.__engine = create_engine(
            'mysql+mysqldb://{}:{}@{}/{}'.format(
                HBNB_MYSQL_USER, HBNB_MYSQL_PWD,
                HBNB_MYSQL_HOST, HBNB_MYSQL_DB
            ),
            pool_pre_ping=True
        )
        if HBNB_ENV == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """
        Returns a dictionary of models of given class or
         all classes currently in storage
        """
        classes = [User, State, City, Amenity, Place, Review]

        if cls is not None:
            classes = [cls]
        my_dict = {}
        for mdl_class in classes:
            objs = self.__session.query(mdl_class).all()
            for obj in objs:
                key = obj.__class__.__name__ + '.' + obj.id
                my_dict.update({key: obj})
        self.__session.commit()
        return my_dict

    def new(self, obj):
        """Adds new object to database session"""
        self.__session.add(obj)

    def delete(self, obj=None):
        """Deletes an object from database"""
        if obj is None:
            return
        obj_sess = self.__session.object_session(obj)
        if obj_sess:
            obj_sess.delete(obj)
        self.save()

    def save(self):
        """Saves session data to the database"""
        self.__session.commit()

    def reload(self):
        """Loads session data from the database"""
        Base.metadata.create_all(self.__engine)
        sess_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        self.__session = scoped_session(sess_factory)
