import tkinter as tk
from tkinter import messagebox
from funciones import *

ventana = tk.Tk()
ventana.title('TP0')
ventana.geometry('1920x1080')

imagen_original = None
imagen_modificada = None

rect_id = None
inicio_rect_x = None
inicio_rect_y =None

modo_seleccion = tk.BooleanVar(value=False)
modo_edicion = tk.BooleanVar(value=False)
modo_recorte = tk.BooleanVar(value=False)
modo_analisis = tk.BooleanVar(value=False)

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


def activar_modo_recorte():

    if imagen_original is None:
        messagebox.showwarning('Aviso', 'Carga una imagen primero')
        return

    modo_recorte.set(not modo_recorte.get())

    if modo_recorte.get():
        boton_recorte.configure(bg='green', fg='white', text='Modo recorte activado')
        panel_original.configure(cursor='plus')
    else:
        boton_recorte.configure(bg="#d9d9d9", fg='black', text='Copiar sector')
        panel_original.configure(cursor='arrow')


def empezar_seleccion(event):

    global inicio_rect_x, inicio_rect_y, rect_id

    if modo_seleccion.get() and imagen_original:
        x, y = event.x, event.y
        valor = imagen_original.getpixel((x, y))

        txt_herramientas.configure(text=f'Coordenadas: {x}, {y} Valor: {valor}')

    if modo_recorte.get() or modo_analisis.get():
        inicio_rect_x, inicio_rect_y = event.x, event.y
        rect_id = panel_original.create_rectangle(inicio_rect_x, inicio_rect_y, inicio_rect_x, inicio_rect_y, outline='red', width=2)


def arrastrar_seleccion(event):

    global rect_id

    if modo_recorte.get() or modo_analisis.get() and rect_id:
        nuevo_x, nuevo_y = event.x, event.y
        panel_original.coords(rect_id, inicio_rect_x, inicio_rect_y, nuevo_x, nuevo_y)


def finalizar_seleccion(event):

    global imagen_modificada, rect_id, inicio_rect_x, inicio_rect_y

    if rect_id is not None:
        fin_rect_x, fin_rect_y = event.x, event.y

        panel_original.delete(rect_id)
        rect_id = None

        x_izq = min(inicio_rect_x, fin_rect_x)
        x_der = max(inicio_rect_x, fin_rect_x)
        y_arr = min(inicio_rect_y, fin_rect_y)
        y_aba = max(inicio_rect_y, fin_rect_y)
        area = (x_izq, y_arr, x_der, y_aba)

        if modo_recorte.get():
            nueva_img = copiar_sector_imagen(imagen_original, area, panel_modificado, txt_herramientas)

            if nueva_img:
                imagen_modificada = nueva_img
            
            activar_modo_recorte()
        
        elif modo_analisis.get():
            analizar_region(imagen_original, area, txt_herramientas)
            activar_modo_analisis()


def realizar_resta():

    global imagen_original, imagen_modificada
    
    resultado = preparar_y_restar(imagen_original, panel_original, panel_modificado, txt_herramientas)
    imagen_modificada = resultado


def activar_modo_analisis():

    if imagen_original is None:
        messagebox.showwarning('Aviso', 'Carga una imagen primero')
        return

    modo_recorte.set(False)
    modo_edicion.set(False)
    modo_analisis.set(not modo_analisis.get())

    if modo_analisis.get():
        boton_analisis.configure(bg='green', fg='white', text='Modo analisis activado')
        panel_original.configure(cursor='sizing')
    else:
        boton_analisis.configure(bg='#d9d9d9', fg='black', text='Analizar region')
        panel_original.configure(cursor='arrow')


boton_cargar_img = tk.Button(zona_botones, text='Cargar imagen', command=cambiar_modo_imagen)
boton_cargar_img.pack(side='left', padx=10)

boton_guardar_img = tk.Button(zona_botones, text='Guardar imagen modificada', command=lambda: guardar_imagen(imagen_modificada))
boton_guardar_img.pack(side='left', padx=10)

boton_activar_seleccion = tk.Button(zona_botones, text='Activar Seleccion', command = lambda: cambiar_modo_seleccion(panel_original, panel_modificado, boton_activar_seleccion, modo_seleccion, imagen_original))
boton_activar_seleccion.pack(side='left', padx=10)

boton_cambiar_pixel =tk.Button(zona_botones, text='Cambiar color pixel', command=activar_modo_edicion)
boton_cambiar_pixel.pack(side='left', padx=10)

boton_recorte = tk.Button(zona_botones, text='Copiar sector', command=activar_modo_recorte)
boton_recorte.pack(side='left', padx=10)

boton_restar = tk.Button(zona_botones, text='Restar imagenes', command=realizar_resta)
boton_restar.pack(side='left', padx=10)

boton_analisis = tk.Button(zona_botones, text='Analizar region', command=activar_modo_analisis)
boton_analisis.pack(side='left', padx=10)

txt_herramientas = tk.Label(ventana, text='Elige una herramienta', font=('Arial', 10))
txt_herramientas.pack(pady=10)

panel_modificado.bind('<Button-1>', manejar_clic_modificado)

panel_original.bind('<ButtonPress-1>', empezar_seleccion)
panel_original.bind('<B1-Motion>', arrastrar_seleccion)
panel_original.bind('<ButtonRelease-1>', finalizar_seleccion)


ventana.mainloop()