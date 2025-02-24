from flask import *
import sqlite3 as sql

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

app = Flask(__name__, static_folder="static", template_folder="templates")
app.secret_key = "supersecretkey"

@app.route("/", methods=['GET', 'POST'])
def index():
    return render_template("index.html")

@app.route("/submit", methods=['GET', 'POST'])
def submit():
    username = request.form.get('username')
    password = request.form.get('password')

    session["username"] = username
    session["password"] = password

    print(session.get("username"))

    return dashboard()

@app.route("/dashboard")
def dashboard():
    username = session.get("username")
    print("here comes the sun, tururu "+ username)
    return render_template("dashboard.html", username = username)

if __name__ == "__main__":
    app.run(debug=True)


        
        
        