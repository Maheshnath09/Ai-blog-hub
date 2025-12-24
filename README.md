# AI Blog Hub

A modern Flask-based blogging platform enhanced with AI capabilities for content summarization, sentiment analysis, and intelligent recommendations.

## Features

### Core Functionality
- **User Authentication**: Registration, login, and profile management
- **Blog Management**: Create, edit, delete, and view blog posts
- **Social Features**: Follow/unfollow users, save posts, comment system
- **Search**: Find posts by title with search functionality
- **Image Support**: Upload images for posts and profile pictures

### AI-Powered Features
- **Content Summarization**: Automatic post summaries using BART model
- **Sentiment Analysis**: Comment sentiment detection using TextBlob
- **Content Recommendations**: Similar post suggestions using TF-IDF and cosine similarity

## Tech Stack

- **Backend**: Flask 3.0.3
- **Database**: SQLite with SQLAlchemy ORM
- **Authentication**: Flask-Login
- **Forms**: Flask-WTF with WTForms
- **UI**: Bootstrap 5 with Flask-Bootstrap
- **AI/ML**: 
  - Transformers (Hugging Face) for summarization
  - TextBlob for sentiment analysis
  - Scikit-learn for recommendations
- **Database Migrations**: Flask-Migrate

## Project Structure

```
ai_blog_hub/
├── app/
│   ├── static/
│   │   ├── css/
│   │   ├── js/
│   │   ├── post_images/      # Uploaded post images
│   │   └── profile_images/   # User profile pictures
│   ├── templates/            # HTML templates
│   ├── __init__.py          # Flask app factory
│   ├── ai_utils.py          # AI functionality
│   ├── forms.py             # WTForms definitions
│   ├── models.py            # Database models
│   └── routes.py            # Application routes
├── instance/
│   └── blog.db              # SQLite database
├── migrations/              # Database migration files
├── venv-stable/            # Virtual environment
├── config.py               # Configuration settings
├── requirements.txt        # Python dependencies
└── run.py                  # Application entry point
```

## Installation

### Option 1: Docker (Recommended)

#### Prerequisites
- Docker
- Docker Compose

#### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd ai_blog_hub
   ```

2. **Build and run with Docker Compose**
   ```bash
   docker-compose up --build
   ```

3. **Or run with Docker directly**
   ```bash
   docker build -t ai-blog-hub .
   docker run -p 5000:5000 -v $(pwd)/instance:/app/instance ai-blog-hub
   ```

The application will be available at `http://localhost:5000`

### Option 2: Local Development

#### Prerequisites
- Python 3.8+
- pip (Python package manager)

#### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <[repository-url](https://github.com/Maheshnath09/Ai-blog-hub)>
   cd ai_blog_hub
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv-stable
   # On Windows:
   venv-stable\Scripts\activate
   # On macOS/Linux:
   source venv-stable/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up the database**
   ```bash
   flask db upgrade
   ```

5. **Run the application**
   ```bash
   python run.py
   ```

The application will be available at `http://localhost:5000`

## Usage

### Getting Started
1. **Register**: Create a new account with username, email, and password
2. **Login**: Access your account using email and password
3. **Create Posts**: Write blog posts with optional image uploads
4. **Explore**: Browse posts, follow users, and save interesting content

### Key Features

#### User Management
- **Profile Customization**: Update username, bio, and profile picture
- **Follow System**: Follow other users to see their posts in your feed
- **Saved Posts**: Bookmark posts for later reading

#### Content Creation
- **Rich Text Posts**: Create posts with titles, content, and images
- **Image Upload**: Support for JPG, JPEG, PNG, and GIF formats
- **Post Management**: Edit or delete your own posts

#### Social Interaction
- **Comments**: Engage with posts through comments
- **Sentiment Analysis**: Automatic sentiment detection on comments
- **Following Feed**: View posts from users you follow

#### AI Features
- **Auto-Summarization**: Posts automatically generate summaries
- **Content Recommendations**: Discover similar posts based on content
- **Search**: Find posts using keyword search

## Database Models

### User Model
- User authentication and profile information
- Relationships: posts, followers, saved posts, comments

### Post Model
- Blog post content with metadata
- Features: title, content, images, timestamps, AI-generated summaries

### Comment Model
- User comments on posts
- Includes sentiment analysis results

## Configuration

The application uses environment variables for configuration:

- `SECRET_KEY`: Flask secret key for sessions (defaults to hardcoded value)
- Database: SQLite file stored in `instance/blog.db`

## AI Components

### Summarization
- **Model**: Facebook BART-large-CNN
- **Purpose**: Generate concise summaries of blog posts
- **Implementation**: Hugging Face Transformers pipeline

### Sentiment Analysis
- **Library**: TextBlob
- **Purpose**: Analyze comment sentiment (positive/negative/neutral)
- **Output**: Sentiment classification for user comments

### Recommendations
- **Algorithm**: TF-IDF vectorization with cosine similarity
- **Purpose**: Suggest similar posts based on content
- **Implementation**: Scikit-learn

## Development

### Database Migrations

#### Local Development
```bash
# Create a new migration
flask db migrate -m "Description of changes"

# Apply migrations
flask db upgrade
```

#### Docker Environment
```bash
# Create a new migration
docker-compose exec web flask db migrate -m "Description of changes"

# Apply migrations
docker-compose exec web flask db upgrade
```

### Docker Commands

```bash
# Build and start containers
docker-compose up --build

# Start containers in background
docker-compose up -d

# Stop containers
docker-compose down

# View logs
docker-compose logs -f

# Access container shell
docker-compose exec web bash
```

### Adding New Features
1. Update models in `models.py`
2. Create/update forms in `forms.py`
3. Add routes in `routes.py`
4. Create templates in `templates/`
5. Run migrations if database changes are needed

## Dependencies

Key packages and their purposes:
- `flask`: Web framework
- `flask-sqlalchemy`: Database ORM
- `flask-login`: User session management
- `flask-wtf`: Form handling and CSRF protection
- `transformers`: AI model integration
- `torch`: PyTorch backend for transformers
- `textblob`: Natural language processing
- `scikit-learn`: Machine learning utilities
- `bootstrap-flask`: UI framework integration

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source and available under the [MIT License](LICENSE).

## Support

For issues, questions, or contributions, please open an issue in the repository or contact the development team.
