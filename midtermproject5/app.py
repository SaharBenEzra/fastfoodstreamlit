import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go

# Configure page
st.set_page_config(
    page_title="Fast Food Restaurants Analysis",
    page_icon="🍔",
    layout="wide"
)

# Title and introduction
st.title("🍔 Fast Food Restaurants Across America")
st.markdown("""
**By: Sahar Ben Ezra – 319074837**

This analysis explores the distribution patterns of fast food restaurants across the United States,
examining brand presence, geographic trends, and regional preferences.

**Dataset Source:** [Kaggle - Fast Food Restaurants Across America](https://www.kaggle.com/datasets/imtkaggleteam/fast-food-restaurants-across-america)
""")

# Load data function
@st.cache_data
def load_data():
    # You'll need to upload your CSV to GitHub or use st.file_uploader
    # For now, using a placeholder - replace with your actual data loading
    try:
        df = pd.read_csv('FastFoodRestaurants.csv')  # Replace with your file path
        df.columns = df.columns.str.strip()
        return df
    except:
        st.error("Please upload the dataset file")
        return None

# Load the data
df = load_data()

if df is not None:
    # Sidebar for filters
    st.sidebar.header("Filters")
    
    # State filter
    states = ['All'] + sorted(df['province'].unique().tolist())
    selected_state = st.sidebar.selectbox("Select State:", states)
    
    # Brand filter
    brands = ['All'] + sorted(df['name'].unique().tolist())
    selected_brand = st.sidebar.selectbox("Select Brand:", brands)
    
    # Apply filters
    filtered_df = df.copy()
    if selected_state != 'All':
        filtered_df = filtered_df[filtered_df['province'] == selected_state]
    if selected_brand != 'All':
        filtered_df = filtered_df[filtered_df['name'] == selected_brand]
    
    # Dataset Overview
    st.header("📊 Dataset Overview")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Restaurants", len(filtered_df))
    with col2:
        st.metric("Unique Brands", filtered_df['name'].nunique())
    with col3:
        st.metric("States Covered", filtered_df['province'].nunique())
    with col4:
        st.metric("Missing Values", filtered_df.isnull().sum().sum())
    
    # Main Analysis Tabs
    tab1, tab2, tab3, tab4 = st.tabs(["Brand Analysis", "Geographic Distribution", "Regional Comparison", "Interactive Map"])
    
    with tab1:
        st.subheader("Top Fast Food Brands")
        
        # Top brands chart
        top_brands = filtered_df['name'].value_counts().head(10)
        
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(x=top_brands.values, y=top_brands.index, palette='viridis', ax=ax)
        ax.set_title('Top 10 Fast Food Brands')
        ax.set_xlabel('Number of Locations')
        ax.set_ylabel('Brand')
        plt.tight_layout()
        st.pyplot(fig)
        
        # Show data table
        if st.checkbox("Show detailed brand data"):
            st.dataframe(filtered_df['name'].value_counts())
    
    with tab2:
        st.subheader("Geographic Distribution")
        
        # State distribution
        state_counts = filtered_df['province'].value_counts().head(15)
        
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(x=state_counts.values, y=state_counts.index, palette='crest', ax=ax)
        ax.set_title('Top 15 States by Restaurant Count')
        ax.set_xlabel('Number of Locations')
        ax.set_ylabel('State')
        plt.tight_layout()
        st.pyplot(fig)
        
        # Distribution histogram
        st.subheader("Distribution Analysis")
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
        
        # Latitude distribution
        filtered_df['latitude'].hist(bins=30, ax=ax1, alpha=0.7)
        ax1.set_title('Latitude Distribution')
        ax1.set_xlabel('Latitude')
        ax1.set_ylabel('Frequency')
        
        # Longitude distribution
        filtered_df['longitude'].hist(bins=30, ax=ax2, alpha=0.7)
        ax2.set_title('Longitude Distribution')
        ax2.set_xlabel('Longitude')
        ax2.set_ylabel('Frequency')
        
        plt.tight_layout()
        st.pyplot(fig)
    
    with tab3:
        st.subheader("Regional Brand Comparison")
        
        # Select states to compare
        states_to_compare = st.multiselect(
            "Select states to compare:",
            df['province'].unique(),
            default=['CA', 'TX', 'FL', 'NY']
        )
        
        if states_to_compare:
            comparison_data = []
            for state in states_to_compare:
                state_data = df[df['province'] == state]
                top_brands_state = state_data['name'].value_counts().head(5)
                for brand, count in top_brands_state.items():
                    comparison_data.append({'State': state, 'Brand': brand, 'Count': count})
            
            if comparison_data:
                comparison_df = pd.DataFrame(comparison_data)
                
                # Create grouped bar chart
                fig = px.bar(comparison_df, x='State', y='Count', color='Brand',
                           title='Top Brands by State Comparison',
                           height=500)
                st.plotly_chart(fig, use_container_width=True)
    
    with tab4:
        st.subheader("Interactive Restaurant Map")
        
        # Sample the data for better performance
        map_data = filtered_df.sample(min(1000, len(filtered_df)))
        
        # Create map
        fig = px.scatter_mapbox(
            map_data,
            lat="latitude",
            lon="longitude",
            color="name",
            hover_name="name",
            hover_data=["address", "province"],
            zoom=3,
            height=600,
            title="Fast Food Restaurant Locations"
        )
        
        fig.update_layout(mapbox_style="open-street-map")
        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        st.plotly_chart(fig, use_container_width=True)
    
    # Insights Section
    st.header("🔍 Key Insights")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("Brand Dominance")
        st.write("""
        McDonald's leads with the highest number of locations nationally,
        followed by major chains like Burger King and Taco Bell.
        This reflects their extensive marketing reach and franchise model.
        """)
    
    with col2:
        st.subheader("Geographic Concentration")
        st.write("""
        California and Texas dominate in total restaurant count,
        correlating with their large populations and car-dependent culture.
        This suggests market size drives expansion strategies.
        """)
    
    with col3:
        st.subheader("Regional Preferences")
        st.write("""
        Different states show varying brand preferences.
        Regional chains like Whataburger in Texas demonstrate
        local market adaptation and consumer loyalty.
        """)

else:
    st.error("Unable to load dataset. Please check the file path.")
    st.info("Upload your dataset file or update the file path in the code.")
