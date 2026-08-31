import os
from dotenv import load_dotenv

load_dotenv()

# ── Database ──
DATABASE_URL = os.getenv("DATABASE_URL")

# ── Email ──
RESEND_API_KEY = os.getenv("RESEND_API_KEY")
RESEND_FROM_EMAIL = os.getenv("RESEND_FROM_EMAIL")

# ── App ──
BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")
TOKEN_EXPIRY_MINUTES = 30
