import streamlit as st
import pandas as pd
import plotly.express as px

# Load the data
data_path = 'unemployment.csv'  # Replace with your file path if needed
data = pd.read_csv(data_path)

# Rename columns for easier handling
data.columns = [
    "States", "Date", "Frequency",
    "Estimated Unemployment Rate", "Estimated Employed",
    "Estimated Labour Participation Rate", "Region",
    "Longitude", "Latitude"
]

# Strip whitespace from 'Date' column
data['Date'] = data['Date'].str.strip()

# Convert 'Date' to datetime
data['Date'] = pd.to_datetime(data['Date'], format='%d-%m-%Y')

# Streamlit App

st.title('Unemployment Analysis in India')
st.markdown("""### Welcome to the Unemployment Analysis Dashboard
This interactive application is developed by Dibyanshi Singh. Explore the dynamic changes in unemployment rates across various regions and states of India during the Covid-19 pandemic. Dive into the data and uncover trends through various time periods.
""")
# Sidebar filters

# Sidebar filters
st.sidebar.header('Filter Options')

states = st.sidebar.multiselect(
    'Select States',
    options=data['States'].unique(),
    default=data['States'].unique()
)

regions = st.sidebar.multiselect(
    'Select Regions',
    options=data['Region'].unique(),
    default=data['Region'].unique()
)

# Set start_date and end_date using min and max from the data
date_range = st.sidebar.date_input(
    "Select Date Range",
    value=[data['Date'].min().date(), data['Date'].max().date()],
    format="YYYY-MM-DD"
)

# Ensure both dates are selected
if isinstance(date_range, tuple) and len(date_range) == 2:
    start_date, end_date = date_range
else:
    st.error("Please select a valid date range.")
    st.stop()

# Filter data based on sidebar inputs
filtered_data = data[
    (data['States'].isin(states)) &
    (data['Region'].isin(regions)) &
    (data['Date'] >= pd.to_datetime(start_date)) &
    (data['Date'] <= pd.to_datetime(end_date))
]

# Display filtered data
st.dataframe(filtered_data)

# Unemployment Rate over Time
st.subheader('Unemployment Rate Over Time')
fig = px.line(
    filtered_data,
    x='Date',
    y='Estimated Unemployment Rate',
    color='States',
    title='Estimated Unemployment Rate Over Time'
)
st.plotly_chart(fig)

# Employment Distribution with adjustable bins
st.subheader('Estimated Employed by Region')

# Add a slider to let the user control the number of bins
bins = st.slider('Number of Bins', min_value=5, max_value=100, value=20)

# Plot the histogram with the selected number of bins
fig2 = px.histogram(
    filtered_data,
    x='Estimated Employed',
    color='Region',
    nbins=bins,  # Setting the number of bins dynamically
    title='Estimated Employed Distribution by Region'
)

# Optionally, you can set range limits for the x-axis (employment numbers)
fig2.update_layout(
    xaxis_title='Estimated Employed',
    yaxis_title='Count',
    xaxis=dict(range=[filtered_data['Estimated Employed'].min(), filtered_data['Estimated Employed'].max()])
)

st.plotly_chart(fig2)


# Sunburst Chart for Unemployment Rate
st.subheader('Unemployment Rate by Region and State')
fig3 = px.sunburst(
    filtered_data,
    path=['Region', 'States'],
    values='Estimated Unemployment Rate',
    title='Unemployment Rate by Region and State'
)
st.plotly_chart(fig3)
@st.cache
def convert_df(df):
    return df.to_csv(index=False).encode('utf-8')

csv = convert_df(filtered_data)
st.download_button("Download Filtered Data", data=csv, file_name='filtered_unemployment.csv')

# Display raw data toggle
if st.checkbox("Show Raw Data"):
    st.write(filtered_data)
