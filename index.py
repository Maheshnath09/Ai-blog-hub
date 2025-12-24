from app import create_app
import os

app = create_app()

# Initialize database for Vercel
if os.environ.get('VERCEL'):
    with app.app_context():
        try:
            from app import db
            
            # Only create tables if they don't exist (don't drop existing data)
            db.create_all()
            print("Database tables created/updated successfully")
                
        except Exception as e:
            print(f"Database initialization error: {e}")
            # Continue anyway - don't crash the app

if __name__ == "__main__":
    app.run()