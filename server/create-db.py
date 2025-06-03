from app import app, db
from db.models import *


with app.app_context():
    db.create_all()