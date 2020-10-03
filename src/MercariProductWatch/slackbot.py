import os
from slack import WebClient
from slack.errors import SlackApiError

import logging 
import time
import random

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

requests_logger = logging.getLogger('requests')
requests_logger.setLevel(logging.INFO)

class SlackBot:
    client = WebClient(token='xoxb-1181594001541-1309684331156-6GjG5KNdMoQGZreyyxMJ99Wf')
    MAIN_CHANNEL = 'G018XEQ3MMG'
    USER_ID = 'U015K4GK6RJ'
    MESSAGES_PER_PAGE = 5
    def send_message(self,message, channel_id = None):
        if channel_id is None:
            channel_id = self.MAIN_CHANNEL
        try:
            time.sleep(random.random())
            response = self.client.chat_postMessage(channel=channel_id, text=message)
        except SlackApiError as e:
            logging.error(f"Can not send message with Slack. Get error: {e.response['error']}")
    def receive_message(self,ts = None):
        response = self.client.conversations_history(
            channel=self.MAIN_CHANNEL,
            limit=self.MESSAGES_PER_PAGE,
            oldest = ts
        )     
        for message in response['messages']:
            yield message

    def get_channels(self):
        response = self.client.conversations_list(  
            types="public_channel, private_channel"
        )
        conversations = response["channels"]
        for conversation in conversations:
            yield conversation
    
    def create_channel(self, channel_name):
        channel_name = channel_name.lower().replace(" ", "_")
        response = self.client.conversations_create(
            name=channel_name
            )
        channel_id = response["channel"]["id"]
        response = self.client.conversations_invite(channel=channel_id, users=self.USER_ID)        
        # response = self.client.conversations_archive(channel=channel_id)
        return channel_id

    def find_create_channel(self, channel_name):
        channel_name = channel_name.lower().replace(" ", "_")
        for channel in self.get_channels():
            if channel_name == channel['name']:
                return channel['id']
        return self.create_channel(channel_name)
    
    def get_users(self):
        response =  self.client.users_list()
        users = response['members']
        for user in users:
            yield user

    def delete_message(self, message_ts, channel = None):
        if channel == None:
            channel = self.MAIN_CHANNEL
        response = self.client.chat_delete(
            channel= channel,
            ts = message_ts
        )

if __name__ == "__main__":
    bot = SlackBot()
    bot.MESSAGES_PER_PAGE = 100
    messages = bot.receive_message()
    for message in messages:
        if 'bot_id' in message:
            bot.delete_message(message['ts'])
            time.sleep(random.random())

    # bot.receive_message()
    from pprint import pprint
    # for channel in bot.get_channels():
        # pprint(channel['name'])


    # pprint(bot.list_user())