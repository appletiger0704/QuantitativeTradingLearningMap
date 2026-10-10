"""Tests for the toy backtest. Run: python -m unittest discover -s examples -v"""
import csv
import tempfile
import unittest
from pathlib import Path

from lesson01_ma_backtest import backtest, max_drawdown, read_bars, sma_targets


DATA = Path(__file__).parent / "data" / "toy_bars.csv"


class TeachingExampleTests(unittest.TestCase):
    def setUp(self):
        self.bars = read_bars(DATA)

    def test_expected_buy_and_sell_execute_next_day(self):
        result = backtest(self.bars, slippage_rate=0, commission_rate=0, sell_tax_rate=0)
        self.assertEqual([x.side for x in result.fills], ["BUY", "SELL"])
        buy, sell = result.fills
        self.assertEqual((buy.signal_day.isoformat(), buy.fill_day.isoformat()), ("2026-01-12", "2026-01-13"))
        self.assertEqual((sell.signal_day.isoformat(), sell.fill_day.isoformat()), ("2026-01-19", "2026-01-20"))
        self.assertEqual((buy.price, sell.price), (12.0, 8.0))
        self.assertEqual(result.ending_shares, 0)

    def test_no_future_leakage_in_targets(self):
        self.assertEqual(sma_targets(self.bars[:-1]), sma_targets(self.bars)[:-1])

    def test_last_bar_signal_cannot_trade_at_last_bar_close(self):
        limited = self.bars[:6]  # first bullish signal occurs on final day's close
        result = backtest(limited)
        self.assertTrue(result.latest_target)
        self.assertEqual(result.fills, [])

    def test_transaction_costs_reduce_equity(self):
        clean = backtest(self.bars, commission_rate=0, sell_tax_rate=0, slippage_rate=0)
        charged = backtest(self.bars, commission_rate=0.001, sell_tax_rate=0.003, slippage_rate=0.001)
        self.assertLess(charged.curve[-1][1], clean.curve[-1][1])
        self.assertGreaterEqual(charged.ending_cash, 0)
        self.assertTrue(all(x.fees_and_tax >= 0 for x in charged.fills))

    def test_invalid_data_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "bad.csv"
            with DATA.open(encoding="utf-8", newline="") as f:
                rows = list(csv.DictReader(f))
            with path.open("w", encoding="utf-8", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=rows[0].keys())
                writer.writeheader()
                writer.writerows(rows + [rows[-1]])  # duplicate trading day
            with self.assertRaisesRegex(ValueError, "Duplicate"):
                read_bars(path)

    def test_invalid_parameters_rejected(self):
        with self.assertRaises(ValueError):
            sma_targets(self.bars, fast=5, slow=3)
        with self.assertRaises(ValueError):
            backtest(self.bars, initial_cash=0)
        with self.assertRaises(ValueError):
            backtest(self.bars, sell_tax_rate=-0.1)

    def test_max_drawdown(self):
        self.assertAlmostEqual(max_drawdown([(self.bars[0].day, 100), (self.bars[1].day, 80)]), -0.2)


if __name__ == "__main__":
    unittest.main()
