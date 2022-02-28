import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from my_chat.models import City
from my_chat.serializer import CitySerializer, MessageSerializer


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        city_serializer = CitySerializer(data={'name': self.room_name})
        print(city_serializer)
        if city_serializer.is_valid():
            city_serializer.save()
        print(city_serializer)
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data, **kwargs):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        city_pk = text_data_json['pk']
        print(city_pk)

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'pk': city_pk
            }
        )

    # Receive message from room group
    def chat_message(self, event):
        print(event)
        print(self.room_name)
        message = event['message']
        city_id = event['pk']
        print(city_id)
        message_serializer = MessageSerializer(data={'content': message, 'city_id': city_id})
        if message_serializer.is_valid():
            message_serializer.save()
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message
        }))  # Receive message from room group
