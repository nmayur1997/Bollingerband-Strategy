import yfinance as yf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


symbol = '^NSEI'
data = yf.download(symbol, start='2020-01-01', end='2024-01-01')


data['Diff'] = data['Close'].diff()


data['moving_average'] = data['Diff'].rolling(window=5).mean()
data['moving_std_dev'] = data['Diff'].rolling(window=5).std()
data['upper_band'] = data['moving_average'] + data['moving_std_dev']
data['lower_band'] = data['moving_average'] - data['moving_std_dev']


data['long_entry'] = data['Diff'] < data['lower_band']
data['long_exit'] = data['Diff'] >= data['moving_average']
data['positions_long'] = np.nan
data.loc[data['long_entry'], 'positions_long'] = 1
data.loc[data['long_exit'], 'positions_long'] = 0
data['positions_long'] = data['positions_long'].ffill()  

data['short_entry'] = data['Diff'] > data['upper_band']
data['short_exit'] = data['Diff'] <= data['moving_average']
data['positions_short'] = np.nan
data.loc[data['short_entry'], 'positions_short'] = -1
data.loc[data['short_exit'], 'positions_short'] = 0
data['positions_short'] = data['positions_short'].ffill()  

data['positions'] = data['positions_long'] + data['positions_short']
data['price_difference'] = data['Diff'] - data['Diff'].shift(1)
data['pnl'] = data['positions'].shift(1) * data['price_difference']
data['cumpnl'] = data['pnl'].cumsum()


starting_capital = 100000


data['portfolio_value'] = starting_capital + data['cumpnl']


num_long_entries = data['long_entry'].sum()
num_short_entries = data['short_entry'].sum()


long_profits = data[data['positions_long'] == 1]['pnl'].sum()
short_profits = data[data['positions_short'] == -1]['pnl'].sum()


data['year'] = data.index.year
roi_per_year = data.groupby('year')['cumpnl'].last().pct_change().fillna(0) * 100


ending_capital = data['portfolio_value'].iloc[-1]


all_pnls = pd.concat([data[data['positions_long'] == 1][['pnl']], data[data['positions_short'] == -1][['pnl']]], axis=0)


average_profit = all_pnls[all_pnls['pnl'] > 0]['pnl'].mean()
average_loss = all_pnls[all_pnls['pnl'] < 0]['pnl'].mean()


max_profit = all_pnls['pnl'].max()
max_loss = all_pnls['pnl'].min()


print(f"Number of Long Entries: {num_long_entries}")
print(f"Number of Short Entries: {num_short_entries}")
print(f"Total Profit from Long Entries: {long_profits:.2f}")
print(f"Total Profit from Short Entries: {short_profits:.2f}")
print(f"Year-on-Year ROI (%):\n{roi_per_year}")
print(f"Starting Capital: {starting_capital:.2f}")
print(f"Ending Capital: {ending_capital:.2f}")
print(f"Total Return (%): {(ending_capital / starting_capital - 1) * 100:.2f}%")
print(f"Average Profit: {average_profit:.2f}")
print(f"Average Loss: {average_loss:.2f}")
print(f"Maximum Profit: {max_profit:.2f}")
print(f"Maximum Loss: {max_loss:.2f}")


long_entries = data[data['long_entry']].copy()
short_entries = data[data['short_entry']].copy()


long_entries['Entry_Type'] = 'Long'
short_entries['Entry_Type'] = 'Short'


long_entries['Date'] = long_entries.index.date
long_entries['Time'] = long_entries.index.time
short_entries['Date'] = short_entries.index.date
short_entries['Time'] = short_entries.index.time


long_entries_export = long_entries[['Date', 'Time', 'Entry_Type', 'pnl']].reset_index(drop=True)
short_entries_export = short_entries[['Date', 'Time', 'Entry_Type', 'pnl']].reset_index(drop=True)


entries_export = pd.concat([long_entries_export, short_entries_export])


excel_file = 'bollinger_band_strategy_results.xlsx'
with pd.ExcelWriter(excel_file) as writer:
    entries_export.to_excel(writer, sheet_name='All Entries', index=False)
    
    
    summary_df = pd.DataFrame({
        'Metric': ['Number of Long Entries', 'Number of Short Entries', 'Total Profit from Long Entries', 
                   'Total Profit from Short Entries', 'Starting Capital', 'Ending Capital', 
                   'Total Return (%)', 'Average Profit', 'Average Loss', 'Maximum Profit', 
                   'Maximum Loss'],
        'Value': [num_long_entries, num_short_entries, long_profits, short_profits, starting_capital, 
                  ending_capital, (ending_capital / starting_capital - 1) * 100, average_profit, 
                  average_loss, max_profit, max_loss]
    })
    summary_df.to_excel(writer, sheet_name='Summary Statistics', index=False)

print(f"Results saved to {excel_file}")
