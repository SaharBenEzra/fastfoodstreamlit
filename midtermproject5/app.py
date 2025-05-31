import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

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
    try:
        # Replace this URL with your actual file URL
        url = "https://raw.githubusercontent.com/your-username/your-repo/main/FastFoodRestaurants.csv"
        df = pd.read_csv(url)
        df.columns = df.columns.str.strip()
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        # Create sample data for demonstration
        sample_data = {
            'name': ['McDonald\'s', 'Burger King', 'Taco Bell', 'KFC', 'Pizza Hut'] * 100,
            'province': ['CA', 'TX', 'FL', 'NY', 'OH'] * 100,
            'latitude': np.random.uniform(25, 49, 500),
            'longitude': np.random.uniform(-125, -65, 500),
            'address': ['Sample Address'] * 500
        }
        return pd.DataFrame(sample_data)

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
    tab1, tab2, tab3, tab4 = st.tabs(["Brand Analysis", "Geographic Distribution", "Regional Comparison", "Data Explorer"])
    
    with tab1:
        st.subheader("Top Fast Food Brands")
        
        # Number of top brands to show
        n_brands = st.slider("Number of top brands to display:", 5, 20, 10)
        
        # Top brands chart
        top_brands = filtered_df['name'].value_counts().head(n_brands)
        
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(x=top_brands.values, y=top_brands.index, palette='viridis', ax=ax)
        ax.set_title(f'Top {n_brands} Fast Food Brands')
        ax.set_xlabel('Number of Locations')
        ax.set_ylabel('Brand')
        ax.grid(axis='x', alpha=0.3)
        plt.tight_layout()
        st.pyplot(fig)
        
        # Market share
        st.subheader("Market Share Analysis")
        total_restaurants = len(filtered_df)
        market_share = (top_brands / total_restaurants * 100).round(2)
        
        col1, col2 = st.columns(2)
        with col1:
            st.write("**Top Brands by Count:**")
            for brand, count in top_brands.head(5).items():
                st.write(f"• {brand}: {count} locations")
        
        with col2:
            st.write("**Market Share (%):**")
            for brand, share in market_share.head(5).items():
                st.write(f"• {brand}: {share}%")
    
    with tab2:
        st.subheader("Geographic Distribution")
        
        # State distribution
        n_states = st.slider("Number of top states to display:", 5, 25, 15)
        state_counts = filtered_df['province'].value_counts().head(n_states)
        
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(x=state_counts.values, y=state_counts.index, palette='crest', ax=ax)
        ax.set_title(f'Top {n_states} States by Restaurant Count')
        ax.set_xlabel('Number of Locations')
        ax.set_ylabel('State')
        ax.grid(axis='x', alpha=0.3)
        plt.tight_layout()
        st.pyplot(fig)
        
        # Distribution analysis
        st.subheader("Geographic Distribution Analysis")
        
        if 'latitude' in filtered_df.columns and 'longitude' in filtered_df.columns:
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
            
            # Latitude distribution
            filtered_df['latitude'].hist(bins=30, ax=ax1, alpha=0.7, color='skyblue')
            ax1.set_title('Latitude Distribution')
            ax1.set_xlabel('Latitude')
            ax1.set_ylabel('Frequency')
            ax1.grid(alpha=0.3)
            
            # Longitude distribution
            filtered_df['longitude'].hist(bins=30, ax=ax2, alpha=0.7, color='lightcoral')
            ax2.set_title('Longitude Distribution')
            ax2.set_xlabel('Longitude')
            ax2.set_ylabel('Frequency')
            ax2.grid(alpha=0.3)
            
            plt.tight_layout()
            st.pyplot(fig)
        
        # Scatter plot of locations
        if len(filtered_df) <= 1000:  # Only show if not too many points
            st.subheader("Restaurant Locations Scatter Plot")
            fig, ax = plt.subplots(figsize=(10, 6))
            
            # Create scatter plot with different colors for different brands
            brands_for_plot = filtered_df['name'].value_counts().head(5).index
            colors = sns.color_palette("Set1", len(brands_for_plot))
            
            for i, brand in enumerate(brands_for_plot):
                brand_data = filtered_df[filtered_df['name'] == brand]
                ax.scatter(brand_data['longitude'], brand_data['latitude'], 
                          label=brand, alpha=0.6, s=30, color=colors[i])
            
            ax.set_xlabel('Longitude')
            ax.set_ylabel('Latitude')
            ax.set_title('Restaurant Locations by Brand')
            ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
            ax.grid(alpha=0.3)
            plt.tight_layout()
            st.pyplot(fig)
    
    with tab3:
        st.subheader("Regional Brand Comparison")
        
        # Select states to compare
        all_states = sorted(df['province'].unique())
        default_states = ['CA', 'TX', 'FL', 'NY'] if all(state in all_states for state in ['CA', 'TX', 'FL', 'NY']) else all_states[:4]
        
        states_to_compare = st.multiselect(
            "Select states to compare:",
            all_states,
            default=default_states
        )
        
        if states_to_compare:
            # Create comparison data
            fig, axes = plt.subplots(2, 2, figsize=(15, 10))
            axes = axes.flatten()
            
            for i, state in enumerate(states_to_compare[:4]):  # Limit to 4 states for display
                if i < len(axes):
                    state_data = df[df['province'] == state]
                    top_brands_state = state_data['name'].value_counts().head(8)
                    
                    sns.barplot(x=top_brands_state.values, y=top_brands_state.index, 
                              palette='mako', ax=axes[i])
                    axes[i].set_title(f'Top Brands in {state}')
                    axes[i].set_xlabel('Number of Locations')
                    axes[i].set_ylabel('Brand')
                    axes[i].grid(axis='x', alpha=0.3)
            
            # Hide unused subplots
            for i in range(len(states_to_compare), len(axes)):
                axes[i].set_visible(False)
            
            plt.tight_layout()
            st.pyplot(fig)
            
            # Comparison table
            st.subheader("State Comparison Summary")
            comparison_summary = []
            for state in states_to_compare:
                state_data = df[df['province'] == state]
                top_brand = state_data['name'].value_counts().index[0] if len(state_data) > 0 else "N/A"
                total_count = len(state_data)
                unique_brands = state_data['name'].nunique()
                
                comparison_summary.append({
                    'State': state,
                    'Total Restaurants': total_count,
                    'Unique Brands': unique_brands,
                    'Top Brand': top_brand
                })
            
            comparison_df = pd.DataFrame(comparison_summary)
            st.dataframe(comparison_df, use_container_width=True)
    
    with tab4:
        st.subheader("Data Explorer")
        
        # Show raw data sample
        st.write("**Dataset Sample:**")
        st.dataframe(filtered_df.head(10), use_container_width=True)
        
        # Basic statistics
        st.write("**Dataset Statistics:**")
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Numerical Columns:**")
            if 'latitude' in filtered_df.columns:
                st.write(filtered_df[['latitude', 'longitude']].describe())
        
        with col2:
            st.write("**Categorical Columns:**")
            st.write(f"• Total Brands: {filtered_df['name'].nunique()}")
            st.write(f"• Total States: {filtered_df['province'].nunique()}")
            st.write(f"• Total Records: {len(filtered_df)}")
        
        # Brand frequency distribution
        st.subheader("Brand Frequency Distribution")
        brand_counts = filtered_df['name'].value_counts()
        
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.hist(brand_counts.values, bins=20, alpha=0.7, color='steelblue')
        ax.set_xlabel('Number of Locations')
        ax.set_ylabel('Number of Brands')
        ax.set_title('Distribution of Brand Frequencies')
        ax.grid(alpha=0.3)
        plt.tight_layout()
        st.pyplot(fig)
    
    # Insights Section
    st.header("🔍 Key Insights")
    
    # Calculate insights dynamically
    top_brand = df['name'].value_counts().index[0]
    top_state = df['province'].value_counts().index[0]
    total_brands = df['name'].nunique()
    total_states = df['province'].nunique()
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("Brand Dominance")
        st.write(f"""
        **{top_brand}** leads with the highest number of locations nationally.
        
        Out of {total_brands} unique brands in the dataset, the top 10 brands 
        account for a significant portion of all locations, reflecting 
        the dominance of major franchise chains in the fast food industry.
        """)
    
    with col2:
        st.subheader("Geographic Concentration")
        st.write(f"""
        **{top_state}** has the highest concentration of fast food restaurants.
        
        The distribution across {total_states} states shows clear patterns 
        correlating with population density and urbanization levels. 
        Larger states with major metropolitan areas dominate the rankings.
        """)
    
    with col3:
        st.subheader("Market Structure")
        st.write(f"""
        The fast food market shows both **national consolidation** and 
        **regional variation**.
        
        While major chains dominate nationally, different states show 
        varying preferences, suggesting regional tastes and local 
        competition influence market dynamics.
        """)
    
    # Footer
    st.markdown("---")
    st.markdown("**Data Science Midterm Project - Reichman University 2025**")

else:
    st.error("Unable to load dataset. Please check the file path.")
    st.info("Make sure your CSV file is accessible and the URL is correct.")
