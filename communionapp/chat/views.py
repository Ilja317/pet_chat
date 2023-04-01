from django.shortcuts import render

from polsovatel.models import ChatRoomName
from .models import MesseageModels, Chats
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response




# Create your views here.
def chat(request, pk):
    chat = Chats.objects.get(id=pk)
    if not chat.lastSender == request.user:
        print(chat.lastSender.username)
        Chats.objects.filter(id=pk).update(read=False)
    messeagesour = MesseageModels.objects.filter(owner=chat.ownerone,sender=chat.ownertwo).order_by("data")
    messeagesend = MesseageModels.objects.filter(sender=chat.ownerone,owner=chat.ownertwo).order_by("data")
    print([*messeagesour])
    print([*messeagesend])
    messeages = {*messeagesour,*messeagesend}

    container = {
        "messeages": sorted(messeages,key=lambda x: x.data),
        "room": "chat_%s" % ChatRoomName.objects.get(owner=request.user).room,
        "id": chat.id,
        "owner":  "we" if chat.lastSender == request.user else "not we",
        "sender": chat.ownerone.id if not chat.ownerone == request.user else chat.ownertwo.id
    }
    print(container["sender"])
    print("да")
    return render(request,"chat/chat.html",container)

def chats(request):
    chatowner = Chats.objects.filter(ownerone=request.user)
    chatsender = Chats.objects.filter(ownertwo=request.user)
    chat = sorted([*chatowner, *chatsender], key=lambda x: x.data, reverse=True)
    container = {
        "chats": chat,
        "room": "chat_%s" % ChatRoomName.objects.get(owner=request.user).room,
    }
    return render(request, "chat/chats.html", container)


def sendMesseage(request,pk):
    if request.method == "POST":
        text = request.POST["text"]
        owner = User.objects.get(id=pk)
        MesseageModels.objects.create(owner=owner,sender=request.user,text=text)
    container = {
        "room": "chat_%s" % ChatRoomName.objects.get(owner=request.user).room
    }
    return render(request, "chat/sendmesseage.html", container)


class SendMessege(APIView):
    def post (self, request, id):
        print("sendMesseage")
        print(request.data["text"])
        user = User.objects.get(id=id)
        text = request.data["text"]
        MesseageModels.objects.create(owner=user, sender=request.user, text=text)
        return Response({
            "text": "Отправлено"
        })
