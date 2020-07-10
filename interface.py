from flask import Flask, render_template, request, redirect, flash, session, url_for
from flask_login import UserMixin
from database.Logics import adminAdministrador, adminClientes, adminTrabajadores, adminDepAndMun

app = Flask(__name__) #Page 30
app.secret_key = "Latrenge3456"


@app.route("/")
def index(): # View function
    if 'msg' in session:
        flash(session['msg']) # version no funcional de flash
        del(session['msg'])

    return render_template('login.html')

@app.route("/register/<string:kind>")
def register(kind): # View function

    admin = adminDepAndMun()
    ltsDepartamentos = admin.getDepartamentos()
    ltsMunicipios = admin.getMunicipios()
    
    if kind == "worker":
        return render_template('registrotrabajador.html', departamentos = ltsDepartamentos, municipios = ltsMunicipios)
    elif kind == "user":
        return render_template('registrousuario.html', departamentos = ltsDepartamentos, municipios = ltsMunicipios)

# Servlets
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
        nombre = request.form.get('nombre')
        apellido = request.form.get('apellido')
        correo = request.form.get('correo')
        contrasena = request.form.get('contraseña')
        dui = request.form.get('dui')
        telefono = request.form.get('telefono')
        genero = request.form.get('genero')
        descripcion = request.form.get('descripcion')
        departamento = int(request.form.get('departamento'))
        municipio = int(request.form.get('municipio'))
        direccion = (request.form.get('direccion'))
        nombre = request.form.get('nombre')
        descripcion = request.form.get('descripcion')
        foto = request.form.get('imagen')
        aceptado = 0 # Siempre se inicia sin estar aceptado
        membresia = 1 # La membresía 1 es una membresía siempre inactiva

        admin = adminTrabajadores()

        success = admin.insert(dui, nombre, apellido, telefono, direccion, correo, contrasena, descripcion, departamento, municipio, genero, aceptado, membresia, foto)

    if success is not None and success:
        session['msg'] = "Bienvenido, usted ha sido registrado con éxito. Favor ingrese sus credenciales"
        return redirect("/")
    else:
        session['msg']  = "Error interno. No se pudo registrar el valor. Favor intente nuevamente"
        return redirect("/servlet/register/user")
        
@app.route("/servlet/login", methods=['POST'])
def login():
    admin = adminAdministrador()
    password = str(request.form.get('contra'))
    mail = str(request.form.get('correo'))
    dictionary = admin.verify(mail, password)
    encontrado = dictionary['encontrado']
    permitido = dictionary['permitido']
    tipo = dictionary['tipo']

    if encontrado and permitido:
        if tipo == "admin":
            return "Registrado como admin"
        elif tipo == "worker":
            return "Registrado como trabajador"
        elif tipo == "user":
            return "Registrado como usuario"
    else:
        redirect("/")


if __name__=='__main__':
    app.run(debug=True)