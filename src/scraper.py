# create a scraper object
from google_play_scraper import app,sort,reviews
import pandas as pd
from config import SCRAPING_CONFIG, APP_IDS, BANK_NAMES, DATA_PATHES
from fileLoader import FileLoader
import time
class Scraper:
    def __init__(self,):
        self.app_ids = APP_IDS
        self.bank_names = BANK_NAMES
        self.max_retries = SCRAPING_CONFIG["max_retries"]
        self.reviews_per_bank = SCRAPING_CONFIG["reviews_per_bank"]
        self.lang = SCRAPING_CONFIG["lang"]
        self.country = SCRAPING_CONFIG["country"]
    
    def get_scraper_info(self):
        return {
            "app_ids": self.app_ids,
            "bank_names": self.bank_names,
            "max_retries": self.max_retries,
            "reviews_per_bank": self.reviews_per_bank,
            "lang": self.lang,
            "country": self.country
        }
    
    def get_reviews(self,app_id, count=400):
        # scrape reviews from google play store
        print(f"Scraping {count} reviews from {self.bank_names[app_id]}")
        for i in range(self.max_retries):
            try:
                result, _ = reviews(
                    app_id,
                    lang=self.lang,
                    country=self.country,
                    sort=sort.NEWEST,
                    count=count,
                    filter_score_with=None,
                )
                return result
            except Exception as e:
                print("failed at attempt", i)
                if i < self.max_retries-1:
                    print(f"Sleeping for 5 seconds before retrying")
                    time.sleep(5)
                else:
                    print(f"Failed after {self.max_retries} attempts")
                    return []
    
    