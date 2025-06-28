import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import json
import urllib.parse
import pandas as pd

# Page config
st.set_page_config(
    page_title="Survey Dashboard Hub",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for dashboard pages only
def load_dashboard_css():
    st.markdown("""
        <style>
        /* make selected radio blue */
        input[type="radio"]:checked {
            accent-color: #3b82f6 !important;  /* Tailwind blue-600 */
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css" rel="stylesheet">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
        
        /* Global styles */
        * {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        }
        
        /* Constrain main content width */
        .main .block-container {
            max-width: 1800px;
            padding: 0 3rem 2rem 3rem;
            margin: 0 auto;
        }
        
        /* Remove all top padding */
        .main {
            padding-top: 0 !important;
        }
        
        .main > div:first-child {
            padding-top: 0 !important;
        }
        
        .element-container:first-child {
            margin-top: 0 !important;
        }
        
        header[data-testid="stHeader"] {
            height: 0 !important;
        }
        
        .appview-container {
            padding-top: 0 !important;
        }
        
        section[data-testid="stSidebar"] {
            padding-top: 0 !important;
        }
        
        /* Hide Streamlit elements */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        .stDeployButton {display: none;}
        
        /* Header styling - simplified since we're using columns */
        .user-info {
            background: white;
            padding: 0.5rem 1rem;
            border-radius: 30px;
            display: flex;
            align-items: center;
            gap: 0.75rem;
            border: 1px solid #e2e8f0;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        }
        
        .user-avatar {
            width: 36px;
            height: 36px;
            border-radius: 50%;
            background: #3b82f6;
            color: white;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 600;
            font-size: 0.9rem;
        }
        
        /* Enhanced metric cards */
        .metric-card {
            background: white;
            border-radius: 16px;
            padding: 1.75rem;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
            border: 1px solid rgba(0, 0, 0, 0.05);
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }
        
        .metric-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
        }
        
        .metric-value {
            font-size: 2rem;
            font-weight: 700;
            color: #1e293b;
            margin: 0.25rem 0;
        }
        
        .metric-label {
            color: #64748b;
            font-size: 0.95rem;
            font-weight: 500;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        .metric-change {
            color: #10b981;
            font-size: 0.9rem;
            font-weight: 600;
        }
        
        /* Enhanced tracker cards */
        .tracker-card {
            background: white;
            border-radius: 16px;
            padding: 2rem;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
            border: 1px solid rgba(0, 0, 0, 0.05);
            position: relative;
            overflow: hidden;
            height: 280px;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: space-between;
            text-align: center;
            transition: box-shadow 0.3s ease;
        }
        
        .tracker-card:hover {
            box-shadow: 0 8px 30px rgba(0, 0, 0, 0.12);
        }
        
        .tracker-icon {
            width: 60px;
            height: 60px;
            margin-bottom: 1rem;
            display: flex;
            align-items: center;
            justify-content: center;
            background: #f0f4f8;
            border-radius: 16px;
        }
        
        .tracker-icon svg {
            width: 32px;
            height: 32px;
        }
        
        .tracker-card.sports .tracker-icon {
            background: #dbeafe;
        }
        
        .tracker-card.sports .tracker-icon svg {
            fill: #3b82f6;
        }
        
        .tracker-card.toys .tracker-icon {
            background: #d1fae5;
        }
        
        .tracker-card.toys .tracker-icon svg {
            fill: #10b981;
        }
        
        .tracker-card.education .tracker-icon {
            background: #fed7aa;
        }
        
        .tracker-card.education .tracker-icon svg {
            fill: #f59e0b;
        }
        
        .tracker-card h3 {
            color: #1e293b;
            font-size: 1.5rem;
            margin: 0.5rem 0;
            font-weight: 600;
        }
        
        .tracker-card p {
            color: #64748b;
            font-size: 0.95rem;
            line-height: 1.5;
            margin-bottom: 1.5rem;
            flex-grow: 1;
        }
        
        /* Enhanced buttons */
        .stButton > button {
            border-radius: 8px;
            font-weight: 600;
            transition: all 0.3s ease;
            padding: 0.75rem 1.5rem;
        }
        
        .stButton > button[kind="primary"] {
            background: linear-gradient(135deg, #0369a1 0%, #0284c7 100%);
            color: white;
            border: none;
            box-shadow: 0 4px 15px rgba(3, 105, 161, 0.3);
        }
        
        .stButton > button[kind="primary"]:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(3, 105, 161, 0.4);
        }
        
        .stButton > button[kind="secondary"] {
            background: white;
            color: #0369a1;
            border: 1px solid #0369a1;
        }
        
        .stButton > button[kind="secondary"]:hover {
            background: #f0f9ff;
        }
        
        /* Default button styling for those without kind attribute */
        .stButton > button:not([kind]) {
            background: #0369a1;
            color: white;
            border: none;
        }
        
        .stButton > button:not([kind]):hover {
            background: #0284c7;
        }
        
        /* Tracker-specific button colors */
        .tracker-button-sports button {
            background: #3b82f6 !important;
        }
        
        .tracker-button-sports button:hover {
            background: #2563eb !important;
        }
        
        .tracker-button-toys button {
            background: #10b981 !important;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1) !important;
        }
        
        .tracker-button-toys button:hover {
            background: #059669 !important;
            box-shadow: 0 4px 8px rgba(16, 185, 129, 0.3) !important;
        }
        
        .tracker-button-education button {
            background: #a855f7 !important;
        }
        
        .tracker-button-education button:hover {
            background: #9333ea !important;
        }
        
        .tracker-button-health button {
            background: #ef4444 !important;
        }
        
        .tracker-button-health button:hover {
            background: #dc2626 !important;
        }
        
        .tracker-button-consumer button {
            background: #f59e0b !important;
        }
        
        .tracker-button-consumer button:hover {
            background: #d97706 !important;
        }
        
        /* Common button styles for all tracker buttons */
        [class*="tracker-button-"] button {
            color: white !important;
            border-radius: 8px !important;
            padding: 0.75rem 1.75rem !important;
            font-weight: 600 !important;
            font-size: 0.95rem !important;
            border: none !important;
            width: 100% !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            gap: 0.5rem !important;
        }
        
        [class*="tracker-button-"] button:hover {
            transform: translateY(-1px) !important;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15) !important;
        }
        
        /* Tracker card container styling */
        [data-testid="stVerticalBlock"] > [data-testid="column"] {
            min-height: 440px;
        }
        
        /* Ensure proper card layout */
        [data-testid="column"] > div {
            height: 100%;
        }
        
        /* Fix button positioning within cards */
        .element-container:has([class*="tracker-button-"]) {
            position: relative;
            z-index: 1;
        }
        
        /* Enhanced insight cards */
        .insight-card {
            background: white;
            border-radius: 16px;
            padding: 1.5rem;
            margin-bottom: 1rem;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
            cursor: pointer;
            transition: all 0.3s ease;
            border: 2px solid transparent;
            position: relative;
            overflow: hidden;
        }
        
        .insight-card:hover {
            transform: translateY(-4px);
            box-shadow: 0 8px 30px rgba(0, 0, 0, 0.12);
        }
        
        .insight-card.selected {
            border-color: #0369a1;
            box-shadow: 0 8px 30px rgba(3, 105, 161, 0.3);
        }
        
        /* Tag styling */
        .tag-container {
            display: flex;
            gap: 0.5rem;
            flex-wrap: wrap;
            margin-top: 0.75rem;
        }
        
        .tag {
            padding: 0.35rem 0.85rem;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: 600;
            transition: all 0.2s ease;
        }
        
        .tag-play-patterns {
            background: #dbeafe;
            color: #1e40af;
        }
        
        .tag-discovery {
            background: #fed7aa;
            color: #c2410c;
        }
        
        .tag-values {
            background: #fce7f3;
            color: #be185d;
        }
        
        /* Enhanced filters */
        .filter-container {
            background: #f8fafc;
            border-radius: 16px;
            padding: 1.5rem;
            margin-bottom: 2rem;
            border: 1px solid #e2e8f0;
        }
        
        /* Chart containers */
        .chart-container {
            background: white;
            border-radius: 16px;
            padding: 1.5rem;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
            margin-bottom: 1.5rem;
            transition: all 0.3s ease;
        }
        
        .chart-container:hover {
            box-shadow: 0 8px 30px rgba(0, 0, 0, 0.12);
        }
        
        /* Sidebar styling */
        .sidebar-section {
            background: white;
            border-radius: 16px;
            padding: 1.5rem;
            margin-bottom: 1.5rem;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
        }
        
        .download-item {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 0.75rem 0;
            border-bottom: 1px solid #e2e8f0;
        }
        
        .download-item:last-child {
            border-bottom: none;
        }
        
        /* Tab styling */
        .stTabs [data-baseweb="tab-list"] {
            gap: 2rem;
            background: #f8fafc;
            padding: 0.5rem;
            border-radius: 12px;
        }
        
        .stTabs [data-baseweb="tab"] {
            padding: 0.75rem 1.5rem;
            border-radius: 8px;
            font-weight: 600;
            transition: all 0.2s ease;
        }
        
        .stTabs [aria-selected="true"] {
            background: white;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        }
        
        /* Input styling */
        .stTextInput > div > div > input,
        .stSelectbox > div > div > select {
            border-radius: 10px;
            border: 2px solid #e2e8f0;
            padding: 0.75rem 1rem;
            transition: all 0.2s ease;
        }
        
        .stTextInput > div > div > input:focus,
        .stSelectbox > div > div > select:focus {
            border-color: #0369a1;
            box-shadow: 0 0 0 3px rgba(3, 105, 161, 0.1);
        }
        
        /* Wave badge */
        .wave-badge {
            background: #fbbf24;
            color: #78350f;
            padding: 0.25rem 0.65rem;
            border-radius: 20px;
            font-size: 0.75rem;
            font-weight: 600;
            margin-left: 0.5rem;
            display: inline-block;
        }
        
        /* Animation for page transitions */
        .main-content {
            animation: fadeIn 0.5s ease-out;
            padding-top: 1rem;
        }
        
        @keyframes fadeIn {
            from {
                opacity: 0;
                transform: translateY(20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        /* Custom scrollbar */
        ::-webkit-scrollbar {
            width: 8px;
            height: 8px;
        }
        
        ::-webkit-scrollbar-track {
            background: #f1f5f9;
        }
        
        ::-webkit-scrollbar-thumb {
            background: #cbd5e0;
            border-radius: 4px;
        }
        
        ::-webkit-scrollbar-thumb:hover {
            background: #a0aec0;
        }
        
        /* Selected insight card styling */
        .insight-card-selected {
            background: #dbeafe !important;
            border: 2px solid #3b82f6 !important;
            box-shadow: 0 8px 30px rgba(59, 130, 246, 0.15) !important;
        }
        
        /* Clickable card button styling */
        .insight-card-button {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: transparent;
            border: none;
            cursor: pointer;
            z-index: 10;
        }
    </style>
    """, unsafe_allow_html=True)

# Login page - using standard Streamlit components
def login_page():
    # Apply minimal CSS to remove top padding for login too
    st.markdown("""
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css" rel="stylesheet">
    <style>
        .main {
            padding-top: 0 !important;
        }
        header[data-testid="stHeader"] {
            height: 0 !important;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Add some top spacing
    st.markdown("<div style='height: 5vh;'></div>", unsafe_allow_html=True)
    
    # Center the login form
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col2:
        # Center the logo using columns
        logo_col1, logo_col2, logo_col3 = st.columns([1, 2, 1])
        with logo_col2:
            try:
                st.image("tif.png", use_container_width=True)
            except:
                # Fallback icon if image not found
                st.markdown("""
                    <div style='
                        background: #3b82f6;
                        width: 80px;
                        height: 80px;
                        border-radius: 20px;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        color: white;
                        font-size: 40px;
                        margin: 0 auto 2rem auto;
                    '>
                        <i class="fa-solid fa-chart-bar"></i>
                    </div>
                """, unsafe_allow_html=True)
        
        st.markdown("<h2 style='text-align: center; margin-top: 1.5rem;'>Survey Dashboard Hub</h2>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #666; margin-bottom: 2rem;'>Sign in to access your analytics</p>", unsafe_allow_html=True)
        
        with st.form("login_form", clear_on_submit=False):
            username = st.text_input("Username", placeholder="Enter your username")
            password = st.text_input("Password", type="password", placeholder="Enter your password")
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            submit = st.form_submit_button("Sign In", use_container_width=True)
            
            if submit:
                if username and password:
                    st.session_state.logged_in = True
                    st.session_state.current_page = 'trackers'
                    st.session_state.username = username
                    st.rerun()
                else:
                    st.error("Please enter both username and password")

# Trackers selection page
def trackers_page():
    load_dashboard_css()

    # Top margin
    st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)

    # Header
    header_col1, header_col2 = st.columns([3, 1])
    with header_col1:
        logo_col, text_col = st.columns([0.15, 0.55])
        with logo_col:
            try:
                st.image("tif.png", width=1000)
            except:
                st.markdown("""
                    <div style='
                        background: #3b82f6;
                        width: 50px;
                        height: 50px;
                        border-radius: 12px;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        color: white;
                        font-size: 24px;
                        margin-top: 0.25rem;
                    '>
                        <i class="fa-solid fa-chart-bar"></i>
                    </div>
                """, unsafe_allow_html=True)
        with text_col:
            st.markdown("""
                <div>
                    <h1 style='margin: 0; color: #1e293b; font-size: 1.5rem;'>Survey Dashboard Hub</h1>
                    <p style='margin: 0; color: #64748b;'>Select a tracker to explore insights and data</p>
                </div>
            """, unsafe_allow_html=True)

    with header_col2:
        st.markdown(f"""
            <div class="user-info" style='margin-top: 0.5rem;'>
                <div class="user-avatar" style="font-size: 1rem;">{st.session_state.get('username', 'User')[0].upper()}</div>
                <div>
                    <p style='margin: 0; font-weight: 600; color: #1e293b; font-size: 0.95rem;'>{st.session_state.get('username', 'Sarah Johnson')}</p>
                    <p style='margin: 0; font-size: 0.8rem; color: #64748b;'>Research Analyst</p>
                </div>
            </div>
        """, unsafe_allow_html=True)

    # Section heading
    st.markdown("<h2 style='font-size: 1.625rem; color: #1e293b;'>Available Trackers</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: #64748b; margin-bottom: 2rem; font-size: 1.05rem;'>Choose a tracker to dive into detailed analytics and insights</p>", unsafe_allow_html=True)

    # Trackers data
    trackers = [
        {
            "name": "Sports Tracker",
            "description": "Track children's sports participation and activity patterns",
            "icon_color": "#3b82f6",
            "bg_color": "#dbeafe",
            "icon": "fa-solid fa-trophy",
            "active": False,
            "surveys": "12",
            "responses": "2,450",
            "updated": "2 days ago"
        },
        {
            "name": "Toys & Play",
            "description": "Monitor toy preferences, play patterns, and benefits",
            "icon_color": "#10b981",
            "bg_color": "#d1fae5",
            "icon": "fa-solid fa-gamepad",
            "active": True,
            "surveys": "8",
            "responses": "1,890",
            "updated": "1 day ago"
        },
        {
            "name": "Education Tracker",
            "description": "Analyze learning preferences and outcomes",
            "icon_color": "#a855f7",
            "bg_color": "#f3e8ff",
            "icon": "fa-solid fa-graduation-cap",
            "active": False,
            "surveys": "15",
            "responses": "3,200",
            "updated": "3 hours ago"
        },
        {
            "name": "Health & Wellness",
            "description": "Track children's health habits, nutrition choices, and wellness activities",
            "icon_color": "#ef4444",
            "bg_color": "#fee2e2",
            "icon": "fa-solid fa-heart",
            "active": False,
            "surveys": "10",
            "responses": "1,650",
            "updated": "5 hours ago"
        },
        {
            "name": "Consumer Behavior",
            "description": "Understand family purchasing decisions, brand preferences, and spending patterns",
            "icon_color": "#f59e0b",
            "bg_color": "#fef3c7",
            "icon": "fa-solid fa-shopping-cart",
            "active": False,
            "surveys": "6",
            "responses": "980",
            "updated": "1 week ago"
        }
    ]

    # Render trackers
    for i in range(0, len(trackers), 3):
        cols = st.columns(3, gap="medium")
        for col, tracker in zip(cols, trackers[i:i+3]):
            with col:
                st.markdown(f"""
                    <div style="
                        background: white;
                        border: 1px solid #e2e8f0;
                        border-radius: 16px;
                        padding: 1rem;
                        box-shadow: 0 2px 6px rgba(0,0,0,0.04);
                    ">
                        <div style="
                            background: {tracker['bg_color']};
                            border: 1px solid {tracker['icon_color']};
                            border-radius: 12px;
                            padding: 1.25rem;
                            position: relative;
                            min-height: 380px;
                            display: flex;
                            flex-direction: column;
                            justify-content: space-between;
                        ">
                            <div style="position: absolute; top: 1rem; right: 1rem; font-size: 1rem; color: #94a3b8;">
                                <i class="fa-solid fa-arrow-right"></i>
                            </div>
                            <div style="flex: 1;">
                                <div style="
                                    background: white;
                                    width: 48px;
                                    height: 48px;
                                    display: flex;
                                    align-items: center;
                                    justify-content: center;
                                    border-radius: 12px;
                                    box-shadow: 0 2px 6px rgba(0,0,0,0.08);
                                    font-size: 1.25rem;
                                    margin-bottom: 0.5rem;
                                    color: {tracker['icon_color']};
                                ">
                                    <i class="{tracker['icon']}"></i>
                                </div>
                                <h3 style="margin: 0; font-size: 1.2rem; color: #0f172a;">{tracker['name']}</h3>
                                <p style="color: #475569; font-size: 0.9rem; margin: 0.5rem 0 1rem;">{tracker['description']}</p>
                                <div style="font-size: 0.8rem; color: #1e293b;">
                                    <div style="display: flex; justify-content: space-between;"><span>Surveys</span><span>{tracker['surveys']}</span></div>
                                    <div style="display: flex; justify-content: space-between;"><span>Responses</span><span>{tracker['responses']}</span></div>
                                    <div style="display: flex; justify-content: space-between; color: #64748b;"><span>Last Updated</span><span>{tracker['updated']}</span></div>
                                </div>
                            </div>
                            <div style="margin-top: 1rem;">
                """, unsafe_allow_html=True)

                # clickable pill link
                if tracker["active"]:
                    import urllib.parse
                    encoded_name = urllib.parse.quote(tracker['name'].replace(' ', '_'))

                    # capture the username from session
                    username = st.session_state.get("username", "User")
                    encoded_user = urllib.parse.quote(username.replace(" ", "_"))

                    href = f"?open={encoded_name}&user={encoded_user}"

                    st.markdown(f"""
                        <a href="{href}" style="
                            display: block;
                            background: {tracker['icon_color']};
                            color: white;
                            text-align: center;
                            padding: 0.6rem 1rem;
                            border-radius: 999px;
                            font-weight: 600;
                            font-size: 0.9rem;
                            text-decoration: none;
                            margin-top: 0.5rem;
                        ">
                            Open Dashboard
                        </a>
                    """, unsafe_allow_html=True)

                else:
                    st.markdown("""
                        <div style="
                            background: #e2e8f0;
                            color: #94a3b8;
                            text-align: center;
                            padding: 0.6rem 1rem;
                            border-radius: 999px;
                            font-weight: 600;
                            font-size: 0.9rem;
                            margin-top: 0.5rem;
                        ">
                            Coming Soon
                        </div>
                    """, unsafe_allow_html=True)

                st.markdown("</div></div></div>", unsafe_allow_html=True)


    # Add the research solutions section
    #st.markdown("<br><br><br>", unsafe_allow_html=True)
    st.markdown("<h2 style='font-size: 1.625rem; color: #1e293b;'>Research Solutions</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: #64748b; margin-bottom: 2rem; font-size: 1.05rem;'>Comprehensive research methodologies for deeper insights</p>", unsafe_allow_html=True)

    solutions = [
        {
            "name": "Attitude and Usage",
            "description": "Comprehensive studies on consumer attitudes, behaviors, and product usage",
            "icon": "fa-solid fa-users",
            "icon_color": "#06b6d4",
            "bg_color": "#ecfeff"
        },
        {
            "name": "Brand Health Check",
            "description": "Monitor brand perception, awareness, and competitive positioning over time",
            "icon": "fa-solid fa-circle-check",
            "icon_color": "#10b981",
            "bg_color": "#f0fdf4"
        },
        {
            "name": "Brand Lift",
            "description": "Measure the impact of campaigns on brand metrics and consumer behavior",
            "icon": "fa-solid fa-chart-line",
            "icon_color": "#8b5cf6",
            "bg_color": "#faf5ff"
        },
        {
            "name": "Innovation",
            "description": "Test new concepts, products, and ideas to drive successful innovation strategies",
            "icon": "fa-solid fa-lightbulb",
            "icon_color": "#f59e0b",
            "bg_color": "#fffbeb"
        }
    ]

    research_cols = st.columns(4, gap="medium")
    for col, solution in zip(research_cols, solutions):
        with col:
            st.markdown(f"""
                <div style="
                    background: white;
                    border: 1px solid #e2e8f0;
                    border-radius: 16px;
                    padding: 2.25rem 1.75rem;
                    box-shadow: 0 2px 6px rgba(0,0,0,0.04);
                    text-align: center;
                    height: 340px;
                    display: flex;
                    flex-direction: column;
                    justify-content: space-between;
                ">
                    <div>
                        <div style="margin-bottom: 0.5rem; color: #94a3b8; font-size: 0.9rem;">
                            Coming Soon
                        </div>
                        <div style="
                            width: 64px;
                            height: 64px;
                            margin: 1rem auto;
                            background: {solution['bg_color']};
                            border-radius: 14px;
                            display: flex;
                            align-items: center;
                            justify-content: center;
                            font-size: 1.75rem;
                            color: {solution['icon_color']};
                        ">
                            <i class="{solution['icon']}"></i>
                        </div>
                        <h3 style="margin: 1rem 0 0.5rem 0; font-size: 1.2rem; color: #1e293b; font-weight: 600;">
                            {solution['name']}
                        </h3>
                        <p style="color: #64748b; font-size: 0.9rem; line-height: 1.5; margin: 0;">
                            {solution['description']}
                        </p>
                    </div>
                    <div style="margin-top: 1.5rem;">
                        <div style="
                            background: rgba(226, 232, 240, 0.8);
                            color: #94a3b8;
                            padding: 0.75rem 1.75rem;
                            border-radius: 8px;
                            font-weight: 600;
                            font-size: 0.95rem;
                            text-align: center;
                        ">
                            Coming Soon
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)

    # Footer
    st.markdown("""
        <div style='text-align: center; color: #64748b; font-size: 0.95rem; padding: 2rem 0;'>
            <i class="fa-solid fa-chart-line"></i> TIF Trackers • 2025 • Powered by Advanced Analytics
        </div>
    """, unsafe_allow_html=True)


# Load full JSON data
def load_full_data():
    try:
        with open('toy_dashboard_data.json', 'r') as f:
            data = json.load(f)
            print("✅ JSON file successfully loaded.")
            return data
    except:
        return {
            "settings": {
                "insightCards": [
                    {
                        "insight": "Hands-on fun dominates: Play-Doh is the #1 toy for daily play, starring in 17 of 123 daily sessions",
                        "relatedQuestions": ["Q003", "Q012"],
                        "category": ["Play Patterns"],
                        "tags": ["Favorite Toy", "Play Frequency"]
                    },
                    {
                        "insight": "Store shelves still sway decisions: 110 kids (22.0%) discovered their toy in-store—edging out YouTube",
                        "relatedQuestions": ["Q010"],
                        "category": ["Discovery"],
                        "tags": ["Toy Discovery"]
                    },
                    {
                        "insight": "Back-to-basics for older kids: 68 of 189 6-8-year-olds (36.0%) prefer physical-only play—the highest of all age groups",
                        "relatedQuestions": ["Q020", "Q001"],
                        "category": ["Values"],
                        "tags": ["Age", "Digital vs. Physical"]
                    }
                ]
            },
            "data": [
                {
                    "code": "Q001",
                    "question": "Age",
                    "type": "numeric",
                    "respondents": 500,
                    "chartType": "bar",
                    "responses": {
                        "3": 74, "4": 66, "5": 74, "6": 61,
                        "7": 89, "8": 76, "9": 60
                    }
                },
                {
                    "code": "Q002",
                    "question": "Gender",
                    "type": "categorical",
                    "respondents": 500,
                    "chartType": "pie",
                    "responses": {
                        "Male": 251,
                        "Female": 249
                    }
                }
            ]
        }

def render_key_insights():
    data = load_full_data()
    insights = data.get("settings", {}).get("insightCards", [])

    # session state
    if "selected_question_codes" not in st.session_state:
        st.session_state.selected_question_codes = []
    if "insights_page" not in st.session_state:
        st.session_state.insights_page = 0

    # categories
    category_counts = {}
    for i in insights:
        for cat in i.get("category", []):
            category_counts[cat] = category_counts.get(cat, 0) + 1

    categories = sorted(category_counts.keys())
    categories.insert(0, "All")

    cat_labels = []
    for cat in categories:
        count = len(insights) if cat == "All" else category_counts.get(cat, 0)
        cat_labels.append(f"{cat} ({count})")

    if "active_insight_category" not in st.session_state:
        st.session_state.active_insight_category = cat_labels[0]

    st.markdown("""
        <h2 style='font-size: 1.5rem; color: #1e293b;'>Key Insights</h2>
        <p style='color:#64748b; margin-bottom: 1rem;'>Showing key insights from the current dataset. Click the button inside a card to filter the related survey questions.</p>
    """, unsafe_allow_html=True)

    chosen_label = st.radio(
        label="Select an insight category",
        options=cat_labels,
        index=cat_labels.index(st.session_state.active_insight_category),
        horizontal=True,
        label_visibility="collapsed",
    )

    st.session_state.active_insight_category = chosen_label
    active_category = chosen_label.split(" (")[0]

    if active_category == "All":
        filtered_insights = insights
    else:
        filtered_insights = [
            i for i in insights if active_category in i.get("category", [])
        ]

    # pagination
    page_size = 3
    total_pages = max((len(filtered_insights) - 1) // page_size + 1, 1)
    current_page = st.session_state.insights_page
    start_idx = current_page * page_size
    end_idx = start_idx + page_size
    page_insights = filtered_insights[start_idx:end_idx]

    # render cards
    insight_cols = st.columns(3, gap="large")

    for idx, insight in enumerate(page_insights):
        col = insight_cols[idx % 3]
        with col:
            tags = insight.get("tags", [])
            related_qs = insight.get("relatedQuestions", [])
            related_qs_str = ", ".join(related_qs)
            is_selected = st.session_state.selected_question_codes == related_qs

            card_bg = "#dbeafe" if is_selected else "white"
            border_color = "#3b82f6" if is_selected else "#e2e8f0"
            box_shadow = (
                "0 8px 30px rgba(59, 130, 246, 0.15)"
                if is_selected else "0 2px 4px rgba(0,0,0,0.05)"
            )

            # the card itself
            with st.container(border=False):
                st.markdown(f"""
                    <div style="
                        background:{card_bg};
                        border:2px solid {border_color};
                        border-radius:16px;
                        padding:1rem;
                        box-shadow:{box_shadow};
                        display:flex;
                        flex-direction:column;
                        justify-content:space-between;
                        height: 220px;
                        transition: all 0.2s ease;
                    ">
                        <div>
                            <p style="margin:0 0 0.5rem 0; font-size:0.95rem; color:#1e293b; font-weight:600;">
                                {insight['insight']}
                            </p>
                            <div style="margin-bottom:0.5rem;">
                                {"".join([
                                    f"<span style='background:#e2e8f0;color:#475569;margin-right:0.5rem;"
                                    f"padding:2px 6px;border-radius:4px;font-size:0.75rem;'>{tag}</span>"
                                    for tag in tags
                                ]) if tags else (
                                    "<span style='background:#f1f5f9;color:#94a3b8;margin-right:0.5rem;"
                                    "padding:2px 6px;border-radius:4px;font-size:0.75rem;'>no tag</span>"
                                )}
                            </div>
                            <p style="margin:0; font-size:0.75rem; color:#475569;">
                                <strong>Related Questions:</strong> {related_qs_str}
                            </p>
                        </div>
                    </div>
                """, unsafe_allow_html=True)

                with st.form(key=f"insight_form_{start_idx + idx}"):
                    button_clicked = st.form_submit_button(
                        "Clear Filter" if is_selected else "Filter Questions"
                    )
                    if button_clicked:
                        if is_selected:
                            st.session_state.selected_question_codes = []
                        else:
                            st.session_state.selected_question_codes = related_qs
                        st.rerun()

    # horizontal pagination buttons
    with st.container():
        pag_col1, pag_col2 = st.columns([1, 1])
        with pag_col1:
            if st.button("⬅ Previous", key="prev_page", disabled=(current_page == 0)):
                st.session_state.insights_page -= 1
                st.rerun()
        with pag_col2:
            if st.button("Next ➡", key="next_page", disabled=(current_page >= total_pages - 1)):
                st.session_state.insights_page += 1
                st.rerun()

        # styling
        st.markdown("""
            <style>
            [data-testid="baseButton-primary"][aria-label*="Filter Questions"],
            [data-testid="baseButton-primary"][aria-label*="Clear Filter"] {
                background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%) !important;
                color: white !important;
                border: none !important;
                border-radius: 999px !important;
                font-weight: 600 !important;
                font-size: 0.9rem !important;
                box-shadow: 0 4px 15px rgba(59, 130, 246, 0.3) !important;
                padding: 0.6rem 1rem !important;
                margin-top: 0.75rem !important;
                transition: all 0.2s ease !important;
            }
            [data-testid="baseButton-primary"][aria-label*="Filter Questions"]:hover,
            [data-testid="baseButton-primary"][aria-label*="Clear Filter"]:hover {
                background: linear-gradient(135deg, #2563eb 0%, #1e40af 100%) !important;
                box-shadow: 0 6px 20px rgba(59, 130, 246, 0.4) !important;
                transform: translateY(-1px);
            }
            div[data-testid="stForm"] {
                border: none !important;
                padding: 0 !important;
                margin: 0 !important;
                box-shadow: none !important;
                background: transparent !important;
            }
            [data-testid="baseButton-primary"][aria-label*="prev_page"] button,
            [data-testid="baseButton-primary"][aria-label*="next_page"] button {
                background: #f1f5f9 !important;
                color: #64748b !important;
                border: none !important;
                border-radius: 12px !important;
                font-weight: 600 !important;
                padding: 0.6rem 1.5rem !important;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1) !important;
                transition: all 0.2s ease;
                margin-right: 0.5rem !important;
                width: 100% !important;
            }
            [data-testid="baseButton-primary"][aria-label*="prev_page"] button:hover,
            [data-testid="baseButton-primary"][aria-label*="next_page"] button:hover {
                background: #e2e8f0 !important;
            }
            </style>
        """, unsafe_allow_html=True)

# Dashboard page
def dashboard_page():
    load_dashboard_css()
    data = load_full_data()

    # Initialize session state for selected questions
    if "selected_question_codes" not in st.session_state:
        st.session_state.selected_question_codes = []

    # Show page sections:
    render_header_top()
    render_header_filters()
    render_key_insights() 
    filter_values = render_filters()

    # Pass the selected codes to render_survey_questions
    shown_codes = set(st.session_state.get("selected_question_codes", []))
    render_survey_questions(data, shown_codes, filter_values)


def render_header_top():
    # Small top margin for header
    st.markdown("<div style='height: 0.5rem;'></div>", unsafe_allow_html=True)

    # Header with logo and user info
    header_col1, header_col2 = st.columns([3, 1])

    with header_col1:
        logo_col, text_col = st.columns([0.15, 0.55])
        with logo_col:
            try:
                st.image("tif.png", width=1000)
            except:
                # Fallback to icon if image not found
                st.markdown("""
                    <div style='
                        background: #3b82f6;
                        width: 50px;
                        height: 50px;
                        border-radius: 12px;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        color: white;
                        font-size: 24px;
                        margin-top: 0.25rem;
                    '>
                        <i class="fa-solid fa-chart-bar"></i>
                    </div>
                """, unsafe_allow_html=True)
        with text_col:
            st.markdown("""
                <div>
                    <h1 style='margin: 0; color: #1e293b; font-size: 1.5rem;'>Toys & Play - June 2025</h1>
                    <p style='margin: 0; color: #64748b;'>Advanced Survey Analytics</p>
                </div>
            """, unsafe_allow_html=True)

    with header_col2:
        st.markdown(f"""
            <div class="user-info" style='margin-top: 0.5rem;'>
                <div class="user-avatar" style="font-size: 1rem;">
                    {(st.session_state.username[0].upper() if 'username' in st.session_state and st.session_state.username else 'U')}
                </div>
                <div>
                    <p style='margin: 0; font-weight: 600; color: #1e293b; font-size: 0.95rem;'>
                        {st.session_state.username if 'username' in st.session_state else 'User'}
                    </p>
                    <p style='margin: 0; font-size: 0.8rem; color: #64748b;'>Research Analyst</p>
                </div>
            </div>
        """, unsafe_allow_html=True)



def render_header_filters():
    st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)

    col_left, col_right = st.columns([6, 3])

    with col_left:
        if st.button("← Back to Dashboard Hub", key="back_to_hub", type="primary"):
            st.session_state.current_page = "trackers"
            st.rerun()

    with col_right:
        sel_col1, sel_col2, badge_col = st.columns([1.2, 1.2, 2])

        with sel_col1:
            country = st.selectbox(
                "Country",
                ["UK", "US", "France", "Germany", "Spain", "Italy"],
                key="country_select"
            )
        with sel_col2:
            wave = st.selectbox(
                "Wave",
                ["Wave 1", "Wave 2", "Wave 3"],
                key="wave_select"
            )
        with badge_col:
            st.markdown(f"""
                <div style="margin-top:1.7rem;">
                    <span style="background:#fbbf24;color:#1e293b;padding:0.2rem 0.5rem;
                    border-radius:8px;font-weight:600;">{wave}</span>
                    <span style="color:#64748b;font-size:0.8rem;margin-left:0.5rem;">
                        Survey Dashboard 2025 · Uploaded: 27/06/2025
                    </span>
                </div>
            """, unsafe_allow_html=True)

    st.markdown("<hr style='margin:0.75rem 0 1rem 0; border:0; border-top:1px solid #e2e8f0;'>", unsafe_allow_html=True)


def render_filters():
    # check if we need to reset on this rerun
    if st.session_state.get("reset_filters", False):
        st.session_state.age_min = 2
        st.session_state.age_max = 9
        st.session_state.gender = "All"
        st.session_state.location = "All"
        st.session_state.income = "All"
        st.session_state.reset_filters = False  # clear the flag

    # initialize defaults if first time
    if "age_min" not in st.session_state:
        st.session_state.age_min = 2
    if "age_max" not in st.session_state:
        st.session_state.age_max = 9
    if "gender" not in st.session_state:
        st.session_state.gender = "All"
    if "location" not in st.session_state:
        st.session_state.location = "All"
    if "income" not in st.session_state:
        st.session_state.income = "All"

    with st.form("filters_form"):
        st.markdown("""
            <div style="background:#f8fafc;padding:1rem;border:1px solid #e2e8f0;
            border-radius:12px;margin-bottom:1rem;">
                <h3 style="margin:0 0 1rem 0;color:#1e293b;">Filters</h3>
            </div>
        """, unsafe_allow_html=True)

        col1, col2, col3, col4, col5 = st.columns(5)

        age_min = col1.selectbox(
            "Min Age", list(range(2, 10)),
            index=list(range(2, 10)).index(st.session_state.age_min),
            key="age_min"
        )
        age_max = col2.selectbox(
            "Max Age", list(range(2, 10)),
            index=list(range(2, 10)).index(st.session_state.age_max),
            key="age_max"
        )
        gender = col3.selectbox(
            "Gender", ["All", "Boy", "Girl"],
            index=["All", "Boy", "Girl"].index(st.session_state.gender),
            key="gender"
        )
        location_options = [
            "All", "London", "South East", "South West", "East of England", "West Midlands",
            "East Midlands", "Yorkshire and Humber", "North West", "North East", "Scotland",
            "Wales", "Northern Ireland"
        ]
        location = col4.selectbox(
            "Location", location_options,
            index=location_options.index(st.session_state.location),
            key="location"
        )
        income_options = [
            "All", "Under £25,000", "£25,000 - £39,999", "£40,000 - £59,999",
            "£60,000 - £79,999", "£80,000 - £99,999", "£100,000+", "Rather not say"
        ]
        income = col5.selectbox(
            "Income", income_options,
            index=income_options.index(st.session_state.income),
            key="income"
        )

        col_submit, col_clear = st.columns(2)
        with col_submit:
            submitted = st.form_submit_button("Apply Filters")
        with col_clear:
            clear = st.form_submit_button("Clear All")

        if clear:
            st.session_state.reset_filters = True
            st.rerun()

    # active filter display
    st.markdown(f"""
        <div style="margin:0.5rem 0;color:#64748b;">
            <strong>Active Filters:</strong> Age {age_min}-{age_max}, Gender: {gender},
            Location: {location}, Income: {income}
        </div>
    """, unsafe_allow_html=True)

    return {
        "age_min": age_min,
        "age_max": age_max,
        "gender": gender,
        "location": location,
        "income": income
    }


def render_survey_questions(data, shown_codes, filters):
    st.markdown("<h2 style='color:#1e293b;margin-top:2rem;'>Survey Questions & Results</h2>", unsafe_allow_html=True)

    # Show reset button if questions are filtered
    if shown_codes:
        if st.button("Show All Survey Questions", type="secondary"):
            st.session_state.selected_question_codes = []
            st.rerun()
        
        # Show which questions are being displayed
        st.markdown(f"""
            <p style='color:#64748b; margin-bottom: 1rem;'>
                Showing questions: {', '.join(sorted(shown_codes))}
            </p>
        """, unsafe_allow_html=True)

    questions = data.get("data", [])
    question_cols = st.columns(2)

    # Counter for column distribution
    col_idx = 0
    
    for question in questions:
        # Skip if we have filtered codes and this question isn't in them
        if shown_codes and question["code"] not in shown_codes:
            continue

        with question_cols[col_idx % 2]:
            with st.container():
                fig = render_chart(question)
                if fig:
                    st.plotly_chart(fig, use_container_width=True, key=f"{question['code']}-survey")
        
        col_idx += 1  # Only increment when we actually display a chart





def render_chart(q):
    chart_type = q.get("chartType", "bar")
    responses = q.get("responses", {})
    chart_title = q.get("question", "Chart")

    if chart_type == "bar":
        fig = px.bar(
            x=list(responses.keys()),
            y=list(responses.values()),
            color_discrete_sequence=["#0369a1"],
            title=chart_title
        )
        fig.update_layout(
            showlegend=False,
            height=350,
            margin=dict(l=20, r=20, t=40, b=40),
            plot_bgcolor="white",
            paper_bgcolor="white",
            title_x=0.01,  # left align the title
            title_font=dict(size=20, color="#0f172a"),
            xaxis=dict(
                showgrid=False,
                linecolor="#e2e8f0",
                linewidth=1,
                title="Answer",   # ← Label for X axis
                title_font=dict(size=14, color="#334155"),
                tickfont=dict(size=12, color="#475569")
            ),
            yaxis=dict(
                gridcolor="#e2e8f0",
                title="Count",    # ← Label for Y axis
                title_font=dict(size=14, color="#334155"),
                tickfont=dict(size=12, color="#475569"),
                title_standoff=15,
                automargin=True
            )
        )
        return fig

    elif chart_type == "barh" or chart_type == "horizontal_bar":
        fig = px.bar(
            x=list(responses.values()),
            y=list(responses.keys()),
            orientation="h",
            color_discrete_sequence=["#0369a1"],
            title=chart_title
        )
        fig.update_layout(
            showlegend=False,
            height=350,
            margin=dict(l=20, r=20, t=40, b=40),
            plot_bgcolor="white",
            paper_bgcolor="white",
            title_x=0.01,  # left align the title
            title_font=dict(size=20, color="#0f172a"),
            xaxis=dict(
                gridcolor="#e2e8f0",
                title="Count",    # ← X is "Count"
                title_font=dict(size=14, color="#334155"),
                tickfont=dict(size=12, color="#475569")
            ),
            yaxis=dict(
                showgrid=False,
                linecolor="#e2e8f0",
                linewidth=1,
                title="Answer",   # ← Y is "Answer"
                title_font=dict(size=14, color="#334155"),
                tickfont=dict(size=12, color="#475569"),
                automargin=True
            )
        )
        return fig

    elif chart_type == "pie":
        fig = px.pie(
            names=list(responses.keys()),
            values=list(responses.values()),
            color_discrete_sequence=px.colors.qualitative.Pastel,
            title=chart_title
        )
        fig.update_layout(
            height=350,
            margin=dict(l=20, r=20, t=40, b=40),
            paper_bgcolor="white",
            font=dict(size=12, color="#334155"),
            title_x=0.01,
            title_font=dict(size=20, color="#0f172a")
        )
        fig.update_traces(
            textposition="inside",
            textinfo="percent+label",
            hovertemplate="%{label}: %{value} (%{percent})"
        )
        return fig

    elif chart_type == "table":
        df = pd.DataFrame({
            "Label": list(responses.keys()),
            "Value": list(responses.values())
        })
        # Add a label above the table (use question text or custom)
        st.markdown(
            f"<h4 style='margin-bottom:0.5rem;color:#0f172a;font-size:25px;'>{q.get('question','Table')}</h4>",
            unsafe_allow_html=True,
        )
        st.dataframe(df, hide_index=True)
        return None  # No figure to return

    else:
        st.warning(f"Chart type '{chart_type}' is not supported yet.")
        return None




# Main app logic
def main():
    import urllib.parse
    if "selected_question_codes" not in st.session_state:
        st.session_state.selected_question_codes = []

    
    # Initialize session state ONLY here, not at the top of the file
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 'login'
    if 'dashboard_data' not in st.session_state:
        st.session_state.dashboard_data = {"settings": {"insightCards": []}, "data": []}
    if 'selected_insight' not in st.session_state:
        st.session_state.selected_insight = None
    if 'selected_tag' not in st.session_state:
        st.session_state.selected_tag = "All Insights"
    
    # NOW check query params after session state exists
    if "open" in st.query_params:
        tracker_clicked = st.query_params.get("open")
        user_passed = st.query_params.get("user")

        if user_passed:
            st.session_state.username = urllib.parse.unquote(user_passed.replace("_", " "))

        tracker_clicked = urllib.parse.unquote(tracker_clicked)
        
        # Define trackers here
        trackers = [
            {"name": "Sports Tracker", "active": False},
            {"name": "Toys & Play", "active": True},
            {"name": "Education Tracker", "active": False},
            {"name": "Health & Wellness", "active": False},
            {"name": "Consumer Behavior", "active": False}
        ]
        
        clicked_tracker = None
        for tracker in trackers:
            if tracker["name"].replace(" ", "_") == tracker_clicked:
                clicked_tracker = tracker
                break
        
        if clicked_tracker is not None and clicked_tracker["active"]:
            st.session_state.logged_in = True
            st.session_state.current_page = "dashboard"
            st.query_params.clear()
            st.rerun()

    # Now proceed with page routing
    if not st.session_state.logged_in:
        login_page()
    elif st.session_state.current_page == 'trackers':
        trackers_page()
    elif st.session_state.current_page == 'dashboard':
        dashboard_page()


if __name__ == "__main__":
    main()