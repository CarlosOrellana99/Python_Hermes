from flask import Flask, render_template, request, redirect, flash, session, url_for
from database.Logics import adminAdministrador, adminClientes, adminTrabajadores, adminOpciones,adminCategorias,adminCitas
import base64

app = Flask(__name__) #Page 30
app.secret_key = "Latrenge3456"


@app.route("/")
def index(): # View function
    session['user'] = {"correo": "esteCorreoNoExiste<>"}
    session['kind'] = "None"

    admin = adminAdministrador()
    images = admin.getImages()

    if 'msg' in session:
        flash(session['msg']) # version no funcional de flash
        del(session['msg'])

    return render_template('login.html', imagenes = images)

@app.route("/register/<string:kind>")
def register(kind): # View function
    adminA = adminAdministrador()
    images = adminA.getImages()
    admin = adminOpciones()
    ltsDepartamentos = admin.getDepartamentos()
    ltsMunicipios = admin.getMunicipios()
    
    if kind == "worker":
        return render_template('registrotrabajador.html', departamentos = ltsDepartamentos, municipios = ltsMunicipios, imagenes = images)
    elif kind == "user":
        return render_template('registrousuario.html', departamentos = ltsDepartamentos, municipios = ltsMunicipios, imagenes = images)

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
        imagen = request.files['imagen']
        foto = imagen.read()
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
        imagen = request.files['imagen']
        foto = imagen.read()
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
            return redirect("/Hammer.com/worker")
        elif tipo == "user":
            return redirect("/Hammer.com/u")
    else:
        return redirect("/")

# Admin UI
@app.route("/Hammer.com/admin")
def adminIndex():
    adminA = adminAdministrador()
    admin = session['user']
    tipo = session['kind']
    image = adminA.getImages()
    adminCompleto = adminA.getAdminByCorreo(admin['correo'])
    if not tipo == "admin":
        return f"""<h1>You do not have access to this page</h1><br>
                    <h2>Please sing up in this </h2><a href="/">link</a>""", 402
    else:
        
        top5 = adminA.getTopN()
        stats = adminA.getStats()
        return render_template("inicioadmin.html", top5 = top5, admin =  adminCompleto, stats = stats, imagenes = image)

@app.route("/Hammer.com/admin/<acceso>")
def TrabajadoresAcceso(acceso):
    adminA = adminAdministrador()
    image = adminA.getImages()
    tipo = session['kind']
    admin = session['user']
    adminCompleto = adminA.getAdminByCorreo(admin['correo'])

    if not tipo == "admin":
        return f"""<h1>You do not have access to this page</h1><br>
                    <h2>Please sing up in this </h2><a href="/">link</a>""", 402  
    else:
        if acceso== 'sinAcceso':
            lista = adminA.getTrabajadoresSinAcceso()
            cantidad = len(lista)
            return render_template("trabajadoresSinAcceso.html", admin = adminCompleto, trabajadores = lista, cantidad = cantidad,  imagenes = image)
        elif acceso== 'conAcceso':
            lista = adminA.getTrabajadoresConAcceso()
            cantidad = len(lista)
            return render_template("trabajadoresConAcceso.html", admin = adminCompleto, trabajadores = lista, imagenes = image, cantidad = cantidad)

@app.route("/Hammer.com/admin/servlet", methods=['POST'])
def adminServlet():
    tipo = session['kind']
    if not tipo == "admin":
        return f"""<h1>You do not have access to this page</h1><br>
                    <h2>Please sing up in this </h2><a href="/">link</a>""", 402   
    else:
        idForm = request.form.get('id')
        adminA = adminAdministrador()
        adminT = adminTrabajadores()
        if idForm== '1':
            exito = adminA.revocarLicenciaDeudores()
            if exito:
                return redirect("/Hammer.com/admin")
            else:
                return "Process failed. Either there are no licences to revoque or an internal problem has occurred"
        if idForm == '2':
            idT = request.form.get('idT')
            adminT.setAcceso(idT, 1)
            render = f"/Hammer.com/admin/worker/visulize/{idT}"
            
            return redirect(render)

        if idForm == '3':
            idT = request.form.get('idT')
            success = adminT.setAcceso(idT, 0)
            print(success)
            render = f"/Hammer.com/admin/worker/visulize/{idT}"
            print(render)
            return redirect(render)

