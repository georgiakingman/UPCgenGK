import streamlit as st
import pandas as pd
from rapidfuzz import process, fuzz

st.title("🧠 Fuzzy Product Code Matcher")

st.write("""
Upload two CSV files:

- A **reference** CSV that contains the correct `ITEM_NAME` and `UPC`
- An **input** CSV with messy `Description`s to match

This app will fuzzy match each input item to the best reference name and return the matched UPC.
""")
reference_file = st.file_uploader("📘 Upload reference CSV (with ITEM_NAME and UPC)", type="csv")
input_file = st.file_uploader("📗 Upload input CSV (with Description)", type="csv")
score_threshold = st.slider("🔍 Match Score Threshold", min_value=0, max_value=100, value=85, step=1)
if reference_file and input_file:
    reference_df = pd.read_csv(reference_file)
    input_df = pd.read_csv(input_file)
    reference_name_col = 'ITEM_NAME'
    reference_code_col = 'UPC'
    input_name_col = 'Description'
  reference_df[reference_name_col] = reference_df[reference_name_col].astype(str).str.lower().str.strip()
    reference_names = reference_df[reference_name_col].tolist()
def match_item_name(item_name):
        if pd.isna(item_name):
            return pd.Series([None, None, None])
          item_name_clean = str(item_name).lower().strip()
result = process.extractOne(item_name_clean, reference_names, scorer=fuzz.token_set_ratio)

        if result is None:
            return pd.Series([None, None, None])

        matched_name, score = result[0], result[1]
if score < score_threshold:
            return pd.Series([None, score, matched_name])

        matched_row = reference_df[reference_df[reference_name_col] == matched_name]
        if matched_row.empty:
            return pd.Series([None, score, matched_name])

        matched_code = matched_row.iloc[0][reference_code_col]
        return pd.Series([matched_code, score, matched_name])
input_df[['Matched UPC', 'Match Score', 'Matched Item Name']] = input_df[input_name_col].apply(match_item_name)

    st.success("✅ Matching complete!")
    st.write(input_df)

    # Download button
    csv_output = input_df.to_csv(index=False).encode('utf-8')
    st.download_button("⬇️ Download Matched CSV", csv_output, "matched_output.csv", "text/csv")
else:
    st.info("Please upload both reference and input CSV files to begin.")
