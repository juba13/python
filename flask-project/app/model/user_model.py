# models.py

from flask_login import UserMixin
from werkzeug.security import generate_password_hash
from .. import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    is_admin = db.Column(db.Boolean, default=False)   

    def __init__(self,form_data=None):
      self.first_name=""
      self.last_name=""
      self.email=""
      self.password=""
      self.is_admin=False
    
    @staticmethod
    def getSuperAdmin():
        user=User()
        user.id=99999999
        user.first_name="Super"
        user.last_name="Admin"
        user.email="admin@pridevision.com"
        user.password=generate_password_hash("admin", method='sha256')
        user.is_admin=True
        return user

    @staticmethod
    def isSuperAdmin(email):
        user=User.getSuperAdmin()
        return user.email==email      