@app.route("/Hammer.com/admin/buscar", methods=['POST'])
def adminBuscar():
    adminA = adminAdministrador()
    images = adminA.getImages()
    admin = session['user']
    tipo = session['kind']
    adminCompleto = adminA.getAdminByCorreo(admin['correo'])
    if not tipo == "admin":
        return redirect("/Hammer.com/notAccess")    
    word = str(request.form.get('wd'))
    adminT = adminTrabajadores()
    lista = adminT.fetchAllWorkersByWord(word, kind = ['trabajadores.DUI', 'trabajadores.Nombre', 'trabajadores.Apellido'])
    numeros = range(5,105,5)
    numero = len(lista)
    return render_template("busquedaAdmin.html", trabajadores = lista, admin = adminCompleto, numeros = numeros, word = word, imagenes = images, cantidad = numero)

@app.route("/Hammer.com/admin/buscar/advanced/", methods=['POST'])
def adminBuscarConfigurado():
    adminA = adminAdministrador()
    images = adminA.getImages()
    admin = session['user']
    tipo = session['kind']
    adminCompleto = adminA.getAdminByCorreo(admin['correo'])
    if not tipo == "admin":
        return redirect("/Hammer.com/notAccess") 
    adminT = adminTrabajadores()
    cantidad = (request.form.get('cantidad'))
    buscarEn = str(request.form.get('buscarEn'))
    word = str(request.form.get('wd'))
    lista = adminT.fetchAllWorkersByWord(word, cantidad, [buscarEn])

    numero = len(lista)
    numeros = range(5,105,5)
    return render_template("busquedaAdmin.html", trabajadores = lista, admin = adminCompleto, numeros = numeros, word = word, imagenes= images, cantidad= numero)


@app.route("/Hammer.com/admin/worker/visulize/<idT>")
def workerVisualize(idT):
    adminT = adminTrabajadores()
    adminA = adminAdministrador()
    imagenes = adminA.getImages()
    trabajador = adminT.getWorkerbyId(idT)
    admin = session['user']
    tipo = session['kind']
    adminCompleto = adminA.getAdminByCorreo(admin['correo'])
    historial = adminT.HistorialTrabajadores(idT)
    if not tipo == "admin":
        return redirect("/Hammer.com/notAccess") 
    return render_template("perfilDeTrabajadoresAdmin.html", worker = trabajador, imagenes = imagenes, admin = adminCompleto, historial = historial)


# User UI
@app.route("/Hammer.com/u")
def paginaprincipalusuario():
    adminC=adminClientes()
    user = session['user']
    print(user)
    usuario = adminC.getUserbyCorreo(user['correo'])
    admincat = adminCategorias()
    listacategorias = admincat.getCategoriaConFoto()
    listacat = admincat.convertirimagenes(listacategorias)
    admin = adminOpciones()
    ltsDepartamentos = admin.getDepartamentos()
    return render_template("principalUsuario.html",categorias=listacat,usuarioactivo=usuario,departamentos =ltsDepartamentos)

