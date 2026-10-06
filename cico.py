from flask import Flask, request, redirect, url_for, session, render_template_string
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "cico-secret-key-2026"

# -----------------------------
# CICO DATA
# -----------------------------

users = {
    "demo": {
        "username": "demo",
        "password": generate_password_hash("1234"),
        "name": "Cico User",
        "age": "25",
        "location": "Nigeria",
        "bio": "Welcome to Cico!",
        "premium": False,
        "likes": [],
        "super_likes": [],
        "messages": []
    }
}

# Your OPay receiving account
OPAY_NUMBER = "9052206505"


# -----------------------------
# PAGE DESIGN
# -----------------------------

PAGE = """
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<title>Cico</title>

<style>

* {
    box-sizing: border-box;
}

body {
    margin: 0;
    font-family: Arial, sans-serif;
    background: #f5f5f5;
    color: #222;
}

.header {
    background: linear-gradient(135deg, #ff1744, #ff4081);
    color: white;
    padding: 18px;
    text-align: center;
}

.header h1 {
    margin: 0;
    font-size: 32px;
}

.container {
    width: 94%;
    max-width: 900px;
    margin: 20px auto;
}

.card {
    background: white;
    padding: 20px;
    border-radius: 18px;
    margin-bottom: 18px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.08);
}

input, textarea, select {
    width: 100%;
    padding: 13px;
    margin: 8px 0;
    border: 1px solid #ddd;
    border-radius: 10px;
    font-size: 16px;
}

button {
    border: none;
    padding: 12px 18px;
    border-radius: 10px;
    background: #ff1744;
    color: white;
    font-size: 15px;
    cursor: pointer;
    margin: 5px 2px;
}

button:hover {
    opacity: 0.9;
}

.secondary {
    background: #333;
}

.premium {
    background: linear-gradient(135deg, #171717, #444);
    color: white;
}

.vip {
    color: #ffd700;
    font-weight: bold;
}

.profile {
    border: 1px solid #eee;
    padding: 15px;
    border-radius: 15px;
    margin-top: 12px;
}

.nav {
    display: flex;
    flex-wrap: wrap;
    gap: 7px;
    margin-bottom: 20px;
}

.nav a {
    text-decoration: none;
    background: white;
    color: #ff1744;
    padding: 10px 13px;
    border-radius: 10px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.08);
}

.message {
    background: #f1f1f1;
    padding: 10px;
    margin: 8px 0;
    border-radius: 10px;
}

.success {
    background: #d9ffd9;
    padding: 12px;
    border-radius: 10px;
    color: #166616;
}

.error {
    background: #ffdada;
    padding: 12px;
    border-radius: 10px;
    color: #991111;
}

.big {
    font-size: 20px;
    font-weight: bold;
}

.center {
    text-align: center;
}

</style>
</head>

<body>

<div class="header">
    <h1>❤️ Cico</h1>
    <p>Meet people. Connect. Chat.</p>
</div>

<div class="container">

{% if user %}
<div class="nav">
    <a href="{{ url_for('home') }}">Home</a>
    <a href="{{ url_for('discover') }}">Discover</a>
    <a href="{{ url_for('messages') }}">Messages</a>
    <a href="{{ url_for('likes') }}">Likes</a>
    <a href="{{ url_for('premium') }}">💎 Premium</a>
    <a href="{{ url_for('profile') }}">Profile</a>
    <a href="{{ url_for('logout') }}">Logout</a>
</div>
{% endif %}

{{ content|safe }}

</div>

</body>
</html>
"""


def page(content):
    username = session.get("username")
    user = users.get(username) if username else None

    return render_template_string(
        PAGE,
        content=content,
        user=user
    )


# -----------------------------
# HOME
# -----------------------------

