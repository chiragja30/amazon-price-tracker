import sys
sys.stdout.reconfigure(line_buffering=True)

import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime, timedelta
import time
import random
import os
import pytz  # For Indian timezone
from openpyxl import load_workbook

# ----------------------------
# ENV DETECTION
# ----------------------------
IS_GITHUB = os.getenv("GITHUB_ACTIONS") == "true"

# ----------------------------
# 1. PRODUCT LIST (UPDATED)
# ----------------------------
URLS = [
    "https://amzn.in/d/bqE35ja", "https://amzn.in/d/8DkcqwJ", "https://amzn.in/d/27dBhA1",
    "https://amzn.in/d/5fRuGGr", "https://amzn.in/d/i9MHRbf", "https://amzn.in/d/4mstrat",
    "https://amzn.in/d/8D9SlMj", "https://amzn.in/d/0V4kPll", "https://amzn.in/d/bGuw5EZ",
    "https://amzn.in/d/aNPi1U2", "https://amzn.in/d/isCQv09", "https://amzn.in/d/7mqmyMs",
    "https://amzn.in/d/axvUrmf", "https://amzn.in/d/0D9RJyQ", "https://amzn.in/d/iUJnAAG",
    "https://amzn.in/d/fCdbdzb", "https://amzn.in/d/fGRPZHm", "https://amzn.in/d/d8JD7Ef",
    "https://amzn.in/d/9Vmpx9L", "https://amzn.in/d/1yTk7TG", "https://amzn.in/d/amDxu6e",
    "https://amzn.in/d/8MCAq5Z", "https://amzn.in/d/8Xctx1i", "https://amzn.in/d/fETFYB9",
    "https://amzn.in/d/eQdsGNY",
    "https://amzn.in/d/9pq9YSq", "https://amzn.in/d/dtZzFoi",
    "https://amzn.in/d/9inaJOw", "https://amzn.in/d/9XD40k7",
    "https://amzn.in/d/htTfjgp", "https://amzn.in/d/2ryRfHD",
]

# ----------------------------
# 2. USER AGENTS (45+ DEVICES)
# ----------------------------
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/121.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 11.0; Win64; x64) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; rv:123.0) Gecko/20100101 Firefox/123.0",
    "Mozilla/5.0 (Windows NT 11.0; rv:122.0) Gecko/20100101 Firefox/122.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_3) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_2) Chrome/121.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_1) Safari/605.1.15",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_6) Safari/605.1.15",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 12_7) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64; rv:123.0) Gecko/20100101 Firefox/123.0",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64) Chrome/121.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Fedora; Linux x86_64) Firefox/122.0",
    "Mozilla/5.0 (Linux; Android 14; Pixel 8 Pro) Chrome/122.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 14; Pixel 7) Chrome/121.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; SM-S918B) Chrome/121.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; SM-A536B) Chrome/120.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 12; Redmi Note 11) Chrome/119.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 11; OnePlus 9) Chrome/118.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 10; SM-G973F) Chrome/117.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 9; Mi A2) Chrome/116.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X) Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_3 like Mac OS X) Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_7 like Mac OS X) Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 15_8 like Mac OS X) Safari/604.1",
    "Mozilla/5.0 (iPad; CPU OS 17_3 like Mac OS X) Safari/604.1",
    "Mozilla/5.0 (iPad; CPU OS 16_6 like Mac OS X) Safari/604.1",
    "Mozilla/5.0 (iPad; CPU OS 15_8 like Mac OS X) Safari/604.1",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Edg/122.0.0.0 Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 11.0; Win64; x64) Edg/121.0.0.0 Chrome/121.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_6) Edg/121.0.0.0 Chrome/121.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) OPR/106.0.0.0 Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) Vivaldi/6.6 Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) Chrome/117.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) Chrome/116.0.0.0 Safari/537.36",
]

# ----------------------------
# REFERERS
# ----------------------------
REFERERS = [
    "https://www.google.com/",
    "https://www.amazon.in/",
    "https://www.bing.com/"
]

# ----------------------------
# CONFIG
# ----------------------------
FILENAME = "price_tracker_final.xlsx"
IST = pytz.timezone("Asia/Kolkata")

# ----------------------------
# ENSURE EXCEL EXISTS
# ----------------------------
def ensure_excel_file():
    if not os.path.exists(FILENAME):
        pd.DataFrame(columns=["SKU Name", "Product URL"]).to_excel(FILENAME, index=False)

# ----------------------------
# AMAZON SCRAPER
# ----------------------------
def get_amazon_data(url):
    for attempt in range(1, 4):
        time.sleep(random.uniform(4, 7) if IS_GITHUB else random.uniform(8, 15))
        try:
            headers = {
                "User-Agent": random.choice(USER_AGENTS),
                "Accept-Language": "en-IN,en;q=0.9",
                "Referer": random.choice(REFERERS),
                "Connection": "keep-alive"
            }

            r = requests.get(url, headers=headers, timeout=15)
            if r.status_code != 200:
                continue

            soup = BeautifulSoup(r.text, "html.parser")
            title = soup.find("span", id="productTitle")
            price = soup.select_one(".a-price-whole") or soup.select_one(".apexPriceToPay .a-offscreen")

            if not title or not price:
                continue

            price_val = int("".join(filter(str.isdigit, price.text.replace(",", ""))))
            return {
                "Product": title.text.strip(),
                "Price": price_val,
                "URL": url
            }
        except Exception:
            pass
    return None

# ----------------------------
# TRACKER
# ----------------------------
def run_price_tracker():
    run_time = datetime.now(IST).strftime("%Y-%m-%d %H:%M")
    df = pd.read_excel(FILENAME)

    if "SKU Name" not in df.columns:
        df.insert(0, "SKU Name", "")
    if "Product URL" not in df.columns:
        df.insert(1, "Product URL", "")
    if run_time not in df.columns:
        df.insert(2, run_time, "")

    random.shuffle(URLS)

    for url in URLS:
        data = get_amazon_data(url)
        if not data:
            continue

        sku = data["Product"]
        price = data["Price"]
        link = data["URL"]

        if sku in df["SKU Name"].values:
            df.loc[df["SKU Name"] == sku, run_time] = price
        else:
            row = {c: "" for c in df.columns}
            row["SKU Name"] = sku
            row["Product URL"] = link
            row[run_time] = price
            df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)

    df.to_excel(FILENAME, index=False)

    wb = load_workbook(FILENAME)
    ws = wb.active
    url_col = list(df.columns).index("Product URL") + 1

    for r in range(2, ws.max_row + 1):
        cell = ws.cell(row=r, column=url_col)
        if cell.value:
            cell.hyperlink = cell.value
            cell.style = "Hyperlink"

    for col in ws.columns:
        ws.column_dimensions[col[0].column_letter].width = (
            max(len(str(c.value)) if c.value else 0 for c in col) + 5
        )

    wb.save(FILENAME)

# ----------------------------
# MAIN
# ----------------------------
if __name__ == "__main__":
    ensure_excel_file()
    run_price_tracker()
