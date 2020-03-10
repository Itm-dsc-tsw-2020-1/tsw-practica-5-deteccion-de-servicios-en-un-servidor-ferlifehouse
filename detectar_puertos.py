#Importamos todo lo necesario para que el programa corra :D
import os
import re
import mysql.connector as mysql
import tkinter as tk
from tkinter import ttk

#Comandos para crear la base de datos
#En la carpeta del mysql: mysql -u root -h localhost -p
#CREATE DATABASE ports;
#USE ports;
#CREATE TABLE schedule (ip VARCHAR(15), port VARCHAR(15), state VARCHAR(20), service VARCHAR(20), PRIMARY KEY(ip, port, state, service));

""" Aquí seleccionamos la pc, anteriormente usamos el código siguiente en otro script python para
saber a cuál computadora podíamos hacerle esta prueba de puertos

Código:

import os
red = "200.33.171.0/24"
os.system("nmap -sP "+red) """

#Función para buscar patrón en todo el texto
def buscar(patron, texto):
    li = re.findall(patron, texto)
    return li

#Función para imprimir (prueba)
def imprimir(listita):
    for x in range(len(listita)):
        print(listita[x]+str(x))

#Hacemos la conexión a la base de datos
conexion = mysql.connect(host='localhost', user='root', passwd='', db='ports')
#Creamos el cursor para trabajar con la base de datos
operacion = conexion.cursor()

#Se ejecuta el comando de nmap y se captura la salida
red = "200.33.171.13"
resultado = os.popen("nmap -sT "+red).read()

#Se buscan las cadenas necesarias a extraer
pat = '([0-9]+/tcp|[0-9]+/udp)'
li_port = buscar(pat, resultado)
pat = '(open|closed)'
li_state = buscar(pat, resultado)
pat = '(open.+[a-z0-9]+|closed.+[a-z0-9]+)'
li_service = buscar(pat, resultado)

#Método para extraer solo el servicio de li_service
contador = 0
while contador < len(li_service):
    llave = li_service[contador].find("open")
    if llave == 0:
        li_service[contador] = li_service[contador][6:]
    llave = li_service[contador].find("open")
    if llave == 0:
        li_service[contador] = li_service[contador][8:]
    contador = contador + 1

imprimir(li_port)
imprimir(li_state)
imprimir(li_service)

#Se inserta la información en la tabla schedule de ports
contador = 0
while contador < len(li_service):
    operacion.execute("INSERT INTO schedule (ip, port, state, service) VALUES (%s, %s, %s, %s)", (red, li_port[contador], li_state[contador], li_service[contador]))
    conexion.commit()
    contador = contador + 1

#Se imprime la tabla en consola para ver que los datos se subieron correctamente a la base de datos
operacion.execute( "SELECT * FROM schedule" )
for ip, port, state, service in operacion.fetchall() :
    print (ip, port, state, service)
conexion.close()

"""Ahora, para generar una ventana y que se muestren los datos, solo tenemos que hacer uso de la librería de Tkinter,
para ello, hacemos lo siguiente..."""

#Se creael objeto de la ventana
ventana = tk.Tk()

#Se crean 4 grupos para listas, cada grupo corresponde a un campo: IP, Ports, States, Services
listbox1 = tk.Listbox(ventana)
listbox1.grid(column=0, row=0)
listbox2 = tk.Listbox(ventana)
listbox2.grid(column=1, row=0)
listbox3 = tk.Listbox(ventana)
listbox3.grid(column=2, row=0)
listbox4 = tk.Listbox(ventana)
listbox4.grid(column=3, row=0)

#Título de la ventana
ventana.title("Detección de puertos - NMAP - Fernando Campos")

#Se escriben estáticamente los campos de la ventana
listbox1.insert(0, "IP")
listbox2.insert(0, "Puertos")
listbox3.insert(0, "Estado")
listbox4.insert(0, "Servicio")

#Ciclo para añadir los datos a los grupos de listas creados anteriormente
contador = 0
while contador < len(li_service):
    listbox1.insert(contador+1, red)
    listbox2.insert(contador+1, li_port[contador])
    listbox3.insert(contador+1, li_state[contador])
    listbox4.insert(contador+1, li_service[contador])
    contador = contador + 1

#Indicamos la redimensión y corremos el loop para que se muestre la ventana
ventana.resizable(0,0)
ventana.mainloop()

