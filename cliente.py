from SimpleXMLRPCServer import SimpleXMLRPCServer
from SimpleXMLRPCServer import SimpleXMLRPCRequestHandler
import xmlrpclib
import Tkinter, tkFileDialog #Esta libreria es para seleccionar la carpeta a compartir.
import threading
import socket #importamos esta libreria ya que usamos un metodo de esta para optener la direccion ip.
from os import listdir
import os
from os import walk

#Carpeta que se va a compartir
def lsitaArchivos():
    return listdir('.\compartido')

#Conectandose al servidor.
print 'hola'
op = xmlrpclib.ServerProxy('http://192.168.8.184:9999') #Ensallar con la direccion ip del servidor.
lista_archivos = lsitaArchivos()
print lista_archivos
ip, puerto, lista_archivo = op.Crear_cliente(lista_archivos)
print ip
print puerto

# while True:
#     print 'conecte'