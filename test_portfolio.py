import unittest
from Portfolio import Portfolio
"""
Before running test make sure all "_portfolio.txt" files are empty or deleted.
"""
class TestPortfolio(unittest.TestCase):

    def test_get_file_path(self):
        p1 = Portfolio(first_name="John", last_name="Doe")
        p2 = Portfolio(first_name="Susan", last_name="Smith")

        self.assertEqual(p1.get_file_path(), "JohnDoe_portfolio.txt")
        self.assertEqual(p2.get_file_path(), "SusanSmith_portfolio.txt")

    def test_get_stock_avg(self):
        p1 = Portfolio(first_name="Julin", last_name="Patel")
        p1.add_stock("APPL", 1, 170)
        p1.add_stock("SPY", 2, 270)

        self.assertEqual(p1.stock_tick_avg, {"APPL": 170, "SPY": 270})

    def test_get_stock_opt(self):
        p1 = Portfolio(first_name="Julin", last_name="Patel")
        p1.add_stock("APPL", 1, 170)
        p1.add_stock("SPY", 2, 270)

        self.assertIsNotNone(p1.get_stock_opt())

    def test_get_first_name(self):
        p1 = Portfolio(first_name="John", last_name="Doe")
        p2 = Portfolio(first_name="Susan", last_name="Smith")

        self.assertEqual(p1.get_first_name(), "John")
        self.assertEqual(p2.get_first_name(), "Susan")

    def test_get_last_name(self):
        p1 = Portfolio(first_name="John", last_name="Doe")
        p2 = Portfolio(first_name="Susan", last_name="Smith")

        self.assertEqual(p1.get_last_name(), "Doe")
        self.assertEqual(p2.get_last_name(), "Smith")

    def test_add_stock(self):
        p1 = Portfolio(first_name="Julin", last_name="Patel")
        p1.add_stock("APPL", 1, 170)
        p1.add_stock("SPY", 2, 270)

        self.assertEqual(p1.stock_tick_opt,{"APPL": 1, "SPY": 2})
        self.assertEqual(p1.stock_tick_avg, {"APPL": 170, "SPY": 270})

    # If Robinhood Account is not logged in it will return 401 Error. Test will still run successfully
    def test_sell_stock(self):
        p5 = Portfolio(first_name="James", last_name="Doland")
        p5.add_stock("T", 1, 170)
        p5.add_stock("SPHD", 2, 270)

        p5.sell_stock("SPHD", 1)

        self.assertEqual(p5.stock_tick_opt, {"T": 1.0, "SPHD": 1.0})
        self.assertEqual(p5.stock_tick_avg, {"T": 170.0, "SPHD": 270.0})


if __name__ == '__main__':
    unittest.main()
