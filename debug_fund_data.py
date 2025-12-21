#!/usr/bin/env python3
"""
Debug script to see what fund data is available from yfinance
"""

import yfinance as yf

def debug_fund_data():
    """Print all available fund information to understand the data structure."""
    print("Debugging Fund Data from yfinance")
    print("="*50)
    
    # Test with a known fund
    ticker = 'VTI'
    fund = yf.Ticker(ticker)
    info = fund.info
    
    print(f"Available data for {ticker}:")
    print("-" * 30)
    
    # Print all available keys and their values
    for key, value in sorted(info.items()):
        print(f"{key}: {value}")
    
    print("\nSpecifically checking expense ratio related fields:")
    expense_fields = [
        'expenseRatio',
        'annualReportExpenseRatio', 
        'grossExpRatio',
        'netExpRatio',
        'fundOperatingExpenseRatio',
        'trailingThreeMonthOperatingExpense',
        'expenseRatioValue'
    ]
    
    for field in expense_fields:
        value = info.get(field, 'NOT FOUND')
        print(f"{field}: {value}")

if __name__ == "__main__":
    debug_fund_data()