import os
from dotenv import load_dotenv

load_dotenv()

# ── Database ──
DATABASE_URL = os.getenv("DATABASE_URL")

# ── Email ──
FROM_EMAIL = os.getenv("FROM_ADDRESS")
FROM_PASSWORD = os.getenv("FROM_PASSWORD")

# ── App ──
BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")
TOKEN_EXPIRY_MINUTES = 30
