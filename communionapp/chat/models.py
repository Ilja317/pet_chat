from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from polsovatel.models import ChatRoomName


# Create your models here.
class MesseageModels(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Получатель", related_name="owner")
    sender = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Отправитель", related_name="sender")
    data = models.DateTimeField(auto_now_add=True, verbose_name="Дата отправки")
    text = models.TextField(verbose_name="Сообщения")

    def __str__(self):
        return self.owner.username


    class Meta :
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"


class Chats(models.Model):
    ownerone = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Получатель", related_name="owner_chat")
    ownertwo = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Отправитель", related_name="sender_chat")
    data = models.DateTimeField(auto_now=True, verbose_name="Дата отправки")
    text = models.TextField(verbose_name="Сообщения")
    lastSender = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Последний отправитель", related_name="last_sender")
    read = models.BooleanField(default=True)
    def __str__(self):
        return self.ownerone.username + " и " + self.ownertwo.username


    class Meta :
        verbose_name = "Чат"
        verbose_name_plural = "Чаты"


def recieveMesseage(sender, instance, created, **kwargs):
    channel_layer = get_channel_layer()
    if Chats.objects.filter(ownerone=instance.owner, ownertwo=instance.sender).exists() or Chats.objects.filter(ownerone=instance.sender, ownertwo=instance.owner).exists():
        chat = Chats.objects.get(ownerone=instance.owner, ownertwo=instance.sender) if Chats.objects.filter(ownerone=instance.owner, ownertwo=instance.sender).exists() else Chats.objects.get(ownerone=instance.sender, ownertwo=instance.owner)
        chat.text = instance.text
        chat.lastSender = instance.sender
        chat.read = True
        chat.save()
        room = ChatRoomName.objects.get(owner=instance.owner).room
        print(room)
        print("room")
        async_to_sync(channel_layer.group_send)("chat_%s" % room, {
            "type": "chat_message",
            "id": chat.id,
            "sender": instance.sender.username,
            "message": instance.text,
        })

    else:
        Chats.objects.create(ownerone=instance.owner, ownertwo=instance.sender, text=instance.text, lastSender=instance.sender)
        chat = Chats.objects.get(ownerone=instance.owner, ownertwo=instance.sender) if Chats.objects.filter(ownerone=instance.owner, ownertwo=instance.sender).exists() else Chats.objects.get(ownerone=instance.sender, ownertwo=instance.owner)
        room = ChatRoomName.objects.get(owner=instance.owner).room
        print(room)
        print("room")
        async_to_sync(channel_layer.group_send)(
            "chat_%s" % room, {"type": "chat_message",
                   "id": chat.id,
                   "sender": instance.sender.username,
                   "message": instance.text,
                   }
        )

post_save.connect(recieveMesseage, sender=MesseageModels)