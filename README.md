# Medicaid DQ Atlas - Demo Streamlit Application

A beautiful and interactive Streamlit application inspired by the official Medicaid Data Quality (DQ) Atlas. This demo app provides comprehensive data quality assessments for Medicaid and CHIP data across states.

## Features

- **Welcome Dashboard**: Overview of key metrics and features
- **Data Quality Dashboard**: Interactive visualizations and state-level quality assessments
- **State Comparisons**: Side-by-side comparison of data quality metrics between states
- **Trends Over Time**: Historical analysis of data quality trends
- **About Page**: Information about the DQ Atlas mission and methodology

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

## Installation

1. **Clone or navigate to the project directory**:
   ```bash
   cd /Users/pawanpreet.sangari/demo_deploy_ui_streamlit_app
   ```

2. **Create a virtual environment (recommended)**:
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**:
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```

4. **Install required packages**:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

1. **Start the Streamlit app**:
   ```bash
   streamlit run app.py
   ```

2. **Access the application**:
   - The app will automatically open in your default browser
   - If not, navigate to: `http://localhost:8501`

## Usage

### Navigation
Use the sidebar to navigate between different pages:
- 🏠 **Welcome**: Introduction and overview
- 📊 **Data Quality Dashboard**: Explore state-level quality metrics with interactive filters
- 🗺️ **State Comparisons**: Compare data quality between two states
- 📈 **Trends Over Time**: View historical trends and patterns
- 📖 **About**: Learn more about the DQ Atlas

### Interactive Features
- **Filters**: Select specific states and quality ratings
- **Visualizations**: Interactive charts with hover tooltips
- **Comparisons**: Side-by-side state comparisons with radar charts
- **Metrics**: Real-time metric calculations and summaries

## Data

This demo uses randomly generated sample data for demonstration purposes. The metrics include:
- Enrollment Completeness
- Claims Accuracy
- Provider Data Quality
- Demographic Data Quality
- Overall Quality Score

## Customization

To customize the application:
1. Modify the sample data generation in `app.py`
2. Update the color scheme in the custom CSS section
3. Add new pages or visualizations as needed
4. Replace sample data with real data sources

## Project Structure

```
demo_deploy_ui_streamlit_app/
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

## Dependencies

- **streamlit**: Web application framework
- **pandas**: Data manipulation and analysis
- **plotly**: Interactive visualizations
- **numpy**: Numerical computing

## Troubleshooting

### Port already in use
If port 8501 is already in use, run:
```bash
streamlit run app.py --server.port 8502
```

### Package installation issues
If you encounter issues installing packages, try upgrading pip:
```bash
pip install --upgrade pip
```

### Browser doesn't open automatically
Manually navigate to `http://localhost:8501` in your browser.

## Reference

This application is inspired by the official Medicaid DQ Atlas:
- Official Site: https://www.medicaid.gov/dq-atlas/welcome

## License

This is a demo application created for educational and testing purposes.

## Support

For questions or issues with this demo application, please refer to the Streamlit documentation:
- Streamlit Docs: https://docs.streamlit.io

