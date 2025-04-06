import pandas as pd
import random

def generate_recommendations(data):
    """
    Generate actionable recommendations based on trend analysis
    
    Args:
        data (pd.DataFrame): DataFrame containing social media trend data
        
    Returns:
        dict: Dictionary containing categorized recommendations
    """
    # Initialize recommendations dictionary
    recommendations = {
        "Content Strategy": [],
        "Engagement Opportunities": [],
        "Platform-Specific": []
    }
    
    # Generate content strategy recommendations
    recommendations["Content Strategy"] = generate_content_recommendations(data)
    
    # Generate engagement opportunity recommendations
    recommendations["Engagement Opportunities"] = generate_engagement_recommendations(data)
    
    # Generate platform-specific recommendations
    recommendations["Platform-Specific"] = generate_platform_recommendations(data)
    
    return recommendations

def generate_content_recommendations(data):
    """
    Generate content strategy recommendations based on trending topics
    
    Args:
        data (pd.DataFrame): DataFrame containing social media trend data
        
    Returns:
        list: List of content strategy recommendations
    """
    # Get top trending topics
    if 'topic' in data.columns:
        top_topics = data.groupby('topic').agg({
            'engagement': 'sum',
            'growth_rate': 'mean'
        }).sort_values('engagement', ascending=False).head(3).index.tolist()
    else:
        # Use trends if topics aren't available
        top_topics = data.groupby('trend').agg({
            'engagement': 'sum',
            'growth_rate': 'mean'
        }).sort_values('engagement', ascending=False).head(3).index.tolist()
    
    # Get top industries
    if 'industry' in data.columns:
        top_industries = data.groupby('industry').size().sort_values(ascending=False).head(3).index.tolist()
    else:
        top_industries = ["Technology", "Entertainment", "Fashion"]
    
    # Create recommendations list
    recommendations = []
    
    # Add recommendations based on top topics
    if top_topics:
        recommendations.append({
            "title": f"Create content around '{top_topics[0]}'",
            "description": f"'{top_topics[0]}' is trending with high engagement. Creating content on this topic can help you reach a larger audience and increase engagement.",
            "action_steps": [
                f"Develop a series of posts or articles discussing '{top_topics[0]}'",
                "Incorporate relevant hashtags in your content",
                "Create visual content (images, videos) related to this topic",
                "Consider starting conversations about this topic in comments or replies"
            ],
            "metrics": {
                "relevance": 9,
                "potential_reach": data[data['trend'] == top_topics[0]]['engagement'].sum() if 'trend' in data.columns else 10000,
                "effort": 6
            }
        })
    
    # Add recommendation about content formats
    platforms = data['platform'].unique() if 'platform' in data.columns else ["Twitter", "Instagram", "TikTok"]
    recommended_formats = {
        "Twitter": "short-form text with visuals",
        "Instagram": "high-quality images and carousel posts",
        "TikTok": "short-form vertical videos"
    }
    
    format_rec = {
        "title": "Optimize content formats for each platform",
        "description": "Different platforms favor different content formats. Adapting your content to each platform's preferred format will increase engagement.",
        "action_steps": [
            f"For {platform}, focus on {recommended_formats.get(platform, 'platform-specific content')}" 
            for platform in platforms
        ] + ["Repurpose content across platforms while adapting to each platform's format"],
        "metrics": {
            "relevance": 8,
            "potential_reach": 25000,
            "effort": 7
        }
    }
    recommendations.append(format_rec)
    
    # Add recommendation about timing
    timing_rec = {
        "title": "Optimize posting schedule based on trend cycles",
        "description": "Posting at optimal times when your audience is most active can significantly increase engagement and visibility.",
        "action_steps": [
            "Analyze your audience's activity patterns to identify peak engagement times",
            "Schedule posts to align with trend lifecycle (early for thought leadership, during peak for maximum reach)",
            "Maintain consistent posting frequency to build audience expectations",
            "Test different posting times and analyze performance"
        ],
        "metrics": {
            "relevance": 7,
            "potential_reach": 15000,
            "effort": 5
        }
    }
    recommendations.append(timing_rec)
    
    # Add industry-specific recommendation if available
    if top_industries:
        industry_rec = {
            "title": f"Leverage '{top_industries[0]}' industry trends",
            "description": f"The {top_industries[0]} industry is showing high engagement. Creating content that connects your brand to this industry can help you tap into this engaged audience.",
            "action_steps": [
                f"Identify connections between your brand/content and {top_industries[0]}",
                "Partner with influencers or brands in this industry",
                "Join conversations about trending topics in this industry",
                "Create content that bridges your niche with this industry"
            ],
            "metrics": {
                "relevance": 8,
                "potential_reach": 20000,
                "effort": 6
            }
        }
        recommendations.append(industry_rec)
    
    return recommendations

