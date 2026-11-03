import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from simulation import run_monte_carlo

st.set_page_config(page_title="Retirement Wealth Simulator", layout="wide")

st.title("📊 Wealth Decumulation & Monte Carlo Retirement Planner")
st.markdown("Designed for Private Wealth & Asset Management Advisory Portfolio Analysis.")

# Sidebar user inputs
st.sidebar.header("Client Parameters")
current_age = st.sidebar.slider("Current Age", 20, 60, 22)
retirement_age = st.sidebar.slider("Retirement Age", 50, 75, 65)
death_age = st.sidebar.slider("Planning Horizon (Age)", 80, 100, 90)

initial_portfolio = st.sidebar.number_input("Current Portfolio Value ($)", value=25000, step=5000)
annual_contribution = st.sidebar.number_input("Annual Savings/Contribution ($)", value=10000, step=1000)
annual_spending = st.sidebar.number_input("Annual Retirement Spending ($)", value=60000, step=5000)

st.sidebar.header("Capital Market Assumptions")
expected_return = st.sidebar.slider("Expected Market Return (%)", 3.0, 12.0, 7.5) / 100
volatility = st.sidebar.slider("Portfolio Volatility (Std Dev %)", 5.0, 25.0, 15.0) / 100
inflation_rate = st.sidebar.slider("Expected Inflation Rate (%)", 1.0, 6.0, 2.5) / 100

# Run Simulation Button
if st.sidebar.button("Run Monte Carlo Simulation"):
    with st.spinner("Running 5,000 market pathways..."):
        df_results = run_monte_carlo(
            current_age, retirement_age, death_age,
            initial_portfolio, annual_contribution, annual_spending,
            expected_return, volatility, inflation_rate, num_simulations=5000
        )
        
        # Calculate success rate (ending wealth > 0 at death_age)
        ending_wealth = df_results.iloc[-1, :]
        success_rate = (ending_wealth > 0).mean() * 100
        
        # Metrics Display
        col1, col2, col3 = st.columns(3)
        col1.metric("Portfolio Success Rate", f"{success_rate:.1f}%")
        col2.metric("Median Ending Wealth", f"${np.median(ending_wealth):,.0f}")
        col3.metric("10th Percentile (Worst-Case)", f"${np.percentile(ending_wealth, 10):,.0f}")
        
        # Plotting with Plotly
        fig = go.Figure()
        
        # Plot percentiles
        ages = df_results.index
        p90 = np.percentile(df_results, 90, axis=1)
        p50 = np.percentile(df_results, 50, axis=1)
        p10 = np.percentile(df_results, 10, axis=1)
        
        fig.add_trace(go.Scatter(x=ages, y=p90, mode='lines', name='90th Percentile (Optimistic)', line=dict(color='green')))
        fig.add_trace(go.Scatter(x=ages, y=p50, mode='lines', name='Median Outcome (50th)', line=dict(color='blue', width=3)))
        fig.add_trace(go.Scatter(x=ages, y=p10, mode='lines', name='10th Percentile (Conservative)', line=dict(color='red')))
        
        fig.update_layout(
            title="Monte Carlo Wealth Trajectory (5,000 Simulations)",
            xaxis_title="Age",
            yaxis_title="Portfolio Value ($)",
            hovermode="x"
        )
        
        st.plotly_chart(fig, use_container_width=True)
else:
    st.info("Adjust your client parameters in the sidebar and click **Run Monte Carlo Simulation** to generate the model.")
