
from datetime import datetime
from plotly.subplots import make_subplots
from scipy.stats import zscore
from utils.data_loader import load_data
import ast
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import pytz
import streamlit as st

df = load_data()
st.title("DAX Trends: A Temporal Analysis")

st.markdown("""
    This page provides an in-depth examination of how DAX
    usage has evolved over time. Our analysis encompasses:
    
    - Temporal patterns in DAX query frequency
    - Evolution of DAX function utilization and query complexity
    - Community engagement metrics
    - Industry-specific DAX adoption rates
    - Longitudinal changes in response quality and resolution times
    
    Through these data visualizations, we aim to offer valuable insights into the dynamic landscape of DAX usage and the 
    growth of the DAX community. This analysis serves as a resource for both DAX novices and experts, informing professional 
    development paths and deepening understanding of DAX's role in contemporary data analysis.

""")

st.markdown("---")

st.header("📊 DAX Question Trends Over Time")

df['Asked Date'] = pd.to_datetime(df['Asked Date'])
questions_over_time = df.groupby(df['Asked Date'].dt.to_period('M')).size().reset_index(name='Count')
questions_over_time['Asked Date'] = questions_over_time['Asked Date'].dt.to_timestamp()

fig = px.line(questions_over_time, x='Asked Date', y='Count', 
              title="DAX Questions: Historical Trend Analysis",
              labels={'Count': 'Number of Questions', 'Asked Date': 'Date'})

fig.update_traces(line_color='#1f77b4', line_width=2)
fig.update_layout(
    xaxis_title="Date",
    yaxis_title="Number of Questions",
    hovermode="x unified",
    template="plotly_white"
)

fig.add_trace(go.Scatter(
    x=questions_over_time['Asked Date'],
    y=questions_over_time['Count'],
    mode='markers',
    marker=dict(color='#1f77b4', size=4),
    showlegend=False
))

st.plotly_chart(fig, use_container_width=True)

st.markdown("""
This visualization illustrates the trend of DAX-related questions over time. The line graph represents the monthly 
count of questions asked, providing insights into the growing interest and adoption of DAX.

""")

st.markdown("---")

st.write("")

def get_main_timezones():
    return [
        'UTC', 'America/New_York', 'America/Chicago', 'America/Denver', 'America/Los_Angeles',
        'America/Anchorage', 'America/Vancouver', 'America/Toronto', 'America/Mexico_City',
        'America/Phoenix', 'America/Havana', 'America/Puerto_Rico',
        'America/Sao_Paulo', 'America/Buenos_Aires', 'America/Santiago', 'America/Lima',
        'America/Bogota', 'America/Caracas',
        'Europe/London', 'Europe/Paris', 'Europe/Berlin', 'Europe/Rome', 'Europe/Madrid',
        'Europe/Moscow', 'Europe/Istanbul', 'Europe/Stockholm', 'Europe/Amsterdam',
        'Europe/Athens', 'Europe/Dublin', 'Europe/Lisbon', 'Europe/Vienna',
        'Africa/Cairo', 'Africa/Lagos', 'Africa/Johannesburg', 'Africa/Nairobi',
        'Africa/Casablanca', 'Africa/Accra', 'Africa/Addis_Ababa', 'Africa/Harare',
        'Asia/Dubai', 'Asia/Jerusalem', 'Asia/Riyadh', 'Asia/Tehran', 'Asia/Baghdad',
        'Asia/Kolkata', 'Asia/Bangkok', 'Asia/Singapore', 'Asia/Tokyo', 'Asia/Seoul',
        'Asia/Shanghai', 'Asia/Hong_Kong', 'Asia/Taipei', 'Asia/Manila', 'Asia/Jakarta',
        'Asia/Kuala_Lumpur', 'Asia/Ho_Chi_Minh', 'Asia/Kathmandu', 'Asia/Dhaka',
        'Asia/Karachi', 'Asia/Tashkent',
        'Australia/Sydney', 'Australia/Melbourne', 'Australia/Perth', 'Australia/Brisbane',
        'Pacific/Auckland', 'Pacific/Fiji', 'Pacific/Guam', 'Pacific/Honolulu',
        'Atlantic/Azores', 'America/St_Johns', 'Pacific/Kiritimati', 'Indian/Maldives',
        'Antarctica/McMurdo'
    ]

def convert_hour(utc_hour, local_tz):
    if pd.isna(utc_hour):
        return pd.NaT
    utc_time = datetime.now(pytz.UTC).replace(hour=int(utc_hour), minute=0, second=0, microsecond=0)
    local_time = utc_time.astimezone(local_tz)
    return local_time.hour

