from sqlalchemy import Column, Integer, String
from database import Base

# データベース上の tickets テーブルを定義するクラス
class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    stock = Column(Integer, default=0, nullable=False)
