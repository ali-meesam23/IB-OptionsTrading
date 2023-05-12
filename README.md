# Overview

This is a Flask application that serves as a trading platform. Here's a summary:

The app is built using Flask and includes necessary imports and configurations.
It establishes a connection with InteractiveBrokers or Questrade (readonly - market data for redundancy) through the TradeHandler object (not included in this repo).
The app provides an index route for rendering the main trading interface and handling buy/sell orders.
It supports buying and selling call/put options and provides options to close open orders or positions.
The app includes routes for starting, stopping, and canceling global orders.
It uses the PackageDB object to update relevant data for a specific ticker and days to expire.
The Flask application is set up to run on host '0.0.0.0' and port 5001.
In summary, this app serves as a trading platform built using Flask, providing functionality for executing options trades, managing orders and positions, and interacting with InteractiveBrokers or Questrade.