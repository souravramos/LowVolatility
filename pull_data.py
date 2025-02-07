import yfinance as yf
from datetime import datetime, timedelta
import traceback
from pycparser.ply.cpp import t_CPP_ID

import variables as vb
import logging, logger_config
logger = logging.getLogger(__name__)
from file_paths import UNIVERSE_FILE_PATH, DATA_PATH
import pandas as pd

start_date = vb.START_DATE
end_date = vb.END_DATE
end_date = (datetime.strptime(end_date, "%Y-%m-%d") + timedelta(days=1)).strftime("%Y-%m-%d")


def Pull_Data_From_YFinance(ticker, start_date=start_date, end_date=end_date):
    # Fetch historical daily data
    try:
        data = yf.download(ticker + '.NS', start=start_date, end=end_date, interval="1d")
        if not data.empty:
            logger.info(f"Fetched 1-Day data for {ticker} from {start_date} to {end_date}")
        else:
            logger.warning(f"No data found for {ticker}. It may be delisted or check the symbol.")

    except Exception as e:
        data = pd.DataFrame()
        logger.error(f"Error fetching the data for {ticker}: {e}")
        logger.error(traceback.format_exc())

    return data




# nifty_50_stocks = pd.read_csv(UNIVERSE_FILE_PATH + 'NIFTY50.csv')
# print(nifty_50_stocks)
# for stock in nifty_50_stocks['Symbol']:
#     print(stock)
#     print(Pull_Data_From_YFinance(stock, start_date, end_date))
