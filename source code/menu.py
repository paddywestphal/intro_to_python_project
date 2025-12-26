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

from typing import Callable, Dict, Optional, Tuple, Sequence, Set, Type, TypeVar, Union

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

#Helpers: Input validation. These helpers are UI-level utilities to validate user input.
#They do not perform business logic (buy/sell/value), only input checking.
T = TypeVar("T", int, str)


def prompt_choice(valid_choices: Sequence[T], prompt: str = "Choose an option: ") -> T:
    """
    Prompt user until they enter a value in valid_choices.
    Return type matches the type of items in valid_choices (str or int).
    """
    if not valid_choices:
        raise ValueError("valid_choices must not be empty.")

    expected_type: Type[T] = type(valid_choices[0])  # infer int vs str
    choice_set: Set[T] = set(valid_choices)

    while True:
        raw = input(prompt).strip()

        try:
            if expected_type is int:
                value: Union[int, str] = int(raw)
            else:
                value = raw
        except ValueError:
            print("Invalid input type. Please try again.")
            continue

        if value in choice_set:
            return value  # type: ignore[return-value]

        allowed = ", ".join(str(c) for c in valid_choices)
        print(f"Invalid choice. Allowed: {allowed}")


def prompt_symbol(stocks: dict, prompt: str = "Enter stock symbol (e.g., AAPL): ") -> str:
    """
    Prompt for a ticker symbol until it exists in the stocks dict.
    Returns the validated symbol (uppercase).
    """
    if not isinstance(stocks, dict) or not stocks:
        raise ValueError("stocks must be a non-empty dictionary of available tickers.")

    while True:
        symbol = input(prompt).strip().upper()
        if not symbol:
            print("Symbol cannot be empty.")
            continue
        if symbol not in stocks:
            print(f"Unknown symbol '{symbol}'. Please choose one that exists in the stocks list.")
            continue
        return symbol


def prompt_positive_int(prompt: str = "Enter a positive whole number: ") -> int:
    """
    Prompt until the user enters a positive integer (>= 1).
    """
    while True:
        raw = input(prompt).strip()
        try:
            value = int(raw)
        except ValueError:
            print("Please enter a whole number (integer).")
            continue

        if value < 1:
            print("Please enter a number >= 1.")
            continue

        return value


def _prompt_nonempty(prompt: str) -> str:
    """Prompt until user enters a non-empty string."""
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Input cannot be empty. Please try again.")


def _prompt_path(prompt: str, default_path: str) -> str:
    """Prompt for a file path; return default if user presses Enter."""
    raw = input(f"{prompt} (Enter for default: {default_path}): ").strip()
    return raw if raw else default_path


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

    Loads stocks on startup from a CSV.
    """
    print("=== Stock Portfolio Tracker ===")

    # Load stocks once at startup.
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

        choice = prompt_choice(
            ["1", "2", "3", "4", "5", "6", "7", "8", "9"],
            "Choose an option (1-9): "
        )

        if choice == "1":
            def action() -> None:
                table = data_io.format_stock_table(stocks)
                print(table)

            _safe_call("View stocks", action)

        elif choice == "2":
            def action() -> None:
                symbol = prompt_symbol(stocks)
                qty = prompt_positive_int("Quantity to buy: ")
                updated = transactions.buy(portfolio, stocks, symbol, qty)
                portfolio.clear()
                portfolio.update(updated)
                print(f"Bought {qty} shares of {symbol}.")
                _print_portfolio_summary(portfolio)

            _safe_call("Buy", action)

        elif choice == "3":
            def action() -> None:
                symbol = prompt_symbol(stocks)
                qty = prompt_positive_int("Quantity to sell: ")
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



if __name__ == "__main__":
    main_menu_loop()
