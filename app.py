import streamlit as st
import pandas as pd
import plotly.express as px
from io import BytesIO

# 🎨 Custom Styling
st.set_page_config(page_title="📊 Data Manager", layout="wide")
st.markdown(
    """
    <style>
        body { background-color: #f5f5f5; }
        .main { background-color: #ffffff; padding: 20px; border-radius: 10px; }
        h1 { color: #6a1b9a; text-align: center; font-family: 'Arial', sans-serif; }
        .stButton>button { background: linear-gradient(45deg, #6a1b9a, #9c27b0); color: white; border-radius: 8px; }
        .stSidebar { background-color: #e1bee7; padding: 15px; border-radius: 10px; }
    </style>
    """,
    unsafe_allow_html=True,
)

# 🎯 Function to Load Data
@st.cache_data
def load_data(file):
    return pd.read_csv(file)

# 🎯 Function to Clean Data
def clean_data(df):
    df.drop_duplicates(inplace=True)
    df.fillna("Missing", inplace=True)
    return df

# 🎯 Function to Convert Data
def convert_data(df, format):
    output = BytesIO()
    if format == "CSV":
        df.to_csv(output, index=False)
    elif format == "Excel":
        df.to_excel(output, index=False, engine='openpyxl')
    return output.getvalue()

# 🏡 Main App Title
st.title("📊 Data Management & Cleaning Tool")

# 📂 Sidebar for File Upload
st.sidebar.header("📂 Upload Your CSV File")
uploaded_file = st.sidebar.file_uploader("Choose a CSV file", type=["csv"])

if uploaded_file:
    df = load_data(uploaded_file)
    st.markdown("### 🔍 Data Preview", unsafe_allow_html=True)
    st.dataframe(df.head(), use_container_width=True)

    # Data Cleaning Options
    st.subheader("🧹 Data Cleaning Options")
    if st.button("🧹 Remove Duplicates"):
        df = clean_data(df)
        st.success("✅ Duplicates removed & missing values filled!")
        st.dataframe(df.head())
    
    # Column Selection
    st.subheader("📌 Select Columns to Keep")
    selected_columns = st.multiselect("Choose columns to keep", df.columns, default=df.columns.tolist())
    df = df[selected_columns]
    
    # Data Visualization
    st.subheader("📈 Data Visualization")
    numeric_columns = df.select_dtypes(include=['number']).columns
    if len(numeric_columns) > 0:
        selected_column = st.selectbox("Select a column for visualization", numeric_columns)
        chart_type = st.radio("Choose Chart Type", ["Histogram", "Scatter", "Line"])
        if chart_type == "Histogram":
            fig = px.histogram(df, x=selected_column, title=f"Histogram of {selected_column}")
        elif chart_type == "Scatter":
            fig = px.scatter(df, x=selected_column, y=numeric_columns[0], title=f"Scatter Plot")
        elif chart_type == "Line":
            fig = px.line(df, x=df.index, y=selected_column, title=f"Line Chart")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("⚠️ No numeric columns available for visualization!")

    # Data Conversion
    st.subheader("📂 Convert Data Format")
    format_option = st.radio("Choose format", ["CSV", "Excel"])
    converted_data = convert_data(df, format_option)
    st.download_button(label=f"⬇️ Download {format_option}", data=converted_data, file_name=f"cleaned_data.{format_option.lower()}", mime=f"text/{format_option.lower()}")
