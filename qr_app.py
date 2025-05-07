import streamlit as st
import pandas as pd
import qrcode
from PIL import Image
import io
import uuid
import os
from datetime import datetime

# ---------- CONFIGURATION ----------
DATA_FILE = "data.csv"
BASE_URL = "https://child-health-qr-app.streamlit.app"  # Update this after deployment


# ---------- INITIAL SETUP ----------
# If data file does not exist, create it with headers
if not os.path.exists(DATA_FILE):
    df_init = pd.DataFrame(columns=["id", "name", "allergies", "timestamp"])
    df_init.to_csv(DATA_FILE, index=False)


# ---------- APP LOGIC ----------
st.set_page_config(page_title="Child Info QR Generator", layout="centered")

query_params = st.query_params

if "id" in query_params:
    # ---------- QR VIEW MODE ----------
    child_id = query_params["id"]
    df = pd.read_csv(DATA_FILE)
    row = df[df["id"] == child_id]

    st.title("Child Info Viewer")
    if not row.empty:
        child_info = row.iloc[0]
        st.markdown(f"**Name:** {child_info['name']}")
        st.markdown(f"**Allergies / Health Info:** {child_info['allergies']}")
        st.markdown(f"**Submitted At:** {child_info['timestamp']}")
    else:
        st.error("No information found for this ID.")
else:
    # ---------- FORM MODE ----------
    st.title("Generate QR for Child Health Info")

    name = st.text_input("Child's Full Name")
    allergies = st.text_area("Enter allergies / health-related information")

    if st.button("Generate QR Code"):
        if not name.strip() or not allergies.strip():
            st.warning("Please fill in both name and health info.")
        else:
            # Generate unique ID for this entry
            child_id = str(uuid.uuid4())

            # Save info to CSV
            new_data = pd.DataFrame([{
                "id": child_id,
                "name": name,
                "allergies": allergies,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }])
            new_data.to_csv(DATA_FILE, mode='a', header=False, index=False)

            # Generate the QR Code linking to the child's info page
            qr_url = f"{BASE_URL}/?id={child_id}"
            qr = qrcode.make(qr_url)

            # Convert to in-memory image
            img_buffer = io.BytesIO()
            qr.save(img_buffer, format="PNG")
            img_buffer.seek(0)

            st.success("QR Code generated! Scan it to view child info.")
            st.image(qr, caption="Scan this QR code", width=250)

            st.markdown(f"**Or open directly:** [View Info]({qr_url})")

            # Download QR code
            st.download_button(
                label="Download QR Code",
                data=img_buffer,
                file_name=f"{name.replace(' ', '_')}_qr.png",
                mime="image/png"
            )
