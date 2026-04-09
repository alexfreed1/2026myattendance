import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env before anything reads os.environ
load_dotenv(Path(__file__).parent / ".env")

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'fallback-dev-secret-key'
    SUPABASE_URL = os.environ.get('SUPABASE_URL')
    SUPABASE_KEY = os.environ.get('SUPABASE_KEY')
