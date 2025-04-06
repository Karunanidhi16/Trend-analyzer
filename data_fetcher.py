import pandas as pd
import requests
import os
import json
import random
from datetime import datetime, timedelta

def fetch_social_media_data(platform='All Platforms', days=7):
    """
    Fetch social media trend data from APIs or generate mock data for development
    
    Args:
        platform (str): Social media platform to fetch data from ('All Platforms', 'Twitter', 'Instagram', 'TikTok')
        days (int): Number of days of data to fetch
        
    Returns:
        pd.DataFrame: Processed social media trend data
    """
    # In a production environment, this would use actual API calls
    # For this implementation, we'll generate structured data that resembles real social media data
    
    # Create date range
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    date_range = pd.date_range(start=start_date, end=end_date, freq='D')
    
    # Industries
    industries = ['Technology', 'Fashion', 'Entertainment', 'Food', 'Travel', 'Fitness', 'Beauty', 'Business', 'Education']
    
    # Platforms
    platforms = ['Twitter', 'Instagram', 'TikTok']
    if platform != 'All Platforms':
        platforms = [platform]
    
    # Trends and hashtags by industry
    industry_trends = {
        'Technology': {
            'trends': ['AI Ethics', 'Web3', 'Quantum Computing', 'AR Experiences', 'Green Tech'],
            'hashtags': ['#AI', '#Tech', '#Innovation', '#Web3', '#SmartHome', '#5G', '#MachineLearning'],
            'growth_range': (5, 25)
        },
        'Fashion': {
            'trends': ['Sustainable Fashion', 'Y2K Revival', 'Gender-Neutral', 'Vintage', 'Upcycling'],
            'hashtags': ['#OOTD', '#Fashion', '#Vintage', '#Sustainable', '#StyleTips', '#FashionWeek'],
            'growth_range': (8, 30)
        },
        'Entertainment': {
            'trends': ['Streaming Exclusives', 'Interactive Content', 'Comeback Tours', 'Fan Edits', 'Character Analysis'],
            'hashtags': ['#Netflix', '#MovieNight', '#NewMusic', '#Premiere', '#MustWatch', '#TVShow'],
            'growth_range': (10, 35)
        },
        'Food': {
            'trends': ['Plant-Based Recipes', 'Food Fusion', 'Local Sourcing', 'Cloud Kitchens', 'Food Reels'],
            'hashtags': ['#Foodie', '#Recipes', '#Cooking', '#Vegan', '#FoodPhotography', '#HomeCooking'],
            'growth_range': (4, 18)
        },
        'Travel': {
            'trends': ['Off-Grid Travel', 'Workations', 'Sustainable Tourism', 'Virtual Tours', 'Solo Travel'],
            'hashtags': ['#Travel', '#Wanderlust', '#Vacation', '#TravelTips', '#Adventure', '#Explore'],
            'growth_range': (6, 22)
        },
        'Fitness': {
            'trends': ['Home Workouts', 'Mental Fitness', 'Hybrid Gyms', 'Recovery Focus', 'Community Challenges'],
            'hashtags': ['#Fitness', '#Workout', '#HealthyLifestyle', '#Exercise', '#FitnessGoals', '#ActiveLife'],
            'growth_range': (7, 24)
        },
        'Beauty': {
            'trends': ['Clean Beauty', 'Skincare Tech', 'Inclusive Products', 'Male Beauty', 'Beauty Subscriptions'],
            'hashtags': ['#BeautyTips', '#Skincare', '#Makeup', '#BeautyHacks', '#Cosmetics', '#SelfCare'],
            'growth_range': (9, 28)
        },
        'Business': {
            'trends': ['Remote Work', 'ESG Investing', 'Creator Economy', 'NFT Business', 'Direct-to-Consumer'],
            'hashtags': ['#Business', '#Entrepreneur', '#Marketing', '#StartUp', '#Leadership', '#Strategy'],
            'growth_range': (3, 15)
        },
        'Education': {
            'trends': ['Microlearning', 'EdTech', 'Skill Certificates', 'Cohort Learning', 'Education Pods'],
            'hashtags': ['#Education', '#Learning', '#StudentLife', '#Study', '#OnlineLearning', '#TeacherLife'],
            'growth_range': (2, 12)
        }
    }
    
    # Create empty list to store data
    data_list = []
    
    # Generate data for each date, platform, and industry
    for date in date_range:
        for plt in platforms:
            # Determine how many trends to generate for this platform and date
            num_trends = random.randint(5, 15)
            
            for _ in range(num_trends):
                # Randomly select an industry
                industry = random.choice(industries)
                
                # Get trends and hashtags for this industry
                industry_data = industry_trends[industry]
                trend = random.choice(industry_data['trends'])
                hashtag = random.choice(industry_data['hashtags'])
                
                # Generate growth rate
                growth_low, growth_high = industry_data['growth_range']
                growth_rate = round(random.uniform(growth_low, growth_high), 1)
                
                # Generate engagement metrics
                engagement = random.randint(100, 10000)
                
                # Generate sample content
                content_templates = [
                    f"Check out this {trend} update! {hashtag}",
                    f"I can't believe how fast {trend} is growing! {hashtag}",
                    f"Anyone else following the latest {trend} developments? {hashtag}",
                    f"Just shared my thoughts on {trend} - what do you think? {hashtag}",
                    f"New post about {trend} is now live! {hashtag}"
                ]
                content = random.choice(content_templates)
                
                # Create data entry
                data_entry = {
                    'date': date.strftime('%Y-%m-%d'),
                    'platform': plt,
                    'trend': trend,
                    'hashtags': hashtag,
                    'industry': industry,
                    'engagement': engagement,
                    'growth_rate': growth_rate,
                    'content': content
                }
                
                data_list.append(data_entry)
    
    # Convert to DataFrame
    df = pd.DataFrame(data_list)
    
    # Convert date to datetime
    df['date'] = pd.to_datetime(df['date'])
    
    return df

