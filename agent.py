from datetime import datetime
import json
from groq import Groq
from config import GROQ_API_KEY, DEALS_BOARD_ID, WORK_ORDERS_BOARD_ID
from monday_client import fetch_board_items
from data_cleaning import board_json_to_df
from bi_engine import (
    pipeline_this_quarter,
    revenue_this_quarter,
    pipeline_by_sector,
    completed_work_orders_this_quarter
)

client = Groq(api_key=GROQ_API_KEY)


# ============================================================
# Interpret User Intent Using Groq
# ============================================================

def interpret_query(user_input, chat_history=None):

    system_prompt = """
You are a Business Intelligence routing engine.

Return STRICT JSON in this format:

{
  "intent": "pipeline" | "revenue" | "compare" | "breakdown",
  "sector": "sector name or null"
}

If no sector mentioned, return null for sector.
Only return valid JSON.
"""

    messages = [{"role": "system", "content": system_prompt}]

    if chat_history:
        messages.extend(chat_history)

    messages.append({"role": "user", "content": user_input})

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
        temperature=0
    )

    content = response.choices[0].message.content.strip()

    # Safe JSON parsing
    try:
        return json.loads(content)
    except:
        return {"intent": "breakdown", "sector": None}


# ============================================================
# Generate Executive Summary
# ============================================================

def generate_summary(user_input, computed_data):

    prompt = f"""
User asked:
{user_input}

Computed metrics:
{computed_data}

Write a concise executive-level business summary.
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )

    return response.choices[0].message.content.strip()


# ============================================================
# Main Agent Function (Now Accepts Chat History)
# ============================================================

def run_agent(user_input, chat_history=None):

    trace = []
    query_time = datetime.now()

    try:
        # 1️⃣ Interpret query via Groq
        interpretation = interpret_query(user_input, chat_history)
        trace.append("Groq interpreted user intent")

        intent = interpretation.get("intent")
        sector = interpretation.get("sector")

        # 2️⃣ Fetch Deals board
        deals_json = fetch_board_items(DEALS_BOARD_ID)
        trace.append("Fetched Deals board via live API")

        deals_df = board_json_to_df(deals_json)
        trace.append(f"Deals rows retrieved: {len(deals_df)}")

        result_data = ""

        # ---------------------------------------------------
        # PIPELINE
        # ---------------------------------------------------
        if intent == "pipeline":
            total = pipeline_this_quarter(deals_df, sector)
            result_data = f"Pipeline Total: ${total:,.2f}"

        # ---------------------------------------------------
        # REVENUE
        # ---------------------------------------------------
        elif intent == "revenue":
            total = revenue_this_quarter(deals_df, sector)
            result_data = f"Revenue Total: ${total:,.2f}"

        # ---------------------------------------------------
        # COMPARE
        # ---------------------------------------------------
        elif intent == "compare":
            work_json = fetch_board_items(WORK_ORDERS_BOARD_ID)
            trace.append("Fetched Work Orders board via live API")

            work_df = board_json_to_df(work_json)

            revenue_total = revenue_this_quarter(deals_df)
            work_total = completed_work_orders_this_quarter(work_df)

            execution_rate = (
                (work_total / revenue_total) * 100
                if revenue_total > 0 else 0
            )

            result_data = f"""
Revenue: ${revenue_total:,.2f}
Work Orders: ${work_total:,.2f}
Execution Rate: {execution_rate:.1f}%
"""

        # ---------------------------------------------------
        # DEFAULT BREAKDOWN
        # ---------------------------------------------------
        else:
            breakdown = pipeline_by_sector(deals_df)
            result_data = str(breakdown)

        # 3️⃣ Generate executive summary
        summary = generate_summary(user_input, result_data)
        trace.append("Groq generated executive summary")

        return {
            "summary": summary,
            "trace": build_trace(trace, query_time)
        }

    except Exception as e:
        return {
            "summary": f"⚠ Error: {str(e)}",
            "trace": build_trace(trace, query_time)
        }


# ============================================================
# Trace Builder
# ============================================================

def build_trace(trace_list, query_time):

    return f"""
🔍 Agent Trace
{"\n".join(trace_list)}
Query Time: {query_time}
""".strip()