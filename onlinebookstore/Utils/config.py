import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__)) 

class Config:
   SECRET_KEY = os.environ.get("SECRET_KEY") or "remember-to-add-secret-key"   
   SQLALCHEMY_DATABASE_URI = (                           
           os.environ.get('DATABASE_URL') or
           'sqlite:///' + os.path.join(BASE_DIR, 'onlinebookstore.db')
   )
   SQLALCHEMY_TRACK_MODIFICATIONS = False
   #BABEL_DEFAULT_LOCALE = 'en'
  # BABEL_TRANSLATION_DIRECTORIES = 'translations'
  # REDIS_URL = "redis://:sinan_cos_2023@localhost:6379/0"
   LANGUAGES = [
        {'code': 'gb', 'name': 'English'},
        {'code': 'de', 'name': 'German'},
        {'code': 'fr', 'name': 'French'},
        {'code': 'tr', 'name': 'Turkish'},
        {'code': 'ae', 'name': 'Arabic'}
        ]
   
   UPLOAD_FOLDER = 'onlinebookstore\\static\\images'