from flask import Flask
from flask import send_file
from sqlalchemy_sessions import global_init
import sqlalchemy as sa

import os
import argparse
from typing import Optional
import json
import logging

from app import db_manager


wsgi_app = Flask(__name__)
logger = logging.getLogger(__name__)
logger.setLevel("DEBUG")

from app import show_pages, edit_pages 


def init(sqlite_path: Optional[str] = None):
    if sqlite_path is not None:
        global_init(f"sqlite:///" + sqlite_path)
    else:
        user = os.getenv("POSTGRES_USER")
        password = os.getenv("POSTGRES_PASSWORD")
        database = os.getenv("POSTGRES_DB")
        port = os.getenv("POSTGRES_PORT") or 5432
        host = os.getenv("POSTGRES_HOST")
        global_init(f"postgresql://{user}:{password}@{host}:{port}/{database}")
    db_manager.create_default()

