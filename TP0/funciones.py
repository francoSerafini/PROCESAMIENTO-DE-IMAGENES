from tkinter import filedialog, messagebox, simpledialog
from PIL import Image, ImageTk
import numpy as np

imagen_tk_original = None
imagen_tk_modificada = None


def cargar_raw(ruta, ancho, alto, profundidad='unit8'):
    
    with open(ruta, 'rb') as f:
        datos = np.fromfile(f, dtype=profundidad)

    matriz = datos.reshape((alto, ancho))
    return Image.fromarray(matriz)

def cargar_imagen(panel_or, panel_mod):

    global imagen_original, imagen_tk_original
    

    ruta = filedialog.askopenfilename(
        title='Seleccionar imagen',
        filetypes=[('Archivos de imagen', '*.jpg *.jpeg *.png *.RAW')]
        )
    
    extension, nombre = ruta.lower().split('.')[-1], ruta.lower().split('/')[-1]

    if extension == 'raw':
        ancho = simpledialog.askinteger('Configuracion RAW', f'Ancho img {nombre} (px):')
        alto = simpledialog.askinteger('Configuracion RAW', f'Alto img {nombre} (px)')

        if not ancho or not alto: return

        with open(ruta, 'rb') as f:
            datos = np.fromfile(f, dtype=np.uint8)
            matriz = datos.reshape((alto, ancho))
            imagen_original = Image.fromarray(matriz)
    
    else:
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
        defaultextension='.png',
        filetypes=[('PNG', '*.png'), ('JPEG', '*.jpg')]
    )

    if ruta_guardar:
        imagen_modificada.save(ruta_guardar)
        messagebox.showinfo('Exito', 'Imagen guardada')


def cambiar_modo_seleccion(panel_or, panel_mod, var_modo, imagen):

    if imagen is None:
        messagebox.showwarning('Aviso', 'Primero debes cargar una imagen para activar el modo seleccion.')
        var_modo.set(False)
        return
    
    if var_modo.get():
        panel_or.configure(cursor='cross')
        panel_mod.configure(cursor='cross')
    else:
        panel_mod.configure(cursor='arrow')
        panel_or.configure(cursor='arrow')

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


def preparar_y_restar(img1, panel_or, panel_mod, lbl_info):

    if img1 is None: 
        messagebox.showwarning('Aviso', 'Carga la primer imagen.')
        return None

    ruta_img2 = filedialog.askopenfilename(title='Seleccione la segunda imagen para restar.', filetypes=[('JPEG', '*.jpg') ,('PNG', '*.png')])
    img2 = Image.open(ruta_img2)

    if img1.size != img2.size:
        opcion = messagebox.askyesnocancel(
            'Dimensiones diferentes',
            'Redimensionar la mas grande? (SI)\n'
            'Rellenar con ceros la mas chica (NO)'
        )
    
        if opcion is True:
            if img1.width * img1.height > img2.width * img2.height:
                img1 = img1.resize(img2.size)
            else:
                img2 = img2.resize(img1.size)
        elif opcion is False:
            nuevo_ancho = max(img1.width, img2.width)
            nuevo_alto = max(img1.height, img2.height)

            aux1 = Image.new(img1.mode, (nuevo_ancho, nuevo_alto), 0)
            aux2 = Image.new(img2.mode, (nuevo_ancho, nuevo_alto), 0)
            aux1.paste(img1, (0,0))
            aux2.paste(img2, (0,0))
            img1, img2 = aux1, aux2
        else:
            return None
    
    global tk_img1, tk_img2
    tk_img1 = ImageTk.PhotoImage(img1)
    tk_img2 = ImageTk.PhotoImage(img2)

    panel_or.delete('all')
    panel_or.configure(width=img1.width, height=img1.height)
    panel_or.create_image(0, 0, anchor='nw', image=tk_img1)
    panel_or.image = tk_img1

    panel_mod.delete('all')
    panel_mod.configure(width=img2.width, height=img2.height)
    panel_mod.create_image(0, 0, anchor='nw', image=tk_img2)

    lbl_info.configure(text='Imagenes listas. Presione Aceptar para restar.')

    if messagebox.askokcancel('Operacion', 'Restar imagenes?'):
        arr1= np.array(img1, dtype=np.int16)
        arr2 = np.array(img2, dtype=np.int16)

        resta_arr = arr1 - arr2
        min_resta, max_resta = np.min(resta_arr), np.max(resta_arr)
        resta_arr = ((resta_arr - min_resta) / (max_resta - min_resta)) * 255
        resta_arr = resta_arr.astype(np.uint8)
        img_resta = Image.fromarray(resta_arr)

        panel_or.delete('all')
        panel_or.configure(width=1, height=1)

        global tk_res
        tk_res = ImageTk.PhotoImage(img_resta)
        panel_mod.configure(width=img_resta.width, heigh=img_resta.height)
        panel_mod.create_image(0, 0, anchor='nw', image=tk_res)
        panel_mod.image = tk_res

        lbl_info.configure(text='Resultado de la resta.')
        return img_resta

    return None


