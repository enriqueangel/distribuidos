from SimpleXMLRPCServer import SimpleXMLRPCServer
from SimpleXMLRPCServer import SimpleXMLRPCRequestHandler
import xmlrpclib
import Tkinter, tkFileDialog #Esta libreria es para seleccionar la carpeta a compartir.
import threading
import socket #importamos esta libreria ya que usamos un metodo de esta para optener la direccion ip.
from os import listdir
import os
from os import walk

class compartido:
    def __init__(self):
        self.nombre_archivo = []
        self.directorio = 0

#Clase con los metodos a utlilzar.
class clase:
    
    def Envio_contenido(self, directorio, nombre):
        archivo = open(directorio+'/'+nombre)
        contenido = archivo.read()
        return contenido

    def Actualizar_contenido(self, directorio, nombre, contenido):
        os.unlink(directorio+"/"+nombre)
        archivo = open(directorio+"/"+nombre, 'w')
        archivo.write(contenido)
        archivo.close()
        return "Archivo actualizado"

#El cliente selecciona los archivos que se van a compartir.
def Archivos_compartidos(directorio):
    lista_archivos = []
    for (path, ficheros, archivos) in walk(directorio): #Muestra los archivos y carpetas y subcarpetas con direccion
        archivo = compartido()
        archivo.directorio = path
        archivo.nombre_archivo = archivos
        lista_archivos.append(archivo)
    return lista_archivos

#Carpeta que se va a compartir
def Seleccionar_carpeta():
    return '/compartido'

def Menu_operaciones_archivo():
    print '\nEscoja una opcion.'
    print '1. Abrir archivo.'
    print '2. Modificar archivo.'
    print '3. Salir.'
    return raw_input('Opcion: ')

def Menu_lista_archivos(archivos):
    print '\nEscoja un archivo.'
    for i in range(len(archivos)):
        print ' ' + str(i) + '. ' + archivos[i]['archivo'] + "el permiso es: ",archivos[i]['permiso'] 
    return raw_input('Opcion: ')



#Conectandose al servidor.
print 'hola'
op = xmlrpclib.ServerProxy('http://192.168.8.184:9999') #Ensallar con la direccion ip del servidor.
carpeta = Seleccionar_carpeta()
lista_archivos = Archivos_compartidos(carpeta)
ip, puerto, lista_archivo = op.Crear_cliente(carpeta, lista_archivos)

#Crenado el servidor
server = SimpleXMLRPCServer((str(ip), puerto)) #Ensallar con la direccion ip del equipo
server.register_introspection_functions()
server.register_instance(clase())
salir = False
#server.serve_forever()
while True:   #LOS PERMISOS PARA LOS ARCHIVOS SON 0 = NINGUNO, 1 = LECTURA, 2 = ESCRITURA
    if salir == False:
        t = threading.Thread(target=server.serve_forever)
        t.start()
    else:
        break
    opcion = Menu_operaciones_archivo()
    if(opcion == '3'):
        print op.Salir(ip, puerto)
        salir = True
    if(opcion == "1"):
        lista_archivo = op.Comparar_archivos(lista_archivo)
        opcion_archivo = Menu_lista_archivos(lista_archivo)
        if(lista_archivo[int(opcion_archivo)]['permiso'] == 0):
            print "No tiene permisos para leer este archivo."
        else:
            contenido_archivo = op.Abrir_archivo(int(opcion_archivo))
            print contenido_archivo
    if(opcion == "2"):
        lista_archivo = op.Comparar_archivos(lista_archivo)
        opcion_archivo = Menu_lista_archivos(lista_archivo)
        if(lista_archivo[int(opcion_archivo)]['permiso'] != 2):
            print "No tiene permisos para leer este archivo."
        else:
            contenido = op.Abrir_archivo_escritura(int(opcion_archivo))
            if(type(contenido) != bool):
                print contenido
                archivo = open("archivo_editar.txt", "w")
                archivo.write(str(contenido))
                archivo.write(raw_input("Contenido agregar: "))
                archivo.close()
                archivo = open("archivo_editar.txt")
                contenido_nuevo = archivo.read()
                archivo.close()
                mensaje = op.Modificar_archivo(contenido_nuevo, int(opcion_archivo))
                os.unlink("archivo_editar.txt")
                print mensaje
            else:
                print "el archivo se encuentra ocupado."