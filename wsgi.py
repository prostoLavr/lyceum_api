from flask import Flask, request
import json


wsgi_app = Flask(__name__)

lessons_type = dict[str, dict[str, bool or list[tuple]]]


def get_lessons(school_class: str or None) -> lessons_type:
    pass


def lessons_to_json(lessons: lessons_type) -> bytes:
    pass


@wsgi_app.route('/lessons')
def lessons():
    school_class = request.args.get("class")
    lessons = get_lessons(school_class)
    json_lessons = lessons_to_json(lessons)
    return json_lessons

