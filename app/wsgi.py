from flask import Flask, request
import json
from sqlalchemy_sessions import global_init
from data import db_manager
import os


user = os.getenv("POSTGRES_USER")
password = os.getenv("POSTGRES_PASSWORD")
database = os.getenv("POSTGRES_DB")
port = os.getenv("POSTGRES_PORT") or 5432
host = os.getenv("POSTGRES_HOST")
global_init(f"postgresql://{user}:{password}@{host}:{port}/{database}")

wsgi_app = Flask(__name__)

db_manager.create_default()


lessons_type = dict[str, dict[str, str or bool or list[list[int]]]]


def get_lessons(school_class: str or None) -> lessons_type:
    return {
            "name": "математика", 
            "required": True, 
            "times": {"10Б": {"monday": [[8, 0, 8, 30], [8, 40, 9, 10]]}}, 
            "teacher": "Full Teacher Name"
    }



@wsgi_app.route("/lessons")
def lessons() -> str:
    school_class = request.args.get("class")
    lessons = get_lessons(school_class)
    json_lessons = json.dumps(lessons, ensure_ascii=False).encode("utf8")
    return json_lessons


if __name__ == "__main__":
    wsgi_app.run("0.0.0.0", 8080)

