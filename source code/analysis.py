"""
Role D (Analysis):
- portfolio_value/ portfolio_cost_basis/ roi_percent

Shared contracts:
- stocks: {"AAPL": {"initial_price": 150.0, "current_price": 165.0}, ...}
- portfolio: {"AAPL": 3, "MSFT": 1, ...}  # only tickers with qty > 0
"""

from __future__ import annotations

from typing import Dict


def _validate_inputs(portfolio: Dict[str, int], stocks: Dict[str, Dict[str, float]]) -> None:
    """
        Internal helper: validate that portfolio and stocks roughly match the agreed data shapes.
  """
    if not isinstance(portfolio, dict):
        raise TypeError("portfolio must be a dict like {'AAPL': 3, 'MSFT': 1}")
    if not isinstance(stocks, dict):
        raise TypeError("stocks must be a dict like {'AAPL': {'initial_price': 150.0, 'current_price': 165.0}}")

    # Check portfolio quantities are integers and positive (per contract: only tickers with qty > 0)
    for symbol, qty in portfolio.items():
        if not isinstance(symbol, str):
            raise TypeError("portfolio keys (symbols) must be strings.")
        if not isinstance(qty, int):
            raise TypeError(f"portfolio quantity for {symbol} must be int, got {type(qty).__name__}.")
        if qty <= 0:
            raise ValueError(f"portfolio must only contain tickers with qty > 0. Found {symbol}: {qty}.")

    # Check stock entries shape
    for symbol, price_info in stocks.items():
        if not isinstance(symbol, str):
            raise TypeError("stocks keys (symbols) must be strings.")
        if not isinstance(price_info, dict):
            raise TypeError(
                f"stocks[{symbol}] must be a dict like {{'initial_price': ..., 'current_price': ...}}."
            )


def _get_price(
    stocks: Dict[str, Dict[str, float]],
    symbol: str,
    price_key: str
) -> float:
    if symbol not in stocks:
        raise KeyError(f"Unknown stock symbol '{symbol}' (not found in stocks data).")

    price_info = stocks[symbol]
    if price_key not in price_info:
        raise KeyError(f"Missing '{price_key}' for symbol '{symbol}' in stocks data.")

    price = price_info[price_key]     # We allow int/float, but store as float for calculations
    if not isinstance(price, (int, float)):
        raise TypeError(f"Price for {symbol}.{price_key} must be a number, got {type(price).__name__}.")
    if price < 0:
        raise ValueError(f"Price for {symbol}.{price_key} cannot be negative (got {price}).")

    return float(price)

#  Calculate total portfolio value using a chosen price field.
def portfolio_value(
    portfolio: Dict[str, int],
    stocks: Dict[str, Dict[str, float]],
    price_key: str = "current_price",
) -> float:
    _validate_inputs(portfolio, stocks)

    total = 0.0
    # We loop through each holding in the portfolio:
    # symbol = "AAPL", qty = 3
    for symbol, qty in portfolio.items():
        price = _get_price(stocks, symbol, price_key)
        total += qty * price

    return total

    # Calculate the initial investment (cost basis) of the portfolio.

def portfolio_cost_basis(
    portfolio: Dict[str, int],
    stocks: Dict[str, Dict[str, float]],
    price_key: str = "initial_price",
) -> float:
    return portfolio_value(portfolio, stocks, price_key=price_key)


def roi_percent(
    portfolio: Dict[str, int],
    stocks: Dict[str, Dict[str, float]]
) -> float:
    """
        Calculate ROI (Return on Investment) in percent.
        -------
        float
            ROI percentage.
        Edge cases
        ----------
        - If initial investment is 0, ROI is not defined.
          We raise ZeroDivisionError to make the issue explicit.
        """
    _validate_inputs(portfolio, stocks)

    # Optional UX improvement for menu option "ROI" (choice 5)
    if not portfolio:
        raise ValueError("Portfolio is empty. Buy shares or load a portfolio first.")

    current_val = portfolio_value(portfolio, stocks, price_key="current_price")
    initial_val = portfolio_cost_basis(portfolio, stocks, price_key="initial_price")

    return (current_val - initial_val) / initial_val * 100.0
