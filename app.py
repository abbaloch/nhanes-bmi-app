import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# ----------------------------------
# Page config
# ----------------------------------
st.set_page_config(page_title="NHANES BMI & Lifestyle Dashboard", layout="wide")

# ----------------------------------
# Header / About (as requested)
# ----------------------------------
st.title("🍎 What Really Influences BMI? — Insights from NHANES")
st.caption("Introduction to Data Science — University of Helsinki (2025)")

st.markdown("<center><small>University of Helsinki — <br>Mini-Project: “What Really Influences BMI?”</small></center>", unsafe_allow_html=True)
with st.expander("About this project"):
    st.markdown("""
Our group explored the NHANES dataset to understand what influences BMI beyond weight and height. 
The goal was to present these findings in a simple way for everyone, not just data experts.

We combined different data aspects such as daily sugar, calories, sleep hours, gender, and race. 
Using visual analysis and interactive charts, we found patterns showing that people who sleep between **7–9 hours** tend to have slightly lower BMI, 
while higher **daily sugar intake** often appears in groups with higher BMI.

These insights do not prove cause and effect but show how lifestyle and demographic factors connect to BMI — highlighting how **balanced sleep and reduced sugar intake** may help maintain healthier body composition.
""")

with st.expander("👥 Team Contributions"):
    st.markdown("""
This mini-project was a collaborative effort by our group, where each member played a distinct and complementary role throughout the workflow.  

- **Saba** – Led **data collection, cleaning, and preprocessing**, performed **feature engineering**, and also **presented the project** during the final presentation.  
- **Abdullah** – Responsible for **exploratory data analysis (EDA)**, **additional feature engineering**, **Streamlit dashboard development**, and **technical report preparation**.  
- **Imaan** – Focused on **machine-learning model development**, including **Random Forest** and **XGBoost** training, **model evaluation**, and **presentation slide design**.
""")

with st.expander("🙏 Acknowledgment"):
    st.markdown("""
We thank the **course instructors and teaching assistants** for their continuous guidance and support throughout this mini-project.
""")

st.markdown("---")

# ----------------------------------
# Helper functions
# ----------------------------------
def mean_two(a, b):
    a = pd.to_numeric(a, errors="coerce")
    b = pd.to_numeric(b, errors="coerce")
    return pd.concat([a, b], axis=1).mean(axis=1)

def make_sleep_group(s):
    try:
        x = float(s)
    except:
        return "Unknown"
    if x < 6: return "<6h"
    if x <= 7: return "6–7h"
    if x <= 9: return "7–9h"
    return ">9h"

def map_gender(code):
    m = {1: "Male", 2: "Female"}
    try:
        return m.get(int(code), "Unknown")
    except:
        return "Unknown"

def map_race(code):
    m = {
        1: "Mexican American",
        2: "Other Hispanic",
        3: "Non‑Hispanic White",
        4: "Non‑Hispanic Black",
        5: "Other/Multi"
    }
    try:
        return m.get(int(code), "Unknown")
    except:
        return "Unknown"

# ----------------------------------
# Load and prepare dataset
# ----------------------------------
@st.cache_data
def load_and_prepare(path):
    df = pd.read_csv(path)
    if "DR1TSUGR" in df.columns or "DR2TSUGR" in df.columns:
        df["sugar_avg"] = mean_two(df.get("DR1TSUGR"), df.get("DR2TSUGR"))
    if "DR1TKCAL" in df.columns or "DR2TKCAL" in df.columns:
        df["kcal_avg"] = mean_two(df.get("DR1TKCAL"), df.get("DR2TKCAL"))
    if "SLD012" in df.columns or "SLD013" in df.columns:
        df["sleep_avg"] = mean_two(df.get("SLD012"), df.get("SLD013"))
        df["sleep_group"] = df["sleep_avg"].apply(make_sleep_group)
    if "RIAGENDR" in df.columns:
        df["gender_label"] = df["RIAGENDR"].apply(map_gender)
    if "RIDRETH1" in df.columns:
        df["race_label"] = df["RIDRETH1"].apply(map_race)
    for c in ["BMXBMI", "sugar_avg", "kcal_avg", "sleep_avg"]:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce")
    return df

data_path = st.sidebar.text_input("Path to data CSV", "cleaned_data.csv")
try:
    df = load_and_prepare(data_path)
    st.success(f"Loaded {len(df):,} rows from {data_path}")
except Exception as e:
    st.error(f"Could not load data from '{data_path}'. Error: {e}")
    st.stop()

# ----------------------------------
# Sidebar filters
# ----------------------------------
st.sidebar.header("Filters")
genders = ["All"]
if "gender_label" in df.columns:
    genders = ["All"] + sorted([g for g in df["gender_label"].dropna().unique().tolist()])
gender_sel = st.sidebar.selectbox("Gender", genders, index=0)

if "sleep_avg" in df.columns and df["sleep_avg"].notna().any():
    smin = int(max(0, np.nanmin(df["sleep_avg"])))
    smax = int(min(12, np.nanmax(df["sleep_avg"])))
else:
    smin, smax = 0, 12
sleep_min, sleep_max = st.sidebar.slider("Sleep hours (avg)", 0, 12, (smin, smax))

if "sugar_avg" in df.columns and df["sugar_avg"].notna().any():
    sug_min = int(np.nanmin(df["sugar_avg"]))
    sug_max = int(np.nanmax(df["sugar_avg"]))
else:
    sug_min, sug_max = 0, 400
sugar_min, sugar_max = st.sidebar.slider("Daily sugar (g)", max(0, sug_min), max(1, sug_max), (max(0, sug_min), min(300, max(1, sug_max))))

