import streamlit as st
import pandas as pd
import plotly.express as px

# --- PAGE CONFIG ---
st.set_page_config(page_title="Car Sales Dashboard", page_icon="🚗", layout="wide")

# --- LOAD DATA ---
@st.cache_data
def load_data():
    df = pd.read_csv("Car_sales.csv")
    return df

df = load_data()

st.title("🚘 Car Sales Dashboard")
st.markdown("#### A fully interactive and error-proof visualization dashboard for your car dataset.")

st.markdown("---")

# --- AUTO-DETECT COLUMNS ---
numeric_cols = df.select_dtypes(include=["int64", "float64"]).columns.tolist()
categorical_cols = df.select_dtypes(include=["object"]).columns.tolist()

# --- SIDEBAR FILTERS ---
st.sidebar.header("🔧 Filters")

# Pick manufacturer or similar categorical column
if len(categorical_cols) > 0:
    main_cat_col = st.sidebar.selectbox("Select Main Category (e.g., Manufacturer)", categorical_cols)
    unique_vals = ["All"] + sorted(df[main_cat_col].dropna().unique().tolist())
    selected_cat = st.sidebar.selectbox(f"Filter by {main_cat_col}", unique_vals)
    if selected_cat != "All":
        df = df[df[main_cat_col] == selected_cat]
else:
    st.sidebar.warning("⚠️ No categorical columns found for filtering.")

# --- KPI SECTION ---
st.markdown("### 📈 Key Statistics")
cols = st.columns(4)
for i, col in enumerate(numeric_cols[:4]):  # Show up to 4 KPIs
    cols[i].metric(f"{col}", f"{df[col].mean():,.2f}")

st.markdown("---")

# --- DATA PREVIEW ---
with st.expander("📋 View Dataset"):
    st.dataframe(df)

# --- VISUALIZATION 1: BAR CHART ---
if len(categorical_cols) > 0 and len(numeric_cols) > 0:
    st.subheader("📊 Bar Chart")
    x_col = st.selectbox("Select Category (X-axis):", categorical_cols)
    y_col = st.selectbox("Select Numeric Value (Y-axis):", numeric_cols)
    bar_data = df.groupby(x_col)[y_col].mean().sort_values(ascending=False).head(15)
    fig_bar = px.bar(
        bar_data,
        x=bar_data.index,
        y=bar_data.values,
        title=f"Average {y_col} by {x_col}",
        labels={"x": x_col, "y": y_col},
        color=bar_data.values,
        color_continuous_scale="Viridis"
    )
    fig_bar.update_layout(template="plotly_white")
    st.plotly_chart(fig_bar, use_container_width=True)

# --- VISUALIZATION 2: SCATTER PLOT ---
if len(numeric_cols) >= 2:
    st.subheader("📉 Scatter Plot")
    scatter_x = st.selectbox("X-axis", numeric_cols, key="xaxis")
    scatter_y = st.selectbox("Y-axis", numeric_cols, key="yaxis")
    color_col = st.selectbox("Color by (optional)", [None] + categorical_cols)
    fig_scatter = px.scatter(
        df,
        x=scatter_x,
        y=scatter_y,
        color=color_col,
        hover_data=df.columns,
        title=f"{scatter_x} vs {scatter_y}",
        color_discrete_sequence=px.colors.qualitative.Bold
    )
    fig_scatter.update_layout(template="plotly_white")
    st.plotly_chart(fig_scatter, use_container_width=True)

# --- VISUALIZATION 3: HISTOGRAM ---
if len(numeric_cols) > 0:
    st.subheader("📦 Distribution Plot")
    hist_col = st.selectbox("Select Numeric Column", numeric_cols, key="hist")
    fig_hist = px.histogram(df, x=hist_col, nbins=25, color_discrete_sequence=["#1f77b4"])
    fig_hist.update_layout(template="plotly_white", title=f"Distribution of {hist_col}")
    st.plotly_chart(fig_hist, use_container_width=True)

# --- VISUALIZATION 4: PIE CHART ---
if len(categorical_cols) > 0:
    st.subheader("🥧 Category Distribution")
    pie_col = st.selectbox("Select Categorical Column", categorical_cols, key="pie")
    pie_data = df[pie_col].value_counts().head(10)
    fig_pie = px.pie(
        values=pie_data.values,
        names=pie_data.index,
        title=f"Top {pie_col} Distribution",
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    st.plotly_chart(fig_pie, use_container_width=True)

# --- DOWNLOAD FILTERED DATA ---
st.markdown("---")
st.subheader("📥 Download Filtered Data")
csv = df.to_csv(index=False).encode("utf-8")
st.download_button("Download as CSV", csv, "filtered_car_sales.csv", "text/csv")

st.markdown("<br>", unsafe_allow_html=True)
st.caption("🚗 Built with ❤️ using Streamlit + Plotly | © 2025")
