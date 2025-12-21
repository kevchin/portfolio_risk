#!/usr/bin/env python3
"""
Index Fund Fee Structure Analyzer

This program analyzes the fee structure of index funds based on their ticker symbols.
It fetches expense ratio data and provides analysis and comparison features.
"""

import requests
import json
import pandas as pd
from typing import Dict, List, Optional
import yfinance as yf


class IndexFundFeeAnalyzer:
    """
    A class to analyze the fee structures of index funds based on ticker symbols.
    """
    
    def __init__(self):
        """Initialize the analyzer."""
        self.fund_data = {}
        
    def get_fund_info(self, ticker: str) -> Optional[Dict]:
        """
        Get fund information including expense ratio from Yahoo Finance.
        
        Args:
            ticker: The ticker symbol of the fund
            
        Returns:
            Dictionary containing fund information or None if not found
        """
        try:
            fund = yf.Ticker(ticker)
            info = fund.info
            
            # Try multiple possible field names for expense ratio
            expense_ratio = None
            for field in ['netExpenseRatio', 'expenseRatio', 'annualReportExpenseRatio', 'grossExpRatio', 'netExpRatio']:
                if field in info and info[field] is not None:
                    expense_ratio = info[field]
                    # Handle different formats of expense ratio data
                    # The yfinance API sometimes returns expense ratios in different formats
                    # If the value is between 0.01 and 1.0, it might be in percentage form 
                    # (e.g., 0.03 meaning 0.03% rather than 0.03 as a decimal)
                    if 0.01 <= expense_ratio <= 1.0:
                        # This is likely in percentage form (0.03 = 0.03%), convert to decimal (0.0003)
                        expense_ratio = expense_ratio / 100
                    elif 1 < expense_ratio <= 100:
                        # This is definitely in percentage form, convert to decimal
                        expense_ratio = expense_ratio / 100
                    break
            
            # If no expense ratio found, default to N/A
            if expense_ratio is None:
                expense_ratio = 'N/A'
            
            # Extract relevant fee information
            fund_info = {
                'ticker': ticker,
                'name': info.get('longName', 'N/A'),
                'expense_ratio': expense_ratio,
                'category': info.get('category', 'N/A'),
                'fundFamily': info.get('fundFamily', 'N/A'),
                'totalAssets': info.get('totalAssets', 'N/A'),
                'yield': info.get('yield', 'N/A'),
                'dividendRate': info.get('dividendRate', 'N/A'),
                'fiveYearAvgReturn': info.get('fiveYearAverageReturn', 'N/A'),
                'threeYearAvgReturn': info.get('threeYearAverageReturn', 'N/A'),
            }
            
            return fund_info
        except Exception as e:
            print(f"Error fetching data for {ticker}: {str(e)}")
            return None
    
    def analyze_single_fund(self, ticker: str) -> Dict:
        """
        Analyze the fee structure of a single fund.
        
        Args:
            ticker: The ticker symbol of the fund
            
        Returns:
            Dictionary with analysis results
        """
        fund_info = self.get_fund_info(ticker)
        
        if not fund_info:
            return {"error": f"Could not retrieve data for {ticker}"}
        
        analysis = {
            'ticker': fund_info['ticker'],
            'name': fund_info['name'],
            'expense_ratio': fund_info['expense_ratio'],
            'fee_category': self._categorize_expense_ratio(fund_info['expense_ratio']),
            'annual_cost_per_10k': self._calculate_annual_cost(10000, fund_info['expense_ratio']),
            'category': fund_info['category'],
            'fund_family': fund_info['fundFamily']
        }
        
        return analysis
    
    def _categorize_expense_ratio(self, expense_ratio) -> str:
        """
        Categorize expense ratio into low/medium/high.
        
        Args:
            expense_ratio: The expense ratio as a decimal or percentage
            
        Returns:
            String category ('Low', 'Medium', 'High', or 'N/A')
        """
        if expense_ratio == 'N/A':
            return 'N/A'
        
        # Convert to decimal if it's a percentage
        if isinstance(expense_ratio, (int, float)):
            ratio = expense_ratio
        else:
            # Assume it's already a decimal if less than 1, otherwise convert from percentage
            try:
                ratio = float(expense_ratio)
                if ratio > 1:  # It's a percentage, convert to decimal
                    ratio = ratio / 100
            except ValueError:
                return 'N/A'
        
        if ratio <= 0.001:  # 0.1% or lower
            return 'Low'
        elif ratio <= 0.005:  # 0.5% or lower
            return 'Medium'
        else:
            return 'High'
    
    def _calculate_annual_cost(self, investment_amount: float, expense_ratio) -> float:
        """
        Calculate the annual cost based on investment amount and expense ratio.
        
        Args:
            investment_amount: The amount invested
            expense_ratio: The expense ratio as a decimal (e.g., 0.0003 for 0.03%)
            
        Returns:
            Annual cost in dollars
        """
        if expense_ratio == 'N/A':
            return 0
        
        # Convert to decimal if needed
        if isinstance(expense_ratio, (int, float)):
            ratio = expense_ratio
        else:
            try:
                ratio = float(expense_ratio)
                if ratio > 1:  # It's a percentage, convert to decimal
                    ratio = ratio / 100
            except ValueError:
                return 0
        
        return investment_amount * ratio
    
    def compare_funds(self, tickers: List[str]) -> pd.DataFrame:
        """
        Compare multiple funds based on their fee structures.
        
        Args:
            tickers: List of ticker symbols to compare
            
        Returns:
            DataFrame with comparison results
        """
        results = []
        
        for ticker in tickers:
            analysis = self.analyze_single_fund(ticker)
            if 'error' not in analysis:
                results.append(analysis)
        
        if not results:
            print("No valid fund data retrieved.")
            return pd.DataFrame()
        
        df = pd.DataFrame(results)
        
        # Sort by expense ratio
        df = df.sort_values(by='expense_ratio', key=lambda x: pd.to_numeric(x, errors='coerce'), ascending=True)
        
        return df
    
    def generate_report(self, tickers: List[str]) -> str:
        """
        Generate a comprehensive fee analysis report for the given tickers.
        
        Args:
            tickers: List of ticker symbols to analyze
            
        Returns:
            Formatted report string
        """
        report_lines = ["Index Fund Fee Structure Analysis Report", "="*50]
        
        # Add overall statistics
        df = self.compare_funds(tickers)
        
        if df.empty:
            return "No valid fund data could be retrieved for the provided tickers."
        
        report_lines.append(f"\nAnalyzed {len(df)} funds:")
        report_lines.append("-" * 30)
        
        for _, row in df.iterrows():
            report_lines.append(f"{row['ticker']:<8} - {row['name']}")
            report_lines.append(f"         Expense Ratio: {row['expense_ratio']} ({row['fee_category']})")
            report_lines.append(f"         Annual Cost (on $10K): ${row['annual_cost_per_10k']:.2f}")
            report_lines.append("")
        
        # Summary statistics
        numeric_ratios = pd.to_numeric(df['expense_ratio'], errors='coerce').dropna()
        if len(numeric_ratios) > 0:
            report_lines.append("Summary Statistics:")
            report_lines.append("-" * 20)
            report_lines.append(f"Average Expense Ratio: {(numeric_ratios.mean() * 100):.3f}%")
            report_lines.append(f"Median Expense Ratio: {(numeric_ratios.median() * 100):.3f}%")
            report_lines.append(f"Lowest Expense Ratio: {(numeric_ratios.min() * 100):.3f}%")
            report_lines.append(f"Highest Expense Ratio: {(numeric_ratios.max() * 100):.3f}%")
        
        return "\n".join(report_lines)


