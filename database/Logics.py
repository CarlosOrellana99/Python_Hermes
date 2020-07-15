from database.DatabaseZ import DatabaseZ
from base64 import b64encode
from datetime import date

class adminAdministrador(DatabaseZ):
    """Administrador de la cuenta Administrador
    ----
    Tiene acceso a todas las cuentas y al la de Administrador
    """

    def __init__(self):
        self.database = DatabaseZ()
        self.adminClientes = adminClientes()
        self.adminTrabajadores = adminTrabajadores()

    def verify(self, correo, contra):
        """Verifica si el par Correo-Contraseña pertenece a algún usuario de cualquier clase
        ----
        Devuelve un diccionario que que contiene :
        {"encontrado": encontrado, "permitido": contraseña_coincide, "user": diccionario_datos_usuario, "tipo": string_tipo_usuario}
        """

        encontrado = False
        permitido = False
        tipo = None
        lista = self.adminClientes.getUserbyCorreo(correo)
        if len(lista) == 0:
            lista = self.adminTrabajadores.getWorkerbyCorreo(correo)
            if len(lista) == 0:
                lista = self.getAdminByCorreo(correo)
                if not len(lista) == 0:
                    encontrado = True
                    tipo = "admin"
            else:
                encontrado = True
                tipo = "worker"

        else:
            encontrado = True
            tipo = "user"

        if encontrado:
            permitido = self.checkContra(contra, lista)

        encontrado = len(lista) > 0
        permitido = encontrado and permitido

        conclusion = {
            "encontrado": encontrado,
            "permitido": permitido,
            "user": lista,
            "tipo": tipo,
        }
        return conclusion

    def getAdminByCorreo(self, correo):
        """Debuele una lista con los datos del usuario con ese correo"""
        database = self.database
        sql = f"SELECT * FROM hermes.administradoes where administradoes.Correo = '{correo}' limit 1;"
        data = database.executeQuery(sql)
        lista = {}
        if len(data) > 0:
            lista = self.convertTuplaToList(data[0])
        return lista

    def checkContra(self, contra, lista):
        valor = contra == lista["contra"]
        return valor

    def convertTuplaToList(self, tupla):
        lista = {}
        if tupla is not None:
            lista = {
                "id": tupla[0],
                "nombre": tupla[1],
                "apellido": tupla[2],
                "correo": tupla[3],
                "contra": tupla[4],
                "foto": tupla[5],
            }
        return lista

    def searchWorker(self, word, limit = "20"):
        """
        Devuelve una lista con todos los trabajadores relacionados a una palabra
        ---
        La palabra se bueca en el dui, el nomre, el apellido, el celular, la dirección, el correo, la descripción o la categoría
        "limit" ajusta el número de trabajadores devueltos
        """
        admin = self.adminTrabajadores
        lista = admin.fetchAllWorkersByWord(word, limit)

    def revocarLicenciaDeudores(self):
        sql = "update hermes.membresias set membresias.Vigencia = 0 where datediff(now(), UltimoPago) > 31;"
        exito = self.database.executeNonQueryBool(sql)
        return exito
    
class adminClientes(DatabaseZ):
    """Aministración de los clientes en la base de datos
    ----
    """

    def __init__(self):
        self.database = DatabaseZ()

    def insert(self, dui, nombre, apellido, celular, direccion, correo, contrasena, departamento, municipio, genero, foto=None ):
        """ Inserta los componentes de un cliente en la base de datos
        -------
        Devuelve True si se ejecutó con éxito y false si no se hicieron cambios"""
        success = False
        if  foto == "":
            sql = """INSERT INTO hermes.clientes 
            (`DUI`, `Nombre`, `Apellido`, `Celular`, `Direccion`, `Correo`, `Contrasena`, `Departamento`, `Municipio`, `Genero` )  
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"""
            val = (dui, nombre, apellido, celular, direccion, correo, contrasena, departamento, municipio, genero)
        else:
            sql = """INSERT INTO hermes.clientes 
            (`DUI`, `Nombre`, `Apellido`, `Celular`, `Direccion`, `Correo`, `Contrasena`, `Departamento`, `Municipio`, `Foto`, `Genero` ) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"""

            val = ( dui, nombre, apellido, celular, direccion, correo, contrasena, departamento, municipio, foto, genero)

        database = self.database
        success = database.executeMany(sql, val)
        return success

    def getUserbyCorreo(self, correo):
        """Debuele una lista con los datos del usuario con ese correo"""
        database = self.database
        sql = f"""SELECT clientes.*, departamentos.Nombre as dep, municipios.Nombre as mun FROM hermes.clientes 
                    inner join hermes.departamentos on departamentos.idDepartamento = clientes.Departamento
                    inner join hermes.municipios on municipios.idMunicipio = clientes.Municipio
                    where clientes.Correo = '{correo}' limit 1;"""
        data = database.executeQuery(sql)
        lista = {}
        if len(data) > 0:
            lista = self.convertTuplaToList(data[0])
        return lista

    def convertTuplaToList(self, tupla):
        if tupla is not None:
            lista = {
                "id": tupla[0],
                "dui": tupla[1],
                "nombre": tupla[2],
                "apellido": tupla[3],
                "telefono": tupla[4],
                "direccion": tupla[5],
                "correo": tupla[6],
                "contra": tupla[7],
                "foto": tupla[8],
                "departamento": tupla[11],
                "municipio": tupla[12],
            }
        return lista

