#bibliotecas unidas
import tkinter as tk 
import pymongo 
from tkinter import messagebox, Toplevel
import pymongo.errors


#sistema de usuarios
MONGO_HOST = "localhost"
MONGO_PUERTO = "27017"
MONGO_TIEMPO_FUERA = 1000

MONGO_URI = "mongodb://localhost:27017/"
NOMBRE_DATABASE = "Biblioteca"
MONGO_COLECCION = "Registro"
MONGO_COLECCION_LIBROS = "libros"
MONGO_COLLECION_PRESTAMO = "prestamo"

global USUARIO

try:
    cliente = pymongo.MongoClient(MONGO_URI,serverSelectionTimeoutMS = MONGO_TIEMPO_FUERA)
    print("SE CONECTO AL SERVIDOR")
    base_datos = cliente[NOMBRE_DATABASE]
    COLLECCION = base_datos[MONGO_COLECCION]
    COLLECION_LIBROS = base_datos[MONGO_COLECCION_LIBROS]
    COLLECCION_PRESTAMO = base_datos[MONGO_COLLECION_PRESTAMO]
except pymongo.errors.ServerSelectionTimeoutError as ErrorTiempo:
    print("TIEMPO EXCEDIDO ", ErrorTiempo)
except pymongo.errors.ConnectionFailure as errorConexion:
    print("FALLO AL CONECTARSE AL MONGO DB ",errorConexion)

sesion_activa = {}

#ventana princial
ventana = tk.Tk() 
ventana.title("BIBLIOTECA")
ventana.geometry("200x105")
ventana.config(background="blue2")

#PAGINA DE INICIO DE SESION 
def iniciar_sesion():    
    #ventana de inicio de sesion 
    pagina_inicio = Toplevel(ventana)
    pagina_inicio.title("INICIO DE SESION")
    pagina_inicio.geometry("300x300")
    pagina_inicio.config(background="blue2")
    
    #mensaje1
    mensaje1 = tk.Label(master= pagina_inicio,text= " USUARIO ", background= "blue",font= "ARIAL 10")
    mensaje1.place(x = 50 , y = 30 )

    #entrada de informaci ( usuario )
    usuario = tk.Entry(pagina_inicio,font=("ARIAL 14"), width = 20)
    usuario.place(x = 50, y = 50 )
    usuario.configure(background= "silver")

    #mensaje2
    mensaje2 = tk.Label(master = pagina_inicio, text= "CONTRASEÑA", background="blue", font="arial 10")
    mensaje2.place(x = 50, y = 90 )

    #entrada de  informacion ( contraseña )
    contraseña = tk.Entry(pagina_inicio, font = ("Arial 14"), width = 20)
    contraseña.place(x = 50, y = 110 )
    contraseña.configure(background= "silver")

    #boton de inicio de sesion 
    usuario_entrada = tk.Button(pagina_inicio, text= "INICIAR SESION", bg = "steel blue", border = 5, command= lambda : verificar_usuario())  
    usuario_entrada.place(x = 100, y = 150 )

    def verificar_usuario():
        if COLLECCION.find_one({"nombre":usuario.get(), "contra": contraseña.get()}):
            sesion_activa [usuario.get()] = True
            print(sesion_activa)
            pagina_inicio.withdraw()
            pagina_del_usuario(usuario.get())
            ventana.withdraw()
        else:
            messagebox.showinfo("ERROR", "CONTRASEÑA O USUARIO INCORRECTOS")
        usuario.delete(0, 100)
        contraseña.delete(0, 100)

#PAGINA DE REGISTRO DE USUARIOS

