from app import create_app
import os

app = create_app()

# Initialize database for Vercel
if os.environ.get('VERCEL'):
    with app.app_context():
        try:
            from app import db
            
            # Drop and recreate all tables with correct schema
            db.drop_all()
            db.create_all()
            print("Database tables recreated successfully")
                
        except Exception as e:
            print(f"Database initialization error: {e}")
            # Continue anyway - don't crash the app

if __name__ == "__main__":
    app.run()