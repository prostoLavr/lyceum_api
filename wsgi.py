from flask import Flask, request
import json


wsgi_app = Flask(__name__)

lessons_type = dict[str, dict[str, str or bool or list[tuple]]]


def get_lessons(school_class: str or None) -> lessons_type:
    return {"monday": {"name": "math", 
                       "required": True,
                       "times": [("8:00", "8:30")]}
           }



@wsgi_app.route('/lessons')
def lessons():
    school_class = request.args.get("class")
    lessons = get_lessons(school_class)
    json_lessons = json.dumps(lessons)
    return json_lessons
