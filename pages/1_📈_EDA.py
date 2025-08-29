# 📊_EDA.py
import streamlit as st
from backend import get_data  # Import our general function
import plotly.express as px
from utils import format_date_with_ordinal  # Import the helper function we need


# Set up the page
st.set_page_config(page_title="EDA - Sakila Dashboard")
st.title("📊 Exploratory Data Analysis")
st.write("This is the EDA page. Let's test the database connection.")


# # Page title
# st.title("Basic EDA Page")
# # Write a simple query
# query = "SELECT * FROM actor ORDER BY last_name LIMIT 10;"

# # Create a button
# if st.button("Get Actor Data"):
#     # When the button is clicked, run the query
#     result_df = get_data(query)
    
#     # Show the result as a table
#     st.write("Here is the data from the Actor table:")
#     st.dataframe(result_df) # This creates the interactive table

st.divider()

# Create an expander to keep the test neat
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

# 2. Main Query for the Line Plot
st.subheader("Daily Rentals by Store in 2005")

query = """
SELECT
    DATE(rental_date) AS rental_day,
    store_id,
    COUNT(rental_id) AS rental_count
FROM
    rental
JOIN
    inventory USING (inventory_id)
WHERE
    EXTRACT(YEAR FROM rental_date) = 2005  -- CHANGED HERE for PostgreSQL
GROUP BY
    rental_day, store_id
ORDER BY
    rental_day;
"""

# Fetch the data
df = get_data(query)

# 3. Create and display the interactive Plotly chart

# First, calculate the date range for the title
# Use the imported function from utils.py
start_date = format_date_with_ordinal(df['rental_day'].min())
end_date = format_date_with_ordinal(df['rental_day'].max())
date_range_str = f"{start_date} to {end_date}"

fig = px.line(
    df,
    x='rental_day',
    y='rental_count',
    color='store_id',
    title=f'Daily Rentals by Store in 2005 ({date_range_str})',
    labels={
        'rental_day': 'Date',
        'rental_count': 'Number of Rentals',
        'store_id': 'Store ID'
    }
)
fig.update_layout(hovermode='x unified')
st.plotly_chart(fig, use_container_width=True)

# 4. Data Summary
st.subheader("2005 Data Summary")

# Find the peak day for each store
peak_day_store1 = df[df['store_id'] == 1].sort_values('rental_count', ascending=False).iloc[0]
peak_day_store2 = df[df['store_id'] == 2].sort_values('rental_count', ascending=False).iloc[0]

# Format the date range nicely (e.g., "May 24 - Aug 23")
start_date = df['rental_day'].min().strftime('%b %d') # e.g., "May 24"
end_date = df['rental_day'].max().strftime('%b %d')   # e.g., "Aug 23"
date_range_str = f"{start_date} - {end_date}"

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Rental Days", df['rental_day'].nunique())

with col2:
    st.metric("Store 1: Peak Day", f"{peak_day_store1['rental_count']} rentals")
    st.write(f"*on {peak_day_store1['rental_day']}*")

with col3:
    st.metric("Store 2: Peak Day", f"{peak_day_store2['rental_count']} rentals")
    st.write(f"*on {peak_day_store2['rental_day']}*")

# =======

st.divider()

# 5. Bar Plot: Total Revenue by Store
st.subheader("Revenue Comparison")

# Write the new query for total revenue (it's the same query, the name is what changes)
revenue_query = """
SELECT
    s.store_id,
    SUM(p.amount) AS total_revenue
FROM
    payment p
JOIN
    rental r ON p.rental_id = r.rental_id
JOIN
    inventory i ON r.inventory_id = i.inventory_id
JOIN
    store s ON i.store_id = s.store_id
GROUP BY
    s.store_id
ORDER BY
    s.store_id;
"""

# Fetch the data
revenue_df = get_data(revenue_query)

# Display the results as a df (only to test)
# st.write("**Total Revenue per Store:**")
# st.dataframe(revenue_df)


# 6. Create and display the interactive Bar Chart

revenue_df['store_id'] = revenue_df['store_id'].astype(str)

