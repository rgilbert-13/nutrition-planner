import streamlit as st

# Page configuration
st.set_page_config(
    page_title="PlateMate",
    page_icon="🍽️",
    layout="wide"
)

# Title
st.title("🍽️ PlateMate")
st.caption("Your AI nutrition assistant — Coming Soon")

# Simple test content
st.markdown("---")

# Test columns to show layout works
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("📝 Log Meals")
    st.write("Coming soon: text and photo logging")

with col2:
    st.subheader("📊 Track Nutrition")
    st.write("Coming soon: calories, protein, macros")

with col3:
    st.subheader("🛒 Grocery Lists")
    st.write("Coming soon: smart shopping lists with pricing")

st.markdown("---")

# Simple interactive test
st.subheader("Test Connection")
user_input = st.text_input("Type something to test:", placeholder="Hello!")
if user_input:
    st.success(f"You typed: {user_input}")

# Display environment info (for testing)
st.markdown("---")
st.caption(f"✅ Streamlit version: {st.__version__}")
st.caption("🚀 Ready for deployment")