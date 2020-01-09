import unittest
import os, re, requests

from django.conf import settings
from app.models import *


class TestBasic(unittest.TestCase):

    def test_without_file(self):
        self.slack_message = {'token': '***', 'team_id': '***', 'api_app_id': '***',
                               'event': {'client_msg_id': '***', 'type': 'message',
                                         'text': 'test',
                                         'user': '***', 'ts': '***', 'team': '***',
                                         'channel': '***',
                                         'event_ts': '***', 'channel_type': 'channel'},
                               'type': 'event_callback',
                               'event_id': '***', 'event_time': '****', 'authed_users': ['***']}
        self.assertTrue(self.slack_message.get('event').get('type') != 'message' or 'files' not in self.slack_message['event'])
        message = Message.objects.create(
            text=self.slack_message['event']['text']
        )
        self.assertTrue(message.text == 'test')
        self.assertTrue(message.filetype == '')

    def test_regexp_found(self):
        self.slack_message = {
            'token': '***', 'team_id': '***', 'api_app_id': '***', 'event': {
                'type': 'message', 'text': '', 'files': [{
                    'id': 'FNL1KFPE3', 'created': 1568903795, 'timestamp': 1568903795, 'name': 'file1.txt', 'title': 'file1.txt', 'mimetype': 'text/plain',
                    'filetype': 'text', 'pretty_type': 'Plain Text', 'user': 'UNJHDBB8W', 'editable': True, 'size': 4253, 'mode': 'snippet', 'is_external': False,
                    'external_type': '', 'is_public': True, 'public_url_shared': False, 'display_as_bot': False, 'username': '',
                    'url_private': 'https://files.slack.com/files-pri/TNJHDBAGN-FN5CVKMFC/file1.txt', 'other': 'other',
                }],
                'upload': True, 'user': '***', 'other': 'other'
            },
            'type': 'event_callback', 'other': 'other'
        }
        self.assertTrue(self.slack_message.get('event').get('type') == 'message' and 'files' in self.slack_message['event'])
        r = requests.get(self.slack_message['event']['files'][0]['url_private'], headers={
            'Authorization': 'Bearer %s' % settings.SLACK_API_TOKEN})
        message = Message.objects.create(
            text=self.slack_message['event']['text']
        )

        reg = '\w+\.'
        if re.search(reg, r.text):
            message.pattern_found = True
            message.save()
        self.assertTrue(message.pattern_found)

    def test_regexp_not_found(self):
        r = requests.get('https://files.slack.com/files-pri/TNJHDBAGN-FNLCUKPD4/file2.json', headers={
            'Authorization': 'Bearer %s' % settings.SLACK_API_TOKEN})
        message = Message.objects.create(
            text='test'
        )

        reg = '\w+\.'
        if re.search(reg, r.text):
            message.pattern_found = True
            message.save()

        self.assertFalse(message.pattern_found)

    def test_multi_files_with_regexp(self):
        self.slack_message = {'event': {'files': [
             {'url_private': 'https://files.slack.com/files-pri/TNJHDBAGN-FNHNXKXB6/file1.txt',
              },
             {'url_private': 'https://files.slack.com/files-pri/TNJHDBAGN-FNJ78HPAL/file3.svg',
              }
        ]}}


        message1 = Message.objects.create(
            text='test1'
        )
        message2 = Message.objects.create(
            text='test2'
        )

        for ind, item in enumerate(self.slack_message['event']['files']):
            r = requests.get(self.slack_message['event']['files'][ind]['url_private'], headers={
                'Authorization': 'Bearer %s' % settings.SLACK_API_TOKEN})
            reg = '\w+\. '
            if re.search(reg, r.text):
                print(re.search(reg, r.text))
                if ind == 0:
                    message1.pattern_found = True
                    message1.save()
                    self.assertTrue(message1.pattern_found)
                else:
                    message2.pattern_found = True
                    message2.save()
                    self.assertTrue(message2.pattern_found)
            else:
                if ind == 0:
                    message1.pattern_found = True
                    message1.save()
                    self.assertFalse(message1.pattern_found)
                else:
                    self.assertFalse(message2.pattern_found)