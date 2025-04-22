from flask import *
import sqlite3 as sql
import hashlib
from datetime import datetime as dt
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import uuid
import io
import requests
import os

matplotlib.use('Agg')

class Database:
    def __init__(self, db_name="name.db"):
        self.db_name = db_name

    def execute(self, query, params=(), fetchone=False, fetchall=False, commit=True):
        conn = sql.connect(self.db_name)
        curr = conn.cursor()

        curr.execute(query, params)

        data = None

        if fetchone:
            data = curr.fetchone()
        elif fetchall:
            data = curr.fetchall()

        if commit:
            conn.commit()
        conn.close()

        return data
    
db = Database("expensify.db")
    

class User:
    def __init__(self, id, name, email, password):
        self.id = id
        self.name = name
        self.email = email
        self.password = password

    def hash_password(self, password):
        return hashlib.sha256(password.encode('utf-8')).hexdigest()

    def create(cls, name, email, password):
        user_id = str(uuid.uuid4())
        hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()

        db.execute("INSERT INTO users (id, name, email, password) VALUES (?,?,?,?)", (user_id, name, email, hashed_password), commit=True)

        return cls(user_id, name, email, hashed_password)
    
    def get_user_by_email(cls, email):
        user_data = db.execute("SELECT * FROM users WHERE email=?", (email,), fetchone=True, commit=True)

        if user_data:
            return cls(*user_data)
        else:
            return None
        
    def get_user_by_id(cls, id):
        user_data = db.execute("SELECT * FROM users WHERE id=?", (id,), fetchone=True, commit=True)
        if user_data:
            return cls(*user_data)
        else:
            return None
    
    def check_password(self, password):
        return self.password == self.hash_password(password)


class BusinessType:
    def __init__(self, id, business_type, tax):
        self.id = id
        self.business_type = business_type
        self.tax = tax

class Business(BusinessType):
    def __init__(self, id, owner, business_name, business_type, net_worth):
        self.id = id
        self.owner = owner
        self.business_name = business_name
        self.business_type = business_type
        self.net_worth = net_worth
        

    def create(cls, owner_id, business_type, business_name, net_worth):
        id = str(uuid.uuid4())
        db.execute("""INSERT INTO businesses (id, owner_id, business_name, business_type, net_worth) VALUES (?,?,?,?,?)""", (id, owner_id, business_name, business_type, net_worth))
        return cls(id, owner_id, business_type, business_name, net_worth)

    def get_by_owner(cls, owner_id):

        businesses = db.execute("SELECT * FROM businesses WHERE owner_id=?", (owner_id,), fetchall=True)
        if businesses:
            return [cls(*business) for business in businesses]
        else:
            return []
        
    def get_by_name(cls, name, owner_id):
        business = db.execute("SELECT * FROM businesses WHERE business_name=? AND owner_id=?", (name, owner_id), fetchone=True)

        if business: 
            return cls(*business)
        else:
            return None
        

class Transaction(Business):
    def __init__(self, id, amount, sender, reciever): 
        self.id = id
        self.amount = amount
        self.sender = sender
        self.reciever = reciever

    def create(cls, user_id, amount, sender, reciever):
        id = str(uuid.uuid4())
        db.execute("INSERT INTO transactions (id, user_id, amount, sender, reciever) VALUES (?,?,?,?,?)", (id, user_id, amount, sender, reciever))
        return cls(id, amount, sender, reciever)


def get_all_users():
    conn = sql.connect("expensify.db")
    curr = conn.cursor()

    curr.execute(""" SELECT * FROM users """)
    data = curr.fetchall()

    conn.close()

    return data

def get_businesses(owner_id):
    conn = sql.connect("expensify.db")
    curr = conn.cursor()

    curr.execute("""SELECT business_name FROM businesses WHERE owner_id=? """, (owner_id,))
    data = curr.fetchall()

    conn.close()

    return [business[0] for business in data]

def get_business_history(business_id):
    conn = sql.connect("expensify.db")
    curr = conn.cursor()

    curr.execute("""SELECT timestamp, net_worth FROM business_history WHERE business_id = ? ORDER BY timestamp ASC""", (business_id,))
    history = curr.fetchall()

    conn.close()
    
    return history




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
    name = request.form.get("name")
    email = request.form.get("username")
    password = request.form.get("password")

    if User.get_user_by_email(User, email):
        return render_template("signup.html", error="Email already in use")
    
    user = User.create(User, name, email, password)

    session["user_id"] = user.id

    return redirect(url_for("index"))
    



@app.route("/submit", methods=['GET', 'POST'])
def submit():
    email = request.form.get('username')
    password = request.form.get('password')

    user = User.get_user_by_email(User, email)

    if user and user.check_password(password):
        session["user_id"] = user.id
        return redirect(url_for("dashboard"))
    else:
        return render_template("index.html", error="Wrong username or password")
    

