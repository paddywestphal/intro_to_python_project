"""
This module produces a pie chart showing each stock's share of the total portfolio value.
"""

from __future__ import annotations

from typing import Dict

import matplotlib.pyplot as plt


def _validate_inputs(portfolio: Dict[str, int], stocks: Dict[str, Dict[str, float]]) -> None:

    if not isinstance(portfolio, dict):
        raise TypeError("portfolio must be a dict like {'AAPL': 3, 'MSFT': 1}")
    if not isinstance(stocks, dict):
        raise TypeError("stocks must be a dict like {'AAPL': {'initial_price': 150.0, 'current_price': 165.0}}")

    for symbol, qty in portfolio.items():
        if not isinstance(symbol, str):
            raise TypeError("portfolio keys (symbols) must be strings.")
        if not isinstance(qty, int):
            raise TypeError(f"portfolio quantity for {symbol} must be int, got {type(qty).__name__}.")
        if qty <= 0:
            raise ValueError(f"portfolio must only contain tickers with qty > 0. Found {symbol}: {qty}.")

    for symbol, price_info in stocks.items():
        if not isinstance(symbol, str):
            raise TypeError("stocks keys (symbols) must be strings.")
        if not isinstance(price_info, dict):
            raise TypeError(f"stocks[{symbol}] must be a dict.")


def _get_current_price(stocks: Dict[str, Dict[str, float]], symbol: str) -> float:

    if symbol not in stocks:
        raise KeyError(f"Unknown stock symbol '{symbol}' (not found in stocks data).")

    info = stocks[symbol]
    if "current_price" not in info:
        raise KeyError(f"Missing 'current_price' for symbol '{symbol}' in stocks data.")

    price = info["current_price"]
    if not isinstance(price, (int, float)):
        raise TypeError(f"Price for {symbol}.current_price must be a number, got {type(price).__name__}.")
    if price < 0:
        raise ValueError(f"Price for {symbol}.current_price cannot be negative (got {price}).")

    return float(price)


def plot_allocation_pie(portfolio: Dict[str, int], stocks: Dict[str, Dict[str, float]]) -> None:
    """
    Plot a pie chart showing how the portfolio's total *current value* is allocated across stocks.
    - Create a pie chart that shows what share of total portfolio value comes from each stock.
    - Use matplotlib.
    - It can simply display the chart (plt.show()).
    """
    _validate_inputs(portfolio, stocks)

    if not portfolio:
        # If portfolio is empty, there is nothing to plot.
        # Raising an error is clearer than showing an empty chart.
        raise ValueError("Cannot plot allocation: portfolio is empty.")

    labels = []
    values = []

    # Build data for the pie chart: value_per_stock = quantity * current_price
    for symbol, qty in portfolio.items():
        current_price = _get_current_price(stocks, symbol)
        labels.append(symbol)
        values.append(qty * current_price)

    total_value = sum(values)
    if total_value <= 0:
        raise ValueError("Cannot plot allocation: total portfolio value is zero or negative.")

    # Plot
    plt.figure()  # create a new figure, so plots don't overlap in interactive sessions
    plt.pie(values, labels=labels, autopct="%1.1f%%")
    plt.title("Portfolio Allocation (by Current Value)")
    plt.axis("equal")  # makes the pie chart a circle
    plt.show()
