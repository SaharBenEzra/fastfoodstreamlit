import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

# Debug file path
st.write("Current directory:", os.getcwd())
if not os.path.exists("FastFoodRestaurants.csv"):
    st.error("FastFoodRestaurants.csv not found!")
    st.stop()

# Load data
df = pd.read_csv("FastFoodRestaurants.csv")
df.columns = df.columns.str.strip()

# Title and intro
st.title("🍔 Fast Food Restaurants Across America")
st.markdown("""
**Author:** Sahar Ben Ezra  
**Dataset:** [Kaggle - Fast Food Restaurants](https://www.kaggle.com/datasets/imtkaggleteam/fast-food-restaurants-across-america)

This dashboard analyzes the distribution and popularity of fast food brands across U.S. states.
""")

# Preview data
st.subheader("🔍 Sample of the Data")
st.dataframe(df.head())

# Dataset structure
st.subheader("📊 Dataset Overview")
st.write("Shape of dataset:", df.shape)
st.write("Column types:")
st.write(df.dtypes)
st.write("Missing values per column:")
st.write(df.isnull().sum())
st.write("Number of unique brands:", df['name'].nunique())
st.write("Top 10 brands:")
st.write(df['name'].value_counts().head(10))

# Plot 1: Top 10 Brands
st.subheader("🏆 Top 10 Fast Food Brands in the U.S.")
top_brands = df['name'].value_counts().head(10).reset_index()
top_brands.columns = ['Brand', 'Count']
fig1, ax1 = plt.subplots(figsize=(10,6))
sns.barplot(data=top_brands, x='Count', y='Brand', palette='viridis', ax=ax1)
st.pyplot(fig1)

# Plot 2: Top 15 States
st.subheader("🗺️ Top 15 States by Number of Restaurants")
top_states = df['province'].value_counts().head(15).reset_index()
top_states.columns = ['State', 'Count']
fig2, ax2 = plt.subplots(figsize=(10,6))
sns.barplot(data=top_states, x='Count', y='State', palette='crest', ax=ax2)
st.pyplot(fig2)

# State filter
st.subheader("📍 Explore by State")
selected_state = st.selectbox("Choose a U.S. state:", sorted(df['province'].unique()))
df_state = df[df['province'] == selected_state]
top_state_brands = df_state['name'].value_counts().head(10).reset_index()
top_state_brands.columns = ['Brand', 'Count']
fig3, ax3 = plt.subplots(figsize=(10,6))
sns.barplot(data=top_state_brands, x='Count', y='Brand', palette='magma', ax=ax3)
st.pyplot(fig3)

# Insights
st.subheader("💡 Insights")
st.markdown("""
**Insight 1: Brand Dominance**  
McDonald's is the most dominant brand nationally, followed by Burger King and Taco Bell.

**Insight 2: Geographic Concentration**  
States like California and Texas have the highest number of fast food locations, reflecting population size and car dependency.

**Insight 3: Regional Preferences**  
Different states show variation in brand rankings, highlighting regional preferences.
""")
