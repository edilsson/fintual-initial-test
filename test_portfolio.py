import unittest

from portfolio import AllocatedStock, Holding, Portfolio, Stock, declare_example_case


class TestRebalance(unittest.TestCase):
    """Each test pins down one of the rebalance decisions documented in the README."""

    def setUp(self) -> None:
        # Example case: AAPL 27066 (25.04%), GOOGL 64666 (59.83%), MSFT 16350 (15.13%)
        # Total value: 108082. Target: AAPL 0.65, GOOGL 0.25, NVDA 0.1
        self.result = declare_example_case().rebalance()
        self.sell = dict(self.result["sell"])
        self.buy = dict(self.result["buy"])

    def test_underweight_stock_is_bought(self):
        # AAPL target: 0.65 * 108082 = 70253.3 -> buy (70253.3 - 27066) / 347
        self.assertNotIn("AAPL", self.sell)
        self.assertAlmostEqual(self.buy["AAPL"], (70253.3 - 27066) / 347)

    def test_overweight_stock_is_sold(self):
        # GOOGL target: 0.25 * 108082 = 27020.5 -> sell (64666 - 27020.5) / 217
        self.assertNotIn("GOOGL", self.buy)
        self.assertAlmostEqual(self.sell["GOOGL"], (64666 - 27020.5) / 217)

    def test_allocated_stock_not_held_is_bought_from_zero(self):
        # NVDA target: 0.1 * 108082 = 10808.2 -> buy 10808.2 / 1266
        self.assertNotIn("NVDA", self.sell)
        self.assertAlmostEqual(self.buy["NVDA"], 10808.2 / 1266)

    def test_held_stock_not_allocated_is_fully_liquidated(self):
        self.assertNotIn("MSFT", self.buy)
        self.assertEqual(self.sell["MSFT"], 150)

    def test_total_value_is_preserved(self):
        prices = {"AAPL": 347, "GOOGL": 217, "MSFT": 109, "NVDA": 1266}
        sold = sum(prices[name] * shares for name, shares in self.result["sell"])
        bought = sum(prices[name] * shares for name, shares in self.result["buy"])
        self.assertAlmostEqual(sold, bought)

    def test_balanced_portfolio_has_no_operations(self):
        # 217 AAPL * 347 == 347 GOOGL * 217, so a 50/50 target is already met
        aapl, googl = Stock("AAPL"), Stock("GOOGL")
        portfolio = Portfolio(
            [Holding(aapl, 217), Holding(googl, 347)],
            [AllocatedStock(aapl, 0.5), AllocatedStock(googl, 0.5)],
        )
        self.assertEqual(portfolio.rebalance(), {"sell": [], "buy": []})


class TestCheckTotalAllocation(unittest.TestCase):
    def test_allocation_summing_to_one_is_accepted(self):
        declare_example_case().check_total_allocation()

    def test_allocation_with_float_rounding_is_accepted(self):
        # 0.06 + 0.57 + 0.37 == 0.9999999999999999 in floating point
        aapl, googl, msft = Stock("AAPL"), Stock("GOOGL"), Stock("MSFT")
        portfolio = Portfolio(
            [Holding(aapl, 10)],
            [
                AllocatedStock(aapl, 0.06),
                AllocatedStock(googl, 0.57),
                AllocatedStock(msft, 0.37),
            ],
        )
        portfolio.check_total_allocation()

    def test_allocation_not_summing_to_one_is_rejected(self):
        aapl, googl = Stock("AAPL"), Stock("GOOGL")
        portfolio = Portfolio(
            [Holding(aapl, 10)],
            [AllocatedStock(aapl, 0.5), AllocatedStock(googl, 0.4)],
        )
        with self.assertRaises(ValueError):
            portfolio.check_total_allocation()


if __name__ == "__main__":
    unittest.main()