@app.route("/Hammer.com/tu-Cuenta/")
def paginaprmodificarcuenta():
    adminC=adminClientes()
    usuario = session['user']
    session['idusuarioactual']= usuario['id']
    session['correoactual']=usuario['correo']
    session['passwordactual']=usuario['contra']
    admin = adminOpciones()
    ltsDepartamentos = admin.getDepartamentos()
    ltsMunicipios = admin.getMunicipios()
    admincat = adminCategorias()
    listacategorias = admincat.getCategoriaConFoto()
    listacat = admincat.convertirimagenes(listacategorias)
    usuarioi = adminC.getUserbyCorreo(usuario['correo'])
    return render_template("modificarUsuario.html",departamentos = ltsDepartamentos,categorias=listacat, municipios = ltsMunicipios, datosusuario=usuarioi)

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
    imagen=request.files['imagen']
    if not imagen.filename =="":
        foto= imagen.read()
    else:
        foto=None
    diccionariouser = {"id": idusuario, "nombre": nombre,"apellido":apellido,"correo":correo,"contra":contrasena,"dui":dui,
                        "telefono":telefono,"genero":genero,"departamento":departamento,"municipio":municipio,"direccion":direccion,"foto":foto}
    adminmodificar=adminClientes()
    success = adminmodificar.updateusuario(diccionariouser)
    diccionariouser['departamento'],diccionariouser['municipio']=adminmodificar.getDepartamentoMunicipioCliente(idusuario)
    if success == True:
        print("datos de vuenta modificados con exito")
        session['msg'] = "Sus datos de cuenta ha sido modificado con exito, vuelva a ingresar"
        session['idusuarioactual']=""
        session['user']
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
    adminC=adminClientes()
    usuarioi = adminC.getUserbyCorreo(usuario['correo'])
    admincat = adminCategorias()
    listacategorias = admincat.getCategoriaConFoto()
    listacat = admincat.convertirimagenes(listacategorias)
    admin = adminOpciones()
    ltsDepartamentos = admin.getDepartamentos()
    return render_template("citasU.html",citaspendientes=citaspendientes,citasnoconfirmadas=citasnoconfirmadas,citaspasadas=citaspasadas,categorias=listacat,usuarioactivo=usuarioi,departamentos =ltsDepartamentos)

@app.route("/Hammer.com/buscarTrabajadores/<form>",methods=['POST'])
def busquedaTrabajadoresCliente(form):
    adminC=adminClientes()
    user = session['user']
    usuario = adminC.getUserbyCorreo(user['correo'])
    admincat = adminCategorias()
    listacategorias = admincat.getCategoriaConFoto()
    listacat = admincat.convertirimagenes(listacategorias)
    admin = adminOpciones()
    ltsDepartamentos = admin.getDepartamentos()
    adminworker = adminTrabajadores()
    adminoptions= adminOpciones()
    if form == "busqueda":
        palabra = request.form.get('palabra')
        departamento=request.form.get('filtroDepartamento')
        categoria=request.form.get('filtroCategoria')
    elif form=="categoria":
        palabra = ""
        departamento="Todos"
        categoria=request.form.get('categoriaButton')

    default=['trabajadores.DUI']
    if not palabra=="":
        getBusqueda = adminworker.fetchAllWorkersByWord(palabra)
    else:
        getBusqueda = adminworker.fetchAllWorkersByWord("",kind=default)
    
    if departamento=="Todos":
        filtroDepartamento=departamento
    else:
        filtroDepartamento=adminoptions.getDepartamentoById(departamento)
    
    if categoria=="Todos":
        filtroCategoria=categoria
    else:
        filtroCategoria=adminoptions.getCategoriaById(categoria)


    listafiltrada = adminworker.filtrarTrabajadoresByDepCat(getBusqueda,filtroDepartamento,filtroCategoria)

    return render_template("busquedaTrabajadores.html",busqueda=listafiltrada,categorias=listacat,usuarioactivo=usuario,departamentos =ltsDepartamentos,departamentobusqueda=filtroDepartamento,categoriabusqueda=filtroCategoria,palabrabusqueda=palabra)

@app.route("/Hammer.com/agendarCita/<funcion>",methods=['POST'])
def agendarCita(funcion):
    adminworkers = adminTrabajadores()
    adminAgendar = adminCitas()
    if funcion == "form":
        correoTrabajador=request.form.get('Trabajador')
        busquedacorreos=["trabajadores.Correo"]
        diccTrabajador = adminworkers.fetchAllWorkersByWord(correoTrabajador,kind=busquedacorreos,aprox=False)
        adminC=adminClientes()
        user = session['user']
        usuario = adminC.getUserbyCorreo(user['correo'])
        admincat = adminCategorias()
        listacategorias = admincat.getCategoriaConFoto()
        listacat = admincat.convertirimagenes(listacategorias)
        admin = adminOpciones()
        ltsDepartamentos = admin.getDepartamentos()
        return render_template("agendarCita.html", trabajadorCita=diccTrabajador,categorias=listacat,usuarioactivo=usuario,departamentos =ltsDepartamentos)
    
    if funcion=="agendar":
        usuario = session['user']

        cita = {
                    "Fecha": request.form.get('fechaPropuesta'),
                    "Hora": request.form.get('horaPropuesta'),
                    "Trabajador":request.form.get('idTrabajador'),
                    "Cliente":usuario['id'],
                    "Finalizada":"False",
                    "DescripcionTrabajo":request.form.get('descripcionTrabajo'),
                    "Confirmacion":"False"
                }
        success = adminAgendar.insertCita(cita)
        return redirect("/Hammer.com/u")

