### **Project Plan: Basic Structure**

**1. Frontend (What the user sees in the browser)**
*   **Three Pages:** A navigation menu to switch between them.
    *   **Home:** A title and an image.
    *   **EDA:** Three sections:
        1.  A line chart.
        2.  A bar chart.
        3.  A small data table.
    *   **Prediction:** A text box and a "Get Your Prediction" button. When clicked, it shows a list of 3 movie titles.

**2. Backend (The code that makes it work)**
*   **Data:** One MySQL database file (`sakila.db`).
*   **For the EDA Page:**
    *   Code to connect to the database.
    *   3 SQL queries to get the data for the charts and table.
    *   Code to draw the charts.
*   **For the Prediction Page:**
    *   Code to load all movie descriptions from the database.
    *   A function that takes the user's text and finds the 3 most similar movies.
    *   Code to display the results.

The **Frontend** is built with Streamlit commands (`st.title`, `st.button`, `st.pyplot`). 

The **Backend** with Python, SQL, and data science libraries (Pandas, Scikit-Learn, Sentence Transformers).


Perfect. This is an excellent way to structure your thinking. Here is the plan broken down by components.

-----

### **Project Plan: Component Structure**

#### **1. EDA Page Components**

**Component 1: Daily Rentals Line Plot**
*   **Purpose:** Show rental trends over time for each store.
*   **Backend (SQL Query):**
    *   Join `rental`, `inventory`, and `store` tables.
    *   Filter for year = 2005.
    *   Count rentals grouped by day and store.
*   **Frontend (Streamlit):**
    *   `st.subheader("Daily Rentals (2005)")`
    *   `st.line_chart(data)` or `st.pyplot(fig)`

**Component 2: Total Benefit Bar Plot**
*   **Purpose:** Compare total profit between stores.
*   **Backend (SQL Query):**
    *   Join `payment`, `rental`, `inventory`, and `store` tables.
    *   Sum the `amount` grouped by store.
*   **Frontend (Streamlit):**
    *   `st.subheader("Total Profit by Store")`
    *   `st.bar_chart(data)` or `st.pyplot(fig)`

**Component 3: Top 5 Movies Dataframe**
*   **Purpose:** Display the most popular movies for each store.
*   **Backend (SQL Query):**
    *   Join `rental`, `inventory`, `film`, and `store` tables.
    *   Count rentals grouped by store and film title.
    *   Get the top 5 for each store.
*   **Frontend (Streamlit):**
    *   `st.subheader("Top 5 Movies per Store")`
    *   `st.dataframe(df)` 

---

#### **2. Prediction Page Component**

**Component: Movie Recommendation Engine**
*   **Purpose:** User inputs a description, gets 3 similar movies.
*   **Backend (The Logic):**
    1.  **SQL Query:** Get all movie titles, descriptions, and ratings from the `film` table.
    2.  **Model:** Use `SentenceTransformer` to turn all descriptions into numerical vectors.
    3.  **Function:** When user clicks the button:
        *   Turn the user's input text into a vector.
        *   Use `cosine_similarity` to compare it to all movie vectors.
        *   Find the 3 most similar movies.
*   **Frontend (Streamlit UI):**
    *   `st.subheader("Find Similar Movies")`
    *   `user_input = st.text_area("Describe a movie you like...")`
    *   `if st.button("Get Recommendations"):`
    *   `st.write("Top 3 Recommendations:")`
    *   `st.write(result_df)`