# ui.py
import streamlit as st
import plotly.express as px
import pandas as pd  
from backend import get_data
from utils import format_date_with_ordinal

# ==============

# helper functions

def _show_daily_rentals_metrics(df):
    """Show metrics for daily rentals plot (matches original design)"""
    st.subheader("2005 Performance Summary")
    peak_day_store1 = df[df['store_id'] == 1].sort_values('rental_count', ascending=False).iloc[0]
    peak_day_store2 = df[df['store_id'] == 2].sort_values('rental_count', ascending=False).iloc[0]

    # Format the date range nicely (e.g., "May 24 - Aug 23") - YOUR ORIGINAL CODE
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

def _show_revenue_metrics(df):
    """Show centered revenue metric with border (matches your design)"""
    total_revenue = df['total_revenue'].sum()
    
    # Create a centered layout using columns
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col2:  # This puts the content only in the middle column
        container = st.container(border=True)
        # Display the metric (the number will automatically be prominent)
        container.metric("Total Revenue from both stores", f"${total_revenue:,.2f}")
    
    st.subheader("")  # Add some space at the bottom

def _show_top_movies_metrics(df):
    """Show metrics for top movies"""
    st.write("**Summary:**")
    for store_id in sorted(df['store_id'].unique()):
        store_movies = df[df['store_id'] == store_id]
        top_movie = store_movies[store_movies['movie_rank'] == 1].iloc[0]
        st.write(f"**Store {store_id}**: '{top_movie['title']}' was the most rented movie with {top_movie['rental_count']} rentals.")


# ==============
# Plot 1: LINE PLOT that displays the daily rentals

def plot_daily_rentals():
    """Creates and displays the daily rentals line plot"""
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
    
    df = get_data(query)

    # Convert to datetime if needed (SQLite returns strings, PostgreSQL returns dates)
    if df['rental_day'].dtype == 'object':
        df['rental_day'] = pd.to_datetime(df['rental_day'])
    
    # Format dates with ordinal suffixes for the title
    start_date = format_date_with_ordinal(df['rental_day'].min())
    end_date = format_date_with_ordinal(df['rental_day'].max())
    date_range_str = f"{start_date} to {end_date}"
    
    
    # 3. Create and display the interactive Plotly chart
    fig = px.line(
        df,
        x='rental_day',
        y='rental_count',
        color='store_id',
        title=f'Daily Rentals by Store in 2005 ({date_range_str})',  # <-- Formatted title
        labels={
            'rental_day': 'Date',
            'rental_count': 'Number of Rentals',
            'store_id': 'Store ID'
        }
    )
    fig.update_layout(hovermode='x unified')
    st.plotly_chart(fig, use_container_width=True)
    
    # Show metrics using the helper function
    _show_daily_rentals_metrics(df)
    
    return df


# ==============
# Plot 2: BAR PLOT that displays the revenue

def plot_revenue_by_store():
    """Creates and displays the revenue bar plot and metrics"""
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

    # Show metrics using the helper function
    _show_revenue_metrics(revenue_df)
    
    return revenue_df


# ==============
# Plot 2b: Top movies dataframe (Table) with streamlit:

def plot_revenue_by_store_st():
    """Creates and displays the revenue bar plot using st.bar_chart with two colors"""
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
    
    # RESHAPE THE DATA - This is the key trick!
    # Create a DataFrame where each store is a separate column
    chart_df = revenue_df.set_index('store_id').T  # Transpose the data
    
    # Now st.bar_chart will see two different series and use different colors!
    st.bar_chart(chart_df, height=400)
    
    # Add title
    st.markdown("### Total Revenue by Store")
    
    # Show metrics using the helper function
    _show_revenue_metrics(revenue_df)
    
    return revenue_df


# ==============
# Plot 3: Top movies dataframe (Table)

def show_top_movies():
    """Displays the top movies dataframe"""
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

    st.dataframe(top_movies_df)

    # Show metrics using the helper function
    _show_top_movies_metrics(top_movies_df)

    return top_movies_df