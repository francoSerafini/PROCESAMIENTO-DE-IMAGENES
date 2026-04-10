import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
from funciones import cargar_imagen, guardar_imagen

ventana = tk.Tk()
ventana.title('Ventana')
ventana.geometry('600x400')

imagen = None

panel = tk.Label(ventana, text='No se ha cargado ninguna imagen')
panel.pack(expand=True)

boton_cargar_img = tk.Button(ventana, text='Cargar imagen', command=lambda: cargar_imagen(panel))
boton_cargar_img.pack(pady=10)

boton_guardar_img = tk.Button(ventana, text='Guardar imagen', command=lambda: guardar_imagen(imagen))
boton_guardar_img.pack(pady=10)


ventana.mainloop()