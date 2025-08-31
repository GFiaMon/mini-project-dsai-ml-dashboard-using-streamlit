# backend.py

import streamlit as st

# 1. Import necessary libraries
from sqlalchemy.exc import SQLAlchemyError  # <-- ADD THIS LINE
import pandas as pd
from sqlalchemy import create_engine


# Libraries for the ML model
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


# backend.py
def get_engine():
    """
    Creates a SQLAlchemy engine for PostgreSQL using the Supabase connection string.
    """
    # Get the complete connection string from environment variable
    # connection_string = os.getenv('SUPABASE_CONNECTION_STRING')
    connection_string = st.secrets['SUPABASE_CONNECTION_STRING']

    
    if not connection_string:
        raise ValueError("❌ SUPABASE_CONNECTION_STRING not found in environment variables")
    
    # Create and return the engine
    engine = create_engine(connection_string)
    return engine

@st.cache_data
def get_data(query):
    """
    A general function to execute an SQL query and return a DataFrame.
    
    Parameters:
    query (str): The SQL query to execute.
    
    Returns:
    pandas.DataFrame: A DataFrame containing the results of the query.
    
    Raises:
    Exception: If there is an error connecting to the database or executing the query.
    """
    engine = get_engine()
    try:
        # Use pandas to run the query and get the result directly as a DataFrame
        df = pd.read_sql_query(query, engine)
        print("✅ Query executed successfully!")
        return df
    
    except SQLAlchemyError as e:
        # This will catch errors related to the database operation
        error = str(e.__dict__['orig'])
        print(f"❌ Database error: {error}")
        raise Exception(f"Database error: {error}")
    except Exception as e:
        # This will catch any other errors
        print(f"❌ An unexpected error occurred: {e}")
        raise Exception(f"An unexpected error occurred: {e}")
    finally:
        # This code runs whether the try block was successful or not
        # It ensures the database connection is always closed
        engine.dispose()
        print("Database connection closed.")


# ===============================


def get_movie_descriptions():
    """
    Fetches all movies with their title, description, rating, and category.
    Returns: A pandas DataFrame.
    """
    query = """
    SELECT 
        f.film_id, 
        f.title, 
        f.description, 
        f.rating,
        c.name as category  -- Be explicit with table aliases
    FROM 
        film f
    JOIN
        film_category fc ON f.film_id = fc.film_id  -- Use ON instead of USING
    JOIN
        category c ON fc.category_id = c.category_id  -- Use ON instead of USING
    WHERE 
        f.description IS NOT NULL;
    """
    
    df = get_data(query)
    return df

# ===============================


# Loads the movie data and prepares the model.
@st.cache_resource
def setup_recommendation_engine():
    """
    Loads the movie data and prepares the AI model for recommendations.
    Returns: 
        model: The SentenceTransformer model
        df: DataFrame with movie information
        embeddings: Numerical vectors of all movie descriptions
    """
    # 1. Load the movie data
    df = get_movie_descriptions()
    
    # 2. Load the AI model (this might take a moment first time)
    model = SentenceTransformer('all-MiniLM-L6-v2')
    
    # 3. Convert all descriptions to numerical vectors (embeddings)
    embeddings = model.encode(df['description'].tolist())
    
    return model, df, embeddings

# Finds the movies
def find_similar_movies(user_input, model, df, embeddings, top_n=3):
    """
    Finds movies most similar to the user's input description.
    """
    # 1. Convert user input to numerical vector
    input_embedding = model.encode([user_input])
    
    # 2. Calculate similarity between input and all movies
    similarities = cosine_similarity(input_embedding, embeddings)
    
    # 3. Get indices of top N most similar movies
    top_indices = np.argsort(similarities[0])[-top_n:][::-1]
    
    # 4. Return the top N most similar movies
    results = df.iloc[top_indices].copy()
    results['similarity_score'] = similarities[0][top_indices]  # Add similarity score
    
    return results

# ===============================


def get_user_info(customer_id):
    """Get customer name and basic info by ID"""
    query = f"""
    SELECT 
        customer_id,
        first_name || ' ' || last_name AS customer_name,
        address,
        city,
        country
    FROM customer
    JOIN address USING (address_id)
    JOIN city USING (city_id) 
    JOIN country USING (country_id)
    WHERE customer_id = {customer_id};
    """
    return get_data(query)


def get_rental_history(customer_id):
    """Get complete rental history for a customer"""
    query = f"""
    SELECT 
        r.rental_id,
        f.film_id,
        f.title,
        f.description,
        c.name AS category,
        f.rating,
        r.rental_date,
        r.return_date
    FROM rental r
    JOIN inventory i ON r.inventory_id = i.inventory_id
    JOIN film f ON i.film_id = f.film_id
    JOIN film_category fc ON f.film_id = fc.film_id
    JOIN category c ON fc.category_id = c.category_id
    WHERE r.customer_id = {customer_id}
    ORDER BY r.rental_date DESC;
    """
    return get_data(query)

def get_user_top_movies(customer_id, limit=10):
    """Get top most rented movies by a customer"""
    query = f"""
    SELECT 
        f.title,
        c.name AS category,
        f.rating,
        COUNT(r.rental_id) AS rental_count,
        MAX(r.rental_date) AS last_rented
    FROM rental r
    JOIN inventory i ON r.inventory_id = i.inventory_id
    JOIN film f ON i.film_id = f.film_id
    JOIN film_category fc ON f.film_id = fc.film_id
    JOIN category c ON fc.category_id = c.category_id
    WHERE r.customer_id = {customer_id}
    GROUP BY f.film_id, c.name
    ORDER BY rental_count DESC, last_rented DESC
    LIMIT {limit};
    """
    return get_data(query)