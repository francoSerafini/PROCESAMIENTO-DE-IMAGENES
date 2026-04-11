from tkinter import filedialog, messagebox
from PIL import Image, ImageTk


def cargar_imagen(panel):
    global imagen, imagen_tk
    ruta = filedialog.askopenfilename(
        title='Seleccionar imagen',
        filetypes=[('Archivos de imagen', '*.jpg *.jpeg *.png *bmp')]
        )
    
    if ruta:
        imagen = Image.open(ruta)

        if imagen.height > 1920 or imagen.width > 1080:
            imagen = imagen.resize((1280, 720))
            
        imagen_tk = ImageTk.PhotoImage(imagen)
        panel.configure(width=imagen.width, height=imagen.height)
        panel.create_image(0, 0, anchor='nw', image=imagen_tk)
        panel.image = imagen_tk
        return imagen


def guardar_imagen(imagen):

    if imagen is None:
        messagebox.showwarning('Aviso', 'Primero debes cargar una imagen')
        return

    ruta_guardar = filedialog.asksaveasfilename(
        defaultextension='.jpg',
        filetypes=[('PNG', '*.png'), ('JPEG', '*.jpg')]
    )

    if ruta_guardar:
        imagen.save(ruta_guardar)
        messagebox.showinfo('Exito', 'Imagen guardada')


def cambiar_modo_seleccion(panel, boton_activar, var_modo):

    modo_seleccion = not var_modo.get()
    var_modo.set(modo_seleccion)

    if modo_seleccion:
        boton_activar.configure(text='Seleccion: ACTIVADO', bg='green', fg='white')
        panel.configure(cursor='cross')
    else:
        boton_activar.configure(text='Activar Seleccion', bg='SystemButtonFace')
        panel.configure(cursor = 'arrow')


def obtener_valor_pixel(event, lbl_color, modo_seleccion, imagen):

    if modo_seleccion.get() and imagen:
   
        x, y = event.x, event.y
        valor = imagen.getpixel((x, y))

        lbl_color.configure(text=f'Coordenadas: {x}, {y} Valor: {valor}')


    
