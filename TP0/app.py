import tkinter as tk
from tkinter import messagebox
from funciones import cargar_imagen, guardar_imagen, cambiar_modo_seleccion, cambiar_color_pixel, cambiar_color_por_coordenadas

ventana = tk.Tk()
ventana.title('TP0')
ventana.geometry('1920x1080')

imagen_original = None
imagen_modificada = None

modo_seleccion = tk.BooleanVar(value=False)
modo_edicion = tk.BooleanVar(value=False)

zona_botones = tk.Frame(ventana, pady=10)
zona_botones.pack(side='top', fill='x')

zona_imagenes = tk.Frame(ventana, bg='black')
zona_imagenes.pack(side='top', expand=True, fill='both', padx=10, pady=10)

frame_izq = tk.Frame(zona_imagenes)
frame_izq.pack(side='left', expand=True, fill='both', padx=5)
tk.Label(frame_izq, text='ORIGINAL', font=('Arial', 12, 'bold')).pack()
panel_original = tk.Canvas(frame_izq, bg='gray')
panel_original.pack(expand=True)

frame_der = tk.Frame(zona_imagenes)
frame_der.pack(side='left', expand=True, fill='both', padx=5)
tk.Label(frame_der, text='MODIFICADA', font=('Arial', 12, 'bold')).pack()
panel_modificado = tk.Canvas(frame_der, bg='gray')
panel_modificado.pack(expand=True)


def cambiar_modo_imagen():

    global imagen_original, imagen_modificada
    imagen_or, imagen_mod = cargar_imagen(panel_original, panel_modificado)
    imagen_original, imagen_modificada = imagen_or, imagen_mod



def obtener_valor_pixel(event):

    global imagen_original

    if modo_seleccion.get() and imagen_original:
   
        x, y = event.x, event.y
        valor = imagen_original.getpixel((x, y))

        txt_herramientas.configure(text=f'Coordenadas: {x}, {y} Valor: {valor}')


def activar_modo_edicion():

    if imagen_original is None:
        messagebox.showwarning('Aviso', 'Carga una imagen primero')
        return
    
    ventana_opciones = tk.Toplevel(ventana)
    ventana_opciones.title('Seleccione metodo')
    ventana_opciones.geometry('300x150')
    ventana_opciones.grab_set()

    tk.Label(ventana_opciones, text='Elija metodo de edicion', pady=10).pack()
    
    def modo_mouse():
        modo_edicion.set(True)
        boton_cambiar_pixel.configure(text='Modo mouse: ACTIVO', bg='green')
        panel_modificado.configure(cursor='pencil')
        ventana_opciones.destroy()

    def modo_coordenadas():
        ventana_opciones.destroy()
        cambiar_color_por_coordenadas(imagen_modificada, panel_modificado, txt_herramientas)

    tk.Button(ventana_opciones, text='Tocar con el mouse', command=modo_mouse, width=20).pack(pady=5)
    tk.Button(ventana_opciones, text='Ingresar Coordenadas', command=modo_coordenadas, width=20).pack(pady=5)


def manejar_clic_modificado(event):
    
    if modo_edicion.get():
        cambiar_color_pixel(event, imagen_modificada, panel_modificado, txt_herramientas)


boton_cargar_img = tk.Button(zona_botones, text='Cargar imagen', command=cambiar_modo_imagen)
boton_cargar_img.pack(side='left', padx=10)

boton_guardar_img = tk.Button(zona_botones, text='Guardar imagen modificada', command=lambda: guardar_imagen(imagen_modificada))
boton_guardar_img.pack(side='left', padx=10)

boton_activar_seleccion = tk.Button(zona_botones, text='Activar Seleccion', command = lambda: cambiar_modo_seleccion(panel_original, panel_modificado, boton_activar_seleccion, modo_seleccion, imagen_original))
boton_activar_seleccion.pack(side='left', padx=10)

boton_cambiar_pixel =tk.Button(zona_botones, text='Cambiar color pixel', command=activar_modo_edicion)
boton_cambiar_pixel.pack(side='left', padx=10)


txt_herramientas = tk.Label(ventana, text='Elige una herramienta', font=('Arial', 10))
txt_herramientas.pack(pady=10)

panel_original.bind('<Button-1>', obtener_valor_pixel)
panel_modificado.bind('<Button-1>', manejar_clic_modificado)




ventana.mainloop()