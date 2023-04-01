from django.db import models
from django.contrib.auth.models import User
import uuid

from django.db.models.signals import post_save


# Create your models here.
class ChatRoomName(models.Model):
    owner = models.ForeignKey(User,on_delete=models.CASCADE,verbose_name="Владелец")
    room = models.CharField(max_length=255,verbose_name="Название комнаты")
    def __str__(self):
        return self.owner.username

    class Meta :
        verbose_name = "Комната"
        verbose_name_plural = "Комната"

def recieveMesseage(sender, instance, created, **kwargs):
    if created :
        id = str(uuid.uuid4())
        ChatRoomName.objects.create(owner=instance,room=id.replace("-",''))

post_save.connect(recieveMesseage, sender=User)