from transformers import pipeline
from textblob import TextBlob
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from .models import Post

# Load pre-trained summarizer (BART model)
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def generate_summary(content):
    try:
        summary = summarizer(content, max_length=130, min_length=30, do_sample=False)[0]['summary_text']
        return summary
    except Exception:
        return "Summary generation failed."

def analyze_sentiment(comment):
    blob = TextBlob(comment)
    polarity = blob.sentiment.polarity
    if polarity > 0:
        return "positive"
    elif polarity < 0:
        return "negative"
    else:
        return "neutral"

def get_recommendations(post_id, num_recs=3):
    posts = Post.query.all()
    if not posts:
        return []

    contents = [p.content for p in posts]
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(contents)

    current_idx = next(i for i, p in enumerate(posts) if p.id == post_id)
    similarities = cosine_similarity(tfidf_matrix[current_idx], tfidf_matrix).flatten()
    similar_indices = similarities.argsort()[-num_recs-1:-1][::-1]  # Top N excluding itself

    return [posts[i] for i in similar_indices]