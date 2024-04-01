import json
import os
from notion import NotionClass
from yahooFinance import YahooFinance

class Main:
    def __init__(self):
        self.notion_token = os.environ.get('NOTION_TOKEN')
        self.datanase_id = os.environ.get('DATABASE_ID')
        self.headers = self.initialize_headers()

    def load_config(self):
        with open(self.config_file, 'r') as file:
            config_data = json.load(file)
        return config_data

    def initialize_headers(self):
        headers = {
            "Authorization": "Bearer " + self.notion_token,
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28",
        }
        return headers

    def run(self):
        print("=== Lancement de l'application ===")

        # Init
        notion = NotionClass(database_id=self.datanase_id, headers=self.headers)
        yahooFinance = YahooFinance()

        # Récupération des pages 
        pages = notion.get_pages()

        for page in pages:
            page_id     = page.get("id")
            page_ticker  = page.get("properties").get("Ticker").get("title")[0].get("plain_text")
            page_name, page_price = yahooFinance.get_stock_price(page_ticker)
            if(page_price):
                print(f"{page_name} : {page_price}")
                update_data = {
                    "Label : Nom" : {"rich_text": [{"type": "text", "text": {"content": page_name}}]},
                    "Prix actuel": {"number": round(page_price, 2)}
                }
                notion.update_page(page_id, update_data)
            else:
                print(f"Pas de mise à jour pour {page_ticker}.")

        print("=== Arrêt de l'application ===")

if __name__ == "__main__":
    main_app = Main()
    main_app.run()
