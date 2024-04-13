from flask import Blueprint, abort
from sqlalchemy import and_

blp = Blueprint('back-end', __name__)

@blp.route("/")
def hello_world():
    return "<p>Hello, World!</p>"