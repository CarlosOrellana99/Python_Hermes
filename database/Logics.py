from database.DatabaseZ import DatabaseZ

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
        encontrado, contraseña_coincide, diccionario_user, tipo
        """
        
        encontrado = False
        permitido = False
        tipo = None
        lista = self.adminClientes.getUserbyCorreo(correo)
        if len(lista) == 0:
            lista = self.adminTrabajadores.getWorkerbyCorreo(correo)
            if len(lista) == 0:
                    lista = getAdminByCorreo(correo)
                    if len(lista) == 0:
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

        conclusion = {"encontrado": encontrado, "permitido": permitido, "user": lista, "tipo": tipo}
        return conclusion

    def getAdminByCorreo(self, correo):
        """Debuele una lista con los datos del usuario con ese correo"""
        database = self.database
        sql = f"SELECT * FROM hermes.administradoes where administradoes.Correo = '{correo}' limit 1;"
        data = database.executeQuery(sql)
        lista = {}
        lista = self.convertTuplaToList(data[0])
        return lista
    
    def checkContra(self, contra, lista):
        valor = contra == lista["contra"]
        return valor

    def convertTuplaToList(self, tupla):
        if tupla is None:
            lista = {
                "id": tupla[0],
                "nombre": tupla[1],
                "apellido": tupla[2],
                "correo": tupla[3],
                "contra": tupla[4],
                "foto": tupla[5]
            }

class adminClientes(DatabaseZ):
    """Aministración de los clientes en la base de datos
    ----
    """

    def __init__(self):
        self.database = DatabaseZ()

    def insert(self, dui, nombre, apellido, celular, direccion, correo, contrasena, departamento, municipio, foto = None):
        """ Inserta los componentes de un cliente en la base de datos
        -------
        Devuelve True si se ejecutó con éxito y false si no se hicieron cambios"""
        success = False
        if foto == '':
            sql = """INSERT INTO hermes.clientes 
            (`DUI`, `Nombre`, `Apellido`, `Celular`, `Direccion`, `Correo`, `Contrasena`, `Departamento`, `Municipio`) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);"""
            val = (dui, nombre, apellido, celular, direccion, correo, contrasena, departamento, municipio)
        else: 
            sql = """INSERT INTO hermes.clientes 
            (`DUI`, `Nombre`, `Apellido`, `Celular`, `Direccion`, `Correo`, `Contrasena`, `Departamento`, `Municipio`, `Foto`) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"""

            val = (dui, nombre, apellido, celular, direccion, correo, contrasena, departamento, municipio, foto)

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
        lista = self.convertTuplaToList(data[0])
        return lista

    def convertTuplaToList(self, tupla):
        if tupla is not None:
            lista = {
                "id" : tupla[0],
                "dui" : tupla[1],
                "nombre" : tupla[2],
                "apellido" : tupla[3],
                "telefono" : tupla[4],
                "direccion" : tupla[5],
                "correo" : tupla[6],
                "contra": tupla[7],
                "foto" : tupla[8],
                "departamento" : tupla[11],
                "municipio" : tupla[12]
            }
        return lista

class adminTrabajadores(DatabaseZ):
    """"Aministración de los trabajadores en la base de datos
    ----
    """

    def __init__(self):
        self.database = DatabaseZ()

    def insert(self, dui, nombre, apellido, celular, direccion, correo, contrasena, descripcion, departamento, municipio, genero, aceptado, membresia, foto = None):
        """ Inserta los componentes de un cliente en la base de datos
        -------
        Devuelve True si se ejecutó con éxito y false si no se hicieron cambios"""
        success = False
        if foto == '':
            sql = """INSERT INTO `hermes`.`trabajadores` 
            (`DUI`, `Nombre`, `Apellido`, `Celular`, `Direccion`, `Correo`, `Contrasena`, `Descripcion`, `Departamento`, `Municipio`, `Genero`, `Aceptado`, `Membresia`) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"""
            val = (dui, nombre, apellido, celular, direccion, correo, contrasena, descripcion, departamento, municipio, genero, aceptado, membresia)
        else:
            sql = """INSERT INTO `hermes`.`trabajadores` 
            (`DUI`, `Nombre`, `Apellido`, `Celular`, `Direccion`, `Correo`, `Contrasena`, `Descripcion`, `Departamento`, `Municipio`, `Genero`, `Aceptado`, `Membresia`, `Foto`) 
            VALUES (%s, s, %s, %s, %s, s, %s, %s, %s, %s, %s, %s, %s, %s );"""
            val = (dui, nombre, apellido, celular, direccion, correo, contrasena, descripcion, departamento, municipio, genero, aceptado, membresia, foto)

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
        lista = self.convertTuplaToList(data)
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
                "descripcion": tupla[8], #
                "genero": tupla[11],
                "foto": tupla[12],
                "aceptado": tupla[13],
                "membresia": tupla[14],
                "departamento": tupla[15],
                "municipio": tupla[16],
            }
        return lista

class adminDepAndMun(DatabaseZ):
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

    def listToDicc(self, data):
        """Convierte la lista de tuplas a una lista de diccionarios"""
        lista = []
        for x in data:
            dicc = {
                "id": x[0],
                "nombre": x[1]
            }
            lista.append(dicc)
        return lista


        

