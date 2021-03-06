from SimpleXMLRPCServer import SimpleXMLRPCServer
from SimpleXMLRPCServer import SimpleXMLRPCRequestHandler
import xmlrpclib
import threading
import random


#Sobre escribimos el rpc para obtener las direcciones ip de los clientes.
class RequestHandler(SimpleXMLRPCRequestHandler):
    def __init__(self, request, client_address, server):
        Mostrar_direccion(client_address)
        SimpleXMLRPCRequestHandler.__init__(self, request, client_address, server)


def Mostrar_direccion(ip):
    carpeta = '.\compartido'
    puerto = 0
    dato = Manejo(ip[0], carpeta, puerto, 0, 0)
    Clientes_conectados.append(dato)



#Clase para le manejo de direcciones y directorios.
class Manejo:

    def __init__ (self, direccion_ip, carpeta, puerto, archivo, espacio):
        self.ip = direccion_ip
        self.directorio = carpeta
        self.puerto = puerto
        self.archivos = archivo
        self.espacio = espacio

class Manejo_archivo_servidor:
    def __init__(self, ip, puerto, archivo, tsl):
        self.ip = ip
        self.puerto = puerto
        self.archivos = archivo
        self.copia = []
        self.tsl = tsl

    def CrearCopia(self,ListaClientes):
        ClientesLLenos = []
        while True:
            if len(ListaClientes) == 1:
                break
            else:
                cliente = random.randint(0,len(ListaClientes)-1)
                if(ListaClientes[cliente].espacio < 10 and (ListaClientes[cliente].ip != self.ip or ListaClientes[cliente].puerto != self.puerto)):
                    IpCliente = ListaClientes[cliente].ip
                    PuertoCliente = ListaClientes[cliente].puerto
                    s = xmlrpclib.ServerProxy('http://'+str(IpCliente)+':'+str(PuertoCliente))
                    ContenidoArchivo = s.MandarArchivo(self.archivos)
                    Mensaje = s.CrearCopia(self.archivos, ContenidoArchivo)
                    print Mensaje
                    ListaClientes[cliente].espacio += 1
                    copia = [ListaClientes[cliente].ip, ListaClientes[cliente].puerto]
                    self.copia.append(copia)
                    break
                else:
                    if(len(ListaClientes) == len(ClientesLLenos)):
                        break
                    else:
                        bandera = False
                        for i in ClientesLLenos:
                            if cliente == i:
                                bandera = True
                                break
                        if not(bandera):
                            ClientesLLenos.append(cliente)



