mport os
from supabase import create_client, Client

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def sync_to_supabase_auth(email: str):
    try:
        supabase.auth.admin.create_user({
            "email": email,
            "password": "TemporaryPassword123!",
            "email_confirm": True
        })
        print(f"Successfully synced {email} to Supabase Auth.")
    except Exception as e:
        print(f"Supabase sync skipped or errored: {e}")