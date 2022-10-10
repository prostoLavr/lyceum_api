from sqlalchemy_sessions import SqlAlchemyBase
import sqlalchemy as sa


class School(SqlAlchemyBase):
    __tablename__ = "schools"

    school_id = sa.Column(sa.Integer, primary_key=True, 
                         autoincrement=True, index=True)
    name = sa.Column(sa.VARCHAR(256))
    address = sa.Column(sa.VARCHAR(512))
    
