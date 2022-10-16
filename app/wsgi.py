from flask import Flask, request

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


def get_lessons(
        school_id: Optional[int] = None,
        school_class_id: Optional[int] = None
        ) -> lessons_type:
    if school_id is not None:
        db_manager.get_lessons_by_school_id(school_id)
    elif school_class_id is not None:
        print(db_manager.get_lessons_by_school_class_id(school_class_id))
    else:
        raise Exception

    return {
            "name": "математика", 
            "required": True, 
            "times": {"10Б": {"monday": [[8, 0, 8, 30], [8, 40, 9, 10]]}}, 
            "teacher": "Full Teacher Name"
    }


def to_json(data: dict) -> str:
    return json.dumps(data, ensure_ascii=False).encode("utf8")


@wsgi_app.route("/school/<int:school_id>")
def all_lessons(school_id: int) -> str:
    lessons = get_lessons(school_id=school_id)
    return to_json(lessons)


@wsgi_app.route("/school_class/<int:school_class_id>")
def class_lessons(school_class_id: int) -> str:
    lessons = get_lessons(school_class_id=school_class_id)
    return to_json(lessons)


if __name__ == "__main__":
    wsgi_app.run("0.0.0.0", 8080)

