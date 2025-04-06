import pandas as pd
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import random

# Download NLTK resources
nltk.download('vader_lexicon')

def analyze_sentiment(data):
    """
    Analyze sentiment of trend content
    
    Args:
        data (pd.DataFrame): DataFrame containing social media trend data
        
    Returns:
        pd.DataFrame: Data with sentiment analysis results
    """
    # Create a copy of the data to avoid modifying the original
    sentiment_data = data.copy()
    
    # Check if content column exists for sentiment analysis
    if 'content' in sentiment_data.columns:
        # Initialize the VADER sentiment analyzer
        sia = SentimentIntensityAnalyzer()
        
        # Apply sentiment analysis to each content item
        def get_sentiment(text):
            if pd.isna(text) or text == '':
                return 'Neutral'
                
            sentiment_score = sia.polarity_scores(text)
            
            # Classify based on compound score
            if sentiment_score['compound'] >= 0.05:
                return 'Positive'
            elif sentiment_score['compound'] <= -0.05:
                return 'Negative'
            else:
                return 'Neutral'
                
        # Add sentiment column to the dataframe
        sentiment_data['sentiment'] = sentiment_data['content'].apply(get_sentiment)
    else:
        # If no content column, simulate sentiment distribution (for demonstration)
        # In real implementation, this would analyze actual content
        sentiments = ['Positive', 'Neutral', 'Negative']
        weights = [0.45, 0.35, 0.20]  # More positive than negative
        sentiment_data['sentiment'] = random.choices(
            sentiments, 
            weights=weights, 
            k=len(sentiment_data)
        )
    
    return sentiment_data

def get_sentiment_distribution(sentiment_data):
    """
    Calculate the distribution of sentiments
    
    Args:
        sentiment_data (pd.DataFrame): DataFrame with sentiment analysis results
        
    Returns:
        pd.DataFrame: Sentiment distribution summary
    """
    # Group by sentiment and count occurrences
    sentiment_dist = sentiment_data.groupby('sentiment').size().reset_index(name='count')
    
    # Calculate percentage
    total = sentiment_dist['count'].sum()
    sentiment_dist['percentage'] = (sentiment_dist['count'] / total * 100).round(1)
    
    return sentiment_dist

def analyze_sentiment_by_industry(sentiment_data):
    """
    Analyze sentiment distribution across different industries
    
    Args:
        sentiment_data (pd.DataFrame): DataFrame with sentiment analysis results
        
    Returns:
        pd.DataFrame: Industry-wise sentiment distribution
    """
    # Check if industry column exists
    if 'industry' in sentiment_data.columns:
        # Group by industry and sentiment
        industry_sentiment = sentiment_data.groupby(['industry', 'sentiment']).size().reset_index(name='count')
        
        # Calculate percentage within each industry
        industry_totals = industry_sentiment.groupby('industry')['count'].transform('sum')
        industry_sentiment['percentage'] = (industry_sentiment['count'] / industry_totals * 100).round(1)
        
        return industry_sentiment
    else:
        # Return empty dataframe if industry column doesn't exist
        return pd.DataFrame(columns=['industry', 'sentiment', 'count', 'percentage'])

def get_sentiment_keywords(sentiment_data):
    """
    Extract keywords that appear most frequently in each sentiment category
    
    Args:
        sentiment_data (pd.DataFrame): DataFrame with sentiment analysis results
        
    Returns:
        dict: Dictionary with lists of keywords for each sentiment
    """
    # Check if content and sentiment columns exist
    if 'content' in sentiment_data.columns and 'sentiment' in sentiment_data.columns:
        # Initialize dictionary to store keywords
        sentiment_keywords = {
            'Positive': [],
            'Neutral': [],
            'Negative': []
        }
        
        # Function to extract keywords (simplified version)
        def extract_keywords(text):
            # In a real implementation, this would use NLP techniques to extract meaningful keywords
            # For simplicity, we're just splitting the text into words
            if pd.isna(text) or text == '':
                return []
            
            words = text.lower().split()
            # Filter out short words and common stopwords
            stopwords = ['the', 'and', 'is', 'in', 'to', 'for', 'of', 'that', 'this', 'a', 'an']
            keywords = [word for word in words if len(word) > 3 and word not in stopwords]
            return keywords
        
        # Process each sentiment category
        for sentiment in ['Positive', 'Neutral', 'Negative']:
            # Filter data for the current sentiment
            filtered_data = sentiment_data[sentiment_data['sentiment'] == sentiment]
            
            # Extract keywords from all content
            all_keywords = []
            for content in filtered_data['content']:
                all_keywords.extend(extract_keywords(content))
            
            # Count keyword frequencies
            keyword_counts = {}
            for keyword in all_keywords:
                keyword_counts[keyword] = keyword_counts.get(keyword, 0) + 1
            
            # Sort by frequency and get top keywords
            sorted_keywords = sorted(keyword_counts.items(), key=lambda x: x[1], reverse=True)
            top_keywords = [keyword for keyword, count in sorted_keywords[:10]]
            
            sentiment_keywords[sentiment] = top_keywords
        
        return sentiment_keywords
    else:
        # Return empty dictionary if required columns don't exist
        return {
            'Positive': [],
            'Neutral': [],
            'Negative': []
        }
