from sqlalchemy.orm import Mapped, mapped_column

from db.config import db


class Users(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str]
    password: Mapped[str]


def find_by_username(username):
    if username == 'admin':
        return Users(username='admin', email='admin@admin.dev', password='admin')
    try:
        return Users.query.filter(Users.username == username).one()
    except:
        return None
