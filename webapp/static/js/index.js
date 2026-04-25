let messages = undefined;
window.onload = () => {
    document.getElementById("message").addEventListener("keypress", (event) => {
        if (event.key === "Enter") {
            SendMessage();
        }
    });
}

function SendMessage() {
    fetch("http://" + window.location.hostname + "/sendMessage", 
        {
            "method": "POST",
            headers: {
                "Content-Type": "application/json"
            },
            "body": JSON.stringify({
                content: document.getElementById('message').value
            })
        }
    ).then(response => {
        document.getElementById("message").value = "";
        response.text().then(text => {
            if (text == "error") {
                window.location.href = "/";
            }
        });
    });
}

function createMessage(userName, date, content) {
    let msgdiv = document.createElement("div");
    let un = document.createElement("p");
    let dt = document.createElement("p");
    let cn = document.createElement("p");


    un.innerHTML = userName;
    dt.innerHTML = date;
    cn.innerHTML = content;

    msgdiv.className = "message";

    
    un.className = "atom";
    dt.className = "atom";
    cn.className = "atom";

    msgdiv.appendChild(un);
    msgdiv.appendChild(dt);
    msgdiv.appendChild(cn);
    return msgdiv;
}

function getMessages() {
    fetch("http://localhost/getMessages").then(data => {
        data.json().then(json => {
            if (messages ==  undefined || messages != json) {
                messages = json;
                const container = document.getElementById("messages-container");
                container.replaceChildren();
                json.forEach(entry => {
                    let un = entry[2];
                    let cn = entry[3];
                    let dt = entry[4];
                    let msg = createMessage(un, dt, cn);
                    container.appendChild(msg);
                });
            }
        })
    })
}

setInterval(() => {getMessages()}, 500);