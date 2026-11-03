import numpy as np
import pandas as pd

def run_monte_carlo(
    current_age,
    retirement_age,
    death_age,
    initial_portfolio,
    annual_contribution,
    annual_spending,
    expected_return,
    volatility,
    inflation_rate,
    num_simulations=5000
):
    working_years = retirement_age - current_age
    retirement_years = death_age - retirement_age
    total_years = working_years + retirement_years
# Initialize arrays to store results
    portfolio_paths = np.zeros((total_years + 1, num_simulations))
    portfolio_paths[0, :] = initial_portfolio
    
    # Adjust expected return and volatility for inflation (Fisher Effect approximation)
    real_return = (1 + expected_return) / (1 + inflation_rate) - 1  
for year in range(1, total_years + 1):
        # Generate random normal shocks for each simulation path
        random_shocks = np.random.normal(0, 1, num_simulations)
        
        # Calculate asset growth using log-normal return model
        annual_returns = np.exp((real_return - 0.5 * (volatility ** 2)) + volatility * random_shocks)
  previous_wealth = portfolio_paths[year - 1, :]
        
        if year <= working_years:
            # Accumulation phase: grow previous wealth + add contribution
            new_wealth = (previous_wealth * annual_returns) + annual_contribution
        else:
            # Decumulation phase: grow previous wealth - withdraw annual spending
            new_wealth = (previous_wealth * annual_returns) - annual_spending
            
        # Floor wealth at 0 (cannot have negative debt in portfolio tracking)
        portfolio_paths[year, :] = np.maximum(new_wealth, 0)