def iniciar_registro():
    #VENTANAS 
    register = Toplevel(ventana)
    register.title("REGISTARSE")
    register.geometry("400x400")
    register.config(background= "blue2")

    #REGISTRO

    mensaje1 = tk.Label(master = register,text= "USUARIO", background= "blue", font="ARIAL 10")
    mensaje1.place(x = 50, y = 50)

    usuario = tk.Entry(master= register, font ="ARIAL 10 ", width= 20)
    usuario.place(x = 50, y = 70)

    mensaje2 = tk.Label(master = register, text = "CONTRASEÑA", background= "blue", font= "ARIAL 10" )
    mensaje2.place(x = 50, y = 90)

    contraseña = tk.Entry(master= register, font = "ARIAL 10", width= 20)
    contraseña.place(x = 50, y = 110)

    mensaje3 = tk.Label(master=register, text ="CONFIRMAR CONTRASEÑA", background= "blue", font = "ARIAL 10")
    mensaje3.place(x = 50, y = 130)

    confir_contraseña = tk.Entry(master = register, font = "ARIAL 10 ", width= 20)
    confir_contraseña.place(x = 50, y = 150)

    #BOTON REGISTRO 
    boton_registro = tk.Button(master= register, text = "REGISTRAR USUARIO ", bg = "steel blue", border = 5, command= lambda: registrar_user())
    boton_registro.place(x = 250, y = 100)
    def registrar_user():
        if COLLECCION.find_one({"nombre": usuario.get()}):
            messagebox.showinfo("ERROR", "USUARIO YA REGISTRADO")
        else:
            if contraseña.get() != confir_contraseña.get():
                messagebox.showinfo("ERROR", "CONTRASEÑA NO COINCIDE")
            else:
                if len (usuario.get()) != 0 and len(contraseña.get()) != 0 and len(confir_contraseña.get()) != 0:
                    documento = {"nombre": usuario.get(), "contra":contraseña.get()}
                    COLLECCION.insert_one(documento)
                    messagebox.showinfo("LOGIN", "SE REGISTRO USUARIO EXITOSAMENTE")
        usuario.delete(0,100)
        confir_contraseña.delete(0,100)
        contraseña.delete(0,100)
    register.mainloop()

#CERRAR LAS VENTANAS OCULTAS
def cerrar():
    for widget in ventana.winfo_children():
        if isinstance(widget, Toplevel):
            widget.destroy()
    ventana.destroy()

#VENTANA PARA PRESTAR LOS LIBROS SEGUN USUARIOS
def pagina_prestar_libro(usr1):
    usuario = usr1
    ventana_prestar = Toplevel(ventana)
    ventana_prestar.title("PRESTAR LIBRO")
    ventana_prestar.geometry("300x200")
    ventana_prestar.configure(background="blue2")
    
    libro_a_prestar = tk.Label(master=ventana_prestar,text="LIBRO A PRESTAR", background="blue2", font="ARIAL 15")
    libro_a_prestar.place(x=50, y=20)

    libro_prestar = tk.Entry(master=ventana_prestar, font=("ARIAL 15"), width= 20)
    libro_prestar.place(x=50, y=50)

    autor_a_prestar = tk.Label(master=ventana_prestar, text="AUTOR", background="blue2",font="ARIAL 15")
    autor_a_prestar.place(x=50, y=80)

    autor_prestar = tk.Entry(master=ventana_prestar, font=("ARIAL 15"),width=20)
    autor_prestar.place(x=50, y=110)

    prestar = tk.Button(master=ventana_prestar,text = "SOLICITAR PRESTAMO", bg = "steel blue", border = 5, command=lambda: solicitar_prestamo(usuario,libro_prestar.get(),autor_prestar.get()))
    prestar.place(x = 83 , y = 135)
    libro_prestar.delete(1,tk.END)
    autor_prestar.delete(1,tk.END)
    def solicitar_prestamo(usuario,libro,autor):
        usuario = usuario
        libro = libro 
        autor = autor 
        if COLLECION_LIBROS.find_one({"nombre_libro": libro, "autor": autor}):
            documento = {
                "libro": libro,
                "autor": autor,
                "estado": "Prestado",
                "solicitante": usuario
            }
            COLLECCION_PRESTAMO.insert_one(documento)
            COLLECION_LIBROS.delete_one({"nombre_libro": libro, "autor": autor})
            messagebox.showinfo("EXITO", "LIBRO PRESTADO EXITOSAMENTE")
            return True
        else:
            messagebox.showinfo("LO LAMENTAMOS", "EL LIBRO YA ESTA EN PRESTAMO")
            return False

