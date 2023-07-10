"""
This program seeks to get stock information(closing date for yesterday and day before), and check for a percentage increase/decrease. It must also get the relevent recent news data. Then send a telegram message to a bot informing price increase/decrease, headlines, and briefing. 
"""
import auth, requests, datetime
stock_api_key = auth.stock_api_key
news_api_key = auth.news_api_key

# Getting stock info
class StockBot():
    def __init__(self, ticker) -> None:
        self.ticker = ticker

    def get_dates(self):
        current_date = datetime.date.today()

        last_weekday = current_date

        while last_weekday.weekday() >= 5 or last_weekday.weekday() == 0:  # 5 and 6 represent Saturday and Sunday
            last_weekday -= datetime.timedelta(days=1)

        if last_weekday == 0:
            last_last_weekday = 4
        else:
            last_last_weekday = last_weekday - datetime.timedelta(days=1)
        
        return (last_weekday, last_last_weekday)

    def get_stock_change(self, ticker):
        days = self.get_dates()
        stock_api_parameters = {
            "function" : "TIME_SERIES_DAILY_ADJUSTED",
            "symbol" : ticker,
            "apikey" : stock_api_key
        }

        stock_api_url = f'https://www.alphavantage.co/query'
        response = requests.get(url=stock_api_url, params=stock_api_parameters)
        response.raise_for_status()

        data = response.json()['Time Series (Daily)']
        # We need close from previous day, and close from day before that
        prev_close = float(data[str(days[0])]['4. close'])
        prev_prev_close = float(data[str(days[1])]['4. close'])

        increase = prev_close - prev_prev_close
        percent_change = round(increase / prev_prev_close * 100, 2)
        return percent_change

    # Now we have to access relevant news using news api

    def get_stock_news(self, ticker):
        news_api_params = {
            "q" : ticker,
            "apikey" : news_api_key,
            "sortBy" : "popularity"
        }

        news_api_url = 'https://newsapi.org/v2/everything'
        news_response = requests.get(url=news_api_url, params=news_api_params)
        news_response.raise_for_status()
        news_data = news_response.json()['articles']
        article = news_data[0]
        return article

    def get_emoji(self, percentage):
        if percentage > 0:
            return "📈"
        else:
            return "📉"

    def send_telegram_message(self):
        article = self.get_stock_news(self.ticker)
        percent_change = self.get_stock_change(self.ticker)
        token = auth.bot_token
        title = article['title']
        description = article['description']
        source = article['source']['name']
        parameters = {
            "chat_id" : auth.chat_id,
            "text" : f"""
        From {source}! {ticker} {self.get_emoji(percent_change)} {percent_change}%!
        {title}
        {description}"""
        }
        url = f'https://api.telegram.org/bot{token}/sendMessage'
        

        response = requests.post(url, params=parameters)
        response.raise_for_status()
        return response

if __name__ == "__main__":
    ticker = "AMZN" # How do I make this interactive for the user?
    bot = StockBot(ticker)
    bot.send_telegram_message()