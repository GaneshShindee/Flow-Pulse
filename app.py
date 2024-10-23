from supabase import create_client
import pandas as pd 
import streamlit as st 
import plotly.express as px
import time

# Supabase credentials
API_URL = 'https://bolsgescbuufddyjwxqb.supabase.co'
API_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJvbHNnZXNjYnV1ZmRkeWp3eHFiIiwicm9sZSI6ImFub24iLCJpYXQiOjE3Mjg4MTAwNzIsImV4cCI6MjA0NDM4NjA3Mn0.AL-ESq9iKFceAtaActhElvxPzkU6VFQ40IVdANWubEU'
supabase = create_client(API_URL, API_KEY)

# Set up the Streamlit app layout
st.set_page_config(page_title="Flow Rate Dashboard", layout='centered', initial_sidebar_state='collapsed')

# Auto-refresh loop
while True:
    # Fetch data from Supabase
    supabase_list = supabase.table('maintable').select('*').execute().data

    # Create DataFrame from fetched data
    df = pd.DataFrame(supabase_list)

    # Convert created_at to datetime and extract date and time
    df['created_at'] = pd.to_datetime(df['created_at'])
    df['DateTime'] = df['created_at']
    df['date'] = df['created_at'].dt.date
    df['time'] = df['created_at'].dt.time

    # Filter out rows where flow rates are zero or missing
    df_filtered = df[(df['flow_rate_1'] > 0) & (df['flow_rate_2'] > 0)]

    # Plot Flow Rate Sensor 1
    st.markdown('### Flow Rate Sensor 1')
    fig1 = px.line(df_filtered, x='DateTime', y='flow_rate_1', title='Flow Rate 1', markers=True)
    st.plotly_chart(fig1, use_container_width=True)

    # Plot Flow Rate Sensor 2
    st.markdown('### Flow Rate Sensor 2')
    fig2 = px.line(df_filtered, x='DateTime', y='flow_rate_2', title='Flow Rate 2', markers=True)
    st.plotly_chart(fig2, use_container_width=True)

    # Plot Flow Rate Difference
    st.markdown('### Flow Rate Difference')
    df_filtered['flow_diff'] = df_filtered['flow_rate_1'] - df_filtered['flow_rate_2']
    fig3 = px.line(df_filtered, x='DateTime', y='flow_diff', title='Flow Rate Difference', markers=True)
    st.plotly_chart(fig3, use_container_width=True)

    # Refresh every second
    time.sleep(1)
    st.experimental_rerun()
