import pandas as pd
from messari import MessariData
import matplotlib.pyplot as plt


def prepare_euro_ref_data(ref_file, base_currency, min_date, max_date):
    # read csv containing exchange rate and parsing dates explicitly for Date column
    euro_csv = pd.read_csv(ref_file, parse_dates=['Date'])

    # select date along with target current
    euro_csv = euro_csv[['Date', base_currency]]

    # defining date filters
    filters = (euro_csv['Date'] >= min_date) & (euro_csv['Date'] <= max_date)

    # applying filters
    euro_csv = euro_csv[filters].sort_values(by=['Date'])

    return euro_csv

def generate_viz(merged_df):
    """
        generate picture from dataframe with default properties
    """
    plt.figure(figsize=(15,10))
    plt.grid(True)
    plt.plot(merged_df['amount'], label="token_in_USD")
    plt.plot(merged_df['eur'], label="token_in_EUR")
    plt.plot(merged_df['rolling_avg'], label="7day_rolling_average")
    plt.legend(loc=2)
    plt.savefig("rolling_average_picture.png")
    return 

def calculate_rolling_average(ref_file, token, metric, year, base_currency, min_date, max_date):
    """
        Calculate rolling average
    """

    # instantiate object to get bitcoin price for the given year
    token_timeseries_data = MessariData(token, metric, year).get_asset_timeseries()

    # get source data
    euro_ref = prepare_euro_ref_data(ref_file, base_currency, min_date, max_date)

    # create dataframe with response data
    try:
        token_df = pd.DataFrame(token_timeseries_data['data']['values'], columns=['Date', 'amount'])
    except:
        raise ("Error extracting response")
    
    # converting date to dateime to have consistency across both dataframe before joining
    token_df['Date'] = pd.to_datetime(token_df['Date']).dt.date.astype('datetime64')

    # marge source and reference data to calculate euro conversion from USD
    merged_df = euro_ref.merge(token_df, on='Date')
    merged_df['eur'] = merged_df['USD'] * merged_df['amount']

    # calculate 7 rolling average and dropping nulls
    merged_df['rolling_avg'] = merged_df['eur'].rolling(7).mean()
    merged_df = merged_df.dropna()

    # prepare visualization
    generate_viz(merged_df)

    return 

print(calculate_rolling_average('data/eurofxref-hist.csv',
                                'bitcoin', 'price', '2021', 'USD',
                                '2021-01-01', '2021-12-31'))