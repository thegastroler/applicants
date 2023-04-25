from datetime import datetime

from infrastructure.sql.db import Base
from sqlalchemy import (TIMESTAMP, VARCHAR, Boolean, Column, Integer,
                        SmallInteger, BigInteger, UniqueConstraint)


class Applicants(Base):
    __tablename__ = "applicants"
    id = Column(Integer, primary_key=True, autoincrement=True)
    snils = Column(VARCHAR(50), nullable=False)
    code = Column(VARCHAR(255), nullable=True)
    university = Column(VARCHAR(255), nullable=False)
    score = Column(SmallInteger, nullable=True)
    origin = Column(Boolean, nullable=False)
    position = Column(SmallInteger, nullable=True)

    created_at = Column(TIMESTAMP, default=datetime.now(), nullable=False)
    updated_at = Column(TIMESTAMP, onupdate=datetime.now(), nullable=True)

    __table_args__ = (UniqueConstraint("snils", "code", "university", name="snils_code_university"),)

    class Config:
        orm_mode = True