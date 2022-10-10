from data.lesson import Lesson
from data.school_class import SchoolClass
from data.school import School
from data.subject import Subject
from data.teacher import Teacher
from data.day import Day


from sqlalchemy_sessions import search_func, add_func
from sqlalchemy.orm import Session


@add_func
def create_default(db_sess: Session):
    School.my_create(db_sess=db_sess, name="Lyceum 2", address="Irkutsk")


@add_func
def create_school(db_sess: Session, name: str, address: str):
    return School(name=name, address=address)
    
