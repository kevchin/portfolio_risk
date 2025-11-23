# Fidelity Portfolio Risk Analysis

This repository contains tools for performing risk analysis on your investment portfolio using data exported from Fidelity.

## Files Overview

### Data Files
- `sample_holdings.csv` - Sample portfolio holdings data exported from Fidelity, containing stock symbols, quantities, current values, and descriptions
- `sample_history.csv` - Sample historical price data for the portfolio holdings and benchmark index (e.g. SPY), used for risk calculations
- `Portfolio Risk Analysis (sample).pdf` - Sample output report showing the results of the risk analysis

### Code Files
- `sample_risk_analysis.ipynb` - Jupyter notebook that performs comprehensive portfolio risk analysis including:
  - Loading and processing portfolio holdings
  - Calculating portfolio weights and returns
  - Computing correlation matrix between holdings
  - Generating risk metrics and visualizations
- `process_portfolio.py` - Python script to clean and filter portfolio data from Fidelity exports
- `correlation_matrix.png` - Generated correlation matrix visualization showing relationships between portfolio holdings

## Usage Instructions

### 1. Prepare Your Data
- Export your portfolio holdings from Fidelity as a CSV file (rename to match the script expectations)
- Generate historical price data for your holdings using the Google Sheets formula:
  ```
  =GOOGLEFINANCE(A2,"price",DATE(YEAR(TODAY())-5,1,1),TODAY(),"daily")
  ```
  Or use alternative data sources for the past 5+ years of daily closing prices.

### 2. Process Your Portfolio
- Use `process_portfolio.py` to clean and filter your Fidelity export data
- Update the input filename in the script to match your exported file

### 3. Run Risk Analysis
- Open and run `sample_risk_analysis.ipynb` in Jupyter Notebook
- The notebook will generate correlation matrices, risk metrics, and visualizations
- Results will include correlation_matrix.png and various risk statistics

## Key Features
- Portfolio diversification analysis through correlation matrices
- Risk metric calculations (volatility, correlation between holdings)
- Visual representation of portfolio relationships
- Automated data processing from Fidelity exports
