# 🏠_Home.py
import streamlit as st

def show_home_page():
    """
    This function contains all the code for the Home page.
    """
    # Set page config
    st.set_page_config(
        page_title="Sakila Dashboard",
        page_icon="🎬",
        layout="wide"
    )
    
    # Header section - Title first, then big banner
    def _show_header():
        st.title("Sakila Movie Analytics Dashboard")
        st.subheader("Step Back into the Video Rental Era")
        # st.image("images/sakila_dashboard_banner_smll.png",width=100, use_container_width=True)
    
        # Wide banner image - using container width but controlling height
        st.image("images/retro_video_store_wide3.png", 
                use_container_width=True,  # Fills the width
                output_format="auto")      # Keeps it sharp    


    # Main content section
    def _show_main_content():
        st.markdown("""
        ### 📊 About This Project

        This interactive dashboard analyzes the **Sakila Movie Rental Database**, providing insights into:
        - **Rental trends** and store performance throughout 2005
        - **Revenue analysis** by store and category  
        - **Movie recommendations** based on AI-powered content analysis
        """)
        
        # Navigation guide
        with st.expander("🚀 How to Use This Dashboard"):
            st.markdown("""
            1.  **📈 EDA Page**: Explore interactive charts and business metrics
            2.  **🔮 Prediction Page**: Get personalized movie recommendations
            """)
        
        # Tech stack
        with st.expander("💡 Technology Stack"):
            st.markdown("""
            - **Backend**: Python, PostgreSQL, Scikit-Learn
            - **Frontend**: Streamlit, Plotly, Pandas  
            - **AI**: Sentence Transformers for semantic search
            """)
        
        st.write("")
        st.caption("Explore the data that powered video rental stores in the pre-streaming era!")
    
    # Footer section
    def _show_footer():
        st.divider()
        st.caption("Built with Streamlit • Sakila Database • Guillermo Fiallo-Montero • 2025")
    
    # Execute all sections
    _show_header()
    _show_main_content()
    _show_footer()

# Main execution
if __name__ == "__main__":
    show_home_page()



















# # 🏡_Home.py
# import streamlit as st

# # 1. Define a function for the main content of the home page
# def show_home_page():
#     """
#     This function contains all the code for the Home page.
#     """
#     st.title('Sakila Dashboard Home')
#     st.write("Hello! This is my first Streamlit app.")
#     st.subheader("This is a smaller header")

#     # Create an expander for the project description
#     with st.expander("📋 See Project Description"):
#         st.write("""
#         **Project Overview:**
#         This is a dashboard for the Sakila movie rental database.
#         - **EDA Page:** Explore charts and data.
#         - **Prediction Page:** Get movie recommendations.
#         """)

#     st.write("Here is a simple data table:")
#     data = {"Movie": ["The Lord of the Rings", "Inception", "Toy Story"], "Rating": ["PG-13", "PG-13", "G"]}
#     st.dataframe(data)

# # 2. This is the main part of the script that runs the function
# if __name__ == "__main__":
#     show_home_page()


