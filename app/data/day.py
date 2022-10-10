from sqlalchemy_sessions import SqlAlchemyBase
import sqlalchemy as sa


class Day(SqlAlchemyBase):
    __tablename__ = "days"

    day_id = sa.Column(sa.Integer, primary_key=True, 
                       autoincrement=True, index=True)
    name = sa.Column(sa.VARCHAR(16), nullable=False)
    
