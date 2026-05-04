import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import os
from streamlit_option_menu import option_menu

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="InsightGrid | Sales Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CUSTOM CSS FOR PREMIUM UI ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700;800&display=swap');

    /* Main container styling */
    .main {
        background: linear-gradient(135deg, #f6f9fc 0%, #edf2f9 100%);
    }
    
    /* Base text */
    * {
        font-family: 'Outfit', sans-serif !important;
    }
    
    /* Custom Card Styling - Glassmorphism */
    .metric-card {
        background: rgba(255, 255, 255, 0.7);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border-radius: 16px;
        padding: 1.5rem;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.8);
        margin-bottom: 1rem;
        transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
        position: relative;
        overflow: hidden;
    }
    
    /* Card Accent */
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 4px;
        height: 100%;
        background: linear-gradient(to bottom, #4f46e5, #ec4899);
        border-radius: 16px 0 0 16px;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.1);
        background: rgba(255, 255, 255, 0.9);
    }
    
    .metric-label {
        color: #64748b;
        font-size: 0.875rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 0.5rem;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    
    .metric-value {
        color: #0f172a;
        font-size: 2rem;
        font-weight: 800;
        line-height: 1.2;
        background: linear-gradient(90deg, #0f172a, #334155);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid #e2e8f0;
    }
    
    /* Title styling */
    h1 {
        color: #0f172a;
        font-weight: 800 !important;
        margin-bottom: 2rem !important;
        background: linear-gradient(90deg, #1e293b, #475569);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    h3, h2 {
        color: #1e293b;
        font-weight: 700 !important;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# --- HELPER FUNCTIONS ---
@st.cache_data
def load_data(file):
    try:
        # If it's a file path (string), read it. If it's an uploaded file object, read it.
        df = pd.read_csv(file)
        
        # Column Normalization
        col_map = {
            'date': 'Date',
            'product': 'Product',
            'category': 'Category',
            'quantity': 'Quantity',
            'price': 'Price',
            'revenue': 'Revenue',
            'sales': 'Revenue'
        }
        
        # Rename columns case-insensitively
        df.columns = [col.strip().lower() for col in df.columns]
        df = df.rename(columns={k: v for k, v in col_map.items() if k in df.columns})
        
        # Convert Date to datetime
        if 'Date' in df.columns:
            df['Date'] = pd.to_datetime(df['Date'])
        
        # Calculate Revenue if missing but Quantity and Price exist
        if 'Revenue' not in df.columns and 'Quantity' in df.columns and 'Price' in df.columns:
            df['Revenue'] = df['Quantity'] * df['Price']
            
        # Basic Cleaning
        df = df.dropna(subset=['Date', 'Revenue'])
        
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

def kpi_card(label, value, prefix="", icon=""):
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">{icon} {label}</div>
        <div class="metric-value">{prefix}{value}</div>
    </div>
    """, unsafe_allow_html=True)

# --- TOP NAVIGATION BAR ---
selected = option_menu(
    menu_title=None,
    options=["Home", "Data Hub", "Dashboard"],
    icons=["house", "cloud-upload", "bar-chart-line"],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal",
    styles={
        "container": {"padding": "0!important", "background-color": "transparent"},
        "icon": {"color": "#4f46e5", "font-size": "18px"}, 
        "nav-link": {"font-size": "16px", "text-align": "center", "margin":"0px", "--hover-color": "#e2e8f0"},
        "nav-link-selected": {"background-color": "#4f46e5", "color": "white", "icon-color": "white"},
    }
)

# --- SESSION STATE ---
if 'sales_data' not in st.session_state:
    # Try to load sample data by default
    if os.path.exists("sample_data.csv"):
        st.session_state['sales_data'] = load_data("sample_data.csv")
    else:
        st.session_state['sales_data'] = None

# --- VIEW: HOME ---
if selected == "Home":
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center; font-size: 3.5rem;'>Welcome to InsightGrid</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 1.2rem; color: #64748b;'>Transform raw data into actionable insights instantly.</p>", unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div class="metric-card" style="text-align: center; padding: 2rem;">
            <h2 style="font-size: 3rem; margin-bottom: 1rem;">🚀</h2>
            <h3>Lightning Fast</h3>
            <p style="color: #64748b;">Powered by advanced caching, your data loads instantly.</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="metric-card" style="text-align: center; padding: 2rem;">
            <h2 style="font-size: 3rem; margin-bottom: 1rem;">💎</h2>
            <h3>Premium Design</h3>
            <p style="color: #64748b;">A beautiful, distraction-free environment for your analytics.</p>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="metric-card" style="text-align: center; padding: 2rem;">
            <h2 style="font-size: 3rem; margin-bottom: 1rem;">🧠</h2>
            <h3>Smart Insights</h3>
            <p style="color: #64748b;">Automated intelligence to find trends without the legwork.</p>
        </div>
        """, unsafe_allow_html=True)

# --- VIEW: DATA HUB ---
elif selected == "Data Hub":
    st.title("📁 Data Hub")
    st.markdown("Upload your CSV file here to power the dashboard. The system will automatically map common columns like Date, Product, Category, and Revenue.")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader("Drop your Sales CSV here", type=["csv"])
    
    if uploaded_file:
        df = load_data(uploaded_file)
        if df is not None:
            st.session_state['sales_data'] = df
            st.success("✅ Data loaded successfully! You can now view the Dashboard.")
            
    # Always show a preview of whatever is in session state
    if st.session_state['sales_data'] is not None:
        st.markdown("### Current Data Preview")
        st.dataframe(st.session_state['sales_data'].head(10), use_container_width=True)
        st.info(f"Loaded {len(st.session_state['sales_data'])} rows.")
    else:
        st.warning("No data loaded. Please upload a file.")

# --- VIEW: DASHBOARD ---
elif selected == "Dashboard":
    df_raw = st.session_state['sales_data']
    
    if df_raw is None:
        st.warning("No data found! Please head over to the **Data Hub** to upload your CSV.")
    else:
        # --- SIDEBAR (ONLY ON DASHBOARD) ---
        with st.sidebar:
            st.title("🛡️ Filters")
            st.markdown("---")
            
            # Date Filter
            min_date = df_raw['Date'].min().to_pydatetime()
            max_date = df_raw['Date'].max().to_pydatetime()
            
            date_range = st.date_input(
                "📅 Select Date Range",
                value=(min_date, max_date),
                min_value=min_date,
                max_value=max_date
            )
            
            # Category Filter
            categories = sorted(df_raw['Category'].unique().tolist())
            selected_categories = st.multiselect("🏷️ Select Categories", categories, default=categories)
            
            # Product Filter
            products = sorted(df_raw[df_raw['Category'].isin(selected_categories)]['Product'].unique().tolist())
            selected_products = st.multiselect("📦 Select Products", products, default=products)

        # Apply Filters
        mask = (
            (df_raw['Date'].dt.date >= date_range[0]) & 
            (df_raw['Date'].dt.date <= date_range[1]) &
            (df_raw['Category'].isin(selected_categories)) &
            (df_raw['Product'].isin(selected_products))
        )
        df = df_raw.loc[mask]

        st.title("Sales Analytics Overview")
        
        # 1. KPI SECTION
        col1, col2, col3, col4 = st.columns(4)
        
        total_revenue = df['Revenue'].sum()
        total_orders = len(df)
        aov = total_revenue / total_orders if total_orders > 0 else 0
        top_product = df.groupby('Product')['Revenue'].sum().idxmax() if not df.empty else "N/A"
        
        with col1:
            kpi_card("Total Revenue", f"{total_revenue:,.2f}", "₹", "💰")
        with col2:
            kpi_card("Total Orders", f"{total_orders:,}", "", "📦")
        with col3:
            kpi_card("Avg Order Value", f"{aov:,.2f}", "₹", "📈")
        with col4:
            kpi_card("Top Product", top_product, "", "🏆")

        st.markdown("---")

        # 2. CHARTS SECTION - ROW 1
        c1, c2 = st.columns(2)
        
        with c1:
            st.subheader("📈 Revenue Over Time")
            daily_revenue = df.groupby('Date')['Revenue'].sum().reset_index()
            fig_revenue = px.line(
                daily_revenue, x='Date', y='Revenue',
                template="plotly_white",
                color_discrete_sequence=['#4C6EF5']
            )
            fig_revenue.update_layout(
                margin=dict(l=0, r=0, t=20, b=0), 
                height=350,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                xaxis=dict(showgrid=False),
                yaxis=dict(showgrid=True, gridcolor='#e2e8f0')
            )
            st.plotly_chart(fig_revenue, use_container_width=True)

        with c2:
            st.subheader("🏷️ Sales by Category")
            cat_sales = df.groupby('Category')['Revenue'].sum().reset_index().sort_values('Revenue', ascending=False)
            fig_cat = px.bar(
                cat_sales, x='Category', y='Revenue',
                template="plotly_white",
                color='Category',
                color_discrete_sequence=px.colors.qualitative.Safe
            )
            fig_cat.update_layout(
                margin=dict(l=0, r=0, t=20, b=0), 
                height=350, 
                showlegend=False,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                xaxis=dict(showgrid=False),
                yaxis=dict(showgrid=True, gridcolor='#e2e8f0')
            )
            st.plotly_chart(fig_cat, use_container_width=True)

        # 3. CHARTS SECTION - ROW 2
        c3, c4 = st.columns([0.6, 0.4])
        
        with c3:
            st.subheader("🏆 Top 10 Products by Revenue")
            prod_sales = df.groupby('Product')['Revenue'].sum().reset_index().sort_values('Revenue', ascending=False).head(10)
            fig_prod = px.bar(
                prod_sales, y='Product', x='Revenue',
                orientation='h',
                template="plotly_white",
                color='Revenue',
                color_continuous_scale='Blues'
            )
            fig_prod.update_layout(
                margin=dict(l=0, r=0, t=20, b=0), 
                height=400,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                xaxis=dict(showgrid=True, gridcolor='#e2e8f0'),
                yaxis=dict(showgrid=False)
            )
            st.plotly_chart(fig_prod, use_container_width=True)

        with c4:
            st.subheader("🍕 Category Distribution")
            fig_pie = px.pie(
                cat_sales, values='Revenue', names='Category',
                template="plotly_white",
                hole=0.4,
                color_discrete_sequence=px.colors.qualitative.Safe
            )
            fig_pie.update_layout(
                margin=dict(l=0, r=0, t=20, b=0), 
                height=400,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig_pie, use_container_width=True)

        st.markdown("---")

        # 4. INSIGHTS SECTION
        st.subheader("💡 Automated Insights")
        
        if not df.empty:
            df['Month'] = df['Date'].dt.strftime('%B %Y')
            best_month = df.groupby('Month')['Revenue'].sum().idxmax()
            
            df['Day'] = df['Date'].dt.day_name()
            best_day = df.groupby('Day')['Revenue'].sum().idxmax()
            
            top_cat = cat_sales.iloc[0]['Category']
            
            insight_col1, insight_col2 = st.columns(2)
            with insight_col1:
                st.markdown(f"""
                - **Highest Revenue Month:** The peak performance was recorded in **{best_month}**.
                - **Top Performing Category:** **{top_cat}** accounts for the largest share of your sales.
                """)
            with insight_col2:
                st.markdown(f"""
                - **Peak Sales Day:** Most transactions and revenue tend to occur on **{best_day}s**.
                - **Product Catalog:** You are currently tracking **{df['Product'].nunique()}** unique products across **{df['Category'].nunique()}** categories.
                """)
        else:
            st.write("No data available for the selected filters.")

        st.markdown("---")

        # 5. DATA TABLE
        with st.expander("📄 View Filtered Data Table"):
            st.dataframe(df.sort_values('Date', ascending=False), use_container_width=True)
            
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download Filtered Data as CSV",
                data=csv,
                file_name=f"insightgrid_filtered_data_{datetime.now().strftime('%Y%m%d')}.csv",
                mime='text/csv',
            )

# --- FOOTER ---
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #718096; font-size: 0.8rem;'>"
    "InsightGrid Sales Analytics Dashboard | Built with Python, Streamlit & Plotly"
    "</div>", 
    unsafe_allow_html=True
)
