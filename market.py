import yfinance as yf
import time

TROY_OUNCE_TO_GRAM = 31.1035
ASSET_MAP = {
    "gold": "GC=F",
    "silver": "SI=F",
    "usd_inr": "INR=X"
}

price_cache = {
    "data": {},
    "last_updated": 0
}

def get_live_prices():
    current_time = time.time()
    if current_time - price_cache["last_updated"] < 60:
        return price_cache["data"]

    prices = {}
    try:
        usd_inr = yf.Ticker(ASSET_MAP["usd_inr"]).fast_info['last_price']
        
        for asset, ticker in ASSET_MAP.items():
            if asset == "usd_inr": continue
            
            raw_price = yf.Ticker(ticker).fast_info['last_price']
            price_per_gram_inr = (raw_price / TROY_OUNCE_TO_GRAM) * usd_inr
            prices[asset] = round(price_per_gram_inr, 2)
    except Exception as e:
        # Fallback if yfinance is temporarily down
        prices = {"gold": 7500.00, "silver": 90.00}
    
    price_cache["data"] = prices
    price_cache["last_updated"] = current_time
    return prices