from app import create_app
import os

app = create_app()

# Initialize database tables if needed
if os.environ.get('VERCEL'):
    with app.app_context():
        try:
            from app import db
            db.create_all()
        except Exception as e:
            print(f"Database initialization error: {e}")

if __name__ == "__main__":
    app.run()