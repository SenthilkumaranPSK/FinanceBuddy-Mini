import streamlit as st
import finance_lib as glib
import demo_data
import json
import pandas as pd

# --- Page Configuration ---
st.set_page_config(
    page_title="FinanceBuddy Mini",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom CSS ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    
    .stApp {
        background-color: #0e1117;
        font-family: 'Inter', sans-serif;
    }
    
    h1, h2, h3 {
        color: #ffffff;
    }
    
    .metric-card {
        background-color: #1e2329;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #2d333b;
        text-align: center;
    }
    
    .stButton button {
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)

# --- Sidebar ---
with st.sidebar:
    st.title("💰 FinanceBuddy")
    st.markdown("### Upload Expenses")
    
    uploaded_file = st.file_uploader("Upload CSV", type=["csv"])
    
    st.markdown("---")
    st.markdown("### Or Try Demo Data")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Normal"):
            st.session_state['csv_content'] = demo_data.NORMAL_CSV
            st.session_state['data_source'] = "Demo: Normal"
            
    with col2:
        if st.button("Fraud"):
            st.session_state['csv_content'] = demo_data.FRAUD_CSV
            st.session_state['data_source'] = "Demo: Fraud Patterns"
            
    if uploaded_file:
        st.session_state['csv_content'] = uploaded_file.read().decode("utf-8")
        st.session_state['data_source'] = f"File: {uploaded_file.name}"

# --- Main Content ---
st.title("FinanceBuddy Mini")
st.markdown("#### 🤖 Explainable Budget & Fraud-Alert Agent System")

if 'csv_content' in st.session_state:
    st.info(f"Loaded Data: **{st.session_state['data_source']}**")
    
    if st.button("🔍 Analyze Finances", type="primary"):
        progress_bar = st.progress(0, text="Starting analysis...")
        
        try:
            # 1. File Parser
            progress_bar.progress(20, text="Parsing file structure...")
            parsed_data = glib.parse_file(st.session_state['csv_content'])
            transactions = parsed_data.get('normalized_data', [])
            
            # 2. Categorizer
            progress_bar.progress(40, text="Categorizing transactions...")
            categorized = glib.categorize_transactions(transactions)
            
            # 3. Anomaly Detection
            progress_bar.progress(60, text="Scanning for anomalies...")
            anomalies = glib.detect_anomalies(transactions)
            
            # 4. Forecasting
            progress_bar.progress(80, text="Generating forecast & plan...")
            forecast = glib.forecast_and_plan(transactions)
            
            progress_bar.progress(100, text="Analysis complete!")
            progress_bar.empty()
            
            # --- Dashboard ---
            st.markdown("---")
            
            # Summary Metrics
            total_income = sum(t['amount'] for t in transactions if t['amount'] > 0)
            total_expenses = sum(abs(t['amount']) for t in transactions if t['amount'] < 0)
            balance = total_income - total_expenses
            
            m1, m2, m3 = st.columns(3)
            m1.metric("Total Income", f"₹{total_income:,.2f}")
            m2.metric("Total Expenses", f"₹{total_expenses:,.2f}")
            m3.metric("Net Balance", f"₹{balance:,.2f}", delta_color="normal")
            
            # Category Breakdown
            st.subheader("📊 Category Report")
            df_cat = pd.DataFrame(categorized)
            # Filter expenses only for chart
            df_expenses = df_cat[df_cat['amount'] < 0].copy()
            df_expenses['amount'] = df_expenses['amount'].abs()
            
            if not df_expenses.empty:
                cat_chart = df_expenses.groupby('category')['amount'].sum().sort_values(ascending=False)
                st.bar_chart(cat_chart)
            else:
                st.write("No expenses to chart.")
                
            # Anomalies
            st.subheader("🚨 Alerts and Red Flags")
            if anomalies.get('anomalies_detected', 0) > 0:
                for item in anomalies.get('items', []):
                    st.error(f"**{item['description']}**: {item.get('reason', 'Suspicious activity')}")
            else:
                st.success("No anomalies detected. Your spending looks normal.")
                
            # Forecast & Plan
            st.subheader("🧠 Personalized Monthly Plan")
            col_plan, col_forecast = st.columns(2)
            
            with col_plan:
                st.markdown("#### 💡 Suggested Plan")
                for tip in forecast.get('suggested_plan', []):
                    st.write(f"- {tip}")
                st.info(f"**Savings Target:** ₹{forecast.get('savings_target', 0):,.2f}")
                
            with col_forecast:
                st.markdown("#### 📈 Forecast")
                st.write(f"**Predicted Spending:** ₹{forecast.get('predicted_spending', 0):,.2f}")
                st.write(forecast.get('explanation', ''))
            
            # Debug View
            with st.expander("🔍 Raw Data (Debug)"):
                st.json({
                    "parsed": parsed_data,
                    "categorized": categorized,
                    "anomalies": anomalies,
                    "forecast": forecast
                })
                
        except Exception as e:
            st.error(f"An error occurred: {e}")
else:
    st.info("👈 Upload a CSV or select a Demo Dataset to begin.")

st.markdown("---")
st.markdown("© 2025 FinanceBuddy. All rights reserved.")