def fetch_historical_trends(trend_name, days=30):
    """
    Fetch historical data for a specific trend
    
    Args:
        trend_name (str): Name of the trend to fetch data for
        days (int): Number of days of historical data to fetch
        
    Returns:
        pd.DataFrame: Historical data for the trend
    """
    # In a production environment, this would use actual API calls
    # For this implementation, we'll generate simulated historical data
    
    # Create date range
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    date_range = pd.date_range(start=start_date, end=end_date, freq='D')
    
    # Create empty list to store data
    data_list = []
    
    # Generate baseline volume with some randomness
    baseline_volume = random.randint(500, 5000)
    
    # Generate data for each date
    for i, date in enumerate(date_range):
        # Add some trend pattern to the volume
        day_factor = 1 + (i / days)  # Increasing trend over time
        weekend_factor = 1.2 if date.dayofweek >= 5 else 1.0  # Higher on weekends
        
        # Add some randomness
        random_factor = random.uniform(0.8, 1.2)
        
        # Calculate volume for this day
        volume = int(baseline_volume * day_factor * weekend_factor * random_factor)
        
        # Create data entry
        data_entry = {
            'date': date.strftime('%Y-%m-%d'),
            'trend': trend_name,
            'volume': volume
        }
        
        data_list.append(data_entry)
    
    # Convert to DataFrame
    df = pd.DataFrame(data_list)
    
    # Convert date to datetime
    df['date'] = pd.to_datetime(df['date'])
    
    return df

def fetch_related_trends(trend_name, limit=5):
    """
    Fetch trends related to a specific trend
    
    Args:
        trend_name (str): Name of the trend to fetch related trends for
        limit (int): Maximum number of related trends to return
        
    Returns:
        list: List of related trend names
    """
    # In a production environment, this would use actual API calls
    # For this implementation, we'll generate simulated related trends
    
    # Define some related trends for common categories
    related_trends = {
        'AI Ethics': ['Machine Learning Bias', 'Responsible AI', 'AI Governance', 'Ethical Computing', 'AI Transparency'],
        'Web3': ['Blockchain', 'Decentralized Apps', 'Crypto', 'NFTs', 'Metaverse'],
        'Sustainable Fashion': ['Eco Fashion', 'Slow Fashion', 'Ethical Clothing', 'Green Fashion', 'Circular Fashion'],
        'Plant-Based Recipes': ['Vegan Cooking', 'Meatless Meals', 'Vegetarian Options', 'Dairy Alternatives', 'Whole Foods'],
        'Home Workouts': ['No-Equipment Exercise', 'Living Room Fitness', 'Online Training', 'Fitness Apps', 'Virtual Classes']
    }
    
    # Return related trends if they exist for this trend
    if trend_name in related_trends:
        return related_trends[trend_name][:limit]
    else:
        # Generate generic related trends
        return [f"{trend_name} - Variation {i+1}" for i in range(limit)]


