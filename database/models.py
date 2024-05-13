from sqlalchemy import Column, String, TIMESTAMP, Text, ForeignKey
from sqlalchemy.orm import relationship
from base import Base

class User(Base):
    __tablename__ = 'User'

    Id = Column(String(10), primary_key=True)
    Name = Column(String(20), nullable=False)
    Password = Column(String(30), nullable=False)
    Registration_date = Column(TIMESTAMP)
    Last_login_time = Column(TIMESTAMP)

    # Relationship to Record
    records = relationship("Record", back_populates="user")

class Dialogue(Base):
    __tablename__ = 'Dialogue'

    D_id = Column(String(10), primary_key=True)
    Type = Column(String(20), nullable=False)
    Content = Column(Text)

    # Relationship to Record
    records = relationship("Record", back_populates="dialogue")

class Record(Base):
    __tablename__ = 'Record'

    Id = Column(String(10), ForeignKey('User.Id'), primary_key=True)
    D_id = Column(String(10), ForeignKey('Dialogue.D_id'), primary_key=True)
    R_time = Column(TIMESTAMP)

    # Relationships
    user = relationship("User", back_populates="records")
    dialogue = relationship("Dialogue", back_populates="records")
