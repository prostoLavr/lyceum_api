from flask import Flask
from flask import send_file

import os
import argparse
from typing import Optional
import json
import logging


from app import wsgi_app, db_manager

right_lessons_type = dict[str, dict[str, str or bool or list[list[int]]]]
error_msg_type = dict[str, str]
lessons_type = right_lessons_type | error_msg_type
page_type = str | bytes


logger = logging.getLogger(__name__)


def get_lessons(
        school_id: Optional[int] = None,
        school_class_id: Optional[int] = None) -> lessons_type:
    return db_manager.get_lessons(school_id=school_id,
                                  school_class_id=school_class_id)


def to_json(data: dict) -> bytes:
    return json.dumps(data, ensure_ascii=False).encode("utf8")


@wsgi_app.route("/school")
def schools() -> page_type:
    return to_json(db_manager.get_schools())


@wsgi_app.route("/school/<int:school_id>/image")
def school_image(school_id: int) -> page_type:
    return send_file(f"/images/schools/{school_id}.jpg", mimetype='image/gif')


@wsgi_app.route("/school/<int:school_id>/school_class")
def school_classes_list(school_id: int) -> page_type:
    school_classes = db_manager.get_school_classes(school_id)
    return to_json(school_classes)


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