def analizar_region(imagen, area, lbl_info):

    region = imagen.crop(area)
    ancho, alto = region.size
    total_pixels = ancho * alto
    
    if total_pixels == 0:
        return
    
    datos = np.array(region)

    if len(datos.shape) == 3:

        promedios = np.mean(datos, axis=(0, 1))
        r_prom = round(promedios[0], 2)
        v_prom = round(promedios[1], 2)
        a_prom = round(promedios[2], 2)

        resultado = (f'Region: {ancho}x{alto} - Total px: {total_pixels}\n'
                     f'Promedio color -> R: {r_prom}, V: {v_prom}, A: {a_prom}')
    
    else: 
        
        promedio_gris = round(np.mean(datos), 2)
        resultado = (f'Region: {ancho}x{alto} - Total px: {total_pixels}\n'
                     f'Promedio gris: {promedio_gris}')
    
    lbl_info.configure(text=resultado)


def funcion_gamma(imagen, gamma):

    c = 255 / (255**gamma)
    
    arr_imagen = np.array(imagen)

    if len(arr_imagen.shape) == 2:
        for x in range(arr_imagen.shape[0]):
            for y in range(arr_imagen.shape[1]):
                
                r = arr_imagen[x][y]
                arr_imagen[x][y] = c*(r**gamma)
    
    else:
        for x in range(arr_imagen.shape[0]):
            for y in range(arr_imagen.shape[1]):
                for canal in range(arr_imagen.shape[2]):
                    rcanal = arr_imagen[x][y][canal]
                    arr_imagen[x][y][canal] = c*(rcanal**gamma)
    
    imagen_transformada = Image.fromarray(arr_imagen)
    return imagen_transformada


def aplicar_negativo(imagen):

    arr_imagen = np.array(imagen)

    if len(arr_imagen.shape) == 2:
        for x in range(arr_imagen.shape[0]):
            for y in range(arr_imagen.shape[1]):
                
                arr_imagen[x][y] = 255 - arr_imagen[x][y]
    
    else:
        for x in range(arr_imagen.shape[0]):
            for y in range(arr_imagen.shape[1]):
                for canal in range(arr_imagen.shape[2]):

                    arr_imagen[x][y][canal] = 255 - arr_imagen[x][y][canal]
    
    imagen_negativa = Image.fromarray(arr_imagen)
    return imagen_negativa


def obtener_histograma(imagen):

    arr_imagen = np.array(imagen)
    cant_valores_unicos = np.unique(arr_imagen, return_counts=True)
    frecuencias = dict(zip(cant_valores_unicos[0], cant_valores_unicos[1]))

    return frecuencias


def binarizar_imagen(imagen, umbral):

    arr_iamgen = np.array(imagen)

    for x in range(arr_iamgen.shape[0]):
        for y in range(arr_iamgen.shape[1]):
            
            r = arr_iamgen[x][y]

            if r >= umbral:
                arr_iamgen[x][y] = 255
            else:
                arr_iamgen[x][y] = 0
    
    imagen_binarizada = Image.fromarray(arr_iamgen)
    return imagen_binarizada


    