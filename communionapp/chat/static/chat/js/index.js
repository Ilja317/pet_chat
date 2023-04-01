document.addEventListener("DOMContentLoaded",()=>{
       window.onload = function(){
    document.querySelectorAll('li')[document.querySelectorAll('li').length - 1].scrollIntoView(true);};   const id = JSON.parse(document.getElementById('id').textContent);
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
        if(id == data["id"]) {
            const list = document.querySelector(".chatlist")
            if (data["owner"] == "we") {
                const li = document.createElement("li")
                li.classList.add("our-messeage")
                li.textContent = data["text"]
                list.append(li)
            }else {
                const li = document.createElement("li")
                li.classList.add("not-our-messeage")
                li.textContent = data["text"]
                list.append(li)
            }
            document.querySelectorAll('li')[document.querySelectorAll('li').length - 1].scrollIntoView(true);
        }
    };

    chatSocket.onclose = function(e) {
        console.error('Chat socket closed unexpectedly');
    };



    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    
    chatSocket.onclose = function(e) {
        console.error('Chat socket closed unexpectedly');
    };

    const textinput = document.querySelector(".text-input")
    const btn = document.querySelector(".btn")
    const sendMesseage = async (text)=>{ 
        const csrftoken = getCookie('csrftoken');
        console.log(csrftoken)
        const sender = JSON.parse(document.getElementById('sender').textContent);
        console.log("/chat/api/send/" + sender)
        const request = await fetch("/chat/api/send/" + sender,{
            method: "POST",
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify({
                "text":text
            })
        })
        request.json().then(item=>{
            console.log(item["text"])
        })
    }
    btn.addEventListener("click",(event)=>{
        event.preventDefault();
        if (textinput.value.length > 0) {
            const list = document.querySelector(".chatlist")
            const li = document.createElement("li")
            li.classList.add("our-messeage")
            li.textContent = textinput.value
            list.append(li)
            sendMesseage(textinput.value)
            textinput.value = ''
        }
    })
})