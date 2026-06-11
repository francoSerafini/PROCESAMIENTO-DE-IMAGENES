from tkinter import filedialog, messagebox, simpledialog
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
import numpy as np
import random

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
        filetypes=[('Archivos de imagen', '*.jpg *.jpeg *.png *.RAW *xcf')]
    )
    
    if not ruta: return None, None

    partes = ruta.split('.')
    extension = partes[-1].lower()
    nombre = ruta.split('/')[-1]

    if extension == 'raw':
        ancho_raw = simpledialog.askinteger('Configuracion RAW', f'Ancho img {nombre} (px):')
        alto_raw = simpledialog.askinteger('Configuracion RAW', f'Alto img {nombre} (px):')

        if not ancho_raw or not alto_raw: return None, None

        with open(ruta, 'rb') as f:
            datos = np.fromfile(f, dtype=np.uint8)
            matriz = datos.reshape((alto_raw, ancho_raw))
            imagen_original = Image.fromarray(matriz)
    else:
        imagen_original = Image.open(ruta)
    
    # Límites máximos basados en la pantalla
    max_ancho_pantalla = panel_or.winfo_toplevel().winfo_screenwidth() - 100
    max_alto_pantalla = panel_or.winfo_toplevel().winfo_screenheight() - 200
    max_ancho_por_panel = max_ancho_pantalla // 2

    # =========================================================================
    # NUEVA LÓGICA DE ESCALADO CONDICIONAL
    # =========================================================================
    # Solo calculamos la escala si la imagen desborda el panel horizontal o verticalmente
    if imagen_original.width > max_ancho_por_panel or imagen_original.height > max_alto_pantalla:
        factor_ancho = max_ancho_por_panel / imagen_original.width
        factor_alto = max_alto_pantalla / imagen_original.height
        factor_escala = min(factor_ancho, factor_alto)
    else:
        # Si es más chica que los límites, no se toca (escala 1:1)
        factor_escala = 1.0

    # Si el factor es 1.0, el tamaño final va a ser el mismo que el original
    nuevo_ancho = int(imagen_original.width * factor_escala)
    nuevo_alto = int(imagen_original.height * factor_escala)
        
    # Solo llamamos a resize si realmente cambió el tamaño (factor_escala < 1.0)
    if factor_escala < 1.0:
        imagen_original = imagen_original.resize((nuevo_ancho, nuevo_alto), Image.Resampling.LANCZOS)
    # =========================================================================

    imagen_modificada = imagen_original.copy()
        
    imagen_tk_original = ImageTk.PhotoImage(imagen_original)
    imagen_tk_modificada = ImageTk.PhotoImage(imagen_modificada)

    panel_or.configure(width=imagen_original.width, height=imagen_original.height)
    panel_or.delete('all') 
    panel_or.create_image(0, 0, anchor='nw', image=imagen_tk_original)
    panel_or.image = imagen_tk_original

    panel_mod.configure(width=imagen_modificada.width, height=imagen_modificada.height)
    panel_mod.delete('all')
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

    for x in range(arr_imagen.shape[0]):
        for y in range(arr_imagen.shape[1]):
            
            r = arr_imagen[x][y]
            arr_imagen[x][y] = c*(r**gamma)
        
    imagen_transformada = Image.fromarray(arr_imagen)
    return imagen_transformada


def aplicar_negativo(imagen):

    arr_imagen = np.array(imagen)

    for x in range(arr_imagen.shape[0]):
        for y in range(arr_imagen.shape[1]):
            
            arr_imagen[x][y] = 255 - arr_imagen[x][y]
        
    imagen_negativa = Image.fromarray(arr_imagen)
    return imagen_negativa


def obtener_histograma(imagen):

    arr_imagen = np.array(imagen)
    total_pixeles = arr_imagen.size
    cant_valores_unicos = np.unique(arr_imagen, return_counts=True)
    frecuencias_relativas = cant_valores_unicos[1] / total_pixeles
    frecuencias = dict(zip(cant_valores_unicos[0], frecuencias_relativas))

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


def obtener_prob_y_norm(valor, suma, s_min, total_pixeles):

    prob = valor / total_pixeles
    s_k = prob + suma
    if s_min == 0 and s_k != 0: s_min = s_k
    s_k_norm = 255 * ((s_k- s_min) / (1 - s_min))

    return s_k, round(s_k_norm), s_min


def aplicar_ecualizacion(imagen):

    frecuencias = obtener_histograma(imagen)
    arr_imagen = np.array(imagen)
    acum = 0
    s_min = 0
    total_pixeles = sum(frecuencias.values())
    tabla = {}

    for i in range(256):

        frecuencia = frecuencias.get(i, 0)

        acum, s_k_norm, s_min = obtener_prob_y_norm(frecuencia, acum, s_min, total_pixeles)
        tabla[i] = s_k_norm
    
    for x in range(arr_imagen.shape[0]):
        for y in range(arr_imagen.shape[1]):
            
            nivel_gris = arr_imagen[x][y]
            arr_imagen[x][y] = tabla[nivel_gris]
    
    return Image.fromarray(arr_imagen)


