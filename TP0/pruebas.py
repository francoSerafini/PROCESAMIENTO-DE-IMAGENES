import tkinter as tk

ventana = tk.Tk()
canvas = tk.Canvas(ventana, width=600,  height=400, bg="white")
canvas.pack()

# Dibujar un círculo
circulo = canvas.create_oval(100, 100, 150, 150, fill="blue")

# Evento click
def on_click(event):
    print(f"Click en: ({event.x}, {event.y})")
    
    # Verificar si clickeó dentro del círculo
    items = canvas.find_overlapping(event.x, event.y, event.x, event.y)
    if circulo in items:
        print("¡Clickeaste el círculo!")

canvas.bind("<Button-1>", on_click)  # Click izquierdo

# Dibujar con el mouse (como Paint)
def dibujar(event):
    x, y = event.x, event.y
    canvas.create_oval(x-2, y-2, x+2, y+2, fill="black")

canvas.bind("<B1-Motion>", dibujar)  # Arrastrar con click

ventana.mainloop()