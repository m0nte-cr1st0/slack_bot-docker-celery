# from app.models import Team
# from slackclient import SlackClient
# from django.core.management.base import BaseCommand
# import time
#
#
#
# class Command(BaseCommand):
#     help = 'Starts the bot for the first'
#
#
# def start_listening(self):
#     team = Team.objects.first()
#     client = SlackClient(team.bot_access_token)
#     if client.rtm_connect():
#         while True:
#             events = client.rtm_read()
#             for event in events:
#                 if event['type']=='message' and event['text']=='hi':
#                     client.rtm_send_message(
#                         event['channel'],
#                         "Hello World!"
#                     )
#             time.sleep(1)


import os
import slack

@slack.RTMClient.run_on(event='message')
def say_hello(**payload):
    data = payload['data']
    web_client = payload['web_client']
    rtm_client = payload['rtm_client']
    print(7)
    if 'Hello' in data['text']:
        print(7)
        channel_id = data['channel']
        thread_ts = data['ts']
        user = data['user']

        web_client.chat_postMessage(
            channel=channel_id,
            text=f"Hi <@{user}>!",
            thread_ts=thread_ts
        )

slack_token = "xoxb-766591384566-766339821815-466Ma86fn4qJeW3Nm9xJ4MfX"
rtm_client = slack.RTMClient(token=slack_token)
print(rtm_client.token, rtm_client.base_url)
print(dir(rtm_client))
rtm_client.start()