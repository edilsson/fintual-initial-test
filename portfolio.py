import math


class Stock:
    """Represents a stock with its name and current price."""

    def __init__(self, name: str) -> None:
        self.name = name

    def get_current_price(self):
        """Placeholder for current price, replace with actual logic to fetch price."""
        stock_prices = {
            "AAPL": 347,
            "GOOGL": 217,
            "MSFT": 109,
            "NVDA": 1266,
        }
        return stock_prices.get(self.name, 0)


class Holding:
    """Represents a holding of a stock with its amount."""

    def __init__(self, stock: Stock, amount: int) -> None:
        self.stock = stock
        self.amount = amount

    def get_total_value(self):
        """Calculate the total value of the shares held."""
        return self.stock.get_current_price() * self.amount


class AllocatedStock:
    """Represents a stock with its allocated percentage in the portfolio."""

    def __init__(self, stock: Stock, allocation: float) -> None:
        self.stock = stock
        self.allocation = allocation


class Portfolio:
    """Represents a portfolio of shares and their allocated stocks."""

    def __init__(
        self,
        holdings: list[Holding],
        allocated_stocks: list[AllocatedStock],
    ) -> None:
        self.holdings = holdings
        self.allocated_stocks = allocated_stocks

    def rebalance(self) -> dict:
        """Rebalance the portfolio based on allocated stocks."""
        sell, buy = [], []
        allocated_stocks_names = [als.stock.name for als in self.allocated_stocks]
        total_value = sum(holding.get_total_value() for holding in self.holdings)

        for holding in self.holdings:
            stock = holding.stock
            if stock.name in allocated_stocks_names:
                current_value = holding.get_total_value()
                current_price = stock.get_current_price()
                allocated_stock = next(
                    als for als in self.allocated_stocks if als.stock.name == stock.name
                )
                target_value = allocated_stock.allocation * total_value
                shares_to_operate = abs(current_value - target_value) / current_price
                if current_value > target_value:
                    sell.append((stock.name, shares_to_operate))
                elif current_value < target_value:
                    buy.append((stock.name, shares_to_operate))
                allocated_stocks_names.remove(stock.name)
            else:
                sell.append((stock.name, holding.amount))

        # Handle stocks that are in allocated_stocks but not in current portfolio
        if allocated_stocks_names:
            for stock_name in allocated_stocks_names:
                allocated_stock = next(
                    als for als in self.allocated_stocks if als.stock.name == stock_name
                )
                shares_to_buy = (
                    allocated_stock.allocation
                    * total_value
                    / allocated_stock.stock.get_current_price()
                )
                buy.append((stock_name, shares_to_buy))

        return {"sell": sell, "buy": buy}

    def check_total_allocation(self) -> None:
        """Check if the total allocation of allocated stocks equals 1.0."""
        total_allocation = sum(als.allocation for als in self.allocated_stocks)
        if not math.isclose(total_allocation, 1.0):
            raise ValueError("Total allocation must be equal to 1.0")

    def print_rebalance(self, rebalance_result) -> None:
        """Print the rebalance results."""
        print("Stocks to Sell:")
        for stock_name, shares in rebalance_result["sell"]:
            print(f"{stock_name}: {shares:.5f} shares")
        print("\nStocks to Buy:")
        for stock_name, shares in rebalance_result["buy"]:
            print(f"{stock_name}: {shares:.5f} shares")


def declare_example_case() -> Portfolio:
    """Declare an example case for the portfolio."""
    stock1 = Stock("AAPL")
    stock2 = Stock("GOOGL")
    stock3 = Stock("MSFT")
    stock4 = Stock("NVDA")
    holding1 = Holding(stock1, 78)
    holding2 = Holding(stock2, 298)
    holding3 = Holding(stock3, 150)
    allocated_stock1 = AllocatedStock(stock1, 0.65)
    allocated_stock2 = AllocatedStock(stock2, 0.25)
    allocated_stock3 = AllocatedStock(stock4, 0.1)

    return Portfolio(
        [holding1, holding2, holding3],
        [allocated_stock1, allocated_stock2, allocated_stock3],
    )


def main() -> None:
    # Example usage
    portfolio = declare_example_case()
    portfolio.check_total_allocation()
    rebalance_result = portfolio.rebalance()
    portfolio.print_rebalance(rebalance_result)


if __name__ == "__main__":
    main()