def generar_datos_gauss(mu, sigma, cant=10000, graficar_distribucion=False):

    datos_gauss = np.random.normal(mu, sigma, cant)

    if graficar_distribucion:

        plt.figure(figsize=(8, 5))
        plt.hist(datos_gauss, bins=50, color='skyblue', edgecolor='black', alpha=0.7)
        plt.title(f'Distribucion Gaussiana mu={mu}, sigma={sigma}')
        plt.xlabel('Numeros')
        plt.ylabel('Densidad')
        plt.show()
    
    return datos_gauss

#generar_datos_gauss(0, 5, 10000, True)

def generar_datos_exponecial(lambd, cant=10000, graficar_distribucion=False):

    datos_exp = np.random.exponential(1/lambd, cant)

    if graficar_distribucion:

        plt.figure(figsize=(8,5))
        plt.hist(datos_exp, bins=50, color='skyblue', edgecolor='black', alpha=0.7)
        plt.title(f'Distribucion exponencial lambda {lambd}')
        plt.xlabel('Numeros')
        plt.ylabel('Densidad')
        plt.show()

    return datos_exp

#generar_datos_exponecial(3, 10000, True)

def contaminar_ruido_gaus(imagen, porcentaje, sigma):

    arr_imagen = np.array(imagen).astype(np.float64)
    filas, columnas = arr_imagen.shape 
    cant_pixeles = filas * columnas
    cant_a_contaminar = int(cant_pixeles * (porcentaje / 100))

    coord_posibles = np.argwhere(np.ones(arr_imagen.shape))

    indices = np.random.choice(len(coord_posibles), cant_a_contaminar, replace=False)
    seleccionadas = coord_posibles[indices]

    datos_gauss = generar_datos_gauss(0, sigma, cant_a_contaminar)

    for i in range(cant_a_contaminar):
        fila, col = seleccionadas[i][0], seleccionadas[i][1]
        arr_imagen[fila][col] += datos_gauss[i]
        
    arr_imagen = np.clip(arr_imagen, 0, 255).astype(np.uint8)

    imagen_contaminada = Image.fromarray(arr_imagen)

    return imagen_contaminada
    

def contaminar_ruido_exponencial(imagen, porcentaje, lambd):

    arr_imagen = np.array(imagen).astype(np.float64)
    filas, columnas = arr_imagen.shape
    cant_pixeles = filas * columnas
    cant_a_contaminar = int(cant_pixeles * (porcentaje/100))

    coord_posibles = np.argwhere(np.ones(arr_imagen.shape))
    
    indices = np.random.choice(len(coord_posibles), cant_a_contaminar, replace=False)
    seleccionadas = coord_posibles[indices]

    datos_exp = generar_datos_exponecial(lambd, cant_a_contaminar)

    for i in range(cant_a_contaminar):
        fila, col = seleccionadas[i][0], seleccionadas[i][1]
        arr_imagen[fila][col] = arr_imagen[fila][col] * datos_exp[i]
    
    arr_imagen = np.clip(arr_imagen, 0, 255).astype(np.uint8)

    imagen_contaminada = Image.fromarray(arr_imagen)

    return imagen_contaminada


def contaminar_sal_pim(imagen, p):

    arr_imagen = np.array(imagen)
    
    for fila in range(arr_imagen.shape[0]):
        for col in range(arr_imagen.shape[1]):
            
            x = np.random.random()
            
            if x <= p:
                arr_imagen[fila][col] = 0
            
            elif x > 1-p:
                arr_imagen[fila][col] = 255
    
    imagen_contaminada = Image.fromarray(arr_imagen)
    return imagen_contaminada


def tomar_valores_vecindad(matriz, radio, x, y):

    valores = np.array([])

    for filas in range((x-radio), (x+radio+1)):
        for col in range((y-radio), (y+radio+1)):
            
            valores = np.append(valores, matriz[filas][col])

    return valores


def tomar_valores_vecindad_b(matriz, radio, x, y):

    return matriz[x - radio : x + radio + 1, y - radio : y + radio + 1]


def pedir_entero_inpar():

    while True:
        valor = simpledialog.askinteger('Tam. filtro', 'Ingrese un numero entero impar:')
    
        if valor is None:
            return None

        if valor % 2 != 0:
            return valor
        
        else:
            messagebox.showerror('Error', f'El numero {valor}, es par, ingrese un numero impar.')


def aplicar_filtro_media(imagen, tam_fil):

    arr_img = np.array(imagen)
    filas, col = arr_img.shape
    img_filtrada = arr_img.copy()
    radio = int((tam_fil - 1) / 2)
    peso = 1  / (tam_fil**2)

    total_filas = (filas - radio) - radio
    contador_filas = 0

    print(f'Inicio filtrado de media ({tam_fil}x{tam_fil})...')

    for x in range(radio, (filas - radio)):
        for y in range(radio, (col - radio)):
            
            vecindad = tomar_valores_vecindad(arr_img, radio, x, y)
            nuevo_valor = (vecindad * peso).sum()
            img_filtrada[x][y] = int(nuevo_valor)
        
        contador_filas += 1
        porcetaje = (contador_filas / total_filas) * 100
        
        print(f'\rProgreso: {porcetaje:.2f}%', end="")
    
    print('\nFiltrado completado.')
    
    return Image.fromarray(img_filtrada)
    

