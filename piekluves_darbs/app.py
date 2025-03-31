from flask import *
import sqlite3 as sql
import hashlib
import datetime as dt
import matplotlib.pyplot as plt
import numpy as np
import uuid
import io

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

    def create(self, cls,  name, email, password):
        user_id = str(uuid.uuid4())
        hashed_password = self.hash_password(password)

        db.execute("INSERT INTO users (id, name, email, password) VALUES (?,?,?,?)", (user_id, name, email, password), commit=True)

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
    def __init__(self, id, business_type, business_name, net_worth, owner):
        self.id = id
        self.business_type = business_type
        self.business_name = business_name
        self.net_worth = net_worth
        self.owner = owner

    def get_by_owner(cls, owner_id):

        businesses = db.execute("SELECT * FROM businesses WHERE owner_id=?", (owner_id,), fetchall=True)
        if businesses:
            return [cls(*business) for business in businesses]
        else:
            return []
        

        



        

class Transaction(Business):
    def __init__(self, id, amount, sender, reciever): 
        self.id = id
        self.amount = amount
        self.sender = sender
        self.reciever = reciever

    def create(cls, user_id, amount, sender, reciever):
        id = uuid.uuid4()
        db.execute("INSERT INTO transactions (id, user_id, amount, sender, reciever) VALUES (?,?,?,?,?)", (id, user_id, amount, sender, reciever))





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

    if User.get_user_by_email(email):
        return render_template("signup.html", error="Email already in use")
    
    user = User.create(name, email, password)

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

    name = User.get_user_by_id(User, user_id).name

    data = Business.get_by_owner(Business, user_id)
    businesses = []
    for business in data:
        businesses.append(business.business_name)

    print(businesses)
    



    return render_template("dashboard.html", username = name, businesses = businesses)

# @app.route("/plot")
# def plot_history():
#     pass
#     data = db.execute("SELECT timestamp, net_worth FROM business_history WHERE business_id=?", (business_id,), fetchall=True)
#     x = []
#     y = []

#     for tuple in data:
#         x.append(tuple[0])
#         y.append(tuple[1])
    
#     fig, ax = plt.subplots()
#     ax.plot(x, y)
    
#     buf = io.BytesIO()
#     fig.savefig(buf, format='png')
#     buf.seek(0)
    
#     return send_file(buf, mimetype='image/png')

@app.route("/overview")
def overview():
    user_id = session["user_id"]

    name = User.get_user_by_id(User, user_id).name

    return render_template("overview.html", username = name)
    

@app.route("/add_transaction", methods=['POST','GET'])
def add_transaction():
    user_id = session["user_id"]
    amount = request.form.get("amount")
    sender = request.form.get("sender")
    reciever = request.form.get("reciever")

    transaction = Transaction.create(user_id, amount, sender, reciever)

    db.execute("""UPDATE businesses SET net_worth=net_worth+? WHERE business_name = ?""", (amount, sender))

    business_id = db.execute("""SELECT id FROM businesses WHERE business_name = ?""", (sender,), fetchone=True)

    net_worth = db.execute("""SELECT net_worth FROM businesses WHERE business_name = ?""", (sender,), fetchone=True)

    db.execute("""INSERT INTO business_history (business_id, net_worth) VALUES (?,?)""", (business_id[0], net_worth[0]))

    return redirect(url_for("dashboard"))

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


        
        
        