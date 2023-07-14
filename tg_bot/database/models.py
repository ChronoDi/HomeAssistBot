from sqlalchemy import ForeignKey, Column, Integer, String
from sqlalchemy.orm import relationship, Mapped, mapped_column

from tg_bot.database.base import Base

class Entities(Base):
    __tablename__ = 'entities'

    id = Column(Integer, unique=True, autoincrement=True, primary_key=True)
    name = Column(String, unique=True)
    friendly_name = Column(String)
    group_id = Column(String, ForeignKey('groups.id'))
    room_id = Column(Integer, ForeignKey('rooms.id'))
    groups = relationship('Groups', back_populates='entities')
    rooms = relationship('Rooms', back_populates='entities')


class Groups(Base):
    __tablename__ = 'groups'

    id = Column(String, primary_key=True, unique=True)
    friendly_name = Column(String(20))
    entities = relationship('Entities', back_populates='groups')

class Rooms(Base):
    __tablename__ = 'rooms'

    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    name = Column(String(20))
    friendly_name = Column(String(20))
    entities = relationship('Entities', back_populates='rooms')

