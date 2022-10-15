from flask import Flask, request
import json
from sqlalchemy_sessions import global_init
import db_manager
import os
import argparse
from dataclasses import dataclass


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

    @dataclass
    class VoidArgs:
        user: None
        password: None
        database: None
        port: None
        host: None
    
    args = VoidArgs(None, None, None, None, None)
    

if sqlite_path is None:
    args = parser.parse_args()
    user = args.user or os.getenv("POSTGRES_USER")
    password = args.password or os.getenv("POSTGRES_PASSWORD")
    database = args.database or os.getenv("POSTGRES_DB")
    port = args.port or os.getenv("POSTGRES_PORT") or 5432
    host = args.host or os.getenv("POSTGRES_HOST")
    global_init(f"postgresql://{user}:{password}@{host}:{port}/{database}")
else:
    global_init(f"sqlite://{sqlite_path}")

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

