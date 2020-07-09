from flask import Flask, render_template, request, redirect, flash
from flask_login import UserMixin
from database.Logics import *

app = Flask(__name__) #Page 30

@app.route("/")
def index(): # View function
    return render_template('login.html')

@app.route("/register/<kind>")
def register(kind): # View function
    if kind == "worker":
        return render_template('registrotrabajador.html')
    elif kind == "user":
        return render_template('registrousuario.html')

@app.route("/servlet/register/<kind>", methods=['POST'])
def registerUser(kind):

    if kind == "user":
        success = False
        nombre = request.form.get('nombre')
        apellido = request.form.get('apellido')
        correo = request.form.get('email')
        contrasena = request.form.get('contraseña')
        dui = request.form.get('dui')
        celular = request.form.get('telefono')
        departamento = int(request.form.get('departamento'))
        municipio = int(request.form.get('municipio'))
        direccion = request.form.get('direccion')
        foto = request.form.get('imagen')

        admin = adminClientes()

        success = admin.insert(dui, nombre, apellido, celular, direccion, correo, contrasena, departamento, municipio, foto)
    elif kind == "worker":
        success = False
        

    if success is not None and success:
        redirect("/")
        flash("Bienvenido, usted ha sido registrado con éxito. Favor ingrese sus credenciales")
    else:
        redirect("/servlet/register/user")
        flash("Error interno. No se pudo registrar el valor. Favor intente nuevamente")



if __name__=='__main__':
    app.run(debug=True)