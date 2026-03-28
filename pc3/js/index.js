function send(){
    let chatdiv = document.getElementById("chatdiv");
    let textfield = document.getElementById("textfield");
    let message = textfield.value.trim();
    if (message === "") return;

    textfield.value = "";
    chatdiv.innerHTML += '<p class="user-message">' + message + '</p>'
    chatdiv.scrollTop = chatdiv.scrollHeight;
}