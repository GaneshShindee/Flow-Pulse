from supabase import create_client
import pandas as pd 
import streamlit as st 
import plotly.express as px
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Supabase credentials
API_URL = 'https://bolsgescbuufddyjwxqb.supabase.co'
API_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJvbHNnZXNjYnV1ZmRkeWp3eHFiIiwicm9zZSI6ImFub24iLCJpYXQiOjE3Mjg4MTAwNzIsImV4cCI6MjA0NDM4NjA3Mn0.AL-ESq9iKFceAtaActhElvxPzkU6VFQ40IVdANWubEU'
supabase = create_client(API_URL, API_KEY)

# Email credentials
EMAIL_ADDRESS = 'ganeshshinde0100@gmail.com'  # Your email
EMAIL_PASSWORD = 'Ganesh@143'  # Your email password (or app password)

# Function to send email notification
def send_email(flow_rate_1, flow_rate_2, flow_diff):
    recipient_email = 'ganeshfromsawari@gmail.com'  # Replace with recipient's email

    subject = 'Flow Rate Alert'
    body = f"""
    Alert! The following flow rate conditions have been met:
    
    Flow Rate Sensor 1: {flow_rate_1}
    Flow Rate Sensor 2: {flow_rate_2}
    Flow Rate Difference: {flow_diff}

    Please check the system.
    """

    msg = MIMEMultipart()
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = recipient_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(msg)
        print("Email sent successfully.")
    except Exception as e:
        print(f"Failed to send email: {e}")

# Fetch data from Supabase
supabase_list = supabase.table('maintable').select('*').execute().data

# Create DataFrame from fetched data
df = pd.DataFrame(supabase_list)

# Convert created_at to datetime and extract date and time
df['created_at'] = pd.to_datetime(df['created_at'])
df['DateTime'] = df['created_at']
df['date'] = df['created_at'].dt.date
df['time'] = df['created_at'].dt.time

# Set up the Streamlit app layout
st.set_page_config(page_title="Flow Rate Dashboard", layout='centered', initial_sidebar_state='collapsed')

st.markdown('### Flow Rate Sensor 1')
fig1 = px.line(df, x='DateTime', y='flow_rate_1', title='Flow Rate 1', markers=True)
st.plotly_chart(fig1, use_container_width=True)

st.markdown('### Flow Rate Sensor 2')
fig2 = px.line(df, x='DateTime', y='flow_rate_2', title='Flow Rate 2', markers=True)
st.plotly_chart(fig2, use_container_width=True)

st.markdown('### Flow Rate Difference')
df['flow_diff'] = df['flow_rate_1'] - df['flow_rate_2']
fig3 = px.line(df, x='DateTime', y='flow_diff', title='Flow Rate Difference', markers=True)
st.plotly_chart(fig3, use_container_width=True)

# Check flow rates and send email if conditions are met
if not df.empty:
    latest_row = df.iloc[-1]
    flow_rate_1 = latest_row['flow_rate_1']
    flow_rate_2 = latest_row['flow_rate_2']
    flow_diff = latest_row['flow_diff']

    if flow_rate_1 > 1 and flow_diff > 30:
        send_email(flow_rate_1, flow_rate_2, flow_diff)