#PAGINA PARA DEVLOVER LOS LIBROS PRESTADOS POR LOS USUARIOS
def pagina_devolver_libro(usr1):
    usuario = usr1
    ventana_devolver = Toplevel(ventana)
    ventana_devolver.title("DEVOLVER LIBRO")
    ventana_devolver.geometry("300x200")
    ventana_devolver.configure(background="blue2")

    libro_a_devolver = tk.Label(master=ventana_devolver, text="LIBRO A DEVOLVER", background="blue2", font="ARIAL 15")
    libro_a_devolver.place(x=50, y=20)

    libro_devolver = tk.Entry(master=ventana_devolver, font=("ARIAL 15"), width= 20)
    libro_devolver.place(x=50, y=50)

    autor_a_devolver = tk.Label(master=ventana_devolver, text="AUTOR", background="blue2",font = ("ARIAL 15"))
    autor_a_devolver.place(x=50, y=80)
    
    autor_devolver = tk.Entry(master=ventana_devolver, font=("ARIAL 15"), width= 20)
    autor_devolver.place(x=50, y=110)

    devoler = tk.Button(master=ventana_devolver,text = "DEVOLUCION DEL LIBRO", bg = "steel blue", border = 5, command=lambda: devolucion_libro(usuario,libro_devolver.get(),autor_devolver.get()))
    devoler.place(x = 83 , y = 135)
    def devolucion_libro(usuario,libro,autor):
        usuario = usuario
        libro = libro
        autor = autor
        if COLLECCION_PRESTAMO.find_one({"libro": libro, "autor":autor, "estado": "Prestado", "solicitante": usuario}):
            documento = {"libro": libro, "autor": autor}
            COLLECION_LIBROS.insert_one(documento)
            COLLECCION_PRESTAMO.delete_one({"libro": libro, "autor":autor, "estado": "Prestado", "solicitante": usuario})
            messagebox.showinfo("EXITO", "LIBRO DEVUELTO EXITOSAMENTE")
            return True
        else :
            messagebox.showinfo("LO LAMENTAMOS", "EL LIBRO NO ESTA EN PRESTAMO, SI LO TIENES EN EL INVENTARIO, PORFAVOR COMUNICATE CON NOSOTROS")
            libro_devolver.delete(1,tk.END)
            autor_devolver.delete(1,tk.END)


#REGISTRAR UN LIBRO CON NOMBRE Y AUTOR 
def pagina_agregar_libro():
    pagina_agregar = Toplevel(ventana)
    pagina_agregar.title("PAGINA DE AGREGAR LIBRO")
    pagina_agregar.geometry("300x170")
    pagina_agregar.config(background= "blue2")
    titulo1 = tk.Label(master = pagina_agregar, text = "TITULO DEL LIBRO",bg= "steel blue", border=5, font="ARIAL 15")
    titulo1.place(x = 50, y = 25)

    titulo = tk.Entry(master = pagina_agregar, font=("ARIAL 15"), width= 20)
    titulo.place(x = 40 , y = 50 )

    titulo2 = tk.Label(master = pagina_agregar, text = "AUTOR DEL LIBRO", bg = "steel blue", border=5, font="ARIAL 15")
    titulo2.place(x = 50, y = 80)

    autor = tk.Entry(master = pagina_agregar, font=("ARIAL 15"), width= 20)
    autor.place(x = 40 , y = 105)

    ingresar_libro = tk.Button(master= pagina_agregar, text = "AGREGAR EL LIBRO", bg = "steel blue", border = 5, command= lambda: registrar_libro())
    ingresar_libro.place(x = 100, y = 135)
    def registrar_libro():
        if len(titulo.get()) != 0 and len(autor.get()) != 0:
            COLLECION_LIBROS.insert_one({"nombre_libro":titulo.get(), "autor":autor.get()})
            messagebox.showinfo("LIBRO AGREGADO!!", "EL LIBRO HA SIDO AGREGADO A LA BASE DE DATOS")
            titulo.delete(0,100)
            autor.delete(0,100)
        else:
            messagebox.showinfo("ALERTA", "DEBE INGRESAR TITULO Y AUTOR")
        titulo.delete(1,tk.END)
        autor.delete(1,tk.END)

