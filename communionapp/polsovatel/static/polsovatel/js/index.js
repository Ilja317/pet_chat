document.addEventListener("DOMContentLoaded",()=>{
    const room = JSON.parse(document.getElementById('room-name').textContent);
    console.log(room)
    const chatSocket = new WebSocket(
        'ws://'
        + window.location.host
        + '/ws/chat/'
        + room
        + '/'
    );
    console.log(chatSocket)
    chatSocket.onmessage = function(e) {
        const data = JSON.parse(e.data);
        const listMesseges = document.querySelector(".new-messeages-block")
        const itemMesseges = document.createElement("li")
        itemMesseges.classList.add("new-messeage-block")
        listMesseges.prepend(itemMesseges)
        const span = document.createElement("span")
        span.textContent = "Новое сообщение"
        itemMesseges.append(span)
        span.style.display = "block"
        const strong = document.createElement("strong")
        strong.textContent = data["sender"]
        console.log(data)
        itemMesseges.append(strong)
        const p = document.createElement("p")
        itemMesseges.append(p)
        const a = document.createElement("a")
        a.textContent = data["text"]
        a.setAttribute("href","/chat/chat/" + data["id"])
        p.append(a)
        const delli = setTimeout(()=>{
            itemMesseges.remove()
            clearTimeout(delli)
        },15000)
        
    };

    chatSocket.onclose = function(e) {
        console.error('Chat socket closed unexpectedly');
    };



    // document.querySelector('#chat-message-submit').onclick = function(e) {
    //     const messageInputDom = document.querySelector('#chat-message-input');
    //     const message = messageInputDom.value;
    //     chatSocket.send(JSON.stringify({
    //         'message': message
    //     }));
    //     messageInputDom.value = '';
    // };
})