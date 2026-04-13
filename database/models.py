from sqlalchemy import Column, Integer, String
from geoalchemy2 import Geometry
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey
from geoalchemy2 import Geometry
from db import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True)
    password = Column(String)
    plan = Column(String)

class Farm(Base):
    __tablename__ = "farms"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))
    geom = Column(Geometry("POLYGON", srid=4326))   

Base = declarative_base()

class Farm(Base):
    __tablename__ = "farms"

    id = Column(Integer, primary_key=True)
    name = Column(String)

    # 🌍 PostGIS geometry
    geom = Column(Geometry("POLYGON", srid=4326))
    from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from geoalchemy2 import Geometry

Base = declarative_base()

class Farm(Base):
    __tablename__ = "farms"

    id = Column(Integer, primary_key=True)
    name = Column(String)

    # 🌍 GEOMETRIA REAL
    geom = Column(Geometry("POLYGON", srid=4326))
    from sqlalchemy import Column, Integer, Float, String
from db import Base

class NDVIHistory(Base):
    __tablename__ = "ndvi_history"

    id = Column(Integer, primary_key=True)
    farm_id = Column(Integer)
    season = Column(String)
    mean_ndvi = Column(Float)