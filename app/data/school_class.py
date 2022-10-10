from sqlalchemy_sessions import SqlAlchemyBase
import sqlalchemy as sa


class SchoolClass(SqlAlchemyBase):
    __tablename__ = "school_classes"

    school_class_id = sa.Column(sa.Integer, primary_key=True, 
                                autoincrement=True, index=True)
    number = sa.Column(sa.Integer, nullable=False)
    letter = sa.Column(sa.VARCHAR(1), nullable=False)
    school_id = sa.Column(sa.Integer, sa.ForeignKey("schools.school_id"), 
                          nullable=False)
    
