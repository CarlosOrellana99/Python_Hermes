import sys
sys.path.append('d:\\78GDO\\Documents\\ProyectoProgramación\\Python_Hermes')
from database.Logics import adminClientes, adminAdministrador, adminTrabajadores, adminOpciones
from datetime import date
# Escriba el número de test que desea correr
test = '9'
if test == '1':
    admin = adminClientes()
    data = admin.getUserbyCorreo("a")
    print(data)
    data = admin.getUserbyCorreo("moris32345@hotmail.es")
    print(data)
    tupla = data[0]
    print(tupla)
    print(tupla[0])
    list = admin.convertTuplaToList(tupla)
    print(list)

elif test == '2':
    admin = adminTrabajadores()
    data = admin.getWorkerbyCorreo("a")
    print(data)
    data = admin.getWorkerbyCorreo("moris32345@hotmail.es")
    tupla = data[0]
    print(tupla)
    print(admin.convertTuplaToList(tupla))

elif test == '3':
    admin = adminAdministrador()
    data = admin.getAdminByCorreo("moris32345@hotmail.es")
    print(data)

elif test == '4':
    admin = adminAdministrador()
    lista = admin.verify("moris32345@hotmail.es", "contrasena")
    print(lista)
    lista = admin.verify("moris32345@hotmail.es","moris32345")
    print(lista)

elif test == '5':
    admin = adminOpciones()
    departamentos = admin.getDepartamentos()
    print(departamentos)
    print("-"*10)
    municipios = admin.getMunicipios()
    print(municipios)
    categorias = admin.getCategorias()
    print(categorias)

elif test == '6':
    admin = adminAdministrador()
    dicti = admin.verify("moris32345@hotmail.es", "nocorrecta")
    print(dicti)

elif test == '7':
    print(len("Hi"))

elif test == '8':
    admin = adminTrabajadores()
    lista = admin.fetchAllWorkersByWord("14", kind={'trabajadores.idTrabajadores'}, mode="asc", aprox= False)
    print(lista)

elif test == 'p':
    admin = adminTrabajadores()
    admin.createMembresia()

elif test == '9':
    admin = adminAdministrador()
    print(admin.verify("dedroperka@enayu.com", "contrasena"))
    