#Clase con los metodos a utilizar.
class clase:

    #Cuando el cliente se conecte con el servidor definira la carpeta que compartira los archivos y guardamos las archivos que a a compartir.
    def Crear_cliente(self, lista_archivos):
        global Clientes_conectados
        global ClientesActivos
        global Lista_global_archivos
        lista_archivos_cliente = []
        i = len(Clientes_conectados)
        ip = Clientes_conectados[i-1].ip
        puerto = 9999 - i
        directorio = ".\compartido"
        espacio = len(lista_archivos)
        dato = Manejo(ip, directorio, puerto, lista_archivos, espacio)
        ClientesActivos.append(dato)
        self.Agregar_archivos_globales(ip, puerto,lista_archivos, Lista_global_archivos, lista_archivos_cliente)
        return ip, puerto, lista_archivos_cliente

    def Agregar_archivos_globales(self, ip, puerto, lista_archivos, Lista_global_archivos, lista_archivos_cliente):
        global ClientesActivos
        f = len(ClientesActivos) - 1
        for j in Lista_global_archivos:
            archivo_copia = j.archivos
            lista_archivos_cliente.append(archivo_copia)
        for i in lista_archivos:
            tsl = ".\compartido/tsl"+i
            archivo = open('.\compartido/tsl' + i, 'w')
            archivo.write("0")
            archivo.close()
            archivo = Manejo_archivo_servidor(ip, puerto, i, tsl)
            ClientesActivos[f].espacio += 1
            Lista_global_archivos.append(archivo)
            archivo_cliente = i
            lista_archivos_cliente.append(archivo_cliente)
            print archivo
        return Lista_global_archivos, lista_archivos_cliente

    def CrearCopias(self, lista_archivos, ip, puerto):
        global ClientesActivos
        global Lista_global_archivos
        for i in lista_archivos:
            for n in Lista_global_archivos:
                if(n.ip == ip and n.puerto == puerto and n.archivos == i):
                    n.CrearCopia(ClientesActivos)
                    n.CrearCopia(ClientesActivos)
        return "copias guardadas satisfactoriamente"

    def Comparar_archivos(self, lista_archivos_cliente):
        global Lista_global_archivos
        i = len(lista_archivos_cliente)
        n = len(Lista_global_archivos)
        if(i == n):
            return lista_archivos_cliente
        if(i < n):
            while i < n:
                nombre = Lista_global_archivos[i].archivos
                archivo = nombre
                lista_archivos_cliente.append(archivo)
                i = i + 1
            return lista_archivos_cliente
        if(i > n):
            a= 0
            b= 0
            while n != i:
                if(b < n): 
                    nombre_servidor = Lista_global_archivos[a].archivos
                    nombre_cliente = lista_archivos_cliente[b]
                    if(nombre_cliente == nombre_servidor):
                        a = a+1
                        b= b+1
                    else:
                        lista_archivos_cliente.pop(b)
                        a = a+1
                        i = i-1
                else:
                    while(b < i):
                        lista_archivos_cliente.pop(b)
                        i = i-1
            return lista_archivos_cliente

    def Abrir_archivo(self, indice):
        global Lista_global_archivos
        ip = Lista_global_archivos[indice].ip
        puerto = Lista_global_archivos[indice].puerto
        directorio = '.\compartido'
        nombre = Lista_global_archivos[indice].archivos
        s = xmlrpclib.ServerProxy('http://'+str(ip)+':'+str(puerto))
        contenido = s.Envio_contenido(directorio, nombre)
        return contenido

    def Abrir_archivo_escritura(self, indice):
        global Lista_global_archivos 
        ip = Lista_global_archivos[indice].ip
        puerto = Lista_global_archivos[indice].puerto
        directorio = '.\compartido'
        nombre = Lista_global_archivos[indice].archivos
        s = xmlrpclib.ServerProxy('http://'+str(ip)+':'+str(puerto))
        contenido = s.Envio_contenido(directorio, nombre)
        return contenido

    def Modificar_archivo(self,contenido, indice):
        global Lista_global_archivos
        ip = Lista_global_archivos[indice].ip
        puerto = Lista_global_archivos[indice].puerto
        directorio = directorio = '.\compartido'
        nombre = Lista_global_archivos[indice].archivos
        s = xmlrpclib.ServerProxy('http://'+str(ip)+':'+str(puerto))
        actualizado = s.Actualizar_contenido(directorio, nombre, contenido)
        return actualizado

    def ModficiarCopias(self,contenido, indice):
        global Lista_global_archivos
        ip = Lista_global_archivos[indice].ip
        puerto = Lista_global_archivos[indice].puerto
        directorio = directorio = '.\compartido'
        if len(Lista_global_archivos[indice].copia) > 0:
            for i in Lista_global_archivos[indice].copia:
                nombre = "copia"+Lista_global_archivos[indice].archivos
                s = xmlrpclib.ServerProxy('http://'+str(ip)+':'+str(puerto))
                actualizado = s.ActualizarCopia(directorio, nombre, contenido)
                print actualizado
        else: 
            print "No tiene copias para actualizar"
        return True

    def Tsl(self, indice):
        global Lista_global_archivos
        ip = Lista_global_archivos[indice].ip
        puerto = Lista_global_archivos[indice].puerto
        directorio = directorio = '.\compartido'
        nombre = "tsl"+Lista_global_archivos[indice].archivos
        s = xmlrpclib.ServerProxy('http://'+str(ip)+':'+str(puerto))
        permiso = s.Tsl(directorio, nombre)
        return permiso

    def TslLibre(self, indice):
        global Lista_global_archivos
        ip = Lista_global_archivos[indice].ip
        puerto = Lista_global_archivos[indice].puerto
        directorio = directorio = '.\compartido'
        nombre = "tsl"+Lista_global_archivos[indice].archivos
        s = xmlrpclib.ServerProxy('http://'+str(ip)+':'+str(puerto))
        permiso = s.TslLibre(directorio, nombre)
        return permiso


    def Salir(self, ip, puerto):
        global Clientes_conectados
        i = 0
        n = 0
        while i < len(Lista_global_archivos):
            if(Lista_global_archivos[i].ip == ip and Lista_global_archivos[i].puerto == puerto):
                Lista_global_archivos.pop(i)
            else:
                i = i+1
        while n < len(Clientes_conectados):
            if(Clientes_conectados[n].ip == ip and Clientes_conectados[n].puerto == puerto):
                Clientes_conectados.pop(n)
            else:
                n = n+1
        return 'Hasta luego'


#creando servidor.
server = SimpleXMLRPCServer(("192.168.0.5", 9999), requestHandler=RequestHandler)
server.register_introspection_functions()
server.register_instance(clase())
Clientes_conectados = [] #Lista de clientes conectados al servidor.
ClientesActivos = []
Lista_global_archivos = []#Lista donde se encuentran todos los archivos que comparten todos los clientes.
#Este hilo se ecnarga de recibir nuevos clientes y la carpeta a compartir.
t = threading.Thread(target=server.serve_forever)
t.start()
