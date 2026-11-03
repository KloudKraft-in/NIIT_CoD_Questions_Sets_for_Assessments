from typing import List, Generator, Tuple, Callable
from functools import wraps
import sys

# Complete the 'generate_trading_report' function below.
#
# The function is expected to return a LIST_OF_STRINGS.
# The function accepts INTEGER_ARRAY prices as parameter.
#
# You must implement:
# 1. A decorator 'validate_prices' to validate input
# 2. A generator function 'find_transactions' that yields transaction tuples
# 3. The main function 'generate_trading_report' that formats the output

def validate_prices(func: Callable) -> Callable:
    """Decorator to validate price data"""
    @wraps(func)
    def wrapper(prices: List[int]) -> Generator[Tuple[int, int, int, int, int], None, None]:
        # Add validation logic here
        return func(prices)
    return wrapper

@validate_prices
def find_transactions(prices: List[int]) -> Generator[Tuple[int, int, int, int, int], None, None]:
    """Generator that yields (buy_day, buy_price, sell_day, sell_price, profit)"""
    pass

def generate_trading_report(prices: List[int]) -> List[str]:
    """Generate formatted trading report"""
    pass


#Don't make changes in below code.
if __name__ == '__main__':
    # Standard HackerRank input reading
    line1 = input().strip()
    if not line1:
        sys.exit(0)
    n = int(line1)
    
    line2 = input().strip()
    prices = list(map(int, line2.split()))

    report = generate_trading_report(prices)

    for line in report:
        print(line)
