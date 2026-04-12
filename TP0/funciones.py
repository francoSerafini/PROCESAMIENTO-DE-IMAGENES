from tkinter import filedialog, messagebox, simpledialog
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


def cambiar_color_pixel(event, imagen, panel_mod, lbl_info):

    if imagen is None:
        messagebox.showwarning('Aviso', 'Primero debes cargar una imagen para usar esta funcion.')
        return

    x, y = event.x, event.y
    
    rojo = simpledialog.askinteger('Input', 'Valor Rojo (0-255):', minvalue=0, maxvalue=255)
    if rojo is None: return

    verde = simpledialog.askinteger('Input', 'Valor Verde (0-255):', minvalue=0, maxvalue=255)
    if verde is None: return

    azul = simpledialog.askinteger('Input', 'Valor Azul (0-255)', minvalue=0, maxvalue=255)
    if azul is None: return

    nuevo_color = (rojo, verde, azul)

    imagen.putpixel((x, y), nuevo_color)

    nueva_imagen_tk = ImageTk.PhotoImage(imagen)
    panel_mod.create_image(0, 0, anchor='nw', image=nueva_imagen_tk)
    panel_mod.image = nueva_imagen_tk

    lbl_info.config(text=f'Pixel en ({x}, {y}) cambiado a {nuevo_color}')

def cambiar_color_por_coordenadas(imagen, panel_mod, lbl_info):

    if imagen is None: return

    x = simpledialog.askinteger('Input', f'Coordenada X (0-{imagen.width-1}):', minvalue=0, maxvalue=imagen.width-1)
    if x is None: return

    y = simpledialog.askinteger('Input', f'Coordenada Y (0-{imagen.height-1}):', minvalue=0, maxvalue=imagen.height-1)
    if y is None: return

    rojo = simpledialog.askinteger('Input', 'Rojo (0-255):', minvalue=0, maxvalue=255)
    if rojo is None: return

    verde = simpledialog.askinteger('Input', 'Verde (0-255)', minvalue=0, maxvalue=255)
    if verde is None: return

    azul = simpledialog.askinteger('Input', 'Azul (0-255)', minvalue=0, maxvalue=255)
    if azul is None: return

    nuevo_color = (rojo, verde, azul)

    imagen.putpixel((x, y), nuevo_color)

    nueva_imagen_tk = ImageTk.PhotoImage(imagen)
    panel_mod.create_image(0, 0, anchor='nw', image=nueva_imagen_tk)
    panel_mod.image = nueva_imagen_tk

    lbl_info.config(text=f'Pixel en ({x}, {y}) cambiado a {nuevo_color}')
    

def copiar_sector_imagen(img_original, area, panel_mod, lbl_info):

    img_recortada = img_original.crop(area)

    global recorte_tk
    recorte_tk = ImageTk.PhotoImage(img_recortada)

    panel_mod.delete('all')
    panel_mod.configure(width=img_recortada.width, height=img_recortada.height)
    panel_mod.create_image(0, 0, anchor='nw', image=recorte_tk)
    panel_mod.image = recorte_tk

    lbl_info.configure(text=f'Sector recortado: {img_recortada.width}x{img_recortada.height}')
    
    return img_recortada


    
