from SimpleXMLRPCServer import SimpleXMLRPCServer
from SimpleXMLRPCServer import SimpleXMLRPCRequestHandler
import xmlrpclib
import Tkinter, tkFileDialog #Esta libreria es para seleccionar la carpeta a compartir.
import threading
import socket #importamos esta libreria ya que usamos un metodo de esta para optener la direccion ip.
from os import listdir
import os
from os import walk

#Metodos del servidor
class Servidor(object):
    
    def MandarArchivo(self, nombre):
        archivo = open('.\compartido/' + nombre)
        contenido = archivo.read()
        archivo.close()
        return contenido

    def CrearCopia(self, nombre, contenido):
        archivo = open('.\compartido/copia' + nombre, 'w')
        archivo.write(contenido)
        archivo.close()
        return 'Copia creada'
        

#Carpeta que se va a compartir
def listaArchivos():
    return listdir('.\compartido')

#Conectandose al servidor.
print 'hola'
op = xmlrpclib.ServerProxy('http://192.168.9.72:9999') #Ensallar con la direccion ip del servidor.
lista_archivos = listaArchivos()
ip, puerto, lista_archivo = op.Crear_cliente(lista_archivos)
print ip
print puerto
print lista_archivo

#Crenado el servidor
server = SimpleXMLRPCServer((str(ip), puerto)) #Ensallar con la direccion ip del equipo
print 'Servidor creado'
server.register_introspection_functions()
server.register_instance(Servidor())

t = threading.Thread(target = server.serve_forever)
t.start()

op.CrearCopias(lista_archivos, ip, puerto)

while True:
    a = 0
