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

function createMessage(userName, date, content, msgClass) {
    let msgwrapper = document.createElement("div");
    let msgdiv     = document.createElement("div");
    let header     = document.createElement("div");
    let un         = document.createElement("p");
    let dt         = document.createElement("p");
    let cn         = document.createElement("p");

    date = new Date(date);
    const pad = (n) => String(n).padStart(2, '0');
    date = `${date.getFullYear()}-${pad(date.getMonth() + 1)}-${pad(date.getDate())} `
  + `${pad(date.getUTCHours())}:${pad(date.getUTCMinutes())}:${pad(date.getSeconds())}`;

    un.innerHTML = userName;
    dt.innerHTML = date;
    cn.innerHTML = content;

    header.className = "message-header";
    msgdiv.className = "message";
    msgwrapper.className = "message-wrapper "
    msgwrapper.className += msgClass

    un.className = "atom";
    dt.className = "atom";
    cn.className = "atom";

    header.appendChild(un);
    header.appendChild(dt);
    msgdiv.appendChild(header);
    msgdiv.appendChild(cn);
    msgwrapper.appendChild(msgdiv);
    return msgwrapper;
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
                    let msgClass = userName == un ? "message-mine" : "message-yours";
                    let msg = createMessage(un, dt, cn, msgClass);
                    container.appendChild(msg);
                });
            }
        })
    })
}

setInterval(() => {getMessages()}, 500);