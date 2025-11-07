import streamlit as st
import pandas as pd
import time
import threading

# Auto-refresh function to keep the app active (runs in background)
def keep_alive():
    """
    Function to ping the app every 5 minutes to keep it active
    """
    while True:
        try:
            # Wait for 5 minutes (300 seconds)
            time.sleep(300)
            
            # Refresh the app by triggering a rerun
            st.rerun()
            
        except Exception as e:
            # If there's an error, continue anyway
            continue

# Start the keep-alive thread only once
if 'keep_alive_started' not in st.session_state:
    st.session_state.keep_alive_started = True
    keep_alive_thread = threading.Thread(target=keep_alive, daemon=True)
    keep_alive_thread.start()

# title with clickable link
st.markdown(
    "<h1 style='text-align: center;'><a href='#' target='_blank' style='text-decoration: none; color: inherit;'>Bayes' Theorem: Student Performance Analysis</a></h1>",
    unsafe_allow_html=True
)

st.subheader("Case Study: ABES Institute of Technology")

# default dataset
st.write("Example Dataset")
st.text("1: Late Students, 0: On Time Students")

sample_data = {
    'Student': ['Arpit', 'Bablu', 'Anuj', 'Ansh', 'Shalini', 'Ravi', 'Rishabh', 'Nikita'],
    'Late':     [1, 0, 1, 1, 0, 0, 1, 0],
    'Attendance': ['Low', 'High', 'Low', 'Low', 'High', 'High', 'Low', 'High'],
    'Result':   ['Fail', 'Pass', 'Fail', 'Fail', 'Pass', 'Pass', 'Fail', 'Pass']
}
df_default = pd.DataFrame(sample_data)
st.dataframe(df_default)

# bayes theorem
def compute_bayes(df):
    total = len(df)
    late = df[df['Late'] == 1]
    passed = df[df['Result'].str.lower() == 'pass']
    P_Late = len(late) / total
    P_Pass = len(passed) / total
    P_Late_Pass = len(passed[passed['Late'] == 1]) / len(passed) if len(passed) > 0 else 0

    st.write("Bayes' Theorem Calculation")
    st.latex(r"P(Pass \mid Late) = \frac{P(Late \mid Pass) \cdot P(Pass)}{P(Late)}")
    st.write(f"P(Late): {P_Late:.2f}")
    st.write(f"P(Pass): {P_Pass:.2f}")
    st.write(f"P(Late | Pass): {P_Late_Pass:.2f}")

    if P_Late > 0:
        result = (P_Late_Pass * P_Pass) / P_Late
        st.write(f"P(Pass | Late): {result:.2f}")
    else:
        st.warning("Cannot compute because P(Late) = 0.")

# run on default data
compute_bayes(df_default)

# upload csv
st.write("---")
st.subheader("Upload Your Own Dataset")
uploaded_file = st.file_uploader("CSV must include: Late, Attendance, Result", type=["csv"])

if uploaded_file:
    df_uploaded = pd.read_csv(uploaded_file)
    cols = {'Late', 'Attendance', 'Result'}
    if not cols.issubset(df_uploaded.columns):
        st.error("Missing required columns")
    else:
        st.write("Uploaded Dataset")
        st.dataframe(df_uploaded)
        compute_bayes(df_uploaded)
else:
    st.info("Upload a CSV file to replace the default dataset")