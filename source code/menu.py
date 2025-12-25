"""
menu.py (Role B)

Menu/UI orchestration for the Stock Portfolio Tracker project.

Responsibilities:
- Display numbered menu options (proposal requirement)
- Collect and validate user input
- Coordinate calls to other modules via the shared contracts
- Print user-facing output (UI only)
"""

from __future__ import annotations

from typing import Callable, Dict, Optional, Tuple

import data_io
import transactions
import analysis
import visualization

TEST_MODE = True  # set to False when integrating with data_io

# Optional config defaults (fallback to common filenames if config.py not ready yet)
try:
    import config  # type: ignore

    DEFAULT_STOCKS_CSV: str = getattr(config, "DEFAULT_STOCKS_CSV", "stocks.csv")
    DEFAULT_PORTFOLIO_CSV: str = getattr(config, "DEFAULT_PORTFOLIO_CSV", "portfolio.csv")
except Exception:
    DEFAULT_STOCKS_CSV = "stocks.csv"
    DEFAULT_PORTFOLIO_CSV = "portfolio.csv"


StocksDict = Dict[str, Dict[str, float]]
PortfolioDict = Dict[str, int]


def _prompt_nonempty(prompt: str) -> str:
    """Prompt until user enters a non-empty string."""
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Input cannot be empty. Please try again.")


def _prompt_int(prompt: str, *, min_value: Optional[int] = None) -> int:
    """Prompt until user enters a valid integer (optionally with a minimum)."""
    while True:
        raw = input(prompt).strip()
        try:
            value = int(raw)
        except ValueError:
            print("Please enter a whole number (integer).")
            continue

        if min_value is not None and value < min_value:
            print(f"Please enter a value >= {min_value}.")
            continue

        return value


def _prompt_path(prompt: str, default_path: str) -> str:
    """Prompt for a file path; return default if user presses Enter."""
    raw = input(f"{prompt} (Enter for default: {default_path}): ").strip()
    return raw if raw else default_path


def _prompt_symbol(stocks: StocksDict) -> str:
    """Prompt for a stock ticker symbol, normalized to uppercase."""
    symbol = _prompt_nonempty("Enter stock symbol (e.g., AAPL): ").upper()
    if symbol not in stocks:
        # We still return it (transactions may handle), but give immediate feedback.
        print(f"Warning: '{symbol}' not found in available stocks.")
    return symbol


def _print_portfolio_summary(portfolio: PortfolioDict) -> None:
    """UI helper: print a short summary of current holdings."""
    if not portfolio:
        print("Portfolio is currently empty.")
        return
    print("Current portfolio holdings:")
    for symbol, qty in sorted(portfolio.items()):
        print(f"  - {symbol}: {qty}")


def _safe_call(action_name: str, fn: Callable[[], None]) -> None:
    """
    Run a menu action with basic error handling to prevent the loop from crashing.
    This is UI-level only; modules should raise exceptions or return normal values.
    """
    try:
        fn()
    except Exception as exc:
        print(f"[{action_name}] Error: {exc}")


def main_menu_loop() -> None:
    """
    Main CLI loop with numbered options:
    view stocks, buy, sell, value, ROI, pie chart, save, load, exit.

    Loads stocks on startup from a CSV (proposal requirement).
    """
    print("=== Stock Portfolio Tracker ===")

    # Load stocks once at startup (proposal).
    if TEST_MODE:
        stocks: StocksDict = {
            "AAPL": {"initial_price": 150.0, "current_price": 165.0},
            "MSFT": {"initial_price": 300.0, "current_price": 310.0},
            "TSLA": {"initial_price": 200.0, "current_price": 190.0},
        }
        print("TEST_MODE: using hardcoded stocks (no CSV loaded).")
    else:
        stocks_csv = _prompt_path("Stock prices CSV path", DEFAULT_STOCKS_CSV)
        try:
            stocks = data_io.load_stocks(stocks_csv)
        except Exception as exc:
            print(f"Failed to load stocks from '{stocks_csv}': {exc}")
            print("Exiting program.")
            return

    portfolio: PortfolioDict = {}

    menu_options: Tuple[Tuple[str, str], ...] = (
        ("1", "View available stocks"),
        ("2", "Buy shares"),
        ("3", "Sell shares"),
        ("4", "Check portfolio value"),
        ("5", "Show ROI (%)"),
        ("6", "Pie chart allocation"),
        ("7", "Save portfolio"),
        ("8", "Load portfolio"),
        ("9", "Exit"),
    )

    while True:
        print("\n--- Main Menu ---")
        for key, label in menu_options:
            print(f"{key}) {label}")

        choice = input("Choose an option (1-9): ").strip()

        if choice == "1":
            def action() -> None:
                table = data_io.format_stock_table(stocks)
                print(table)

            _safe_call("View stocks", action)

        elif choice == "2":
            def action() -> None:
                symbol = _prompt_symbol(stocks)
                qty = _prompt_int("Quantity to buy: ", min_value=1)
                updated = transactions.buy(portfolio, stocks, symbol, qty)
                portfolio.clear()
                portfolio.update(updated)
                print(f"Bought {qty} shares of {symbol}.")
                _print_portfolio_summary(portfolio)

            _safe_call("Buy", action)

        elif choice == "3":
            def action() -> None:
                symbol = _prompt_symbol(stocks)
                qty = _prompt_int("Quantity to sell: ", min_value=1)
                updated = transactions.sell(portfolio, stocks, symbol, qty)
                portfolio.clear()
                portfolio.update(updated)
                print(f"Sold {qty} shares of {symbol}.")
                _print_portfolio_summary(portfolio)

            _safe_call("Sell", action)

        elif choice == "4":
            def action() -> None:
                value = analysis.portfolio_value(portfolio, stocks, price_key="current_price")
                print(f"Current portfolio value: {value:.2f}")

            _safe_call("Portfolio value", action)

        elif choice == "5":
            def action() -> None:
                roi = analysis.roi_percent(portfolio, stocks)
                print(f"ROI: {roi:.2f}%")

            _safe_call("ROI", action)

        elif choice == "6":
            def action() -> None:
                if not portfolio:
                    print("Portfolio is empty. Buy shares or load a portfolio first.")
                    return
                visualization.plot_allocation_pie(portfolio, stocks)

            _safe_call("Pie chart", action)

        elif choice == "7":
            def action() -> None:
                path = _prompt_path("Save portfolio CSV path", DEFAULT_PORTFOLIO_CSV)
                data_io.save_portfolio(path, portfolio)
                print(f"Portfolio saved to '{path}'.")

            _safe_call("Save portfolio", action)

        elif choice == "8":
            def action() -> None:
                path = _prompt_path("Load portfolio CSV path", DEFAULT_PORTFOLIO_CSV)
                loaded = data_io.load_portfolio(path)
                portfolio.clear()
                portfolio.update(loaded)
                print(f"Portfolio loaded from '{path}'.")
                _print_portfolio_summary(portfolio)

            _safe_call("Load portfolio", action)

        elif choice == "9":
            print("Goodbye.")
            break

        else:
            print("Invalid choice. Please enter a number from 1 to 9.")


if __name__ == "__main__":
    main_menu_loop()
