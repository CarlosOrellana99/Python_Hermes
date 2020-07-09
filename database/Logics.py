from database.DatabaseZ import DatabaseZ

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

class adminTrabajadores(DatabaseZ):
    """"Aministración de los trabajadores en la base de datos
    ----
    """

    def __init__(self):
        self.database = DatabaseZ()

    def insert(self, dui, nombre, apellido, celular, direccion, correo, contrasena, departamento, municipio, genero, aceptado, membresia, categoria, foto = None):
        """ Inserta los componentes de un cliente en la base de datos
        -------
        Devuelve True si se ejecutó con éxito y false si no se hicieron cambios"""
        success = False
        if foto == '':
            sql = """INSERT INTO `hermes`.`trabajadores` (`DUI`, `Nombre`, `Apellido`, `Celular`, `Direccion`, `Correo`, `Contrasena`, `Descripcion`, `Departamento`, `Municipio`, `Genero`, `Aceptado`, `Membresia`, `Categoria`) 
            VALUES ('%s, '%s, '%s, '%s, '%s, '%s, '%s, '%s, '%s, '%s, '%s, '%s, '%s, '%s);"""
            val = (dui, nombre, apellido, celular, direccion, correo, contrasena, departamento, municipio, genero, aceptado, membresia, categoria)
        else:
            sql = """INSERT INTO `hermes`.`trabajadores` (`DUI`, `Nombre`, `Apellido`, `Celular`, `Direccion`, `Correo`, `Contrasena`, `Descripcion`, `Departamento`, `Municipio`, `Genero`, `Aceptado`, `Membresia`, `Categoria`, `Foto`) 
            VALUES ('%s, '%s, '%s, '%s, '%s, '%s, '%s, '%s, '%s, '%s, '%s, '%s, '%s, '%s, '%s);"""
            val = (dui, nombre, apellido, celular, direccion, correo, contrasena, departamento, municipio, genero, aceptado, membresia, categoria, foto)

        database = self.database
        success = database.executeMany(sql, val)
        return success