class adminTrabajadores(DatabaseZ):
    """
    Aministración de los trabajadores en la base de datos
    ----
    """

    def __init__(self):
        self.database = DatabaseZ()

    def insert( self, dui, nombre, apellido, celular, direccion, correo, contrasena, descripcion, departamento, municipio, genero, aceptado, membresia="AAAA-0000-0000", foto=None,):
        """ Inserta los componentes de un cliente en la base de datos
        -------
        Devuelve True si se ejecutó con éxito y false si no se hicieron cambios"""
        success = False
        fecha = date.today()
        fechaF = fecha.strftime("%d-%m-%Y")
        if foto == "":
            sql = """INSERT INTO `hermes`.`trabajadores` 
            (`DUI`, `Nombre`, `Apellido`, `Celular`, `Direccion`, `Correo`, `Contrasena`, `Descripcion`, `Departamento`, `Municipio`, `Genero`, `Aceptado`, `Membresia`, `fechaDeEntrada`) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"""
            val = ( dui, nombre, apellido, celular, direccion, correo, contrasena, descripcion, departamento, municipio, genero, aceptado, membresia, fechaF)
        else:
            sql = """INSERT INTO `hermes`.`trabajadores` 
            (`DUI`, `Nombre`, `Apellido`, `Celular`, `Direccion`, `Correo`, `Contrasena`, `Descripcion`, `Departamento`, `Municipio`, `Genero`, `Aceptado`, `Membresia`, `Foto`, `fechaDeEntrada`) 
            VALUES (%s, s, %s, %s, %s, s, %s, %s, %s, %s, %s, %s, %s, %s );"""
            val = (
                dui,
                nombre,
                apellido,
                celular,
                direccion,
                correo,
                contrasena,
                descripcion,
                departamento,
                municipio,
                genero,
                aceptado,
                membresia,
                foto,
                fechaF
            )

        database = self.database
        success = database.executeMany(sql, val)
        return success

    def getWorkerbyCorreo(self, correo):

        """Debuele una lista con los datos del usuario con ese correo"""
        database = self.database
        sql = f"""
                SELECT trabajadores.*, departamentos.Nombre as dep, municipios.Nombre as mun FROM hermes.trabajadores 
                inner join hermes.departamentos on departamentos.idDepartamento = trabajadores.Departamento
                inner join hermes.municipios on municipios.idMunicipio = trabajadores.Municipio
                where trabajadores.Correo = '{correo}' limit 1;"""
        data = database.executeQuery(sql)
        lista = {}
        if len(data) > 0:
            lista = self.convertTuplaToDicc(data[0])
        return lista

    def fetchAllWorkersByWord(self, word, limit = str(20), kind = [], order = "fechaDeEntrada", mode = "desc", aprox=True, cat = True):

        """"Lista de {limit} trabajadores con características que parescan a {word}
        ----
        {Kind} es la lista de lugares en que se buscará 
        Kind puede ser: ['trabajadores.DUI', 'trabajadores.Nombre', 'trabajadores.Apellido', 'trabajadores.Celular', 'trabajadores.Direccion', 'trabajadores.Descripcion', 'membresias.Membresia', 'municipios.nombre', 'departamentos.nombre']
        Si desea que la busqueda no incluya a categoria escriba cat = False en los argumentos
        Para buscar a un trabajador por su id escriba 'trabajadores.idTrabajadores' en kind
        La búsqueda se ordena con la fecha de entrada descendente. Para ajustar, el campo {order} es el campo de ordenamiento y {mode} es el modo de ordenamiento
        Si desea una búsqueda exacta ingrese False en aprox
        """
        database = self.database 
        if aprox:
            like = f"like  '%{word.upper()}%'"
        else:
            like = f"= '{word.upper()}'"
        final = []

        if len(kind) == 0:
            lista = ['trabajadores.DUI', 'trabajadores.Nombre', 'trabajadores.Apellido', 'trabajadores.Celular', 'trabajadores.Direccion', 'trabajadores.Descripcion', 'membresias.Membresia', 'municipios.nombre', 'departamentos.nombre', 'categoria.nombre']
        else:
            lista = kind

        select = "trabajadores.idTrabajadores, trabajadores.DUI, trabajadores.Nombre, trabajadores.Apellido, trabajadores.Celular, trabajadores.Direccion, trabajadores.Correo, trabajadores.Contrasena, trabajadores.Descripcion, trabajadores.Genero, trabajadores.Foto, trabajadores.Aceptado,  membresias.Membresia, departamentos.nombre as depa, municipios.nombre as mun, trabajadores.trabajos"
        # Búsquedas generales
        for x in lista:

            sql = f"""  SELECT distinct {select}
                    FROM categorias 
                    right join trabajadores on trabajadores.idTrabajadores = categorias.Trabajador
                    left join categoria on categoria.idCategoria = categorias.Categoria
                    inner join hermes.departamentos on departamentos.idDepartamento = trabajadores.Departamento
                    inner join hermes.municipios on municipios.idMunicipio = trabajadores.Municipio
                    inner join hermes.membresias on membresias.idMembresias = trabajadores.Membresia
                    where {x} {like}
                    order by {order} {mode} limit {limit};"""

            
            data = database.executeQuery(sql)
            temporal = self.convertDataToList(data)
            final += temporal
            
        return final
    
    def convertDataToList(self, data):
        """De los datos devueltos de un select de trabajadores, devuelve una lista de diccionarios"""
        lista = []
        value = None
        if len(data) > 0:
            for x in data:
                value = self.convertTuplaToDicc(x)
                lista.append(value)
        return lista

    def convertTuplaToDicc(self, tupla):
        """Converts a tuple to a dictionary"""
        if tupla is not None:
            lista = {
                "id": tupla[0],
                "dui": tupla[1],
                "nombre": tupla[2],
                "apellido": tupla[3],
                "telefono": tupla[4],
                "direccion": tupla[5],
                "correo": tupla[6],
                "contra": tupla[7],
                "descripcion": tupla[8],  
                "genero": tupla[9],
                "foto":  b64encode(tupla[10]).decode("utf-8"),
                "aceptado": tupla[11],
                "membresia": tupla[12],
                "departamento": tupla[13],
                "municipio": tupla[14],
                "trabajos": tupla[15],
                "Categoría": self.getCategoriasById(tupla[0])
            }
        return lista

    def getCategoriasById(self, idTrabajador):
        """Retorna la lista de categorias a las que pertenece el trabajador con el id especificado"""
        sql = f"""SELECT categoria.nombre FROM hermes.categorias
            left join categoria on categoria.idCategoria = categorias.categoria
            where categorias.Trabajador = '{idTrabajador}';"""
        
        data = self.database.executeQuery(sql)
        lista = []
        for x in data:
            lista.append(x[0])
        return lista
    
    def generarMembresiaEnTrabajador(self, idW):
        trabajador = self.fetchAllWorkersByWord(str(idW), limit='1', kind= ['trabajadores.idTrabajadores'], order='trabajadores.idTrabajadores', aprox=False, cat=False)
        membActual, exito = trabajador[0]['membresia'], False
        last = self.getLastMembresia()
        if membActual == "AAAA-0000-0000": # Esto significa que aún no se le ha asignado ninguna membresía
            new = self.createMembresia(last)
            sql = f"""  UPDATE hermes.membresias inner join hermes.trabajadores on trabajadores.Membresia = membresias.idMembresias
                        set membresias.Membresia = '{new}'
                        where trabajadores.idTrabajadores = '{idW}';"""
            exito = self.database.executeNonQueryBool(sql)
        return exito

    def createMembresia(self, last):
        # last = self.getLastMembresia()
        numeros_ok = ['1', '2', '3', '4', '5', '6', '7', '8', '0']
        abecedario = {"A": "B", "B": "C", "C": "D", "D": "E", "E": "F", "F": "A"}
        letras = ['A', 'B', 'C', 'D', 'E', 'F']
        nueva, value, added, num="", "", False, 0
        for x in reversed(last):
            print(x)
            if x in numeros_ok:
                value = int(x)
                value += 1
                added = True
            elif x == '9':
                value = "0"
            elif x in letras:
                value = abecedario[x]
                num += 1
                added = not (value == "A") or (num > 3)
            else:
                value = '-'
            nueva += str(value)
            if added:
                break
        final = last[0:(14-len(nueva))] + nueva[::-1]
        return final
        
    def getLastMembresia(self):
        """Devuelve el valor de la última membresía ingresada"""
        database = self.database
        sql = """   SELECT membresias.Membresia FROM hermes.trabajadores 
                    inner join hermes.membresias on membresias.idMembresias = trabajadores.Membresia
                    order by membresias.Membresia desc limit 1;"""
        data = database.executeQuery(sql)
        membresia = data[0][0]
        return membresia

    def fragmentarMembersia(self, membresia):
        """Devuelve un diccionario con lo siguiente:
            {'membresia': '00-0000-0000', 'primeraParte': '00', 'segundaParte': '0000', 'terceraParte': '0000'}
        """
        dicc = {
        "membresia": membresia,
        "primeraParte": membresia[0:2],
        "segundaParte": membresia[3:7],
        "terceraParte": membresia[8:12] 
        }
        return dicc

