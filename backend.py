# backend.py

import streamlit as st

# 1. Import necessary libraries
from sqlalchemy.exc import SQLAlchemyError  # <-- ADD THIS LINE
import pandas as pd
from sqlalchemy import create_engine
# Import the library to read the .env file
from dotenv import load_dotenv
# Import os to access environment variables
import os

# Libraries for the ML model
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# 1. Load the environment variables from the .env file
load_dotenv()

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




# # 2. Function to create the database engine
# def get_engine():
#     """
#     Creates a SQLAlchemy engine for MySQL using credentials from the .env file.
#     Returns: A SQLAlchemy engine object.
#     """
#     # Get database credentials from environment variables
#     db_host = os.getenv('DB_HOST')
#     db_name = os.getenv('DB_NAME')
#     db_user = os.getenv('DB_USER')
#     db_password = os.getenv('DB_PASSWORD')
    
#     # Create the connection string for MySQL
#     connection_string = f'mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}'
    
#     # Create and return the engine
#     engine = create_engine(connection_string)
#     return engine

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


# Add to backend.py
def get_movie_descriptions():
    """
    Fetches all movies with their title, description, and rating from the film table.
    Returns: A pandas DataFrame.
    """
    query = """
    SELECT 
        film_id, 
        title, 
        description, 
        rating
    FROM 
        film
    WHERE 
        description IS NOT NULL;
    """
    
    df = get_data(query)
    return df

# getting movie descriptions:

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


# Loads the movie data and prepares the model.
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