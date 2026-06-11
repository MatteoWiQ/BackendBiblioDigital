from sqlalchemy import Column, Float, Integer, String
from database import Base
class User(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(150), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)

    rol = Column(String(50), default="Usuario", nullable=False) 


class Book(Base):
    __tablename__ = "libros"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String(200), index=True)
    autor = Column(String(150))
    descripcion = Column(String(500))
    url_pdf = Column(String(255))

    categoria = Column(String(100))
    precio = Column(Float) 