from flask import Flask, render_template, request, redirect, flash, session, url_for
from database.Logics import adminAdministrador, adminClientes, adminTrabajadores, adminOpciones,adminCategorias,adminCitas

app = Flask(__name__) #Page 30
app.secret_key = "Latrenge3456"


@app.route("/")
def index(): # View function
    session['user'] = None
    session['kind'] = None

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
        session['kind'] = tipo
        if tipo == "admin":
            return redirect("/Hammer.com/admin")
        elif tipo == "worker":
            return "Registrado como trabajador"
        elif tipo == "user":
            print(dictionary['user'])
            return redirect("/Hammer.com/u")
    else:
        return redirect("/")

# Admin UI
@app.route("/Hammer.com/admin")
def adminIndex():
    adminA = adminAdministrador()
    admin = session['user']
    tipo = session['kind']
    adminCompleto = adminA.getAdminByCorreo(admin['correo'])
    if not tipo == "admin":
        return f"""<h1>You do not have access to this page</h1><br>
                    <h2>Please sing up in this </h2><a href="/">link</a>""", 402
    else:
        
        top5 = adminA.getTopN()
        stats = adminA.getStats()
        return render_template("inicioadmin.html", top5 = top5, admin =  adminCompleto, stats = stats)

@app.route("/Hammer.com/admin/<acceso>")
def TrabajadoresAcceso(acceso):
    adminA = adminAdministrador()
    tipo = session['kind']
    admin = session['user']
    adminCompleto = adminA.getAdminByCorreo(admin['correo'])

    if not tipo == "admin":
        return f"""<h1>You do not have access to this page</h1><br>
                    <h2>Please sing up in this </h2><a href="/">link</a>""", 402  
    else:
        if acceso== 'sinAcceso':
            lista = adminA.getTrabajadoresSinAcceso()
            return render_template("trabajadoresSinAcceso.html", admin = adminCompleto, trabajadores = lista)
        elif acceso== 'conAcceso':
            lista = adminA.getTrabajadoresConAcceso()
            return render_template("trabajadoresConAcceso.html", admin = adminCompleto, trabajadores = lista)

@app.route("/Hammer.com/admin/servlet", methods=['POST'])
def adminServlet():
    tipo = session['kind']
    if not tipo == "admin":
        return f"""<h1>You do not have access to this page</h1><br>
                    <h2>Please sing up in this </h2><a href="/">link</a>""", 402    
    else:
        idForm = request.form.get('id')
        if idForm== '1':
            adminA = adminAdministrador()
            exito = adminA.revocarLicenciaDeudores()
            if exito:
                return redirect("/Hammer.com/admin")
            else:
                return "Process failed. Either there are no licences to revoque or an internal problem has occurred"

@app.route("/Hammer.com/admin/buscar", methods=['GET'])
def adminBuscar():
    adminA = adminAdministrador()
    admin = session['user']
    tipo = session['kind']
    adminCompleto = adminA.getAdminByCorreo(admin['correo'])
    if not tipo == "admin":
        return f"""<h1>You do not have access to this page</h1><br>
                    <h2>Please sing up in this </h2><a href="/">link</a>""", 402    
    word = str(request.args.get('wd'))
    adminT = adminTrabajadores()
    lista = adminT.fetchAllWorkersByWord(word)
    return render_template("busquedaAdmin.html", trabajadores = lista, admin = adminCompleto)

# User UI
@app.route("/Hammer.com/u")
def paginaprincipalusuario():
    usuario = session['user']
    print (f"{usuario}")
    admincat = adminCategorias()
    listacategorias = admincat.getCategoriaConFoto()
    listacat = admincat.convertirimagenes(listacategorias)
    admin = adminOpciones()
    ltsDepartamentos = admin.getDepartamentos()
    return render_template("principalUsuario.html",categorias=listacat,usuarioactivo=usuario,departamentos =ltsDepartamentos)

@app.route("/Hammer.com/tu-Cuenta/")
def paginaprmodificarcuenta():
    usuario = session['user']
    session['idusuarioactual']= usuario['id']
    session['correoactual']=usuario['correo']
    session['passwordactual']=usuario['contra']
    admin = adminOpciones()
    ltsDepartamentos = admin.getDepartamentos()
    ltsMunicipios = admin.getMunicipios()
    return render_template("modificarUsuario.html",departamentos = ltsDepartamentos, municipios = ltsMunicipios,datosusuario=usuario)

@app.route("/Hammer.com/servlet/tu-Cuenta/", methods=['POST'])
def modificarcuenta():
    success=False
    idusuario= session['idusuarioactual']
    correoactual = session['correoactual']
    passwordactual=session['passwordactual']
    nombre = request.form.get('nombre')
    apellido = request.form.get('apellido')
    correo = request.form.get('email')
    contrasena = request.form.get('contraseña')
    dui = request.form.get('dui')
    telefono = request.form.get('telefono')
    genero = request.form.get('genero')
    departamento = int(request.form.get('departamento'))
    municipio = int(request.form.get('municipio'))
    direccion = (request.form.get('direccion'))
    diccionariouser = {"id": idusuario, "nombre": nombre,"apellido":apellido,"correo":correo,"contra":contrasena,"dui":dui,
                        "telefono":telefono,"genero":genero,"departamento":departamento,"municipio":municipio,"direccion":direccion}
    adminmodificar=adminClientes()
    success = adminmodificar.updateusuario(diccionariouser)
    if success == True:
        print("datos de vuenta modificados con exito")
        session['msg'] = "Sus datos de cuenta ha sido modificado con exito, vuelva a ingresar"
        session['idusuarioactual']=""
        usuario=session['user']
        if not correoactual== diccionariouser['correo'] or not passwordactual==diccionariouser['contra']:
            session['correoactual']=""
            session['passwordactual']=""
            return redirect("/")
        else:
            session['user']= diccionariouser
            return redirect("/Hammer.com/tu-Cuenta/")

@app.route("/Hammer.com/citas")
def CitasCliente():
    admincitas=adminCitas()
    usuario = session['user']
    citaspendientes,citasnoconfirmadas,citaspasadas=admincitas.getCitasCliente(usuario['id'])
    return render_template("citasU.html",citaspendientes=citaspendientes,citasnoconfirmadas=citasnoconfirmadas,citaspasadas=citaspasadas)

@app.route("/Hammer.com/buscarTrabajadores",methods=['POST'])
def busquedaTrabajadoresCliente():
    palabra = request.form.get('palabra')
    
    return render_template("busquedaTrabajadores.html")

# Tests
@app.route("/test")
def test():
    adminA = adminAdministrador()
    dictionary = adminA.verify("moris32345@hotmail.es", "moris32345", True)
    admin = dictionary['user']
    top5 = adminA.getTopN()
    stats = adminA.getStats()
    return render_template("inicioadmin.html", top5 = top5, admin =  admin, stats = stats)

@app.route("/test2")
def test2():
    adminA = adminAdministrador()
    dictionary = adminA.verify("moris32345@hotmail.es", "moris32345", True)
    admin = dictionary['user']
    top5 = adminA.getTopN()
    stats = adminA.getStats()
    return render_template("busquedaAdmin.html", top5 = top5, admin =  admin, stats = stats)

if __name__=='__main__':
    app.run(debug=True)
