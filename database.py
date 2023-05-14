from config import *
import sqlalchemy as sq
from sqlalchemy.orm import declarative_base
from sqlalchemy.exc import IntegrityError, InvalidRequestError


Base = declarative_base()


class SortedByViewed(Base):
    __tablename__ = 'SortedByViewed'

    id = sq.Column(sq.Integer, primary_key=True, autoincrement=True)
    vk_id = sq.Column(sq.Integer, unique=True)


def create_tables(engine):
    Base.metadata.create_all(engine)


def sorted_users_by_viewed(owner_id):
    if db.query(SortedByViewed).filter_by(vk_id=owner_id).first() is None:
        return True
    else:
        return False


def add_user(owner_id):
    try:
        if sorted_users_by_viewed(owner_id) is False:
            return False
        else:
            new_user = SortedByViewed(vk_id=owner_id)
            db.add(new_user)
            db.commit()
            return True
    except(IntegrityError, InvalidRequestError):
        pass


db.close()

# if __name__ == '__main__':
#     create_tables(engine)
