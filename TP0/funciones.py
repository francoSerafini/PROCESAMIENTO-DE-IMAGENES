from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

imagen_tk_original = None
imagen_tk_modificada = None


def cargar_imagen(panel_or, panel_mod):

    global imagen_original, imagen_tk_original
    

    ruta = filedialog.askopenfilename(
        title='Seleccionar imagen',
        filetypes=[('Archivos de imagen', '*.jpg *.jpeg *.png')]
        )
    
    if ruta:
        imagen_original = Image.open(ruta)
        imagen_modificada = imagen_original.copy()

        if imagen_original.height > 960 or imagen_original.width > 540:
            imagen_original = imagen_original.resize((960, 540))
            imagen_modificada = imagen_modificada.resize((960, 540))
            
        imagen_tk_original = ImageTk.PhotoImage(imagen_original)
        imagen_tk_modificada = ImageTk.PhotoImage(imagen_modificada)

        panel_or.configure(width=imagen_original.width, height=imagen_original.height)
        panel_or.create_image(0, 0, anchor='nw', image=imagen_tk_original)
        panel_or.image = imagen_tk_original

        panel_mod.configure(width=imagen_modificada.width, height=imagen_modificada.height)
        panel_mod.create_image(0, 0, anchor='nw', image=imagen_tk_modificada)
        panel_mod.image = imagen_tk_modificada

        return imagen_original, imagen_modificada


def guardar_imagen(imagen_modificada):

    if imagen_modificada is None:
        messagebox.showwarning('Aviso', 'Primero debes cargar una imagen')
        return

    ruta_guardar = filedialog.asksaveasfilename(
        defaultextension='.jpg',
        filetypes=[('PNG', '*.png'), ('JPEG', '*.jpg')]
    )

    if ruta_guardar:
        imagen_modificada.save(ruta_guardar)
        messagebox.showinfo('Exito', 'Imagen guardada')


def cambiar_modo_seleccion(panel_or, panel_mod, boton_activar, var_modo, imagen):

    if imagen is None:
        messagebox.showwarning('Aviso', 'Primero debes cargar una imagen para activar el modo seleccion.')
        return
    
    modo_seleccion = not var_modo.get()
    var_modo.set(modo_seleccion)

    if modo_seleccion:
        boton_activar.configure(text='Seleccion: ACTIVADO', bg='green', fg='white', activebackground='darkgreen')
        panel_or.configure(cursor='cross')
        panel_mod.configure(cursor='cross')
    else:
        boton_activar.configure(text='Activar Seleccion', bg='#d9d9d9', fg='black', activebackground='#ececec')
        panel_or.configure(cursor = 'arrow')
        panel_mod.configure(cursor = 'arrow')



    
