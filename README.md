# Bollinger Bands Momentum Crossover Strategy

This repository contains a Python implementation of the Bollinger Bands Momentum Crossover Strategy applied to the NIFTY50 stock index using historical data from Yahoo Finance. The strategy utilizes Bollinger Bands to generate trading signals and evaluates the performance of these signals through various metrics.

## Features

- **Fetch Historical Data**: Retrieve historical stock data for NIFTY50 from Yahoo Finance.
- **Bollinger Bands Calculation**: Compute Bollinger Bands using a 5-day moving average and standard deviation.
- **Trading Signals Generation**: Identify long and short entry and exit signals based on Bollinger Bands.
- **Performance Analysis**: Calculate various performance metrics including total profit, average profit/loss, maximum profit/loss, and overall return on investment (ROI).
- **Excel Export**: Save detailed trading entries and summary statistics to an Excel file.

## Prerequisites

Ensure you have the following Python packages installed:

- `numpy`
- `pandas`
- `matplotlib`
- `yfinance`

Install the required packages using pip:

```bash
pip install numpy pandas matplotlib yfinance


##Strategy Overview
Bollinger Bands Calculation
Moving Average: A 5-day simple moving average of the daily price difference.
Standard Deviation: A 5-day rolling standard deviation of the daily price difference.
Upper Band: Moving average plus standard deviation.
Lower Band: Moving average minus standard deviation.

##Trading Signals
Long Entry: Generated when the price difference falls below the lower Bollinger Band, indicating a potential buying opportunity.
Long Exit: Triggered when the price difference rises above the moving average, signaling the end of the buying opportunity.
Short Entry: Triggered when the price difference exceeds the upper Bollinger Band, indicating a potential selling opportunity.
Short Exit: Generated when the price difference falls below the moving average, signaling the end of the selling opportunity.
