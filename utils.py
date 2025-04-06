import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

def filter_by_industry(data, industry):
    """
    Filter social media data by industry
    
    Args:
        data (pd.DataFrame): DataFrame containing social media trend data
        industry (str): Industry to filter for
        
    Returns:
        pd.DataFrame: Filtered DataFrame
    """
    if 'industry' in data.columns:
        return data[data['industry'] == industry]
    else:
        # If no industry column, return original data
        return data

def filter_by_platform(data, platform):
    """
    Filter social media data by platform
    
    Args:
        data (pd.DataFrame): DataFrame containing social media trend data
        platform (str): Platform to filter for
        
    Returns:
        pd.DataFrame: Filtered DataFrame
    """
    if 'platform' in data.columns:
        return data[data['platform'] == platform]
    else:
        # If no platform column, return original data
        return data

def filter_by_date_range(data, days):
    """
    Filter social media data to include only the last N days
    
    Args:
        data (pd.DataFrame): DataFrame containing social media trend data
        days (int): Number of days to include
        
    Returns:
        pd.DataFrame: Filtered DataFrame
    """
    if 'date' in data.columns:
        # Calculate cutoff date
        cutoff_date = datetime.now() - timedelta(days=days)
        
        # Filter data
        return data[data['date'] >= cutoff_date]
    else:
        # If no date column, return original data
        return data

def get_growth_forecast(data):
    """
    Generate growth forecasts for trends
    
    Args:
        data (pd.DataFrame): DataFrame containing social media trend data
        
    Returns:
        pd.DataFrame: DataFrame with growth forecasts
    """
    # Create a copy of the data to avoid modifying the original
    forecast_data = data.copy()
    
    # Get unique trends
    trends = forecast_data['trend'].unique()
    
    # Create empty list to store forecast data
    forecast_list = []
    
    # Generate forecast for each trend
    for trend in trends:
        # Filter data for this trend
        trend_data = forecast_data[forecast_data['trend'] == trend]
        
        # Sort by date
        trend_data = trend_data.sort_values('date')
        
        # Get the latest date in the data
        latest_date = trend_data['date'].max()
        
        # Get current values
        current_engagement = trend_data['engagement'].mean()
        current_growth = trend_data['growth_rate'].mean()
        
        # Calculate forecast values
        forecast_days = 7  # Forecast for 7 days
        
        for i in range(1, forecast_days + 1):
            # Calculate forecast date
            forecast_date = latest_date + timedelta(days=i)
            
            # Calculate forecast volume with some randomness
            # Growth compounds each day
            daily_growth_factor = 1 + (current_growth / 100)
            compound_factor = daily_growth_factor ** i
            forecast_volume = int(current_engagement * compound_factor)
            
            # Add some randomness to make it realistic
            randomness = random.uniform(0.9, 1.1)
            forecast_volume = int(forecast_volume * randomness)
            
            # Create forecast entry
            forecast_entry = {
                'trend': trend,
                'date': latest_date,  # Historical date
                'volume': current_engagement,  # Historical volume
                'forecast_date': forecast_date,  # Forecast date
                'forecast_volume': forecast_volume,  # Forecast volume
                'growth_forecast': current_growth,  # Growth forecast percentage
                'industry': trend_data['industry'].iloc[0] if 'industry' in trend_data.columns else 'Unknown'
            }
            
            forecast_list.append(forecast_entry)
    
    # Convert to DataFrame
    forecast_df = pd.DataFrame(forecast_list)
    
    return forecast_df

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

def calculate_engagement_rate(data):
    """
    Calculate engagement rates for trends
    
    Args:
        data (pd.DataFrame): DataFrame containing social media trend data
        
    Returns:
        pd.DataFrame: Trends with engagement rate metrics
    """
    # Required columns check
    required_cols = ['trend', 'engagement', 'impressions']
    if not all(col in data.columns for col in required_cols):
        # If impressions column is missing, estimate it
        if 'impressions' not in data.columns:
            data['impressions'] = data['engagement'] * random.uniform(5, 15)
    
    # Calculate engagement rate
    data['engagement_rate'] = (data['engagement'] / data['impressions'] * 100).round(2)
    
    return data

def format_number(num):
    """
    Format large numbers in a readable way (e.g., 1K, 1M)
    
    Args:
        num (int): Number to format
        
    Returns:
        str: Formatted number
    """
    if num >= 1000000:
        return f"{num/1000000:.1f}M"
    elif num >= 1000:
        return f"{num/1000:.1f}K"
    else:
        return str(num)

def calculate_trend_score(data):
    """
    Calculate a composite trend score based on engagement, growth, and recency
    
    Args:
        data (pd.DataFrame): DataFrame containing social media trend data
        
    Returns:
        pd.DataFrame: Data with trend scores
    """
    # Create a copy of the data
    scored_data = data.copy()
    
    # Calculate recency factor (more recent = higher score)
    if 'date' in scored_data.columns:
        latest_date = scored_data['date'].max()
        scored_data['days_old'] = (latest_date - scored_data['date']).dt.days
        scored_data['recency_factor'] = 1 - (scored_data['days_old'] / max(scored_data['days_old'].max(), 1))
    else:
        scored_data['recency_factor'] = 1.0
    
    # Normalize engagement (0-1 scale)
    if 'engagement' in scored_data.columns:
        max_engagement = scored_data['engagement'].max()
        scored_data['norm_engagement'] = scored_data['engagement'] / max_engagement if max_engagement > 0 else 0
    else:
        scored_data['norm_engagement'] = 0.5
    
    # Normalize growth rate (0-1 scale)
    if 'growth_rate' in scored_data.columns:
        min_growth = scored_data['growth_rate'].min()
        max_growth = scored_data['growth_rate'].max()
        growth_range = max_growth - min_growth
        scored_data['norm_growth'] = (scored_data['growth_rate'] - min_growth) / growth_range if growth_range > 0 else 0.5
    else:
        scored_data['norm_growth'] = 0.5
    
    # Calculate composite score (weights can be adjusted)
    engagement_weight = 0.4
    growth_weight = 0.4
    recency_weight = 0.2
    
    scored_data['trend_score'] = (
        (scored_data['norm_engagement'] * engagement_weight) +
        (scored_data['norm_growth'] * growth_weight) +
        (scored_data['recency_factor'] * recency_weight)
    ) * 10  # Scale to 0-10
    
    # Round to 1 decimal place
    scored_data['trend_score'] = scored_data['trend_score'].round(1)
    
    return scored_data
