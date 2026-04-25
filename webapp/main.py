from flask import Flask, render_template, request, session, redirect, abort
from database import Database

app = Flask(__name__)
app.secret_key = "MY_SUPER_SECRET_KEY"
app.config['SESSION_COOKIE_HTTPONLY'] = False

db = Database("mysql",
              "webmaster",
              "securep",
              "xss")

def logged_in():
    token = session.get("token")
    user = db.get_user_by_token(token)
    if not user:
        session["token"] = None
    return user

def nuke_token(token):
    session.clear()
    db.delete_token(token)

def generate_messages_template():
    result = """"""
    messages = db.get_messages()
    for entry in messages:
        username = entry[2]
        content = entry[3]
        date = entry[4]
        msg_class = "message-mine" if session.get("username") == username else "message-yours"
        template = f"""<div class="message-wrapper {msg_class}">
                            <div class="message">
                                <div class="message-header">
                                    <p class="atom">{username}</p>
                                    <p class="atom">{date}</p>
                                </div>
                                <p class="atom">{content}</p>
                            </div>
                        </div>"""
        result += template
    
    return result

# LOGIN/LOGOUT ------------------------------------------

@app.route("/", methods=["GET"])
def root():
    if logged_in():
        return redirect("/chat")
    return render_template("index.html")

@app.route("/register", methods=["GET"])
def register():
    return render_template("register.html")

@app.route("/logout", methods=["GET"])
def logout():
    token = session.get("token")
    if token:
        nuke_token(token)
    return redirect("/")

# FORMS ------------------------------------------

@app.route("/loginForm", methods=["POST"])
def login_form():
    username = request.form["username"]
    password = request.form["password"]
    user = db.get_user(username, password)
    if user:
        token = db.set_token(username, password)
        session["token"] = token
        session["username"] = username
        return redirect("/chat")
    return abort(401)    

@app.route("/registerForm", methods=["POST"])
def register_form():
    email    = request.form["email"]
    username = request.form["username"]
    password = request.form["password"]
    user_u = db.get_user_by_name(username)
    user_e = db.get_user_by_email(email)
    if not user_u and not user_e:
        db.register(email, username, password)
        return redirect("/?chngd=2")
    elif not user_u and user_e:
        err = "err=2"
    elif user_u and not user_e:
        err = "err=1"
    else:
        err = "err=3"
    return redirect(f"/register?{err}")

# CHAT ------------------------------------------

@app.route("/chat", methods=["GET"])
def chat():
    token = session.get("token")
    user = db.get_user_by_token(token)
    if user:
        return render_template("chat.html", username=user[0][1], messages=generate_messages_template())
    else:
        session["token"] = None
        return redirect("/")

# PROFILE ------------------------------------------

@app.route("/profile", methods=["GET"])
def profile():
    user = logged_in()
    user = user[0] if user else user
    if user:
        return render_template("profile.html", email=user[2], username=user[1], password=user[3])
    else:
        return redirect("/")
    
@app.route("/changePassword", methods=["POST"])
def change_password():
    user = logged_in()
    user = user[0] if user else user
    if user:
        password = request.form.get("password")
        if password:
            db.change_password(user[1], password)
        nuke_token(user[4])
    return redirect("/?chngd=1")
    
# MESSAGES ------------------------------------------

@app.route("/sendMessage", methods=["POST"])
def send_message():
    jsn = request.json
    try:
        token = session.get("token")
        content = jsn["content"]
        user = db.get_user_by_token(token)
        if user:
            if content:
                db.insert_message(token, content)
        else:
            return "error"
    except:
        return "error"
    return "ok"

@app.route("/getMessages", methods=["GET"])
def gm():
    return db.get_messages()


app.run(host="0.0.0.0", port=80)