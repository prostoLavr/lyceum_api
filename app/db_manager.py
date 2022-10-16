from data.lesson import Lesson
from data.school_class import SchoolClass
from data.school import School
from data.subject import Subject
from data.teacher import Teacher


from sqlalchemy_sessions import search_func, add_func, edit_func, remove_func
from sqlalchemy.orm import Session

from datetime import time
from typing import Optional


@add_func
def create(db_sess: Session, cls, *args, **kwargs):
    return cls(*args, **kwargs)


@edit_func
def create_if_nonexist(db_sess: Session, cls, **kwargs):
    query = db_sess.query(cls).filter_by(**kwargs)
    return query.one_or_none() or cls(**kwargs)


@edit_func
def create_default(db_sess: Session):
    school = create_if_nonexist(
            db_sess, School, name="Lyceum 2", address="Irkutsk"
    )
    teacher = create_if_nonexist(
            db_sess, Teacher, name="Lawrence Naumov"
    )
    school_class = create_if_nonexist(
            db_sess, SchoolClass, number=10, letter='B', 
            school_id=school.school_id
    )
    subject = create_if_nonexist(
            db_sess, Subject, name="Math", 
            school_class_id=school_class.school_class_id
    )
    lesson = create_if_nonexist(
            db_sess, Lesson, subject_id=subject.subject_id, 
            teacher_id=teacher.teacher_id, start_time=time(8, 0), 
            end_time=time(8, 30), day=0
    )


@search_func
def get_lessons_by_school_class_id(
        db_sess: Session, 
        school_class_id: Optional[int], 
        required=False):

    query = db_sess.query(
            Subject.name,
            School.name,
            SchoolClass.number,
            SchoolClass.letter,
            Lesson.day,
            Lesson.start_time, 
            Lesson.end_time,
            Teacher.name
    )
    
    query = query.select_from(Lesson)

    query = query.join(
            Subject, 
            Lesson.subject_id == Subject.subject_id
    )
    query = query.filter(
            Subject.school_class_id == school_class_id
    )

    query = query.join(
            SchoolClass, 
            Subject.school_class_id == SchoolClass.school_class_id
    )
    query = query.join(
            Teacher,
            Subject.teacher_id == Teacher.teacher_id
    )

    return query.all()

