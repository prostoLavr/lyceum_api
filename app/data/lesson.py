from sqlalchemy_sessions import SqlAlchemyBase
import sqlalchemy as sa


class Lesson(SqlAlchemyBase):
    __tablename__ = "lessons"

    lesson_id = sa.Column(sa.Integer, primary_key=True, 
                          autoincrement=True, index=True)
    day_id = sa.Column(sa.Integer, sa.ForeignKey("days.day_id"), nullable=False)
    start_time = sa.Column(sa.Time)
    end_time = sa.Column(sa.Time)
    teacher_id = sa.Column(sa.Integer, sa.ForeignKey("teachers.teacher_id"))
    subject_id = sa.Column(sa.Integer, sa.ForeignKey("subjects.subject_id"), 
                          nullable=False)
    
