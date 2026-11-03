# import pandas as pd
# import sys

# class PortfolioAnalyzer:
#     def __init__(self):
#         self.df = None

#     def load_portfolio(self, csv_path: str):
#         # Implementation here
#         pass

#     def calculate_metrics(self):
#         # Implementation here
#         pass

#     def get_total_market_value(self) -> float:
#         # Implementation here
#         return 0.0

#     def get_top_performer(self) -> str:
#         # Implementation here
#         return ""

#     def get_underperforming_assets(self, threshold_pct: float) -> list:
#         # Implementation here
#         return []

#     def apply_sector_mapping(self, sector_csv: str):
#         # Implementation here
#         pass
import pandas as pd
import sys
import os

class PortfolioAnalyzer:
    def __init__(self):
        self.df = None

    def load_portfolio(self, csv_path: str):
        self.df = pd.read_csv(csv_path)

    def calculate_metrics(self):
        self.df['cost_basis'] = self.df['shares'] * self.df['purchase_price']
        self.df['market_value'] = self.df['shares'] * self.df['current_price']
        self.df['gain_loss'] = self.df['market_value'] - self.df['cost_basis']
        self.df['gain_loss_pct'] = (self.df['gain_loss'] / self.df['cost_basis']) * 100

    def get_total_market_value(self) -> float:
        return float(self.df['market_value'].sum())

    def get_top_performer(self) -> str:
        idx = self.df['gain_loss_pct'].idxmax()
        return self.df.loc[idx, 'symbol']

    def get_underperforming_assets(self, threshold_pct: float) -> list:
        subset = self.df[self.df['gain_loss_pct'] <= threshold_pct]
        return subset['symbol'].tolist()

    def apply_sector_mapping(self, sector_csv: str):
        sector_df = pd.read_csv(sector_csv)
        self.df = self.df.merge(sector_df, on='symbol', how='left')
if __name__ == "__main__":
    # Command processor for standardized evaluation
    analyzer = PortfolioAnalyzer()
    input_data = sys.stdin.read().splitlines()
    for line in input_data:
        parts = line.strip().split()
        if not parts: continue
        cmd = parts[0]
        if cmd == "LOAD": analyzer.load_portfolio(parts[1])
        elif cmd == "CALC": analyzer.calculate_metrics()
        elif cmd == "TOTAL":
            val = analyzer.get_total_market_value()
            print(f"Total Value: {val:.1f}")
        elif cmd == "TOP": print(f"Top: {analyzer.get_top_performer()}")
        elif cmd == "UNDER": print(f"Under: {', '.join(analyzer.get_underperforming_assets(float(parts[1])))}")
        elif cmd == "SECTOR": analyzer.apply_sector_mapping(parts[1])
        elif cmd == "SHOW": print(analyzer.df[['symbol', 'gain_loss_pct', 'sector']].to_string(index=False))
