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

# ── Phiz  ──
PHIZ_API_SERVER = os.getenv("PHIZ_API_SERVER", "")
PHIZ_APP_ID = os.getenv("PHIZ_APP_ID", "")
PHIZ_PERSONAL_ACCESS_TOKEN = os.getenv("PHIZ_PERSONAL_ACCESS_TOKEN", "")