def aplicar_filtro_mediana(imagen, tam_filtro):

    arr_imagen = np.array(imagen)
    filas, col = arr_imagen.shape
    img_filtrada = arr_imagen.copy()
    radio = int((tam_filtro-1) / 2)
    
    total_filas = (filas - radio) - radio
    contador_filas = 0

    print(f'Inicio de filtrado mediana ({tam_filtro}x{tam_filtro})')

    for x in range(radio, (filas - radio)):
        for y in range(radio, (col - radio)):

            vecindad = tomar_valores_vecindad(arr_imagen, radio, x, y)
            ind_valor_medio = len(vecindad) // 2
            peso = np.sort(vecindad)[ind_valor_medio]
            img_filtrada[x][y] = peso

        contador_filas += 1
        porcentaje = (contador_filas / total_filas) * 100

        print(f'\rProgreso: {porcentaje:.2f}%', end="")

    print('\nFiltrado completado.')

    return(Image.fromarray(img_filtrada))


def aplicar_filtro_mediana_ponderada(imagen, repeticiones):

    arr_imagen = np.array(imagen)
    filas, col = arr_imagen.shape
    img_filtrada = arr_imagen.copy()
    tam_lado = int(np.sqrt(len(repeticiones)))
    radio = int((tam_lado-1) / 2)
    
    total_filas = (filas - radio) - radio
    contador_filas = 0

    print(f'Inicio de filtrado mediana ponderada')

    for x in range(radio, (filas - radio)):
        for y in range(radio, (col - radio)):

            vecindad = tomar_valores_vecindad(arr_imagen, radio, x, y)
            vecindad_rep = np.repeat(vecindad, repeticiones)
            vecindad_ordenada = np.sort(vecindad_rep)
            ind_valor_medio = len(vecindad_rep) // 2
            img_filtrada[x][y] = vecindad_ordenada[ind_valor_medio]

        contador_filas += 1
        porcentaje = (contador_filas / total_filas) * 100

        print(f'\rProgreso: {porcentaje:.2f}%', end="")

    print('\nFiltrado completado.')

    return(Image.fromarray(img_filtrada))


def tomar_valores_vecindad_y_coord(matriz, radio, x, y):

    valores = np.array([])
    coordenadas = []
    
    for i in range((x-radio), (x+radio+1)):
        for j in range((y-radio), (y+radio+1)):
            
            valores = np.append(valores, matriz[i][j])
            coordenadas.append((i-x, j-y))
    
    return valores, np.array(coordenadas)


def aplicar_fitro_gauss(imagen, desviacion):

    arr_imagen = np.array(imagen)
    
    k = round(2 * desviacion + 1)
    if k % 2 == 0: k += 1

    filas, col = arr_imagen.shape
    img_filtrada = arr_imagen.copy()
    radio = int((k-1) / 2)

    total_filas = (filas - radio) - radio
    contador_filas = 0

    print(f'Inicio de filtrado Gaussiano ({k}, Sigma={desviacion})')

    for x in range(radio, (filas - radio)):
        for y in range(radio, (col - radio)):

            vecindad, coordenadas = tomar_valores_vecindad_y_coord(arr_imagen, radio, x, y)
           
            exponentes = -(coordenadas[:, 0]**2 + coordenadas[:, 1]**2) / (2 * desviacion**2)
            
            pesos = (1 / (2 * np.pi * desviacion**2)) * np.exp(exponentes) 
            pesos = pesos / np.sum(pesos)

            nuevo_valor = np.sum(vecindad * pesos) 
            
            img_filtrada[x][y] = nuevo_valor           

        contador_filas += 1
        porcentaje = (contador_filas / total_filas) * 100

        print(f'\rProgreso: {porcentaje:.2f}%', end="")

    print('\nFiltrado completado.')

    return(Image.fromarray(img_filtrada))


def aplicar_filtro_realce(imagen, tam_filtro):

    arr_img = np.array(imagen)
    filas, col = arr_img.shape
    img_filtrada = arr_img.copy()
    pesos = np.full((tam_filtro**2), -1)
    ind_valor_medio = (tam_filtro**2) // 2
    pesos[ind_valor_medio] = (tam_filtro**2) - 1
    radio = int((tam_filtro - 1) / 2)
    total_filas = (filas - radio) - radio
    contador_filas = 0

    print(f'Inicio filtrado de realce ({tam_filtro}x{tam_filtro})...')

    for x in range(radio, (filas - radio)):
        for y in range(radio, (col - radio)):
            
            vecindad = tomar_valores_vecindad(arr_img, radio, x, y)
            nuevo_valor = (vecindad * pesos).sum()
            img_filtrada[x][y] = np.clip(nuevo_valor, 0, 255)
        
        contador_filas += 1
        porcetaje = (contador_filas / total_filas) * 100
        
        print(f'\rProgreso: {porcetaje:.2f}%', end="")
    
    print('\nFiltrado completado.')
    
    return Image.fromarray(img_filtrada)   


