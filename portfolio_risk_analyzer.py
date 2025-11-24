import pandas as pd
import numpy as np
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

class PortfolioRiskAnalyzer:
    """
    A class to analyze portfolio risk by reading CSV files and assessing individual asset risks.
    """
    
    def __init__(self, holdings_file=None, history_file=None):
        """
        Initialize the risk analyzer with optional CSV file paths.
        
        Args:
            holdings_file (str): Path to holdings CSV file
            history_file (str): Path to historical price CSV file
        """
        self.holdings_df = None
        self.history_df = None
        
        if holdings_file:
            self.load_holdings(holdings_file)
        if history_file:
            self.load_history(history_file)
    
    def load_holdings(self, file_path):
        """Load holdings data from CSV file."""
        try:
            self.holdings_df = pd.read_csv(file_path)
            print(f"Successfully loaded holdings from {file_path}")
            print(f"Holdings data shape: {self.holdings_df.shape}")
        except Exception as e:
            print(f"Error loading holdings file: {e}")
    
    def load_history(self, file_path):
        """Load historical price data from CSV file."""
        try:
            self.history_df = pd.read_csv(file_path)
            # Convert date column to datetime if it exists
            if 'Date' in self.history_df.columns:
                self.history_df['Date'] = pd.to_datetime(self.history_df['Date'])
            print(f"Successfully loaded history from {file_path}")
            print(f"History data shape: {self.history_df.shape}")
        except Exception as e:
            print(f"Error loading history file: {e}")
    
    def calculate_asset_returns(self):
        """Calculate daily returns for each asset in the history data."""
        if self.history_df is None:
            print("No history data loaded. Cannot calculate returns.")
            return None
        
        # Get all columns except 'Date'
        price_columns = [col for col in self.history_df.columns if col != 'Date']
        returns_data = {}
        
        for col in price_columns:
            # Calculate daily returns
            returns = self.history_df[col].pct_change().dropna()
            returns_data[col] = returns
        
        returns_df = pd.DataFrame(returns_data)
        return returns_df
    
    def calculate_volatility(self, returns_df):
        """Calculate annualized volatility for each asset."""
        if returns_df is None:
            return None
            
        # Calculate annualized volatility (standard deviation of returns * sqrt(252))
        volatility = returns_df.std() * np.sqrt(252)
        return volatility
    
    def calculate_beta(self, returns_df, market_symbol='SPY'):
        """Calculate beta for each asset relative to the market."""
        if returns_df is None or market_symbol not in returns_df.columns:
            print(f"Market symbol {market_symbol} not found in data or returns not calculated.")
            return None
        
        market_returns = returns_df[market_symbol]
        betas = {}
        
        for asset in returns_df.columns:
            if asset != market_symbol and not returns_df[asset].isna().all():
                # Calculate covariance between asset and market
                covariance = np.cov(returns_df[asset], market_returns)[0][1]
                # Calculate market variance
                market_variance = np.var(market_returns)
                # Calculate beta
                beta = covariance / market_variance
                betas[asset] = beta
        
        return pd.Series(betas)
    
    def calculate_value_at_risk(self, returns_df, confidence_level=0.05):
        """Calculate Value at Risk (VaR) for each asset."""
        if returns_df is None:
            return None
            
        var_values = {}
        for asset in returns_df.columns:
            if not returns_df[asset].isna().all():
                # Calculate VaR at the given confidence level
                var_values[asset] = returns_df[asset].quantile(confidence_level)
        
        return pd.Series(var_values)
    
    def calculate_sharpe_ratio(self, returns_df, risk_free_rate=0.02):
        """Calculate Sharpe ratio for each asset."""
        if returns_df is None:
            return None
            
        sharpe_ratios = {}
        for asset in returns_df.columns:
            if not returns_df[asset].isna().all():
                # Calculate excess returns (returns - risk free rate / 252 for daily)
                excess_returns = returns_df[asset] - (risk_free_rate / 252)
                mean_excess_return = excess_returns.mean()
                volatility = returns_df[asset].std()
                
                if volatility != 0:
                    sharpe_ratio = mean_excess_return / volatility
                    sharpe_ratios[asset] = sharpe_ratio
                else:
                    sharpe_ratios[asset] = np.nan
        
        return pd.Series(sharpe_ratios)
    
    def calculate_max_drawdown(self, returns_df):
        """Calculate maximum drawdown for each asset."""
        if returns_df is None:
            return None
            
        max_drawdowns = {}
        
        for asset in returns_df.columns:
            if not returns_df[asset].isna().all():
                # Calculate cumulative returns
                cumulative_returns = (1 + returns_df[asset]).cumprod()
                # Calculate running maximum
                running_max = cumulative_returns.expanding().max()
                # Calculate drawdown
                drawdown = (cumulative_returns - running_max) / running_max
                # Get maximum drawdown
                max_drawdowns[asset] = drawdown.min()
        
        return pd.Series(max_drawdowns)
    
    def assess_individual_asset_risk(self):
        """Comprehensive risk assessment for individual assets."""
        print("="*60)
        print("PORTFOLIO RISK ANALYSIS REPORT")
        print("="*60)
        
        if self.history_df is None:
            print("Historical price data is required for risk analysis.")
            return
        
        # Calculate returns
        returns_df = self.calculate_asset_returns()
        if returns_df is None:
            print("Could not calculate returns. Check historical data format.")
            return
        
        print("\n1. ANNUALIZED VOLATILITY (Risk Indicator)")
        print("-" * 40)
        volatility = self.calculate_volatility(returns_df)
        if volatility is not None:
            for asset, vol in volatility.items():
                risk_level = self._classify_risk_level(vol)
                print(f"{asset:5s}: {vol*100:.2f}% ({risk_level})")
        
        print("\n2. BETA (Market Sensitivity)")
        print("-" * 40)
        beta = self.calculate_beta(returns_df)
        if beta is not None:
            for asset, b in beta.items():
                sensitivity = self._classify_beta_sensitivity(b)
                print(f"{asset:5s}: {b:.2f} ({sensitivity})")
        
        print("\n3. VALUE AT RISK (VaR - 5% Confidence)")
        print("-" * 40)
        var_95 = self.calculate_value_at_risk(returns_df, 0.05)
        if var_95 is not None:
            for asset, var in var_95.items():
                print(f"{asset:5s}: {var*100:.2f}%")
        
        print("\n4. SHARPE RATIO (Risk-Adjusted Return)")
        print("-" * 40)
        sharpe = self.calculate_sharpe_ratio(returns_df)
        if sharpe is not None:
            for asset, ratio in sharpe.items():
                if not np.isnan(ratio):
                    performance = self._classify_performance(ratio)
                    print(f"{asset:5s}: {ratio:.2f} ({performance})")
                else:
                    print(f"{asset:5s}: NaN (insufficient data)")
        
        print("\n5. MAXIMUM DRAWDOWN")
        print("-" * 40)
        max_dd = self.calculate_max_drawdown(returns_df)
        if max_dd is not None:
            for asset, dd in max_dd.items():
                print(f"{asset:5s}: {dd*100:.2f}%")
        
        # Summary risk matrix
        self._create_risk_summary(returns_df)
    
    def _classify_risk_level(self, volatility):
        """Classify risk level based on volatility."""
        if volatility < 0.15:
            return "Low"
        elif volatility < 0.25:
            return "Medium"
        elif volatility < 0.40:
            return "High"
        else:
            return "Very High"
    
    def _classify_beta_sensitivity(self, beta):
        """Classify market sensitivity based on beta."""
        if beta < 0.5:
            return "Low sensitivity"
        elif beta < 1.0:
            return "Below avg sensitivity"
        elif beta < 1.5:
            return "Average sensitivity"
        else:
            return "High sensitivity"
    
    def _classify_performance(self, sharpe_ratio):
        """Classify performance based on Sharpe ratio."""
        if sharpe_ratio > 1.0:
            return "Excellent"
        elif sharpe_ratio > 0.5:
            return "Good"
        elif sharpe_ratio > 0:
            return "Poor"
        else:
            return "Negative"
    
    def _create_risk_summary(self, returns_df):
        """Create a summary of risk metrics for all assets."""
        print("\n6. COMPREHENSIVE RISK SUMMARY")
        print("-" * 40)
        
        volatility = self.calculate_volatility(returns_df)
        beta = self.calculate_beta(returns_df)
        var_95 = self.calculate_value_at_risk(returns_df, 0.05)
        sharpe = self.calculate_sharpe_ratio(returns_df)
        max_dd = self.calculate_max_drawdown(returns_df)
        
        # Create a summary DataFrame
        summary_data = {
            'Volatility': volatility,
            'Beta': beta,
            'VaR (5%)': var_95,
            'Sharpe Ratio': sharpe,
            'Max Drawdown': max_dd
        }
        
        summary_df = pd.DataFrame(summary_data)
        print(summary_df.round(4))
        
        # Identify highest and lowest risk assets
        print("\n7. RISK RANKINGS")
        print("-" * 40)
        
        if volatility is not None:
            # Highest volatility (riskiest)
            if not volatility.empty:
                highest_vol_asset = volatility.idxmax()
                lowest_vol_asset = volatility.idxmin()
                print(f"Highest volatility: {highest_vol_asset} ({volatility[highest_vol_asset]*100:.2f}%)")
                print(f"Lowest volatility: {lowest_vol_asset} ({volatility[lowest_vol_asset]*100:.2f}%)")
        
        if sharpe is not None:
            # Highest Sharpe ratio (best risk-adjusted return)
            if not sharpe.empty:
                valid_sharpe = sharpe.dropna()
                if not valid_sharpe.empty:
                    best_sharpe_asset = valid_sharpe.idxmax()
                    worst_sharpe_asset = valid_sharpe.idxmin()
                    print(f"Best risk-adjusted return: {best_sharpe_asset} (Sharpe: {valid_sharpe[best_sharpe_asset]:.2f})")
                    print(f"Worst risk-adjusted return: {worst_sharpe_asset} (Sharpe: {valid_sharpe[worst_sharpe_asset]:.2f})")
        
        if max_dd is not None:
            # Highest drawdown (worst loss)
            if not max_dd.empty:
                worst_dd_asset = max_dd.idxmin()  # min because drawdowns are negative
                best_dd_asset = max_dd.idxmax()   # max because less negative is better
                print(f"Largest drawdown: {worst_dd_asset} ({max_dd[worst_dd_asset]*100:.2f}%)")
                print(f"Smallest drawdown: {best_dd_asset} ({max_dd[best_dd_asset]*100:.2f}%)")

def main():
    """Main function to demonstrate the portfolio risk analyzer."""
    print("Portfolio Risk Analyzer")
    print("="*50)
    
    # Initialize analyzer with sample files
    analyzer = PortfolioRiskAnalyzer(
        holdings_file='sample_holdings.csv',
        history_file='sample_history.csv'
    )
    
    # Perform risk analysis
    analyzer.assess_individual_asset_risk()

if __name__ == "__main__":
    main()