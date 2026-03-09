import numpy as np
import pickle
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import streamlit.components.v1 as components

# ===============================
# PAGE CONFIG
# ===============================
st.set_page_config(
    page_title="CarValue - AI Price Prediction",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ===============================
# ENHANCED GLOBAL CSS + BOOTSTRAP + ANIMATIONS
# ===============================
st.markdown("""
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
<link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap" rel="stylesheet">

<style>
/* ========== GLOBAL STYLES ========== */
* {
    font-family: 'Poppins', sans-serif;
}

/* Body Background - Subtle Gradient */
.stApp {
    background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
}

/* Main Content Animation */
@keyframes fadeInUp {
    from { 
        opacity: 0; 
        transform: translateY(30px); 
    }
    to { 
        opacity: 1; 
        transform: translateY(0); 
    }
}

.main, [data-testid="stMainBlockContainer"] {
    animation: fadeInUp 0.8s ease-out;
}

/* ========== SIDEBAR STYLES ========== */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
    padding: 20px 10px;
    box-shadow: 4px 0 20px rgba(0,0,0,0.3);
}

[data-testid="stSidebar"] * {
    color: #ecf0f1 !important;
}

/* Sidebar Logo */
.sidebar-logo {
    text-align: center;
    padding: 20px 0;
    animation: pulse 2s ease-in-out infinite;
}

.sidebar-logo h1 {
    font-size: 32px;
    font-weight: 700;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 0;
}

@keyframes pulse {
    0%, 100% { transform: scale(1); }
    50% { transform: scale(1.05); }
}

/* Sidebar Buttons */
.stButton > button {
    width: 100%;
    background: rgba(255,255,255,0.1) !important;
    color: white !important;
    border: 2px solid rgba(255,255,255,0.2) !important;
    border-radius: 12px !important;
    padding: 14px 20px !important;
    font-weight: 600 !important;
    font-size: 16px !important;
    margin: 8px 0 !important;
    transition: all 0.3s ease !important;
    text-align: left !important;
}

.stButton > button:hover {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
    transform: translateX(8px) !important;
    box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4) !important;
    border-color: transparent !important;
}

/* ========== HERO SECTION ========== */
.hero-section {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 50px 40px;
    border-radius: 20px;
    color: white;
    margin-bottom: 30px;
    box-shadow: 0 20px 60px rgba(102, 126, 234, 0.4);
    position: relative;
    overflow: hidden;
    animation: fadeInUp 1s ease-out;
}

.hero-section::before {
    content: '';
    position: absolute;
    top: -50%;
    right: -50%;
    width: 200%;
    height: 200%;
    background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
    animation: rotate 20s linear infinite;
}

@keyframes rotate {
    from { transform: rotate(0deg); }
    to { transform: rotate(360deg); }
}

.hero-section h1 {
    font-size: 48px;
    font-weight: 700;
    margin-bottom: 15px;
    position: relative;
    z-index: 1;
}

.hero-section p {
    font-size: 20px;
    font-weight: 300;
    margin: 0;
    position: relative;
    z-index: 1;
}

/* ========== CARD STYLES ========== */
.custom-card {
    background: white;
    padding: 30px;
    border-radius: 20px;
    box-shadow: 0 10px 40px rgba(0,0,0,0.1);
    transition: all 0.4s ease;
    animation: fadeInUp 0.8s ease-out;
    border: 1px solid rgba(0,0,0,0.05);
}

.custom-card:hover {
    transform: translateY(-10px);
    box-shadow: 0 20px 60px rgba(0,0,0,0.15);
}

.card-header-custom {
    font-size: 24px;
    font-weight: 700;
    color: #2c3e50;
    margin-bottom: 25px;
    padding-bottom: 15px;
    border-bottom: 3px solid #667eea;
}

/* ========== FORM INPUTS - TEXT INPUTS ========== */
.stNumberInput, .stTextInput, .stSelectbox {
    animation: fadeInUp 0.6s ease-out;
}

/* Style for number input boxes */
.stNumberInput > div > div > input,
.stTextInput > div > div > input {
    background: #f8f9fa !important;
    border: 2px solid #e0e0e0 !important;
    border-radius: 12px !important;
    padding: 12px 16px !important;
    font-size: 16px !important;
    font-weight: 500 !important;
    color: #2c3e50 !important;
    transition: all 0.3s ease !important;
}

.stNumberInput > div > div > input:focus,
.stTextInput > div > div > input:focus {
    border-color: #667eea !important;
    box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1) !important;
    background: white !important;
}

.stNumberInput > div > div > input:hover,
.stTextInput > div > div > input:hover {
    border-color: #667eea !important;
    background: white !important;
}

/* Selectbox styling */
.stSelectbox > div > div > div {
    background: #f8f9fa !important;
    border: 2px solid #e0e0e0 !important;
    border-radius: 12px !important;
    padding: 8px 12px !important;
    transition: all 0.3s ease !important;
}

.stSelectbox > div > div > div:hover {
    border-color: #667eea !important;
    background: white !important;
}

label {
    font-weight: 600 !important;
    color: #2c3e50 !important;
    font-size: 15px !important;
    margin-bottom: 8px !important;
}

/* ========== PREDICT BUTTON ========== */
.predict-btn button {
    background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 15px !important;
    padding: 18px 40px !important;
    font-weight: 700 !important;
    font-size: 18px !important;
    width: 100% !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 10px 30px rgba(245, 87, 108, 0.4) !important;
}

.predict-btn button:hover {
    transform: scale(1.05) !important;
    box-shadow: 0 15px 40px rgba(245, 87, 108, 0.6) !important;
}

/* ========== PRICE DISPLAY BOX ========== */
.price-result {
    background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
    color: white;
    padding: 40px;
    border-radius: 20px;
    text-align: center;
    margin-top: 25px;
    animation: zoomIn 0.6s ease-out;
    box-shadow: 0 15px 50px rgba(17, 153, 142, 0.4);
}

@keyframes zoomIn {
    from { 
        opacity: 0; 
        transform: scale(0.8); 
    }
    to { 
        opacity: 1; 
        transform: scale(1); 
    }
}

.price-result h2 {
    font-size: 22px;
    font-weight: 300;
    margin-bottom: 15px;
}

.price-result h1 {
    font-size: 48px;
    font-weight: 700;
    margin: 0;
}

/* ========== IMAGE STYLES ========== */
.image-container {
    border-radius: 20px;
    overflow: hidden;
    box-shadow: 0 10px 40px rgba(0,0,0,0.15);
    transition: transform 0.4s ease;
}

.image-container:hover {
    transform: scale(1.03);
}

.image-container img {
    border-radius: 20px;
}

/* ========== KPI CARDS ========== */
.kpi-card {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 30px 20px;
    border-radius: 20px;
    text-align: center;
    color: white;
    animation: float 3s ease-in-out infinite;
    box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
    transition: all 0.3s ease;
}

.kpi-card:hover {
    transform: translateY(-8px);
    box-shadow: 0 15px 40px rgba(102, 126, 234, 0.5);
}

@keyframes float {
    0%, 100% { transform: translateY(0px); }
    50% { transform: translateY(-10px); }
}

.kpi-card h3 {
    font-size: 16px;
    font-weight: 400;
    margin-bottom: 10px;
    opacity: 0.9;
}

.kpi-card h1 {
    font-size: 36px;
    font-weight: 700;
    margin: 0;
}

/* ========== ANALYTICS PAGE ========== */
.analytics-header {
    background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
    padding: 40px;
    border-radius: 20px;
    color: white;
    margin-bottom: 30px;
    box-shadow: 0 15px 50px rgba(250, 112, 154, 0.3);
}

.analytics-header h1 {
    font-size: 42px;
    font-weight: 700;
    margin: 0;
}

/* ========== DATA TABLE ========== */
.dataframe-container {
    animation: fadeInUp 0.8s ease-out;
}

.table {
    border-radius: 15px;
    overflow: hidden;
    box-shadow: 0 10px 30px rgba(0,0,0,0.1);
}

.table thead {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
}

.table-hover tbody tr:hover {
    background-color: rgba(102, 126, 234, 0.1);
    transform: scale(1.01);
    transition: all 0.2s ease;
}

/* ========== ABOUT PAGE ========== */
.about-section {
    background: white;
    padding: 50px;
    border-radius: 20px;
    box-shadow: 0 15px 50px rgba(0,0,0,0.1);
    animation: fadeInUp 0.8s ease-out;
}

.about-section h1 {
    color: #667eea;
    font-size: 42px;
    font-weight: 700;
    margin-bottom: 30px;
}

.feature-card {
    background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    padding: 30px;
    border-radius: 15px;
    margin-bottom: 20px;
    transition: all 0.3s ease;
    border-left: 5px solid #667eea;
}

.feature-card:hover {
    transform: translateX(10px);
    box-shadow: 0 10px 30px rgba(0,0,0,0.1);
}

.feature-card i {
    font-size: 36px;
    color: #667eea;
    margin-bottom: 15px;
}

.feature-card h3 {
    color: #2c3e50;
    font-weight: 700;
    margin-bottom: 10px;
}

/* ========== LOADING ANIMATION ========== */
@keyframes spin {
    from { transform: rotate(0deg); }
    to { transform: rotate(360deg); }
}

.loading {
    display: inline-block;
    animation: spin 1s linear infinite;
}

/* ========== RESPONSIVE ========== */
@media (max-width: 768px) {
    .hero-section h1 { font-size: 32px; }
    .hero-section p { font-size: 16px; }
    .price-result h1 { font-size: 36px; }
}

/* ========== INFO BOXES ========== */
.info-box {
    background: linear-gradient(135deg, #30cfd0 0%, #330867 100%);
    color: white;
    padding: 25px;
    border-radius: 15px;
    margin: 20px 0;
    box-shadow: 0 10px 30px rgba(48, 207, 208, 0.3);
}

.info-box i {
    font-size: 28px;
    margin-bottom: 10px;
}

/* ========== INPUT FIELD ICONS ========== */
.input-wrapper {
    position: relative;
    margin-bottom: 20px;
}

.input-icon {
    position: absolute;
    left: 12px;
    top: 50%;
    transform: translateY(-50%);
    color: #667eea;
    font-size: 18px;
    pointer-events: none;
}

</style>
""", unsafe_allow_html=True)

# ===============================
# LOAD MODEL
# ===============================
@st.cache_resource
def load_model():
    try:
        with open("Cars.pkl", "rb") as f:
            return pickle.load(f)
    except:
        # Mock model for demonstration if file doesn't exist
        return None

model = load_model()

# ===============================
# SESSION STATE INITIALIZATION
# ===============================
if "page" not in st.session_state:
    st.session_state.page = "Home"

if "history" not in st.session_state:
    st.session_state.history = []

# ===============================
# SIDEBAR NAVIGATION
# ===============================
with st.sidebar:
    st.markdown("""
        <div class="sidebar-logo">
            <h1><i class="fas fa-car"></i> CarValue</h1>
            <p style="font-size: 12px; color: #bdc3c7;">AI-Powered Price Prediction</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    if st.button("🏠 Home", key="home_btn"):
        st.session_state.page = "Home"
    
    if st.button("📊 Analytics Dashboard", key="analytics_btn"):
        st.session_state.page = "Analytics"
    
    if st.button("ℹ️ About CarValue", key="about_btn"):
        st.session_state.page = "About"
    
    st.markdown("---")
    
    # Sidebar Stats
    if len(st.session_state.history) > 0:
        st.markdown("""
            <div style="background: rgba(255,255,255,0.1); padding: 20px; border-radius: 15px; margin-top: 20px;">
                <h4 style="color: white; margin-bottom: 15px;"><i class="fas fa-chart-line"></i> Quick Stats</h4>
        """, unsafe_allow_html=True)
        st.metric("Total Predictions", len(st.session_state.history))
        st.metric("Avg Price", f"₹{int(pd.DataFrame(st.session_state.history)['Price'].mean()):,}")
        st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("""
        <div style="text-align: center; padding: 15px; font-size: 11px; color: #95a5a6;">
            <p>© 2026 CarValue<br>Powered by AI & ML</p>
        </div>
    """, unsafe_allow_html=True)

# =========================================================
# HOME PAGE - PRICE PREDICTION
# =========================================================
if st.session_state.page == "Home" or st.session_state.page == "🏠 Home":
    
    # Hero Section
    st.markdown("""
        <div class="hero-section">
            <h1><i class="fas fa-car-side"></i> Car Price Prediction</h1>
            <p>Get instant AI-powered resale value estimates with advanced machine learning algorithms</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Main Content Layout
    col1, col2 = st.columns([2.5, 1.5], gap="large")
    
    with col1:
        st.markdown('<div class="">', unsafe_allow_html=True)
        st.markdown('<h2 class="card-header-custom"><i class="fas fa-edit"></i> Vehicle Details</h2>', unsafe_allow_html=True)
        
        # Input Fields - Row 1
        row1_col1, row1_col2 = st.columns(2)
        with row1_col1:
            vehicle_age = st.number_input(
                "🕐 Vehicle Age (Years)", 
                min_value=0.0, 
                max_value=20.0, 
                value=5.0, 
                step=0.5,
                format="%.1f"
            )
        with row1_col2:
            km_driven = st.number_input(
                "🛣️ Kilometers Driven", 
                min_value=0, 
                max_value=300000, 
                value=60000, 
                step=5000
            )
        
        # Input Fields - Row 2
        row2_col1, row2_col2 = st.columns(2)
        with row2_col1:
            mileage = st.number_input(
                "⛽ Mileage (km/l)", 
                min_value=5.0, 
                max_value=40.0, 
                value=18.0, 
                step=0.5,
                format="%.1f"
            )
        with row2_col2:
            engine = st.number_input(
                "⚙️ Engine CC", 
                min_value=500, 
                max_value=5000, 
                value=1200, 
                step=100
            )
        
        # Input Fields - Row 3
        row3_col1, row3_col2 = st.columns(2)
        with row3_col1:
            max_power = st.number_input(
                "💪 Max Power (bhp)", 
                min_value=20.0, 
                max_value=500.0, 
                value=90.0, 
                step=5.0,
                format="%.1f"
            )
        with row3_col2:
            seats = st.number_input(
                "🪑 Seats", 
                min_value=2, 
                max_value=10, 
                value=5, 
                step=1
            )
        
        st.markdown("---")
        
        # Dropdowns - Row 4
        row4_col1, row4_col2, row4_col3 = st.columns(3)
        with row4_col1:
            fuel_type = st.selectbox(
                "⛽ Fuel Type", 
                ["Petrol", "Diesel", "CNG", "LPG", "Electric"]
            )
        with row4_col2:
            seller_type = st.selectbox(
                "👤 Seller Type", 
                ["Dealer", "Individual"]
            )
        with row4_col3:
            transmission_type = st.selectbox(
                "⚡ Transmission", 
                ["Manual", "Automatic"]
            )
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        # Image Card
        st.markdown('<div class=>', unsafe_allow_html=True)
        st.image(
            "https://i.pinimg.com/originals/6e/28/7d/6e287d49682bca3e0cc97b04bc124c8d.jpg",
            use_container_width=True
        )
        st.caption("🎯 Smart AI-based valuation")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Info Box
        st.markdown("""
            <div class="info-box">
                <i class="fas fa-info-circle"></i>
                <h4>How It Works</h4>
                <p style="font-size: 14px; margin: 0;">
                    Our AI model analyzes 15+ parameters to provide accurate price predictions based on real market data.
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        # Predict Button
        st.markdown('<div class="predict-btn">', unsafe_allow_html=True)
        if st.button("🚀 Predict Price Now", use_container_width=True):
            
            if model is None:
                st.error("⚠️ Model file not found. Please ensure 'Cars.pkl' is in the directory.")
            else:
                with st.spinner("🔄 Analyzing vehicle data..."):
                    # Prepare input
                    X = np.array([[
                        vehicle_age, km_driven, mileage, engine, max_power, seats,
                        int(seller_type == "Dealer"),
                        int(seller_type == "Individual"),
                        int(fuel_type == "CNG"),
                        int(fuel_type == "Diesel"),
                        int(fuel_type == "Electric"),
                        int(fuel_type == "LPG"),
                        int(fuel_type == "Petrol"),
                        int(transmission_type == "Automatic"),
                        int(transmission_type == "Manual")
                    ]])
                    
                    # Predict
                    price = max(50000, model.predict(X)[0])
                    
                    # Save to history
                    st.session_state.history.append({
                        "Date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                        "Price": price,
                        "Fuel": fuel_type,
                        "Transmission": transmission_type,
                        "KM": km_driven,
                        "Age": vehicle_age,
                        "Mileage": mileage
                    })
                    
                    # Display Result
                    st.markdown(f"""
                        <div class="price-result">
                            <h2><i class="fas fa-check-circle"></i> Estimated Market Value</h2>
                            <h1>₹ {price:,.0f}</h1>
                            <p style="font-size: 14px; margin-top: 15px; opacity: 0.9;">
                                Based on current market trends and vehicle specifications
                            </p>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    st.balloons()
        
        st.markdown('</div>', unsafe_allow_html=True)

# =========================================================
# ANALYTICS PAGE
# =========================================================
elif st.session_state.page == "Analytics" or st.session_state.page == "📊 Analytics Dashboard":
    
    # Header
    st.markdown("""
        <div class="analytics-header">
            <h1><i class="fas fa-chart-bar"></i> Analytics Dashboard</h1>
            <p style="font-size: 18px; margin: 0;">Comprehensive insights from your price predictions</p>
        </div>
    """, unsafe_allow_html=True)
    
    if len(st.session_state.history) == 0:
        st.markdown("""
            <div class="custom-card" style="text-align: center; padding: 60px;">
                <i class="fas fa-chart-line" style="font-size: 72px; color: #667eea; margin-bottom: 20px;"></i>
                <h2>No Predictions Yet</h2>
                <p style="color: #7f8c8d;">Start predicting car prices to see analytics and insights here!</p>
            </div>
        """, unsafe_allow_html=True)
    else:
        df = pd.DataFrame(st.session_state.history)
        
        # KPI Cards
        st.markdown("### 📈 Key Metrics")
        c1, c2, c3, c4 = st.columns(4)
        
        with c1:
            st.markdown(f"""
                <div class="kpi-card">
                    <h3><i class="fas fa-calculator"></i> Total Predictions</h3>
                    <h1>{len(df)}</h1>
                </div>
            """, unsafe_allow_html=True)
        
        with c2:
            st.markdown(f"""
                <div class="kpi-card" style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);">
                    <h3><i class="fas fa-chart-line"></i> Average Price</h3>
                    <h1>₹{int(df.Price.mean()):,}</h1>
                </div>
            """, unsafe_allow_html=True)
        
        with c3:
            st.markdown(f"""
                <div class="kpi-card" style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);">
                    <h3><i class="fas fa-arrow-up"></i> Maximum Price</h3>
                    <h1>₹{int(df.Price.max()):,}</h1>
                </div>
            """, unsafe_allow_html=True)
        
        with c4:
            st.markdown(f"""
                <div class="kpi-card" style="background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);">
                    <h3><i class="fas fa-arrow-down"></i> Minimum Price</h3>
                    <h1>₹{int(df.Price.min()):,}</h1>
                </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Charts Section
        st.markdown("### 📊 Visual Analytics")
        
        chart_col1, chart_col2 = st.columns(2, gap="large")
        
        with chart_col1:
            # Scatter: Price vs KM
            fig1 = px.scatter(
                df, x="KM", y="Price",
                color="Fuel",
                size="Age",
                title="🚗 Price vs Kilometers Driven",
                template="plotly_white",
                color_discrete_sequence=px.colors.qualitative.Vivid,
                hover_data={"Age": True, "KM": ":,", "Price": ":,.0f"}
            )
            fig1.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(family="Poppins", size=12),
                title_font_size=18,
                xaxis_title="Kilometers Driven",
                yaxis_title="Price (₹)"
            )
            fig1.update_xaxes(tickformat=",")
            fig1.update_yaxes(tickprefix="₹", tickformat=",")
            st.plotly_chart(fig1, use_container_width=True)
        
        with chart_col2:
            # Scatter: Price vs Age
            fig2 = px.scatter(
                df, x="Age", y="Price",
                color="Fuel",
                size="KM",
                title="📉 Price vs Vehicle Age",
                template="plotly_white",
                color_discrete_sequence=px.colors.qualitative.Bold,
                hover_data={"Age": ":.1f", "KM": ":,", "Price": ":,.0f"}
            )
            fig2.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(family="Poppins", size=12),
                title_font_size=18,
                xaxis_title="Vehicle Age (Years)",
                yaxis_title="Price (₹)"
            )
            fig2.update_yaxes(tickprefix="₹", tickformat=",")
            st.plotly_chart(fig2, use_container_width=True)
        
        # Box Plot - Full Width
        fig3 = px.box(
            df,
            x="Fuel",
            y="Price",
            color="Fuel",
            points="all",   # shows all data points
            title="💰 Price Distribution by Fuel Type",
            template="plotly_white",
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        
        fig3.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Poppins", size=13),
            title_font_size=20,
            yaxis_title="Car Price (₹)",
            xaxis_title="Fuel Type",
            showlegend=False,
            height=500
        )
        
        fig3.update_yaxes(tickprefix="₹", tickformat=",")
        st.plotly_chart(fig3, use_container_width=True)
        
        # Additional Charts Row
        chart_col3, chart_col4 = st.columns(2, gap="large")
        
        with chart_col3:
            # Price Trend Over Time
            fig4 = px.line(
                df, x="Date", y="Price",
                title="📈 Price Prediction Trend Over Time",
                markers=True,
                template="plotly_white"
            )
            fig4.update_traces(
                line_color='#667eea',
                line_width=3,
                marker=dict(size=10, color='#f5576c')
            )
            fig4.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(family="Poppins", size=12),
                title_font_size=18,
                xaxis_title="Date & Time",
                yaxis_title="Price (₹)",
                height=400
            )
            fig4.update_yaxes(tickprefix="₹", tickformat=",")
            st.plotly_chart(fig4, use_container_width=True)
        
        with chart_col4:
            # Pie Chart: Fuel Type Distribution
            fuel_counts = df['Fuel'].value_counts()
            fig5 = px.pie(
                values=fuel_counts.values,
                names=fuel_counts.index,
                title="⛽ Fuel Type Distribution",
                template="plotly_white",
                color_discrete_sequence=px.colors.qualitative.Pastel,
                hole=0.4  # Makes it a donut chart
            )
            fig5.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(family="Poppins", size=12),
                title_font_size=18,
                height=400
            )
            fig5.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig5, use_container_width=True)
        
        # Bar Chart: Average Price by Transmission Type
        if 'Transmission' in df.columns:
            avg_price_transmission = df.groupby('Transmission')['Price'].mean().reset_index()
            fig6 = px.bar(
                avg_price_transmission,
                x='Transmission',
                y='Price',
                title="⚡ Average Price by Transmission Type",
                template="plotly_white",
                color='Transmission',
                color_discrete_sequence=['#667eea', '#f5576c']
            )
            fig6.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(family="Poppins", size=12),
                title_font_size=18,
                xaxis_title="Transmission Type",
                yaxis_title="Average Price (₹)",
                showlegend=False,
                height=400
            )
            fig6.update_yaxes(tickprefix="₹", tickformat=",")
            st.plotly_chart(fig6, use_container_width=True)
        
        # Data Table
        st.markdown("### 📋 Detailed Prediction History")
        st.markdown('<div class="dataframe-container">', unsafe_allow_html=True)
        
        # Format dataframe
        df_display = df.copy()
        df_display['Price'] = df_display['Price'].apply(lambda x: f"₹{int(x):,}")
        df_display['KM'] = df_display['KM'].apply(lambda x: f"{int(x):,} km")
        df_display['Age'] = df_display['Age'].apply(lambda x: f"{x} yrs")
        df_display['Mileage'] = df_display['Mileage'].apply(lambda x: f"{x} km/l")
        
        st.markdown(df_display.to_html(
            classes="table table-hover table-bordered",
            index=False,
            escape=False
        ), unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Download Button
        csv = df.to_csv(index=False)
        st.download_button(
            label="📥 Download Data as CSV",
            data=csv,
            file_name=f"carvalue_predictions_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )


# =========================================================
# ABOUT PAGE
# =========================================================
elif st.session_state.page in ["About", "ℹ️ About CarValue"]:

    components.html(
        """
        <!DOCTYPE html>
        <html>
        <head>
            <!-- Font Awesome -->
            <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">

            <!-- Bootstrap -->
            <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css">

            <style>
                body {
                    font-family: 'Segoe UI', sans-serif;
                    background: #f9f9f9;
                    padding: 20px;
                }
                .about-section {
                    background: white;
                    padding: 40px;
                    border-radius: 20px;
                }
                .feature-card {
                    background: #f4f6fb;
                    padding: 25px;
                    border-radius: 15px;
                    text-align: center;
                    margin-bottom: 25px;
                }
                .feature-card i {
                    font-size: 40px;
                    color: #667eea;
                    margin-bottom: 15px;
                }
            </style>
        </head>

        <body>
            <div class="about-section">
                <h1 class="text-center mb-3">
                    <i class="fas fa-info-circle"></i> About CarValue
                </h1>
                <p class="text-center text-muted mb-5">
                    Your trusted AI-powered car price prediction platform
                </p>

                <div class="row">
                    <div class="col-md-6">
                        <div class="feature-card">
                            <i class="fas fa-brain"></i>
                            <h4>Advanced AI Technology</h4>
                            <p>Machine learning models trained on real car market data.</p>
                        </div>
                    </div>

                    <div class="col-md-6">
                        <div class="feature-card">
                            <i class="fas fa-chart-line"></i>
                            <h4>Real-Time Analytics</h4>
                            <p>Interactive dashboards with deep insights.</p>
                        </div>
                    </div>

                    <div class="col-md-6">
                        <div class="feature-card">
                            <i class="fas fa-shield-alt"></i>
                            <h4>Accurate Predictions</h4>
                            <p>Considers 15+ parameters for precision.</p>
                        </div>
                    </div>

                    <div class="col-md-6">
                        <div class="feature-card">
                            <i class="fas fa-mobile-alt"></i>
                            <h4>Responsive Design</h4>
                            <p>Works perfectly on desktop & mobile.</p>
                        </div>
                    </div>
                </div>

                <hr>

                <div class="text-center">
                    <h3 class="mb-3">👨‍💻 Developer</h3>
                    <h4>Kiran More</h4>
                    <p>Data Scientist & ML Enthusiast</p>
                </div>

                <hr>

                <p class="text-center text-muted">
                    Version 2.5 Enhanced | February 2026
                </p>
            </div>
        </body>
        </html>
        """,
        height=1100,
        scrolling=True
    )

# =========================================================
# FALLBACK (if page state is undefined)
# =========================================================
else:
    st.session_state.page = "Home"
    st.rerun()

# ===============================
# FOOTER
# ===============================
st.markdown("""
    <div style="text-align: center; padding: 20px; margin-top: 50px; color: #7f8c8d; font-size: 12px;">
        <p>Made with ❤️ using Streamlit | Powered by Advanced Machine Learning</p>
    </div>
""", unsafe_allow_html=True)