@app.route("/")
def home():

    if "username" not in session:

        content = """
        <div class="card center">

            <h1>Welcome to Cico ❤️</h1>

            <p>
            A new place to meet people, make connections
            and chat.
            </p>

            <a href="/register">
                <button>Create Free Account</button>
            </a>

            <a href="/login">
                <button class="secondary">Login</button>
            </a>

        </div>

        <div class="card">
            <h2>✨ Cico Features</h2>

            <p>✓ Free registration</p>
            <p>✓ Free messaging</p>
            <p>✓ Discover people</p>
            <p>✓ Likes</p>
            <p>✓ Super Likes</p>
            <p>✓ Private Chat</p>
            <p>✓ VIP membership</p>
            <p>✓ Profile boost</p>
            <p>✓ Who-liked-you</p>
            <p>✓ VIP badge</p>
        </div>
        """

        return page(content)

    username = session["username"]
    user = users[username]

    content = f"""
    <div class="card">
        <h2>Welcome, {user['name']} 👋</h2>

        <p>
        Welcome back to Cico.
        </p>

        <p>
        Find people, like profiles and start chatting.
        </p>
    </div>

    <div class="card premium">

        <h2>💎 Cico Premium</h2>

        <p>Get more features with Premium.</p>

        <p>⭐ Super Likes</p>
        <p>💬 Private Chat</p>
        <p>👀 See Who Liked You</p>
        <p>🚀 Profile Boost</p>
        <p>🏆 VIP Badge</p>

        <a href="/premium">
            <button>View Premium</button>
        </a>

    </div>
    """

    return page(content)


# -----------------------------
# REGISTER
# -----------------------------

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form.get("username", "").strip().lower()
        password = request.form.get("password", "")
        name = request.form.get("name", "").strip()
        age = request.form.get("age", "").strip()
        location = request.form.get("location", "").strip()
        bio = request.form.get("bio", "").strip()

        if not username or not password or not name:
            return page("""
            <div class="card error">
            Please fill in username, password and name.
            </div>
            """)

        if username in users:
            return page("""
            <div class="card error">
            Username already exists.
            </div>
            """)

        users[username] = {
            "username": username,
            "password": generate_password_hash(password),
            "name": name,
            "age": age,
            "location": location,
            "bio": bio,
            "premium": False,
            "likes": [],
            "super_likes": [],
            "messages": []
        }

        session["username"] = username

        return redirect(url_for("home"))

    content = """
    <div class="card">

        <h2>Create your free Cico account ❤️</h2>

        <form method="POST">

            <input
                name="name"
                placeholder="Your name"
                required
            >

            <input
                name="username"
                placeholder="Username"
                required
            >

            <input
                type="password"
                name="password"
                placeholder="Password"
                required
            >

            <input
                name="age"
                placeholder="Age"
            >

            <input
                name="location"
                placeholder="Location"
            >

            <textarea
                name="bio"
                placeholder="Tell people about yourself"
            ></textarea>

            <button type="submit">
                Register Free
            </button>

        </form>

        <p>
        Already have an account?
        <a href="/login">Login</a>
        </p>

    </div>
    """

    return page(content)


# -----------------------------
# LOGIN
# -----------------------------

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form.get("username", "").strip().lower()
        password = request.form.get("password", "")

        user = users.get(username)

        if user and check_password_hash(
            user["password"],
            password
        ):

            session["username"] = username

            return redirect(url_for("home"))

        return page("""
        <div class="card error">
        Incorrect username or password.
        </div>
        """)

    content = """
    <div class="card">

        <h2>Login to Cico</h2>

        <form method="POST">

            <input
                name="username"
                placeholder="Username"
                required
            >

            <input
                type="password"
                name="password"
                placeholder="Password"
                required
            >

            <button type="submit">
                Login
            </button>

        </form>

    </div>
    """

    return page(content)


# -----------------------------
# LOGOUT
# -----------------------------

@app.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("home"))


# -----------------------------
# DISCOVER
# -----------------------------

