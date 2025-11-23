# Portfolio Risk Analyzer

This Python program analyzes the risk of a portfolio by reading CSV files and providing various assessments of risk for individual assets.

## Features

The program calculates and displays the following risk metrics for each asset in your portfolio:

1. **Annualized Volatility** - A measure of price fluctuations over time
2. **Beta** - Sensitivity to market movements (relative to SPY ETF)
3. **Value at Risk (VaR)** - Potential loss at 5% confidence level
4. **Sharpe Ratio** - Risk-adjusted return measure
5. **Maximum Drawdown** - Largest peak-to-trough decline
6. **Risk Rankings** - Comparative analysis of assets

## Required Files

The program works with two types of CSV files:

1. **Holdings CSV** - Contains current portfolio holdings
   - Expected columns: Symbol, Quantity, Current Value, etc.
   - Used for portfolio composition analysis

2. **Historical Prices CSV** - Contains historical price data
   - First column should be "Date"
   - Other columns should be asset symbols (e.g., AAPL, MSFT, etc.)
   - Used for risk calculations

## Usage

### Basic Usage
```python
from portfolio_risk_analyzer import PortfolioRiskAnalyzer

# Initialize analyzer with file paths
analyzer = PortfolioRiskAnalyzer(
    holdings_file='sample_holdings.csv',
    history_file='sample_history.csv'
)

# Perform risk analysis
analyzer.assess_individual_asset_risk()
```

### Command Line Usage
```bash
python portfolio_risk_analyzer.py
```

## Risk Metrics Explained

- **Volatility**: Annualized standard deviation of daily returns
  - Low: < 15%, Medium: 15-25%, High: 25-40%, Very High: > 40%

- **Beta**: Sensitivity to market movements (SPY ETF)
  - < 0.5: Low sensitivity, 0.5-1.0: Below avg, 1.0-1.5: Average, > 1.5: High

- **Sharpe Ratio**: Risk-adjusted return
  - > 1.0: Excellent, 0.5-1.0: Good, 0-0.5: Poor, < 0: Negative

## Dependencies

- pandas
- numpy

Install with: `pip install pandas numpy`

## Sample Output Interpretation

The program generates a comprehensive report with:
- Individual risk metrics for each asset
- Risk classifications (Low, Medium, High, etc.)
- Comparative rankings of assets by different risk measures
- Summary table with all metrics

## Customization

You can customize the risk analysis by:
- Changing the risk-free rate in `calculate_sharpe_ratio()` (default: 2%)
- Adjusting the confidence level in `calculate_value_at_risk()` (default: 5%)
- Modifying the market symbol used for beta calculation (default: SPY)