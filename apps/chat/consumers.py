from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from . models import Message
from apps.accounts.models import User
import json
from django.utils import timezone


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        user = self.scope['user']
        print(self.scope)
        await self.accept()

    async def disconnect(self, code):
        pass
    
    async def receive(self, text_data = None, bytes_data = None):
        text_data_json = json.loads(text_data)
        print(text_data_json)
        await self.send(text_data=json.dumps(text_data_json))