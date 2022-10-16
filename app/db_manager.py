from data.lesson import Lesson
from data.school_class import SchoolClass
from data.school import School
from data.subject import Subject
from data.teacher import Teacher


from sqlalchemy_sessions import search_func, add_func, edit_func, remove_func
from sqlalchemy.orm import Session

from datetime import time
import calendar
from typing import Optional


@add_func
def create(db_sess: Session, cls, **kwargs):
    return cls(**kwargs)


@edit_func
def create_if_nonexist(db_sess: Session, cls, **kwargs):
    query = db_sess.query(cls).filter_by(**kwargs)
    if (db_object := query.one_or_none()) is not None:
        return db_object
    return create(db_sess, cls, **kwargs)


@edit_func
def create_default(db_sess: Session):
    school = create_if_nonexist(
            db_sess, School, name="Лицей №2", address="Иркутск"
    )
    teacher = create_if_nonexist(
            db_sess, Teacher, name="Мария Александровна"
    )
    school_class = create_if_nonexist(
            db_sess, SchoolClass, number=10, letter='Б', 
            school_id=school.school_id
    )
    subject = create_if_nonexist(
            db_sess, Subject, name="Математика",
            school_class_id=school_class.school_class_id,
            teacher_id=teacher.teacher_id
    )
    lesson = create_if_nonexist(
            db_sess, Lesson, subject_id=subject.subject_id, 
            teacher_id=teacher.teacher_id, start_time=time(8, 0), 
            end_time=time(8, 30), day=0
    )

def add_row_to_lessons(row, lessons):
    row = list(row)
    for lesson in lessons:
        lesson_info = [lesson['subject'], 
                       lesson['required'], 
                       lesson['teacher']]
        if lesson_info == row[:3]:
            add_lesson_info_to_times(row[3:], lesson['times'])
            break
    else:
        lesson_dict = {'name': row[0], 
                       'required': row[1], 
                       'teacher': row[2], 
                       'times': {}}
        add_lesson_info_to_times(row[3:], lesson_dict['times'])
        lessons.append(lesson_dict)

def add_lesson_info_to_times(lesson_info, times):
    school_class = f'{lesson_info[0]}{lesson_info[1]}'
    if school_class not in times.keys():
        time_for_class = times[school_class] = {}
    day_name = calendar.day_name[lesson_info[2]]
    if day_name not in time_for_class:
        time_for_class[day_name] = []
    start_end_time = [lesson_info[3].hour,
                      lesson_info[3].minute,
                      lesson_info[4].hour,
                      lesson_info[4].minute]
    if start_end_time not in time_for_class[day_name]:
        time_for_class[day_name].append(start_end_time)
            

def format_lessons_by_school_class_id(query_result: list[tuple]) -> dict:
    output = {'lessons': []}
    lessons = output['lessons']
    for row in query_result:
        add_row_to_lessons(row, lessons)
    return output 


@search_func
def get_lessons_by_school_class_id(
        db_sess: Session, 
        school_class_id: Optional[int], 
        required=False):

    query = db_sess.query(
            Subject.name,
            Subject.required,
            Teacher.name,
            SchoolClass.number,
            SchoolClass.letter,
            Lesson.day,
            Lesson.start_time, 
            Lesson.end_time,
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

    return format_lessons_by_school_class_id(query.all())