@app.route("/discover")
def discover():

    if "username" not in session:
        return redirect(url_for("login"))

    current = session["username"]

    html = """
    <div class="card">
        <h2>🔎 Discover People</h2>
        <p>Find people on Cico.</p>
    </div>
    """

    for username, user in users.items():

        if username == current:
            continue

        badge = ""

        if user["premium"]:
            badge = '<span class="vip">💎 VIP</span>'

        html += f"""
        <div class="card profile">

            <h2>
                {user["name"]} {badge}
            </h2>

            <p>
            Age: {user["age"]}
            </p>

            <p>
            Location: {user["location"]}
            </p>

            <p>
            {user["bio"]}
            </p>

            <a href="/like/{username}">
                <button>❤️ Like</button>
            </a>

            <a href="/super-like/{username}">
                <button>⭐ Super Like</button>
            </a>

            <a href="/chat/{username}">
                <button>💬 Chat</button>
            </a>

        </div>
        """

    return page(html)


# -----------------------------
# LIKE
# -----------------------------

@app.route("/like/<username>")
def like(username):

    if "username" not in session:
        return redirect(url_for("login"))

    current = session["username"]

    if username not in users:
        return redirect(url_for("discover"))

    if current not in users[username]["likes"]:
        users[username]["likes"].append(current)

    return redirect(url_for("discover"))


# -----------------------------
# SUPER LIKE
# -----------------------------

@app.route("/super-like/<username>")
def super_like(username):

    if "username" not in session:
        return redirect(url_for("login"))

    current = session["username"]
    user = users[current]

    if not user["premium"]:

        return page("""
        <div class="card premium">

            <h2>⭐ Super Likes are Premium</h2>

            <p>
            Upgrade to Cico Premium to use Super Likes.
            </p>

            <a href="/premium">
                <button>Upgrade Now</button>
            </a>

        </div>
        """)

    if username in users:

        if current not in users[username]["super_likes"]:
            users[username]["super_likes"].append(current)

    return page("""
    <div class="card success">
        ⭐ Super Like sent successfully!
        <br><br>
        <a href="/discover">Back to Discover</a>
    </div>
    """)


# -----------------------------
# LIKES
# -----------------------------

@app.route("/likes")
def likes():

    if "username" not in session:
        return redirect(url_for("login"))

    current = session["username"]
    user = users[current]

    if not user["premium"]:

        return page("""
        <div class="card premium">

            <h2>👀 Who Liked You</h2>

            <p>
            This is a Premium feature.
            </p>

            <a href="/premium">
                <button>Unlock Premium</button>
            </a>

        </div>
        """)

    html = """
    <div class="card">

        <h2>❤️ People Who Liked You</h2>

    """

    if not user["likes"]:
        html += "<p>No likes yet.</p>"

    for person in user["likes"]:

        person_data = users.get(person)

        if person_data:
            html += f"""
            <div class="profile">

                <h3>
                {person_data['name']}
                </h3>

                <a href="/chat/{person}">
                    <button>💬 Chat</button>
                </a>

            </div>
            """

    html += "</div>"

    return page(html)


# -----------------------------
# CHAT
# -----------------------------

@app.route("/chat/<username>", methods=["GET", "POST"])
def chat(username):

    if "username" not in session:
        return redirect(url_for("login"))

    current = session["username"]

    if username not in users:
        return redirect(url_for("discover"))

    if request.method == "POST":

        message = request.form.get("message", "").strip()

        if message:

            users[current]["messages"].append({
                "to": username,
                "from": current,
                "message": message
            })

            users[username]["messages"].append({
                "to": username,
                "from": current,
                "message": message
            })

        return redirect(url_for("chat", username=username))

    other = users[username]

    html = f"""
    <div class="card">

        <h2>💬 Chat with {other['name']}</h2>

    """

    # Show conversation
    for msg in users[current]["messages"]:

        if (
            msg["to"] == username
            or msg["from"] == username
        ):

            html += f"""
            <div class="message">
                <b>{msg['from']}:</b>
                {msg['message']}
            </div>
            """

    html += """
        <form method="POST">

            <input
                name="message"
                placeholder="Type your message..."
                required
            >

            <button type="submit">
                Send Message
            </button>

        </form>

    </div>
    """

    return page(html)


# -----------------------------
# MESSAGES
# -----------------------------

