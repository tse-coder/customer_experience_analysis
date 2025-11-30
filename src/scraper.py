# create a scraper object
from google_play_scraper import app, Sort,reviews
import pandas as pd
from config import SCRAPING_CONFIG, APP_IDS, BANK_NAMES, DATA_PATHES
from fileLoader import FileLoader
import time
class Scraper:
    def __init__(self):
        self.app_ids = APP_IDS
        self.bank_names = BANK_NAMES
        # ensure numeric types for config values
        try:
            self.max_retries = int(SCRAPING_CONFIG["max_retries"])
        except Exception:
            self.max_retries = 3
        try:
            self.reviews_per_bank = int(SCRAPING_CONFIG["reviews_per_bank"])
        except Exception:
            self.reviews_per_bank = 400
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
    
    def get_reviews(self, app_identifier, count=None):
        """Fetch reviews from Google Play.
        If `count` is None we'll use the configured `reviews_per_bank`.
        """
        count = count or int(self.reviews_per_bank)

        # normalize the app id: accept both bank key and package id
        if app_identifier in self.app_ids:
            app_id = self.app_ids[app_identifier]
            bank_label = self.bank_names.get(app_identifier)
        else:
            app_id = app_identifier
            # try to find a friendly bank name from the known mapping
            bank_label = None
            for k, v in self.app_ids.items():
                if v == app_id:
                    bank_label = self.bank_names.get(k)
                    break

        display_name = bank_label or app_id
        print(f"Scraping {count} reviews from {display_name} (app id='{app_id}')")

        for i in range(self.max_retries):
            try:
                result, _ = reviews(
                    app_id,
                    lang=self.lang,
                    country=self.country,
                    sort=Sort.NEWEST,
                    count=count,
                    filter_score_with=None,
                )
                # only take reviews, ratings, dates, and app names
                df = pd.DataFrame(result)
                out_df = pd.DataFrame()
                out_df['reviewId'] = df['reviewId']
                out_df['review'] = df['content']
                out_df['rating'] = df['score']
                out_df['date'] = df['at']
                out_df['app_name'] = display_name
                out_df['bank_name'] = bank_label
                file_loader = FileLoader(f"{DATA_PATHES["raw"]}/{app_id}.csv", out_df)
                file_loader.save()
                return out_df
            except Exception as e:
                # surface the error to help debugging (don't swallow details)
                print(f"failed at attempt {i} for app '{app_id}': {e}")
                if i < self.max_retries-1:
                    print(f"Sleeping for 5 seconds before retrying")
                    time.sleep(5)
                else:
                    print(f"Failed after {self.max_retries} attempts")
                    return []
    