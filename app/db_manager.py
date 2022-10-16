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
            db_sess, School, school_id=1, name="Лицей №2", address="Иркутск"
    )
    teacher = create_if_nonexist(
            db_sess, Teacher, teacher_id=1, name="Мария Александровна Зубакова"
    )
    school_class = create_if_nonexist(
            db_sess, SchoolClass, school_class_id=1, number=10, letter='Б', 
            school_id=school.school_id
    )
    subject = create_if_nonexist(
            db_sess, Subject, name="Математика", subject_id=1,
            school_class_id=school_class.school_class_id,
            teacher_id=teacher.teacher_id
    )
    lesson = create_if_nonexist(
            db_sess, Lesson, subject_id=subject.subject_id, lesson_id=1,
            teacher_id=teacher.teacher_id, start_time=time(8, 0), 
            end_time=time(8, 30), day=0
    )

def add_row_to_lessons(row, lessons):
    row = list(row)
    lesson_id, *row = row
    print(f'{row=}')
    for lesson in lessons:
        if lesson['id'] == lesson_id:
            add_lesson_info_to_times(row[3:], lesson['times'])
            break
    else:
        lesson_dict = {'id': lesson_id,
                       'name': row[0], 
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
            

def format_lessons(query_result: list[tuple]) -> dict:
    output = {'lessons': []}
    lessons = output['lessons']
    for row in query_result:
        add_row_to_lessons(row, lessons)
    return output 


def get_lessons_by_school_class_id(school_class_id: Optional[int]):
    data = _get_lessons_by_school_class_id(school_class_id)
    return format_lessons(data)

@search_func
def _get_lessons_by_school_class_id(
        db_sess: Session, school_class_id: Optional[int]):

    query = db_sess.query(
            Lesson.lesson_id,
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

    return query.all()


@search_func
def _get_schools(db_sess: Session) -> list[tuple]:
    return db_sess.query(School.school_id, School.name, School.address).all()


def format_schools(query_result: list[tuple]) -> dict:
    keys = ['id', 'name', 'address']
    return {'schools': [dict(zip(keys, row)) for row in query_result]}


def get_schools() -> dict:
    return format_schools(_get_schools())


def format_school_classes(query_result: list[tuple]) -> dict:
    keys = ['id', 'number', 'letter']
    school_classes = [dict(zip(keys, row)) for row in query_result]
    return {'school_classes': school_classes}


def get_school_classes_by_school_id(school_id: int) -> dict:
    data = _get_school_classes_by_school_id(school_id)
    return format_school_classes(data)


@search_func
def _get_school_classes_by_school_id(db_sess: Session, 
                                      school_id: int) -> list[int]:
    query = db_sess.query(
            SchoolClass.school_class_id, 
            SchoolClass.number,
            SchoolClass.letter
    )
    query = query.filter_by(school_id=school_id)
    return query.all()

def get_lessons_by_school_id(school_id: int) -> dict:
    data = _get_lessons_by_school_id(school_id)
    return format_lessons(data)


@search_func
def _get_lessons_by_school_id(db_sess: Session, school_id: int) -> dict:
    school_classes = _get_school_classes_by_school_id(db_sess, school_id)
    output = []
    for school_class_id, *_ in school_classes:
        output.extend(_get_lessons_by_school_class_id(school_class_id))
    return output

