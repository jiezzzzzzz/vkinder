import sqlalchemy as sq
from sqlalchemy.orm import sessionmaker
from models import User, Photo, Favorite, BlackList
from environs import Env
from sqlalchemy.orm import declarative_base


Base = declarative_base()
env = Env()
env.read_env()

db_url = env('URL')


def crete_engine_connection():
    engine = sq.create_engine(db_url)
    return engine


class Vkinder:
    def __init__(self):
        self.engine = crete_engine_connection()
        session = sessionmaker(bind=self.engine)
        self.session = session()

    def create_tables(self):
        Base.metadata.create_all(self.engine)

    def drop_tables(self):
        Base.metadata.drop_all(bind=self.engine, tables=[User.__table__, Photo.__table__])

    def add_user_data(self, user_data: list):
        for record in user_data:
            self.session.add(
                User(
                    user_id=record["id"],
                    name=record["name"],
                    surname=record["surname"],
                )
            )
        self.session.commit()

    def get_one_user(self, user_id: int):
        return self.session.query(User).filter(User.id == user_id).first()

    def search_user(self, user_id: int):
        return self.session.query(User).filter(User.user_id == user_id).first()

    def get_all_users(self):
        return self.session.query(User).all()

    def add_photo_urls(self, user_id: int, urls: list):
        for url in urls:
            self.session.add(
                Photo(
                    user_id=user_id,
                    url=url,
                )
            )
        self.session.commit()

    def get_photo_urls(self, user_id: int):
        return self.session.query(Photo).filter(Photo.user_id == user_id).all()

    def add_to_favorites(self, user_id: int):
        self.session.add(
            Favorite(
                user_id=user_id,
            )
        )
        self.session.commit()

    def check_favorites(self, user_id: int):
        if (
            self.session.query(Favorite)
            .filter(Favorite.user_id == user_id)
            .first()
            is None
        ):
            return False
        else:
            return True

    def get_all_from_favorites(self):
        return self.session.query(Favorite).all()

    def add_to_blacklist(self, user_id: int):
        self.session.add(
            BlackList(
                user_id=user_id,
            )
        )
        self.session.commit()

    def check_blacklist(self, user_id: int):
        if (
            self.session.query(BlackList)
            .filter(BlackList.user_id == user_id)
            .first()
            is None
        ):
            return False
        else:
            return True

    def delete_from_blacklist(self, user_id: int):
        current_user = self.session.query(BlackList).filter_by(user_id=user_id).first()
        self.session.delete(current_user)
        self.session.commit()

    def delete_from_favorites(self, user_id: int):
        current_user = self.session.query(Favorite).filter_by(user_id=user_id).first()
        self.session.delete(current_user)
        self.session.commit()