from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import mysql.connector


# Crear la base de datos en caso de que no este creada.
def createbd():
    try:
        mibase = mysql.connector.connect(
            host="localhost", user="root", passwd=""
        )

        micursor = mibase.cursor()

        micursor.execute("CREATE DATABASE mi_plantilla")

        mibase = mysql.connector.connect(
            host="localhost", user="root", passwd="", database="mi_plantilla"
        )

        micursor = mibase.cursor()

        micursor.execute("""CREATE TABLE agenda( id int(11) NOT NULL PRIMARY KEY AUTO_INCREMENT,
            nombre VARCHAR(128) COLLATE utf8_spanish2_ci NOT NULL,
            apellido VARCHAR(128) COLLATE utf8_spanish2_ci NOT NULL,
            numero VARCHAR(128) COLLATE utf8_spanish2_ci NOT NULL)""")
        messagebox.showinfo("Exito", "La base de datos fue creada con exito.")
    except:
        messagebox.showwarning("Error", "La base de datos no pudo ser creada.")


# Funcion que limpia los Entrys de la ventana
def reset():
    id_entry.delete("0", END)
    name_entry.delete("0", END)
    surname_entry.delete("0", END)
    number_entry.delete("0", END)


def updatelist():
    # Limpio treeview
    records = tv.get_children()
    for element in records:
        tv.delete(element)
    # Conecto a la BD
    mibase = mysql.connector.connect(
        host="localhost", user="root", passwd="", database="mi_plantilla"
    )
    # Creo un cursor
    cursor = mibase.cursor()

    sql = "SELECT * FROM agenda"

    cursor.execute(sql)
    data = cursor.fetchall()
    # Imprimo los datos en la Treeview
    for i in data:
        tv.insert("", "end", values=i)

    # Cierro la conexion
    mibase.close()


def addcontact():
    # Obtengo los datos desde los entrys
    enombre = name_entry.get()
    eapellido = surname_entry.get()
    enumero = number_entry.get()

    # Conecto a la BD
    mibase = mysql.connector.connect(
        host="localhost", user="root", passwd="", database="mi_plantilla"
    )
    # Creo un cursor
    cursor = mibase.cursor()

    # Selecciono la columna "numero"
    cursor.execute("SELECT numero FROM agenda")

    # Selecciono toda la columna
    numeros_agenda = cursor.fetchall()

    # El numero ingresado por el usuario es convertido a una tupla
    # para poder chequear si el numero ya existe en la agenda.
    if (enumero,) in numeros_agenda:
        messagebox.showerror("Error", "El numero ingresado ya existe")
    else:
        # Ingreso los datos provenientes del entry a la DB
        sql = """INSERT INTO agenda
            (nombre, apellido, numero)
            VALUES (%s, %s, %s)"""
        datos = (enombre, eapellido, enumero)

        cursor.execute(sql, datos)

        # Confirmo los cambios en la DB
        mibase.commit()

        messagebox.showinfo("Exito", "Contacto agregado")
        # Cierro la conexion
        mibase.close()

        reset()
    updatelist()


def updatecontact():
    # Conecto a la DB
    mibase = mysql.connector.connect(
        host="localhost", user="root", passwd="", database="mi_plantilla"
    )
    # Creo un cursor
    micursor = mibase.cursor()

    # Le digo a la DB que actualice los datos Nombre, Apellido y Numero
    # en la ID que figura en el entry de la ventana.
    sql = """UPDATE agenda
        SET nombre = %s, apellido = %s, numero = %s
        WHERE id = %s"""
    # Tomo los datos de los entrys
    datos = (
        name_entry.get(),
        surname_entry.get(),
        number_entry.get(),
        id_entry.get()
    )

    micursor.execute(sql, datos)

    # Confirmo los cambios a la DB
    mibase.commit()

    messagebox.showinfo("Exito", "Contacto actualizado")

    # Cierro la conexion
    mibase.close()

    reset()
    updatelist()


def deletecontact():
    # Conecto a la DB
    mibase = mysql.connector.connect(
        host="localhost", user="root", passwd="", database="mi_plantilla"
    )
    # Creo un cursor
    micursor = mibase.cursor()

    # Le digo a la DB que elimine todos los datos de la fila del ID
    # que se encuentra en el entry.
    sql = "DELETE FROM agenda WHERE id = %s"
    id = (id_entry.get(),)

    micursor.execute(sql, id)

    # Confirmo los cambios a la DB
    mibase.commit()

    messagebox.showinfo("Exito", "Contacto eliminado")

    # Cierro la conexion
    mibase.close()

    reset()
    updatelist()


