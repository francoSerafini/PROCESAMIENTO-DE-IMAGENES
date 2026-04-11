import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
from funciones import cargar_imagen, guardar_imagen, obtener_valor_pixel, cambiar_modo_seleccion

ventana = tk.Tk()
ventana.title('TP0')
ventana.geometry('1920x1080')

imagen = None
modo_seleccion = tk.BooleanVar(value=False)

panel = tk.Canvas(ventana, bg='gray')
panel.pack(pady=10)

def cambiar_modo_imagen():
    global imagen
    imagen = cargar_imagen(panel)

boton_cargar_img = tk.Button(ventana, text='Cargar imagen', command=cambiar_modo_imagen)
boton_cargar_img.pack(pady=5)

boton_guardar_img = tk.Button(ventana, text='Guardar imagen', command=lambda: guardar_imagen(imagen))
boton_guardar_img.pack(pady=5)

boton_activar_seleccion = tk.Button(ventana, text='Activar Seleccion', command = lambda: cambiar_modo_seleccion(ventana, boton_activar_seleccion, modo_seleccion))
boton_activar_seleccion.pack(pady=5)


lbl_color = tk.Label(ventana, text='Elige una herramienta', font=('Arial', 10))
lbl_color.pack(pady=10)
panel.bind('<Button-1>', lambda event: obtener_valor_pixel(event, lbl_color, modo_seleccion, imagen))




ventana.mainloop()