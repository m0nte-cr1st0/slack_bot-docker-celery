from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .tasks import parse_message


class Events(APIView):
    def post(self, request, *args, **kwargs):
        slack_message = request.data
        if slack_message.get('type') == 'url_verification':
            return Response(data=slack_message,
                            status=status.HTTP_200_OK)
        if slack_message.get('event') and not 'bot_id' in slack_message.get('event'):
            parse_message.delay(slack_message)
        return Response(status=status.HTTP_200_OK)