def aplicar_filtro_prewitt(imagen):

    arr_img = np.array(imagen)
    filas, col = arr_img.shape[:2]
    img_filtrada = arr_img.copy()
    pesos_ver = [-1, -1, -1, 0, 0, 0, 1, 1, 1]
    pesos_hor = [-1, 0, 1, -1, 0, 1, -1, 0, 1]
    radio = 1
    total_filas = (filas - radio) - radio
    contador_filas = 0

    print(f'Inicio filtrado de Prewitt')

    for x in range(radio, (filas - radio)):
        for y in range(radio, (col - radio)):
            
            if len(arr_img.shape) == 3:
                vecindad = tomar_valores_vecindad_b(arr_img, radio, x, y)
                r = vecindad[:, :, 0] 
                g = vecindad[:, :, 1]  
                b = vecindad[:, :, 2]  
                nuevo_valor_ver_r = (r.flatten() * pesos_ver).sum()
                nuevo_valor_ver_g = (g.flatten() * pesos_ver).sum()
                nuevo_valor_ver_b = (b.flatten() * pesos_ver).sum()
                nuevo_valor_hor_r = (r.flatten() * pesos_hor).sum()
                nuevo_valor_hor_g = (g.flatten() * pesos_hor).sum()
                nuevo_valor_hor_b = (b.flatten() * pesos_hor).sum()
                valor_final_r = (np.sqrt(nuevo_valor_ver_r**2 + nuevo_valor_hor_r**2))
                valor_final_g = (np.sqrt(nuevo_valor_ver_g**2 + nuevo_valor_hor_g**2))
                valor_final_b = (np.sqrt(nuevo_valor_ver_b**2 + nuevo_valor_hor_b**2))
                valor_final = [np.clip(valor_final_r, 0, 255), np.clip(valor_final_g, 0, 255), np.clip(valor_final_b, 0, 255)]
                img_filtrada[x][y] = valor_final
            
            else:
                vecindad = tomar_valores_vecindad(arr_img, radio, x, y)

                nuevo_valor_ver = (vecindad * pesos_ver).sum()
                nuevo_valor_hor = (vecindad * pesos_hor).sum()
                valor_final = np.sqrt(nuevo_valor_ver**2 + nuevo_valor_hor**2)
                img_filtrada[x][y] = np.clip(valor_final, 0, 255)
        
        contador_filas += 1
        porcetaje = (contador_filas / total_filas) * 100
        
        print(f'\rProgreso: {porcetaje:.2f}%', end="")
    
    print('\nFiltrado completado.')
    return Image.fromarray(img_filtrada)   


def aplicar_filtro_sobel(imagen):

    arr_img = np.array(imagen)
    filas, col = arr_img.shape[:2]
    img_filtrada = arr_img.copy()
    pesos_ver = [-1, -2, -1, 0, 0, 0, 1, 2, 1]
    pesos_hor = [-1, 0, 1, -2, 0, 2, -1, 0, 1]
    radio = 1
    total_filas = (filas - radio) - radio
    contador_filas = 0

    print(f'Inicio filtrado de Sobel')

    for x in range(radio, (filas - radio)):
        for y in range(radio, (col - radio)):

            vecindad = tomar_valores_vecindad_b(arr_img, radio, x, y)

            if len(arr_img.shape) == 3:
                r = vecindad[:, :, 0]
                g = vecindad[:, :, 1] 
                b = vecindad[:, :, 2]  
                nuevo_valor_ver_r = (r.flatten() * pesos_ver).sum()
                nuevo_valor_ver_g = (g.flatten() * pesos_ver).sum()
                nuevo_valor_ver_b = (b.flatten() * pesos_ver).sum()
                nuevo_valor_hor_r = (r.flatten() * pesos_hor).sum()
                nuevo_valor_hor_g = (g.flatten() * pesos_hor).sum()
                nuevo_valor_hor_b = (b.flatten() * pesos_hor).sum()
                valor_final_r = (np.sqrt(nuevo_valor_ver_r**2 + nuevo_valor_hor_r**2))
                valor_final_g = (np.sqrt(nuevo_valor_ver_g**2 + nuevo_valor_hor_g**2))
                valor_final_b = (np.sqrt(nuevo_valor_ver_b**2 + nuevo_valor_hor_b**2))
                valor_final = [np.clip(valor_final_r, 0, 255), np.clip(valor_final_g, 0, 255), np.clip(valor_final_b, 0, 255)]
                img_filtrada[x][y] = valor_final

            else:        
                vecindad = tomar_valores_vecindad(arr_img, radio, x, y)
                nuevo_valor_ver = (vecindad * pesos_ver).sum()
                nuevo_valor_hor = (vecindad * pesos_hor).sum()
                valor_final = np.sqrt(nuevo_valor_ver**2 + nuevo_valor_hor**2)
                img_filtrada[x][y] = np.clip(valor_final, 0, 255)
        
        contador_filas += 1
        porcetaje = (contador_filas / total_filas) * 100
        
        print(f'\rProgreso: {porcetaje:.2f}%', end="")
    
    print('\nFiltrado completado.')
    
    return Image.fromarray(img_filtrada)