def main():
    """Main function to demonstrate the analyzer."""
    analyzer = IndexFundFeeAnalyzer()
    
    # Example tickers for popular index funds
    example_tickers = [
        'VTI',    # Vanguard Total Stock Market ETF
        'VOO',    # Vanguard S&P 500 ETF
        'IVV',    # iShares Core S&P 500 ETF
        'SPY',    # SPDR S&P 500 ETF
        'QQQ',    # Invesco QQQ Trust
        'VTIAX',  # Vanguard Total Stock Market Index Fund
        'FXAIX',  # Fidelity 500 Index Fund
    ]
    
    print("Index Fund Fee Structure Analyzer")
    print("="*50)
    
    while True:
        print("\nOptions:")
        print("1. Analyze single fund")
        print("2. Compare multiple funds")
        print("3. Run example analysis")
        print("4. Exit")
        
        choice = input("\nEnter your choice (1-4): ").strip()
        
        if choice == '1':
            ticker = input("Enter fund ticker symbol: ").strip().upper()
            analysis = analyzer.analyze_single_fund(ticker)
            
            if 'error' in analysis:
                print(f"\n{analysis['error']}")
            else:
                print(f"\nAnalysis for {analysis['ticker']} - {analysis['name']}:")
                print(f"Expense Ratio: {analysis['expense_ratio']}")
                print(f"Fee Category: {analysis['fee_category']}")
                print(f"Annual Cost (on $10,000): ${analysis['annual_cost_per_10k']:.2f}")
                
        elif choice == '2':
            tickers_input = input("Enter fund ticker symbols separated by commas: ").strip()
            tickers = [t.strip().upper() for t in tickers_input.split(',')]
            
            df = analyzer.compare_funds(tickers)
            if not df.empty:
                print(f"\nComparison of {len(df)} funds:")
                print(df[['ticker', 'name', 'expense_ratio', 'fee_category', 'annual_cost_per_10k']].to_string(index=False))
            else:
                print("No valid fund data could be retrieved.")
                
        elif choice == '3':
            print("\nRunning example analysis...")
            report = analyzer.generate_report(example_tickers[:5])  # Using first 5 for faster example
            print(report)
            
        elif choice == '4':
            print("Thank you for using the Index Fund Fee Analyzer!")
            break
            
        else:
            print("Invalid choice. Please enter 1, 2, 3, or 4.")


if __name__ == "__main__":
    main()