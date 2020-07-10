from database.Logics import adminClientes, adminAdministrador, adminTrabajadores

# Escriba el número de test que desea correr
test = '4'

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



