import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or '151033b81c28f882895d0d3865735597230b9b51083e7e3f'
    
    # Database configuration
    if os.environ.get('VERCEL'):
        # Use Vercel Postgres
        SQLALCHEMY_DATABASE_URI = os.environ.get('POSTGRES_URL') or os.environ.get('DATABASE_URL')
        if SQLALCHEMY_DATABASE_URI and SQLALCHEMY_DATABASE_URI.startswith('postgres://'):
            SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace('postgres://', 'postgresql://', 1)
    else:
        # Local development
        basedir = os.path.abspath(os.path.dirname(__file__))
        SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'instance', 'blog.db')
        # Ensure instance directory exists for local development
        instance_dir = os.path.join(basedir, 'instance')
        if not os.path.exists(instance_dir):
            os.makedirs(instance_dir)
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False