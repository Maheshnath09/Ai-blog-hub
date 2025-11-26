import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or '151033b81c28f882895d0d3865735597230b9b51083e7e3f'
    basedir = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'instance', 'blog.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Ensure instance directory exists
    instance_dir = os.path.join(basedir, 'instance')
    if not os.path.exists(instance_dir):
        os.makedirs(instance_dir)