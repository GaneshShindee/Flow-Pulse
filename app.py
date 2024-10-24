# from supabase import create_client
# import pandas as pd
# import streamlit as st
# import plotly.express as px

# # Supabase credentials
# API_URL = 'https://bolsgescbuufddyjwxqb.supabase.co'
# API_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJvbHNnZXNjYnV1ZmRkeWp3eHFiIiwicm9sZSI6ImFub24iLCJpYXQiOjE3Mjg4MTAwNzIsImV4cCI6MjA0NDM4NjA3Mn0.AL-ESq9iKFceAtaActhElvxPzkU6VFQ40IVdANWubEU'
# supabase = create_client(API_URL, API_KEY)

# # Fetch data from Supabase and debug if data is fetched properly
# try:
#     supabase_list = supabase.table('maintable').select('*').execute().data
#     if not supabase_list:
#         st.error("No data fetched from Supabase.")
#         st.stop()
# except Exception as e:
#     st.error(f"Error fetching data: {e}")
#     st.stop()

# # Create DataFrame from fetched data
# try:
#     df = pd.DataFrame(supabase_list)
#     st.write("Data fetched successfully:", df.head())  # Display top of the data for debugging
# except Exception as e:
#     st.error(f"Error creating DataFrame: {e}")
#     st.stop()

# # Check if required columns are present
# required_columns = ['created_at', 'flow_rate_1', 'flow_rate_2']
# missing_columns = [col for col in required_columns if col not in df.columns]
# if missing_columns:
#     st.error(f"Missing required columns: {missing_columns}")
#     st.stop()

# # Convert created_at to datetime and extract date and time
# df['created_at'] = pd.to_datetime(df['created_at'], errors='coerce')
# if df['created_at'].isnull().all():
#     st.error("All 'created_at' values are invalid or missing.")
#     st.stop()

# df['DateTime'] = df['created_at']
# df['date'] = df['created_at'].dt.date
# df['time'] = df['created_at'].dt.time

# # Set up the Streamlit app layout
# st.set_page_config(page_title="Flow Rate Dashboard", layout='centered', initial_sidebar_state='collapsed')

# # Plot Flow Rate Sensor 1
# st.markdown('### Flow Rate Sensor 1')
# try:
#     fig1 = px.line(df, x='DateTime', y='flow_rate_1', title='Flow Rate 1', markers=True)
#     st.plotly_chart(fig1, use_container_width=True)
# except Exception as e:
#     st.error(f"Error plotting Flow Rate Sensor 1: {e}")

# # Plot Flow Rate Sensor 2
# st.markdown('### Flow Rate Sensor 2')
# try:
#     fig2 = px.line(df, x='DateTime', y='flow_rate_2', title='Flow Rate 2', markers=True)
#     st.plotly_chart(fig2, use_container_width=True)
# except Exception as e:
#     st.error(f"Error plotting Flow Rate Sensor 2: {e}")

# # Plot Flow Rate Difference
# st.markdown('### Flow Rate Difference')
# try:
#     df['flow_diff'] = df['flow_rate_1'] - df['flow_rate_2']
#     fig3 = px.line(df, x='DateTime', y='flow_diff', title='Flow Rate Difference', markers=True)
#     st.plotly_chart(fig3, use_container_width=True)
# except Exception as e:
#     st.error(f"Error plotting Flow Rate Difference: {e}")
