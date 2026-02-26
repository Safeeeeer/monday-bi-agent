import pandas as pd
from dateutil import parser


# ============================================================
# Currency Cleaning
# ============================================================

def clean_currency(val):
    if val is None or val == "":
        return 0

    try:
        val = str(val)
        val = val.replace("$", "")
        val = val.replace(",", "")
        val = val.replace("₹", "")
        val = val.strip()
        return float(val)
    except:
        return 0


# ============================================================
# Date Parsing (Handles messy formats)
# ============================================================

def parse_date(val):
    if val is None or val == "":
        return None

    try:
        return parser.parse(str(val))
    except:
        return None


# ============================================================
# Convert Monday JSON → DataFrame (Safe Version)
# ============================================================

def board_json_to_df(board_json):

    # Handle API errors
    if board_json is None:
        raise Exception("Empty response from Monday API")

    if "errors" in board_json:
        raise Exception(f"Monday API Error: {board_json['errors']}")

    boards = board_json.get("data", {}).get("boards", [])

    if not boards:
        raise Exception("No boards returned. Check board ID or permissions.")

    items = boards[0].get("items_page", {}).get("items", [])

    rows = []

    for item in items:
        row = {"Item Name": item.get("name")}

        for col in item.get("column_values", []):
            column_title = col.get("column", {}).get("title")
            row[column_title] = col.get("text")

        rows.append(row)

    df = pd.DataFrame(rows)

    return df