from textblob import TextBlob
from .models import Post
import re

def generate_summary(content):
    """Generate a simple summary by taking first few sentences"""
    try:
        # Remove HTML tags if any
        clean_content = re.sub('<.*?>', '', content)
        sentences = clean_content.split('.')
        # Take first 2-3 sentences or first 150 characters
        if len(sentences) >= 2:
            summary = '. '.join(sentences[:2]) + '.'
        else:
            summary = clean_content[:150] + '...' if len(clean_content) > 150 else clean_content
        return summary
    except Exception:
        return "Summary generation failed."

def analyze_sentiment(comment):
    """Analyze sentiment using TextBlob"""
    try:
        blob = TextBlob(comment)
        polarity = blob.sentiment.polarity
        if polarity > 0.1:
            return "positive"
        elif polarity < -0.1:
            return "negative"
        else:
            return "neutral"
    except Exception:
        return "neutral"

def get_recommendations(post_id, num_recs=3):
    """Simple recommendation based on common words"""
    try:
        current_post = Post.query.get(post_id)
        if not current_post:
            return []
        
        all_posts = Post.query.filter(Post.id != post_id).all()
        if not all_posts:
            return []
        
        # Simple word-based similarity
        current_words = set(current_post.content.lower().split())
        recommendations = []
        
        for post in all_posts:
            post_words = set(post.content.lower().split())
            common_words = len(current_words.intersection(post_words))
            if common_words > 0:
                recommendations.append((post, common_words))
        
        # Sort by common words and return top recommendations
        recommendations.sort(key=lambda x: x[1], reverse=True)
        return [rec[0] for rec in recommendations[:num_recs]]
    except Exception:
        return []