def obtener_matrices_sobel(imagen):

    arr_img = np.array(imagen).astype(np.float64)
    filas, col = arr_img.shape[:2]
    matriz_ver = np.zeros_like(arr_img)
    matriz_hor = np.zeros_like(arr_img)
    pesos_ver = [-1, -2, -1, 0, 0, 0, 1, 2, 1]
    pesos_hor = [-1, 0, 1, -2, 0, 2, -1, 0, 1]
    radio = 1
    total_filas = (filas - radio) - radio
    contador_filas = 0

    print(f'Inicio filtrado de Sobel')

    for x in range(radio, (filas - radio)):
        for y in range(radio, (col - radio)):
            
            vecindad = tomar_valores_vecindad(arr_img, radio, x, y)
            nuevo_valor_ver = (vecindad * pesos_ver).sum()
            nuevo_valor_hor = (vecindad * pesos_hor).sum()
            matriz_ver[x][y] = nuevo_valor_ver
            matriz_hor[x][y] = nuevo_valor_hor
        
        contador_filas += 1
        porcetaje = (contador_filas / total_filas) * 100
        
        print(f'\rProgreso: {porcetaje:.2f}%', end="")
    
    print('\nFiltrado completado.')
    
    return matriz_ver, matriz_hor



def aplicar_metodo_laplaciano(imagen):
    arr_img = np.array(imagen).astype(np.float64)
    filas, col = arr_img.shape
    img_filtrada = np.zeros_like(arr_img)
    matriz = np.zeros_like(arr_img)
    pesos = [0, -1, 0, -1, 4, -1, 0, -1, 0]
    radio = 1
    
    total_filas = filas - 2 * radio
    contador_filas = 0

    print(f'Inicio metodo Laplaciano')

    for x in range(radio, (filas - radio)):
        for y in range(radio, (col - radio)):
            vecindad = tomar_valores_vecindad(arr_img, radio, x, y)
            nuevo_valor = (vecindad * pesos).sum()
            matriz[x][y] = nuevo_valor
        
        contador_filas += 1
        porcentaje = (contador_filas / total_filas) * 100
        print(f'\rProgreso: {porcentaje:.2f}%', end="")
    
    print('\nBuscando cruces por cero...')
    
    for x in range(radio, (filas - radio)):
        for y in range(radio, (col - radio)):

            pixel_actual = matriz[x][y]
            cruce = False

            pixel_derecha = matriz[x][y+1] if (y + 1 < col) else 0

            if (pixel_actual > 0 and pixel_derecha < 0) or (pixel_actual < 0 and pixel_derecha > 0):
                cruce = True
            elif pixel_actual == 0:
                pixel_izquierda = matriz[x][y-1] if (y - 1 >= 0) else 0
                if (pixel_izquierda > 0 and pixel_derecha < 0) or (pixel_izquierda < 0 and pixel_derecha > 0):
                    cruce = True

            if not cruce:
                pixel_abajo = matriz[x+1][y] if (x + 1 < filas) else 0

                if (pixel_actual > 0 and pixel_abajo < 0) or (pixel_actual < 0 and pixel_abajo > 0):
                    cruce = True
                elif pixel_actual == 0:
                    pixel_arriba = matriz[x-1][y] if (x - 1 >= 0) else 0
                    if (pixel_arriba > 0 and pixel_abajo < 0) or (pixel_arriba < 0 and pixel_abajo > 0):
                        cruce = True

            img_filtrada[x][y] = 255 if cruce else 0
    
    print('Filtrado completado.')
    return Image.fromarray(img_filtrada.astype(np.uint8))


def aplicar_metodo_laplaciano_pendiente(imagen, umbral):
    arr_img = np.array(imagen).astype(np.float64)
    filas, col = arr_img.shape
    img_filtrada = np.zeros_like(arr_img)
    matriz = np.zeros_like(arr_img)
    pesos = [0, -1, 0, -1, 4, -1, 0, -1, 0]
    radio = 1
    total_filas = filas - 2 * radio
    contador_filas = 0

    print(f'Inicio metodo Laplaciano')

    for x in range(radio, (filas - radio)):
        for y in range(radio, (col - radio)):
            vecindad = tomar_valores_vecindad(arr_img, radio, x, y)
            nuevo_valor = (vecindad * pesos).sum()
            matriz[x][y] = nuevo_valor
        
        contador_filas += 1
        porcentaje = (contador_filas / total_filas) * 100
        print(f'\rProgreso: {porcentaje:.2f}%', end="")
    

    for x in range(radio, (filas - radio)):
        for y in range(radio, (col - radio)):

            pixel_actual = matriz[x][y]
            cruce = False
            pendiente = 0.0

            pixel_derecha = matriz[x][y+1] if (y + 1 < col) else 0

            if (pixel_actual > 0 and pixel_derecha < 0) or (pixel_actual < 0 and pixel_derecha > 0):
                cruce = True
                pendiente = abs(pixel_actual - pixel_derecha)
            elif pixel_actual == 0:
                pixel_izquierda = matriz[x][y-1] if (y - 1 >= 0) else 0
                if (pixel_izquierda > 0 and pixel_derecha < 0) or (pixel_izquierda < 0 and pixel_derecha > 0):
                    cruce = True
                    pendiente = abs(pixel_izquierda - pixel_derecha) 

            if not cruce:
                pixel_abajo = matriz[x+1][y] if (x + 1 < filas) else 0

                if (pixel_actual > 0 and pixel_abajo < 0) or (pixel_actual < 0 and pixel_abajo > 0):
                    cruce = True
                    pendiente = abs(pixel_actual - pixel_abajo)
                elif pixel_actual == 0:
                    pixel_arriba = matriz[x-1][y] if (x - 1 >= 0) else 0
                    if (pixel_arriba > 0 and pixel_abajo < 0) or (pixel_arriba < 0 and pixel_abajo > 0):
                        cruce = True
                        pendiente = abs(pixel_arriba - pixel_abajo)

            if cruce and pendiente >= umbral:
                img_filtrada[x][y] = 255
            else:
                img_filtrada[x][y] = 0
    
    print('Filtrado completado.')
    return Image.fromarray(img_filtrada.astype(np.uint8))


