import time
import csv
from urllib.parse import quote_plus
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
import os

QUERIES = [
    "Boycott India",
    "India fascist",
    "Hindutva danger",
    "Modi resign",
    "India human rights abuse",
    "Anti India campaign",
    "Stop India violence",
    "Free Punjab Khalistan",
    "Against India army"
]

CSV_FILE = "tweets_dataset.csv"

options = Options()
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--start-maximized")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

driver.get("https://x.com/login")
time.sleep(60)

def scroll_and_collect(query, scrolls=35):
    print(f"🔍 Scraping query: {query}")
    search_url = f"https://x.com/search?q={quote_plus(query)}&src=typed_query&f=live"
    driver.get(search_url)
    time.sleep(5)

    collected = []
    last_height = driver.execute_script("return document.body.scrollHeight")

    for i in range(scrolls):
        driver.find_element(By.TAG_NAME, "body").send_keys(Keys.END)
        time.sleep(2 + (i % 3))# random-ish sleep to simulate human scroll

        soup = BeautifulSoup(driver.page_source, "html.parser")
        articles = soup.find_all("article")

        for article in articles:
            try:
                content = article.get_text(" ", strip=True)
                user_tag = article.find("a", href=True)
                user = user_tag["href"] if user_tag else "Unknown"
                time_tag = article.find("time")
                date = time_tag["datetime"] if time_tag else "Unknown"

                stats = article.find_all("span", string=lambda x: x and x.replace(',', '').isdigit())
                replies = stats[0].text if len(stats) > 0 else "0"
                retweets = stats[1].text if len(stats) > 1 else "0"
                likes = stats[2].text if len(stats) > 2 else "0"

                tweet = {
                    "query": query,
                    "user": user,
                    "date": date,
                    "content": content,
                    "replies": replies,
                    "retweets": retweets,
                    "likes": likes
                }
                if tweet not in collected:
                    collected.append(tweet)
            except (StaleElementReferenceException, IndexError, AttributeError):
                continue

        # stop if page height didn't change (no more tweets)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    return collected

all_tweets = []

for q in QUERIES:
    tweets = scroll_and_collect(q, scrolls=35)
    all_tweets.extend(tweets)

keys = ["query", "user", "date", "content", "replies", "retweets", "likes"]

if os.path.exists(CSV_FILE):
    with open(CSV_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writerows(all_tweets)
else:
    with open(CSV_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(all_tweets)

driver.quit()


# Priyans48875918