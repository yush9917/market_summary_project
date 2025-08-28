import requests
from datetime import datetime
import os

# --- Search Agent ---
class SearchAgent:
    def run(self):
        url = "https://api.tavily.com/v1/search"
        headers = {
            "Authorization": "Bearer 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"
        }
        params = {
            "query": "US stock market",
            "topic": "news",
            "search_depth": "basic",
            "max_results": 5,
            "days": 7
        }
        response = requests.get(url, headers=headers, params=params)
        data = response.json()
        news = [item['title'] for item in data.get('results', [])]
        return news

# --- Summary Agent ---
class SummaryAgent:
    def run(self, news_list):
        summary = "Today's Market Summary:\n\n"
        for item in news_list:
            summary += f"- {item}\n"
        return summary

# --- Formatting Agent ---
class FormattingAgent:
    def run(self, summary):
        formatted_summary = summary + "\n\nCharts:\n"
        formatted_summary += "- Chart1: https://example.com/chart1.png\n"
        formatted_summary += "- Chart2: https://example.com/chart2.png\n"
        return formatted_summary

# --- Translation Agent ---
class TranslationAgent:
    def run(self, text, language='Hindi'):
        translations = {
            'hindi': "हिंदी में सारांश:\n",
            'arabic': "ملخص باللغة العربية:\n",
            'hebrew': "תקציר בעברית:\n"
        }
        prefix = translations.get(language.lower(), "")
        return prefix + text

# --- Telegram Agent ---
class TelegramAgent:
    def __init__(self):
        self.bot_token = "8407926127:AAEdjnXQeRGPoG6e-MfPs92UzARMAjAAUQQ"
        self.chat_id = "-1002973273627"  # aapka channel ID

    def run(self, message):
        url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
        payload = {
            "chat_id": self.chat_id,
            "text": message,
            "parse_mode": "HTML"
        }
        response = requests.post(url, data=payload)
        return response.status_code, response.json()

# --- Main Function ---
def main():
    log_file = os.path.join(os.path.dirname(__file__), "market_summary.log")
    try:
        search_agent = SearchAgent()
        news = search_agent.run()

        summary_agent = SummaryAgent()
        summary = summary_agent.run(news)

        formatting_agent = FormattingAgent()
        formatted_summary = formatting_agent.run(summary)

        translation_agent = TranslationAgent()
        translated_summary = translation_agent.run(formatted_summary, language='Hindi')

        telegram_agent = TelegramAgent()
        status, resp = telegram_agent.run(translated_summary)

        # Logging
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(f"{datetime.now()} - Message status: {status}, Response: {resp}\n")

    except Exception as e:
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(f"{datetime.now()} - Error occurred: {e}\n")

# --- Run Main ---
if __name__ == "__main__":
    main()
