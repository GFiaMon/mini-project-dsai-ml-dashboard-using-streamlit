# 📊_EDA.py
import streamlit as st

from ui import plot_daily_rentals, plot_revenue_by_store, show_top_movies
from backend import get_data  # Only needed for the connection test

# import plotly.express as px
# from utils import format_date_with_ordinal  # Import the helper function we need


# Set up the page
st.set_page_config(page_title="EDA - Sakila Dashboard")
st.title("📊 Exploratory Data Analysis")
st.write("This is the EDA page. Let's test the database connection.")

st.divider()

# 1. Connection Test Expander
with st.expander("🔧 Database Connection Test - Actor Table"):
    st.write("""
    **Test Description:** 
    This simple test runs the query `SELECT * FROM actor ORDER BY last_name LIMIT 10;` to see if we can successfully connect to the Sakila database and retrieve data.
    """)
    
    # The button to run the test
    if st.button("Run Test Query", key="test_button"):
        
        # Show a spinner while the query runs (for a better user experience)
        with st.spinner('Running query... Please wait.'):
            # Define the simple test query
            test_query = "SELECT * FROM actor ORDER BY last_name LIMIT 10;"
            
            try:
                # Use our general function from backend.py to get the data
                df_actors = get_data(test_query)
                
                # If successful, display a success message and the data
                st.success("✅ Database connection successful! Query executed.")
                st.write(f"**Number of rows returned:** {len(df_actors)}")
                
                # Display the dataframe as an interactive table
                st.dataframe(df_actors)
                
            except Exception as e:
                # If there's an error, display it clearly
                st.error(f"❌ Connection failed. Error: {e}")
                st.info("""
                **Troubleshooting Tips:**
                1. Is your MySQL server running?
                2. Are the credentials in your `.env` file correct?
                3. Is the Sakila database installed?
                """)

st.divider()

# ================

# 2. Daily Rentals Plot
st.header("Daily Rentals by Store in 2005")
plot_daily_rentals()  # This now handles both plot AND metrics

# 3. Revenue Plot
st.header("Revenue Analysis")
plot_revenue_by_store()  # This now handles both plot AND metrics

# 4. Top Movies
st.header("Top 5 Most Rented Movies by Store")
show_top_movies()  # This now handles both dataframe AND metrics

