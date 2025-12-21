#!/usr/bin/env python3
"""
Test script for the Index Fund Fee Analyzer
"""

from index_fund_fee_analyzer import IndexFundFeeAnalyzer

def test_analyzer():
    """Test the basic functionality of the analyzer."""
    print("Testing Index Fund Fee Analyzer...")
    print("="*50)
    
    analyzer = IndexFundFeeAnalyzer()
    
    # Test single fund analysis
    print("\n1. Testing single fund analysis:")
    vti_analysis = analyzer.analyze_single_fund('VTI')
    print(f"VTI Analysis: {vti_analysis}")
    
    # Test multiple fund comparison
    print("\n2. Testing multiple fund comparison:")
    tickers = ['VTI', 'VOO', 'SPY']
    comparison_df = analyzer.compare_funds(tickers)
    if not comparison_df.empty:
        print("Comparison Results:")
        print(comparison_df[['ticker', 'name', 'expense_ratio', 'fee_category', 'annual_cost_per_10k']])
    else:
        print("No comparison data available (possibly due to network issues)")
    
    # Test report generation
    print("\n3. Testing report generation:")
    report = analyzer.generate_report(['VTI', 'VOO', 'IVV'])
    print(report)

if __name__ == "__main__":
    test_analyzer()