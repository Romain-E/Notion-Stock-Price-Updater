import yfinance as yf
import pandas as pd

class YahooFinance:
    def __init__(self):
        pass

    def get_stock_price(self, symbol):
        try:
            stock = yf.Ticker(symbol)
            data = stock.history(period="1d")
            if data.empty:
                print(f"No data available for {symbol}.")
                return None
            current_price = data["Close"].iloc[-1]
            if pd.isna(current_price):
                print(f"No closing price available for {symbol}.")
                return None
            return current_price
        except KeyError as ke:
            print(f"KeyError while retrieving data for {symbol}: {ke}")
            return None
        except Exception as e:
            print(f"Error while retrieving data for {symbol}: {e}")
            return None

# Exemple d'utilisation :
if __name__ == "__main__":
    finance = YahooFinance()
    stock_symbol = 'AAPL'  # Symbole de l'action à récupérer
    stock_price = finance.get_stock_price(stock_symbol)
    if stock_price is not None:
        print(f"Le prix de l'action {stock_symbol} est de {stock_price} USD.")