def aplicar_metodo_laplaciano_gaussiano(imagen, desviacion, umbral):

    arr_img = np.array(imagen).astype(np.float64)

    k= round(4 * desviacion + 1)
    if k % 2 == 0: k += 1

    matriz = np.zeros_like(arr_img)
    img_filtrada = np.zeros_like(arr_img, dtype=np.uint8)


    filas, col = arr_img.shape[:2]
    radio = int((k-1) / 2)
    
    total_filas = (filas - radio) - radio

    contador_filas = 0

    print(f'Inicio metodo Laplaciano del Gaussiano (Filtro de tamaño: {k}x{k})')

    for x in range(radio, (filas - radio)):
        for y in range(radio, (col - radio)):

            vecindad, coordenadas = tomar_valores_vecindad_y_coord(arr_img, radio, x, y)
           
            distancia_cuadrada = coordenadas[:, 0]**2 + coordenadas[:, 1]**2

            exponencial = np.exp(-distancia_cuadrada / (2 * desviacion**2))
            
            parentesis_laplace = (distancia_cuadrada / (desviacion**2)) - 2

            constante = 1 / (2 * np.pi * (desviacion**3))

            pesos = constante * exponencial * parentesis_laplace

            nuevo_valor = np.sum(vecindad * pesos)

            matriz[x][y] = nuevo_valor
        
        contador_filas += 1
        porcentaje_g = (contador_filas / total_filas) * 100
        print(f'\rProgreso: {porcentaje_g:.2f}%', end="")


    for x in range(radio, (filas - radio)):
            for y in range(radio, (col - radio)):

                pixel_actual = matriz[x][y]
                cruce = False
                pendiente = 0.0

                pixel_derecha = matriz[x][y+1] if (y + 1 < col) else 0

                if (pixel_actual > 0 and pixel_derecha < 0) or (pixel_actual < 0 and pixel_derecha > 0):
                    cruce = True
                    pendiente = abs(pixel_actual - pixel_derecha)
                elif pixel_actual == 0:
                    pixel_izquierda = matriz[x][y-1] if (y - 1 >= 0) else 0
                    if (pixel_izquierda > 0 and pixel_derecha < 0) or (pixel_izquierda < 0 and pixel_derecha > 0):
                        cruce = True
                        pendiente = abs(pixel_izquierda - pixel_derecha) 

                if not cruce:
                    pixel_abajo = matriz[x+1][y] if (x + 1 < filas) else 0

                    if (pixel_actual > 0 and pixel_abajo < 0) or (pixel_actual < 0 and pixel_abajo > 0):
                        cruce = True
                        pendiente = abs(pixel_actual - pixel_abajo)
                    elif pixel_actual == 0:
                        pixel_arriba = matriz[x-1][y] if (x - 1 >= 0) else 0
                        if (pixel_arriba > 0 and pixel_abajo < 0) or (pixel_arriba < 0 and pixel_abajo > 0):
                            cruce = True
                            pendiente = abs(pixel_arriba - pixel_abajo)

                if cruce and pendiente >= umbral:
                    img_filtrada[x][y] = 255
                else:
                    img_filtrada[x][y] = 0
        
    print('Filtrado completado.')
    return Image.fromarray(img_filtrada)




def aplicar_difusion_isotropica(imagen, tiempo, lambd):

    arr_img = np.array(imagen).astype(np.float64)
    img_actutal = arr_img.copy()

    filas, columnas = arr_img.shape

    contador_pasos = 0
    pasos = tiempo

    print(f'Inicio difusion Isotropica')

    for i in range(tiempo):

        img_siguiente = img_actutal.copy()

        for x in range(1, filas-1):
            for y in range(1, columnas-1):

                centro = img_actutal[x][y]
                arriba = img_actutal[x-1][y]
                abajo = img_actutal[x+1][y]
                derecha = img_actutal[x][y+1]
                izquierda = img_actutal[x][y-1]

                dif_arriba = arriba - centro
                dif_abajo = abajo - centro
                dif_derecha = derecha - centro
                dif_izquierda = izquierda - centro
                
                nuevo_valor = centro + ((dif_arriba + dif_abajo + dif_derecha + dif_izquierda) * lambd)

                img_siguiente[x][y] = nuevo_valor
    
        contador_pasos += 1
        porcentaje = (contador_pasos / pasos) * 100
        print(f'\rProgreso: {porcentaje:.2f}%', end="")
    
        img_actutal = img_siguiente.copy()
    
    print('\nDifusion completada.')
    
    img_final = np.clip(img_actutal, 0, 255).astype(np.uint8)
    
    return(Image.fromarray(img_final))



def lecrec(derivada, sigma):
    return np.exp(-(derivada**2) / (sigma**2))

def lorentz(derivada, sigma):
    return 1 / ((derivada**2 / sigma**2) + 1)


