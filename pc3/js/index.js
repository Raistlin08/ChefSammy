const llm = "http://localhost:8080/chat"

async function send(){
    let chatdiv = document.getElementById("chatdiv");
    let textfield = document.getElementById("textfield");
    let message = textfield.value.trim();
    if (message === "") return;

    textfield.value = "";
    chatdiv.innerHTML += '<p class="user-message">' + message + '</p>'
    chatdiv.scrollTop = chatdiv.scrollHeight;

    try {
        let answer = await fetch(llm, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({"user": message})
        });

        if (!answer.ok) {
            throw new Error(`server error: ${answer.status}`);
        }
        let data = await answer.json()
        let llm_message = data["ai"]
        chatdiv.innerHTML += '<p class="ai-message">' + llm_message + '</p>'
        chatdiv.scrollTop = chatdiv.scrollHeight;

    } catch (error) {
        console.error("Problem with fetch:", error);
        chatdiv.innerHTML += `<p class="ai-message" style="color: red;">Errore di connessione.</p>`;
    }

}