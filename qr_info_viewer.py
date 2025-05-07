import streamlit as st
import pandas as pd

st.set_page_config(page_title="View Child Info", layout="centered")
st.title("Child Info Viewer")

# Retrieve data from query params
query_params = st.query_params
child_id = query_params.get("id", None)

if child_id:
    # Convert single value to string if list
    if isinstance(child_id, list):
        child_id = child_id[0]

    # Search in stored session data
    if "child_data" in st.session_state:
        match = next((entry for entry in st.session_state["child_data"] if entry["id"] == child_id), None)
        if match:
            st.subheader(f"Details for {match['name']}")
            st.markdown(f"**Allergies/Conditions:** {match['info']}")
        else:
            st.error("No matching record found.")
    else:
        st.warning("No session data found. This may happen if accessed in a new session.")
else:
    st.info("No child ID provided. Please scan a valid QR code link.")
