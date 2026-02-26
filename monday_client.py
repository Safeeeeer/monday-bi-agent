import requests
from config import MONDAY_API_KEY

MONDAY_URL = "https://api.monday.com/v2"


# ============================================================
# Execute GraphQL Query
# ============================================================

def execute_query(query):

    headers = {
        "Authorization": MONDAY_API_KEY,
        "Content-Type": "application/json"
    }

    response = requests.post(
        MONDAY_URL,
        json={"query": query},
        headers=headers
    )

    if response.status_code != 200:
        raise Exception(f"Monday API HTTP Error: {response.status_code}")

    return response.json()


# ============================================================
# Fetch Board Items (Live Every Time)
# ============================================================

def fetch_board_items(board_id):

    query = f"""
    query {{
      boards(ids: {board_id}) {{
        name
        items_page {{
          items {{
            id
            name
            column_values {{
              text
              column {{
                title
              }}
            }}
          }}
        }}
      }}
    }}
    """

    return execute_query(query)