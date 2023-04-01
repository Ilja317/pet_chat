from django.urls import path,include
from .views import chat,chats,sendMesseage,SendMessege
urls = [
    path("chat/<int:pk>", chat, name="chat"),
    path("", chats, name="chats"),
    path("send/<int:pk>", sendMesseage,name="send"),
    path("api/send/<int:id>", SendMessege.as_view())
]