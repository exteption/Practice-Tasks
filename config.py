
import os


SOURCE_NAME = 'GitHub Trending'
BASE_URL    = 'https://github.com/trending'
BASE_URL_2  = 'https://github.com/trending?spoken_language_code=ru'


DATA_DIR   = os.path.join(os.path.dirname(__file__), 'data')
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), 'output')
SNAPSHOT_1 = os.path.join(DATA_DIR, 'snapshot_1.csv')
SNAPSHOT_2 = os.path.join(DATA_DIR, 'snapshot_2.csv')


HEADERS = {
    'User-Agent': (
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
        'AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/120.0 Safari/537.36'
    )
}
REQUEST_DELAY = 1.5   
TIMEOUT       = 15    


CSV_FIELDS = ['repo', 'owner', 'language', 'stars', 'forks',
              'description', 'scraped_at']

os.makedirs(DATA_DIR,   exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)
