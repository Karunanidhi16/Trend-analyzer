import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import base64

# Import custom modules
from trend_analyzer import analyze_trends, get_trending_hashtags, get_trending_topics
from sentiment_analyzer import analyze_sentiment, get_sentiment_distribution
from data_fetcher import fetch_social_media_data, fetch_trending_images
from recommendation_engine import generate_recommendations
from utils import filter_by_industry, get_growth_forecast

# Set page config
st.set_page_config(
    page_title="TrendSpotter AI",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load custom CSS for better icon rendering and enhanced styling
try:
    with open('style.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
except Exception as e:
    st.warning(f"Could not load custom CSS file: {e}")

# Load custom CSS
try:
    with open('.streamlit/style.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
except FileNotFoundError:
    st.warning("Custom CSS file not found. Using default styling.")

# Add JavaScript for interactive elements and animations
st.markdown("""
<script>
document.addEventListener('DOMContentLoaded', (event) => {
    // Add hover effects to cards
    const cards = document.querySelectorAll('.card, .image-card');
    cards.forEach(card => {
        card.addEventListener('mouseenter', () => {
            card.style.transform = 'translateY(-4px)';
            card.style.boxShadow = '0 10px 15px rgba(0,0,0,0.1)';
        });
        card.addEventListener('mouseleave', () => {
            card.style.transform = 'translateY(0)';
            card.style.boxShadow = '0 1px 3px rgba(0,0,0,0.05)';
        });
    });
    
    // Animate elements when they come into view
    const animateOnScroll = () => {
        const elements = document.querySelectorAll('.animate-on-scroll');
        elements.forEach(element => {
            const position = element.getBoundingClientRect().top;
            const screenPosition = window.innerHeight / 1.3;
            
            if (position < screenPosition) {
                element.classList.add('animate-slideInUp');
                element.style.opacity = '1';
            }
        });
    };
    
    window.addEventListener('scroll', animateOnScroll);
    animateOnScroll(); // Run once on load
    
    // Enable category expansion
    const categoryHeaders = document.querySelectorAll('.category-header');
    categoryHeaders.forEach(header => {
        header.addEventListener('click', () => {
            const content = header.nextElementSibling;
            if (content.classList.contains('show')) {
                content.classList.remove('show');
            } else {
                content.classList.add('show');
            }
        });
    });
});
</script>
""", unsafe_allow_html=True)

# Add CSS for category color scheme
category_colors = {
    'Politics': {'primary': '#E63946', 'secondary': '#1D3557'},
    'Celebrity': {'primary': '#FFD700', 'secondary': '#FF4500'},
    'Technology': {'primary': '#3A86FF', 'secondary': '#38B000'},
    'Fashion': {'primary': '#FF006E', 'secondary': '#8338EC'},
    'Food': {'primary': '#FB8B24', 'secondary': '#06D6A0'},
    'Travel': {'primary': '#0096C7', 'secondary': '#FFDD00'},
    'Fitness': {'primary': '#9D4EDD', 'secondary': '#00B4D8'},
    'Beauty': {'primary': '#FF70A6', 'secondary': '#56CFE1'},
    'Business': {'primary': '#22223B', 'secondary': '#4A4E69'},
    'Education': {'primary': '#386641', 'secondary': '#A7C957'}
}

# Initialize session state variables if they don't exist
if 'selected_platform' not in st.session_state:
    st.session_state.selected_platform = 'All Platforms'
if 'selected_industry' not in st.session_state:
    st.session_state.selected_industry = 'All Industries'
if 'date_range' not in st.session_state:
    st.session_state.date_range = 7  # Default to 7 days
if 'search_term' not in st.session_state:
    st.session_state.search_term = ''

def render_navbar():
    """Render a custom navbar using Streamlit components"""
    # Add CSS styling
    st.markdown("""
    <style>
    .navbar {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 1rem;
        border-bottom: 1px solid #e2e8f0;
        background-color: white;
        margin: -60px -80px 0 -80px;
        padding-left: 80px;
        padding-right: 80px;
    }
    .logo-container {
        display: flex;
        align-items: center;
    }
    .logo-text {
        font-size: 1.5rem;
        font-weight: 700;
        color: #2563eb;
        margin-right: 0.5rem;
    }
    .logo-badge {
        background-color: #14b8a6;
        color: white;
        font-size: 0.75rem;
        padding: 0.125rem 0.5rem;
        border-radius: 9999px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Create the navbar with columns
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        st.markdown("""
        <div class="logo-container">
            <div class="logo-text">TrendSpotter</div>
            <div class="logo-badge">AI</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        # Simple button row using Streamlit components
        button_cols = st.columns(3)
        with button_cols[0]:
            st.button("🔔", key="notification_btn")
        with button_cols[1]:
            st.button("⚙️", key="settings_btn")
        with button_cols[2]:
            st.button("👤", key="profile_btn")

def render_header():
    """Render app header with stats cards"""
    # App header and stats dashboard with animations
    st.markdown(
        '<h1 class="animate-fadeIn" style="color: #0F172A;">Social Media Trend Analysis</h1>',
        unsafe_allow_html=True
    )
    st.markdown(
        '<p class="animate-slideInUp" style="font-size: 1.1rem; color: #64748B; margin-bottom: 1.5rem;">'
        'Analyze emerging trends and get actionable insights for your content strategy'
        '</p>',
        unsafe_allow_html=True
    )
    
    # Enhanced search bar with animation and styling
    st.markdown("""
    <style>
    .search-container {
        background-color: white;
        border-radius: 0.75rem;
        padding: 0.75rem 1rem;
        margin-bottom: 2rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        border: 1px solid #e2e8f0;
        display: flex;
        align-items: center;
        animation: fadeIn 0.5s ease-in-out;
    }
    .search-icon {
        color: #94a3b8;
        margin-right: 0.5rem;
        font-size: 1.25rem;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Search bar - use Streamlit's native components with styled container
    search_col1, search_col2 = st.columns([3, 1])
    with search_col1:
        # We'll use the built-in text input but with enhanced styling
        st.markdown('<div class="search-container animate-slideInUp"><span class="search-icon">🔍</span>', unsafe_allow_html=True)
        search_term = st.text_input("Search for trends, hashtags, or topics...", value=st.session_state.search_term, label_visibility="collapsed")
        st.markdown('</div>', unsafe_allow_html=True)
        st.session_state.search_term = search_term

def main():
    # Render custom navbar and header
    render_navbar()
    render_header()
    
    # Enhanced sidebar for filters and controls
    with st.sidebar:
        # Add custom styling for the sidebar
        st.markdown("""
        <style>
        [data-testid="stSidebar"] {
            background-color: white;
            border-right: 1px solid #e2e8f0;
            padding-top: 1rem;
        }
        .sidebar-title {
            color: #0F172A;
            font-weight: 600;
            font-size: 1.25rem;
            margin-bottom: 1.5rem;
            padding-bottom: 0.5rem;
            border-bottom: 1px solid #e2e8f0;
        }
        .filter-section {
            background-color: #f8fafc;
            border-radius: 0.75rem;
            padding: 1rem;
            margin-bottom: 1.5rem;
            border: 1px solid #e2e8f0;
        }
        .filter-label {
            font-weight: 600;
            color: #475569;
            margin-bottom: 0.5rem;
            font-size: 0.9rem;
        }
        .sidebar-footer {
            position: absolute;
            bottom: 1rem;
            left: 1rem;
            right: 1rem;
            text-align: center;
            color: #94a3b8;
            font-size: 0.8rem;
            padding-top: 1rem;
            border-top: 1px solid #e2e8f0;
        }
        </style>
        """, unsafe_allow_html=True)
        
        # Enhanced header with icon
        st.markdown('<div class="sidebar-title">🎛️ Filters & Controls</div>', unsafe_allow_html=True)
        
        # Platform filter section with platform-specific colors
        st.markdown('<div class="filter-section">', unsafe_allow_html=True)
        st.markdown('<div class="filter-label">🌐 Platform</div>', unsafe_allow_html=True)
        
        # Platform selection with enhanced list including icons
        platform_options = ['All Platforms', 'Twitter', 'Instagram', 'TikTok', 'YouTube', 'LinkedIn']
        platform_icons = {
            'All Platforms': '🌐',
            'Twitter': '🐦',
            'Instagram': '📸',
            'TikTok': '📱',
            'YouTube': '🎬',
            'LinkedIn': '💼'
        }
        
        # Format platform options with icons
        platform_display = [f"{platform_icons[p]} {p}" for p in platform_options]
        
        selected_platform_idx = platform_options.index(st.session_state.selected_platform) if st.session_state.selected_platform in platform_options else 0
        selected_platform_display = st.selectbox(
            "Platform",
            platform_display,
            index=selected_platform_idx,
            label_visibility="collapsed"
        )
        
        # Extract the actual platform name without the icon
        selected_platform = platform_options[platform_display.index(selected_platform_display)]
        st.session_state.selected_platform = selected_platform
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Industry filter section
        st.markdown('<div class="filter-section">', unsafe_allow_html=True)
        st.markdown('<div class="filter-label">🏢 Industry</div>', unsafe_allow_html=True)
        
        # Industry selection with icons
        industry_options = [
            'All Industries', 'Technology', 'Fashion', 'Entertainment', 
            'Food', 'Travel', 'Fitness', 'Beauty', 'Business', 'Education'
        ]
        
        industry_icons = {
            'All Industries': '🏢',
            'Technology': '💻',
            'Fashion': '👗',
            'Entertainment': '🎭',
            'Food': '🍔',
            'Travel': '✈️',
            'Fitness': '💪',
            'Beauty': '💄',
            'Business': '📈',
            'Education': '🎓'
        }
        
        # Format industry options with icons
        industry_display = [f"{industry_icons[i]} {i}" for i in industry_options]
        
        selected_industry_idx = industry_options.index(st.session_state.selected_industry) if st.session_state.selected_industry in industry_options else 0
        selected_industry_display = st.selectbox(
            "Industry",
            industry_display,
            index=selected_industry_idx,
            label_visibility="collapsed"
        )
        
        # Extract the actual industry name without the icon
        selected_industry = industry_options[industry_display.index(selected_industry_display)]
        st.session_state.selected_industry = selected_industry
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Time period section
        st.markdown('<div class="filter-section">', unsafe_allow_html=True)
        st.markdown('<div class="filter-label">⏱️ Time Period</div>', unsafe_allow_html=True)
        
        # Date range selection
        date_range_options = {
            '24 Hours': 1,
            '3 Days': 3,
            '7 Days': 7,
            '2 Weeks': 14,
            '1 Month': 30
        }
        
        selected_date_range = st.selectbox(
            "Time Period",
            list(date_range_options.keys()),
            index=list(date_range_options.values()).index(st.session_state.date_range),
            label_visibility="collapsed"
        )
        st.session_state.date_range = date_range_options[selected_date_range]
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Create a stylized refresh button
        st.markdown("""
        <style>
        div[data-testid="stButton"] > button {
            background-color: #2563EB;
            color: white;
            font-weight: 500;
            border-radius: 0.5rem;
            padding: 0.5rem 1rem;
            width: 100%;
            transition: all 0.2s ease;
        }
        div[data-testid="stButton"] > button:hover {
            background-color: #1d4ed8;
            transform: translateY(-2px);
            box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1), 0 2px 4px -1px rgba(0,0,0,0.06);
        }
        div[data-testid="stButton"] > button:active {
            transform: translateY(0);
        }
        </style>
        """, unsafe_allow_html=True)
        
        # Refresh button
        if st.button("🔄 Refresh Data"):
            st.rerun()
            
        # Add footer with version info and last updated
        st.markdown(
            '<div class="sidebar-footer">TrendSpotter AI v1.0<br>Last updated: April 5, 2025</div>',
            unsafe_allow_html=True
        )
    
    # Main content area - use tabs for organization
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Trending Now", "Trending Images", "Sentiment Analysis", "Growth Forecast", "Recommendations"])
    
    # Fetch data based on filters
    with st.spinner("Fetching social media data..."):
        try:
            data = fetch_social_media_data(
                platform=st.session_state.selected_platform,
                days=st.session_state.date_range
            )
            
            # Filter data by industry if needed
            if st.session_state.selected_industry != 'All Industries':
                data = filter_by_industry(data, st.session_state.selected_industry)
            
            # If no data available after filtering
            if data.empty:
                st.warning(f"No data available for the selected filters. Try changing your selection.")
                return
                
        except Exception as e:
            st.error(f"Error fetching data: {str(e)}")
            return
    
    # Tab 1: Trending Now
    with tab1:
        st.markdown('<h2 class="animate-fadeIn">🔥 Currently Trending 🔥</h2>', unsafe_allow_html=True)
        
        # Add colorful explanation with emoji icons
        st.markdown("""
        <div class="animate-slideInUp" style="background-color: white; border-radius: 0.75rem; 
             padding: 1rem; margin-bottom: 1.5rem; border: 1px solid #e2e8f0;">
            <p style="margin: 0; color: #334155;">
                <span style="font-weight: 600; color: #ef4444;">🔍 Trending analysis</span> shows what's 
                <span style="color: #ef4444; font-weight: 600;">hot</span> across social media right now! 
                <span style="color: #8b5cf6; font-weight: 600;">📱 Browse trending content</span> from all platforms.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Enhanced wave design with news ticker on waves
        st.markdown("""
        <style>
        /* Enhanced wave animation and design */
        .wave-container {
            position: relative;
            height: 150px;
            overflow: hidden;
            margin: -20px -20px 20px -20px;
            background: linear-gradient(180deg, rgba(59,130,246,0.1) 0%, rgba(59,130,246,0) 100%);
        }
        .wave {
            position: absolute;
            bottom: 0;
            left: 0;
            width: 100%;
            height: 120px;
            background: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 1440 320'%3E%3Cpath fill='%232563EB' fill-opacity='1' d='M0,128L48,122.7C96,117,192,107,288,101.3C384,96,480,96,576,117.3C672,139,768,181,864,181.3C960,181,1056,139,1152,122.7C1248,107,1344,117,1392,122.7L1440,128L1440,320L1392,320C1344,320,1248,320,1152,320C1056,320,960,320,864,320C768,320,672,320,576,320C480,320,384,320,288,320C192,320,96,320,48,320L0,320Z'%3E%3C/path%3E%3C/svg%3E");
            background-repeat: repeat-x;
            background-size: 1440px 120px;
            animation: wave-animation 20s cubic-bezier(0.36, 0.45, 0.63, 0.53) infinite;
            filter: drop-shadow(0 0 5px rgba(37, 99, 235, 0.3));
        }
        .wave:nth-child(2) {
            bottom: 10px;
            opacity: 0.7;
            height: 140px;
            background: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 1440 320'%3E%3Cpath fill='%238B5CF6' fill-opacity='0.8' d='M0,96L48,112C96,128,192,160,288,170.7C384,181,480,171,576,144C672,117,768,75,864,69.3C960,64,1056,96,1152,112C1248,128,1344,128,1392,128L1440,128L1440,320L1392,320C1344,320,1248,320,1152,320C1056,320,960,320,864,320C768,320,672,320,576,320C480,320,384,320,288,320C192,320,96,320,48,320L0,320Z'%3E%3C/path%3E%3C/svg%3E");
            animation: wave-animation 15s cubic-bezier(0.36, 0.45, 0.63, 0.53) infinite;
            filter: drop-shadow(0 0 5px rgba(139, 92, 246, 0.3));
        }
        .wave:nth-child(3) {
            bottom: 15px;
            opacity: 0.6;
            height: 130px;
            background: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 1440 320'%3E%3Cpath fill='%2310B981' fill-opacity='0.6' d='M0,64L48,80C96,96,192,128,288,128C384,128,480,96,576,90.7C672,85,768,107,864,138.7C960,171,1056,213,1152,213.3C1248,213,1344,171,1392,149.3L1440,128L1440,320L1392,320C1344,320,1248,320,1152,320C1056,320,960,320,864,320C768,320,672,320,576,320C480,320,384,320,288,320C192,320,96,320,48,320L0,320Z'%3E%3C/path%3E%3C/svg%3E");
            animation: wave-animation 12s cubic-bezier(0.445, 0.05, 0.55, 0.95) infinite;
            filter: drop-shadow(0 0 5px rgba(16, 185, 129, 0.3));
        }
        .wave:nth-child(4) {
            bottom: 0px;
            opacity: 0.3;
            height: 150px;
            background: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 1440 320'%3E%3Cpath fill='%23F43F5E' fill-opacity='0.5' d='M0,32L48,58.7C96,85,192,139,288,149.3C384,160,480,128,576,112C672,96,768,96,864,122.7C960,149,1056,203,1152,213.3C1248,224,1344,192,1392,176L1440,160L1440,320L1392,320C1344,320,1248,320,1152,320C1056,320,960,320,864,320C768,320,672,320,576,320C480,320,384,320,288,320C192,320,96,320,48,320L0,320Z'%3E%3C/path%3E%3C/svg%3E");
            animation: wave-animation 8s cubic-bezier(0.445, 0.05, 0.55, 0.95) infinite;
            filter: drop-shadow(0 0 5px rgba(244, 63, 94, 0.3));
        }
        
        /* Enhanced wave animation */
        @keyframes wave-animation {
            0% { background-position-x: 0; }
            50% { background-position-x: 720px; }
            100% { background-position-x: 1440px; }
        }
        
        /* News ticker directly on waves */
        .wave-news-ticker {
            position: relative;
            top: 40%;
            left: 0;
            width: 100%;
            white-space: nowrap;
            animation: wave-ticker 25s linear infinite;
            display: flex;
            align-items: center;
            height: 40px;
            z-index: 5;
        }
        .wave-news-ticker-2 {
            animation-duration: 30s;
            animation-delay: -8s;
            top: 35%;
        }
        .wave-news-ticker-3 {
            animation-duration: 35s;
            animation-delay: -15s;
            top: 30%;
        }
        .wave-news-ticker span {
            display: inline-flex;
            align-items: center;
            padding: 5px 15px;
            margin: 0 20px;
            font-weight: 600;
            font-size: 0.9rem;
            color: white;
            background-color: rgba(0, 0, 0, 0.3);
            backdrop-filter: blur(5px);
            border-radius: 30px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3);
        }
        @keyframes wave-ticker {
            0% { transform: translateX(100%); }
            100% { transform: translateX(-200%); }
        }
        
        /* Scroll animations with enhanced effects */
        .scroll-color-change {
            transition: all 0.8s ease;
        }
        
        /* Enhanced page transition effect */
        .page-transition {
            animation: fadeScale 0.7s cubic-bezier(0.165, 0.84, 0.44, 1);
        }
        @keyframes fadeScale {
            from {
                opacity: 0;
                transform: scale(0.95) translateY(10px);
            }
            to {
                opacity: 1;
                transform: scale(1) translateY(0);
            }
        }
        
        /* Metrics styling */
        .metrics-container {
            display: flex;
            gap: 1rem;
            margin-bottom: 1.5rem;
        }
        .metric-card {
            flex: 1;
            background-color: white;
            border-radius: 0.75rem;
            padding: 1.25rem;
            border: 1px solid #e2e8f0;
            text-align: center;
            position: relative;
            overflow: hidden;
            transition: all 0.3s ease;
            animation: pulse-glow 3s infinite;
        }
        .metric-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1);
        }
        .metric-icon {
            font-size: 2rem;
            margin-bottom: 0.5rem;
        }
        .metric-value {
            font-size: 1.5rem;
            font-weight: 700;
            color: #0f172a;
            margin-bottom: 0.25rem;
        }
        .metric-label {
            color: #64748b;
            font-size: 0.875rem;
        }
        .fire-icon {
            color: #ef4444;
        }
        .engagement-icon {
            color: #8b5cf6;
        }
        .growth-icon {
            color: #10b981;
        }
        .metric-bg {
            position: absolute;
            top: -20px;
            right: -20px;
            font-size: 5rem;
            opacity: 0.05;
            transform: rotate(15deg);
        }
        
        @keyframes pulse-glow {
            0% { box-shadow: 0 0 0 0 rgba(37, 99, 235, 0); }
            70% { box-shadow: 0 0 0 10px rgba(37, 99, 235, 0.1); }
            100% { box-shadow: 0 0 0 0 rgba(37, 99, 235, 0); }
        }
        </style>
        
        <div class="wave-container">
            <div class="wave">
                <div class="wave-news-ticker">
                    <span>🔥 TikTok surpasses 2 billion downloads worldwide</span>
                    <span>📊 Instagram engagement rates drop 30% for business accounts</span>
                </div>
            </div>
            <div class="wave">
                <div class="wave-news-ticker wave-news-ticker-2">
                    <span>💼 LinkedIn reports 63% growth in content creation</span>
                    <span>📱 YouTube Shorts reaches 1.5 billion monthly active users</span>
                </div>
            </div>
            <div class="wave">
                <div class="wave-news-ticker wave-news-ticker-3">
                    <span>🚀 Twitter sees record growth in video content engagement</span>
                    <span>📈 Facebook Meta Business Suite launches new analytics features</span>
                </div>
            </div>
            <div class="wave"></div>
        </div>
        """, unsafe_allow_html=True)
        
        # Enhanced colorful metrics row with icons
        fire_icon = "🔥"
        engagement_icon = "💬"
        growth_icon = "📈"
        trend_count = len(data)
        avg_engagement = f"{int(data['engagement'].mean()):,}"
        top_growth = f"{data['growth_rate'].max():.1f}"
        
        st.markdown(f"""
        <div class="metrics-container animate-slideInUp page-transition">
            <div class="metric-card">
                <div class="metric-bg">{fire_icon}</div>
                <div class="metric-icon fire-icon">{fire_icon}</div>
                <div class="metric-value">{trend_count}</div>
                <div class="metric-label">Active Trends</div>
            </div>
            
            <div class="metric-card">
                <div class="metric-bg">{engagement_icon}</div>
                <div class="metric-icon engagement-icon">{engagement_icon}</div>
                <div class="metric-value">{avg_engagement}</div>
                <div class="metric-label">Avg. Engagement</div>
            </div>
            
            <div class="metric-card">
                <div class="metric-bg">{growth_icon}</div>
                <div class="metric-icon growth-icon">{growth_icon}</div>
                <div class="metric-value">{top_growth}%</div>
                <div class="metric-label">Highest Growth Rate</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Add scroll color change effect
        st.markdown("""
        <script>
            // Change background color on scroll
            document.addEventListener('DOMContentLoaded', function() {
                window.addEventListener('scroll', function() {
                    var scrollPosition = window.scrollY;
                    var body = document.body;
                    
                    if (scrollPosition > 300) {
                        body.style.backgroundColor = '#f0f9ff'; // Light blue tint
                    } else if (scrollPosition > 200) {
                        body.style.backgroundColor = '#f0fdf4'; // Light green tint
                    } else if (scrollPosition > 100) {
                        body.style.backgroundColor = '#fef2f2'; // Light red tint
                    } else {
                        body.style.backgroundColor = '#f8fafc'; // Original background
                    }
                });
            });
        </script>
        """, unsafe_allow_html=True)
        
        # Enhanced trending hashtags and topics with colorful icons
        st.markdown("""
        <style>
        .trend-section-header {
            display: flex;
            align-items: center;
            margin-bottom: 1rem;
            color: #0f172a;
            font-weight: 600;
            font-size: 1.25rem;
        }
        .trend-icon {
            margin-right: 0.5rem;
            font-size: 1.5rem;
        }
        .hashtag-icon {
            color: #2563eb;
        }
        .topic-icon {
            color: #8b5cf6;
        }
        .trend-card {
            background-color: white;
            border-radius: 0.75rem;
            border: 1px solid #e2e8f0;
            padding: 1rem;
            margin-bottom: 1.25rem;
            box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        }
        </style>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Enhanced header with hashtag icon
            st.markdown('<div class="trend-section-header"><span class="trend-icon hashtag-icon">#️⃣</span> Top Trending Hashtags</div>', unsafe_allow_html=True)
            
            # Get trending hashtags
            trending_hashtags = get_trending_hashtags(data)
            
            # Add trending hashtags card
            st.markdown('<div class="trend-card">', unsafe_allow_html=True)
            
            # Create a bar chart for hashtags with vibrant colors
            fig = px.bar(
                trending_hashtags.head(10),
                x='engagement',
                y='hashtag',
                orientation='h',
                title="Top Hashtags by Engagement 🔥",
                color='engagement',
                color_continuous_scale='Plasma'  # Changed to more vibrant color scale
            )
            fig.update_layout(
                yaxis={'categoryorder': 'total ascending'},
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                title_font=dict(size=18, color='#0f172a'),
                showlegend=False,
                margin=dict(l=10, r=10, t=40, b=10)
            )
            # Make y-axis labels start with # symbol
            fig.update_yaxes(ticktext=['#' + h for h in trending_hashtags.head(10)['hashtag'].tolist()],
                           tickvals=trending_hashtags.head(10)['hashtag'].tolist())
            st.plotly_chart(fig, use_container_width=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
            
        with col2:
            # Enhanced header with topic icon
            st.markdown('<div class="trend-section-header"><span class="trend-icon topic-icon">🔍</span> Trending Topics</div>', unsafe_allow_html=True)
            
            # Get trending topics
            trending_topics = get_trending_topics(data)
            
            # Add trending topics card
            st.markdown('<div class="trend-card">', unsafe_allow_html=True)
            
            # Add topic icons based on category
            topic_icons = {
                'Technology': '💻',
                'Fashion': '👗',
                'Entertainment': '🎭',
                'Food': '🍔',
                'Travel': '✈️',
                'Fitness': '💪',
                'Beauty': '💄',
                'Business': '📈',
                'Education': '🎓',
                'Politics': '🏛️',
                'Sports': '⚽',
                'Music': '🎵',
                'Movies': '🎬',
                'Gaming': '🎮',
                'Health': '🩺'
            }
            
            # Create a treemap for topics with improved styling
            fig = px.treemap(
                trending_topics.head(10),
                path=['topic'],
                values='count',
                color='growth_rate',
                hover_data=['count', 'growth_rate'],
                color_continuous_scale='RdBu',
                title="Hot Topics by Volume & Growth 📈"
            )
            
            # Update layout with better colors and styling
            fig.update_layout(
                title_font=dict(size=18, color='#0f172a'),
                margin=dict(l=10, r=10, t=40, b=10)
            )
            
            # Add labels with icons if possible
            for i, topic in enumerate(trending_topics.head(10)['topic']):
                for key in topic_icons:
                    if key.lower() in topic.lower():
                        # If we could modify the plot more directly, we would add icons here
                        break
            
            st.plotly_chart(fig, use_container_width=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
            
        # Add colorful trend chips with symbols
        st.markdown("""
        <style>
        .trend-chips-container {
            display: flex;
            flex-wrap: wrap;
            gap: 0.5rem;
            margin-bottom: 1.5rem;
        }
        .trend-chip {
            display: inline-flex;
            align-items: center;
            padding: 0.5rem 0.75rem;
            border-radius: 9999px;
            font-size: 0.875rem;
            font-weight: 500;
            color: white;
            background-color: #2563eb;
            transition: all 0.2s ease;
            cursor: pointer;
        }
        .trend-chip:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        }
        .trend-chip-icon {
            margin-right: 0.375rem;
        }
        .trend-chip-fire { background-color: #ef4444; }
        .trend-chip-new { background-color: #10b981; }
        .trend-chip-popular { background-color: #8b5cf6; }
        .trend-chip-rising { background-color: #f59e0b; }
        .trend-chip-viral { background-color: #ec4899; }
        </style>
        
        <div class="trend-section-header"><span class="trend-icon">🏷️</span> Trending Tags</div>
        <div class="trend-chips-container animate-slideInUp">
            <div class="trend-chip trend-chip-fire"><span class="trend-chip-icon">🔥</span>BeReal</div>
            <div class="trend-chip trend-chip-popular"><span class="trend-chip-icon">💫</span>AIart</div>
            <div class="trend-chip trend-chip-new"><span class="trend-chip-icon">✨</span>NewMusic</div>
            <div class="trend-chip trend-chip-rising"><span class="trend-chip-icon">📈</span>StockTips</div>
            <div class="trend-chip trend-chip-viral"><span class="trend-chip-icon">🚀</span>MemeOfTheDay</div>
            <div class="trend-chip trend-chip-fire"><span class="trend-chip-icon">🎬</span>MovieNight</div>
            <div class="trend-chip trend-chip-popular"><span class="trend-chip-icon">🏋️</span>FitCheck</div>
            <div class="trend-chip trend-chip-new"><span class="trend-chip-icon">🍔</span>FoodieFinds</div>
            <div class="trend-chip trend-chip-rising"><span class="trend-chip-icon">🎮</span>GamingLife</div>
            <div class="trend-chip trend-chip-viral"><span class="trend-chip-icon">✈️</span>TravelGoals</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Enhanced timeline section with colorful icons
        st.markdown('<div class="trend-section-header"><span class="trend-icon" style="color: #2563eb;">📊</span> Trend Activity Timeline</div>', unsafe_allow_html=True)
        
        # Add timeline explanation
        st.markdown("""
        <div class="animate-slideInUp" style="background-color: white; border-radius: 0.75rem; 
             padding: 1rem; margin-bottom: 1.5rem; border: 1px solid #e2e8f0;">
            <p style="margin: 0; color: #334155;">
                <span style="font-weight: 600; color: #2563eb;">📈 Timeline analysis</span> shows how trends evolve across 
                platforms over time. Track which platforms lead trend cycles and predict what's coming next!
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Group data by date and platform
        timeline_data = analyze_trends(data)
        
        # Add trending timeline card
        st.markdown('<div class="trend-card">', unsafe_allow_html=True)
        
        # Create enhanced line chart for trend activity with platform-specific colors
        fig = px.line(
            timeline_data,
            x='date',
            y='volume',
            color='platform',
            title="Trend Volume by Platform 📈",
            labels={'volume': 'Trend Volume', 'date': 'Date'},
            color_discrete_map={
                'Instagram': '#E1306C',
                'YouTube': '#FF0000',
                'LinkedIn': '#0077B5',
                'TikTok': '#000000',
                'Twitter': '#1DA1F2',
                'Facebook': '#1877F2',
                'Pinterest': '#E60023',
                'Snapchat': '#FFFC00'
            }
        )
        
        # Enhance the line chart appearance
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            title_font=dict(size=18, color='#0f172a'),
            legend_title="Social Platforms",
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            ),
            margin=dict(l=10, r=10, t=60, b=10)
        )
        
        # Make lines thicker for better visibility
        fig.update_traces(line=dict(width=3))
        
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Add platform-specific trend indicators with emojis
        st.markdown("""
        <style>
        .platform-indicators {
            display: flex;
            flex-wrap: wrap;
            gap: 1rem;
            margin-bottom: 2rem;
        }
        .platform-indicator {
            flex: 1;
            min-width: 150px;
            background-color: white;
            padding: 1rem;
            border-radius: 0.75rem;
            box-shadow: 0 1px 3px rgba(0,0,0,0.05);
            border: 1px solid #e2e8f0;
            display: flex;
            flex-direction: column;
            align-items: center;
            transition: all 0.3s ease;
        }
        .platform-indicator:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 15px -3px rgba(0,0,0,0.1);
        }
        .platform-icon {
            font-size: 2rem;
            margin-bottom: 0.5rem;
        }
        .platform-name {
            font-weight: 600;
            margin-bottom: 0.25rem;
            color: #0f172a;
        }
        .platform-trend {
            display: flex;
            align-items: center;
            margin-top: 0.5rem;
            gap: 0.25rem;
        }
        .trending-up {
            color: #10b981;
        }
        .trending-down {
            color: #ef4444;
        }
        .instagram-color { color: #E1306C; }
        .twitter-color { color: #1DA1F2; }
        .tiktok-color { color: #000000; }
        .youtube-color { color: #FF0000; }
        </style>
        """, unsafe_allow_html=True)
        
        # Create platform indicators using columns for better layout control
        st.markdown('<div class="animate-slideInUp" style="margin-bottom: 2rem;">', unsafe_allow_html=True)
        platform_cols = st.columns(4)
        
        # Instagram
        with platform_cols[0]:
            st.markdown("""
            <div style="background-color: white; border-radius: 0.75rem; padding: 1rem; 
                 border: 1px solid #e2e8f0; height: 100%; text-align: center;">
                <div style="font-size: 2rem; color: #E1306C; margin-bottom: 0.5rem;">📸</div>
                <div style="font-weight: 600; font-size: 1rem; margin-bottom: 0.5rem;">Instagram</div>
                <div style="color: #10b981; display: flex; justify-content: center; align-items: center; gap: 0.25rem; margin-bottom: 0.5rem;">
                    <span>+12.3%</span>
                    <span>📈</span>
                </div>
                <div style="font-size: 0.8rem; color: #64748b;">Reels dominating</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Twitter
        with platform_cols[1]:
            st.markdown("""
            <div style="background-color: white; border-radius: 0.75rem; padding: 1rem; 
                 border: 1px solid #e2e8f0; height: 100%; text-align: center;">
                <div style="font-size: 2rem; color: #1DA1F2; margin-bottom: 0.5rem;">🐦</div>
                <div style="font-weight: 600; font-size: 1rem; margin-bottom: 0.5rem;">Twitter</div>
                <div style="color: #10b981; display: flex; justify-content: center; align-items: center; gap: 0.25rem; margin-bottom: 0.5rem;">
                    <span>+8.7%</span>
                    <span>📈</span>
                </div>
                <div style="font-size: 0.8rem; color: #64748b;">News trends</div>
            </div>
            """, unsafe_allow_html=True)
        
        # TikTok
        with platform_cols[2]:
            st.markdown("""
            <div style="background-color: white; border-radius: 0.75rem; padding: 1rem; 
                 border: 1px solid #e2e8f0; height: 100%; text-align: center;">
                <div style="font-size: 2rem; color: #000000; margin-bottom: 0.5rem;">📱</div>
                <div style="font-weight: 600; font-size: 1rem; margin-bottom: 0.5rem;">TikTok</div>
                <div style="color: #10b981; display: flex; justify-content: center; align-items: center; gap: 0.25rem; margin-bottom: 0.5rem;">
                    <span>+23.9%</span>
                    <span>📈</span>
                </div>
                <div style="font-size: 0.8rem; color: #64748b;">Fastest growing</div>
            </div>
            """, unsafe_allow_html=True)
        
        # YouTube
        with platform_cols[3]:
            st.markdown("""
            <div style="background-color: white; border-radius: 0.75rem; padding: 1rem; 
                 border: 1px solid #e2e8f0; height: 100%; text-align: center;">
                <div style="font-size: 2rem; color: #FF0000; margin-bottom: 0.5rem;">🎬</div>
                <div style="font-weight: 600; font-size: 1rem; margin-bottom: 0.5rem;">YouTube</div>
                <div style="color: #ef4444; display: flex; justify-content: center; align-items: center; gap: 0.25rem; margin-bottom: 0.5rem;">
                    <span>-2.4%</span>
                    <span>📉</span>
                </div>
                <div style="font-size: 0.8rem; color: #64748b;">Shorts growth</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Add platform traffic data visualization (vertical bar chart)
        st.markdown("""
        <style>
        .platform-traffic {
            background-color: white;
            border-radius: 0.75rem;
            border: 1px solid #e2e8f0;
            padding: 1.5rem;
            margin-bottom: 2rem;
            box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        }
        .section-title {
            color: #0f172a;
            font-size: 1.25rem;
            font-weight: 600;
            margin-bottom: 1rem;
            display: flex;
            align-items: center;
        }
        .traffic-icon {
            color: #2563eb;
            margin-right: 0.5rem;
        }
        </style>
        
        <div class="platform-traffic animate-slideInUp">
            <div class="section-title"><span class="traffic-icon">👥</span> Platform Monthly Active Users</div>
        """, unsafe_allow_html=True)
        
        # Create a DataFrame for platform traffic data
        platform_traffic_data = pd.DataFrame({
            'platform': ['YouTube', 'Facebook', 'Instagram', 'TikTok', 'Twitter', 'LinkedIn', 'Pinterest', 'Snapchat'],
            'monthly_active_users': [2500, 2900, 1800, 1500, 450, 810, 480, 620],
            'color': ['#FF0000', '#1877F2', '#E1306C', '#000000', '#1DA1F2', '#0077B5', '#E60023', '#FFFC00']
        })
        
        # Create vertical bar chart for platform traffic
        fig = px.bar(
            platform_traffic_data,
            y='platform',
            x='monthly_active_users',
            orientation='h',
            height=500,  # Increased height
            title="Monthly Active Users by Platform (in millions)",
            color='platform',
            color_discrete_map=dict(zip(platform_traffic_data['platform'], platform_traffic_data['color']))
        )
        
        # Enhance the bar chart appearance
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            title_font=dict(size=20, color='#0f172a'),
            showlegend=False,
            xaxis_title="Monthly Active Users (millions)",
            yaxis_title=None,
            xaxis=dict(
                showgrid=True,
                gridcolor='rgba(0,0,0,0.05)'
            ),
            margin=dict(l=20, r=20, t=50, b=20)
        )
        
        # Add value labels to the bars
        fig.update_traces(
            texttemplate='%{x:,.0f}M',
            textposition='outside',
            textfont=dict(
                size=14,
                color='#0f172a'
            ),
            marker_line_color='white',
            marker_line_width=1,
            opacity=0.9,
            hovertemplate='<b>%{y}</b><br>Monthly Active Users: %{x:,.0f} million<extra></extra>'
        )
        
        # Show the chart
        st.plotly_chart(fig, use_container_width=True)
        
        # Add platform growth comparison with side groups
        st.markdown("""
        <div class="section-title"><span class="traffic-icon">📱</span> Platform Growth & Demographics</div>
        <div style="display: flex; gap: 1rem; margin-bottom: 1.5rem;">
            <!-- Main metrics section -->
            <div style="flex: 2; display: flex; flex-wrap: wrap; gap: 1rem;">
                <div style="flex: 1; min-width: 250px; background-color: #f8fafc; padding: 1rem; border-radius: 0.5rem; border: 1px solid #e2e8f0;">
                    <div style="font-weight: 600; color: #0f172a; margin-bottom: 0.5rem;">Age Demographics</div>
                    <div style="color: #64748b; font-size: 0.875rem;">
                        <div style="display: flex; justify-content: space-between; margin-bottom: 0.25rem;">
                            <span>TikTok:</span>
                            <span style="font-weight: 500; color: #0f172a;">Gen Z (60%)</span>
                        </div>
                        <div style="display: flex; justify-content: space-between; margin-bottom: 0.25rem;">
                            <span>Instagram:</span>
                            <span style="font-weight: 500; color: #0f172a;">Millennials (42%)</span>
                        </div>
                        <div style="display: flex; justify-content: space-between; margin-bottom: 0.25rem;">
                            <span>Facebook:</span>
                            <span style="font-weight: 500; color: #0f172a;">Gen X (38%)</span>
                        </div>
                        <div style="display: flex; justify-content: space-between;">
                            <span>LinkedIn:</span>
                            <span style="font-weight: 500; color: #0f172a;">Professionals (75%)</span>
                        </div>
                    </div>
                </div>
                
                <div style="flex: 1; min-width: 250px; background-color: #f8fafc; padding: 1rem; border-radius: 0.5rem; border: 1px solid #e2e8f0;">
                    <div style="font-weight: 600; color: #0f172a; margin-bottom: 0.5rem;">Growth Rate (YoY)</div>
                    <div style="color: #64748b; font-size: 0.875rem;">
                        <div style="display: flex; justify-content: space-between; margin-bottom: 0.25rem;">
                            <span>TikTok:</span>
                            <span style="font-weight: 500; color: #10b981;">+45.3%</span>
                        </div>
                        <div style="display: flex; justify-content: space-between; margin-bottom: 0.25rem;">
                            <span>YouTube:</span>
                            <span style="font-weight: 500; color: #10b981;">+18.7%</span>
                        </div>
                        <div style="display: flex; justify-content: space-between; margin-bottom: 0.25rem;">
                            <span>Instagram:</span>
                            <span style="font-weight: 500; color: #10b981;">+12.5%</span>
                        </div>
                        <div style="display: flex; justify-content: space-between;">
                            <span>Twitter:</span>
                            <span style="font-weight: 500; color: #ef4444;">-3.2%</span>
                        </div>
                    </div>
                </div>
                
                <div style="flex: 1; min-width: 250px; background-color: #f8fafc; padding: 1rem; border-radius: 0.5rem; border: 1px solid #e2e8f0;">
                    <div style="font-weight: 600; color: #0f172a; margin-bottom: 0.5rem;">Time Spent Daily</div>
                    <div style="color: #64748b; font-size: 0.875rem;">
                        <div style="display: flex; justify-content: space-between; margin-bottom: 0.25rem;">
                            <span>TikTok:</span>
                            <span style="font-weight: 500; color: #0f172a;">95 min</span>
                        </div>
                        <div style="display: flex; justify-content: space-between; margin-bottom: 0.25rem;">
                            <span>YouTube:</span>
                            <span style="font-weight: 500; color: #0f172a;">74 min</span>
                        </div>
                        <div style="display: flex; justify-content: space-between; margin-bottom: 0.25rem;">
                            <span>Instagram:</span>
                            <span style="font-weight: 500; color: #0f172a;">53 min</span>
                        </div>
                        <div style="display: flex; justify-content: space-between;">
                            <span>Facebook:</span>
                            <span style="font-weight: 500; color: #0f172a;">33 min</span>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- Side trend groups column -->
            <div style="flex: 1; min-width: 200px;">
                <div style="background-color: white; border-radius: 0.75rem; padding: 1rem; border: 1px solid #e2e8f0; margin-bottom: 1rem;">
                    <div style="font-weight: 600; color: #0f172a; margin-bottom: 0.5rem;">Trending Categories</div>
                    <div style="color: #64748b; font-size: 0.875rem;">
                        <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem; padding: 0.5rem; background-color: #f8fafc; border-radius: 0.5rem;">
                            <span>Short-form Video</span>
                            <span style="font-weight: 500; color: #10b981;">↑ 68%</span>
                        </div>
                        <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem; padding: 0.5rem; background-color: #f8fafc; border-radius: 0.5rem;">
                            <span>Creator Economy</span>
                            <span style="font-weight: 500; color: #10b981;">↑ 42%</span>
                        </div>
                        <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem; padding: 0.5rem; background-color: #f8fafc; border-radius: 0.5rem;">
                            <span>Social Commerce</span>
                            <span style="font-weight: 500; color: #10b981;">↑ 35%</span>
                        </div>
                        <div style="display: flex; justify-content: space-between; padding: 0.5rem; background-color: #f8fafc; border-radius: 0.5rem;">
                            <span>Long-form Content</span>
                            <span style="font-weight: 500; color: #ef4444;">↓ 8%</span>
                        </div>
                    </div>
                </div>
                
                <div style="background-color: white; border-radius: 0.75rem; padding: 1rem; border: 1px solid #e2e8f0;">
                    <div style="font-weight: 600; color: #0f172a; margin-bottom: 0.5rem;">Content Types</div>
                    <div style="color: #64748b; font-size: 0.875rem;">
                        <div style="display: flex; gap: 0.5rem; flex-wrap: wrap;">
                            <span style="background-color: #FEF2F2; color: #EF4444; padding: 0.25rem 0.5rem; border-radius: 9999px; font-size: 0.75rem;">Videos</span>
                            <span style="background-color: #EFF6FF; color: #3B82F6; padding: 0.25rem 0.5rem; border-radius: 9999px; font-size: 0.75rem;">Stories</span>
                            <span style="background-color: #F0FDF4; color: #22C55E; padding: 0.25rem 0.5rem; border-radius: 9999px; font-size: 0.75rem;">Reels</span>
                            <span style="background-color: #FDF4FF; color: #D946EF; padding: 0.25rem 0.5rem; border-radius: 9999px; font-size: 0.75rem;">Carousel</span>
                            <span style="background-color: #FFF7ED; color: #F97316; padding: 0.25rem 0.5rem; border-radius: 9999px; font-size: 0.75rem;">Lives</span>
                            <span style="background-color: #F0F9FF; color: #0EA5E9; padding: 0.25rem 0.5rem; border-radius: 9999px; font-size: 0.75rem;">Threads</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        </div>
        """
        , unsafe_allow_html=True)
        
        # Add a bubble chart showing the social media ecosystem
        st.markdown("""
        <div class="section-title"><span class="traffic-icon">🌊</span> Social Media Ecosystem</div>
        <div style="margin-bottom: 1.5rem; font-size: 0.9rem; color: #64748b;">
            Bubble size represents relative platform influence and user engagement.
        </div>
        """, unsafe_allow_html=True)
        
        # Create data for the bubble chart
        bubble_data = pd.DataFrame({
            'platform': ['TikTok', 'Instagram', 'YouTube', 'Facebook', 'Twitter', 'Reddit', 'LinkedIn', 'Pinterest'],
            'userAge': [23, 29, 30, 40, 34, 27, 44, 38],  # Average user age
            'engagementRate': [9.38, 5.86, 4.52, 1.98, 3.42, 8.75, 2.32, 3.65],  # Engagement rate (%)
            'userBase': [1500, 1800, 2500, 2900, 450, 430, 810, 480],  # User base in millions
            'category': ['Entertainment', 'Social', 'Video', 'Social', 'News', 'Community', 'Professional', 'Discovery'],
            'color': ['#000000', '#E1306C', '#FF0000', '#1877F2', '#1DA1F2', '#FF4500', '#0077B5', '#E60023']
        })
        
        # Create the bubble chart
        fig = px.scatter(
            bubble_data,
            x='userAge',
            y='engagementRate',
            size='userBase',
            color='platform',
            text='platform',
            size_max=60,
            color_discrete_map=dict(zip(bubble_data['platform'], bubble_data['color'])),
            hover_name='platform'
        )
        
        # Customize the bubble chart
        fig.update_layout(
            title='Platform Comparison: User Age vs. Engagement Rate',
            xaxis_title='Average User Age',
            yaxis_title='Engagement Rate (%)',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            height=500,
            showlegend=False,
        )
        
        # Add hover template
        fig.update_traces(
            hovertemplate='<b>%{hovertext}</b><br>Average User Age: %{x:.1f}<br>Engagement Rate: %{y:.2f}%<br>User Base: %{marker.size} million',
            textposition='top center',
            marker=dict(
                opacity=0.8,
                line=dict(
                    width=2,
                    color='white'
                )
            )
        )
        
        # Show the bubble chart
        st.plotly_chart(fig, use_container_width=True)
    
    # Tab 2: Trending Images from Social Media
    with tab2:
        st.markdown(f"<h2 class='animate-fadeIn'>Trending Images from Social Media</h2>", unsafe_allow_html=True)
        
        # Enhanced filters section with category-specific colors
        st.markdown("""
        <style>
        .filter-container {
            background-color: white;
            border-radius: 0.75rem;
            padding: 1rem;
            margin-bottom: 1.5rem;
            box-shadow: 0 1px 3px rgba(0,0,0,0.05);
            border: 1px solid #e2e8f0;
            display: flex;
            flex-wrap: wrap;
            gap: 1rem;
            align-items: center;
        }
        .filter-title {
            font-weight: 600;
            color: #0f172a;
            margin-right: 0.5rem;
        }
        .platform-filter-instagram { background-color: #E1306C; color: white; }
        .platform-filter-youtube { background-color: #FF0000; color: white; }
        .platform-filter-linkedin { background-color: #0077B5; color: white; }
        .platform-filter-tiktok { background-color: #000000; color: white; }
        .platform-filter-twitter { background-color: #1DA1F2; color: white; }
        </style>
        
        <div class="filter-container animate-slideInUp">
            <div class="filter-title">Filter content:</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Platform filter options with platform-specific colors
        platform_filter_cols = st.columns([1, 1, 1])
        with platform_filter_cols[0]:
            platform_filter = st.selectbox(
                "Platform", 
                ["All Platforms", "Instagram", "YouTube", "LinkedIn", "TikTok", "Twitter"],
                key="img_platform_filter"
            )
            
        # Add category filter in the next column
        with platform_filter_cols[1]:
            category_filter = st.selectbox(
                "Category",
                ["All Categories", "Technology", "Fashion", "Entertainment", "Politics", "Celebrity", 
                 "Food", "Travel", "Fitness", "Beauty", "Business", "Education"],
                key="img_category_filter"
            )
        
        # Fetch trending images with filters
        trending_images = fetch_trending_images(
            platform=platform_filter if platform_filter != "All Platforms" else None,
            industry=st.session_state.selected_industry if st.session_state.selected_industry != 'All Industries' else None,
            limit=9
        )
        
        # Display trending images in a responsive grid
        st.markdown("""
        <style>
        .image-card {
            border: 1px solid #e2e8f0;
            border-radius: 8px;
            overflow: hidden;
            background-color: white;
            box-shadow: 0 1px 3px rgba(0,0,0,0.05);
            margin-bottom: 1rem;
        }
        .image-header {
            display: flex;
            align-items: center;
            padding: 0.75rem;
            border-bottom: 1px solid #e2e8f0;
        }
        .platform-badge {
            font-size: 0.7rem;
            padding: 0.2rem 0.5rem;
            border-radius: 9999px;
            margin-left: auto;
        }
        .instagram-badge { background-color: #E1306C; color: white; }
        .youtube-badge { background-color: #FF0000; color: white; }
        .linkedin-badge { background-color: #0077B5; color: white; }
        .tiktok-badge { background-color: #000000; color: white; }
        .twitter-badge { background-color: #1DA1F2; color: white; }
        .image-content {
            padding: 0;
        }
        .image-footer {
            padding: 0.75rem;
            border-top: 1px solid #e2e8f0;
        }
        .engagement-row {
            display: flex;
            justify-content: space-between;
            margin-top: 0.5rem;
            color: #64748b;
            font-size: 0.85rem;
        }
        </style>
        """, unsafe_allow_html=True)
        
        # Create rows of images (3 per row)
        for i in range(0, len(trending_images), 3):
            cols = st.columns(3)
            
            for j in range(3):
                if i + j < len(trending_images):
                    img = trending_images[i + j]
                    
                    # Platform-specific badge style
                    platform_badge_class = f"{img['platform'].lower()}-badge"
                    
                    # Determine which engagement metrics to show based on platform
                    engagement_html = ""
                    if 'likes' in img['engagement']:
                        engagement_html += f"❤️ {img['engagement']['likes']:,} "
                    if 'views' in img['engagement']:
                        engagement_html += f"👁️ {img['engagement']['views']:,} "
                    if 'reactions' in img['engagement']:
                        engagement_html += f"👍 {img['engagement']['reactions']:,} "
                    if 'comments' in img['engagement']:
                        engagement_html += f"💬 {img['engagement']['comments']:,} "
                    if 'shares' in img['engagement']:
                        engagement_html += f"🔄 {img['engagement']['shares']:,} "
                    if 'retweets' in img['engagement']:
                        engagement_html += f"🔄 {img['engagement']['retweets']:,} "
                    
                    with cols[j]:
                        st.markdown(f"""
                        <div class="image-card">
                            <div class="image-header">
                                <div style="font-weight: 600;">{img['creator']}</div>
                                <div class="platform-badge {platform_badge_class}">{img['platform']}</div>
                            </div>
                            <div class="image-content">
                                <img src="{img['url']}" width="100%" alt="{img['topic']}">
                            </div>
                            <div class="image-footer">
                                <div style="font-weight: 500;">{img['topic']}</div>
                                <div style="color: #64748b; font-size: 0.9rem; margin-top: 0.25rem;">{img['caption']}</div>
                                <div class="engagement-row">
                                    {engagement_html}
                                </div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Add a button for each image that could lead to more details
                        st.button(f"View Details", key=f"view_{img['id']}")
        
        # Platform insights section
        st.subheader("Trending Content Insights")
        
        # Calculate platform distribution
        platform_counts = {}
        for img in trending_images:
            platform = img['platform']
            platform_counts[platform] = platform_counts.get(platform, 0) + 1
        
        # Create data for pie chart
        platform_data = pd.DataFrame({
            'platform': list(platform_counts.keys()),
            'count': list(platform_counts.values())
        })
        
        # Platform distribution pie chart
        fig = px.pie(
            platform_data,
            values='count',
            names='platform',
            title="Content Distribution by Platform",
            color='platform',
            color_discrete_map={
                'Instagram': '#E1306C',
                'YouTube': '#FF0000',
                'LinkedIn': '#0077B5',
                'TikTok': '#000000',
                'Twitter': '#1DA1F2'
            }
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Additional filter for topic analysis
        topic_counts = {}
        for img in trending_images:
            topic = img['topic']
            topic_counts[topic] = topic_counts.get(topic, 0) + 1
        
        # Create data for topic distribution
        topic_data = pd.DataFrame({
            'topic': list(topic_counts.keys()),
            'count': list(topic_counts.values())
        }).sort_values('count', ascending=False)
        
        # Topic distribution bar chart
        fig = px.bar(
            topic_data,
            x='count',
            y='topic',
            orientation='h',
            title="Top Topics in Trending Content",
            color='count',
            color_continuous_scale='Viridis'
        )
        fig.update_layout(yaxis={'categoryorder': 'total ascending'})
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Tab 3: Sentiment Analysis
    with tab3:
        st.header("Sentiment Analysis")
        
        # Analyze sentiment from the data
        sentiment_data = analyze_sentiment(data)
        
        # Get sentiment distribution
        sentiment_dist = get_sentiment_distribution(sentiment_data)
        
        # Display sentiment distribution chart
        col1, col2 = st.columns(2)
        
        with col1:
            # Sentiment distribution pie chart
            fig = px.pie(
                sentiment_dist,
                values='count',
                names='sentiment',
                title="Overall Sentiment Distribution",
                color='sentiment',
                color_discrete_map={
                    'Positive': '#36A2EB',
                    'Neutral': '#FFCE56',
                    'Negative': '#FF6384'
                }
            )
            st.plotly_chart(fig, use_container_width=True)
            
        with col2:
            # Sentiment by platform bar chart
            platform_sentiment = sentiment_data.groupby(['platform', 'sentiment']).size().reset_index(name='count')
            
            fig = px.bar(
                platform_sentiment,
                x='platform',
                y='count',
                color='sentiment',
                title="Sentiment Analysis by Platform",
                barmode='group',
                color_discrete_map={
                    'Positive': '#36A2EB',
                    'Neutral': '#FFCE56',
                    'Negative': '#FF6384'
                }
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Sentiment over time
        st.subheader("Sentiment Trends Over Time")
        
        # Group data by date and sentiment
        sentiment_time = sentiment_data.groupby(['date', 'sentiment']).size().reset_index(name='count')
        
        # Create line chart for sentiment over time
        fig = px.line(
            sentiment_time,
            x='date',
            y='count',
            color='sentiment',
            title="Sentiment Evolution Over Time",
            color_discrete_map={
                'Positive': '#36A2EB',
                'Neutral': '#FFCE56',
                'Negative': '#FF6384'
            }
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Top positive and negative trends
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Top Positive Trends")
            positive_trends = sentiment_data[sentiment_data['sentiment'] == 'Positive'].groupby('trend').size().reset_index(name='count')
            positive_trends = positive_trends.sort_values('count', ascending=False).head(5)
            
            # Display as a table
            st.dataframe(positive_trends, use_container_width=True)
            
        with col2:
            st.subheader("Top Negative Trends")
            negative_trends = sentiment_data[sentiment_data['sentiment'] == 'Negative'].groupby('trend').size().reset_index(name='count')
            negative_trends = negative_trends.sort_values('count', ascending=False).head(5)
            
            # Display as a table
            st.dataframe(negative_trends, use_container_width=True)
    
    # Tab 3: Growth Forecast
    with tab3:
        st.header("Growth Forecast")
        
        # Get the forecast data
        forecast_data = get_growth_forecast(data)
        
        # Top growing trends
        st.subheader("Top 5 Trends with Highest Growth Potential")
        top_growth_trends = forecast_data.sort_values('growth_forecast', ascending=False).head(5)
        
        # Create horizontal bar chart for top growing trends
        fig = px.bar(
            top_growth_trends,
            x='growth_forecast',
            y='trend',
            orientation='h',
            color='growth_forecast',
            title="Trends with Highest Projected Growth",
            color_continuous_scale='Viridis',
            labels={'growth_forecast': 'Projected Growth (%)', 'trend': 'Trend'}
        )
        fig.update_layout(yaxis={'categoryorder': 'total ascending'})
        st.plotly_chart(fig, use_container_width=True)
        
        # Forecast visualization
        st.subheader("Growth Forecast Timeline")
        
        # Select a trend to visualize
        selected_trend = st.selectbox(
            "Select a trend to visualize its growth forecast",
            forecast_data['trend'].unique()
        )
        
        # Filter data for the selected trend
        trend_forecast = forecast_data[forecast_data['trend'] == selected_trend]
        
        # Create a line chart with historical and forecast data
        fig = go.Figure()
        
        # Historical data
        fig.add_trace(go.Scatter(
            x=trend_forecast['date'],
            y=trend_forecast['volume'],
            mode='lines+markers',
            name='Historical Volume',
            line=dict(color='#36A2EB')
        ))
        
        # Forecast data
        fig.add_trace(go.Scatter(
            x=trend_forecast['forecast_date'],
            y=trend_forecast['forecast_volume'],
            mode='lines+markers',
            name='Forecasted Volume',
            line=dict(color='#FF6384', dash='dash')
        ))
        
        fig.update_layout(
            title=f"Growth Forecast for '{selected_trend}'",
            xaxis_title="Date",
            yaxis_title="Volume",
            legend_title="Data Type"
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Growth comparison by industry
        st.subheader("Growth Comparison by Industry")
        
        # Group data by industry and calculate average growth forecast
        industry_growth = forecast_data.groupby('industry')['growth_forecast'].mean().reset_index()
        industry_growth = industry_growth.sort_values('growth_forecast', ascending=False)
        
        # Create bar chart for industry growth
        fig = px.bar(
            industry_growth,
            x='industry',
            y='growth_forecast',
            color='growth_forecast',
            title="Average Growth Forecast by Industry",
            color_continuous_scale='Viridis',
            labels={'growth_forecast': 'Avg. Growth Forecast (%)', 'industry': 'Industry'}
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Tab 5: Recommendations
    with tab5:
        st.markdown("<h2 class='animate-fadeIn'>Actionable Recommendations</h2>", unsafe_allow_html=True)
        
        # Add explanation for the recommendations with animated entry
        st.markdown("""
        <div class="animate-slideInUp" style="background-color: white; border-radius: 0.75rem; 
             padding: 1rem; margin-bottom: 1.5rem; border: 1px solid #e2e8f0;">
            <p style="margin: 0; color: #334155;">
                Our AI analyzes trending content across platforms to provide actionable insights customized 
                to different categories. Click on any recommendation to expand and see detailed steps.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Generate recommendations based on the data
        recommendations = generate_recommendations(data)
        
        # Category-specific styling
        st.markdown("""
        <style>
        .recommendation-header {
            cursor: pointer;
            transition: transform 0.2s ease;
        }
        .recommendation-header:hover {
            transform: translateX(5px);
        }
        </style>
        """, unsafe_allow_html=True)
        
        # Display recommendations by category with Streamlit components
        for category, rec_list in recommendations.items():
            st.subheader(category + " Recommendations")
            
            # Create columns for a responsive grid layout
            cols = st.columns(2)
            
            for i, rec in enumerate(rec_list):
                col_idx = i % 2
                
                with cols[col_idx]:
                    with st.container():
                        # Use Streamlit to create a card-like container with styling
                        st.markdown(f"""
                        <div style="background-color: white; border-radius: 8px; border: 1px solid #e2e8f0; 
                             padding: 1.25rem; margin-bottom: 1rem; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">
                            <div style="display: flex; justify-content: space-between; align-items: center;">
                                <h4 style="color: #2563EB; margin: 0; font-weight: 600;">{rec['title']}</h4>
                                <span style="background-color: #3b82f6; color: white; font-size: 0.75rem; 
                                     padding: 0.25rem 0.5rem; border-radius: 9999px;">{rec['metrics']['relevance']}/10</span>
                            </div>
                            <p style="color: #64748b; margin-top: 0.5rem; margin-bottom: 1rem;">{rec['description']}</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Add action steps using Streamlit components
                        st.markdown("**Action steps:**")
                        for step in rec['action_steps']:
                            st.markdown(f"- {step}")
                        
                        # Add metrics using Streamlit columns
                        if 'metrics' in rec:
                            metric_cols = st.columns(2)
                            metric_cols[0].metric("Potential Reach", f"{rec['metrics']['potential_reach']:,}")
                            metric_cols[1].metric("Implementation Effort", f"{rec['metrics']['effort']}/10")
        
        # Export & Alerts section with Streamlit components
        st.subheader("Export & Alerts")
        
        action_cols = st.columns(2)
        
        # Export card
        with action_cols[0]:
            with st.container():
                st.markdown("""
                <div style="background-color: white; border-radius: 8px; border: 1px solid #e2e8f0; 
                     padding: 1rem; margin-bottom: 1rem; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">
                    <h4 style="margin: 0 0 0.5rem 0; color: #0f172a; font-weight: 600;">
                        <span style="color: #3b82f6;">📥</span> Download Analysis Report
                    </h4>
                    <p style="margin-bottom: 1rem; color: #334155; font-size: 0.9rem;">
                        Download a comprehensive report of all trend analysis, forecasts, and 
                        recommendations for presentation or offline reference.
                    </p>
                </div>
                """, unsafe_allow_html=True)
                
                # Actual download button for functionality
                st.download_button(
                    label="Download Trend Analysis Report (PDF)",
                    data="This would be a generated PDF report in a real implementation",
                    file_name=f"trend_analysis_{datetime.now().strftime('%Y%m%d')}.pdf",
                    mime="application/pdf",
                    disabled=True  # Disabled for this implementation
                )
        
        # Alerts card
        with action_cols[1]:
            with st.container():
                st.markdown("""
                <div style="background-color: white; border-radius: 8px; border: 1px solid #e2e8f0; 
                     padding: 1rem; margin-bottom: 1rem; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">
                    <h4 style="margin: 0 0 0.5rem 0; color: #0f172a; font-weight: 600;">
                        <span style="color: #ef4444;">🔔</span> Set up Trend Alerts
                    </h4>
                    <p style="margin-bottom: 1rem; color: #334155; font-size: 0.9rem;">
                        Receive notifications when new trends emerge in your industry. 
                        Choose your frequency and stay ahead of the competition.
                    </p>
                </div>
                """, unsafe_allow_html=True)
                
                # Alerts form with Streamlit components
                with st.form("trend_alert_form", clear_on_submit=False):
                    st.markdown("**Alert Configuration**")
                    email = st.text_input("Email address")
                    
                    form_cols = st.columns(2)
                    with form_cols[0]:
                        alert_frequency = st.selectbox(
                            "Alert frequency",
                            ["Daily", "Weekly", "Real-time"]
                        )
                    
                    with form_cols[1]:
                        alert_industries = st.multiselect(
                            "Industries to track",
                            industry_options[1:]  # All except 'All Industries'
                        )
                    
                    # Submit button
                    submit = st.form_submit_button("Set up alerts")
                    if submit:
                        if email and alert_industries:
                            st.success(f"Alerts set up successfully for {email}! You'll receive {alert_frequency.lower()} updates for selected industries.")
                        else:
                            st.error("Please provide your email and select at least one industry.")

if __name__ == "__main__":
    main()
