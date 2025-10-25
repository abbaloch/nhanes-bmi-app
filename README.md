# 🎯 Live Streamlit App

👉 **Access the App Here:** [NHANES BMI & Lifestyle Dashboard](https://nhanes-bmi-app-teambinary.streamlit.app/) [![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://nhanes-bmi-app-teambinary.streamlit.app/)


This app explores how sleep, daily sugar intake, calories, and demographics relate to BMI using the NHANES dataset (2021–2023).  
Developed as part of the *Introduction to Data Science* course — University of Helsinki (2025).


# 🧠 What Really Influences BMI? — Insights from NHANES

> This mini-project and Streamlit app were created by **our group** as part of the *Introduction to Data Science* course at the **University of Helsinki (2025)**.  
> I (**Abdullah**) designed and developed the dashboard and technical report, focusing on data analysis and communication through visual insights.

---

### 🎓 **Course**
**Introduction to Data Science — University of Helsinki (2025)**  

### 👥 **Team Members**
- **Saba** — Data collection, cleaning, preprocessing; feature engineering; presented the final project.  
- **Abdullah** — Exploratory Data Analysis (EDA); additional feature engineering; built the Streamlit dashboard; wrote the technical report.  
- **Imaan** — Machine learning models (Random Forest, XGBoost); model evaluation; designed presentation slides.  

---

## 📘 Project Overview

Our project explores the **NHANES dataset** to understand how different lifestyle and demographic factors — such as **sleep duration**, **daily sugar intake**, **calorie intake**, **age**, and **gender** — influence **BMI** (Body Mass Index).  

We used simple visualizations and clear explanations to make the results understandable for everyone, not just technical readers.  

The dashboard helps visualize:
- Whether people who sleep more or less have different BMI values  
- How sugar intake affects BMI  
- How BMI differs by gender  
- The overall relationships between lifestyle factors  

---

## 🚀 How to Run This Project (Local Setup)

Follow these simple steps to open the app on your computer 👇  

### Step 1 — Files needed
Make sure you have these three files together in one folder:
```
app.py
requirements.txt
cleaned_data.csv
```

### Step 2 — Install required libraries
Open **PowerShell** or **Terminal** in that folder and run:
```bash
pip install -r requirements.txt
```

### Step 3 — Run the Streamlit app
Once installation is done, run:
```bash
python -m streamlit run app.py
```

### Step 4 — Open in your browser
You’ll see a link like this:
```
http://localhost:8501
```
Click it or paste it in your browser to open your dashboard 🎉  

---

## ☁️ How I Deployed the App (Streamlit Cloud)

To make my project accessible online, I used **Streamlit Cloud**.  
Here’s how you can also deploy or re-run it:

1. Go to [https://share.streamlit.io](https://share.streamlit.io) and sign in with your **GitHub** account.  
2. Create a **new public repository** and upload these three files:
   ```
   app.py
   requirements.txt
   cleaned_data.csv
   ```
3. On Streamlit Cloud:
   - Choose your repository (`nhanes-bmi-app`)
   - Branch: `main`
   - App file: `app.py`
   - Click **Deploy**

After a minute, your live link will appear, for example:
```
https://nhanes-bmi-app-yourname.streamlit.app
```

That’s the same process I used for deploying my project.

---

## 📊 Dashboard Features

✅ **At-a-glance summary:**  
Average BMI, average sugar intake (g/day), and average sleep (hours/day).  

✅ **Interactive visualizations:**  
1. **🍬 Sugar vs BMI** – scatter plot with trendline  
2. **😴 BMI by Sleep Group** – bar chart comparing groups  
3. **🚻 BMI by Gender** – bar chart showing differences  
4. **📦 Distributions** – histograms and boxplots  
5. **🧮 Correlation Heatmap** – for technical overview  

✅ **Plain-language insights:**  
Explains the patterns we found in simple, clear English.  

✅ **Expandable sections:**  
Includes “About this project,” “Team Contributions,” and “Acknowledgment.”

---

## 🧪 Data Preparation (inside the app)

The app automatically calculates averages and creates readable labels:

| Original Columns | New Feature Created | Description |
|------------------|--------------------|--------------|
| DR1TSUGR, DR2TSUGR | `sugar_avg` | Average daily sugar intake |
| DR1TKCAL, DR2TKCAL | `kcal_avg` | Average daily calories |
| SLD012, SLD013 | `sleep_avg` | Average daily sleep hours |
| SLD012, SLD013 | `sleep_group` | Sleep category: <6h, 6–7h, 7–9h, >9h |
| RIAGENDR | `gender_label` | 1 = Male, 2 = Female |
| RIDRETH1 | `race_label` | Race/ethnicity categories |

---

## 🧠 Findings (Summary)

From our analysis:
- **Females** had a slightly higher average BMI than males.  
- **Black participants** showed the highest mean BMI among groups.  
- People who consume **more sugar daily** tend to fall into higher BMI categories.  
- Those who sleep **7–9 hours per night** usually have a **lower BMI**.  

These are not cause-and-effect relationships but clear **associations** showing how lifestyle habits relate to body weight.  

---

## 📸 App Preview

For a visual overview, you can run the app locally or view it live on Streamlit Cloud (once deployed).

---

## 🧯 Troubleshooting

| Issue | Solution |
|--------|-----------|
| `ModuleNotFoundError` | Run `pip install -r requirements.txt` |
| `FileNotFoundError: cleaned_data.csv` | Ensure the CSV is in the same folder as `app.py` |
| Streamlit Cloud shows error | Click the **⋮ → View logs**, fix line mentioned, then redeploy |

---

## ⚖️ License / Data Use

This project uses **public NHANES data** for educational purposes only.  
It’s designed for learning and analysis — not for medical advice.

---

🧑‍💻 **Created by Abdullah**  
📘 *Introduction to Data Science — University of Helsinki (2025)*  
💡 *This project demonstrates how interactive dashboards can make data analysis understandable for everyone.*
