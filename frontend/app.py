import streamlit as st
import requests
import pandas as pd
import plotly.express as px

# ---------------- Page Setup ----------------
st.set_page_config(page_title="IntelliDataX", layout="wide")

st.title("📊 IntelliDataX")
st.subheader("Intelligent & Secure Data Analytics Platform")
st.write("Upload a dataset to begin.")

# ---------------- Upload Section ----------------
st.markdown("### 📤 Upload Dataset")

uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])

if uploaded_file is not None:
    st.success(f"Selected file: {uploaded_file.name}")

    if st.button("Upload Dataset"):
        files = {"file": uploaded_file}
        response = requests.post(
            "http://127.0.0.1:8000/upload",
            files=files
        )

        if response.status_code == 200:
            st.success("Dataset uploaded successfully!")
            st.json(response.json())
        else:
            st.error("Upload failed. Check backend.")

# ---------------- Data Cleaning ----------------
st.markdown("### 🧹 Data Cleaning")

if st.button("Run Data Cleaning"):
    response = requests.post("http://127.0.0.1:8000/clean")

    if response.status_code == 200:
        st.success("Data cleaning completed!")
        st.json(response.json())
    else:
        st.error("Data cleaning failed.")

# ---------------- Quick EDA ----------------
st.markdown("---")
st.header("📊 Quick EDA")

# ---- Dataset Summary ----
if st.button("Show Dataset Summary"):
    res = requests.get("http://127.0.0.1:8000/eda/summary")
    data = res.json()

    if "error" in data:
        st.error(data["error"])
    else:
        col1, col2, col3 = st.columns(3)
        col1.metric("Rows", data["rows"])
        col2.metric("Columns", data["columns"])
        col3.metric("Missing Values", data["missing_total"])

        st.subheader("Column Data Types")
        st.json(data["dtypes"])

# ---- Simple Histogram ----
st.subheader("Numeric Feature Distribution")

try:
    df = pd.read_csv("data/processed/cleaned_data.csv")
    num_cols = df.select_dtypes(include="number").columns.tolist()

    if num_cols:
        feature = st.selectbox("Select numeric column", num_cols)
        fig = px.histogram(df, x=feature, nbins=30)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No numeric columns found.")
except:
    st.info("Run data cleaning first to enable EDA.")


st.markdown("---")
st.header("📈 Advanced EDA")

# ---- Correlation Heatmap ----
if st.button("Show Correlation Heatmap"):
    res = requests.get("http://127.0.0.1:8000/eda/correlation")
    data = res.json()

    if "error" in data:
        st.error(data["error"])
    else:
        corr_df = pd.DataFrame(data)
        fig = px.imshow(corr_df, text_auto=True, aspect="auto")
        st.plotly_chart(fig, use_container_width=True)

# ---- Missing Values Chart ----
if st.button("Show Missing Values per Column"):
    res = requests.get("http://127.0.0.1:8000/eda/missing")
    data = res.json()

    if "error" in data:
        st.error(data["error"])
    else:
        miss_df = pd.DataFrame({
            "column": data.keys(),
            "missing_values": data.values()
        })
        fig = px.bar(miss_df, x="column", y="missing_values")
        st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
st.header("🧠 Intelligent Insights")

if st.button("Generate Insights"):
    res = requests.get("http://127.0.0.1:8000/eda/insights")
    data = res.json()

    if "error" in data:
        st.error(data["error"])
    else:
        if data["insights"]:
            for insight in data["insights"]:
                st.success(insight)
        else:
            st.info("No significant insights found.")

