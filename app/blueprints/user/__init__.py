from flask import Blueprint

user = Blueprint('user', __name__, template_folder='templates/user')

from .models import User
from . import controller