def generate_engagement_recommendations(data):
    """
    Generate engagement opportunity recommendations
    
    Args:
        data (pd.DataFrame): DataFrame containing social media trend data
        
    Returns:
        list: List of engagement opportunity recommendations
    """
    # Get top hashtags
    if 'hashtags' in data.columns:
        if isinstance(data['hashtags'].iloc[0], list):
            # If hashtags are stored as lists
            all_hashtags = [tag for tags_list in data['hashtags'] for tag in tags_list]
            hashtag_counts = pd.Series(all_hashtags).value_counts().head(5).index.tolist()
        else:
            # If hashtags are stored as strings
            hashtag_counts = data['hashtags'].value_counts().head(5).index.tolist()
    else:
        hashtag_counts = ["#trending", "#viral", "#popular", "#content", "#socialmedia"]
    
    # Create recommendations list
    recommendations = []
    
    # Add recommendation about hashtags
    if hashtag_counts:
        hashtag_rec = {
            "title": "Utilize trending hashtags strategically",
            "description": "Incorporating trending hashtags can significantly increase your content's discoverability, but they should be relevant to your content.",
            "action_steps": [
                f"Include {', '.join(hashtag_counts[:3])} in your upcoming posts",
                "Research hashtag performance before using them",
                "Use a mix of trending and niche hashtags",
                "Don't overuse hashtags - focus on the most relevant ones"
            ],
            "metrics": {
                "relevance": 9,
                "potential_reach": 30000,
                "effort": 3
            }
        }
        recommendations.append(hashtag_rec)
    
    # Add recommendation about conversation participation
    convo_rec = {
        "title": "Join trending conversations authentically",
        "description": "Participating in trending conversations can increase visibility, but authenticity is key to avoid seeming opportunistic.",
        "action_steps": [
            "Monitor trending topics related to your industry",
            "Contribute meaningful insights to ongoing conversations",
            "Ask questions to encourage engagement",
            "Respond promptly to comments and mentions",
            "Create conversation starters related to trending topics"
        ],
        "metrics": {
            "relevance": 8,
            "potential_reach": 15000,
            "effort": 7
        }
    }
    recommendations.append(convo_rec)
    
    # Add recommendation about collaboration
    collab_rec = {
        "title": "Leverage collaboration opportunities",
        "description": "Collaborating with other creators or brands can help you tap into new audiences and increase engagement.",
        "action_steps": [
            "Identify potential collaborators in your niche or adjacent niches",
            "Propose mutually beneficial collaboration ideas",
            "Create co-branded content that aligns with current trends",
            "Cross-promote content across your platforms",
            "Analyze performance of collaborative content to refine future approaches"
        ],
        "metrics": {
            "relevance": 7,
            "potential_reach": 25000,
            "effort": 8
        }
    }
    recommendations.append(collab_rec)
    
    # Add recommendation about user-generated content
    ugc_rec = {
        "title": "Encourage user-generated content",
        "description": "User-generated content increases engagement and creates a sense of community while providing authentic content.",
        "action_steps": [
            "Create branded hashtags for users to tag their content",
            "Run contests or challenges related to trending topics",
            "Feature user content on your platforms (with permission)",
            "Respond to and engage with user-generated content",
            "Provide clear guidelines for the type of content you're looking for"
        ],
        "metrics": {
            "relevance": 8,
            "potential_reach": 20000,
            "effort": 6
        }
    }
    recommendations.append(ugc_rec)
    
    return recommendations

