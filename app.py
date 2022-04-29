from http import client
from flask import Flask, redirect, url_for, request, render_template, session
import datetime
import pymongo
from twilio.rest import Client

# FlASK
#############################################################
app = Flask(__name__)
app.permanent_session_lifetime = datetime.timedelta(days=365)
app.secret_key = "super secret key"
#############################################################


# MONGODB
#############################################################
mongodb_key = "mongodb+srv://desarrollowebuser:desarrollowebpassword@cluster0.dfh7g.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
client = pymongo.MongoClient(
    mongodb_key, tls=True, tlsAllowInvalidCertificates=True)
db = client.Escuela
cuentas = db.alumno
#############################################################


# Twilio
#############################################################
account_sid = "ACb3c6e7f498d0fc46b6ab08a28c67f039"
auth_token = "212e9922845565c0e602aa2771ed655f"
TwilioClient = Client(account_sid, auth_token)

############################################################# 

@app.route('/')
def home():
    email = None
    if 'email' in session:
        email = session['email']
    return render_template('index.html', error=email)


@app.route('/login', methods=['GET'])
def login():
    email = None
    if 'email' in session:
        email = session['email']
        return render_template('index.html', error=email)

    return render_template('login.html', error=email)


@app.route("/login", methods=["GET", "POST"])
def login():
    email = None
    if "email" in session:
        return render_template('index.html', data=session["email"])
    else:
        if (request.method == "GET"):
            return render_template("login.html", data="email")
        else:
            email = request.form["email"]
            password = request.form["password"]
            try:
                user = cuentas.find_one({"correo": (email)})
                if (user != None):
                    if(user["contrasena"]==password):
                        session["email"] = email
                        return render_template("index.html", data=email)
                    else:
                        return render_template("login.html")
                else:
                    return render_template("login.html")
                        
            except Exception as e:
                return "%s" % e


@app.route('/signup', methods=["GET", "POST"])
def signup():
    email = ""
    if 'email' in session:
        return render_template('index.html', data=email)
    else:
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        session['email'] = email
        session['password'] = password
        session['name'] = name

        user = {
            "matricula": "A1746643",
            "nombre": name,
            "correo": email,
            "contrasena": password
        }
        try:
            cuentas.insert_one(user)
            return render_template('index.html', data=email)
        except Exception as e:
            return "<p>Service error =>: %s %s" % type(e), e


@app.route('/logout')
def logout():
    if 'email' in session:
        email = session['email']
    session.clear()
    return redirect(url_for('home'))


@app.route("/usuarios")
def usuarios():
    cursor = cuentas.find({})
    users = []
    for doc in cursor:
        users.append(doc)
    return render_template("/usuarios.html", data=users)

@app.route("/insert")
def insertUsers():
    user = {
        "matricula" : "01746643",
        "nombre" : "Alejandro Perez",
        "correo" : "alep@tec.mx",
        "constrasena" : "nomerobesmicuenta"}
    

    try:
        cuentas.insert_one(user)
        return redirect(url_for("usuarios"))
    except Exception as e:
        return "<p>El servicio no esta disponible =>: %s %s" % type(e), e
    
@app.route("/find_one/<matricula>")
def find_one(matricula):
    try:
        user = cuentas.find_one({"matricula": (matricula)})
        if user == None:
            return "<p>La matricula %s nó existe</p>" % (matricula)
        else:
            return "<p>Encontramos: %s </p>" % (user)
    except Exception as e:
        return "%s" % e 

@app.route("/delete_one/<matricula>")
def delete_one(matricula):
    try:
        user = cuentas.delete_one({"matricula": (matricula)})
        if user.deleted_count == None:
            return "<p>La matricula %s nó existe</p>" % (matricula)
        else:
            return "<p>Eliminamos %d matricula: %s </p>" % (user.deleted_count, matricula)
    except Exception as e:
        return "%s" % e 

@app.route("/update", methods=["POST"])
def update():
    try:
        filter = {"matricula": request.form["matricula"]}
        user = {"$set": {
            "nombre": request.form["nombre"]
        }}
        cuentas.update_one(filter, user)
        return redirect(url_for("usuarios"))
    except Exception as e:
            return "error %s" % (e)


comogusten = TwilioClient.messages.create(
from_="whatsapp:+14155238886",
body="El usuario %s se agregó a tu pagina web" % (
request.form["nombre"]),
to="whatsapp:+5215614735056"
)
print(comogusten.sid) 