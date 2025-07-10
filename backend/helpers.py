from supabase import create_client
import os
from dotenv import load_dotenv
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_API_KEY = os.getenv("SUPABASE_API_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_API_KEY)

def get_top_category_from_db(username):
    query = (
        supabase.table("payments")
        .select("category", "withdrawal")
        .eq("username", username)
        .eq("is_fraud", False)
        .execute()
    )
    data = query.data or []
    if not data:
        return None

    totals = {}
    for item in data:
        cat = item["category"]
        amt = item["withdrawal"] or 0
        totals[cat] = totals.get(cat, 0) + amt

    if not totals:
        return None
    return max(totals.items(), key=lambda x: x[1])[0]