def fetch_trending_images(platform=None, industry=None, limit=6):
    """
    Fetch trending images from various social media platforms
    
    Args:
        platform (str, optional): Specific platform to fetch images from
        industry (str, optional): Specific industry to filter images by
        limit (int): Maximum number of images to return
        
    Returns:
        list: List of dictionaries containing image metadata
    """
    # For demonstration purposes - in a real app we'd call the actual APIs
    # Define image placeholders for different platforms with appropriate aspect ratios
    
    # Use random generated images for placeholders
    image_urls = [
        "https://source.unsplash.com/random/600x600?social,trend",
        "https://source.unsplash.com/random/600x600?marketing", 
        "https://source.unsplash.com/random/600x600?business",
        "https://source.unsplash.com/random/600x600?technology",
        "https://source.unsplash.com/random/600x600?fashion",
        "https://source.unsplash.com/random/600x600?food",
        "https://source.unsplash.com/random/600x600?travel",
        "https://source.unsplash.com/random/600x600?fitness",
        "https://source.unsplash.com/random/600x600?beauty",
        "https://source.unsplash.com/random/600x600?education"
    ]
    
    # Platform-specific settings
    platforms = ['Instagram', 'YouTube', 'LinkedIn', 'TikTok', 'Twitter']
    if platform and platform != 'All Platforms':
        platforms = [platform]
        
    # Generate random trending images with metadata
    trending_images = []
    
    # List of possible trending topics based on industry
    topics = {
        'Technology': ['AI innovations', 'Web3 developments', 'Tech gadgets', 'Coding trends', 'Smart home'],
        'Fashion': ['Summer styles', 'Sustainable fashion', 'Street style', 'Fashion week', 'Accessories'],
        'Entertainment': ['Movie premieres', 'Music releases', 'Celebrity news', 'Streaming shows', 'Events'],
        'Food': ['Recipes', 'Restaurant openings', 'Food photography', 'Cooking tips', 'Dietary trends'],
        'Travel': ['Destinations', 'Travel tips', 'Adventure', 'Hotels', 'Local experiences'],
        'Fitness': ['Workout routines', 'Fitness challenges', 'Health tips', 'Sports', 'Wellness'],
        'Beauty': ['Skincare', 'Makeup trends', 'Hair styling', 'Beauty products', 'Tutorials'],
        'Business': ['Entrepreneurship', 'Marketing', 'Startups', 'Leadership', 'Remote work'],
        'Education': ['Learning resources', 'Study tips', 'Courses', 'Student life', 'Academic']
    }
    
    # Use all topics if no industry specified
    all_topics = []
    if industry and industry != 'All Industries':
        all_topics = topics.get(industry, [])
    else:
        for topic_list in topics.values():
            all_topics.extend(topic_list)
    
    # Generate random engagement numbers
    for i in range(limit):
        platform = random.choice(platforms)
        
        # Different engagement metrics based on platform
        if platform == 'Instagram':
            engagement = {
                'likes': random.randint(500, 50000),
                'comments': random.randint(10, 500),
                'shares': random.randint(5, 200)
            }
        elif platform == 'YouTube':
            engagement = {
                'views': random.randint(1000, 1000000),
                'likes': random.randint(100, 50000),
                'comments': random.randint(10, 1000)
            }
        elif platform == 'LinkedIn':
            engagement = {
                'reactions': random.randint(50, 5000),
                'comments': random.randint(5, 200),
                'shares': random.randint(10, 500)
            }
        elif platform == 'TikTok':
            engagement = {
                'views': random.randint(5000, 1000000),
                'likes': random.randint(500, 100000),
                'shares': random.randint(50, 5000)
            }
        else:  # Twitter
            engagement = {
                'likes': random.randint(100, 10000),
                'retweets': random.randint(10, 1000),
                'replies': random.randint(5, 500)
            }
            
        # Random timestamp within the last week
        timestamp = datetime.now() - timedelta(
            days=random.randint(0, 7),
            hours=random.randint(0, 23),
            minutes=random.randint(0, 59)
        )
        
        # Select a topic
        topic = random.choice(all_topics) if all_topics else f"Trending topic {i+1}"
        
        trending_images.append({
            'id': f"img_{i}_{platform.lower()}",
            'url': random.choice(image_urls),
            'platform': platform,
            'topic': topic,
            'caption': f"Trending content about {topic.lower()} on {platform}",
            'engagement': engagement,
            'timestamp': timestamp,
            'creator': f"@trendsetter{random.randint(100, 999)}",
            'profile_url': f"https://example.com/profile/{random.randint(1000, 9999)}"
        })
    
    return trending_images