with st.container(border=True):
    st.subheader("⏰ Temporal Analysis of DAX Q&A Activity")

    st.markdown("""
    This visualization provides insights into the patterns of DAX-related questions and answers. 
    It allows you to observe when questions are most frequently asked and when they receive their highest-scored answers.
    """)

    df['Asked Hour'] = pd.to_datetime(df['Asked Date']).dt.hour
    df['Answered Hour'] = pd.to_datetime(df['Highest Score Answer Date']).dt.hour

    main_timezones = get_main_timezones()
    selected_timezone = st.selectbox('Select your timezone:', main_timezones)

    local_tz = pytz.timezone(selected_timezone)

    asked_hour_freq = df['Asked Hour'].value_counts().sort_index().reset_index()
    asked_hour_freq.columns = ['Hour', 'Asked Frequency']
    answered_hour_freq = df['Answered Hour'].value_counts().sort_index().reset_index()
    answered_hour_freq.columns = ['Hour', 'Answered Frequency']

    asked_hour_freq['Local Hour'] = asked_hour_freq['Hour'].apply(lambda x: convert_hour(x, local_tz))
    answered_hour_freq['Local Hour'] = answered_hour_freq['Hour'].apply(lambda x: convert_hour(x, local_tz))

    asked_local_hour_freq = asked_hour_freq.groupby('Local Hour')['Asked Frequency'].sum().reset_index()
    answered_local_hour_freq = answered_hour_freq.groupby('Local Hour')['Answered Frequency'].sum().reset_index()

    fig = go.Figure()

    fig.add_trace(go.Scatter(x=asked_local_hour_freq['Local Hour'], y=asked_local_hour_freq['Asked Frequency'],
                             mode='lines', name='Questions Asked', line=dict(color='#1f77b4', width=2)))
    
    fig.add_trace(go.Scatter(x=answered_local_hour_freq['Local Hour'], y=answered_local_hour_freq['Answered Frequency'],
                             mode='lines', name='Highest Scored Answers', line=dict(color='#2ca02c', width=2)))

    fig.update_layout(
        title=f'DAX Activity Distribution by Hour ({selected_timezone})',
        xaxis_title='Hour of Day (Local Time)',
        yaxis_title='Frequency',
        xaxis=dict(tickmode='linear', tick0=0, dtick=1),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        template="plotly_white"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.info("💡 **Insight:** Compare the timing of questions (blue) with their highest-scored answers (green) to identify optimal periods for engagement in the DAX community.")

    st.markdown("---")

    df['Asked Date'] = pd.to_datetime(df['Asked Date'])
    df['Highest Score Answer Date'] = pd.to_datetime(df['Highest Score Answer Date'])

    if df['Asked Date'].dt.tz is None:
        df['Asked Date'] = df['Asked Date'].dt.tz_localize('UTC').dt.tz_convert(local_tz)
    else:
        df['Asked Date'] = df['Asked Date'].dt.tz_convert(local_tz)

    if df['Highest Score Answer Date'].dt.tz is None:
        df['Highest Score Answer Date'] = df['Highest Score Answer Date'].dt.tz_localize('UTC').dt.tz_convert(local_tz)
    else:
        df['Highest Score Answer Date'] = df['Highest Score Answer Date'].dt.tz_convert(local_tz)

    df['Asked Day'] = df['Asked Date'].dt.day_name()
    df['Asked Hour'] = df['Asked Date'].dt.hour
    df['Answered Day'] = df['Highest Score Answer Date'].dt.day_name()
    df['Answered Hour'] = df['Highest Score Answer Date'].dt.hour

    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

    asked_heatmap = df.groupby(['Asked Day', 'Asked Hour']).size().unstack(fill_value=0).reindex(day_order)
    answered_heatmap = df.groupby(['Answered Day', 'Answered Hour']).size().unstack(fill_value=0).reindex(day_order)

    fig = go.Figure(data=[
        go.Heatmap(z=asked_heatmap.values, x=asked_heatmap.columns, y=asked_heatmap.index,
                colorscale='Blues', name='Questions Asked'),
        go.Heatmap(z=answered_heatmap.values, x=answered_heatmap.columns, y=answered_heatmap.index,
                colorscale='Greens', name='Answers Received', visible='legendonly')
    ])

    fig.update_layout(
        title='Weekly Heatmap of DAX Q&A Activity',
        xaxis_title='Hour of Day',
        yaxis_title='Day of Week',
        yaxis=dict(tickmode='array', tickvals=list(range(len(day_order))), ticktext=day_order),
        template="plotly_white"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.markdown("""
    This heatmap visualizes the distribution of DAX questions and answers throughout the week. 
    It provides insights into peak activity times and helps identify patterns in community engagement.

    
    """)

st.write("")
