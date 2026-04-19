import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
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
    panel_original.delete('all')

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
        modo_recorte.set(False)
        return
    
    if modo_recorte.get():
        panel_original.configure(cursor='plus')
        txt_herramientas.configure(text='Modo recorte: Seleccione un area en la imagen original.')
    else:
        panel_original.configure(cursor='arrow')
        txt_herramientas.configure(text='Herramienta desactivada')


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

        x_izq = min(inicio_rect_x, fin_rect_x)
        x_der = max(inicio_rect_x, fin_rect_x)
        y_arr = min(inicio_rect_y, fin_rect_y)
        y_aba = max(inicio_rect_y, fin_rect_y)
        area = (x_izq, y_arr, x_der, y_aba)

        if modo_analisis.get():
            panel_original.itemconfig(rect_id, outline='green', width=2)
            analizar_region(imagen_original, area, txt_herramientas)

        else:
            panel_original.delete(rect_id)
            
            if modo_recorte.get():
                nueva_img = copiar_sector_imagen(imagen_original, area, panel_modificado, txt_herramientas)
            
                if nueva_img:
                    imagen_modificada = nueva_img
                activar_modo_recorte()

    rect_id = None
    
     
def realizar_resta():

    global imagen_original, imagen_modificada
    
    resultado = preparar_y_restar(imagen_original, panel_original, panel_modificado, txt_herramientas)
    imagen_modificada = resultado


def activar_modo_analisis():

    if imagen_original is None:
        messagebox.showwarning('Aviso', 'Carga una imagen primero')
        modo_analisis.set(False)
        return
    
    if modo_analisis.get():
        modo_recorte.set(False)
        modo_edicion.set(False)
        panel_original.configure(cursor='sizing')
        txt_herramientas.configure(text='Modo analisis: DIbuje un rectangulo en la zona deseada.')
    else: 
        panel_original.delete('all')
        panel_original.create_image(0, 0, anchor='nw', image=panel_original.image)
        panel_original.configure(cursor='arrow')

def ejecutar_gamma():
    
    global imagen_original, imagen_modificada

    if imagen_original is None:
        messagebox.showwarning('Aviso', 'Carga una imagen primero')
        return

    valor_gamma = simpledialog.askfloat('Transformacion Gamma', 'Ingrse valor Gamma mayor que 0, menor que 2 y distinto de 1')

    if valor_gamma is None: return

    if valor_gamma < 0 or valor_gamma > 2 or valor_gamma == 1:
        messagebox.showerror('Error', 'Ingrese un valor gamma valido')
        return
    
    resultado = funcion_gamma(imagen_original, valor_gamma)

    imagen_modificada = resultado

    global tk_gamma
    tk_gamma = ImageTk.PhotoImage(imagen_modificada)

    panel_modificado.delete('all')
    panel_modificado.configure(width=imagen_modificada.width, height=imagen_modificada.height)
    panel_modificado.create_image(0, 0, anchor='nw', image=tk_gamma)

    txt_herramientas.configure(text=f'Transformacion realizada con gamma {valor_gamma}')

def ejecutar_negativo():

    global imagen_original, imagen_modificada

    if imagen_original is None:
        messagebox.showwarning('Aviso', 'Carga una imagen primero')

    imagen_modificada = aplicar_negativo(imagen_original)

    global tk_negativo
    tk_negativo = ImageTk.PhotoImage(imagen_modificada)

    panel_modificado.delete('all')
    panel_modificado.configure(width=imagen_modificada.width, height=imagen_modificada.height)
    panel_modificado.create_image(0, 0, anchor='nw', image=tk_negativo)

    txt_herramientas.configure(text=f'Negativo aplicado.')


def ejecutar_histograma():

    if imagen_original is None:
        messagebox.showwarning('Aviso', 'Carga una imagen en escala de grises primero.')
        return
    
    frecuencias = obtener_histograma(imagen_original)

    valores = list(frecuencias.keys())
    conteo = list(frecuencias.values())

    plt.figure(figsize=(8, 5))
    plt.bar(valores, conteo, color='gray', width=1.0)
    plt.title('Histograma de la imagen original')
    plt.xlabel('Nivel de gris (0-255)')
    plt.ylabel('Cantidad de pixeles')
    plt.xlim([-5, 260])
    plt.grid(axis='y', alpha=0.3)
    plt.show()


