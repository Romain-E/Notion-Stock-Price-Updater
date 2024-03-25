import yfinance as yf

class YahooFinance:
    def __init__(self):
        pass

    def get_stock_price(self, symbol):
        try:
            stock = yf.Ticker(symbol)
            price = stock.history(period="1d")["Close"].iloc[-1]
            return price
        except Exception as e:
            print(f"Erreur lors de la récupération du prix de l'action {symbol}: {e}")
            return None

# Exemple d'utilisation :
if __name__ == "__main__":
    finance = YahooFinance()
    stock_symbol = 'AAPL'  # Symbole de l'action à récupérer
    stock_price = finance.get_stock_price(stock_symbol)
    if stock_price is not None:
        print(f"Le prix de l'action {stock_symbol} est de {stock_price} USD.")