#BUSCAR UN LIBRO CON NOMBRE DEL LIBRO Y AUTOR 
def pagina_busqueda_libro():
    pagina_busqueda = Toplevel(ventana)
    pagina_busqueda.title("PAGINA DE BUSQUEDA DE LIBRO")
    pagina_busqueda.geometry("300x170")
    pagina_busqueda.config(background= "blue2")
    titulo1 = tk.Label(master = pagina_busqueda, text = "TITULO DEL LIBRO ",bg= "blue", border=5, font="ARIAL 15")
    titulo1.place(x = 50, y = 25)
    titulo = tk.Entry(master = pagina_busqueda, font=("ARIAL 15"), width= 20)
    titulo.place(x = 40 , y = 50 )

    autor1 = tk.Label(master = pagina_busqueda, text = "AUTOR DEL LIBRO", bg ="blue", border = 5, font = "ARIAL 15")
    autor1.place(x = 50, y = 80)
    autor = tk.Entry(master = pagina_busqueda, font=("ARIAL 15"), width= 20)
    autor.place(x = 40 , y = 105)
    buscar_libro = tk.Button(master = pagina_busqueda, text = "BUSCAR LIBRO", bg = "steel blue", border = 5, command = lambda: buscar_un_libro(titulo.get(), autor.get()))
    buscar_libro.place(x = 100, y = 130)
    def buscar_un_libro(libro,autor):
        libro ={"nombre_libro": libro, "autor": autor}
        if COLLECION_LIBROS.find_one(libro):
            messagebox.showinfo("LIBRO ENCONTRADO!!", "EL LIBRO HA SIDO ENCONTRADO EN LA BASE DE DATOS")
        else:
            messagebox.showinfo("LIBRO NO ENCONTRADO!!", "LO SENTIMOS, EL LIBRO NO HA SIDO ENCONTRADO EN LA BASE DE DATOS, VERIFIQUE QUE LOS DATOS INGRESADOS SEAN CORRECTOS ")
        titulo.delete(1,tk.END)
        autor.delete(1,tk.END)

#VENTANA DE LOS USUARIOS 
def pagina_del_usuario(usr1):
    usuario = usr1
    pagina_del_usuario = Toplevel(ventana)
    pagina_del_usuario.title("PAGINA DEL USUARIO")
    pagina_del_usuario.geometry("200x150")
    pagina_del_usuario.config(background= "blue2")
    buscar_libro = tk.Button(master = pagina_del_usuario,text= "BUSCAR UN LIBRO", bg = "steel blue", border = 5, command =lambda: pagina_busqueda_libro())
    agregar_libro = tk.Button(master=pagina_del_usuario,text= "AGREGAR UN LIBRO", bg = "steel blue", border= 5, command= lambda: pagina_agregar_libro())
    presatar_libro = tk.Button(master = pagina_del_usuario, text="PRESTAR UN LIBRO", bg = "steel blue", border = 5, command = lambda: pagina_prestar_libro(usuario))
    devolver_libro = tk.Button(master = pagina_del_usuario, text = "DEVOLVER UN LIBRO", bg ="steel blue", border = 5, command = lambda: pagina_devolver_libro(usuario))
    cerrar_sesion = tk.Button(master=pagina_del_usuario,text= "CERRAR SESION", bg = "red", border = 5, command = lambda: terminar_sesion())
    
    buscar_libro.place(x = 5 , y = 5)
    agregar_libro.place(x =5 , y = 35)
    presatar_libro.place(x = 5 , y = 65)
    devolver_libro.place(x = 5 , y = 95)
    cerrar_sesion.place(x = 5, y = 125)

    buscar_libro.config(width=25)
    agregar_libro.config(width=25)
    presatar_libro.config(width=25)
    devolver_libro.config(width=25)
    cerrar_sesion.config(width=25)


    def terminar_sesion():
        sesion_activa.clear()
        print(sesion_activa)
        messagebox.showinfo("SESION TERMINADA", "SESION TERMINADA EXITOSAMENTE")
        pagina_del_usuario.withdraw()
        ventana.iconify()

# BOTONES EN PANTALLA 

registrar_user = tk.Button(text="REGISTARSE", bg = "steel blue", border = 5,command = lambda: iniciar_registro())
inicio_sesion = tk.Button(text= "INICIAR SESION", bg = "steel blue", border = 5, command= lambda: iniciar_sesion())
salir = tk.Button(text = "SALIR", bg = "red", border= 5 , command= lambda: cerrar())

#posicion
registrar_user.place(x =5, y = 5 )
inicio_sesion.place(x = 5, y = 35)
salir.place(x = 5, y = 65)

#tamaño
registrar_user.config(width= 25)
inicio_sesion.config(width= 25)
salir.config(width=25)

ventana.mainloop()