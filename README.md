#  Monday.com BI Agent  
### AI-Powered Real-Time Business Intelligence Assistant

An intelligent BI agent that converts natural language into actionable business insights using live data from monday.com.  
Built with a modular AI architecture, this system enables decision-makers to query business metrics instantly—without dashboards or manual analysis.

---

##  Why This Project Stands Out

-  Real-time insights — No caching, always fresh data  
-  LLM-powered intelligence — Converts human queries → structured analytics  
-  Production-style architecture — Modular, scalable, and maintainable  
-  Full transparency — Step-by-step agent decision trace  
-  Handles messy data — Built for real-world datasets  

---

##  Architecture
```bash
User Query
↓
LLM Intent Parser (Groq)
↓
Agent Orchestrator
↓
Live API Fetch (Monday.com GraphQL)
↓
Data Cleaning + Validation
↓
BI Engine (Metrics Computation)
↓
Response Generator + Trace Logs
```
---


---

##  Live Data Integration

- Direct integration with monday.com via GraphQL API  
- Query-time fetching (no preloading or caching)  
- Ensures 100% real-time accuracy  

---

##  Transparency

The agent provides full execution trace:

- Intent interpretation  
- API calls  
- Data processing steps  

 Displayed in UI as **Agent Trace Logs**

---

##  Tech Stack

- Python  
- Streamlit  
- Pandas  
- Groq (LLM)  
- GraphQL API  

---

##  Project Structure
```bash
agent.py # Core orchestration
app.py # Streamlit UI
config.py # Secrets/config
monday_client.py # API integration
data_cleaning.py # Data normalization
bi_engine.py # Metrics computation
intent_parser.py # LLM-based intent extraction
data_quality.py # Data validation
summary_generator.py # Response generation
requirements.txt
```
---

---

##  Quick Start (Local)

```bash
git clone https://github.com/Safeeeeer/monday-bi-agent
cd bi-agent
pip install -r requirements.txt
streamlit run app.py
```
---

##  Secrets Configuration

###  Streamlit Cloud 

Secrets are securely stored using Streamlit Cloud Secrets (no local file needed).

Go to:  
**App Settings → Secrets**

Add:

```toml
GROQ_API_KEY = "your_key"
MONDAY_API_KEY = "your_key"
DEALS_BOARD_ID = "your_board_id"
WORK_ORDERS_BOARD_ID = "your_board_id"

```
---

##  Design Decisions

- No caching → prioritizes correctness over speed  
- Modular architecture → scalable and maintainable  
- LLM + rules → balance between flexibility and control  

 Decision Log:  https://drive.google.com/file/d/1eFcrbGa3Ltc40WQVRMYG2HD4I3kAU69h/view?usp=sharing

---


##  Future Improvements

- Advanced query understanding  
- Custom time filters  
- Interactive dashboards  
- Forecasting and anomaly detection  

---

##  Author

Muhammed Safeer K