@app.route("/messages")
def messages():

    if "username" not in session:
        return redirect(url_for("login"))

    current = session["username"]
    user = users[current]

    conversations = []

    for msg in user["messages"]:

        other = msg["to"]

        if msg["from"] == current:
            other = msg["to"]

        if other != current and other not in conversations:
            conversations.append(other)

    html = """
    <div class="card">

        <h2>💬 Your Messages</h2>
    """

    if not conversations:
        html += """
        <p>You don't have any conversations yet.</p>
        """

    for person in conversations:

        if person in users:

            html += f"""
            <div class="profile">

                <h3>
                {users[person]['name']}
                </h3>

                <a href="/chat/{person}">
                    <button>Open Chat</button>
                </a>

            </div>
            """

    html += "</div>"

    return page(html)


# -----------------------------
# PREMIUM
# -----------------------------

@app.route("/premium")
def premium():

    if "username" not in session:
        return redirect(url_for("login"))

    user = users[session["username"]]

    if user["premium"]:

        return page("""
        <div class="card premium">

            <h2>💎 You are a Cico VIP</h2>

            <p>✓ Super Likes</p>
            <p>✓ Private Chat</p>
            <p>✓ See Who Liked You</p>
            <p>✓ Profile Boost</p>
            <p>✓ VIP Badge</p>

            <div class="success">
                Your Premium membership is active.
            </div>

        </div>
        """)

    content = f"""
    <div class="card premium">

        <h2>💎 Cico Premium / VIP</h2>

        <p class="big">
        Unlock the full Cico experience.
        </p>

        <p>⭐ Super Likes</p>
        <p>💬 Private Chat</p>
        <p>👀 See Who Liked You</p>
        <p>🚀 Profile Boost</p>
        <p>🏆 VIP Badge</p>
        <p>✨ Premium profile visibility</p>

    </div>

    <div class="card">

        <h2>💳 Premium Payment</h2>

        <p>
        To purchase Premium, make your payment
        through OPay.
        </p>

        <p class="big">
        OPay: {OPAY_NUMBER}
        </p>

        <p>
        After payment, keep your payment receipt
        and contact the Cico administrator to activate
        your Premium membership.
        </p>

        <div class="error">
        Important: this test version does not automatically
        verify OPay payments. Automatic payment verification
        requires a proper payment gateway/API integration.
        </div>

    </div>
    """

    return page(content)


# -----------------------------
# ADMIN PREMIUM ACTIVATION
# -----------------------------

@app.route("/activate-premium/<username>")
def activate_premium(username):

    # Simple test activation.
    # Later this should be protected with a real admin login.

    if username in users:

        users[username]["premium"] = True

        return page("""
        <div class="card success">

            <h2>💎 Premium Activated</h2>

            <p>
            The account has been upgraded to Cico Premium.
            </p>

        </div>
        """)

    return page("""
    <div class="card error">
        User not found.
    </div>
    """)


# -----------------------------
# PROFILE
# -----------------------------

@app.route("/profile", methods=["GET", "POST"])
def profile():

    if "username" not in session:
        return redirect(url_for("login"))

    username = session["username"]
    user = users[username]

    if request.method == "POST":

        user["name"] = request.form.get("name", user["name"])
        user["age"] = request.form.get("age", user["age"])
        user["location"] = request.form.get(
            "location",
            user["location"]
        )
        user["bio"] = request.form.get(
            "bio",
            user["bio"]
        )

        return page("""
        <div class="card success">
            Profile updated successfully.
        </div>
        """)

    badge = ""

    if user["premium"]:
        badge = '<span class="vip">💎 VIP</span>'

    content = f"""
    <div class="card">

        <h2>My Profile {badge}</h2>

        <form method="POST">

            <input
                name="name"
                value="{user['name']}"
                placeholder="Name"
            >

            <input
                name="age"
                value="{user['age']}"
                placeholder="Age"
            >

            <input
                name="location"
                value="{user['location']}"
                placeholder="Location"
            >

            <textarea
                name="bio"
                placeholder="Bio"
            >{user['bio']}</textarea>

            <button type="submit">
                Save Profile
            </button>

        </form>

    </div>
    """

    return page(content)


# -----------------------------
# START CICO
# -----------------------------

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )