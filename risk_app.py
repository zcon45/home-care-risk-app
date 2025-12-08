import streamlit as st

# ===============================
# PROFESSIONAL PAGE CONFIG
# ===============================
st.set_page_config(
    page_title="Home Care Comfort Portal",
    page_icon="house",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ===============================
# GORGEOUS STYLING
# ===============================
st.markdown("""
<style>
    .main {background: linear-gradient(135deg, #f5f7fa 0%, #e4edf5 100%);}
    .header-card {
        background: white;
        padding: 3rem 2rem;
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        text-align: center;
        margin: 2rem 0;
    }
    .big-title {
        font-size: 3rem;
        font-weight: 700;
        background: linear-gradient(90deg, #1e40af, #3b82f6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    .subtitle {
        font-size: 1.3rem;
        color: #64748b;
        margin-bottom: 3rem;
    }
    .btn-client, .btn-admin {
        height: 130px;
        width: 300px;
        font-size: 1.4rem;
        font-weight: 600;
        border-radius: 16px;
        margin: 1rem;
        box-shadow: 0 8px 20px rgba(0,0,0,0.15);
        transition: all 0.3s;
    }
    .btn-client {
        background: linear-gradient(135deg, #10b981, #34d399);
        color: white;
    }
    .btn-admin {
        background: linear-gradient(135deg, #6366f1, #8b5cf6);
        color: white;
    }
    .btn-client:hover, .btn-admin:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 30px rgba(0,0,0,0.2);
    }
</style>
""", unsafe_allow_html=True)

# ===============================
# PAGE 1 – HOME / LANDING
# ===============================
def home_page():
    st.markdown("<div class='header-card'>", unsafe_allow_html=True)
    
    st.markdown("<h1 class='big-title'>Home Care Comfort Portal</h1>", unsafe_allow_html=True)
    st.markdown("<p class='subtitle'>Professional Risk Assessment & Care Coordination Platform</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1,1,1])
    
    with col2:
        if st.button("Client Access", key="client", use_container_width=True):
            st.session_state.page = "client"
            st.rerun()
            
        if st.button("Admin Access", key="admin", use_container_width=True):
            st.session_state.page = "admin"
            st.rerun()
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Footer
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#94a3b8; font-size:0.9rem;'>© 2025 Home Care Comfort Portal • Secure & Confidential</p>", unsafe_allow_html=True)

# ===============================
# SESSION STATE & ROUTER
# ===============================
if "page" not in st.session_state:
    st.session_state.page = "home"

if st.session_state.page == "home":
    home_page()
