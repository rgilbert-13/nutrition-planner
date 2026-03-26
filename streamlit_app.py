# streamlit_app.py (with auth)
import streamlit as st
from streamlit import runtime
from streamlit.web.server.websocket_headers import _get_websocket_headers
import sqlite3
from datetime import date

# Check authentication
def get_user():
    """Get authenticated user from Streamlit Cloud"""
    try:
        # This works only on Streamlit Cloud
        headers = _get_websocket_headers()
        if headers and "x-streamlit-user" in headers:
            return {
                "email": headers.get("x-streamlit-user"),
                "is_authenticated": True
            }
    except:
        pass
    return {"email": None, "is_authenticated": False}

# Check if user is logged in
user = get_user()

if not user["is_authenticated"]:
    st.title("🍽️ PlateMate")
    st.caption("Please sign in to continue")
    st.markdown("""
    ### 🔐 Authentication Required
    
    This app requires authentication.
    
    **To enable authentication:**
    1. Go to your app settings on share.streamlit.io
    2. Click "Settings" → "Authentication"
    3. Enable Google or GitHub authentication
    """)
    st.stop()

# Display user info
st.sidebar.write(f"👤 Logged in as: {user['email']}")

# Now use user email to filter database
def get_user_db(email):
    """Get user-specific database connection"""
    # Replace . with _ for filename
    safe_email = email.replace(".", "_").replace("@", "_")
    return f"platemate_{safe_email}.db"

# Your existing code, but use user-specific database