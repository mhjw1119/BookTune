import json
from channels.generic.websocket import AsyncWebsocketConsumer

class SongNotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add(
            "song_notifications",
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            "song_notifications",
            self.channel_name
        )

    async def receive(self, text_data):
        pass

    async def song_notification(self, event):
        # 클라이언트에게 메시지 전송
        await self.send(text_data=json.dumps({
            'type': 'song_notification',
            'message': event['message']
        })) 