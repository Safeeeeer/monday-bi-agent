from datetime import datetime
from data_cleaning import clean_currency, parse_date


# ============================================================
# Detect Important Columns Dynamically
# ============================================================

def detect_columns(df):
    columns = {col.lower(): col for col in df.columns}

    stage_col = next((columns[c] for c in columns if "stage" in c or "status" in c), None)
    sector_col = next((columns[c] for c in columns if "sector" in c or "industry" in c), None)
    amount_col = next((columns[c] for c in columns if "amount" in c or "value" in c or "revenue" in c), None)
    date_col = next((columns[c] for c in columns if "date" in c), None)

    return stage_col, sector_col, amount_col, date_col


# ============================================================
# Core Metric Engine (Reusable)
# ============================================================

def compute_metric(
    df,
    stage_filter=None,          # "open" or "closed"
    quarter_filter=True,
    target_sector=None
):

    stage_col, sector_col, amount_col, date_col = detect_columns(df)

    if not all([stage_col, amount_col, date_col]):
        return 0

    now = datetime.now()
    current_quarter = (now.month - 1) // 3 + 1

    total = 0

    for _, row in df.iterrows():

        stage = str(row.get(stage_col, "")).lower()
        amount = clean_currency(row.get(amount_col))
        date = parse_date(row.get(date_col))

        if not date:
            continue

        deal_quarter = (date.month - 1) // 3 + 1

        # Stage filtering
        if stage_filter == "open":
            if any(x in stage for x in ["closed", "won", "lost", "completed"]):
                continue

        if stage_filter == "closed":
            if not any(x in stage for x in ["closed", "won", "completed"]):
                continue

        # Quarter filtering
        if quarter_filter:
            if date.year != now.year or deal_quarter != current_quarter:
                continue

        # Sector filtering
        if target_sector and sector_col:
            sector = str(row.get(sector_col, "")).lower()
            if target_sector.lower() not in sector:
                continue

        total += amount

    return total


# ============================================================
# Public BI Functions
# ============================================================

def pipeline_this_quarter(df, target_sector=None):
    return compute_metric(
        df,
        stage_filter="open",
        quarter_filter=True,
        target_sector=target_sector
    )


def revenue_this_quarter(df, target_sector=None):
    return compute_metric(
        df,
        stage_filter="closed",
        quarter_filter=True,
        target_sector=target_sector
    )


def pipeline_by_sector(df):

    stage_col, sector_col, amount_col, _ = detect_columns(df)

    if not all([stage_col, sector_col, amount_col]):
        return {}

    results = {}

    for _, row in df.iterrows():

        stage = str(row.get(stage_col, "")).lower()
        sector = str(row.get(sector_col, "Unknown")).strip().lower()
        amount = clean_currency(row.get(amount_col))

        if any(x in stage for x in ["closed", "won", "lost", "completed"]):
            continue

        results[sector] = results.get(sector, 0) + amount

    return results


def completed_work_orders_this_quarter(df):

    stage_col, _, amount_col, date_col = detect_columns(df)

    if not all([stage_col, amount_col, date_col]):
        return 0

    now = datetime.now()
    current_quarter = (now.month - 1) // 3 + 1

    total = 0

    for _, row in df.iterrows():

        status = str(row.get(stage_col, "")).lower()
        amount = clean_currency(row.get(amount_col))
        date = parse_date(row.get(date_col))

        if not date:
            continue

        order_quarter = (date.month - 1) // 3 + 1

        if (
            any(x in status for x in ["done", "complete", "finished"])
            and date.year == now.year
            and order_quarter == current_quarter
        ):
            total += amount

    return total