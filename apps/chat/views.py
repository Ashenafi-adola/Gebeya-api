from django.shortcuts import render
from . models import Message
from . serializers import MessageSerializer
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from apps.accounts.models import User


class MessageListAPIView(generics.ListCreateAPIView):
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
        return User.objects.get(id=self.kwargs['pk'])

    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save(sender=self.request.user, reciever=self.get_reciever())