@app.route("/dashboard")
def dashboard():
    user_id = session["user_id"]
    api_url = "https://api.api-ninjas.com/v1/facts"
    response = requests.get(api_url, headers={'X-Api-Key': 'k96d+MICigaE3Jrx6iAoVw==jzOdUIjbyAEXw5Yw'})
    if response.status_code == requests.codes.ok:
        print(f"Fact of the day: {response.json()[0]['fact']}")
        fact = f"Fact of the day: {response.json()[0]["fact"]}"
    else:
        print(f"Error: {response.status_code} {response.text}")
        fact = f"Error: {response.status_code} {response.text}"



    name = User.get_user_by_id(User, user_id).name

    data = Business.get_by_owner(Business, user_id)
    businesses = []
    for business in data:
        businesses.append(business.business_name)

    has_businesses = len(businesses) > 0

    print(businesses)
    
    transaction_error = request.args.get("transaction_error")

    plot_filename = request.args.get("plot_filename")

    plot_error = request.args.get("plot_error")
    
    return render_template("dashboard.html", username = name, businesses = businesses, has_businesses=has_businesses, transaction_error=transaction_error, api_text = fact, plot_filename=plot_filename, plot_error=plot_error)

@app.route("/get_business_data", methods=["GET", "POST"])
def get_business_data():
    user_id = session["user_id"]
    if request.method =="POST":
        business_name = request.form.get("business_name")
        print(business_name)
        if business_name:
            business_id = db.execute("SELECT id FROM businesses WHERE business_name=? AND owner_id=?", (business_name, user_id), fetchone=True)
            if business_id:
                data = db.execute("SELECT timestamp, net_worth FROM business_history WHERE business_id=?", (business_id[0],), fetchall=True)
                x = []
                y = []

                for business in data:
                    x.append(business[0])
                    y.append(business[1])

                fig, ax = plt.subplots(figsize=(6, 4))
                
                ax.plot(x, y)
                ax.set_title(f"Net worth over time - {business_name}")
                fig.autofmt_xdate()

                filename = f"plot_{user_id}_{business_id[0]}.png"
                filepath = os.path.join("static", filename)
                fig.savefig(filepath)

                return redirect(url_for("dashboard", plot_filename=filename))
            
        return redirect(url_for("dashboard", plot_error="No such business was found"))
    
    return redirect(url_for("dashboard"))

@app.route("/overview")
def overview():
    user_id = session["user_id"]

    name = User.get_user_by_id(User, user_id).name

    add_business_error = request.args.get("add_business_error")

    return render_template("overview.html", username = name, add_business_error=add_business_error)
    

@app.route("/add_transaction", methods=['POST','GET'])
def add_transaction():
    user_id = session["user_id"]
    amount = float(request.form.get("amount"))
    sender = request.form.get("sender")
    reciever = request.form.get("reciever")

    sender_id = db.execute("""SELECT id FROM businesses WHERE business_name = ? AND owner_id=?""", (sender, user_id), fetchone=True)
    reciever_id = db.execute("""SELECT id FROM businesses WHERE business_name = ? AND owner_id=?""", (reciever, user_id), fetchone=True)


    if sender_id and reciever_id:
        sender_net_worth = db.execute("""SELECT net_worth FROM businesses WHERE id=?""", (sender_id[0],), fetchone=True)
        if  amount >= 0:          
            if (sender_net_worth[0]-amount) > 0:
                Transaction.create(cls=Transaction, user_id=user_id, amount=amount, sender=sender_id[0], reciever=reciever_id[0])
                
                db.execute("""UPDATE businesses SET net_worth=net_worth-? WHERE id=?""", (amount, sender_id[0]))
                db.execute("""UPDATE businesses SET net_worth=net_worth+? WHERE id=?""", (amount, reciever_id[0]))

                sender_net_worth = db.execute("""SELECT net_worth FROM businesses WHERE id=?""", (sender_id[0],), fetchone=True)
                db.execute("""INSERT INTO business_history (id, business_id, net_worth) VALUES (?,?,?)""", (str(uuid.uuid4()), sender_id[0], sender_net_worth[0]))

                reciever_net_worth = db.execute("""SELECT net_worth FROM businesses WHERE id=?""", (reciever_id[0],), fetchone=True)
                db.execute("""INSERT INTO business_history (id, business_id, net_worth) VALUES (?,?,?)""", (str(uuid.uuid4()), reciever_id[0], reciever_net_worth[0]))

                print("transaction added!")
                
                return redirect(url_for("dashboard"))
            
            else:
                return redirect(url_for("dashboard", transaction_error = "Not enough funds!"))
            
        else:
            return redirect(url_for("dashboard", transaction_error = "Can't send negative amount of money"))
        
    else:
        return redirect(url_for("dashboard", transaction_error = "Sending or Recieving business doesn't exist"))


        

@app.route("/add_business", methods=['POST', 'GET'])
def add_business():
    owner_id = session["user_id"]
    business_name = request.form.get("business_name")
    business_type = request.form.get("business_type")
    net_worth = float(request.form.get("net_worth"))

    business_list = db.execute("SELECT business_name FROM businesses WHERE owner_id=?", (owner_id,), fetchall=True)
    is_in_use = False

    for business in business_list:
        if business[0] == business_name:
            is_in_use = True

    if not is_in_use:
        if net_worth >= 0:
            Business.create(Business, owner_id=owner_id, business_type=business_type, business_name=business_name, net_worth=net_worth)
            return redirect(url_for("overview"))
        else:
            return redirect(url_for("overview", add_business_error = "can't add business with negative net worth"))
    else:
        return redirect(url_for("overview", add_business_error = "this name is already in use!"))


    

if __name__ == "__main__":
    app.run(debug=True)


        
        
        