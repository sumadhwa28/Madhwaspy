import google.generativeai as genai
from database import get_db_connection
from datetime import datetime, timedelta

# 🛑 ADD YOUR GEMINI API KEY HERE 🛑
genai.configure(api_key="YOUR_GEMINI_API_KEY")
model = genai.GenerativeModel('gemini-1.5-flash')

def get_market_news(asset):
    conn = get_db_connection()
    cache_limit = (datetime.now() - timedelta(minutes=15)).isoformat()
    cached = conn.execute('SELECT * FROM news_cache WHERE asset = ? AND created_at > ?', 
                         (asset, cache_limit)).fetchone()
    
    if cached:
        conn.close()
        return {"title": cached['title'], "snippet": cached['snippet'], "sentiment": cached['sentiment']}

    try:
        prompt = f"Analyze current {asset} market. Return: Title, 1-sentence snippet, and Sentiment (Bullish/Bearish/Neutral). Format: Title|Snippet|Sentiment"
        response = model.generate_content(prompt).text
        
        title, snippet, sentiment = response.split('|')
        conn.execute('INSERT INTO news_cache (asset, title, snippet, sentiment, created_at) VALUES (?,?,?,?,?)',
                     (asset, title.strip(), snippet.strip(), sentiment.strip(), datetime.now().isoformat()))
        conn.commit()
    except Exception as e:
        title, snippet, sentiment = f"{asset.capitalize()} Market Update", "Data currently unavailable or API key not set.", "Neutral"
    
    conn.close()
    return {"title": title, "snippet": snippet, "sentiment": sentiment}