import requests

class NotionClass:
    def __init__(self, database_id, headers):
        self.database_id = database_id
        self.headers = headers

    def create_page(self, data: dict):
        create_url = "https://api.notion.com/v1/pages"

        payload = {"parent": {"database_id": self.database_id}, "properties": data}

        res = requests.post(create_url, headers=self.headers, json=payload)
        return res

    def get_pages(self, num_pages=None):
        url = f"https://api.notion.com/v1/databases/{self.database_id}/query"

        get_all = num_pages is None
        page_size = 100 if get_all else num_pages

        payload = {"page_size": page_size}
        response = requests.post(url, json=payload, headers=self.headers)

        data = response.json()

        results = data["results"]
        while data["has_more"] and get_all:
            payload = {"page_size": page_size, "start_cursor": data["next_cursor"]}
            response = requests.post(url, json=payload, headers=self.headers)
            data = response.json()
            results.extend(data["results"])

        return results

    def update_page(self, page_id: str, data: dict):
        url = f"https://api.notion.com/v1/pages/{page_id}"

        payload = {"properties": data}

        res = requests.patch(url, json=payload, headers=self.headers)
        return res
