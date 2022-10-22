from flask import Flask

from sqlalchemy_sessions import global_init
import db_manager

import os
import argparse
from dataclasses import dataclass
from typing import Optional
import json

# Lawrence's shit code to run with args
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--sqlite')
    parser.add_argument('-u', '--user')
    parser.add_argument('-P', '--password')
    parser.add_argument('-H', '--host')
    parser.add_argument('-d', '--database')
    parser.add_argument('-p', '--port')

    args = parser.parse_args()
    sqlite_path = getattr(args, 'sqlite')
else:
    sqlite_path = None


    # It's is real trash
    @dataclass
    class VoidArgs:
        user: None
        password: None
        database: None
        port: None
        host: None


    args = VoidArgs(None, None, None, None, None)
    # More Nones

if sqlite_path is None:
    user = args.user or os.getenv("POSTGRES_USER")
    password = args.password or os.getenv("POSTGRES_PASSWORD")
    database = args.database or os.getenv("POSTGRES_DB")
    port = args.port or os.getenv("POSTGRES_PORT") or 5432
    host = args.host or os.getenv("POSTGRES_HOST")
    global_init(f"postgresql://{user}:{password}@{host}:{port}/{database}")
else:
    global_init(f"sqlite:///{sqlite_path}")

wsgi_app = Flask(__name__)

db_manager.create_default()

lessons_type = dict[str, dict[str, str or bool or list[list[int]]]]
error_msg_type = dict[str, str]
page_type = str | bytes


def get_lessons(
        school_id: Optional[int] = None,
        school_class_id: Optional[int] = None
) -> lessons_type | error_msg_type:
    if school_id is not None:
        return db_manager.get_lessons_by_school_id(school_id)
    elif school_class_id is not None:
        return db_manager.get_lessons_by_school_class_id(school_class_id)
    else:
        raise ValueError("Expected school_id or school_class_id")


def to_json(data: dict) -> bytes:
    return json.dumps(data, ensure_ascii=False).encode("utf8")


@wsgi_app.route("/school")
def schools() -> page_type:
    return to_json(db_manager.get_schools())


@wsgi_app.route("/school/<int:school_id>/school_class")
def school_classes_list(school_id: int) -> page_type:
    schools = db_manager.get_school_classes_by_school_id(school_id)
    return to_json(schools)


@wsgi_app.route("/school/<int:school_id>/lesson")
def lessons_for_school(school_id: int) -> page_type:
    lessons = get_lessons(school_id=school_id)
    return to_json(lessons)


@wsgi_app.route("/school_class/<int:school_class_id>/lesson")
def lessons_for_school_class(school_class_id: int) -> page_type:
    lessons = get_lessons(school_class_id=school_class_id)
    return to_json(lessons)


if __name__ == "__main__":
    wsgi_app.run("0.0.0.0", 8080)
