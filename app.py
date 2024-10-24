from supabase import create_client
import pandas as pd
import streamlit as st
import plotly.express as px

# Supabase credentials
API_URL = 'https://bolsgescbuufddyjwxqb.supabase.co'
API_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJvbHNnZXNjYnV1ZmRkeWp3eHFiIiwicm9sZSI6ImFub24iLCJpYXQiOjE3Mjg4MTAwNzIsImV4cCI6MjA0NDM4NjA3Mn0.AL-ESq9iKFceAtaActhElvxPzkU6VFQ40IVdANWubEU'
supabase = create_client(API_URL, API_KEY)

# Fetch data from Supabase
supabase_list = supabase.table('maintable').select('*').execute().data

# Check if data is returned from Supabase
if supabase_list is None or len(supabase_list) == 0:
    st.error("No data returned from Supabase")
else:
    # Create DataFrame from fetched data
    df = pd.DataFrame(supabase_list)

    # Check if the necessary columns exist in the DataFrame
    required_columns = ['created_at', 'flow_rate_1', 'flow_rate_2']
    if all(col in df.columns for col in required_columns):
        
        # Convert 'created_at' to datetime and create 'DateTime', 'date', and 'time' columns
        df['created_at'] = pd.to_datetime(df['created_at'], errors='coerce')  # Convert, ignore errors
        df['DateTime'] = df['created_at']
        df['date'] = df['created_at'].dt.date
        df['time'] = df['created_at'].dt.time

        # Set up the Streamlit app layout
        st.set_page_config(page_title="Flow Rate Dashboard", layout='centered', initial_sidebar_state='collapsed')

        # Plot Flow Rate Sensor 1
        st.markdown('### Flow Rate Sensor 1')
        fig1 = px.line(df, x='DateTime', y='flow_rate_1', title='Flow Rate 1', markers=True)
        st.plotly_chart(fig1, use_container_width=True)

        # Plot Flow Rate Sensor 2
        st.markdown('### Flow Rate Sensor 2')
        fig2 = px.line(df, x='DateTime', y='flow_rate_2', title='Flow Rate 2', markers=True)
        st.plotly_chart(fig2, use_container_width=True)

        # Calculate flow rate difference and plot
        df['flow_diff'] = df['flow_rate_1'] - df['flow_rate_2']
        st.markdown('### Flow Rate Difference')
        fig3 = px.line(df, x='DateTime', y='flow_diff', title='Flow Rate Difference', markers=True)
        st.plotly_chart(fig3, use_container_width=True)

        # Logic to check if flow difference is less than 20
        if (df['flow_diff'].abs() < 20).any():
            st.warning("Flow rate difference is less than 20 for some entries. Sending notification email...")
            
            # Add your email notification logic here

    else:
        st.error(f"Required columns {required_columns} not found in the data!")