def generate_platform_recommendations(data):
    """
    Generate platform-specific recommendations
    
    Args:
        data (pd.DataFrame): DataFrame containing social media trend data
        
    Returns:
        list: List of platform-specific recommendations
    """
    # Get platforms from data
    platforms = data['platform'].unique() if 'platform' in data.columns else ["Twitter", "Instagram", "TikTok"]
    
    # Create recommendations list
    recommendations = []
    
    # Platform-specific recommendations
    platform_strategies = {
        "Twitter": {
            "title": "Twitter Strategy: Leverage real-time trends",
            "description": "Twitter excels at real-time conversation and trending topics. Capitalize on this by engaging with current events and trending hashtags.",
            "action_steps": [
                "Monitor Twitter's trending topics daily",
                "Join conversations with thoughtful responses, not just self-promotion",
                "Use Twitter threads for in-depth analysis of trending topics",
                "Incorporate trending hashtags when relevant",
                "Increase posting frequency during peak trending periods"
            ]
        },
        "Instagram": {
            "title": "Instagram Strategy: Focus on visual storytelling",
            "description": "Instagram is a visual platform where aesthetic consistency and storytelling drive engagement with trending content.",
            "action_steps": [
                "Create visually cohesive content related to trending topics",
                "Use Instagram Stories for behind-the-scenes and time-sensitive trend content",
                "Create Instagram Guides to curate trend-related content",
                "Utilize Instagram Reels to capitalize on short-form video trends",
                "Incorporate trending audio and effects in your content"
            ]
        },
        "TikTok": {
            "title": "TikTok Strategy: Embrace trend participation",
            "description": "TikTok is driven by trends and challenges. Participating in these trends can significantly increase visibility and follower growth.",
            "action_steps": [
                "Monitor the Discover page for emerging trends",
                "Put your unique spin on trending challenges or formats",
                "Use trending sounds and effects in your videos",
                "Post consistently to improve algorithm visibility",
                "Analyze trending content structure and adapt it for your niche"
            ]
        }
    }
    
    # Add recommendations for each platform in the data
    for platform in platforms:
        if platform in platform_strategies:
            rec = platform_strategies[platform]
            rec["metrics"] = {
                "relevance": 9,
                "potential_reach": 30000,
                "effort": 7
            }
            recommendations.append(rec)
    
    # Add cross-platform strategy recommendation
    cross_platform_rec = {
        "title": "Implement a cross-platform strategy",
        "description": "Different platforms reach different audiences. A coordinated cross-platform approach can maximize reach and engagement.",
        "action_steps": [
            "Maintain consistent branding across platforms while adapting content formats",
            "Create a content calendar that coordinates messaging across platforms",
            "Drive traffic between your platforms through cross-promotion",
            "Analyze which content performs best on each platform",
            "Prioritize platforms based on audience engagement and business goals"
        ],
        "metrics": {
            "relevance": 8,
            "potential_reach": 35000,
            "effort": 8
        }
    }
    recommendations.append(cross_platform_rec)
    
    # Add recommendation about emerging platforms if relevant
    emerging_platforms_rec = {
        "title": "Explore emerging platform opportunities",
        "description": "New and emerging platforms often offer less competition and higher organic reach. Consider establishing an early presence on these platforms.",
        "action_steps": [
            "Research user demographics of emerging platforms",
            "Test content formats on new platforms with growing user bases",
            "Adapt your content strategy to each platform's unique features",
            "Monitor performance to determine which platforms warrant continued investment",
            "Balance resources between established and emerging platforms"
        ],
        "metrics": {
            "relevance": 6,
            "potential_reach": 15000,
            "effort": 7
        }
    }
    recommendations.append(emerging_platforms_rec)
    
    return recommendations

