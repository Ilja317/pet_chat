document.addEventListener("DOMContentLoaded",()=>{
    const room = JSON.parse(document.getElementById('room-name').textContent);

    const chatSocket = new WebSocket(
        'ws://'
        + window.location.host
        + '/ws/chat/'
        + room
        + '/'
    );

    chatSocket.onmessage = function(e) {
        const data = JSON.parse(e.data);
            const list = document.querySelector(".chatlist")
            try {
                const li = document.querySelector(`li[data-sender='${data["sender"]}']`)
                const a = document.createElement("a")
                a.style.color = "blue"
                a.setAttribute("href","/chat/chat/" + data["id"])
                a.textContent = data["sender"]
                const div = document.createElement("div")
                div.textContent = data["text"]
                li.remove()
                const newli = document.createElement("li")
                newli.append(a)
                newli.append(div)
                newli.style.cssText = "border:solid 2px red"
                newli.setAttribute("data-sender",data["sender"])
                list.prepend(newli)
            }catch{
                const a = document.createElement("a")
                a.style.color = "blue"
                a.setAttribute("href","/chat/chat/" + data["id"])
                a.textContent = data["sender"]
                const div = document.createElement("div")
                div.textContent = data["text"]
                const newli = document.createElement("li")
                newli.append(a)
                newli.append(div)
                newli.style.cssText = "border:solid 2px red"
                newli.setAttribute("data-sender",data["sender"])
                list.prepend(newli)
            }
        }
    ;
})