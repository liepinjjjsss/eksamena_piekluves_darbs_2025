from flask import *
import sqlite3 as sql
import hashlib

class User:
    def __init__(self, name, email, password):
        self.name = name
        self.email = email
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


def hash_password(password):
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def get_all_users():
    conn = sql.connect("expensify.db")
    curr = conn.cursor()

    curr.execute(""" SELECT * FROM users """)
    data = curr.fetchall()

    conn.close()

    return data


app = Flask(__name__, static_folder="static", template_folder="templates")
app.secret_key = "supersecretkey"

@app.route("/", methods=['GET', 'POST'])
def index():
    return render_template("index.html")

@app.route("/signup", methods=['GET', 'POST'])
def signup():
    return render_template("signup.html")
    

@app.route("/create_account", methods=['GET', 'POST'])
def create_account():
    is_registered = False
    
    name = request.form.get('name')
    username = request.form.get('username')
    password = hash_password(request.form.get('password'))

    users = get_all_users()
    for user in users:
        if user[2] == username:
            is_registered = True


    if not is_registered:
        conn = sql.connect("expensify.db")
        cursor = conn.cursor()

        cursor.execute("""INSERT INTO users (name, email, password) VALUES (?,?,?)""", (name, username, password))

        conn.commit()
        conn.close()
    else:
        print("user already registered")
        return render_template("signup.html", error="An account with this email already exists!")

    return redirect(url_for("index"))
    



@app.route("/submit", methods=['GET', 'POST'])
def submit():
    login = False
    username = request.form.get('username')
    password = hash_password(request.form.get('password'))

    users = get_all_users()
    for user in users:
        if user[2] == username and user[3] == password:
            login = True
            conn = sql.connect("expensify.db")
            curr = conn.cursor()

            curr.execute("""SELECT name FROM users WHERE email = ? AND password = ?""", (username, password))
            name  = curr.fetchone()

            curr.execute("""SELECT id FROM users WHERE email = ? AND password = ?""", (username, password))
            id = curr.fetchone()


            print(name)
            print(id)

            session["name"] = name[0]
            session["user_id"] = id[0]

            conn.close()

            return redirect(url_for("dashboard"))
        
    if not login:    
        return render_template("index.html", error="Wrong username or password")
    


    

@app.route("/dashboard")
def dashboard():
    name = session["name"]
    return render_template("dashboard.html", username = name)

@app.route("/overview")
def overview():
    name = session["name"]
    return render_template("overview.html", username = name)

@app.route("/add_transaction", methods=['POST','GET'])
def add_transaction():
    amount = request.form.get("amount")
    reciever = request.form.get("reciever")
    print(amount)
    print(reciever)

    conn = sql.connect("expensify.db")
    curr = conn.cursor()

    curr.execute("""INSERT INTO transactions (user_id, amount, sender, reciever) VALUES (?,?,?,?)""", (session["user_id"], amount, session["name"], reciever))

    conn.commit()
    conn.close()

    return dashboard()

@app.route("/add_business", methods=['POST', 'GET'])
def add_business():
    owner_id = session["user_id"]
    business_name = request.form.get("business_name")
    business_type = request.form.get("business_type")
    net_worth = request.form.get("net_worth")

    conn = sql.connect("expensify.db")
    curr = conn.cursor()    

    curr.execute("""INSERT INTO businesses (owner_id, business_name, business_type, net_worth) VALUES (?,?,?,?)""", (owner_id, business_name, business_type, net_worth))

    conn.commit()
    conn.close()

    return overview()

if __name__ == "__main__":
    app.run(debug=True)


        
        
        