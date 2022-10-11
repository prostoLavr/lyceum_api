from data.lesson import Lesson
from data.school_class import SchoolClass
from data.school import School
from data.subject import Subject
from data.teacher import Teacher


from sqlalchemy_sessions import search_func, add_func, edit_func, search_func, remove_func
from sqlalchemy.orm import Session

from datetime import time
from typing import Optional


@add_func
def create(db_sess: Session, cls, *args, **kwargs):
    return cls(*args, **kwargs)


@edit_func
def create_default(db_sess: Session):
    school = create(
            db_sess, School, name="Lyceum 2", address="Irkutsk"
    )
    teacher = create(
            db_sess, Teacher, name="Lawrence Naumov", 
            school_id=school.school_id
    )
    school_class = create(
            db_sess, SchoolClass, number=10, letter='B', 
            school_id=school.school_id
    )
    subject = create(
            db_sess, Subject, name="Math", 
            school_class_id=school_class.school_class_id
    )
    lesson = create(
            db_sess, Lesson, subject_id=subject.subject_id, 
            teacher_id=teacher.teacher_id, start_time=time(8, 0), 
            end_time=time(8, 30), day=0
    )


@search_func
def api_lessons(school_class: Optional[str], required=False):
    pass

