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
def home():
    return render_template("index.html")


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/login_check", methods=["POST"])
def login_check():

    login_type = request.form["type"]
    userid = request.form["userid"]
    password = request.form["password"]

    if login_type == "admin":
        if userid == "BCA2026" and password == "BCA2026":
            return redirect("/dashboard")
        else:
            return "Invalid Admin Login"

    if login_type == "customer":
        if userid == "CUST001" and password == "1234":
            return redirect("/customer_dashboard")
        else:
            return "Invalid Customer Login"


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
        cur.execute("SELECT COUNT(*) FROM bills")
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

    search = request.args.get("search")

    c = connect_db()
    cur = c.cursor()

    if search:
        cur.execute(
            "SELECT * FROM customers WHERE name LIKE ?",
            ('%' + search + '%',)
        )
    else:
        cur.execute("SELECT * FROM customers")

    d = cur.fetchall()

    c.close()

    return render_template("customer.html", customers=d)


@app.route("/add_customer", methods=["POST"])
def add_customer():

    c = connect_db()
    cur = c.cursor()

    cur.execute(
        "INSERT INTO customers(name,mobile,email,address,panel) VALUES(?,?,?,?,?)",
        (
            request.form["name"],
            request.form["mobile"],
            request.form["email"],
            request.form["address"],
            request.form["panel"]
        )
    )

    c.commit()
    c.close()

    return redirect("/customer")


@app.route("/delete_customer/<int:id>")
def delete_customer(id):

    c = connect_db()
    cur = c.cursor()

    cur.execute("DELETE FROM customers WHERE id=?", (id,))

    c.commit()
    c.close()

    return redirect("/customer")
@app.route("/edit_customer/<int:id>")
def edit_customer(id):

    c = connect_db()
    cur = c.cursor()

    cur.execute("SELECT * FROM customers WHERE id=?", (id,))
    customer = cur.fetchone()

    c.close()

    return render_template("edit_customer.html", customer=customer)


@app.route("/update_customer/<int:id>", methods=["POST"])
def update_customer(id):

    c = connect_db()
    cur = c.cursor()

    cur.execute("""
        UPDATE customers
        SET name=?,
            mobile=?,
            email=?,
            address=?,
            panel=?
        WHERE id=?
    """, (
        request.form["name"],
        request.form["mobile"],
        request.form["email"],
        request.form["address"],
        request.form["panel"],
        id
    ))

    c.commit()
    c.close()

    return redirect("/customer")
@app.route("/panel")
def panel():

    c = connect_db()
    cur = c.cursor()

    cur.execute("SELECT * FROM panels")
    panels = cur.fetchall()

    c.close()

    return render_template("panel.html", panels=panels)

@app.route("/add_panel", methods=["POST"])
def add_panel():

    c = connect_db()
    cur = c.cursor()

    cur.execute("""
        INSERT INTO panels(panel_name, company, watt, price, stock)
        VALUES(?,?,?,?,?)
    """, (
        request.form["panel_name"],
        request.form["company"],
        request.form["watt"],
        request.form["price"],
        request.form["stock"]
    ))

    c.commit()
    c.close()

    return redirect("/panel")

@app.route("/delete_panel/<int:id>")
def delete_panel(id):

    c = connect_db()
    cur = c.cursor()

    cur.execute("DELETE FROM panels WHERE id=?", (id,))

    c.commit()
    c.close()

    return redirect("/panel")


@app.route("/edit_panel/<int:id>")
def edit_panel(id):

    c = connect_db()
    cur = c.cursor()

    cur.execute("SELECT * FROM panels WHERE id=?", (id,))
    panel = cur.fetchone()

    c.close()

    return render_template("edit_panel.html", panel=panel)


@app.route("/update_panel/<int:id>", methods=["POST"])
def update_panel(id):

    c = connect_db()
    cur = c.cursor()

    cur.execute("""
        UPDATE panels
        SET panel_name=?,
            company=?,
            watt=?,
            price=?,
            stock=?
        WHERE id=?
    """, (
        request.form["panel_name"],
        request.form["company"],
        request.form["watt"],
        request.form["price"],
        request.form["stock"],
        id
    ))

    c.commit()
    c.close()

    return redirect("/panel") 

@app.route("/installation")
def installation():

    c = connect_db()
    cur = c.cursor()

    cur.execute("SELECT * FROM installations")
    installations = cur.fetchall()

    c.close()

    return render_template("installation.html", installations=installations)


