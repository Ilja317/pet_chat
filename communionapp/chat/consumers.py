# chat/consumers.py
import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from polsovatel.models import ChatRoomName


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.user = self.scope["user"]
        print(self.user)
        print("комната")
        self.room_name = ChatRoomName.objects.get(owner=self.user).room
        self.room_group_name = "chat_%s" % self.room_name
        print("комната")
        print(self.room_group_name)
        print(self.channel_name)

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        print("закрыли")
        print(close_code)
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {"type": "chat_message", "message": message}
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event["message"]
        id = event["id"]
        sender = event["sender"]
        print("Отправляем")
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            "text": message,
            "id":id,
            "sender":sender
        }))