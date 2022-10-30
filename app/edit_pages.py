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


right_lessons_type = dict[str, dict[str, str or bool or list[list[int]]]]
error_msg_type = dict[str, str]
lessons_type = right_lessons_type | error_msg_type
page_type = str | bytes


logger = logging.getLogger(__name__)