class adminCategorias(DatabaseZ):
    def __init__(self):
        self.database = DatabaseZ()
        
    def getCategoriaConFoto(self):
        """Retorna una lista con los datos completos de las categorias (id,nombre,foto)"""
        database = self.database
        sql = "SELECT * FROM hermes.categoria;"
        data = database.executeQuery(sql)
        return data

    def convertirimagenes(self,listacategoria):
        """Retorna una lista con imagenes transformadas de las categorias (id,nombre,foto)"""
        listafinalcategorias=[]
        dicccategoriaactual=[]
        for x in listacategoria:
            image = b64encode(x[2]).decode("utf-8")
            dicccategoriaactual={
                "id":x[0], 
                "nombre":x[1],
                "imagen":image}
            listafinalcategorias.append(dicccategoriaactual)
        return listafinalcategorias
        
class adminOpciones(DatabaseZ):
    def __init__(self):
        self.database = DatabaseZ()

    def getMunicipios(self):
        """Retorna una lista de diccionarios con los datos de los municipios (id, nombre)"""
        database = self.database
        sql = "SELECT idMunicipio, Nombre FROM hermes.municipios;"
        data = database.executeQuery(sql)
        lista = self.listToDicc(data)
        return lista

    def getDepartamentos(self):
        """Retorna una lista de diccionarios con los datos de los municipios (id, nombre)"""
        database = self.database
        sql = "SELECT idDepartamento, Nombre FROM hermes.departamentos;"
        data = database.executeQuery(sql)
        lista = self.listToDicc(data)
        return lista

    def getCategorias(self):
        """Retorna una lista de diccionarios con los datos de las categorias (id, nombre)"""
        database = self.database
        sql = "SELECT idCategoria,Nombre FROM hermes.categoria;"
        data = database.executeQuery(sql)
        lista = self.listToDicc(data)
        return lista

    def listToDicc(self, data):
        """Convierte la lista de tuplas a una lista de diccionarios
        -----
        Advertencia: Solo aplicable a tuplas que contengan id, nombre
        """
        lista = []
        for x in data:
            dicc = {"id": x[0], "nombre": x[1]}
            lista.append(dicc)
        return lista

class adminCuenta():
    def __init__(self):
        self.database = DatabaseZ()

    def updateusuario(self,datanueva):
        """ actualiza los campos de la cuenta de un usuario recibiendo un diccionario con los nuevos campos y el id"""
        database = self.database
        sql = """UPDATE hermes.clientes SET
            DUI=%s , Nombre=%s, Apellido=%s, Celular=%s, Direccion=%s, Correo=%s ,
            Contrasena=%s , Departamento=%s , Municipio=%s, Genero=%s WHERE idClientes=%s;"""
        val = (
            datanueva['dui'],
             datanueva['nombre'],
             datanueva['apellido'],
            datanueva['telefono'],
            datanueva['direccion'],
            datanueva['correo'],
            datanueva['contra'],
            datanueva['departamento'],
            datanueva['municipio'],
            datanueva['genero'],
            datanueva['id']
            )
        success = database.executeMany(sql,val)
        return success