def aplicar_difusion_anisotropica(imagen, tiempo, lambd, sigma, lec = True):

    arr_img = np.array(imagen).astype(np.float64)
    img_actutal = arr_img.copy()

    filas, columnas = arr_img.shape

    contador_pasos = 0
    pasos = tiempo

    print(f'Inicio difusion Anisotropica')

    for i in range(tiempo):

        img_siguiente = img_actutal.copy()

        for x in range(1, filas-1):
            for y in range(1, columnas-1):

                centro = img_actutal[x][y]
                arriba = img_actutal[x-1][y]
                abajo = img_actutal[x+1][y]
                derecha = img_actutal[x][y+1]
                izquierda = img_actutal[x][y-1]

                dif_arriba = arriba - centro
                dif_abajo = abajo - centro
                dif_derecha = derecha - centro
                dif_izquierda = izquierda - centro

                if lec:
                    c_arriba = lecrec(dif_arriba, sigma)
                    c_abajo = lecrec(dif_abajo, sigma)
                    c_derecha = lecrec(dif_derecha, sigma)
                    c_izquierda = lecrec(dif_izquierda, sigma)

                else:
                    c_arriba = lorentz(dif_arriba, sigma)
                    c_abajo = lorentz(dif_abajo, sigma)
                    c_derecha = lorentz(dif_derecha, sigma)
                    c_izquierda = lorentz(dif_izquierda, sigma)
                    
                nuevo_valor = centro + ((dif_arriba * c_arriba + dif_abajo * c_abajo + dif_derecha * c_derecha + dif_izquierda * c_izquierda) * lambd)

                img_siguiente[x][y] = nuevo_valor
    
        contador_pasos += 1
        porcentaje = (contador_pasos / pasos) * 100
        print(f'\rProgreso: {porcentaje:.2f}%', end="")
    
        img_actutal = img_siguiente.copy()
    
    print('\nDifusion completada.')
    
    img_final = np.clip(img_actutal, 0, 255).astype(np.uint8)
    
    return(Image.fromarray(img_final))


def aplicar_filtro_bilaterial(imagen, sigma_s, sigma_r):

    arr_imagen = np.array(imagen).astype(np.float64)
    
    k = round(2 * sigma_s + 1)
    if k % 2 == 0: k += 1

    filas, col = arr_imagen.shape
    img_filtrada = arr_imagen.copy()
    radio = int((k-1) / 2)

    total_filas = (filas - radio) - radio
    contador_filas = 0

    print(f'Inicio de filtrado Bilaterial (tam_filtro: {k}x{k})')

    for x in range(radio, (filas - radio)):
        for y in range(radio, (col - radio)):

            vecindad, coordenadas = tomar_valores_vecindad_y_coord(arr_imagen, radio, x, y)
            
            distancias_cuadrado = coordenadas[:, 0]**2 + coordenadas[:, 1]**2            
            pesos_esp = np.exp(-distancias_cuadrado / (2 * sigma_s**2))

            centro = arr_imagen[x][y]
            dif_color = vecindad - centro
            pesos_color = np.exp(-(dif_color**2) / (2 * sigma_r**2))

            pesos_totales = pesos_esp * pesos_color

            suma_pixeles = np.sum(vecindad * pesos_totales)
            suma_pesos = np.sum(pesos_totales)
            
            img_filtrada[x][y] = suma_pixeles / suma_pesos          
            
        contador_filas += 1
        porcentaje = (contador_filas / total_filas) * 100

        print(f'\rProgreso: {porcentaje:.2f}%', end="")

    print('\nFiltrado completado.')

    img_final = np.clip(img_filtrada, 0, 255).astype(np.uint8)
    
    return(Image.fromarray(img_final))


def aplicar_umbralizacion_iterativa(imagen, delta_t):

    arr_img = np.array(imagen)

    umbral = np.mean(imagen)

    print('Inicio de Umbralizacion Iterativa')
    iteracion = 0

    while True:
        iteracion += 1

        g1 = arr_img[arr_img > umbral]
        g2 = arr_img[arr_img <= umbral]
    
        m1 = 1/len(g1) * np.sum(g1)
        m2 = 1/len(g2) * np.sum(g2)

        umbral_nuevo = 0.5 * (m1 + m2)

        if np.abs(umbral - umbral_nuevo) < delta_t:
            umbral_final = umbral_nuevo
            break
        else:
            umbral = umbral_nuevo
        
        print(f'Iteracion {iteracion}: Umbral = {umbral:.2f}')
    
    print(f'Fin de las iteraciones. Total de iteraciones: {iteracion}, Umbral Optimo: {umbral_final:.2f}')

    imagen_binarizada = binarizar_imagen(imagen, umbral_final)
    
    return(imagen_binarizada)


def aplicar_metodo_otzu(imagen):
    
    arr_img = np.array(imagen)

    frecuencias = obtener_histograma(imagen)
    p = np.zeros(256) 
    m = np.zeros(256) 
    p1 = np.zeros(256)

    for intensidad, prob in frecuencias.items():
        p[intensidad] = prob
    
    acumulador_m = 0.0
    acumulador_p1 = 0.0

    for t in range(256):

        acumulador_p1 += p[t]
        p1[t] = acumulador_p1

        acumulador_m += t * p[t]
        m[t] = acumulador_m
    
    mg = acumulador_m

    var_clases = np.zeros(256)

    for t in range(256):
            if p1[t] > 0 and p1[t] < 1:
                numerador = (mg * p1[t] - m[t]) ** 2
                denominador = p1[t] * (1 - p1[t])
                var_clases[t] = numerador / denominador
            else:
                var_clases[t] = 0.0

    umbral_optimo = np.argmax(var_clases)

    print(f"Método de Otsu completado. Umbral óptimo: {umbral_optimo}")

    imagen_final = binarizar_imagen(imagen, umbral_optimo)

    return imagen_final, umbral_optimo

