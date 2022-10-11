from flask import Flask, request
import json
from sqlalchemy_sessions import global_init
from data import db_manager



global_init("sqlite:///db.sqlite")

wsgi_app = Flask(__name__)

db_manager.create_default()


lessons_type = dict[str, dict[str, str or bool or list[tuple]]]


def get_lessons(school_class: str or None) -> lessons_type:
    return {
            "name": "математика", 
            "required": True, 
            "times": [[8, 0, 8, 30], [8, 40, 9, 10]], 
            "teacher": "Full Teacher Name"
    }



@wsgi_app.route('/lessons')
def lessons() -> str:
    school_class = request.args.get("class")
    lessons = get_lessons(school_class)
    json_lessons = json.dumps(lessons, ensure_ascii=False).encode('utf8')
    return json_lessons


if __name__ == "__main__":
    wsgi_app.run("0.0.0.0", 8080)

