# Survey Dashboard Hub

A modern, interactive analytics dashboard built with Streamlit for visualizing and exploring survey data. This tool provides an intuitive interface for research analysts to dive deep into survey insights with powerful filtering and visualization capabilities.

**Live Demo**: [[YOUR_STREAMLIT_CLOUD_LINK_HERE]](https://trackertools-ejnvpojv.streamlit.app/)

## Table of Contents
- [Features](#features)
- [Installation](#installation)
- [Navigation Guide](#navigation-guide)
  - [Login Page](#login-page)
  - [Trackers Selection Page](#trackers-selection-page)
  - [Dashboard Page](#dashboard-page)
- [Data Structure](#data-structure)
- [Customization](#customization)
- [Deployment](#deployment)
- [Contributing](#contributing)

## Features

- 🔐 **Secure Login System** - Simple authentication for accessing the dashboard
- 📊 **Multiple Tracker Support** - Organize different survey topics (Sports, Toys, Education, etc.)
- 🎯 **Smart Insights** - AI-generated key insights with question filtering
- 📈 **Interactive Visualizations** - Bar charts, pie charts, horizontal bars, and tables
- 🔍 **Advanced Filtering** - Filter by age, gender, location, and income
- 📱 **Responsive Design** - Works seamlessly on desktop and tablet devices
- 🎨 **Modern UI/UX** - Clean, professional interface with smooth animations

## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Local Setup

1. Clone the repository:
```bash
git clone <your-repository-url>
cd survey-dashboard-hub
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `requirements.txt` file with:
```
streamlit==1.32.0
pandas==2.2.0
plotly==5.19.0
```

5. Run the application:
```bash
streamlit run app.py
```

## Navigation Guide

### Login Page

The login page is your entry point to the dashboard:

- **Username/Password**: Enter any credentials (authentication is simulated)
- **Sign In Button**: Redirects to the Trackers Selection page
- **Design**: Clean, centered login form with the TIF logo

![Login Flow]
```
Login → Enter Credentials → Sign In → Trackers Page
```

### Trackers Selection Page

This is your hub for accessing different survey trackers:

**Main Components:**
1. **Header Section**
   - TIF logo and title
   - User profile display (shows logged-in username)
   
2. **Available Trackers Grid**
   - **Sports Tracker** - Track children's sports participation (Coming Soon)
   - **Toys & Play** - Monitor toy preferences and play patterns (Active)
   - **Education Tracker** - Analyze learning preferences (Coming Soon)
   - **Health & Wellness** - Track health habits and nutrition (Coming Soon)
   - **Consumer Behavior** - Understand purchasing decisions (Coming Soon)

3. **Research Solutions Section**
   - Attitude and Usage studies
   - Brand Health Check
   - Brand Lift measurements
   - Innovation testing

**Navigation:**
- Click "Open Dashboard" on the Toys & Play tracker to access the dashboard
- Other trackers show "Coming Soon" status

### Dashboard Page

The main analytics interface with three key sections:

#### 1. Header and Controls
- **Back Button**: Return to Trackers page
- **Country Selector**: Choose between UK, US, France, Germany, Spain, Italy
- **Wave Selector**: Select Wave 1, 2, or 3
- **User Info**: Displays current user profile

#### 2. Key Insights Section
**Features:**
- **Category Filter**: All, Play Patterns, Discovery, Values, Demographics, etc.
- **Insight Cards**: Display key findings with:
  - Main insight text
  - Related tags
  - Related question codes
  - "Filter Questions" button
- **Pagination**: Navigate through insights with Previous/Next buttons

**How to Use:**
1. Select a category to filter insights
2. Click "Filter Questions" on any insight card to show only related survey questions
3. Use pagination to browse through all insights
4. Click "Clear Filter" to remove question filtering

#### 3. Filters Section
**Available Filters:**
- **Age Range**: Min Age (2-9), Max Age (2-9)
- **Gender**: All, Boy, Girl
- **Location**: UK regions including London, Scotland, Wales, etc.
- **Income**: Various income brackets from Under £25,000 to £100,000+

**Filter Actions:**
- **Apply Filters**: Update the displayed data
- **Clear All**: Reset all filters to defaults

#### 4. Survey Questions & Results
**Visualization Types:**
- **Bar Charts**: Standard vertical bars for categorical data
- **Horizontal Bar Charts**: For binary comparisons
- **Pie Charts**: For distribution visualization
- **Tables**: For detailed seasonal or multi-category data

**Features:**
- Questions arranged in a 2-column grid
- Each chart shows question title and response counts
- Filtered view shows only selected questions
- "Show All Survey Questions" button to reset filtering

## Data Structure

The dashboard uses a JSON file (`toy_dashboard_data.json`) with the following structure:

### Root Structure
```json
{
  "settings": {
    "title": "June 2025",
    "layout": {...},
    "insightCards": [...]
  },
  "data": [...]
}
```

### Settings Object

#### insightCards Array
Each insight card contains:
```json
{
  "insight": "Main insight text displayed on the card",
  "relatedQuestions": ["Q001", "Q002"],  // Question codes to filter
  "category": ["Play Patterns"],         // Categories for filtering
  "tags": ["Favorite Toy", "Age"]       // Display tags
}
```

### Data Array

Each survey question object:
```json
{
  "code": "Q001",                    // Unique question identifier
  "question": "Age",                 // Display title
  "type": "categorical",             // Question type
  "respondents": 500,                // Total respondents
  "chartType": "bar",                // Visualization type
  "responses": {                     // Response data
    "3": 74,
    "4": 66,
    "5": 74
  }
}
```

### Supported Chart Types
- `"bar"` - Vertical bar chart
- `"barh"` or `"horizontal_bar"` - Horizontal bar chart
- `"pie"` - Pie chart
- `"table"` - Data table

## Customization

### Adding New Trackers

1. Update the `trackers` list in `trackers_page()`:
```python
{
    "name": "New Tracker",
    "description": "Description here",
    "icon_color": "#3b82f6",
    "bg_color": "#dbeafe",
    "icon": "fa-solid fa-icon-name",
    "active": True,  # Set to True to enable
    "surveys": "10",
    "responses": "2,000",
    "updated": "1 day ago"
}
```

2. Create a new JSON data file for the tracker
3. Update the dashboard logic to load the appropriate data

### Adding New Insights

Add to the `insightCards` array in your JSON:
```json
{
  "insight": "Your new insight text here",
  "relatedQuestions": ["Q005", "Q006"],
  "category": ["New Category"],
  "tags": ["Tag1", "Tag2"]
}
```

### Modifying Survey Questions

Add new questions to the `data` array:
```json
{
  "code": "Q030",
  "question": "Your Question Title",
  "type": "categorical",
  "respondents": 500,
  "chartType": "bar",
  "responses": {
    "Option 1": 150,
    "Option 2": 200,
    "Option 3": 150
  }
}
```

## Deployment

### Deploying to Streamlit Community Cloud

1. **Prepare Your Repository**
   - Ensure your GitHub repository contains:
     - `app.py` (main application file)
     - `toy_dashboard_data.json` (data file)
     - `requirements.txt` (dependencies)
     - `tif.png` (logo file, optional)

2. **Create Streamlit Cloud Account**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Sign in with your GitHub account

3. **Deploy Your App**
   - Click "New app"
   - Select your repository
   - Choose branch (usually `main`)
   - Set main file path: `app.py`
   - Click "Deploy"

4. **Environment Setup**
   - The app will automatically install dependencies from `requirements.txt`
   - Deployment typically takes 2-3 minutes

5. **Access Your App**
   - Your app will be available at:
     ```
     https://[your-github-username]-[repository-name]-[branch]-[random-string].streamlit.app
     ```

### Configuration Tips

- **Secrets Management**: Use Streamlit secrets for sensitive data
- **Resource Limits**: Free tier provides 1GB RAM and 1GB storage
- **Custom Domain**: Available with Streamlit Cloud Teams plan

## Contributing

### Adding Features

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes
4. Test thoroughly
5. Submit a pull request

### Code Style

- Follow PEP 8 for Python code
- Use meaningful variable names
- Comment complex logic
- Update documentation for new features

### Testing Checklist

- [ ] Login functionality works
- [ ] All navigation links function correctly
- [ ] Filters apply and reset properly
- [ ] Charts render correctly
- [ ] Insight filtering works as expected
- [ ] Responsive design on different screen sizes

## Troubleshooting

### Common Issues

1. **Import Errors**
   - Ensure all packages in requirements.txt are installed
   - Check Python version compatibility

2. **Data Not Loading**
   - Verify `toy_dashboard_data.json` is in the same directory as `app.py`
   - Check JSON syntax is valid

3. **Charts Not Displaying**
   - Confirm Plotly is installed correctly
   - Check browser console for JavaScript errors

4. **Styling Issues**
   - Clear browser cache
   - Ensure Font Awesome CDN is accessible

### Support

For issues or questions:
1. Check existing GitHub issues
2. Create a new issue with:
   - Description of the problem
   - Steps to reproduce
   - Expected vs actual behavior
   - Screenshots if applicable