def segmentar_color(imagen):

    arr_img = np.array(imagen)

    r = arr_img[:, :, 0]
    g = arr_img[:, :, 1]
    b = arr_img[:, :, 2]

    _, r_opt = aplicar_metodo_otzu(r)
    _, g_opt = aplicar_metodo_otzu(g)
    _, b_opt = aplicar_metodo_otzu(b)

    r_seg = np.where(r > r_opt, 255, 0).astype(np.uint8)
    g_seg = np.where(g > g_opt, 255, 0).astype(np.uint8)
    b_seg = np.where(b > b_opt, 255, 0).astype(np.uint8)

    arr_img_seg = np.stack([r_seg, g_seg, b_seg], axis=2)

    return Image.fromarray(arr_img_seg)


def aplicar_detector_canny(imagen, desviacion_gauss, t1, t2):

    arr_img = np.array(imagen)
    filas, col = arr_img.shape[:2]  

    imagen_filtrada = np.array(aplicar_fitro_gauss(imagen, desviacion_gauss))

    matriz_ver, matriz_hor = obtener_matrices_sobel(imagen_filtrada)

    matriz_angulos = np.zeros((filas, col), dtype=np.float64)
    matriz_sobel = np.zeros((filas, col), dtype=np.float64)
    matriz_resultado = np.zeros((filas, col), dtype=np.float64)
    
    matriz_final = np.zeros((filas, col), dtype=np.uint8)

    
    for x in range(1, (filas-1)):
        for y in range(1, (col-1)):

            I_x = matriz_hor[x][y]
            I_y = matriz_ver[x][y]

            if I_x != 0:
                angulo_radianes = np.atan(I_y / I_x)
                angulo = np.degrees(angulo_radianes) + 90
            else:
                angulo = np.degrees(np.pi/2) + 90
        
            if (angulo >= 0 and angulo <= 22.5) or (angulo >= 157.5 and angulo <= 180):
                angulo = 0
            elif (angulo >= 22.5 and angulo <= 67.5):
                angulo = 45
            elif (angulo >= 67.5 and angulo <= 112.5):
                angulo = 90
            else:
                angulo = 135
            
            matriz_angulos[x][y] = angulo
            matriz_sobel[x][y] = np.sqrt(I_x**2 + I_y**2)
    
    for x in range(1, (filas-1)):
        for y in range(1, (col-1)):

            angulo = matriz_angulos[x][y]

            if angulo == 0:
                vecino_1 = matriz_sobel[x][y-1]
                vecino_2 = matriz_sobel[x][y+1]
            elif angulo == 45:
                vecino_1 = matriz_sobel[x+1][y-1]
                vecino_2 = matriz_sobel[x-1][y+1]
            elif angulo == 90:
                vecino_1 = matriz_sobel[x-1][y]
                vecino_2 = matriz_sobel[x+1][y]
            else:
                vecino_1 = matriz_sobel[x-1][y-1]
                vecino_2 = matriz_sobel[x+1][y+1]
            
            centro = matriz_sobel[x][y]
            
            if centro >= vecino_1 and centro >= vecino_2:
                matriz_resultado[x][y] = centro
            else:
                matriz_resultado[x][y] = 0
            
            if matriz_resultado[x][y] >= t2:
                matriz_final[x][y] = 255
            elif matriz_resultado[x][y] < t1:
                matriz_final[x][y] = 0
            else:
                matriz_final[x][y] = 1

    for x in range(1, (filas-1)):
        for y in range(1, (col-1)):

            if matriz_final[x][y] == 255:
                
                if matriz_final[x-1][y-1] == 1: matriz_final[x-1][y-1] = 255
                if matriz_final[x-1][y] == 1: matriz_final[x-1][y] = 255
                if matriz_final[x-1][y+1] == 1: matriz_final[x-1][y+1] = 255
                if matriz_final[x][y-1] == 1: matriz_final[x][y-1] = 255
                if matriz_final[x][y+1] == 1: matriz_final[x][y+1] = 255
                if matriz_final[x+1][y-1] == 1: matriz_final[x+1][y-1] = 255
                if matriz_final[x+1][y] == 1: matriz_final[x+1][y] = 255
                if matriz_final[x+1][y+1] == 1: matriz_final[x+1][y+1] = 255
    #for x in range(1, (filas-1)):
    #     for y in range(1, (col-1)):

    #         if matriz_final[x][y] == 255:
                
    #             if matriz_final[x-1][y] == 1: matriz_final[x-1][y] = 255
    #             if matriz_final[x][y-1] == 1: matriz_final[x][y-1] = 255
    #             if matriz_final[x][y+1] == 1: matriz_final[x][y+1] = 255
    #             if matriz_final[x+1][y] == 1: matriz_final[x+1][y] = 255

    print('Fin detector de Canny')

    return Image.fromarray(matriz_final)
