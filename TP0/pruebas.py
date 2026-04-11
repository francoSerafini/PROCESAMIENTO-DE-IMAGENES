import tkinter as tk

ventana = tk.Tk()

# Sin pady
btn1 = tk.Button(ventana, text="Sin espacio")
btn1.pack()

# Con pady
btn2 = tk.Button(ventana, text="Con 20px de espacio")
btn2.pack(pady=20)  # 20 píxeles arriba y abajo

ventana.mainloop()