### Dashboard View Modes

The dashboard supports multiple view modes:

1. **Compact View**: Shows summary metrics and key charts
2. **Detailed View**: Displays all survey questions with full visualizations
3. **Filtered View**: Shows only charts related to selected insights or tags

Click the view toggle buttons in the top-right to switch between modes.# Survey Dashboard Hub - Streamlit App

A modern, professional survey analytics dashboard built with Streamlit, featuring advanced data visualization for children's toy preferences and market research insights.

## Features

- **Secure Login**: Clean authentication interface with centered login form
- **Dashboard Hub**: Central location to access different survey trackers
- **Advanced Dashboard Layout**:
  - Sidebar with downloads and podcast summary sections
  - Dynamic insight cards with category tags
  - Interactive filters for Age and Gender
  - Wave selector for different survey periods
  - Chart view customization based on selected insights
- **Interactive Visualizations**: 
  - Dynamic Plotly charts
  - Multiple chart types (bar, pie, line)
  - Export and zoom capabilities
- **Modern UI/UX**: 
  - Professional design matching enterprise dashboards
  - Smooth transitions and hover effects
  - Color-coded insight categories
  - Responsive layout
- **Data Management**: 
  - Full report PDF download
  - Raw data CSV export
  - 10+ insights with drill-down capabilities

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. File Structure

Ensure your project directory contains:
```
project_folder/
│
├── app.py                                    # Main Streamlit application
├── generated_toy_dashboard_June2025_CLEANED.json  # Data file
└── requirements.txt                          # Python dependencies
```

### 3. Run the Application

```bash
streamlit run app.py
```

The app will open in your default browser at `http://localhost:8501`

## Usage

### Login
- Enter any username and password to access the dashboard
- User info appears in the top-right corner after login

### Tracker Selection
- View key metrics: Total Trackers, Surveys, Responses, and Active Trackers
- Three tracker options available:
  - Sports Tracker (Coming Soon)
  - Toys & Play (Active)
  - Education Tracker (Coming Soon)
- Click "Open Toys & Play Dashboard" to access the analytics

### Dashboard Features

#### Sidebar
- **Downloads**: Export full report PDF or raw CSV data
- **Podcast Summary**: Access audio discussions

#### Main Dashboard
- **Key Insights**: 
  - View top 3 of 10 available insights
  - Click insights to filter related charts
  - Filter by tags: All Insights, Play Patterns, Discovery, Values, Behavior, Trends
  
- **Filters Section**:
  - Age filter: All Age, 3-5, 6-7, 8-9
  - Gender filter: All Gender, Male, Female
  
- **Survey Results**:
  - Interactive charts for each survey question
  - Chart actions: Change type, sort, download, save image, zoom
  - Dynamic display based on selected insights

- **Wave Selector**: 
  - Switch between different survey periods
  - View comparative data across waves

### Dashboard View Modes

The dashboard supports multiple view modes:

1. **Compact View**: Shows summary metrics and key charts (default)
2. **Detailed View**: Displays all survey questions with full visualizations
3. **Filtered View**: Shows only charts related to selected insights or tags

Use the view toggle buttons (💠 Compact / 📊 Detailed) to switch between modes.

## Customization

### Styling
- Modify the CSS in the `st.markdown()` section for custom branding
- Update color schemes:
  - Primary blue: `#4A90E2` 
  - Success green: `#4CAF50`
  - Tag colors defined in CSS classes (`.tag-play`, `.tag-discovery`, etc.)
- Adjust card shadows and hover effects in `.insight-card` and `.tracker-card` classes

### Data Integration
- Replace `generated_toy_dashboard_June2025_CLEANED.json` with your survey data
- Follow the JSON structure:
  ```json
  {
    "settings": {
      "insightCards": [...],
      "layout": {...}
    },
    "data": [
      {
        "code": "Q001",
        "question": "Question text",
        "type": "categorical",
        "chartType": "bar",
        "responses": {...}
      }
    ]
  }
  ```

