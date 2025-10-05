from flask import Flask,render_template,request, redirect, url_for, session
import sqlite3
app=Flask(__name__)


app.secret_key = 'h-m-s-system'
# needed for data transfer

def initialise_db():
    conn = sqlite3.connect("hospital.db")
    cur = conn.cursor()
    # making table
    cur.execute("""CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        role TEXT NOT NULL DEFAULT 'patient')""")
    # making admin if not available
    cur.execute("SELECT * FROM users WHERE email = ?", ("admin@email",))
    if not cur.fetchone():
        cur.execute(
            "INSERT INTO users (name, email, password,role) VALUES (?, ?, ?,?)",
            ("admin", "admin@email", "root","admin")
        )
    conn.commit()
    conn.close()






@app.route("/")
def home():
    return "You are in default directory hit  /login or  /register"






@app.route("/login",methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        #input taken
        conn = sqlite3.connect("hospital.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email=? AND password = ?",(email,password))
        user = cursor.fetchone()
        conn.close()
        if user:
            # session["id"] = user[0]
            id = user[0]
            # session["name"] = user[1]
            name = user[1]
            # session["email"] = user[2]
            email = user[2]
            # session['password'] = user[3]
            password = user[3]
            # session["role"] = user[4]
            role = user[4]

            if email == email and password == password and role == 'admin':
                return redirect(url_for("admin"))
            elif email == email and password == password and role == "doctor":
                return redirect(url_for("doctor"))
            else:
                return redirect(url_for("patient",id=user[0]))
 

        else:
            return redirect(url_for("error"))

    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["name"]
        password = request.form["password"]
        email = request.form["email"]
        role = "patient"
        # print in console
        # print("Name:", name)
        # print("Email:", email)
        # print("Password:", password)
        conn = sqlite3.connect("hospital.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (name,email,password,role) VALUES(?,?,?,?)",(name,email,password,role))
        conn.commit()
        conn.close() 
        
        return redirect(url_for("login"))
    return render_template("register.html")




@app.route("/admin",methods=["GET", "POST"])
def admin():
    return render_template("admin.html")



@app.route("/patient/<int:id>",methods=["GET", "POST"])
def patient(id):
    conn = sqlite3.connect("hospital.db")
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM users WHERE id = ?", (id,))
    user = cursor.fetchone()
    conn.close()
    if user:
        name = user[0]
        return render_template("patient.html", name=name)
    else:
        name = "Guest"
        return render_template("error.html")


@app.route("/error",methods=["GET", "POST"])
def error():
    return render_template("error.html")


@app.route("/doctor",methods=["GET", "POST"])
def doctor():
    return render_template("doctor.html")


@app.route("/docadd",methods=["GET", "POST"])
def docadd():
    if request.method == "POST":
        name = request.form["name"]
        password = request.form["password"]
        email = request.form["email"]
        role = "doctor"
        conn = sqlite3.connect("hospital.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (name,email,password,role) VALUES(?,?,?,?)",(name,email,password,role))
        conn.commit()
        conn.close()
        return redirect(url_for("login"))
    return render_template("docadd.html")

@app.route("/cardiology",methods=["GET", "POST"])
def cardio():
    return render_template("department.html",dept = "Cardiology")

@app.route("/neurology",methods=["GET", "POST"])
def neuro():
    return render_template("department.html",dept = "Neurology")

@app.route("/orthopedics",methods=["GET", "POST"])
def ortho():
    return render_template("department.html",dept = "Orthopedics")

@app.route("/general",methods=["GET", "POST"])
def general():
    return render_template("department.html",dept = "General")

@app.route("/pediatrics",methods=["GET", "POST"])
def pedia():
    return render_template("department.html",dept = "Pediatrics")



if __name__ == "__main__":
    initialise_db()
    app.run(debug=True)