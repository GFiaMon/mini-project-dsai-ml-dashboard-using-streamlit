# 🔮_Prediction.py
import streamlit as st

from backend import get_movie_descriptions, setup_recommendation_engine, find_similar_movies
import time

# Set up the page
st.set_page_config(page_title="Prediction - Sakila Dashboard")
st.title("🔮 Movie Recommendation Engine")
st.write("Describe a movie you like and get similar recommendations!")

# 1. Set up the recommendation engine (only once when app loads)
# We use st.cache_resource to avoid reloading the model on every interaction
@st.cache_resource
def load_engine():
    with st.spinner('Loading recommendation engine... This may take a moment.'):
        model, df, embeddings = setup_recommendation_engine()
        st.success("✅ Recommendation engine loaded!")
        return model, df, embeddings
    
# Load the engine
model, movies_df, embeddings = load_engine()

# ======== Test the connection:

# Create an expander to keep the test neat
with st.expander("🎬 Test: Load Movie Data with Descriptions & Categories"):
    st.write("""
    **Test Description:** 
    This test runs the query to get all movies with their descriptions, ratings, and categories.
    """)
    
    # Button to run the test
    if st.button("Load Movie Data", key="load_movies_button"):
        
        # Show a spinner while the data loads
        with st.spinner('Loading movie data... This might take a moment.'):
            try:
                # Use our function from backend.py to get the data
                movies_df = get_movie_descriptions()
                
                # If successful, display success message and data summary
                st.success("✅ Movie data loaded successfully!")
                
                # Show basic info about the data
                st.write(f"**Number of movies loaded:** {len(movies_df)}")
                st.write(f"**Columns available:** {list(movies_df.columns)}")
                st.write(f"**Unique categories:** {movies_df['category'].unique()}")
                
                # Display the first 10 rows as a preview
                st.write("**Preview of the data (first 10 rows):**")
                st.dataframe(movies_df.head(10))
                
            except Exception as e:
                # If there's an error, display it
                st.error(f"❌ Failed to load movie data. Error: {e}")


# ===============================

st.divider()

# title = st.text_input("Describe the movie", "Life of Brian with a dog that talks")
# st.write("The current movie title is", title)

# 2. Create the user input interface
st.subheader("Find Similar Movies")
user_input = st.text_area(
    "Describe a movie you like:",
    placeholder="E.g., 'A thrilling action movie with car chases and heroes saving the world...'",
    height=100
)

# 3. Create the button and handle the recommendation
if st.button("🎯 Get Recommendations", type="primary"):
    if user_input.strip():  # Check if input is not empty
        with st.spinner('Finding similar movies...'):
            # Add a small delay so the spinner is visible
            time.sleep(0.5)
            
            # Get recommendations from backend
            results = find_similar_movies(user_input, model, movies_df, embeddings)
            
            # Display results
            st.success("Found similar movies!")
            st.subheader("Top Recommendations:")
            
            # Display each recommendation in a nice card-like format
            for i, (index, row) in enumerate(results.iterrows(), 1):
                with st.container():
                    st.markdown(f"### {i}. {row['title']}")
                    st.markdown(f"**Genre:** {row['category']} | **Rating:** {row['rating']}")
                    st.markdown(f"**Description:** {row['description']}")
                    st.markdown(f"**Similarity Score:** {row['similarity_score']:.3f}")
                    st.progress(round(row['similarity_score'] * 100)) # to show a progress bar.
                    st.divider()
                    
    else:
        st.warning("⚠️ Please enter a movie description first!")