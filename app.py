import streamlit as st
from src.wifi_assessment import WiFiSecurityAssessment
from src.dashboard import create_main_dashboard

# Page configuration
st.set_page_config(
    page_title="WiFi Security Assessment Tool",
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    """Main application routing"""

    # Initialize session state
    if 'wifi_tool' not in st.session_state:
        st.session_state.wifi_tool = WiFiSecurityAssessment()
        st.session_state.scan_completed = False

    # Sidebar navigation
    st.sidebar.title("🧭 Navigation")

    page = st.sidebar.radio(
        "Choose a page:",
        ["🏠 Main Dashboard"]
    )

    # Route to main dashboard
    if page == "🏠 Main Dashboard":
        create_main_dashboard()


if __name__ == "__main__":
    main()