### Adding New Trackers
1. Update `trackers_page()` to add new tracker cards
2. Create a new dashboard function (e.g., `sports_dashboard_page()`)
3. Add routing logic in `main()` function
4. Design tracker-specific insights and visualizations

### Insight Categories
- Add new categories by updating the tag list and CSS classes
- Define category colors in the stylesheet
- Map insights to appropriate related questions

## Troubleshooting

### Common Issues

1. **Data file not found error**:
   - Ensure `generated_toy_dashboard_June2025_CLEANED.json` is in the same directory as `app.py`
   - The app includes fallback sample data if the file is missing

2. **Charts not displaying**:
   - Check that Plotly is properly installed: `pip install plotly>=5.17.0`
   - Verify your browser supports WebGL for Plotly rendering

3. **Login not working**:
   - Current implementation accepts any username/password
   - Check browser console for JavaScript errors

4. **Styling issues**:
   - Clear browser cache
   - Ensure you're using a modern browser (Chrome, Firefox, Safari, Edge)

5. **Session state errors**:
   - Restart the Streamlit server
   - Clear cookies for localhost:8501

## Production Deployment

### Recommended Deployment Options

1. **Streamlit Cloud** (easiest):
   ```bash
   # Push to GitHub, then deploy via streamlit.io
   ```

2. **Docker**:
   ```dockerfile
   FROM python:3.9-slim
   WORKDIR /app
   COPY requirements.txt .
   RUN pip install -r requirements.txt
   COPY . .
   CMD ["streamlit", "run", "app.py"]
   ```

3. **Cloud Platforms**:
   - AWS EC2 with nginx reverse proxy
   - Google Cloud Run
   - Azure App Service

### Security Considerations

- Implement proper authentication (OAuth2, SAML, etc.)
- Use environment variables for sensitive data
- Enable HTTPS with SSL certificates
- Add rate limiting for API endpoints
- Implement user role-based access control
- Sanitize user inputs and file uploads

### Performance Optimization

- **Caching**: Use `@st.cache_data` for data loading functions
- **Lazy Loading**: Load charts only when visible
- **Data Pagination**: For large datasets, implement pagination
- **Optimize Images**: Compress logos and backgrounds
- **Minimize Re-renders**: Use session state effectively

## License

This project is available for educational and commercial use. Please customize it to meet your specific survey analytics needs.

## Best Practices Implemented

1. **Professional UI Design**: 
   - Enterprise-grade dashboard layout
   - Consistent color schemes and spacing
   - Intuitive navigation flow
   
2. **Advanced State Management**: 
   - Persistent selections across page navigation
   - Dynamic content updates without page reload
   - Filter state preservation
   
3. **Interactive Elements**:
   - Clickable insight cards for data filtering
   - Hover effects and visual feedback
   - Multiple chart interaction options
   
4. **Data Visualization**:
   - Appropriate chart types for different data
   - Consistent color coding
   - Clear labeling and legends
   
5. **User Experience**:
   - Clear visual hierarchy
   - Contextual information display
   - Smooth transitions between views
   
6. **Responsive Design**:
   - Flexible grid layouts
   - Adaptive component sizing
   - Mobile-friendly interface

## Future Enhancements

- **Authentication**: Implement OAuth or SSO for enterprise security
- **Real-time Updates**: Connect to live data sources for automatic refresh
- **Advanced Analytics**:
  - Cross-question correlation analysis
  - Predictive insights using ML
  - Trend analysis across waves
- **Customization**:
  - User-specific dashboard layouts
  - Custom insight creation
  - Saved filter presets
- **Export Options**:
  - PowerPoint presentation generation
  - Scheduled report delivery
  - API access for external tools
- **Additional Trackers**:
  - Complete Sports Tracker implementation
  - Education Tracker with learning analytics
  - Custom tracker creation interface
- **Collaboration Features**:
  - Share insights with team members
  - Commenting on specific data points
  - Version control for reports