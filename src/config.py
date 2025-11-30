from dotenv import load_dotenv
import os

load_dotenv()

APP_IDS = {
    "CBE": os.getenv("CBE_APP_ID","com.combanketh.mobilebanking"),
    "BOA" : os.getenv("BOA_APP_ID","com.boa.boaMobileBanking"),
    "DB" : os.getenv("DB_APP_ID","com.dashen.dashensuperapp")
}
BANK_NAMES = {
    "CBE": "Commercial Bank of Ethiopia",
    "BOA" : "Bank of Abyssinia",
    "DB" : "Dashen Bank"
}
SCRAPING_CONFIG = {
    "reviews_per_bank" : os.getenv("REVIEWS_PER_BANK", 400),
    "max_retries": os.getenv("MAX_RETRIES", 3),
    "lang": "en",
    "country": "et"
}
DATA_PATHES = {
    "raw": "../data/raw",
    "processed": "../data/processed",
    "sentiment_results": "../data/sentiment_results",
    "final": "../data/final"
}