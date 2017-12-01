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

	def ActualizarCopia(self, directorio, nombre, contenido):
		os.unlink(directorio+"/"+nombre)
		archivo = open(directorio+"/"+nombre, 'w')
		archivo.write(contenido)
		archivo.close()
		return "Copia actualizada"

	def CrearCopia(self, nombre, contenido):
		archivo = open('.\compartido/copia' + nombre, 'w')
		archivo.write(contenido)
		archivo.close()
		return 'Copia creada'

	def Tsl(self, directorio, nombre):
		archivo = open(directorio+'/'+nombre)
		contenido = archivo.read()
		archivo.close()
		if int(contenido) == 0:
			archivo = open('.\compartido/' + nombre, 'w')
			archivo.write("1")
			archivo.close()
			return True
		else:
			return False

	def TslLibre(self, directorio, nombre):
		archivo = open('.\compartido/' + nombre, 'w')
		archivo.write("0")
		archivo.close()
		return True

#Carpeta que se va a compartir
def listaArchivos():
	return listdir('.\compartido')

def Menu_operaciones_archivo():
	print '\nEscoja una opcion.'
	print '1. Abrir archivo.'
	print '2. Modificar archivo.'
	print '3. Salir.'
	return raw_input('Opcion: ')

def Menu_lista_archivos(archivos):
	print '\nEscoja un archivo.'
	for i in range(len(archivos)):
		print ' ' + str(i) + '. ' + archivos[i] 
	return raw_input('Opcion: ')

#Conectandose al servidor.
print 'hola'
op = xmlrpclib.ServerProxy('http://192.168.0.5:9999') #Ensallar con la direccion ip del servidor.
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
		contenido_archivo = op.Abrir_archivo(int(opcion_archivo))
		print contenido_archivo
	if(opcion == "2"):
		lista_archivo = op.Comparar_archivos(lista_archivo)
		opcion_archivo = Menu_lista_archivos(lista_archivo)
		if op.Tsl(int(opcion_archivo)):
			contenido = op.Abrir_archivo_escritura(int(opcion_archivo))
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
			copia = op.ModficiarCopias(contenido_nuevo, int(opcion_archivo))
			tsl = op.TslLibre(int(opcion_archivo))
			print mensaje
		else:
			print "la pagina se encuentra en la zona critica"
