import streamlit as st

pages = [
    st.Page("pages/overview.py", title="Overview", icon="📊"),
    st.Page("pages/trends_over_time.py", title="Trends over Time", icon="⏳"),
    st.Page("pages/key_concepts_functions.py", title="Key Concepts and Functions", icon="🔑"),
    st.Page("pages/learning_path.py", title="Learning Path", icon="🛤️"),
]

current_page = st.navigation(pages)

st.set_page_config(
    layout="wide",
    page_title=f"{current_page.title} | DAX Analytics Dashboard",
    page_icon=current_page.icon,
    initial_sidebar_state="expanded"
)

current_page.run()
