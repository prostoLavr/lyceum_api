from sqlalchemy_sessions import SqlAlchemyBase
import sqlalchemy as sa


class Subject(SqlAlchemyBase):
    __tablename__ = "subjects"

    subject_id = sa.Column(sa.Integer, primary_key=True, 
                           autoincrement=True, index=True)
    name = sa.Column(sa.VARCHAR(64), nullable=False)
    school_class_id = sa.Column(sa.Integer, sa.ForeignKey("school_classes.school_class_id"), 
                                nullable=False)
    requried = sa.Column(sa.Boolean, default=True)
    teacher_id = sa.Column(sa.Integer, sa.ForeignKey('teachers.teacher_id'))
    
