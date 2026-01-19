"""
Streamlit app for the Stock Portfolio Tracker.
"""
from __future__ import annotations

from pathlib import Path
from typing import Dict, List

import streamlit as st

import sys

REPO_ROOT = Path(__file__).resolve().parent
SOURCE_DIR = REPO_ROOT / "source_code"
if str(SOURCE_DIR) not in sys.path:
    sys.path.append(str(SOURCE_DIR))

import analysis  # noqa: E402
import data_io  # noqa: E402
import transactions  # noqa: E402
import visualization  # noqa: E402

StocksDict = Dict[str, Dict[str, float]]
PortfolioDict = Dict[str, int]

DEFAULT_STOCKS_PATH = REPO_ROOT / "data" / "stocks.csv"
DEFAULT_PORTFOLIO_PATH = REPO_ROOT / "data" / "portfolio.csv"


st.set_page_config(page_title="Stock Portfolio Tracker", layout="centered")


if "prices" not in st.session_state:
    st.session_state.prices = {}
if "portfolio" not in st.session_state:
    st.session_state.portfolio = {}


def _format_portfolio_table(portfolio: PortfolioDict) -> List[Dict[str, int]]:
    rows = []
    for symbol, qty in sorted(portfolio.items()):
        rows.append({"Symbol": symbol, "Shares": qty})
    return rows


def _format_stock_table(stocks: StocksDict) -> List[Dict[str, float]]:
    rows = []
    for symbol in sorted(stocks.keys()):
        rows.append(
            {
                "Symbol": symbol,
                "Initial Price": stocks[symbol]["initial_price"],
                "Current Price": stocks[symbol]["current_price"],
            }
        )
    return rows


st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Go to",
    (
        "Load data",
        "Trade",
        "Portfolio",
        "Analysis",
        "Visualization",
        "Save/Load portfolio",
    ),
)

st.title("Stock Portfolio Tracker")

if page == "Load data":
    st.header("Load stock prices")
    default_path = str(DEFAULT_STOCKS_PATH)
    path = st.text_input("Stocks CSV path", value=default_path)

    if st.button("Load stocks"):
        try:
            st.session_state.prices = data_io.load_stocks(path)
            st.success("Stocks loaded successfully.")
        except Exception as exc:
            st.error(f"Failed to load stocks: {exc}")

    if st.session_state.prices:
        st.subheader("Available Stocks")
        st.table(_format_stock_table(st.session_state.prices))
    else:
        st.info("No stocks loaded yet.")

elif page == "Trade":
    st.header("Buy or sell shares")

    prices: StocksDict = st.session_state.prices
    portfolio: PortfolioDict = st.session_state.portfolio

    if not prices:
        st.warning("Load stock prices first.")
    else:
        trade_action = st.radio("Action", ("Buy", "Sell"))
        symbol = st.selectbox("Symbol", sorted(prices.keys()))
        qty = st.number_input("Quantity", min_value=1, step=1, value=1)

        if st.button("Submit trade"):
            try:
                if trade_action == "Buy":
                    transactions.buy(portfolio, prices, symbol, int(qty))
                    st.success(f"Bought {qty} shares of {symbol}.")
                else:
                    transactions.sell(portfolio, prices, symbol, int(qty))
                    st.success(f"Sold {qty} shares of {symbol}.")
            except Exception as exc:
                st.error(f"Trade failed: {exc}")

        if portfolio:
            st.subheader("Current holdings")
            st.table(_format_portfolio_table(portfolio))
        else:
            st.info("Portfolio is empty.")

elif page == "Portfolio":
    st.header("Portfolio summary")

    prices: StocksDict = st.session_state.prices
    portfolio: PortfolioDict = st.session_state.portfolio

    if not portfolio:
        st.info("Portfolio is empty.")
    else:
        st.table(_format_portfolio_table(portfolio))

        if prices:
            try:
                value = analysis.portfolio_value(portfolio, prices)
                st.metric("Total Value", f"{value:.2f}")
            except Exception as exc:
                st.error(f"Could not calculate value: {exc}")
        else:
            st.warning("Load stock prices to see portfolio value.")

elif page == "Analysis":
    st.header("Portfolio analysis")

    prices: StocksDict = st.session_state.prices
    portfolio: PortfolioDict = st.session_state.portfolio

    if not portfolio:
        st.info("Portfolio is empty.")
    elif not prices:
        st.warning("Load stock prices first.")
    else:
        try:
            current_value = analysis.portfolio_value(portfolio, prices)
            cost_basis = analysis.portfolio_cost_basis(portfolio, prices)
            roi = analysis.roi_percent(portfolio, prices)
        except Exception as exc:
            st.error(f"Analysis failed: {exc}")
        else:
            st.metric("Current Value", f"{current_value:.2f}")
            st.metric("Cost Basis", f"{cost_basis:.2f}")
            st.metric("ROI (%)", f"{roi:.2f}")

elif page == "Visualization":
    st.header("Portfolio visualization")

    prices: StocksDict = st.session_state.prices
    portfolio: PortfolioDict = st.session_state.portfolio

    if not portfolio:
        st.info("Portfolio is empty.")
    elif not prices:
        st.warning("Load stock prices first.")
    else:
        try:
            fig = visualization.allocation_pie_figure(portfolio, prices)
        except Exception as exc:
            st.error(f"Visualization failed: {exc}")
        else:
            st.pyplot(fig)

elif page == "Save/Load portfolio":
    st.header("Save or load portfolio")

    portfolio: PortfolioDict = st.session_state.portfolio

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Save portfolio")
        save_path = st.text_input("Save path", value=str(DEFAULT_PORTFOLIO_PATH), key="save_path")
        if st.button("Save"):
            try:
                data_io.save_portfolio(save_path, portfolio)
                st.success(f"Portfolio saved to {save_path}.")
            except Exception as exc:
                st.error(f"Save failed: {exc}")

    with col2:
        st.subheader("Load portfolio")
        load_path = st.text_input("Load path", value=str(DEFAULT_PORTFOLIO_PATH), key="load_path")
        if st.button("Load"):
            try:
                loaded = data_io.load_portfolio(load_path)
                st.session_state.portfolio = loaded
                st.success(f"Portfolio loaded from {load_path}.")
            except Exception as exc:
                st.error(f"Load failed: {exc}")

    current_portfolio: PortfolioDict = st.session_state.portfolio

    if current_portfolio:
        st.subheader("Current holdings")
        st.table(_format_portfolio_table(current_portfolio))
    else:
        st.info("Portfolio is empty.")
