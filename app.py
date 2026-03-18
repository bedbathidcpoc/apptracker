import streamlit as st
import requests

st.set_page_config(page_title="eSewa Tracker", layout="wide")

# Styling for the Visual Timeline
st.markdown("""
    <style>
    .timeline-wrapper { display: flex; align-items: center; justify-content: center; padding: 40px 0; }
    .step { display: flex; flex-direction: column; align-items: center; position: relative; width: 250px; }
    .dot { height: 40px; width: 40px; background-color: #ddd; border-radius: 50%; display: flex; 
           align-items: center; justify-content: center; color: white; font-weight: bold; z-index: 2; border: 2px solid #fff; }
    .dot-active { background-color: #4CAF50; box-shadow: 0 0 10px rgba(76, 175, 80, 0.5); }
    .line { position: absolute; height: 4px; background-color: #ddd; width: 100%; top: 18px; left: 50%; z-index: 1; }
    .line-active { background-color: #4CAF50; }
    .label { margin-top: 15px; font-weight: bold; color: #333; text-align: center; }
    .date { font-size: 0.8em; color: #777; }
    </style>
    """, unsafe_allow_html=True)

st.title("🚜 Punjab eSewa Quick Tracker")
app_id = st.text_input("Enter Application ID", value="89080987")

if st.button("Track Status"):
    with st.spinner("Fetching status..."):
        url = "https://esewa.punjab.gov.in/common/api/Common/TrackApplicationProcess"
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "User-Agent": "Mozilla/5.0",
            "Origin": "https://esewa.punjab.gov.in",
            "Referer": "https://esewa.punjab.gov.in/trackStatus_DetailedApllication"
        }
        
        try:
            response = requests.post(url, json={"ApplicationId": str(app_id)}, headers=headers, timeout=10)
            res_json = response.json()
            
            if res_json.get("data") and len(res_json["data"][0]) > 0:
                item = res_json["data"][0][0]
                
                # Logic based on your actual data
                # --- REFINED LOGIC ---
                # Step 1: Always active if record exists
                sub_date = item.get("Application_Submitted")
                
                # Step 2: Under Processing - Only green if the portal says "Yes"
                # This fixes the error where 'P' was triggering it too early
                is_processing = item.get("Under_Processing") == "Yes"
                
                # Step 3: Approved or Rejected - Only green if there is a date provided
                final_date = item.get("Approved_or_Rejected_Date")
                is_final = final_date != "No"

                st.subheader(f"Application Id : {app_id}")

                # Display Visuals
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
                st.markdown(html_code, unsafe_allow_html=True)
                
                # Optional: Show details in a clean table below
                with st.expander("View Raw Details"):
                    st.write(item)
            else:
                st.warning("No data found for this ID.")
        except Exception as e:
            st.error(f"Error: {e}")