def generate_custom_recommendations(data, industry=None, platform=None):
    """
    Generate custom recommendations based on specific industry and platform
    
    Args:
        data (pd.DataFrame): DataFrame containing social media trend data
        industry (str, optional): Industry to filter recommendations for
        platform (str, optional): Platform to filter recommendations for
        
    Returns:
        list: List of custom recommendations
    """
    # Filter data if industry or platform specified
    filtered_data = data.copy()
    
    if industry and 'industry' in filtered_data.columns:
        filtered_data = filtered_data[filtered_data['industry'] == industry]
    
    if platform and 'platform' in filtered_data.columns:
        filtered_data = filtered_data[filtered_data['platform'] == platform]
    
    # Get top trends from filtered data
    if not filtered_data.empty:
        top_trends = filtered_data.groupby('trend').agg({
            'engagement': 'sum',
            'growth_rate': 'mean'
        }).sort_values('engagement', ascending=False).head(3).index.tolist()
    else:
        top_trends = []
    
    # Create recommendations list
    recommendations = []
    
    # Industry-specific recommendations
    industry_specific = {
        "Technology": {
            "title": "Tech Industry: Focus on educational content",
            "description": "In the technology sector, educational content that explains complex concepts performs exceptionally well.",
            "action_steps": [
                "Create how-to guides and tutorials related to trending tech topics",
                "Develop infographics that simplify technical concepts",
                "Start conversations about ethical implications of new technologies",
                "Share insights about the future of technology in your niche",
                "Analyze and comment on major tech news and product launches"
            ]
        },
        "Fashion": {
            "title": "Fashion Industry: Emphasize sustainability narratives",
            "description": "Sustainability is a major trend in fashion. Highlighting sustainable practices can resonate with conscious consumers.",
            "action_steps": [
                "Showcase sustainable materials and production methods",
                "Create content about ethical fashion choices",
                "Highlight the longevity and versatility of pieces",
                "Partner with sustainable brands or initiatives",
                "Educate followers about reducing fashion waste"
            ]
        },
        "Entertainment": {
            "title": "Entertainment Industry: Leverage fan communities",
            "description": "Entertainment trends are driven by passionate fan communities. Engaging with these communities can amplify reach.",
            "action_steps": [
                "Create content analyzing trending shows, movies, or music",
                "Develop reaction content to new releases",
                "Host discussions about popular entertainment topics",
                "Create themed content around major entertainment events",
                "Collaborate with fan accounts and community leaders"
            ]
        }
    }
    
    # Add industry-specific recommendation if available
    if industry and industry in industry_specific:
        rec = industry_specific[industry]
        rec["metrics"] = {
            "relevance": 9,
            "potential_reach": 25000,
            "effort": 6
        }
        recommendations.append(rec)
    
    # Add trend-specific recommendation if available
    if top_trends:
        trend_rec = {
            "title": f"Capitalize on '{top_trends[0]}' trend",
            "description": f"The '{top_trends[0]}' trend is showing significant engagement in your selected filters. Creating content around this trend can increase visibility.",
            "action_steps": [
                f"Research the origins and current state of the '{top_trends[0]}' trend",
                "Create content that adds a unique perspective to this trend",
                "Analyze what content about this trend is performing well",
                "Develop a multi-post strategy around this trend",
                "Monitor engagement to determine when to pivot to new trends"
            ],
            "metrics": {
                "relevance": 9,
                "potential_reach": filtered_data[filtered_data['trend'] == top_trends[0]]['engagement'].sum() if 'trend' in filtered_data.columns else 15000,
                "effort": 5
            }
        }
        recommendations.append(trend_rec)
    
    return recommendations
