from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    vk_id = Column(Integer, unique=True, nullable=False)
    name = Column(String, max_lenght=150, nullable=True)
    surname = Column(String, max_lenght=150, nullable=True)


class Photo(Base):
    __tablename__ = 'photos'
    id = Column(Integer, primaty_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.vk_id'), nullable=False) # не уверена на что отсылаться
    url = Column(String(1000), unique=True, nullable=False)
    likes_count = Column(Integer)


class Favorite(Base):
    __teblename__ = 'favorites'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=False, unique=True)


class BlackList(Base):
    __tablename__ = 'blacklist'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, unique=True, nullable=False)


def create_all_tables(engine):
    Base.metadata.create_all(engine)


def drop_all_tables(engine):
    Base.metadata.drop_all(bind=engine, tables=[User.__table__, Photo.__table__])


