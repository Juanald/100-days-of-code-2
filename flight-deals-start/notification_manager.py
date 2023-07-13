import auth, requests

class NotificationManager:
    #This class is responsible for sending notifications with the deal flight details.
    def __init__(self) -> None:
        self.token = auth.TELEGRAM_BOT_TOKEN
        self.chat_id = auth.CHAT_ID
    
    def send_message(self, msg):
        send_text = f'https://api.telegram.org/bot{self.token}/sendMessage?chat_id={self.chat_id}&parse_mode=Markdown&text={msg}'
        response = requests.get(send_text)
        response.raise_for_status()
        return response.json()
