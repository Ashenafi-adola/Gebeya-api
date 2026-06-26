from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from . models import Message
from apps.accounts.models import User, Contact
import json
from django.utils import timezone


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        user = self.scope['user']
        peer_id = int(self.scope['url_route']['kwargs']['id'])

        ur_ids = [user.id, peer_id]
        ur_ids.sort()
        self.room_group_name = f'chat_{ur_ids[0]}_{ur_ids[1]}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, code):
        pass
    
    async def receive(self, text_data = None, bytes_data = None):
        text_data_json = json.loads(text_data)

        message = text_data_json['message']
        sender = text_data_json['sender']
        reciever = text_data_json['reciever']
        id = await self.save_message(message)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type':'chat_message',
                'message': message,
                'sender': sender,
                'reciever': reciever,
                'id':id
            }
        )


    async def chat_message(self, event):
        message = event['message']
        sender = event['sender']
        reciever = event['reciever']
        id = event['id']
        await self.send(text_data=json.dumps({
            'type': 'chat',
            'message': message,
            'sender': sender,
            'reciever': reciever,
            'id': id
        }))

    @database_sync_to_async
    def save_message(self, message):
        sen = User.objects.get(id=self.scope['user'].id)
        rec = User.objects.get(id=int(self.scope['url_route']['kwargs']['id']))
        mes = Message.objects.create(sender=sen, reciever=rec, message=message)
        try:
            con = Contact.objects.create(user=sen)
            cons = con.contacts
            cons.add(rec)
        except Exception:
            con = Contact.objects.get(user=sen)
            a = con.contacts
            cons = con.contacts.all()
            if rec not in cons:
                a.add(rec)
        
        return mes.id