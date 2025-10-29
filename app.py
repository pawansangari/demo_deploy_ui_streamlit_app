import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# Set page configuration
st.set_page_config(
    page_title="Medicaid DQ Atlas",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main {
        padding: 0rem 1rem;
    }
    .stTitle {
        color: #003D7A;
        font-size: 2.5rem !important;
        font-weight: 700 !important;
    }
    .stHeader {
        color: #003D7A;
    }
    .info-box {
        padding: 1.5rem;
        border-radius: 0.5rem;
        background-color: #f0f8ff;
        border-left: 5px solid #003D7A;
        margin-bottom: 1rem;
    }
    .metric-card {
        background-color: #ffffff;
        padding: 1.5rem;
        border-radius: 0.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    </style>
""", unsafe_allow_html=True)

# Generate sample data
@st.cache_data
def load_state_data():
    states = ["Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", 
              "Connecticut", "Delaware", "Florida", "Georgia", "Hawaii", "Idaho",
              "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana"]
    
    data = {
        "State": states,
        "Enrollment Completeness": np.random.randint(75, 98, len(states)),
        "Claims Accuracy": np.random.randint(70, 95, len(states)),
        "Provider Data Quality": np.random.randint(80, 99, len(states)),
        "Demographic Data Quality": np.random.randint(85, 100, len(states)),
        "Overall Score": np.random.randint(75, 95, len(states))
    }
    
    df = pd.DataFrame(data)
    
    # Add quality rating based on overall score
    def get_rating(score):
        if score >= 90:
            return "Low Concern"
        elif score >= 80:
            return "Medium Concern"
        else:
            return "High Concern"
    
    df["Quality Rating"] = df["Overall Score"].apply(get_rating)
    return df

@st.cache_data
def load_metrics_over_time():
    dates = pd.date_range(start='2023-01', end='2024-12', freq='M')
    data = {
        "Date": dates,
        "Enrollment": np.random.randint(85, 95, len(dates)) + np.sin(np.arange(len(dates))) * 2,
        "Claims": np.random.randint(80, 92, len(dates)) + np.sin(np.arange(len(dates))) * 3,
        "Provider": np.random.randint(88, 97, len(dates)) + np.sin(np.arange(len(dates))) * 2,
    }
    return pd.DataFrame(data)

# Sidebar navigation
st.sidebar.image("https://via.placeholder.com/200x80/003D7A/FFFFFF?text=DQ+Atlas", use_column_width=True)
st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Select a page:",
    ["🏠 Welcome", "📊 Data Quality Dashboard", "🗺️ State Comparisons", "📈 Trends Over Time", "📖 About"]
)

# Add filters in sidebar
st.sidebar.markdown("---")
st.sidebar.subheader("Filters")

# Welcome Page
if page == "🏠 Welcome":
    st.title("Welcome to the Medicaid Data Quality (DQ) Atlas")
    
    st.markdown("""
    <div class="info-box">
    <h3>About the DQ Atlas</h3>
    <p>The Data Quality Atlas is a comprehensive platform for monitoring and analyzing the quality of 
    Medicaid and CHIP data across all states. This tool helps stakeholders assess data completeness, 
    accuracy, and reliability to support better decision-making and program management.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Key metrics overview
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(label="States Monitored", value="50+", delta="All US States")
    
    with col2:
        st.metric(label="Data Elements", value="1,000+", delta="Comprehensive Coverage")
    
    with col3:
        st.metric(label="Average Quality Score", value="88%", delta="2.3% ↑")
    
    with col4:
        st.metric(label="Last Updated", value="Oct 2024", delta="Monthly Updates")
    
    st.markdown("---")
    
    # Features section
    st.subheader("Key Features")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 📊 Comprehensive Assessments
        - Enrollment data quality metrics
        - Claims accuracy assessments
        - Provider information completeness
        - Demographic data validation
        """)
        
        st.markdown("""
        ### 🗺️ State-by-State Analysis
        - Compare quality metrics across states
        - Identify areas for improvement
        - Track progress over time
        """)
    
    with col2:
        st.markdown("""
        ### 📈 Trend Analysis
        - Historical data quality trends
        - Seasonal patterns identification
        - Predictive insights
        """)
        
        st.markdown("""
        ### 💡 Actionable Insights
        - Data-driven recommendations
        - Best practice sharing
        - Quality improvement strategies
        """)

# Data Quality Dashboard
elif page == "📊 Data Quality Dashboard":
    st.title("Data Quality Dashboard")
    st.markdown("Explore comprehensive data quality assessments across states.")
    
    df = load_state_data()
    
    # Filter options
    col1, col2 = st.columns([3, 1])
    with col1:
        selected_states = st.multiselect(
            "Filter by States:",
            options=df["State"].tolist(),
            default=df["State"].head(5).tolist()
        )
    
    with col2:
        quality_filter = st.selectbox(
            "Quality Rating:",
            ["All", "Low Concern", "Medium Concern", "High Concern"]
        )
    
    # Apply filters
    filtered_df = df[df["State"].isin(selected_states)] if selected_states else df
    if quality_filter != "All":
        filtered_df = filtered_df[filtered_df["Quality Rating"] == quality_filter]
    
    # Display summary statistics
    st.subheader("Summary Statistics")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Avg Enrollment Quality", f"{filtered_df['Enrollment Completeness'].mean():.1f}%")
    with col2:
        st.metric("Avg Claims Accuracy", f"{filtered_df['Claims Accuracy'].mean():.1f}%")
    with col3:
        st.metric("Avg Provider Quality", f"{filtered_df['Provider Data Quality'].mean():.1f}%")
    with col4:
        st.metric("Avg Overall Score", f"{filtered_df['Overall Score'].mean():.1f}%")
    
    st.markdown("---")
    
    # Data table
    st.subheader("State Data Quality Scores")
    st.dataframe(
        filtered_df.style.background_gradient(
            subset=['Enrollment Completeness', 'Claims Accuracy', 'Provider Data Quality', 'Overall Score'],
            cmap='RdYlGn',
            vmin=70,
            vmax=100
        ),
        height=400
    )
    
    # Visualizations
    st.markdown("---")
    st.subheader("Data Quality Visualizations")
    
    tab1, tab2, tab3 = st.tabs(["📊 Bar Chart", "🗺️ Heatmap", "📉 Distribution"])
    
    with tab1:
        # Bar chart
        fig = px.bar(
            filtered_df,
            x="State",
            y=["Enrollment Completeness", "Claims Accuracy", "Provider Data Quality"],
            title="Data Quality Metrics by State",
            labels={"value": "Quality Score (%)", "variable": "Metric"},
            barmode="group",
            color_discrete_sequence=["#003D7A", "#00A6D6", "#82C341"]
        )
        fig.update_layout(height=500, xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        # Heatmap
        heatmap_data = filtered_df[["State", "Enrollment Completeness", "Claims Accuracy", 
                                     "Provider Data Quality", "Demographic Data Quality"]].set_index("State").T
        fig = px.imshow(
            heatmap_data,
            labels=dict(x="State", y="Metric", color="Score"),
            color_continuous_scale="RdYlGn",
            aspect="auto",
            title="Data Quality Heatmap"
        )
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        # Distribution
        fig = px.histogram(
            filtered_df,
            x="Overall Score",
            nbins=20,
            title="Distribution of Overall Quality Scores",
            labels={"Overall Score": "Quality Score", "count": "Number of States"},
            color_discrete_sequence=["#003D7A"]
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)

# State Comparisons
elif page == "🗺️ State Comparisons":
    st.title("State-by-State Comparisons")
    st.markdown("Compare data quality metrics between selected states.")
    
    df = load_state_data()
    
    # State selection
    col1, col2 = st.columns(2)
    with col1:
        state_1 = st.selectbox("Select First State:", df["State"].tolist(), index=0)
    with col2:
        state_2 = st.selectbox("Select Second State:", df["State"].tolist(), index=1)
    
    # Get data for selected states
    state_1_data = df[df["State"] == state_1].iloc[0]
    state_2_data = df[df["State"] == state_2].iloc[0]
    
    # Comparison metrics
    st.subheader("Quick Comparison")
    col1, col2, col3, col4 = st.columns(4)
    
    metrics = ["Enrollment Completeness", "Claims Accuracy", "Provider Data Quality", "Overall Score"]
    
    for i, (col, metric) in enumerate(zip([col1, col2, col3, col4], metrics)):
        with col:
            val1 = state_1_data[metric]
            val2 = state_2_data[metric]
            delta = val1 - val2
            st.metric(
                label=metric,
                value=f"{val1}%",
                delta=f"{delta:+.1f}% vs {state_2}"
            )
    
    st.markdown("---")
    
    # Radar chart comparison
    st.subheader("Comprehensive Comparison")
    
    categories = ["Enrollment\nCompleteness", "Claims\nAccuracy", "Provider\nData Quality", "Demographic\nData Quality"]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=[state_1_data["Enrollment Completeness"], state_1_data["Claims Accuracy"],
           state_1_data["Provider Data Quality"], state_1_data["Demographic Data Quality"]],
        theta=categories,
        fill='toself',
        name=state_1,
        line_color='#003D7A'
    ))
    
    fig.add_trace(go.Scatterpolar(
        r=[state_2_data["Enrollment Completeness"], state_2_data["Claims Accuracy"],
           state_2_data["Provider Data Quality"], state_2_data["Demographic Data Quality"]],
        theta=categories,
        fill='toself',
        name=state_2,
        line_color='#00A6D6'
    ))
    
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
        showlegend=True,
        height=500,
        title="Radar Chart Comparison"
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Detailed comparison table
    st.subheader("Detailed Metrics")
    comparison_df = pd.DataFrame({
        "Metric": metrics,
        state_1: [state_1_data[m] for m in metrics],
        state_2: [state_2_data[m] for m in metrics],
        "Difference": [state_1_data[m] - state_2_data[m] for m in metrics]
    })
    
    st.dataframe(
        comparison_df.style.background_gradient(
            subset=[state_1, state_2],
            cmap='RdYlGn',
            vmin=70,
            vmax=100
        )
    )

# Trends Over Time
elif page == "📈 Trends Over Time":
    st.title("Data Quality Trends Over Time")
    st.markdown("Analyze how data quality metrics have evolved over time.")
    
    trends_df = load_metrics_over_time()
    
    # Metric selection
    metric_view = st.selectbox(
        "Select Metric to Visualize:",
        ["All Metrics", "Enrollment", "Claims", "Provider"]
    )
    
    # Time series plot
    st.subheader("Historical Trends")
    
    if metric_view == "All Metrics":
        fig = px.line(
            trends_df,
            x="Date",
            y=["Enrollment", "Claims", "Provider"],
            title="Data Quality Trends (All Metrics)",
            labels={"value": "Quality Score (%)", "variable": "Metric"},
            color_discrete_sequence=["#003D7A", "#00A6D6", "#82C341"]
        )
    else:
        fig = px.line(
            trends_df,
            x="Date",
            y=metric_view,
            title=f"Data Quality Trend - {metric_view}",
            labels={metric_view: "Quality Score (%)"},
            color_discrete_sequence=["#003D7A"]
        )
    
    fig.update_layout(height=500, hovermode='x unified')
    st.plotly_chart(fig, use_container_width=True)
    
    # Statistics
    st.markdown("---")
    st.subheader("Trend Statistics")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Latest Enrollment Score", f"{trends_df['Enrollment'].iloc[-1]:.1f}%",
                 delta=f"{trends_df['Enrollment'].iloc[-1] - trends_df['Enrollment'].iloc[-6]:.1f}% (6M)")
    
    with col2:
        st.metric("Latest Claims Score", f"{trends_df['Claims'].iloc[-1]:.1f}%",
                 delta=f"{trends_df['Claims'].iloc[-1] - trends_df['Claims'].iloc[-6]:.1f}% (6M)")
    
    with col3:
        st.metric("Latest Provider Score", f"{trends_df['Provider'].iloc[-1]:.1f}%",
                 delta=f"{trends_df['Provider'].iloc[-1] - trends_df['Provider'].iloc[-6]:.1f}% (6M)")
    
    # Year-over-year comparison
    st.markdown("---")
    st.subheader("Year-over-Year Comparison")
    
    yoy_data = {
        "Metric": ["Enrollment", "Claims", "Provider"],
        "2023 Average": [87.5, 84.3, 91.2],
        "2024 Average": [89.2, 86.1, 92.8],
        "Change": ["+1.7%", "+1.8%", "+1.6%"]
    }
    yoy_df = pd.DataFrame(yoy_data)
    st.dataframe(yoy_df)

# About Page
elif page == "📖 About":
    st.title("About the DQ Atlas")
    
    st.markdown("""
    <div class="info-box">
    <h3>Mission Statement</h3>
    <p>The Medicaid Data Quality Atlas serves as a comprehensive resource for assessing and improving 
    the quality of Medicaid and CHIP data. Our mission is to provide transparent, actionable insights 
    that support better program management and improved outcomes for beneficiaries.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("What is the DQ Atlas?")
        st.markdown("""
        The Data Quality (DQ) Atlas is an interactive platform that:
        
        - **Monitors** data quality across all states
        - **Identifies** areas requiring improvement
        - **Tracks** progress over time
        - **Provides** actionable recommendations
        - **Supports** data-driven decision making
        """)
        
        st.subheader("Data Sources")
        st.markdown("""
        Our assessments are based on:
        
        - Transformed Medicaid Statistical Information System (T-MSIS)
        - State-submitted data files
        - Quality validation processes
        - Automated data quality checks
        """)
    
    with col2:
        st.subheader("Quality Metrics")
        st.markdown("""
        We evaluate data across multiple dimensions:
        
        - **Completeness**: Presence of required data elements
        - **Accuracy**: Correctness of reported information
        - **Consistency**: Alignment across data sources
        - **Timeliness**: Currency of reported data
        - **Validity**: Conformance to expected ranges
        """)
        
        st.subheader("Contact & Resources")
        st.markdown("""
        For more information:
        
        - 📧 Email: dqatlas@cms.hhs.gov
        - 🌐 Website: medicaid.gov/dq-atlas
        - 📄 Documentation: Available in Resources section
        - 🤝 Technical Support: 1-800-XXX-XXXX
        """)
    
    st.markdown("---")
    
    st.info("💡 **Note**: This is a demo application created for testing purposes. " + 
            "For official Medicaid DQ Atlas data, please visit https://www.medicaid.gov/dq-atlas/welcome")

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #666; padding: 1rem;'>
    <p>Medicaid Data Quality Atlas | Demo Application | Last Updated: October 2024</p>
    </div>
""", unsafe_allow_html=True)

