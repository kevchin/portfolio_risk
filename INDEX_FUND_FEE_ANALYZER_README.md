# Index Fund Fee Structure Analyzer

This program analyzes the fee structure of index funds based on their ticker symbols. It provides detailed information about expense ratios and helps investors compare costs between different index funds.

## Features

- **Single Fund Analysis**: Get detailed fee information for a specific fund
- **Multiple Fund Comparison**: Compare expense ratios across multiple funds
- **Cost Calculations**: Calculate annual fees based on investment amount
- **Category Classification**: Categorizes funds as Low/Medium/High fee
- **Comprehensive Reports**: Generate detailed analysis reports

## Requirements

- Python 3.7+
- Required packages: `yfinance`, `pandas`

Install dependencies:
```bash
pip install yfinance pandas
```

## Usage

### Interactive Mode

Run the program in interactive mode:
```bash
python index_fund_fee_analyzer.py
```

The program provides three main options:
1. **Analyze single fund** - Enter a ticker symbol to analyze individual fund fees
2. **Compare multiple funds** - Enter multiple ticker symbols separated by commas
3. **Run example analysis** - See a demonstration with popular index funds

### Programmatic Usage

You can also use the analyzer programmatically:

```python
from index_fund_fee_analyzer import IndexFundFeeAnalyzer

analyzer = IndexFundFeeAnalyzer()

# Analyze a single fund
result = analyzer.analyze_single_fund('VTI')
print(result)

# Compare multiple funds
comparison = analyzer.compare_funds(['VTI', 'VOO', 'SPY'])
print(comparison)

# Generate a report
report = analyzer.generate_report(['VTI', 'VOO', 'IVV'])
print(report)
```

## Fee Categories

The program categorizes expense ratios as follows:
- **Low**: ≤ 0.1% (≤ 0.001)
- **Medium**: 0.1% to 0.5% (0.001 to 0.005)
- **High**: > 0.5% (> 0.005)

## Example Output

When analyzing a fund, you'll see information like:
- Ticker symbol
- Fund name
- Expense ratio
- Fee category
- Annual cost for a $10,000 investment
- Fund category and family

## Common Index Fund Tickers

Some popular index funds to analyze:
- VTI: Vanguard Total Stock Market ETF
- VOO: Vanguard S&P 500 ETF
- IVV: iShares Core S&P 500 ETF
- SPY: SPDR S&P 500 ETF
- QQQ: Invesco QQQ Trust
- VTIAX: Vanguard Total Stock Market Index Fund Admiral Shares
- FXAIX: Fidelity 500 Index Fund

## How It Works

The program uses the yfinance library to fetch fund information from Yahoo Finance. It extracts the expense ratio and other relevant data to provide a comprehensive fee analysis.

Note: Sometimes expense ratio data may not be available through the API, in which case it will show as 'N/A'.

## Understanding Expense Ratios

The expense ratio represents the annual cost of owning a fund as a percentage of your investment. For example:
- A 0.03% expense ratio means $3 per year for every $10,000 invested
- A 0.10% expense ratio means $10 per year for every $10,000 invested

Lower expense ratios generally mean more money stays invested, potentially leading to better long-term returns.