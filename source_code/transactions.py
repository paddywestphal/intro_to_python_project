"""
Module: transactions.py
Role: C (Transactions Logic)
Author: Simon
Description: Handles buying and selling logic, updates the portfolio dictionary,
             and ensures validation (e.g., checking for sufficient funds/shares).
"""

def buy(portfolio: dict, stocks: dict, symbol: str, qty: int) -> dict:
    """
    Adds a specific quantity of shares to the portfolio.

    Args:
        portfolio (dict): The current portfolio holdings (e.g., {"AAPL": 5}).
        stocks (dict): The list of all available stocks (for validation).
        symbol (str): The stock ticker symbol (e.g., "AAPL").
        qty (int): The quantity to buy.

    Returns:
        dict: The updated portfolio.

    Raises:
        ValueError: If the symbol is invalid or quantity is <= 0.
    """
    # 1. Validation: Is the quantity positive?
    if qty <= 0:
        raise ValueError("Quantity must be greater than 0.")

    # 2. Validation: Does the stock exist in our database?
    if symbol not in stocks:
        raise ValueError(f"Stock '{symbol}' not found in database.")

    # 3. Logic: Add stock or create new entry
    # .get(symbol, 0) retrieves the current value or 0 if it doesn't exist yet.
    current_qty = portfolio.get(symbol, 0)
    portfolio[symbol] = current_qty + qty

    return portfolio


def sell(portfolio: dict, stocks: dict, symbol: str, qty: int) -> dict:
    """
    Removes a specific quantity of shares from the portfolio.

    Args:
        portfolio (dict): The current portfolio holdings.
        stocks (dict): The list of all available stocks (kept for interface consistency).
        symbol (str): The stock ticker symbol.
        qty (int): The quantity to sell.

    Returns:
        dict: The updated portfolio.

    Raises:
        ValueError: If quantity <= 0, symbol not owned, or insufficient shares.
    """
    # 1. Validation: Is the quantity positive?
    if qty <= 0:
        raise ValueError("Quantity must be greater than 0.")

    # 2. Validation: Does the user own this stock?
    if symbol not in portfolio:
        raise ValueError(f"You do not own any shares of '{symbol}'.")

    # 3. Validation: Does the user have ENOUGH shares to sell?
    if portfolio[symbol] < qty:
        raise ValueError(f"Insufficient shares. You have {portfolio[symbol]}, but tried to sell {qty}.")

    # 4. Logic: Deduct shares
    portfolio[symbol] -= qty

    # 5. Cleanup: If quantity reaches 0, remove the entry completely
    if portfolio[symbol] == 0:
        del portfolio[symbol]

    return portfolio