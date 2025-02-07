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


