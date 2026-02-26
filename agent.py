from datetime import datetime

from config import DEALS_BOARD_ID, WORK_ORDERS_BOARD_ID
from monday_client import fetch_board_items
from data_cleaning import board_json_to_df
from bi_engine import (
    pipeline_this_quarter,
    revenue_this_quarter,
    pipeline_by_sector,
    completed_work_orders_this_quarter,
    detect_columns
)

from intent_parser import interpret_query
from data_quality import assess_data_quality
from summary_generator import generate_summary


def run_agent(user_input, chat_history=None):

    trace = []
    query_time = datetime.now()

    try:
        # Interpret query
        interpretation = interpret_query(user_input, chat_history)
        trace.append("[LLM] Interpreted query")

        intent = interpretation.get("intent")
        sector = interpretation.get("sector")
        time_range = interpretation.get("time_range")

        trace.append(f"[INTENT] {intent} | sector={sector} | time={time_range}")

        # Clarification
        if intent in ["pipeline", "revenue"] and not sector:
            return {
                "summary": "Which sector should I analyze? (e.g., Energy, Healthcare)",
                "trace": build_trace(trace, query_time)
            }

        # Fetch Deals
        deals_json = fetch_board_items(DEALS_BOARD_ID)
        trace.append(f"[API CALL] Deals board fetched (ID: {DEALS_BOARD_ID})")

        deals_df = board_json_to_df(deals_json)
        trace.append(f"[ROWS] Deals: {len(deals_df)}")
        trace.append("[PROCESS] Data cleaned")

        stage_col, sector_col, amount_col, date_col = detect_columns(deals_df)

        data_issues = assess_data_quality(deals_df, amount_col, date_col)
        trace.append("[CHECK] Data quality evaluated")

        result_data = ""

        # PIPELINE
        if intent == "pipeline":
            total = pipeline_this_quarter(deals_df, sector)
            result_data = f"Pipeline: ${total:,.2f}"

        # REVENUE
        elif intent == "revenue":
            total = revenue_this_quarter(deals_df, sector)
            result_data = f"Revenue: ${total:,.2f}"

        # COMPARE
        elif intent == "compare":
            work_json = fetch_board_items(WORK_ORDERS_BOARD_ID)
            trace.append("[API CALL] Work Orders fetched")

            work_df = board_json_to_df(work_json)

            revenue_total = revenue_this_quarter(deals_df)
            work_total = completed_work_orders_this_quarter(work_df)

            rate = (work_total / revenue_total * 100) if revenue_total > 0 else 0

            result_data = f"""
Revenue: ${revenue_total:,.2f}
Work Orders: ${work_total:,.2f}
Execution Rate: {rate:.1f}%
"""

        # CONVERSION
        elif intent == "conversion":
            work_json = fetch_board_items(WORK_ORDERS_BOARD_ID)
            trace.append("[API CALL] Work Orders fetched")

            work_df = board_json_to_df(work_json)

            deals_count = len(deals_df)
            work_count = len(work_df)

            conversion_rate = (work_count / deals_count * 100) if deals_count > 0 else 0

            result_data = f"""
Deals: {deals_count}
Work Orders: {work_count}
Conversion Rate: {conversion_rate:.1f}%
"""

        # TOP SECTOR
        elif intent == "top_sector":
            breakdown = pipeline_by_sector(deals_df)

            if breakdown:
                top_sector = max(breakdown, key=breakdown.get)
                value = breakdown[top_sector]
                result_data = f"Top Sector: {top_sector} (${value:,.2f})"
            else:
                result_data = "No data available"

        # DEFAULT
        else:
            breakdown = pipeline_by_sector(deals_df)
            result_data = str(breakdown)

        # Data quality notes
        quality_note = ""
        if data_issues:
            quality_note = "\n\nData Notes:\n- " + "\n- ".join(data_issues)

        # Summary
        summary = generate_summary(user_input, result_data + quality_note)
        trace.append("[LLM] Generated summary")

        return {
            "summary": summary,
            "trace": build_trace(trace, query_time)
        }

    except Exception as e:
        return {
            "summary": f"⚠ Error: {str(e)}",
            "trace": build_trace(trace, query_time)
        }


def build_trace(trace_list, query_time):
    return f"""
🔍 Agent Trace
{"\n".join(trace_list)}
Query Time: {query_time}
""".strip()