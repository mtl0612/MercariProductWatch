import os
from slack import WebClient
from slack.errors import SlackApiError

import logging 

class SlackBot:
    client = WebClient(token='xoxb-1181594001541-1309684331156-6GjG5KNdMoQGZreyyxMJ99Wf')
    def send_message(self,message):
        try:
            response = self.client.chat_postMessage(channel='#mercariproductwatch11', text=message)
        except SlackApiError as e:
            logging.error(f"Can not send message with Slack. Get error: {e.response['error']}")

if __name__ == "__main__":
    bot = SlackBot()
    bot.send_message("Test")