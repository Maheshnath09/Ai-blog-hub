from app import create_app
import os

app = create_app()

# For Vercel deployment
if os.environ.get('VERCEL'):
    with app.app_context():
        try:
            from app import db
            db.create_all()
        except Exception as e:
            print(f"Database error: {e}")

if __name__ == "__main__":
    app.run()