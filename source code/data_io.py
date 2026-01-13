# Role A: Fabian Data

import csv


def load_stocks(path: str) -> dict:
    """
    Load stock data from a CSV file.

    Expected CSV header:
    symbol, initial_price, current_price

    Returns:
        dict like:
        {
          "AAPL": {"initial_price": 150.0, "current_price": 165.0},
          ...
        }
    """
    stocks = {}

    with open(path, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        # Basic header check
        required = ["symbol", "initial_price", "current_price"]
        for col in required:
            if col not in reader.fieldnames:
                raise ValueError(f"Stocks CSV is missing column '{col}'. Expected: {required}")

        for row in reader:
            symbol = row["symbol"].strip().upper()
            if not symbol:
                continue

            try:
                initial_price = float(row["initial_price"])
                current_price = float(row["current_price"])
            except ValueError:
                raise ValueError(f"Invalid price value for symbol '{symbol}' (must be a number).")

            if initial_price < 0 or current_price < 0:
                raise ValueError(f"Prices cannot be negative for symbol '{symbol}'.")

            stocks[symbol] = {
                "initial_price": initial_price,
                "current_price": current_price
            }

    if not stocks:
        raise ValueError("No stocks loaded. The CSV may be empty.")

    return stocks


def save_portfolio(path: str, portfolio: dict) -> None:
    """
    Save portfolio to CSV with header: symbol, shares
    portfolio example: {"AAPL": 2, "MSFT": 1}
    """
    with open(path, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["symbol", "shares"])

        for symbol, shares in portfolio.items():
            writer.writerow([symbol, shares])


def load_portfolio(path: str) -> dict:
    """
    Load portfolio from CSV with header: symbol, shares
    Returns dict like: {"AAPL": 2, "MSFT": 1}
    """
    portfolio = {}

    with open(path, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        required = ["symbol", "shares"]
        for col in required:
            if col not in reader.fieldnames:
                raise ValueError(f"Portfolio CSV is missing column '{col}'. Expected: {required}")

        for row in reader:
            symbol = row["symbol"].strip().upper()
            if not symbol:
                continue

            try:
                shares = int(row["shares"])
            except ValueError:
                raise ValueError(f"Invalid shares value for symbol '{symbol}' (must be a whole number).")

            # Contract in analysis/visualization: only keep qty > 0
            if shares > 0:
                portfolio[symbol] = shares

    return portfolio


def format_stock_table(stocks: dict) -> str:
    """
    Return a printable table string for the 'View stocks' menu option.
    """
    if not stocks:
        return "No stocks available."

    lines = []
    lines.append("Available Stocks")
    lines.append("-" * 45)
    lines.append(f"{'SYMBOL':<10}{'INITIAL':>12}{'CURRENT':>12}")
    lines.append("-" * 45)

    for symbol in sorted(stocks.keys()):
        initial_p = stocks[symbol]["initial_price"]
        current_p = stocks[symbol]["current_price"]
        lines.append(f"{symbol:<10}{initial_p:>12.2f}{current_p:>12.2f}")

    lines.append("-" * 45)
    return "\n".join(lines)