# import yfinance as yf
#
#
# def save_to_csv(dataframe, filename):
#     dataframe.to_csv(f'{filename}.csv', index=False)
#
#
# aapl = yf.download("AAPL", start="2017-01-01", end="2021-05-20",
#                    group_by="ticker")
# print(aapl)
# print("aapl.info = ", type(aapl.info), aapl.info)
# hist = aapl.history(period="max")
# print("aapl.actions = ", type(aapl.actions), aapl.actions.head())
# # save_to_csv(aapl.actions, "aapl_actions")
# # show dividends
# print("aapl.dividends = ", type(aapl.dividends), aapl.dividends)
#
# # show splits
# print("aapl.splits = ", type(aapl.splits), aapl.splits)
#
# # show financials
# print("aapl.financials = ", type(aapl.financials), aapl.financials.head())
# # save_to_csv(aapl.financials, "aapl_financials")
#
# print("aapl.quarterly_financials = ", type(aapl.quarterly_financials), aapl.quarterly_financials.head())
# # save_to_csv(aapl.quarterly_financials, "aapl_quarterly_financials")
#
# # show major holders
# print("aapl.major_holders = ", type(aapl.major_holders), aapl.major_holders.head())
# # save_to_csv(aapl.major_holders, "aapl_major_holders")
#
# # show institutional holders
# print("aapl.institutional_holders = ", type(aapl.institutional_holders), aapl.institutional_holders.head())
# # save_to_csv(aapl.institutional_holders, "aapl_institutional_holders")
#
# # show balance sheet
# print("aapl.balance_sheet = ", type(aapl.balance_sheet), aapl.balance_sheet.head())
# # save_to_csv(aapl.balance_sheet, "aapl_balance_sheet")
#
# print("aapl.quarterly_balance_sheet = ", type(aapl.quarterly_balance_sheet), aapl.quarterly_balance_sheet.head())
# # save_to_csv(aapl.quarterly_balance_sheet, "aapl_quarterly_balance_sheet")
#
# # show cashflow
# print("aapl.cashflow = ", type(aapl.cashflow), aapl.cashflow.head())
# # save_to_csv(aapl.cashflow, "aapl_cashflow")
#
# print("aapl.quarterly_cashflow = ", type(aapl.quarterly_cashflow), aapl.quarterly_cashflow.head())
# # save_to_csv(aapl.quarterly_cashflow, "aapl_quarterly_cashflow")
#
# # show earnings
# print("aapl.earnings = ", type(aapl.earnings), aapl.earnings.head())
# # save_to_csv(aapl.earnings, "aapl_earnings")
#
# print("aapl.quarterly_earnings = ", type(aapl.quarterly_earnings), aapl.quarterly_earnings.head())
# # save_to_csv(aapl.quarterly_earnings, "aapl_quarterly_earnings")
#
# # show sustainability
# print("aapl.sustainability = ", type(aapl.sustainability), aapl.sustainability.head())
# # save_to_csv(aapl.sustainability, "aapl_sustainability")
#
# # show analysts recommendations
# print("aapl.recommendations = ", type(aapl.recommendations), aapl.recommendations.head())
# # save_to_csv(aapl.recommendations, "aapl_recommendations")
#
# # show next event (earnings, etc)
# print("aapl.calenda = ", type(aapl.calendar), aapl.calendar.head())
# # save_to_csv(aapl.calendar, "aapl_calendar")
#
# # show ISIN code - *experimental*
# # ISIN = International Securities Identification Number
# print("aapl.isin = ", type(aapl.isin), aapl.isin)
# # save_to_csv(aapl.calendar, "aapl_calendar")
#
# # show options expirations
# print("aapl.options = ", type(aapl.options), aapl.options)
#
# print("aapl = ", type(aapl), aapl)
# # get option chain for specific expiration
# opt = aapl.option_chain('YYYY-MM-DD')
# import pandas as pd
import requests
# from termcolor import colored as cl
# import matplotlib.pyplot as plt

# plt.style.use('seaborn-whitegrid')
# plt.rcParams['figure.figsize'] = (15,8)

iex_api_key = 'pk_b2968a4c180949689e743441f3e2eb5a'


def get_quote(symbols):
    api_url = f'https://cloud.iexapis.com/stable/stock/{symbols}/quote?token={iex_api_key}'
    df = requests.get(api_url).json()
    return df


def get_news(symbols, last=10):
    api_url = f'https://cloud.iexapis.com/stable/stock/{symbols}/news?last={last}&token={iex_api_key}'
    df = requests.get(api_url).json()
    return df


def get_company(symbols):
    api_url = f'https://cloud.iexapis.com/stable/stock/{symbols}/company?token={iex_api_key}'
    df = requests.get(api_url)
    if df.status_code == 404:
        return None
    return df.json()


def get_symbol():
    api_url = f'https://cloud.iexapis.com/stable/ref-data/symbols?token={iex_api_key}'
    df = requests.get(api_url).json()
    return df


def get_key_state(symbols, stat=None):
    api_url = f'https://cloud.iexapis.com/stable/stock/{symbols}/stats'
    data = {"token": iex_api_key}
    if stat:
        data["stat"] = stat
    df = requests.get(api_url, params=data).json()
    return df

