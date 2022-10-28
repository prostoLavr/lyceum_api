from sqlalchemy_sessions import SqlAlchemyBase
import sqlalchemy as sa


class Lesson(SqlAlchemyBase):
    __tablename__ = "lessons"  # Привет

    lesson_id = sa.Column(
            sa.Integer, primary_key=True, 
            autoincrement=True, index=True
    )
    day = sa.Column(sa.Integer, nullable=False)
    start_time = sa.Column(sa.Time, nullable=False)
    end_time = sa.Column(sa.Time, nullable=False)

    teacher_id = sa.Column(
            sa.Integer, sa.ForeignKey("teachers.teacher_id"),
           nullable=False
    )
    subject_id = sa.Column(
            sa.Integer, sa.ForeignKey("subjects.subject_id"),
                           nullable=False
    )
    
