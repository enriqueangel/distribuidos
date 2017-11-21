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
    carpeta = ""
    puerto = 0
    dato = Manejo(ip[0], carpeta, puerto)
    Clientes_conectados.append(dato)



#Clase para le manejo de direcciones y directorios.
class Manejo:

    def __init__ (self, direccion_ip, carpeta, puerto):
        self.ip = direccion_ip
        self.directorio = carpeta
        self.puerto = puerto
        self.archivos = 0

class Manejo_archivo_servidor:
    def __init__(self, ip, puerto, path, archivo):
        self.ip = ip
        self.directorio = path
        self.puerto = puerto
        self.archivos = archivo
        self.ocupado = 0

class Manejo_archivo_cliente:
    def __init__(self, archivo, permiso,):
        self.archivo = archivo
        self.permiso = permiso


#Clase con los metodos a utilizar.
class clase:

    #Cuando el cliente se conecte con el servidor definira la carpeta que compartira los archivos y guardamos las archivos que a a compartir.
    def Crear_cliente(self, carpeta, lista_archivos):
        global Clientes_conectados
        global Lista_global_archivos
        lista_archivos_cliente = []
        i = len(Clientes_conectados)
        puerto = 9999 - i
        Clientes_conectados[i-1].directorio = carpeta
        Clientes_conectados[i-1].puerto = puerto
        Clientes_conectados[i-1].archivos = lista_archivos
        ip = Clientes_conectados[i-1].ip
        self.Agregar_archivos_globales(ip, puerto,lista_archivos, Lista_global_archivos, lista_archivos_cliente)
        return ip, puerto, lista_archivos_cliente


    def Agregar_archivos_globales(self, ip, puerto, lista_archivos, Lista_global_archivos, lista_archivos_cliente):
        for j in Lista_global_archivos:
            permiso = random.randint(0,2)
            archivo_copia = Manejo_archivo_cliente(j.archivos, permiso)
            lista_archivos_cliente.append(archivo_copia)
        for i in lista_archivos:
            path = i["directorio"]
            for n in i["nombre_archivo"]:
                archivo = Manejo_archivo_servidor(ip, puerto, path, n)
                Lista_global_archivos.append(archivo)
                archivo_cliente = Manejo_archivo_cliente(n, 2)
                lista_archivos_cliente.append(archivo_cliente)
        return Lista_global_archivos, lista_archivos_cliente


    def Comparar_archivos(self, lista_archivos_cliente):
        global Lista_global_archivos
        i = len(lista_archivos_cliente)
        n = len(Lista_global_archivos)
        if(i == n):
            return lista_archivos_cliente
        if(i < n):
            while i < n:
                nombre = Lista_global_archivos[i].archivos
                permiso = random.randint(0,2)
                archivo = Manejo_archivo_cliente(nombre, permiso)
                lista_archivos_cliente.append(archivo)
                i = i + 1
            print len(lista_archivos_cliente)
            return lista_archivos_cliente
        if(i > n):
            a= 0
            b= 0
            while n != i:
                if(b < n): 
                    nombre_servidor = Lista_global_archivos[a].archivos
                    nombre_cliente = lista_archivos_cliente[b]['archivo']
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
        directorio = Lista_global_archivos[indice].directorio
        nombre = Lista_global_archivos[indice].archivos
        s = xmlrpclib.ServerProxy('http://'+str(ip)+':'+str(puerto))
        contenido = s.Envio_contenido(directorio, nombre)
        return contenido


    def Abrir_archivo_escritura(self, indice):
        global Lista_global_archivos
        if(Lista_global_archivos[indice].ocupado == 0):  
            ip = Lista_global_archivos[indice].ip
            puerto = Lista_global_archivos[indice].puerto
            directorio = Lista_global_archivos[indice].directorio
            nombre = Lista_global_archivos[indice].archivos
            Lista_global_archivos[indice].ocupado = 1
            s = xmlrpclib.ServerProxy('http://'+str(ip)+':'+str(puerto))
            contenido = s.Envio_contenido(directorio, nombre)
            return contenido
        else:
            return False


    def Modificar_archivo(self,contenido, indice):
        global Lista_global_archivos
        ip = Lista_global_archivos[indice].ip
        puerto = Lista_global_archivos[indice].puerto
        directorio = Lista_global_archivos[indice].directorio
        nombre = Lista_global_archivos[indice].archivos
        s = xmlrpclib.ServerProxy('http://'+str(ip)+':'+str(puerto))
        actualizado = s.Actualizar_contenido(directorio, nombre, contenido)
        Lista_global_archivos[indice].ocupado = 0
        return actualizado



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
server = SimpleXMLRPCServer(("192.168.0.6", 9999), requestHandler=RequestHandler)
server.register_introspection_functions()
server.register_instance(clase())
Clientes_conectados = [] #Lista de clientes conectados al servidor.
Lista_global_archivos = []#Lista donde se encuentran todos los archivos que comparten todos los clientes.
#Este hilo se ecnarga de recibir nuevos clientes y la carpeta a compartir.
t = threading.Thread(target=server.serve_forever)
t.start()



#ensallo = True
#while ensallo == True:
#    if len(Clientes_conectados) > 0:
#        for i in Clientes_conectados:
#            direccion = i.directorio
#            if (direccion != ""):
#                for n in Lista_global_archivos:
#                    print n.archivos
                # for n in i.archivos:
                #     print n['directorio']
                #     #print n.directorio[0]
                #     print n['nombre_archivo'][0]
                # puerto = i.puerto
                # ip = i.ip
                # #print ip
                # #print 'http://'+str(ip)+':'+str(puerto)
                # s = xmlrpclib.ServerProxy('http://'+str(ip)+':'+str(puerto)) #Aqui toca ensallar con la direccion desde otro pc.
                # s.Archivos_compartidos(direccion)
                #ensallo = False
