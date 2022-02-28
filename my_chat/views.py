from django.shortcuts import render
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination

from my_chat.models import Message
from my_chat.serializer import MessageSerializer


def index(request):
    return render(request, 'index.html')


def room(request, room_name):
    return render(request, 'room.html', {
        'room_name': room_name
    })


class MessageApiListPagination(PageNumberPagination):
    page_size = 10


class MessageApiList(ListAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    pagination_class = MessageApiListPagination