@app.route("/add_installation", methods=["POST"])
def add_installation():

    c = connect_db()
    cur = c.cursor()

    cur.execute("""
        INSERT INTO installations(customer_name, install_date, technician, status)
        VALUES(?,?,?,?)
    """, (
        request.form["customer_name"],
        request.form["install_date"],
        request.form["technician"],
        request.form["status"]
    ))

    c.commit()
    c.close()

    return redirect("/installation")


@app.route("/delete_installation/<int:id>")
def delete_installation(id):

    c = connect_db()
    cur = c.cursor()

    cur.execute("DELETE FROM installations WHERE id=?", (id,))

    c.commit()
    c.close()

    return redirect("/installation")


@app.route("/edit_installation/<int:id>")
def edit_installation(id):

    c = connect_db()
    cur = c.cursor()

    cur.execute("SELECT * FROM installations WHERE id=?", (id,))
    installation = cur.fetchone()

    c.close()

    return render_template("edit_installation.html", installation=installation)


@app.route("/update_installation/<int:id>", methods=["POST"])
def update_installation(id):

    c = connect_db()
    cur = c.cursor()

    cur.execute("""
        UPDATE installations
        SET customer_name=?,
            install_date=?,
            technician=?,
            status=?
        WHERE id=?
    """, (
        request.form["customer_name"],
        request.form["install_date"],
        request.form["technician"],
        request.form["status"],
        id
    ))

    c.commit()
    c.close()

    return redirect("/installation")


@app.route("/billing")
def billing():

    c = connect_db()
    cur = c.cursor()

    cur.execute("SELECT * FROM bills")
    bills = cur.fetchall()

    c.close()

    return render_template("billing.html", bills=bills)

@app.route("/add_bill", methods=["POST"])
def add_bill():

    c = connect_db()
    cur = c.cursor()

    # Auto Bill Number
    cur.execute("SELECT COUNT(*) FROM bills")
    bill_count = cur.fetchone()[0] + 1
    bill_no = f"BILL{bill_count:03d}"

    cur.execute("""
        INSERT INTO bills(bill_no, customer_name, amount, gst, total)
        VALUES(?,?,?,?,?)
    """, (
        bill_no,
        request.form["customer_name"],
        request.form["amount"],
        request.form["gst"],
        request.form["total"]
    ))

    c.commit()
    c.close()

    return redirect("/billing")

@app.route("/delete_bill/<int:id>")
def delete_bill(id):

    c = connect_db()
    cur = c.cursor()

    cur.execute("DELETE FROM bills WHERE id=?", (id,))

    c.commit()
    c.close()

    return redirect("/billing")


@app.route("/edit_bill/<int:id>")
def edit_bill(id):

    c = connect_db()
    cur = c.cursor()

    cur.execute("SELECT * FROM bills WHERE id=?", (id,))
    bill = cur.fetchone()

    c.close()

    return render_template("edit_bill.html", bill=bill)


@app.route("/update_bill/<int:id>", methods=["POST"])
def update_bill(id):

    c = connect_db()
    cur = c.cursor()

    cur.execute("""
        UPDATE bills
        SET bill_no=?,
            customer_name=?,
            amount=?,
            gst=?,
            total=?
        WHERE id=?
    """, (
        request.form["bill_no"],
        request.form["customer_name"],
        request.form["amount"],
        request.form["gst"],
        request.form["total"],
        id
    ))

    c.commit()
    c.close()

    return redirect("/billing")

@app.route("/report")
def report():

    c = connect_db()
    cur = c.cursor()

    cur.execute("SELECT COUNT(*) FROM customers")
    total_customers = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM panels")
    total_panels = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM installations")
    total_installations = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM bills")
    total_bills = cur.fetchone()[0]

    c.close()

    return render_template(
        "report.html",
        total_customers=total_customers,
        total_panels=total_panels,
        total_installations=total_installations,
        total_bills=total_bills
    )


@app.route("/customer_dashboard")
def customer_dashboard():
    return render_template("customer_dashboard.html")

@app.route("/print_bill/<int:id>")
def print_bill(id):

    c = connect_db()
    cur = c.cursor()

    cur.execute("SELECT * FROM bills WHERE id=?", (id,))
    bill = cur.fetchone()

    c.close()

    return render_template("print_bill.html", bill=bill)

@app.route("/about")
def about():
    return render_template("about.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)