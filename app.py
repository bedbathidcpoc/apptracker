import streamlit as st
import requests

st.set_page_config(page_title="eSewa Status Tracker", layout="wide")

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
    """, unsafe_allow_index=True)

st.title("🚜 Punjab eSewa Quick Tracker")

app_id = st.text_input("Enter Application ID", value="89080987")

if st.button("Track Status"):
    url = "https://esewa.punjab.gov.in/common/api/Common/TrackApplicationProcess"
    headers = {
        "Content-Type": "application/json;charset=UTF-8",
        "User-Agent": "Mozilla/5.0",
        "Origin": "https://esewa.punjab.gov.in",
        "Referer": "https://esewa.punjab.gov.in/trackStatus_DetailedApllication"
    }
    
    try:
        response = requests.post(url, json={"ApplicationId": str(app_id)}, headers=headers)
        res_json = response.json()
        
        # Digging into the nested data structure you provided
        if res_json.get("data") and len(res_json["data"][0]) > 0:
            item = res_json["data"][0][0]
            
            # Extracting values from your JSON
            sub_date = item.get("Application_Submitted")
            is_processing = item.get("Under_Processing") != "No"
            final_date = item.get("Approved_or_Rejected_Date")
            is_final = final_date != "No"

            st.write(f"### Application Id : {app_id}")

            # HTML for the Progress Bar
            html_code = f"""
            <div class="timeline-wrapper">
                <div class="step">
                    <div class="dot dot-active">✔</div>
                    <div class="line {'line-active' if is_processing or is_final else ''}"></div>
                    <div class="label">Application Submitted</div>
                    <div class="date">{sub_date}</div>
                </div>
                <div class="step">
                    <div class="dot {'dot-active' if is_processing or is_final else ''}">{'✔' if is_processing or is_final else ''}</div>
                    <div class="line {'line-active' if is_final else ''}"></div>
                    <div class="label">Under Processing</div>
                </div>
                <div class="step">
                    <div class="dot {'dot-active' if is_final else ''}">{'✔' if is_final else ''}</div>
                    <div class="label">Accept/Reject</div>
                    <div class="date">{final_date if is_final else ''}</div>
                </div>
            </div>
            """
            st.markdown(html_code, unsafe_allow_index=True)
        else:
            st.warning("No application found with this ID.")
            
    except Exception as e:
        st.error(f"Error fetching data: {e}")