# Funcion que ingresa los datos que el usuario seleccion del treeview
# a los entrys.
def select_record(evento):
    id_entry.delete(0, END)
    name_entry.delete(0, END)
    surname_entry.delete(0, END)
    number_entry.delete(0, END)
    # Variable que selecciona el contacto que hicimos click en la treeview
    selected = tv.focus()

    # Tomo todos los valores del treeview y los llamo "values"
    values = tv.item(selected, "values")

    # Ingreso los datos del treeview a los entrys
    id_entry.insert(0, values[0])
    name_entry.insert(0, values[1])
    surname_entry.insert(0, values[2])
    number_entry.insert(0, values[3])


window = Tk()
window.title("Agenda")
window.resizable(False, False)
window.iconbitmap('sources/agenda.ico')

Frame1 = LabelFrame(window, text="Datos del contacto")
Frame1.grid(padx=15, pady=15)


Inside_Frame1 = Frame(Frame1)
Inside_Frame1.grid(row=0, column=0, padx=15, pady=15)

id_label = Label(Inside_Frame1, text="ID")
id_label.grid(row=0, column=0, padx=5, pady=5)
id_var = StringVar()
id_entry = Entry(
    Inside_Frame1,
    width=5,
    textvariable=id_var,
    bg="#808080",
    fg="#FFFFFF"
)
id_entry.grid(row=0, column=1, padx=5, pady=5)

name_label = Label(Inside_Frame1, text="Nombre")
name_label.grid(row=1, column=0, padx=5, pady=5)
name_var = StringVar()
name_entry = Entry(Inside_Frame1, width=30, textvariable=name_var)
name_entry.grid(row=1, column=1, padx=5, pady=5)

surname_label = Label(Inside_Frame1, text="Apellido")
surname_label.grid(row=2, column=0, padx=5, pady=5)
surname_var = StringVar()
surname_entry = Entry(Inside_Frame1, width=30, textvariable=surname_var)
surname_entry.grid(row=2, column=1, padx=5, pady=5)

number_label = Label(Inside_Frame1, text="Numero")
number_label.grid(row=3, column=0, padx=5, pady=5)
number_var = StringVar()
number_entry = Entry(Inside_Frame1, width=30, textvariable=number_var)
number_entry.grid(row=3, column=1, padx=5, pady=5)

Frame2 = Frame(window)
Frame2.grid(row=0, column=1, padx=15, pady=15, sticky=E)

Add_button = Button(
    Frame2,
    text="Agregar contacto",
    width=15,
    bg="#6B69D6",
    fg="#FFFFFF",
    command=lambda: addcontact(),
)
Add_button.grid(row=0, column=0, padx=8, pady=8)

Update_button = Button(
    Frame2,
    text="Actualizar contacto",
    width=15,
    bg="#6B69D6",
    fg="#FFFFFF",
    command=updatecontact
)
Update_button.grid(row=1, column=0, padx=8, pady=8)

Reset_button = Button(
    Frame2,
    text="Reiniciar",
    width=15,
    bg="#6B69D6",
    fg="#FFFFFF",
    command=reset
)
Reset_button.grid(row=2,column=0,padx=8,pady=8)

displayframe = Frame(window)
displayframe.grid(row=1, column=0, padx=15, pady=15)


tv = ttk.Treeview(displayframe, columns=(1, 2, 3, 4), show="headings", height="4")
tv.column(1, width=20, minwidth=20)
tv.column(2, width=80, minwidth=80)
tv.column(3, width=80, minwidth=80)
tv.column(4, width=100, minwidth=100)
tv.heading(1, text="ID")
tv.heading(2, text="Nombre")
tv.heading(3, text="Apellido")
tv.heading(4, text="Numero")
tv.pack(pady=20)


ActionFrame = Frame(window)
ActionFrame.grid(row=1, column=1, padx=20, pady=20, sticky=E)

Delete_button = Button(
    ActionFrame,
    text="Borrar contacto",
    width=15,
    bg="#D20000",
    fg="#FFFFFF",
    command=deletecontact
)
Delete_button.grid(row=0, column=0, padx=5, pady=5, sticky=S)

Loadbutton = Button(
    ActionFrame,
    text="Actualizar agenda",
    width=15,
    bg="#6B69D6",
    fg="#FFFFFF",
    command=updatelist
)
Loadbutton.grid(row=1, column=0, padx=5, pady=5)

createdb = Button(
    ActionFrame,
    text="Crear BD",
    width=15,
    bg="#008700",
    fg="#FFFFFF",
    command=createbd
)
createdb.grid(row=2, column=0, padx=5, pady=5)

# Asigno al click izquierdo del mouse la funcion "select_record"
# en el treeview.
tv.bind("<ButtonRelease-1>", select_record)

window.mainloop()
