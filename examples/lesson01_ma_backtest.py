"""Teaching example: close-of-day SMA target; next trading day's open fill.

Uses SYNTHETIC prices only. Deliberately omits dividends, tick sizes, lot-size
restrictions, liquidity, limit-up/down, delistings and Taiwan-specific tax rules.
Do not use as a live trading or production-grade backtest engine.
"""
from __future__ import annotations

import csv
from dataclasses import dataclass
from datetime import date
from math import floor
from pathlib import Path


@dataclass(frozen=True)
class Bar:
    day: date
    open: float
    high: float
    low: float
    close: float
    volume: int


@dataclass(frozen=True)
class Fill:
    signal_day: date
    fill_day: date
    side: str
    quantity: int
    price: float
    fees_and_tax: float


@dataclass(frozen=True)
class BacktestResult:
    curve: list[tuple[date, float]]
    fills: list[Fill]
    ending_cash: float
    ending_shares: int
    latest_target: bool | None  # True=invested, False=flat, None=not enough history


def read_bars(path: str | Path) -> list[Bar]:
    """Read strict, ordered OHLCV CSV. Reject invalid data rather than guess."""
    bars: list[Bar] = []
    with Path(path).open(encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream)
        if not {"date", "open", "high", "low", "close", "volume"} <= set(reader.fieldnames or []):
            raise ValueError("CSV needs date,open,high,low,close,volume")
        for row in reader:
            try:
                bar = Bar(
                    day=date.fromisoformat(row["date"]),
                    open=float(row["open"]),
                    high=float(row["high"]),
                    low=float(row["low"]),
                    close=float(row["close"]),
                    volume=int(row["volume"]),
                )
            except (ValueError, TypeError, KeyError) as exc:
                raise ValueError(f"Malformed bar at CSV row {reader.line_num}") from exc
            from math import isfinite
            if not all(isfinite(v) and v > 0 for v in (bar.open, bar.high, bar.low, bar.close)):
                raise ValueError(f"Invalid price at {bar.day}")
            if bar.volume < 0 or bar.high < max(bar.open, bar.close) or bar.low > min(bar.open, bar.close) or bar.low > bar.high:
                raise ValueError(f"Invalid OHLCV at {bar.day}")
            if bars and bar.day <= bars[-1].day:
                raise ValueError("Duplicate or unordered dates")
            bars.append(bar)
    if not bars:
        raise ValueError("Empty bars")
    return bars


def sma_targets(bars: list[Bar], *, fast: int = 3, slow: int = 5) -> list[bool | None]:
    """End-of-day target using only that day and earlier closing prices."""
    if not isinstance(fast, int) or not isinstance(slow, int) or not (1 <= fast < slow):
        raise ValueError("Require 1 <= fast < slow")
    closes = [bar.close for bar in bars]
    result: list[bool | None] = []
    for i in range(len(closes)):
        if i + 1 < slow:
            result.append(None)
            continue
        f = sum(closes[i + 1 - fast:i + 1]) / fast
        s = sum(closes[i + 1 - slow:i + 1]) / slow
        result.append(f > s)
    return result


def backtest(
    bars: list[Bar], *, fast: int = 3, slow: int = 5,
    initial_cash: float = 10_000.0, commission_rate: float = 0.001,
    sell_tax_rate: float = 0.003, slippage_rate: float = 0.001,
) -> BacktestResult:
    """Long-only toy backtest: signal at T close, transaction at T+1 open."""
    from math import isfinite
    if not isfinite(initial_cash) or initial_cash <= 0:
        raise ValueError("initial_cash must be positive")
    if any(not isfinite(x) or x < 0 or x >= 1 for x in (commission_rate, sell_tax_rate, slippage_rate)):
        raise ValueError("Invalid cost assumptions")
    if not bars or any(bars[i].day <= bars[i - 1].day for i in range(1, len(bars))):
        raise ValueError("Bars must be nonempty and ordered")
    targets = sma_targets(bars, fast=fast, slow=slow)
    cash, shares = initial_cash, 0
    curve: list[tuple[date, float]] = []
    fills: list[Fill] = []
    for i, bar in enumerate(bars):
        # IMPORTANT: desired position comes only from yesterday's finished bar.
        target = targets[i - 1] if i else None
        if target is True and shares == 0:
            price = bar.open * (1 + slippage_rate)
            qty = floor(cash / (price * (1 + commission_rate)))
            if qty > 0:
                fee = qty * price * commission_rate
                cash -= qty * price + fee
                shares += qty
                fills.append(Fill(bars[i - 1].day, bar.day, "BUY", qty, price, fee))
        elif target is False and shares > 0:
            price = bar.open * (1 - slippage_rate)
            fee = shares * price * (commission_rate + sell_tax_rate)
            cash += shares * price - fee
            fills.append(Fill(bars[i - 1].day, bar.day, "SELL", shares, price, fee))
            shares = 0
        curve.append((bar.day, cash + shares * bar.close))
    return BacktestResult(curve, fills, cash, shares, targets[-1])


def max_drawdown(curve: list[tuple[date, float]]) -> float:
    if not curve:
        raise ValueError("Empty curve")
    peak = curve[0][1]
    worst = 0.0
    for _, value in curve:
        peak = max(peak, value)
        worst = min(worst, value / peak - 1)
    return worst


if __name__ == "__main__":
    path = Path(__file__).parent / "data" / "toy_bars.csv"
    result = backtest(read_bars(path))
    print("SYNTHETIC STUDY ONLY — not live Taiwan market data")
    for fill in result.fills:
        print(f"{fill.signal_day} signal -> {fill.fill_day} {fill.side} {fill.quantity} @ {fill.price:.2f}")
    print(f"Ending equity: {result.curve[-1][1]:.2f}")
    print(f"Max drawdown (sample only): {max_drawdown(result.curve):.2%}")
    print(f"Last close target (not filled): {result.latest_target}")
