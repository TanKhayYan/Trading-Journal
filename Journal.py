import streamlit as st
import pandas as pd
import numpy as np

#streamlit run "C:\Users\tankh\OneDrive\Desktop\visual studio code\Trading database\Journal.py"
st.set_page_config(page_title="Trading Journal", layout="wide")
st.title("Trading Data")

CSV_FILE = "not1.csv"

# Step 1: Load data into session state once
if "df" not in st.session_state:
    st.session_state.df = pd.read_csv(CSV_FILE)
    st.session_state.df.columns = st.session_state.df.columns.str.strip()

# Step 2: Track save status
if "just_saved" not in st.session_state:
    st.session_state.just_saved = False

# Step 3: Show editable table
edited_df = st.data_editor(st.session_state.df, key="editable_df", use_container_width=True, num_rows="dynamic")

# Step 4: Save button to commit changes
if st.button("💾 Save changes"):
    st.session_state.df = edited_df.copy()
    st.session_state.df.to_csv(CSV_FILE, index=False)
    st.session_state.just_saved = True
    st.rerun()  # Refresh to reflect updates immediately

# Step 5: Show success message once after saving
if st.session_state.just_saved:
    st.success("Changes saved!")
    st.session_state.just_saved = False

# Step 6: Process and plot data
try:
    df = st.session_state.df.copy()
    df["Time"] = pd.to_datetime(df["Time"])
    df = df.sort_values("Time")
    df["Cumulative PnL"] = df["PnL"].cumsum()

    st.write("### PnL Table")
    st.dataframe(df.set_index("Time")[["PnL"]], use_container_width=True)

    st.write("### Cumulative PnL Over Time")
    st.line_chart(df, x="Time", y="Cumulative PnL")

except Exception as e:
    st.error(f"Error while processing data: {e}")