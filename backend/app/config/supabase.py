# app/config/supabase.py
from supabase import create_client, Client
from .settings import settings

class SupabaseClient:
    def __init__(self):
        self.url = settings.SUPABASE_URL
        self.service_key = settings.SUPABASE_SERVICE_KEY
        
        self.client: Client = create_client(self.url, self.service_key)

supabase_client = SupabaseClient()