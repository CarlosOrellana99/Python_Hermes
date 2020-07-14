from flask import Flask, render_template, request, redirect, flash, session, url_for
from database.Logics import adminAdministrador, adminClientes, adminTrabajadores, adminOpciones,adminCategorias

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

    admin = adminOpciones()
    ltsDepartamentos = admin.getDepartamentos()
    ltsMunicipios = admin.getMunicipios()
    
    if kind == "worker":
        return render_template('registrotrabajador.html', departamentos = ltsDepartamentos, municipios = ltsMunicipios)
    elif kind == "user":
        return render_template('registrousuario.html', departamentos = ltsDepartamentos, municipios = ltsMunicipios)

# Servlets
@app.route("/servlet/register/<kind>", methods=['POST'])
def registerUser(kind): # View function

    if kind == "user":
        success = False
        nombre = request.form.get('nombre')
        apellido = request.form.get('apellido')
        correo = request.form.get('email')
        contrasena = request.form.get('contraseña')
        dui = request.form.get('dui')
        genero = request.form.get('genero')
        celular = request.form.get('telefono')
        departamento = int(request.form.get('departamento'))
        municipio = int(request.form.get('municipio'))
        direccion = request.form.get('direccion')
        foto = request.form.get('imagen')

        admin = adminClientes()

        success = admin.insert(dui, nombre, apellido, celular, direccion, correo, contrasena, departamento, municipio, genero, foto)
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
def login(): # View function
    admin = adminAdministrador()
    password = str(request.form.get('contra'))
    mail = str(request.form.get('correo'))
    dictionary = admin.verify(mail, password)
    encontrado = dictionary['encontrado']
    permitido = dictionary['permitido']
    tipo = dictionary['tipo']
    
    if encontrado and permitido:
        session['user'] = dictionary['user']
        if tipo == "admin":
            return "Registrado como admin"
        elif tipo == "worker":
            return "Registrado como trabajador"
        elif tipo == "user":
            return redirect("/Hammer.com/u")
    else:
        return redirect("/")

@app.route("/Hammer.com/u")
def paginaprincipalusuario():
    usuario = session['user']
    print (f"{usuario}")
    admincat = adminCategorias()
    listacategorias = admincat.getCategoriaConFoto()
    listacat = admincat.convertirimagenes(listacategorias)
    return render_template("principalUsuario.html",categorias=listacat,usuarioactivo=usuario)

@app.route("/Hammer.com/tu-Cuenta/")
def paginaprmodificarcuenta():
    usuario = session['user']
    admin = adminOpciones()
    ltsDepartamentos = admin.getDepartamentos()
    ltsMunicipios = admin.getMunicipios()
    return render_template("modificarUsuario.html",departamentos = ltsDepartamentos, municipios = ltsMunicipios,datosusuario=usuario)

@app.route("/test")
def test():
    return render_template("inicioadmin.html")

if __name__=='__main__':
    app.run(debug=True)
