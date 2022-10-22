from data.lesson import Lesson
from data.school_class import SchoolClass
from data.school import School
from data.subject import Subject
from data.teacher import Teacher

from sqlalchemy_sessions import search_func, add_func, edit_func
from sqlalchemy.orm import Session

import datetime as dt
import calendar
from typing import Optional
from dataclasses import dataclass


@add_func
def _create(_: Session, cls, **kwargs):
    """
        Create SQLAlchemy class instance.

        _ - auto created session by sqlalchemy_sessions decorators
                    do not use this argument
        cls - SQLAlchemy Table Class
        **kwargs - object parameters
    """
    return cls(**kwargs)


@edit_func
def _create_if_no_exists(db_sess: Session, cls, **kwargs):
    """
        Create SQLAlchemy class instance if it is not already exists.

        db_sess - auto created session by sqlalchemy_sessions decorators
                        do not use this argument
        cls - SQLAlchemy Table Class
        **kwargs - object parameters
    """
    query = db_sess.query(cls).filter_by(**kwargs)
    if (db_object := query.one_or_none()) is not None:
        return db_object
    return _create(db_sess, cls, **kwargs)


@edit_func
def create_default(db_sess: Session):
    """
        Create default database objects.
        Function is an example to create them.

        db_sess - auto created session by sqlalchemy_sessions decorators
                        do not use this argument
    """
    school = _create_if_no_exists(
        db_sess, School, school_id=1, name="Лицей №2", address="Иркутск"
    )
    teacher = _create_if_no_exists(
        db_sess, Teacher, teacher_id=1, name="Мария Александровна Зубакова"
    )
    school_class = _create_if_no_exists(
        db_sess, SchoolClass, school_class_id=1, number=10, letter='Б',
        school_id=school.school_id
    )
    subject = _create_if_no_exists(
        db_sess, Subject, name="Математика", subject_id=1,
        school_class_id=school_class.school_class_id,
        teacher_id=teacher.teacher_id
    )
    _ = _create_if_no_exists(
        db_sess, Lesson, subject_id=subject.subject_id, lesson_id=1,
        teacher_id=teacher.teacher_id, start_time=dt.time(8, 0),
        end_time=dt.time(8, 30), day=0
    )


@dataclass
class __OneLessonQueryResult:
    """Class to save lesson data from __get_lessons_by_school_class_id"""
    lesson_id: int
    subject_name: str
    required: bool
    teacher: str
    class_id: int
    class_number: int
    class_letter: str
    weekday: int
    start_time: dt.datetime
    end_time: dt.datetime

    def get_lesson_dict_with_void_times(self):
        return {'id': self.lesson_id,
                'name': self.subject_name,
                'required': self.required,
                'teacher': self.teacher,
                'times': []}


def __add_new_lesson_to_lesson_list(
        lesson_query_result: __OneLessonQueryResult,
        list_of_added_lessons: list):
    """
        Add an __OneLessonQueryResult instance to list that
        is as [{"id": 0, "name": "Mathematics", ...}, ...]
    """
    for lesson in list_of_added_lessons:
        if lesson['id'] == lesson_query_result.lesson_id:
            __add_lesson_query_result_to_list_of_lesson_times(
                lesson_query_result, lesson['times']
            )
            break
    else:
        lesson = lesson_query_result.get_lesson_dict_with_void_times()
        __add_lesson_query_result_to_list_of_lesson_times(
            lesson_query_result, lesson['times']
        )
        list_of_added_lessons.append(lesson)


def __add_lesson_query_result_to_list_of_lesson_times(
        lesson_query_result: __OneLessonQueryResult,
        list_of_lesson_times: list[dict]):
    """
        Add an __OneLessonQueryResult instance to list that
        is as [{"school_class_id": 1,
                "times": [
                            {"Monday": [[8, 0, 8, 30], [8, 40, 9, 20]},
                            {"Tuesday": [[9, 45, 10, 25], [10, 40, 11, 20]}
                         ]
                }]
    """
    for lesson_times_for_class in list_of_lesson_times:
        if lesson_times_for_class['school_class_id'] == lesson_query_result.lesson_id:
            break  # lesson_times_for_class is using below
    else:
        lesson_times_for_class = {"school_class_id":
                                  lesson_query_result.class_id}
        list_of_lesson_times.append(lesson_times_for_class)

    day_name = calendar.day_name[lesson_query_result.weekday]
    if day_name not in lesson_times_for_class.keys():
        lesson_times_for_class[day_name] = []
    start_end_time = [lesson_query_result.start_time.hour,
                      lesson_query_result.start_time.minute,
                      lesson_query_result.end_time.hour,
                      lesson_query_result.end_time.minute]
    if start_end_time not in lesson_times_for_class[day_name]:
        lesson_times_for_class[day_name].append(start_end_time)


def __convert_lesson_query_result_to_dict(
        lesson_query_result: list[__OneLessonQueryResult]) -> dict:

    output = {'lessons': []}
    for lesson_query_result in lesson_query_result:
        __add_new_lesson_to_lesson_list(lesson_query_result, output['lessons'])
    return output


def get_lessons_by_school_class_id(school_class_id: Optional[int]):
    data = __get_lessons_by_school_class_id(school_class_id)
    return __convert_lesson_query_result_to_dict(data)


@search_func
def __get_lessons_by_school_class_id(
        db_sess: Session,
        school_class_id: Optional[int]) -> list[__OneLessonQueryResult]:

    query = db_sess.query(
        Lesson.lesson_id,
        Subject.name,
        Subject.required,
        Teacher.name,
        SchoolClass.school_class_id,
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

    return [__OneLessonQueryResult(*row) for row in query.all()]


@search_func
def __get_schools(db_sess: Session) -> list[tuple]:
    return db_sess.query(School.school_id, School.name, School.address).all()


def __format_schools(query_result: list[tuple]) -> dict:
    keys = ['id', 'name', 'address']
    return {'schools': [dict(zip(keys, row)) for row in query_result]}


def get_schools() -> dict:
    return __format_schools(__get_schools())


def __format_school_classes(query_result: list[tuple]) -> dict:
    keys = ['id', 'number', 'letter']
    school_classes = [dict(zip(keys, row)) for row in query_result]
    return {'school_classes': school_classes}


def get_school_classes_by_school_id(school_id: int) -> dict:
    data = __get_school_classes_by_school_id(school_id)
    return __format_school_classes(data)


@search_func
def __get_school_classes_by_school_id(db_sess: Session,
                                      school_id: int) -> list[tuple]:
    query = db_sess.query(
        SchoolClass.school_class_id,
        SchoolClass.number,
        SchoolClass.letter
    )
    query = query.filter_by(school_id=school_id)
    return query.all()


def get_lessons_by_school_id(school_id: int) -> dict:
    data = __get_lessons_by_school_id(school_id)
    return __convert_lesson_query_result_to_dict(data)


@search_func
def __get_lessons_by_school_id(
        db_sess: Session,
        school_id: int) -> list[__OneLessonQueryResult]:
    school_classes = __get_school_classes_by_school_id(db_sess, school_id)
    output = []
    for school_class_id, *_ in school_classes:
        output.extend(__get_lessons_by_school_class_id(school_class_id))
    return output
