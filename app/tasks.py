import re, requests

from slack_bot.celery import app
# import slack
from slack import WebClient

from django.conf import settings
from .models import Message, RegExp


@app.task
def parse_message(slack_message):
    try:
        if slack_message.get('event').get('type') == 'message':
            if 'files' in slack_message['event']:
                for ind, item in enumerate(slack_message['event']['files']):
                    message = Message.objects.create(
                        text=slack_message['event']['text']
                    )
                    message.filetype = slack_message['event']['files'][ind]['filetype']
                    message.file_name = slack_message['event']['files'][ind]['title']
                    message.file_link = slack_message['event']['files'][ind]['url_private']
                    message.with_file = True
                    message.save()
                    r = requests.get(slack_message['event']['files'][ind]['url_private'], headers={
                        'Authorization': 'Bearer %s' % settings.SLACK_API_TOKEN})
                    for pattern in RegExp.objects.values_list('pattern', flat=True):
                        if re.search(pattern, r.text):
                            message.pattern_found = True
                            message.pattern = pattern
                            message.save()
                            break
            else:
                Message.objects.create(
                    text=slack_message['event']['text']
                )
    except:
        client = WebClient(token=settings.SLACK_API_TOKEN)
        event_message = slack_message.get('event')
        user = event_message.get('user')
        channel = event_message.get('channel')
        bot_text = 'Hi <@{}> :wave: . Your message was blocked.'.format(user)
        client.chat_postMessage(
                        channel=channel,
                        text=bot_text,
        )