@app.route("/Hammer.com/eliminarCita",methods=['POST'])
def CancelarCita():
    adminCita=adminCitas()
    idCita = request.form.get('idCita')
    delete = adminCita.deleteCita(idCita)
    return redirect("/Hammer.com/citas")


@app.route("/Hammer.com/informacionEmpresa")
def quienesSomos():
    adminC=adminClientes()
    user = session['user']
    usuario = adminC.getUserbyCorreo(user['correo'])
    admincat = adminCategorias()
    listacategorias = admincat.getCategoriaConFoto()
    listacat = admincat.convertirimagenes(listacategorias)
    admin = adminOpciones()
    ltsDepartamentos = admin.getDepartamentos()
    return render_template("informacionEmpresa.html",categorias=listacat,usuarioactivo=usuario,departamentos =ltsDepartamentos)

@app.route("/Hammer.com/salirU")
def cerrarSesion():
    return redirect("/")
# Errors

@app.route("/Hammer.com/notAccess")
def notAcces():
    adminA = adminAdministrador()
    images = adminA.getImages()
    return render_template("notAccess.html", imagenes = images)

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

#Worker UI

@app.route("/Hammer.com/worker")    
def workerIndex():
    adminT=adminTrabajadores()
    worker = session['user']
    trabajador= adminT.getWorkerbyCorreo(worker['correo'])
    idTrabajador = worker['id']
    proximaCita = adminT.proximaCita(idTrabajador)
    citas = adminT.citasPorMes(idTrabajador)
    citasMes = adminT.citasToArray(citas)
    meses = citasMes[0]
    cantidades = citasMes[1]
    print(citasMes[0], citasMes[1])
    return render_template("trabajadoresHome.html", worker= trabajador, proximaCita=proximaCita, citasMes=citasMes)

@app.route("/Hammer.com/servicioActivo")    
def workerServicioActivo():
    adminT=adminTrabajadores()
    worker = session['user']
    idWorker= worker['id']
    trabajador= adminT.getWorkerbyCorreo(worker['correo'])
    servicio= adminT.ServicioActivo(idWorker)
    return render_template("servicioActivo.html", worker= trabajador, servicio=servicio)

@app.route("/Hammer.com/configuracion")    
def workerConfiguracion():
    adminT=adminTrabajadores()
    worker = session['user']
    idWorker= worker['id']
    trabajador= adminT.getWorkerbyCorreo(worker['correo'])
    servicio= adminT.ServicioActivo(idWorker)
    return render_template("workerConfiguracion.html", worker= trabajador)

@app.route("/Hammer.com/updatePerfil",methods=['POST'])    
def workerUpdatePerfil():
    adminT=adminTrabajadores()
    worker = session['user']
    idWorker= worker['id']
    trabajador= adminT.getWorkerbyCorreo(worker['correo'])

    print(type(idWorker))
    nombre= request.form.get('nombre')
    apellido= request.form.get('apellido')
    telefono= request.form.get('telefono')
    direccion= request.form.get('direccion')
    correo= request.form.get('correo')
    descripcion= request.form.get('descripcion')
    genero= request.form.get('genero')


    update= adminT.updateWorker(idWorker,nombre,apellido,telefono,direccion,correo,descripcion,genero)

    return redirect("/Hammer.com/perfil")

@app.route("/generarMembership", methods=['POST'])
def createMembership():
    idT = request.form.get('idT')
    adminA = adminTrabajadores()
    adminA.generarMembresiaEnTrabajador(idT)
    return redirect('/Hammer.com/worker')
    

@app.route("/Hammer.com/cambiarFoto", methods=['POST'])    
def workerCambiarFoto():
    adminT=adminTrabajadores()
    worker = session['user']
    idWorker= worker['id']
    image = request.files['foto']
    foto = image.read()
    cambiarFoto= adminT.cambiarFoto(idWorker, foto)
    trabajador2=adminT.getWorkerbyCorreo(worker['correo'])
    return redirect("/Hammer.com/configuracion")