def ejecutar_binarizacion():

    global imagen_original, imagen_modificada

    if imagen_original is None:
        messagebox.showwarning('Aviso', 'Carga una imagen en escala de grises primero.')
        return

    umbral = simpledialog.askinteger('UMBRAL', 'Ingrese un umbral entre 0 y 255.')

    if umbral is None: return
    
    if umbral < 0 or umbral > 255:
        messagebox.showerror('ERROR', 'El valor del umbral debe ser entre 0 y 255')
        return

    imagen_modificada = binarizar_imagen(imagen_original, umbral)

    global binarizada_tk
    binarizada_tk = ImageTk.PhotoImage(imagen_modificada)

    panel_modificado.delete('all')
    panel_modificado.configure(width=imagen_modificada.width, height=imagen_modificada.height)
    panel_modificado.create_image(0, 0, anchor='nw', image=binarizada_tk)
    
    txt_herramientas.configure(text=f'Binarizacion aplicada con umbral {umbral}')


def ejecutar_ecualizacion():

    global imagen_original, imagen_modificada
    
    if imagen_original is None:
        messagebox.showwarning('Aviso', 'Carga una imagen en escala de grises primero.')
        return
    
    imagen_modificada = aplicar_ecualizacion(imagen_modificada)

    global tk_ecualizada
    tk_ecualizada = ImageTk.PhotoImage(imagen_modificada)
    panel_modificado.delete('all')
    panel_modificado.create_image(0, 0, anchor='nw', image=tk_ecualizada)

    txt_herramientas.configure(text='Imagen binarizada')
    
barra_menu = tk.Menu(ventana)
ventana.configure(menu=barra_menu)

menu_archivo = tk.Menu(barra_menu, tearoff=0)
barra_menu.add_cascade(label='Archivo', menu=menu_archivo)
menu_archivo.add_command(label='Cargar Imagen', command=cambiar_modo_imagen)
menu_archivo.add_command(label='Guardar como...', command=lambda: guardar_imagen(imagen_modificada))
menu_archivo.add_separator()
menu_archivo.add_command(label='Salir', command=ventana.quit)

menu_operadores = tk.Menu(barra_menu, tearoff=0)
barra_menu.add_cascade(label='Operadores', menu=menu_operadores)
menu_operadores.add_command(label='Restar imagenes', command=realizar_resta)
menu_operadores.add_command(label='Transformacion Gamma', command=ejecutar_gamma)
menu_operadores.add_command(label='Aplicar negativo', command=ejecutar_negativo)
menu_operadores.add_command(label='Binarizar imagen', command=ejecutar_binarizacion)
menu_operadores.add_command(label='Ecualizar imagen', command=ejecutar_ecualizacion)

menu_herramientas = tk.Menu(barra_menu, tearoff=0)
barra_menu.add_cascade(label='Herramientas', menu=menu_herramientas)
menu_herramientas.add_checkbutton(label='Modo seleccion (Pixel)', variable=modo_seleccion, command=lambda: cambiar_modo_seleccion(panel_original, panel_modificado, modo_seleccion, imagen_original))
menu_herramientas.add_command(label='Cambiar color pixel', command=activar_modo_edicion)
menu_herramientas.add_separator()
menu_herramientas.add_checkbutton(label='Recortar region', variable=modo_recorte, command=activar_modo_recorte)
menu_herramientas.add_checkbutton(label='Analizar region', variable=modo_analisis, command=activar_modo_analisis)
menu_herramientas.add_command(label='Generar Histograma', command=ejecutar_histograma)


txt_herramientas = tk.Label(ventana, text='Elige una herramienta', font=('Arial', 10))
txt_herramientas.pack(pady=10)

panel_modificado.bind('<Button-1>', manejar_clic_modificado)

panel_original.bind('<ButtonPress-1>', empezar_seleccion)
panel_original.bind('<B1-Motion>', arrastrar_seleccion)
panel_original.bind('<ButtonRelease-1>', finalizar_seleccion)


ventana.mainloop()