from app import create_app
import os

app = create_app()

# Initialize database for Vercel
if os.environ.get('VERCEL'):
    with app.app_context():
        try:
            from app import db
            from app.models import User
            
            # Force recreate database with your account
            db.drop_all()
            db.create_all()
            
            # Create your user account
            user = User(
                username='mahesh_23',
                email='maheshnath2143@gmail.com'
            )
            user.set_password('mahesh@09')  # Your PostgreSQL password
            db.session.add(user)
            db.session.commit()
            print("Database recreated with your account")
                
        except Exception as e:
            print(f"Database initialization error: {e}")

if __name__ == "__main__":
    app.run()