import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("CORALOGIX_API_KEY")
BASE_URL = os.getenv("CORALOGIX_REGION")
HF_API_KEY = os.getenv("HF_API_KEY")
