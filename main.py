import json
import os
from notion import NotionClass
from yahooFinance import YahooFinance

class Main:
    def __init__(self, config_file):
        self.config_file = config_file
        self.config_data = self.load_config()
        self.headers = self.initialize_headers()

    def load_config(self):
        with open(self.config_file, 'r') as file:
            config_data = json.load(file)
        return config_data

    def initialize_headers(self):
        headers = {
            "Authorization": "Bearer " + self.config_data.get('notion_token'),
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28",
        }
        return headers

    def run(self):
        print("=== Lancement de l'application ===")

        # Init
        notion = NotionClass(database_id=self.config_data.get('database_id'), headers=self.headers)
        yahooFinance = YahooFinance()

        # Récupération des pages 
        pages = notion.get_pages()

        for page in pages:
            page_id     = page.get("id")
            page_stock  = page.get("properties").get("Ticker").get("title")[0].get("plain_text")
            page_price  = yahooFinance.get_stock_price(page_stock)
            update_data = {"Prix actuel": {"number": round(page_price, 2)}}
            notion.update_page(page_id, update_data)

        print("=== Arrêt de l'application ===")

if __name__ == "__main__":
    config_file = 'config/config.json'
    main_app = Main(config_file)
    main_app.run()
