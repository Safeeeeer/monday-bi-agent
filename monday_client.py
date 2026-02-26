import requests
from config import MONDAY_API_KEY

MONDAY_URL = "https://api.monday.com/v2"


def execute_query(query, variables=None):

    headers = {
        "Authorization": MONDAY_API_KEY,
        "Content-Type": "application/json"
    }

    payload = {"query": query}
    if variables:
        payload["variables"] = variables

    response = requests.post(
        MONDAY_URL,
        json=payload,
        headers=headers
    )

    if response.status_code != 200:
        raise Exception(f"Monday API HTTP Error: {response.status_code}")

    data = response.json()

    if "errors" in data:
        raise Exception(f"Monday API Error: {data['errors']}")

    return data


def fetch_board_items(board_id):

    query = """
    query ($boardId: [ID!]) {
      boards(ids: $boardId) {
        name
        items_page(limit: 50) {
          items {
            id
            name
            column_values {
              id
              text
            }
          }
        }
      }
    }
    """

    variables = {"boardId": [board_id]}
    return execute_query(query, variables)