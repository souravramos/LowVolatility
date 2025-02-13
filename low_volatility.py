import pandas as pd
import file_paths
from file_paths import DATA_PATH
import variables as vb
import os
from pull_data import Pull_Data_From_YFinance
from utils import write_df_to_csv

stocks_categories = next(os.walk(file_paths.UNIVERSE_FILE_PATH))[2]

if vb.GENERATE_NEW_DATA:
    for stocks_category in stocks_categories:
        if stocks_category not in vb.INDICES_LIST:
            continue
        print(stocks_category)
        stocks_df = pd.read_csv(file_paths.UNIVERSE_FILE_PATH + '//' + stocks_category)
        stocks = stocks_df['Symbol'].to_list()

        for stock in stocks:
            if stock not in vb.STOCKS_LIST:
                continue
            print(stock)
            stock_df = Pull_Data_From_YFinance(stock, vb.START_DATE, vb.END_DATE)
            output_path = DATA_PATH + "//" + stocks_category.replace('.csv', '') + '//' + stock + '.csv'
            if os.path.isfile(output_path):  # Delete only files, not subdirectories
                os.remove(output_path)
            if not stock_df.empty:
                print(stock)
                write_df_to_csv(stock_df, output_path)

def calculate_moving_average(df, column="Adj_Close", period=200, ma_type="SMA"):
    """
    Calculates the chosen moving average type (SMA, EMA, DEMA) for a given stock dataframe.

    :param df: DataFrame containing stock price data with a 'Close' column
    :param column: The column to calculate the moving average on (default: 'Close')
    :param period: The lookback period (default: 200 days)
    :param ma_type: Type of moving average ('SMA', 'EMA', 'DEMA')
    :return: DataFrame with new column for the selected moving average
    """

    if ma_type == "SMA":
        df[f"{ma_type}_{period}"] = df[column].rolling(window=period).mean()
    elif ma_type == "EMA":
        df[f"{ma_type}_{period}"] = df[column].ewm(span=period, adjust=False).mean()
    elif ma_type == "DEMA":
        ema = df[column].ewm(span=period, adjust=False).mean()
        df[f"{ma_type}_{period}"] = (2 * ema) - ema.ewm(span=period, adjust=False).mean()
    else:
        raise ValueError("Invalid MA type. Choose from 'SMA', 'EMA', or 'DEMA'.")

    return df[f"{ma_type}_{period}"]


def stock_screener(df, index_df=None):
    """Filter stocks based on low-volatility criteria."""

    # Calculate moving averages
    df['50-EMA'] = calculate_moving_average(df, period=50, ma_type='EMA')
    df['200-SMA'] = calculate_moving_average(df, period=200, ma_type='SMA')

    df['Price_Above_200_SMA'] = df['Adj_Close'] > df['200-SMA']
    df['Price_Above_50_EMA'] = df['Adj_Close'] > df['50-EMA']
    # print(df.tail(10))

    return df

df = pd.read_csv(r'D:\Sourav\QuantIQ\Strategies\LowVolatility\Data\NIFTY50\RELIANCE.csv')
df = df.rename(columns={'Adj Close' : 'Adj_Close'})
print(df)
df = stock_screener(df)
df.to_csv(r'D:\Sourav\QuantIQ\Strategies\LowVolatility\Reports\RELIANCE.csv', index=False)