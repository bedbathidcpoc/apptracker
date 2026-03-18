import streamlit as st
import requests

st.set_page_config(page_title="eSewa Tracker", layout="wide")

# (Keep your CSS block here from the previous message, 
# Custom CSS for the "Timeline" look
st.markdown("""
    <style>
    .timeline-wrapper {
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 40px 0;
        font-family: sans-serif;
    }
    .step {
        display: flex;
        flex-direction: column;
        align-items: center;
        position: relative;
        width: 200px;
    }
    .dot {
        height: 40px;
        width: 40px;
        background-color: #bbb;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-weight: bold;
        z-index: 2;
    }
    .dot-active { background-color: #76b852; } /* Green color from your image */
    .line {
        position: absolute;
        height: 4px;
        background-color: #bbb;
        width: 100%;
        top: 18px;
        left: 50%;
        z-index: 1;
    }
    .line-active { background-color: #76b852; }
    .label { margin-top: 15px; font-weight: bold; text-align: center; color: #333; }
    .date { font-size: 0.85em; color: #666; }
    </style>
    """, unsafe_allow_html=True)

st.title("🚜 Punjab eSewa Quick Tracker")

app_id = st.text_input("Enter Application ID", value="89080987")

if st.button("Track Status"):
    # Add a visual loader so you know it's working
    with st.spinner("Connecting to Punjab Govt Servers..."):
        url = "https://esewa.punjab.gov.in/common/api/Common/TrackApplicationProcess"
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
            "Origin": "https://esewa.punjab.gov.in",
            "Referer": "https://esewa.punjab.gov.in/trackStatus_DetailedApllication"
        }
        
        try:
            # Set a 10-second timeout so it doesn't hang forever
            response = requests.post(url, json={"ApplicationId": str(app_id)}, headers=headers, timeout=10)
            
            if response.status_code == 200:
                res_json = response.json()
                # ... (rest of your logic to display the dots)
                st.success("Data Fetched!")
                st.json(res_json) # Temporary: See the data to confirm it's working
            else:
                st.error(f"Government server rejected the request (Status: {response.status_code}). This usually happens if you are using a VPN or non-Indian IP.")
                
        except requests.exceptions.Timeout:
            st.error("Request Timed Out. The eSewa portal is taking too long to respond.")
        except Exception as e:
            st.error(f"An error occurred: {e}")
