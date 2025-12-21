#!/usr/bin/env python3
"""
Example usage of the Index Fund Fee Analyzer
"""

from index_fund_fee_analyzer import IndexFundFeeAnalyzer

def example_usage():
    """Demonstrate how to use the IndexFundFeeAnalyzer class."""
    print("Index Fund Fee Analyzer - Example Usage")
    print("="*50)
    
    # Create an instance of the analyzer
    analyzer = IndexFundFeeAnalyzer()
    
    # Example 1: Analyze a single fund
    print("\n1. Analyzing a single fund (VTI - Vanguard Total Stock Market ETF):")
    vti_analysis = analyzer.analyze_single_fund('VTI')
    if 'error' not in vti_analysis:
        print(f"   Ticker: {vti_analysis['ticker']}")
        print(f"   Name: {vti_analysis['name']}")
        print(f"   Expense Ratio: {vti_analysis['expense_ratio']}")
        print(f"   Fee Category: {vti_analysis['fee_category']}")
        print(f"   Annual Cost (on $10,000): ${vti_analysis['annual_cost_per_10k']:.2f}")
    else:
        print(f"   Error: {vti_analysis['error']}")
    
    # Example 2: Compare multiple funds
    print("\n2. Comparing multiple funds:")
    tickers_to_compare = ['VTI', 'VOO', 'IVV', 'SPY']
    comparison_df = analyzer.compare_funds(tickers_to_compare)
    
    if not comparison_df.empty:
        print("   Comparison Results (sorted by expense ratio):")
        print(comparison_df[['ticker', 'name', 'expense_ratio', 'fee_category', 'annual_cost_per_10k']].to_string(index=False))
    else:
        print("   No valid data retrieved for comparison.")
    
    # Example 3: Generate a report
    print("\n3. Generating a detailed report for selected funds:")
    report = analyzer.generate_report(['VTI', 'VOO', 'QQQ'])
    print(report)
    
    # Example 4: Understanding fee impact over time
    print("\n4. Fee impact comparison:")
    print("   For a $100,000 investment:")
    for ticker in ['VTI', 'VOO', 'QQQ']:
        analysis = analyzer.analyze_single_fund(ticker)
        if 'error' not in analysis:
            annual_cost = analysis['annual_cost_per_10k'] * 10  # Multiply by 10 for $100k
            print(f"   {ticker}: ${annual_cost:.2f} per year in fees")

if __name__ == "__main__":
    example_usage()