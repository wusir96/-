
import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard-to-guess-string'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'mysql+pymysql://root:wusir2004@localhost/hospital_system'
    SQLALCHEMY_TRACK_MODIFICATIONS = False