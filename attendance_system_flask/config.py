import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "a_very_secret_key_that_should_be_changed"
    SUPABASE_URL = "https://zdtxdpbmksaznbhjepjp.supabase.co"
    SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InpkdHhkcGJta3Nhem5iaGplcGpwIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3NTY2NjI5MiwiZXhwIjoyMDkxMjQyMjkyfQ.TA-d5_iv-EmVr9OlMXm9m5Vyirf2IzwckTYNwfL_kxY"