@app.route("/Hammer.com/perfil")    
def workerPerfil():
    adminT=adminTrabajadores()
    worker = session['user']
    trabajador= adminT.getWorkerbyCorreo(worker['correo'])
    return render_template("workerPerfil.html",worker=trabajador)


@app.route("/Hammer.com/workerHistorial")
def workerHistorial():
    adminT=adminTrabajadores()
    worker = session['user']
    trabajador= adminT.getWorkerbyCorreo(worker['correo'])
    idTrabajador = worker['id']
    historial = adminT.HistorialTrabajadores(idTrabajador)
    return render_template("trabajadoresHistorial.html", historial=historial, worker=trabajador)

@app.route('/Hammer.com/workePpagos')
def workerPagos():
    adminT=adminTrabajadores()
    worker = session['user']
    trabajador= adminT.getWorkerbyCorreo(worker['correo'])
    idTrabajador = worker['id']
    return render_template("pagosTrabajadores.html", worker = trabajador )

@app.route('anadirTarjeta', methods=['POST'])
def anadirTarjeta():
    pass

@app.route("/Hammer.com/citasWorker")
def workerCitas():
    adminT=adminTrabajadores()
    worker = session['user']
    trabajador= adminT.getWorkerbyCorreo(worker['correo'])
    idTrabajador = worker['id']
    citasConfirmadas = adminT.citasConfirmadas(idTrabajador)
    citasNoConfirmadas = adminT.citasNoConfirmadas(idTrabajador)
    idUpdate="0"
    return render_template("trabajadoresCitas.html", worker=trabajador, confirmadas=citasConfirmadas, noConfirmadas=citasNoConfirmadas,idUpdate=idUpdate)

@app.route('/Hammer.com/confirmacion/<idCita>')    
def confirmar(idCita=None):    
    adminT=adminTrabajadores()
    finalizar= adminT.confirmarCita(idCita)
    return redirect("/Hammer.com/citasWorker")

@app.route('/Hammer.com/modificaCita/<idCita>')    
def modificarCitaForm(idCita):    
    adminT=adminTrabajadores()
    worker = session['user']
    trabajador= adminT.getWorkerbyCorreo(worker['correo'])
    idTrabajador = worker['id']
    citasConfirmadas = adminT.citasConfirmadas(idTrabajador)
    citasNoConfirmadas = adminT.citasNoConfirmadas(idTrabajador)
    idUpdate=int(idCita)
    return render_template("trabajadoresCitas.html", worker=trabajador, confirmadas=citasConfirmadas, noConfirmadas=citasNoConfirmadas,idUpdateCita=idUpdate)

@app.route("/Hammer.com/servlet/updateCita", methods=['POST'])
def modificarCita(): 
    adminCita= adminCitas()
    idUpdate = int(request.form.get('Updateid'))
    FechaUpdate = request.form.get('UpdateFecha')
    HoraUpdate=request.form.get('UpdateHora')
    citaActual= adminCita.getCitasById(idUpdate)
    dataUpdate={
                    "idCitas": idUpdate,
                    "Fecha": FechaUpdate,
                    "Hora": HoraUpdate,
                    "Trabajador": citaActual['Trabajador'],
                    "Cliente": citaActual['Cliente'],
                    "Finalizada":"False",
                    "DescripcionTrabajo": citaActual['Descripciontrabajo'],
                    "Confirmacion":"True"
                }
    successUpdate=adminCita.updateCitas(dataUpdate)
    return redirect("/Hammer.com/citasWorker")

@app.route('/Hammer.com/declinacion/<idCita>')    
def declinar(idCita=None):    
    adminT=adminTrabajadores()
    finalizar= adminT.declinarCita(idCita)
    return redirect("/Hammer.com/citasWorker")

@app.route('/Hammer.com/finalizarServicio/<idCliente>')    
def finalizarServicio(idCliente=None):    
    adminT=adminTrabajadores()
    idCita= idCliente
    finalizar= adminT.finalizarServicio(idCita)
    return redirect("/Hammer.com/servicioActivo")





if __name__=='__main__':
    app.run(debug=True)
