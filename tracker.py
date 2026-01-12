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
    # New URLs added
    "https://amzn.in/d/9pq9YSq", 
    "https://amzn.in/d/dtZzFoi",
    "https://amzn.in/d/9inaJOw", 
    "https://amzn.in/d/9XD40k7", 
    "https://amzn.in/d/htTfjgp",
    "https://amzn.in/d/2ryRfHD",
]

# ----------------------------
# 2. USER AGENTS (EXPANDED BY 30+)
# ----------------------------
USER_AGENTS = [
    # --- ORIGINAL LIST ---
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; rv:121.0) Firefox/121.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_6_3) Safari/605.1.15",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 12_7_1) Chrome/118.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) Firefox/120.0",
    "Mozilla/5.0 (Windows NT 10.0) Firefox/119.0",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) Chrome/117.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_7_10) Safari/605.1.15",
    "Mozilla/5.0 (Linux; Android 13) Chrome/120.0.6099.144 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 12) Chrome/119.0.6045.193 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 11) Chrome/118.0.5993.90 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 10) Chrome/117.0.5938.132 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 9) Chrome/116.0.5845.92 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_2) Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_7_3) Safari/604.1",
    "Mozilla/5.0 (iPad; CPU OS 17_1) Safari/604.1",
    "Mozilla/5.0 (iPad; CPU OS 16_6) Safari/604.1",
    "Mozilla/5.0 (Windows NT 6.1) Chrome/116.0.5845.140 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) Chrome/117.0.5938.149 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) Chrome/118.0.5993.88 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0) Firefox/118.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5) Chrome/119.0.0.0 Safari/537.36",

    # --- NEWLY ADDED AGENTS (Modern Chrome, Edge, Safari, Firefox) ---
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_2_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:123.0) Gecko/20100101 Firefox/123.0",
    "Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:122.0) Gecko/20100101 Firefox/122.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0",
    "Mozilla/5.0 (Linux; Android 14; Pixel 8 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 14; SM-S918B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.3 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU OS 17_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.3 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Windows NT 11.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 11.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 OPR/106.0.0.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Vivaldi/6.6.3271.45",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_3) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.3 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.2365.66",
    "Mozilla/5.0 (Linux; Android 13; SM-A536B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36"
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
        pd.DataFrame(columns=["SKU Name"]).to_excel(FILENAME, index=False)
        print("📄 Excel file created for first run", flush=True)

# ----------------------------
# AMAZON SCRAPER
# ----------------------------
def get_amazon_data(url):
    for attempt in range(1, 4):
        print(f" Fetching ({attempt}/3): {url}", flush=True)

        delay = random.uniform(3, 6) if IS_GITHUB else random.uniform(10, 18)
        time.sleep(delay)

        try:
            headers = {
                "User-Agent": random.choice(USER_AGENTS),
                "Accept-Language": "en-IN,en-GB,en;q=0.9",
                "Referer": random.choice(REFERERS),
                "Accept-Encoding": "gzip, deflate, br",
                "Connection": "keep-alive"
            }

            response = requests.get(url, headers=headers, timeout=15)

            if response.status_code != 200:
                continue

            if "automated access" in response.text.lower():
                print("⚠️ Amazon blocked request", flush=True)
                continue

            soup = BeautifulSoup(response.text, "html.parser")
            title = soup.find("span", {"id": "productTitle"})
            price = soup.select_one(".a-price-whole") or soup.select_one(".apexPriceToPay .a-offscreen")

            if not title or not price:
                continue

            price_val = int("".join(filter(str.isdigit, price.text.replace(",", ""))))
            return {"Product": title.text.strip(), "Price": price_val}

        except Exception as e:
            print(f"❌ Error: {e}", flush=True)

    return None

# ----------------------------
# TRACKER
# ----------------------------
def run_price_tracker():
    print("🚀 Tracker started", flush=True)

    # ✅ FIX: unique IST timestamp
    run_time = datetime.now(IST).strftime("%Y-%m-%d %H:%M")

    if os.path.exists(FILENAME):
        df = pd.read_excel(FILENAME)
    else:
        df = pd.DataFrame(columns=["SKU Name"])

    if "SKU Name" not in df.columns:
        df.insert(0, "SKU Name", "")

    if run_time not in df.columns:
        df.insert(1, run_time, "")

    random.shuffle(URLS)

    for i, url in enumerate(URLS, 1):
        print(f"[{i}/{len(URLS)}] Processing product", flush=True)
        data = get_amazon_data(url)
        if not data:
            continue

        sku, price = data["Product"], data["Price"]

        if sku in df["SKU Name"].values:
            df.loc[df["SKU Name"] == sku, run_time] = price
        else:
            row = {c: "" for c in df.columns}
            row["SKU Name"] = sku
            row[run_time] = price
            df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)

    # ✅ SAFE: force git diff
    df.attrs["last_run_ist"] = datetime.now(IST).isoformat()

    with pd.ExcelWriter(FILENAME, engine="openpyxl", mode="w") as writer:
        df.to_excel(writer, index=False)
        ws = writer.sheets["Sheet1"]
        for col in ws.columns:
            ws.column_dimensions[col[0].column_letter].width = (
                max(len(str(cell.value)) if cell.value else 0 for cell in col) + 5
            )

    print("✅ Hourly data recorded (even if price unchanged).", flush=True)

# ----------------------------
# MAIN
# ----------------------------
if __name__ == "__main__":
    print("🏁 Script started", flush=True)
    ensure_excel_file()
    run_price_tracker()
