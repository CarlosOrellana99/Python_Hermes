from database.Logics import adminAdministrador

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

    def getWorkerbyCorreo(self, correo, picture = True):

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
            lista = self.convertTuplaToDicc(data[0], picture)
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
            like = f"like  '{word.upper()}%'"
        else:
            like = f"= '{word.upper()}'"
        final = []

        if len(kind) == 0:
            lista = ['trabajadores.DUI', 'trabajadores.Nombre', 'trabajadores.Apellido', 'trabajadores.Celular', 'trabajadores.Direccion', 'trabajadores.Descripcion', 'membresias.Membresia', 'municipios.nombre', 'departamentos.nombre', 'categoria.nombre']
        else:
            lista = kind

        select = "trabajadores.idTrabajadores, trabajadores.DUI, trabajadores.Nombre, trabajadores.Apellido, trabajadores.Celular, trabajadores.Direccion, trabajadores.Correo, trabajadores.Contrasena, trabajadores.Descripcion, trabajadores.Genero, trabajadores.Foto, trabajadores.Aceptado,  membresias.Membresia, departamentos.nombre as depa, municipios.nombre as mun, trabajadores.trabajos, membresias.vigencia"
        # Búsquedas generales
        for x in lista:

            sql = f"""  SELECT distinct {select}
                    FROM categoriatrabajadores 
                    right join trabajadores on trabajadores.idTrabajadores = categoriatrabajadores.Trabajador
                    left join categoria on categoria.idCategoria = categoriatrabajadores.Categoria
                    inner join hermes.departamentos on departamentos.idDepartamento = trabajadores.Departamento
                    inner join hermes.municipios on municipios.idMunicipio = trabajadores.Municipio
                    inner join hermes.membresias on membresias.idMembresias = trabajadores.Membresia
                    where {x} {like}
                    order by {order} {mode} limit {limit};"""
            # print(sql)
            
            data = database.executeQuery(sql)
            temporal = self.convertDataToList(data)
            final += temporal
            
        return final
    
    def convertDataToList(self, data):
        """De los datos devueltos de un select de trabajadores, devuelve una lista de diccionarios"""
        lista = []
        value = None
        numero = 0
        if len(data) > 0:
            for x in data:
                value = self.convertTuplaToDicc(x, numero = numero)
                lista.append(value)
                numero += 1
        return lista

    def convertTuplaToDicc(self, tupla, picture = True, numero = 0):
        """Converts a tuple to a dictionary"""
        if picture:
            foto = b64encode(tupla[10]).decode("utf-8")
        else:
            foto = None
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
                "foto":  foto,
                "aceptado": tupla[11],
                "membresia": tupla[12],
                "vigencia":tupla[16],
                "departamento": tupla[13],
                "municipio": tupla[14],
                "trabajos": tupla[15],
                "Categoría": self.getCategoriasById(tupla[0]),
                "numero": numero
            }
        return lista

    def getCategoriasById(self, idTrabajador):
        """Retorna la lista de categorias a las que pertenece el trabajador con el id especificado"""
        sql = f"""SELECT categoria.nombre FROM hermes.categoriatrabajadores
            left join categoria on categoria.idCategoria = categoriatrabajadores.categoria
            where categoriatrabajadores.Trabajador = '{idTrabajador}';"""
        
        data = self.database.executeQuery(sql)
        lista = []
        texto = ""
        for x in data:
            lista.append(x[0])
            texto += str(x[0])
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
    def filtrarTrabajadoresByDepCat(self,lista,departamento,categoria):
        """Filtra una lista de trabajadores por su departamento y categoria"""
        listaFiltrada =[]
        for y in lista:
            if y["vigencia"]==1 and y["aceptado"]==1:
                if departamento=="Todos":
                    if categoria=="Todos":
                        listaFiltrada.append(y)
                    else:
                        for x in y["Categoría"]:
                            if x == categoria:
                                listaFiltrada.append(y)
                elif y["departamento"]==departamento:
                    if categoria=="Todos":
                        listaFiltrada.append(y)
                    else:
                        for x in y["Categoría"]:
                            if x == categoria:
                                listaFiltrada.append(y)
        return listaFiltrada 

    def HistorialTrabajadores(self, idTrabajador):
        database = self.database
        sql = f"""Select * from citas where Trabajador = '{idTrabajador}' """ 
        data = database.executeQuery(sql)
        return data

    def proximaCita(self, idTrabajador):
        database = self.database
        sql = f"""select * from citas
        where Finalizada = 'False' and Confirmacion = 'True' and Trabajador = '{idTrabajador}'
        order by fecha 
        limit 1"""
        data = database.executeQuery(sql)
        return data

    def solicitudCitas(self, idTrabajador):
        database = self.database
        sql = f"""select * from citas
        where Finalizada = 'False' and Confirmacion = 'False' and Trabajador = '{idTrabajador}'
        order by fecha """
        data = database.executeQuery(sql)
        return data

    #Se vera un grafico con las citas de los ultimos 5 meses para cada trabajador para ver la evolucion
    def citasPorMes(self, idTrabajador):
        database = self.database
        sql = f"""select count(*) from citas
        where Trabajador = '{idTrabajador}'
        group by month(Fecha)
        limit 5"""  
        data = database.executeQuery(sql)
        return data

    def citasMesActual(self, idTrabajador):
        database = self.database
        sql = f"""select count(*) from citas
        where Trabajador = '{idTrabajador}' and month(Fecha) = month(now())
        limit 1"""  
        data = database.executeQuery(sql)
        return data