import streamlit as st

# Page Config
st.set_page_config(
    page_title="Home Care Comfort Portal",
    page_icon="🏠",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Professional CSS
st.markdown("""
<style>
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    .portal-card {
        background: white;
        padding: 3rem;
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
        text-align: center;
        max-width: 800px;
        margin: 2rem auto;
    }
    .portal-title {
        font-size: 3rem;
        color: #2c3e50;
        margin-bottom: 1rem;
        font-weight: 700;
    }
    .portal-subtitle {
        font-size: 1.2rem;
        color: #7f8c8d;
        margin-bottom: 3rem;
    }
    .client-btn {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
    }
    .admin-btn {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    }
    .access-btn {
        color: white !important;
        border: none;
        padding: 1.2rem 2rem;
        border-radius: 50px;
        font-size: 1.2rem;
        font-weight: 600;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        transition: all 0.3s;
    }
    .access-btn:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.3);
    }
    .footer-text {
        margin-top: 3rem;
        color: #bdc3c7;
        font-size: 0.9rem;
    }
</style>
""", unsafe_allow_html=True)

# Session State
if "page" not in st.session_state:
    st.session_state.page = "home"
if "assessment_step" not in st.session_state:
    st.session_state.assessment_step = 1

# Home Page
def home_page():
    st.markdown('<div class="portal-card">', unsafe_allow_html=True)
    st.markdown('<h1 class="portal-title">🏠 Home Care Comfort Portal</h1>', unsafe_allow_html=True)
    st.markdown('<p class="portal-subtitle">Secure, professional assessment and coordination for home care services.</p>', unsafe_allow_html=True)

    # Real Streamlit buttons with custom styling
    col1, col2 = st.columns(2, gap="large")
    
    with col1:
        if st.button("👤 Client Assessment", key="client", use_container_width=True):
            st.session_state.page = "assessment"
            st.session_state.assessment_step = 1
            st.rerun()
    
    with col2:
        if st.button("🛡️ Admin Dashboard", key="admin", use_container_width=True):
            st.session_state.page = "admin"
            st.rerun()

    # Apply custom classes to the buttons (Streamlit allows this via markdown trick)
    st.markdown("""
    <script>
        document.querySelectorAll('[data-testid="stButton"] button')[0].classList.add('access-btn', 'client-btn');
        document.querySelectorAll('[data-testid="stButton"] button')[1].classList.add('access-btn', 'admin-btn');
    </script>
    """, unsafe_allow_html=True)

    st.markdown('<p class="footer-text">Powered by Streamlit • Confidential & Secure</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Placeholder pages (we'll fill these next)
def assessment_page():
    st.title("Client Assessment")
    st.write("Step 1: Basic Information – coming in the next update!")
    if st.button("← Back to Home"):
        st.session_state.page = "home"
        st.rerun()

def admin_page():
    st.title("Admin Dashboard")
    st.info("Admin features will appear here once assessments are submitted.")
    if st.button("← Back to Home"):
        st.session_state.page = "home"
        st.rerun()

# Router
if st.session_state.page == "home":
    home_page()
elif st.session_state.page == "assessment":
    assessment_page()
elif st.session_state.page == "admin":
    admin_page()
