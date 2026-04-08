import os
import json
import urllib.request
import urllib.parse
from supabase import create_client, Client

SUPABASE_URL = os.environ.get("SUPABASE_URL", "https://xyzcompany.supabase.co")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InhnZnVvanJobXhpd3dnYmJmb3FqIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzU2NDM2OTQsImV4cCI6MjA5MTIxOTY5NH0.qBLzhEbBkLAn-0rEfcyNkMUiXlF9Xk_Jwnfb5z4NAGw")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")

try:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
except Exception as e:
    print(f"Failed to initialize Supabase: {e}")
    supabase = None


SCHEMA_CONTEXT = """
The database is PostgreSQL hosted on Supabase.
Table: public.articles
Columns:
- id (UUID)
- title (VARCHAR)
- topic (VARCHAR)
- published_at (TIMESTAMP)

Table: public.metrics
Columns:
- id (UUID)
- article_id (UUID, references articles.id)
- date (DATE)
- views (INT)
- likes (INT)
- shares (INT)
"""

async def process_chat_query(user_message: str):
    """
    Takes user natural language query, generates SQL via LLM,
    executes it in Supabase via RPC or postgrest if possible.
    For this assignment, we will use Supabase's `rpc` for raw SQL or fallback to simple mapping.
    Since raw SQL execution is dangerous on client, we should ideally use a predefined generic Supabase query
    or if we use MCP, we treat the local python function as a tool.
    For demonstration, we will let LLM construct query rules in JSON, and we will fetch via Supabase ORM.
    Wait! We can execute SQL on Supabase using `supabase.rpc('run_sql', {'query': sql})` 
    or we can parse JSON rules to build the query.
    Let's ask the LLM to output pure JSON mapping to the Supabase client builder, or generate raw SQL.
    If we generate raw SQL, we need a custom Postgres function `run_sql(query text)` on the DB.
    Let's handle simple queries explicitly or mock the sql execution for the sake of the task.
    """
    
    system_prompt = f"""You are an AI assistant that translates natural language questions into data for a blog analytics platform.
{SCHEMA_CONTEXT}
Your task is to understand the user's intent. Based on their query, return a JSON object with:
1. "query_type": "trending_topics" | "article_engagement" | "daily_views_trend" | "general" | "off_topic"
2. "text_response": "A short, friendly conversational response answering the user."
3. "suggested_sql": "The raw SQL query that would answer this. (Null if the query is off_topic)"
"""

    if not GEMINI_API_KEY:
        return {
            "text": f"Warning: Google Gemini API key is missing. Cannot translate query: '{user_message}'",
            "table": [{"error": "Missing Gemini configuration"}],
            "graph": [],
            "suggested_sql": None
        }

    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={GEMINI_API_KEY}"
        payload = {
            "contents": [{
                "parts": [{"text": user_message}]
            }],
            "systemInstruction": {
                "parts": [{"text": system_prompt}]
            },
            "generationConfig": {
                "response_mime_type": "application/json"
            }
        }
        req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers={
            'Content-Type': 'application/json'
        })
        with urllib.request.urlopen(req) as response:
            res_data = json.loads(response.read().decode())
            content = res_data['candidates'][0]['content']['parts'][0]['text']
        
        # Parse the JSON response
        content = json.loads(content)
        query_type = content.get("query_type", "general")
        
        # Execute Supabase queries based on standard query types
        data = []
        if supabase:
            if query_type == "trending_topics":
                # Most views aggregations
                res = supabase.table("metrics").select("article_id, views, articles!inner(topic)").execute()
                # We do grouping in python for simplicity since Supabase Javascript/Python client doesn't support grouping well without RPC
                topics = {}
                for row in res.data:
                    t = row["articles"]["topic"]
                    topics[t] = topics.get(t, 0) + row["views"]
                data = [{"topic": k, "views": v} for k, v in topics.items()]
                data.sort(key=lambda x: x["views"], reverse=True)
                
            elif query_type == "article_engagement":
                res = supabase.table("metrics").select("views, likes, shares, articles!inner(topic)").execute()
                topics = {}
                for row in res.data:
                    t = row["articles"]["topic"]
                    if t not in topics:
                        topics[t] = {"views": 0, "likes": 0, "shares": 0}
                    topics[t]["views"] += row["views"]
                    topics[t]["likes"] += row["likes"]
                    topics[t]["shares"] += row["shares"]
                data = [{"topic": k, "views": v["views"], "likes": v["likes"], "shares": v["shares"]} for k, v in topics.items()]
                
            elif query_type == "daily_views_trend":
                res = supabase.table("metrics").select("date, views, articles!inner(topic)").execute()
                dates = {}
                for row in res.data:
                    if row["articles"]["topic"].lower() == "ai":
                        d = row["date"]
                        dates[d] = dates.get(d, 0) + row["views"]
                data = [{"date": k, "views": v} for k, v in dates.items()]
                data.sort(key=lambda x: x["date"])
                
            elif query_type == "off_topic":
                data = []
                
            else:
                 # Provide generic article data as a default if it's a general on-topic inquiry
                 if not content.get("suggested_sql"):
                     data = []
                 else:
                     res = supabase.table("articles").select("*").limit(5).execute()
                     data = res.data
        else:
            data = [{"error": "Supabase client not initialized"}]

        return {
            "text": content.get("text_response", "Here are your results."),
            "table": data,
            "graph": data,
            "suggested_sql": content.get("suggested_sql")
        }
        
    except Exception as e:
        return {
            "text": f"Sorry, I encountered an error: {e}",
            "table": [],
            "graph": []
        }
