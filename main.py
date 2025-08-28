import requests
from datetime import datetime
import os
import openai

# --- API Keys ---
OPENAI_API_KEY = "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"
FINNHUB_API_KEY = "d2nm0jpr01qs6r4chdtgd2nm0jpr01qs6r4chdu0"
TELEGRAM_BOT_TOKEN = "8407926127:AAEdjnXQeRGPoG6e-MfPs92UzARMAjAAUQQ"
TELEGRAM_CHAT_ID = "-1002973273627"

client = openai.OpenAI(api_key=OPENAI_API_KEY)

# --- Search Agent ---
class SearchAgent:
    def run(self):
        url = "https://finnhub.io/api/v1/news"
        params = {"category": "general", "token": FINNHUB_API_KEY}
        response = requests.get(url, params=params)
        data = response.json()
        news = [item['headline'] for item in data[:5]]  # top 5 news only
        return news

# --- Summary Agent ---
class SummaryAgent:
    def run(self, news_list):
        prompt = "Summarize the following financial market news in 5-6 lines, professional tone:\n" + "\n".join(news_list)
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=200
        )
        summary = response.choices[0].message.content
        return summary

# --- Market Price Agent ---
class MarketPriceAgent:
    def run(self):
        symbols = ["AAPL", "TSLA", "MSFT"]
        prices = []
        for symbol in symbols:
            url = f"https://finnhub.io/api/v1/quote?symbol={symbol}&token={FINNHUB_API_KEY}"
            resp = requests.get(url).json()
            current_price = resp.get("c")
            prices.append(f"{symbol}: ${current_price}")
        return "\n".join(prices)

# --- Telegram Agent ---
class TelegramAgent:
    def run(self, message):
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message, "parse_mode": "HTML"}
        requests.post(url, data=payload)

# --- Main Function ---
def main():
    log_file = os.path.join(os.path.dirname(__file__), "market_summary.log")
    try:
        search_agent = SearchAgent()
        news = search_agent.run()

        summary_agent = SummaryAgent()
        summary = summary_agent.run(news)

        price_agent = MarketPriceAgent()
        prices = price_agent.run()

        today = datetime.now().strftime("%Y-%m-%d")
        final_message = f"📊 Daily Market Summary ({today})\n\n{summary}\n\n💹 Stock Prices:\n{prices}"

        telegram_agent = TelegramAgent()
        telegram_agent.run(final_message)

        with open(log_file, "a", encoding="utf-8") as f:
            f.write(f"{datetime.now()} - Message sent successfully.\n")

    except Exception as e:
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(f"{datetime.now()} - Error occurred: {e}\n")

# --- Run ---
if __name__ == "__main__":
    main()
