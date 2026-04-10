from tkinter import filedialog, messagebox
from PIL import Image, ImageTk


def cargar_imagen(ventana):
    global imagen
    ruta = filedialog.askopenfilename(
        title='Seleccionar imagen',
        filetypes=[('Archivos de imagen', '*.jpg *.jpeg *.png *bmp')]
        )
    
    if ruta:
        imagen = Image.open(ruta)
        imagen = imagen.resize((300, 300))
        imagen_tk = ImageTk.PhotoImage(imagen)
    
    ventana.configure(image=imagen_tk)
    ventana.image = imagen_tk

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

