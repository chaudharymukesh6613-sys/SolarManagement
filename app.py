from flask import Flask, render_template, request, redirect
import sqlite3
import os

app = Flask(
    __name__,
    template_folder=os.path.join(os.getcwd(), "templates"),
    static_folder=os.path.join(os.getcwd(), "static")
)
def connect_db():
    return sqlite3.connect("solar.db")
@app.route("/")
def home(): return render_template("index.html")
@app.route("/login")
def login(): return render_template("login.html")
@app.route("/dashboard")
def dashboard():
    c = connect_db()
    cur = c.cursor()

    cur.execute("SELECT COUNT(*) FROM customers")
    total_customers = cur.fetchone()[0]

    try:
        cur.execute("SELECT COUNT(*) FROM panels")
        total_panels = cur.fetchone()[0]
    except:
        total_panels = 0

    try:
        cur.execute("SELECT COUNT(*) FROM installations")
        total_installations = cur.fetchone()[0]
    except:
        total_installations = 0

    try:
        cur.execute("SELECT COUNT(*) FROM billing")
        total_bills = cur.fetchone()[0]
    except:
        total_bills = 0

    c.close()

    return render_template(
        "dashboard.html",
        total_customers=total_customers,
        total_panels=total_panels,
        total_installations=total_installations,
        total_bills=total_bills
    )
@app.route("/customer")
def customer():
    c=connect_db();cur=c.cursor();cur.execute("SELECT * FROM customers");d=cur.fetchall();c.close()
    return render_template("customer.html",customers=d)
@app.route("/add_customer",methods=["POST"])
def add_customer():
    c=connect_db();cur=c.cursor()
    cur.execute("INSERT INTO customers(name,mobile,email,address,panel) VALUES(?,?,?,?,?)",(request.form["name"],request.form["mobile"],request.form["email"],request.form["address"],request.form["panel"]))
    c.commit();c.close();return redirect("/customer")
@app.route("/delete_customer/<int:id>")
def delete_customer(id):
    c=connect_db();cur=c.cursor();cur.execute("DELETE FROM customers WHERE id=?",(id,));c.commit();c.close();return redirect("/customer")
@app.route("/panel")
def panel(): return render_template("panel.html")
@app.route("/installation")
def installation(): return render_template("installation.html")
@app.route("/billing")
def billing(): return render_template("billing.html")
@app.route("/report")
def report(): return render_template("report.html")
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)