mask = pd.Series(True, index=df.index)
if gender_sel != "All" and "gender_label" in df.columns:
    mask &= (df["gender_label"] == gender_sel)
if "sleep_avg" in df.columns:
    mask &= df["sleep_avg"].between(sleep_min, sleep_max, inclusive="both")
if "sugar_avg" in df.columns:
    mask &= df["sugar_avg"].between(sugar_min, sugar_max, inclusive="both")

fdf = df[mask].copy()

# ----------------------------------
# KPI Section
# ----------------------------------
st.subheader("At‑a‑glance")
k1, k2, k3 = st.columns(3)

def fmt_mean(d, col):
    if col not in d.columns or d[col].dropna().empty:
        return "N/A"
    return f"{d[col].mean():.2f}"

k1.metric("Average BMI", fmt_mean(fdf, "BMXBMI"))
k2.metric("Avg daily sugar (g)", fmt_mean(fdf, "sugar_avg"))
k3.metric("Avg sleep (h)", fmt_mean(fdf, "sleep_avg"))
st.markdown("---")

# ----------------------------------
# Tabs for Visualizations
# ----------------------------------
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🍬 Sugar vs BMI", "😴 BMI by Sleep Group", "🚻 BMI by Gender", "📦 Distributions", "🧮 Correlation Heatmap"
])

with tab1:
    st.markdown("#### Sugar vs BMI")
    if all(c in fdf.columns for c in ["sugar_avg", "BMXBMI"]):
        color_col = "sleep_group" if "sleep_group" in fdf.columns else None
        fig = px.scatter(
            fdf, x="sugar_avg", y="BMXBMI", color=color_col,
            color_discrete_sequence=["#1f77b4", "#ff7f0e", "#2ca02c"],
            hover_data=["SEQN"] + [c for c in ["gender_label","race_label","sleep_avg","kcal_avg"] if c in fdf.columns],
            trendline="ols"
        )
        fig.update_layout(height=520, margin=dict(l=10,r=10,t=10,b=10))
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Needed columns not found for this chart: 'sugar_avg' and 'BMXBMI'.")

with tab2:
    st.markdown("#### Average BMI by Sleep Group")
    if all(c in df.columns for c in ["sleep_group", "BMXBMI"]):
        grp = df.groupby("sleep_group", dropna=False)["BMXBMI"].mean().reset_index().sort_values("BMXBMI", ascending=False)
        fig2 = px.bar(grp, x="sleep_group", y="BMXBMI", text="BMXBMI", color="sleep_group",
                      color_discrete_sequence=["#2ca02c","#ff7f0e","#1f77b4","#8c564b"])
        fig2.update_traces(texttemplate="%{text:.2f}", textposition="outside")
        fig2.update_layout(height=520, margin=dict(l=10,r=10,t=10,b=10))
        st.plotly_chart(fig2, use_container_width=True)
    else:
        st.info("Sleep features not available.")

with tab3:
    st.markdown("#### Average BMI by Gender")
    if all(c in df.columns for c in ["gender_label", "BMXBMI"]):
        gg = df.groupby("gender_label", dropna=False)["BMXBMI"].mean().reset_index().sort_values("BMXBMI", ascending=False)
        fig3 = px.bar(gg, x="gender_label", y="BMXBMI", text="BMXBMI", color="gender_label",
                      color_discrete_sequence=["#1f77b4", "#ff7f0e"])
        fig3.update_traces(texttemplate="%{text:.2f}", textposition="outside")
        fig3.update_layout(height=520, margin=dict(l=10,r=10,t=10,b=10))
        st.plotly_chart(fig3, use_container_width=True)
    else:
        st.info("Gender labels not available.")

with tab4:
    st.markdown("#### Distributions")
    numeric_cols = [c for c in fdf.columns if pd.api.types.is_numeric_dtype(fdf[c])]
    default_cols = [c for c in ["BMXBMI","sugar_avg","sleep_avg","kcal_avg"] if c in numeric_cols]
    cols_sel = st.multiselect("Choose numeric columns", options=numeric_cols, default=default_cols)
    if cols_sel:
        for c in cols_sel:
            fig4 = px.histogram(fdf, x=c, nbins=30, marginal="box",
                                color_discrete_sequence=["#1f77b4"])
            st.plotly_chart(fig4, use_container_width=True)
    else:
        st.info("Select at least one numeric column to show distributions.")

with tab5:
    st.markdown("#### Correlation Heatmap (technical view)")
    corr_cols = [c for c in ["BMXBMI","sugar_avg","kcal_avg","sleep_avg","RIDAGEYR","BMXHT","BMXWT","INDFMPIR"] if c in df.columns]
    if len(corr_cols) >= 2:
        cmat = df[corr_cols].corr(method="pearson")
        fig5 = px.imshow(cmat, text_auto=True, aspect="auto", color_continuous_scale="RdBu_r")
        fig5.update_layout(height=520, margin=dict(l=10,r=10,t=10,b=10))
        st.plotly_chart(fig5, use_container_width=True)
    else:
        st.info("Not enough numeric columns to compute a correlation heatmap.")

st.markdown("---")

# ----------------------------------
# Findings section
# ----------------------------------
st.markdown("""
### 🧠 Findings 
From our analysis, we observed that females had a slightly higher average BMI than males, 
and Black participants showed the highest mean BMI among groups. 
When sugar intake increased, more individuals tended to be overweight or obese.

Adding sleep features showed that people who sleep **7–9 hours** tend to have **lower BMI** compared to those sleeping less or more. 
These are associations, not causes, but they highlight how **lifestyle habits** like **sleep and sugar consumption** relate to BMI patterns.

Overall, this project shows that combining **data visualization and simple analysis** can help explain how daily habits may influence health outcomes.
""")
