from django.shortcuts import render
from . models import Message
from . serializers import MessageSerializer
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from apps.accounts.models import User


class MessageListAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MessageSerializer
    
    def get_queryset(self):
        return Message.objects.filter(
            (
                Q(sender=self.request.user) & Q(reciever=self.get_reciever())
            ) | 
            (
                Q(reciever=self.request.user) & Q(sender=self.get_reciever())
            )
        )
    
    def get_reciever(self):
        User.objects.get(id=self.kwargs['pk'])