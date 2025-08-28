# import streamlit as st

# st.title('Home')

# st.divider()

# # 2. Write some text
# st.write("Hello! This is a Streamlit app.")

# # 3. Add a subheader
# st.subheader("This is a smaller header")

# 🏡_Home.py
import streamlit as st

# 1. Define a function for the main content of the home page
def show_home_page():
    """
    This function contains all the code for the Home page.
    """
    st.title('Sakila Dashboard Home')
    st.write("Hello! This is my first Streamlit app.")
    st.subheader("This is a smaller header")

    # Create an expander for the project description
    with st.expander("📋 See Project Description"):
        st.write("""
        **Project Overview:**
        This is a dashboard for the Sakila movie rental database.
        - **EDA Page:** Explore charts and data.
        - **Prediction Page:** Get movie recommendations.
        """)

    st.write("Here is a simple data table:")
    data = {"Movie": ["The Lord of the Rings", "Inception", "Toy Story"], "Rating": ["PG-13", "PG-13", "G"]}
    st.dataframe(data)

# 2. This is the main part of the script that runs the function
if __name__ == "__main__":
    show_home_page()