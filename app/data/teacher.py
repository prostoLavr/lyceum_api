from sqlalchemy_sessions import SqlAlchemyBase
import sqlalchemy as sa


class Teacher(SqlAlchemyBase):
    __tablename__ = "teachers"

    teacher_id = sa.Column(sa.Integer, primary_key=True, 
                           autoincrement=True, index=True)
    name = sa.Column(sa.VARCHAR(128))
    school_id = sa.Column(sa.Integer, sa.ForeignKey("schools.school_id"), 
                          nullable=False)
    
