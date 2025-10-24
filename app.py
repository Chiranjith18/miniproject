import streamlit as st
import pandas as pd
import plotly.express as px

csv_path = "restaurant_final_risk_classification (6).csv"
df = pd.read_csv(csv_path)

risk_order = {"High Risk": 1, "Medium Risk": 2, "Low Risk": 3}
df['Risk_Rank'] = df['Category'].map(risk_order).fillna(99)
cities = df['City'].unique()[:5]

st.set_page_config(page_title="SafeBite Restaurant Risk", page_icon="🍽", layout="wide")

# Top header & team details (black heading)
st.markdown(
    """
    <div style="text-align:center;">
      <h1 style='color:black;'>🍽 Restaurant Risk Dashboard</h1>
      <div style='font-size:20px; color:black;'>
        By <b>Chiranjith</b> | Team: <b>LoneWolf</b> | Team No: <b>A6</b>
      </div>
    </div>
    """,
    unsafe_allow_html=True
)
st.markdown("<hr>", unsafe_allow_html=True)

# Project Resources with explicit ownership
st.markdown(
    """
    <div style="background-color:#e3f2fd;padding:1rem;border-radius:8px;">
      <b>🔗 Project Resources (developed by Chiranjith):</b><br>
      💻 <a href="https://colab.research.google.com/drive/1doBHSL_tcRLhVpY4rpxTO8gkjMD96LR9?usp=sharing" target="_blank" style="color:#1565C0;text-decoration:underline;">Colab Model Notebook (Zero-Shot Classification, Chiranjith's Work)</a><br>
      🛠️ <a href="https://github.com/Chiranjith18/reviewscraper.git" target="_blank" style="color:#1565C0;text-decoration:underline;">Review Scraper (Selenium, Java, Chiranjith's Repo)</a>
    </div>
    """,
    unsafe_allow_html=True
)
st.markdown("<br>", unsafe_allow_html=True)

# City selector
st.subheader("Select a city to view ranked restaurant risk:")
selected_city = st.selectbox("City", options=cities)
st.write(f"### Showing risk info for **{selected_city}** 🏙️")

city_df = df[df['City'] == selected_city].copy().sort_values('Risk_Rank')

# Restaurant count badge
st.markdown(f"<span style='font-size:18px;color:#1976D2;'>Found <b>{len(city_df)}</b> restaurants in <b>{selected_city}</b></span>", unsafe_allow_html=True)

# Risk distribution pie chart
risk_counts = city_df['Category'].value_counts().reset_index()
risk_counts.columns = ['Category', 'Count']
fig = px.pie(
    risk_counts,
    names='Category',
    values='Count',
    color='Category',
    color_discrete_map={
        "High Risk": "red",
        "Medium Risk": "orange",
        "Low Risk": "green"
    },
    title="Risk Distribution"
)
st.plotly_chart(fig, use_container_width=True)

# Top 3 high-risk restaurants
high_risk = city_df[city_df['Category'] == 'High Risk'].head(3)
if not high_risk.empty:
    st.warning("🚨 **Top 3 High Risk Restaurants:**")
    for r in high_risk['Restaurant']:
        st.markdown(f"* {r}")

# Table styling
def color_risk(val):
    if 'high' in str(val).lower():
        return 'background-color: #C62828; color: white; font-weight: bold'
    elif 'medium' in str(val).lower():
        return 'background-color: #FF9800; color: black; font-weight: bold'
    elif 'low' in str(val).lower():
        return 'background-color: #2E7D32; color: white; font-weight: bold'
    return ''

st.markdown("<br><b style='font-size:18px'>🏆 Risk Ranked Restaurants</b>", unsafe_allow_html=True)
st.dataframe(
    city_df[['Restaurant', 'Category']].style.map(color_risk, subset=['Category']),
    height=520,
    use_container_width=True
)

with st.expander("About SafeBite (click to expand)"):
    st.write("""
    - 🚦 Predicts restaurant safety risk from Google reviews
    - Uses Zero-Shot NLP model (Colab, our custom implementation)
    - Java Selenium-powered review scraping (our repo)
    - Data-driven 'High', 'Medium', 'Low' categorization
    - Clean, interactive Streamlit dashboard for presentation
    """)

st.markdown(
    "<hr><p style='text-align:center; font-size:14px;'>Made for <b>HACK IT ON'25</b> | SafeBite by LoneWolf (Chiranjith)</p>", 
    unsafe_allow_html=True
)
