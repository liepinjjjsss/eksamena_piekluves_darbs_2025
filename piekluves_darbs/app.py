from flask import *
import sqlite3 as sql
import hashlib

class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password

class BusinessType:
    def __init__(self, id, business_type, tax):
        self.id = id
        self.business_type = business_type
        self.tax = tax

class Business(BusinessType):
    def __init__(self, business_name, net_worth):
        self.business_type = BusinessType.business_type
        self.business_name = business_name
        self.net_worth = net_worth

class Transaction(Business):
    def __init__(self, amount):
        self.business_name = Business.business_name
        self.amount = amount

# def hash_password(password):
#     return hashlib.sha256(password.encode('utf-8')).hexdigest()  # Fixed hexdigest()

# app = Flask(__name__, static_folder="static", template_folder="templates")
# app.secret_key = "supersecretkey"

# @app.route("/", methods=['GET', 'POST'])
# def index():
#     return render_template("index.html")

# @app.route("/signup", methods=['GET', 'POST'])
# def signup():
#     if request.method == "POST":
#         name = request.form.get('name')
#         username = request.form.get('username')
#         password = request.form.get('password')

#         hashed_pw = hash_password(password)

#         conn = sql.connect("expensify.db")
#         cursor = conn.cursor()
#         cursor.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)", 
#                        (name, username, hashed_pw))
#         conn.commit()
#         conn.close()

#         return redirect(url_for("index"))

#     return render_template("signup.html")

# @app.route("/submit", methods=['GET', 'POST'])
# def submit():
#     username = request.form.get('username')
#     password = request.form.get('password')

#     print(username)
#     print(password)
#     print(hash_password(password))

#     session["username"] = username  # Only store the username

#     return redirect(url_for("dashboard"))

# @app.route("/dashboard")
# def dashboard():
#     if "username" not in session:
#         return redirect(url_for("index"))

#     username = session.get("username")

#     return render_template("dashboard.html", username=username)

# if __name__ == "__main__":
#     app.run(debug=True)

def hash_password(password):
    return hashlib.sha256(password.encode('utf-8')).hexdigest()


app = Flask(__name__, static_folder="static", template_folder="templates")
app.secret_key = "supersecretkey"

@app.route("/", methods=['GET', 'POST'])
def index():
    print("AAAAAAAAAA")
    return render_template("index.html")

@app.route("/signup", methods=['GET', 'POST'])
def signup():
    name = request.form.get('name')
    username = request.form.get('username')
    password = request.form.get('password')



@app.route("/submit", methods=['GET', 'POST'])
def submit():
    print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
    username = request.form.get('username')
    password = request.form.get('password')

    session["username"] = username
    session["password"] = password

    print(username)
    print(password)
    print(hash_password(password))

    return redirect(url_for("dashboard"))

@app.route("/dashboard")
def dashboard():
    print("SSSSAAAAAAAAA")
    conn = sql.connect("expensify.db")
    cursor = conn.cursor()

    username = session.get("username")
    password = session.get("password")

    cursor.execute("""INSERT INTO users (name, email, password) VALUES (?,?,?)""", (username, username, password))

    conn.commit()
    conn.close()

    return render_template("dashboard.html", username = username)

if __name__ == "__main__":
    app.run(debug=True)


        
        
        