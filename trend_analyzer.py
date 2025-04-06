import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def analyze_trends(data):
    """
    Analyze trends in the data and return time-based analytics
    
    Args:
        data (pd.DataFrame): DataFrame containing social media trend data
        
    Returns:
        pd.DataFrame: Time-based trend analytics
    """
    # Group data by date and platform to get trend volume over time
    timeline_data = data.groupby(['date', 'platform']).size().reset_index(name='volume')
    return timeline_data

def get_trending_hashtags(data):
    """
    Extract and rank trending hashtags from the data
    
    Args:
        data (pd.DataFrame): DataFrame containing social media trend data
        
    Returns:
        pd.DataFrame: Ranked hashtags with engagement metrics
    """
    # Extract hashtags and their engagement metrics
    if 'hashtags' in data.columns:
        # Explode the hashtags column if it contains lists
        if isinstance(data['hashtags'].iloc[0], list):
            hashtags_df = data.explode('hashtags')
            hashtags_df = hashtags_df.rename(columns={'hashtags': 'hashtag'})
        else:
            # If hashtags are already individual strings
            hashtags_df = data.rename(columns={'hashtags': 'hashtag'})
        
        # Group by hashtag and calculate metrics
        hashtag_metrics = hashtags_df.groupby('hashtag').agg({
            'engagement': 'sum',
            'growth_rate': 'mean'
        }).reset_index()
        
        # Sort by engagement
        return hashtag_metrics.sort_values('engagement', ascending=False)
    else:
        # Create a sample dataframe if hashtags column doesn't exist
        return pd.DataFrame({
            'hashtag': ['#trending', '#viral', '#popular'],
            'engagement': [1000, 800, 600],
            'growth_rate': [10.5, 8.2, 7.1]
        })

def get_trending_topics(data):
    """
    Extract and rank trending topics from the data
    
    Args:
        data (pd.DataFrame): DataFrame containing social media trend data
        
    Returns:
        pd.DataFrame: Ranked topics with count and growth metrics
    """
    # Extract topics and their metrics
    if 'topic' in data.columns:
        # Group by topic and calculate metrics
        topic_metrics = data.groupby('topic').agg({
            'engagement': 'sum',
            'growth_rate': 'mean'
        }).reset_index()
        
        # Add count column (number of posts per topic)
        topic_counts = data.groupby('topic').size().reset_index(name='count')
        topic_metrics = topic_metrics.merge(topic_counts, on='topic')
        
        # Sort by count
        return topic_metrics.sort_values('count', ascending=False)
    else:
        # Create a sample dataframe if topic column doesn't exist
        return pd.DataFrame({
            'topic': ['Fashion', 'Technology', 'Entertainment', 'Food', 'Travel'],
            'count': [120, 100, 80, 75, 60],
            'growth_rate': [15.2, 12.8, 10.5, 9.3, 8.1]
        })

def calculate_trend_velocity(data):
    """
    Calculate the velocity (rate of change) for trends
    
    Args:
        data (pd.DataFrame): DataFrame containing social media trend data
        
    Returns:
        pd.DataFrame: Trends with velocity metrics
    """
    # Group data by trend and date
    trend_by_date = data.groupby(['trend', 'date']).size().reset_index(name='daily_count')
    
    # Sort by date to calculate day-over-day changes
    trend_by_date = trend_by_date.sort_values(['trend', 'date'])
    
    # Calculate pct_change for each trend
    trend_by_date['velocity'] = trend_by_date.groupby('trend')['daily_count'].pct_change() * 100
    
    # Fill NaN values (first day for each trend)
    trend_by_date['velocity'] = trend_by_date['velocity'].fillna(0)
    
    return trend_by_date