# Create the bar chart with Plotly
fig_bar = px.bar(
    revenue_df,
    x='store_id',
    y='total_revenue',
    title='Total Revenue by Store',
    labels={
        'store_id': 'Store ID',
        'total_revenue': 'Total Revenue ($)'
    },
    color='store_id',
    color_discrete_sequence=px.colors.qualitative.Bold,  # Use a qualitative color scheme
    text_auto='.2s'  # This automatically formats the numbers on the bars (e.g., 30K)
)

# Improve the layout: Format the y-axis to show dollar signs and improve the text on bars
fig_bar.update_layout(
    yaxis_tickprefix='$', 
    yaxis_tickformat=',.0f',
    showlegend=True  # Hides the legend since the colors are self-explanatory
)
fig_bar.update_traces(texttemplate='$%{value:,.0f}', textposition='outside') # Precise $ amount on bars

# === Extra lines and annotations ===
max_revenue = revenue_df['total_revenue'].max()
min_revenue = revenue_df['total_revenue'].min()
min_store = revenue_df.loc[revenue_df['total_revenue'].idxmin(), 'store_id']

# Horizontal dotted line at max revenue
fig_bar.add_hline(y=max_revenue, line_dash="dot", line_color="red")

# Vertical line from min revenue bar to max line
fig_bar.add_shape(
    type="line",
    x0=min_store, x1=min_store,
    y0=min_revenue, y1=max_revenue,
    line=dict(color="red", width=2, dash="dot")
)

# Add annotation with diff + percent
diff = max_revenue - min_revenue
percent_diff = (diff / min_revenue) * 100
fig_bar.add_annotation(
    x=min_store,
    y=(min_revenue + max_revenue) / 2,
    text=f"Diff: ${diff:,.0f} ({percent_diff:.1f}%)",
    showarrow=False,
    font=dict(color="red", size=12)
)

# Display the chart
st.plotly_chart(fig_bar, use_container_width=True)


# =====

# Show a simple metric
total_revenue = revenue_df['total_revenue'].sum()
# st.metric("Total Revenue from Both Stores", f"${total_revenue:,.2f}")


# 7. Centered Metric
# st.subheader("")  # Add some space

# Create a centered layout using columns
col1, col2, col3 = st.columns([1, 2, 1])  # Middle column is twice as wide

with col2:  # This puts the content only in the middle column
    # Use HTML to make the label smaller and centered
    st.markdown(
        """
        <div style='text-align: center;'>
            <h4 style='font-size: 1rem; margin-bottom: 0.5rem;'>Total Revenue from Both Stores</h4>
        </div>
        """, 
        unsafe_allow_html=True
    )
    # Display the metric (the number will automatically be prominent)
    st.metric("", f"${total_revenue:,.2f}")

st.subheader("")  # Add some space at the bottom


# ======

st.divider()


# 8. Top 5 Movies by Store
st.subheader("Top 5 Most Rented Movies by Store (2005)")

top_movies_query = """
WITH ranked_movies AS (
    SELECT 
        i.store_id,
        f.film_id,
        f.title,
        COUNT(r.rental_id) AS rental_count,
        ROW_NUMBER() OVER (PARTITION BY i.store_id ORDER BY COUNT(r.rental_id) DESC) AS movie_rank
    FROM 
        rental r
    JOIN 
        inventory i ON r.inventory_id = i.inventory_id
    JOIN 
        film f ON i.film_id = f.film_id
    WHERE 
        EXTRACT(YEAR FROM r.rental_date) = 2005  -- CHANGED HERE for PostgreSQL
    GROUP BY 
        i.store_id, f.film_id, f.title
)
SELECT 
    store_id,
    film_id,
    title,
    rental_count,
    movie_rank
FROM 
    ranked_movies
WHERE 
    movie_rank <= 5
ORDER BY 
    store_id, movie_rank;
"""

# Fetch the data
top_movies_df = get_data(top_movies_query)

# Display the results
st.dataframe(top_movies_df)

# Add some summary metrics
st.write("**Summary:**")
for store_id in sorted(top_movies_df['store_id'].unique()):
    store_movies = top_movies_df[top_movies_df['store_id'] == store_id]
    top_movie = store_movies[store_movies['movie_rank'] == 1].iloc[0]
    st.write(f"**Store {store_id}**: '{top_movie['title']}' was the most rented movie with {top_movie['rental_count']} rentals.")

