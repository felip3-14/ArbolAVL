import tkinter as tk
from tkinter import ttk, messagebox
import math
from typing import List, Tuple, Optional
from main import AVLTree, Nodo

class AVLVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("Visualizador de Árbol AVL")
        self.root.geometry("1200x800")
        self.root.configure(bg='#f0f0f0')
        
        # Datos del árbol
        self.arbol = AVLTree()
        
        # Secuencias predefinidas
        self.secuencias_predefinidas = {
            "Secuencia Original": [10, 20, 30, 40, 50, 25],
            "Números Aleatorios": [15, 8, 22, 4, 12, 18, 25, 2, 6, 10, 14, 20, 24, 1, 3, 5, 7, 9, 11, 13],
            "Secuencia Creciente": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            "Secuencia Decreciente": [10, 9, 8, 7, 6, 5, 4, 3, 2, 1],
            "Fibonacci": [1, 1, 2, 3, 5, 8, 13, 21, 34, 55],
            "Potencias de 2": [1, 2, 4, 8, 16, 32, 64, 128],
            "Números Primos": [2, 3, 5, 7, 11, 13, 17, 19, 23, 29],
            "Secuencia Mixta": [50, 25, 75, 12, 37, 62, 87, 6, 18, 31, 43, 56, 68, 81, 93],
            "Secuencia Pequeña": [5, 3, 7, 1, 4, 6, 8],
            "Secuencia Balanceada": [8, 4, 12, 2, 6, 10, 14, 1, 3, 5, 7, 9, 11, 13, 15]
        }
        
        self.secuencia = self.secuencias_predefinidas["Secuencia Original"]
        self.paso_actual = 0
        self.historial_arboles = []  # Guarda el estado del árbol en cada paso
        self.historial_logs = []     # Guarda los logs de cada paso
        
        self.setup_ui()
        self.preparar_historial()
        
    def setup_ui(self):
        """Configura la interfaz de usuario."""
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configurar grid
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Panel de controles
        self.setup_control_panel(main_frame)
        
        # Canvas para dibujar el árbol
        self.setup_canvas(main_frame)
        
        # Panel de información
        self.setup_info_panel(main_frame)
        
    def setup_control_panel(self, parent):
        """Configura el panel de controles."""
        control_frame = ttk.LabelFrame(parent, text="Controles", padding="10")
        control_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Selector de secuencias
        seq_frame = ttk.Frame(control_frame)
        seq_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(seq_frame, text="Secuencia:", font=('Arial', 10, 'bold')).pack(side=tk.LEFT)
        
        # Agregar "Personalizada" a las opciones
        opciones = list(self.secuencias_predefinidas.keys()) + ["Personalizada"]
        self.combo_secuencias = ttk.Combobox(seq_frame, values=opciones, 
                                           state="readonly", width=20)
        self.combo_secuencias.set("Secuencia Original")
        self.combo_secuencias.bind("<<ComboboxSelected>>", self.cambiar_secuencia)
        self.combo_secuencias.pack(side=tk.LEFT, padx=(10, 5))
        
        # Entrada personalizada
        ttk.Label(seq_frame, text="Personalizada:").pack(side=tk.LEFT, padx=(20, 5))
        self.entry_personalizada = ttk.Entry(seq_frame, width=30)
        self.entry_personalizada.pack(side=tk.LEFT, padx=(0, 5))
        
        # Agregar placeholder manual
        self.placeholder_text = "Ej: 1,2,3,4,5"
        self.entry_personalizada.insert(0, self.placeholder_text)
        self.entry_personalizada.configure(foreground='gray')
        
        def on_focus_in(event):
            if self.entry_personalizada.get() == self.placeholder_text:
                self.entry_personalizada.delete(0, tk.END)
                self.entry_personalizada.configure(foreground='black')
                
        def on_focus_out(event):
            if not self.entry_personalizada.get():
                self.entry_personalizada.insert(0, self.placeholder_text)
                self.entry_personalizada.configure(foreground='gray')
                
        self.entry_personalizada.bind('<FocusIn>', on_focus_in)
        self.entry_personalizada.bind('<FocusOut>', on_focus_out)
        
        self.btn_aplicar = ttk.Button(seq_frame, text="Aplicar", command=self.aplicar_secuencia_personalizada)
        self.btn_aplicar.pack(side=tk.LEFT)
        
        self.btn_ayuda = ttk.Button(seq_frame, text="❓", command=self.mostrar_ayuda, width=3)
        self.btn_ayuda.pack(side=tk.LEFT, padx=(5, 0))
        
        # Botones de navegación
        btn_frame = ttk.Frame(control_frame)
        btn_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.btn_anterior = ttk.Button(btn_frame, text="◀ Anterior", 
                                     command=self.paso_anterior, state=tk.DISABLED)
        self.btn_anterior.pack(side=tk.LEFT, padx=(0, 5))
        
        self.btn_siguiente = ttk.Button(btn_frame, text="Siguiente ▶", 
                                      command=self.paso_siguiente)
        self.btn_siguiente.pack(side=tk.LEFT, padx=5)
        
        self.btn_reiniciar = ttk.Button(btn_frame, text="🔄 Reiniciar", 
                                      command=self.reiniciar)
        self.btn_reiniciar.pack(side=tk.LEFT, padx=5)
        
        # Información del paso actual
        info_frame = ttk.Frame(control_frame)
        info_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.label_paso = ttk.Label(info_frame, text="Paso 0 de 6", font=('Arial', 12, 'bold'))
        self.label_paso.pack(side=tk.LEFT)
        
        self.label_elemento = ttk.Label(info_frame, text="", font=('Arial', 10))
        self.label_elemento.pack(side=tk.LEFT, padx=(20, 0))
        
    def setup_canvas(self, parent):
        """Configura el canvas para dibujar el árbol."""
        canvas_frame = ttk.LabelFrame(parent, text="Árbol AVL", padding="10")
        canvas_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        
        self.canvas = tk.Canvas(canvas_frame, bg='white', width=600, height=500)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(canvas_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        h_scrollbar = ttk.Scrollbar(canvas_frame, orient=tk.HORIZONTAL, command=self.canvas.xview)
        self.canvas.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        
    def setup_info_panel(self, parent):
        """Configura el panel de información."""
        info_frame = ttk.LabelFrame(parent, text="Información", padding="10")
        info_frame.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Text widget para mostrar información
        self.text_info = tk.Text(info_frame, width=40, height=25, wrap=tk.WORD, 
                               font=('Consolas', 10), bg='#f8f8f8')
        scrollbar_info = ttk.Scrollbar(info_frame, orient=tk.VERTICAL, command=self.text_info.yview)
        self.text_info.configure(yscrollcommand=scrollbar_info.set)
        
        self.text_info.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar_info.pack(side=tk.RIGHT, fill=tk.Y)
        
    def preparar_historial(self):
        """Prepara el historial de todos los pasos."""
        self.historial_arboles = []
        self.historial_logs = []
        
        arbol_temp = AVLTree()
        
        for i, elemento in enumerate(self.secuencia):
            arbol_temp.insertar(elemento)
            logs = arbol_temp.consumir_log()
            
            # Crear una copia del árbol actual
            arbol_copia = self.copiar_arbol(arbol_temp.raiz)
            self.historial_arboles.append(arbol_copia)
            self.historial_logs.append(logs.copy())
        
        self.actualizar_display()
        
    def copiar_arbol(self, nodo: Optional[Nodo]) -> Optional[Nodo]:
        """Crea una copia profunda del árbol."""
        if nodo is None:
            return None
        
        nuevo_nodo = Nodo(nodo.clave)
        nuevo_nodo.altura = nodo.altura
        nuevo_nodo.izq = self.copiar_arbol(nodo.izq)
        nuevo_nodo.der = self.copiar_arbol(nodo.der)
        return nuevo_nodo
        
    def paso_anterior(self):
        """Va al paso anterior."""
        if self.paso_actual > 0:
            self.paso_actual -= 1
            self.actualizar_display()
            
    def paso_siguiente(self):
        """Va al paso siguiente."""
        if self.paso_actual < len(self.secuencia):
            self.paso_actual += 1
            self.actualizar_display()
            
    def reiniciar(self):
        """Reinicia la visualización."""
        self.paso_actual = 0
        self.actualizar_display()
        
    def cambiar_secuencia(self, event=None):
        """Cambia la secuencia cuando se selecciona una del combobox."""
        secuencia_seleccionada = self.combo_secuencias.get()
        if secuencia_seleccionada == "Personalizada":
            # Si selecciona "Personalizada", no hacer nada hasta que aplique una secuencia
            return
        elif secuencia_seleccionada in self.secuencias_predefinidas:
            self.secuencia = self.secuencias_predefinidas[secuencia_seleccionada]
            self.paso_actual = 0
            self.preparar_historial()
            self.actualizar_display()
            
    def aplicar_secuencia_personalizada(self):
        """Aplica una secuencia personalizada ingresada por el usuario."""
        texto = self.entry_personalizada.get().strip()
        if not texto or texto == self.placeholder_text:
            messagebox.showwarning("Advertencia", "Por favor ingresa una secuencia de números.")
            return
            
        try:
            # Parsear la entrada (soporta comas, espacios, o ambos)
            numeros = []
            for parte in texto.replace(',', ' ').split():
                numero = int(parte.strip())
                if numero < 0:
                    messagebox.showerror("Error", "Los números deben ser positivos.")
                    return
                numeros.append(numero)
                
            if len(numeros) == 0:
                messagebox.showwarning("Advertencia", "No se encontraron números válidos.")
                return
                
            if len(numeros) > 20:
                respuesta = messagebox.askyesno("Confirmación", 
                    f"La secuencia tiene {len(numeros)} elementos. ¿Continuar?")
                if not respuesta:
                    return
                    
            self.secuencia = numeros
            self.paso_actual = 0
            self.preparar_historial()
            self.actualizar_display()
            
            # Actualizar el combobox para mostrar "Personalizada"
            self.combo_secuencias.set("Personalizada")
            
        except ValueError:
            messagebox.showerror("Error", "Formato inválido. Usa números separados por comas o espacios.\nEjemplo: 1,2,3,4,5 o 1 2 3 4 5")
            
    def mostrar_ayuda(self):
        """Muestra información sobre las secuencias predefinidas."""
        ayuda_texto = """📚 SECUENCIAS PREDEFINIDAS:

🔹 Secuencia Original: [10, 20, 30, 40, 50, 25]
   - Secuencia básica con rotaciones RR y RL

🔹 Números Aleatorios: [15, 8, 22, 4, 12, 18, 25, 2, 6, 10, 14, 20, 24, 1, 3, 5, 7, 9, 11, 13]
   - Secuencia larga con muchos reordenamientos

🔹 Secuencia Creciente: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
   - Caso extremo: árbol degenerado (solo rotaciones RR)

🔹 Secuencia Decreciente: [10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
   - Caso extremo: árbol degenerado (solo rotaciones LL)

🔹 Fibonacci: [1, 1, 2, 3, 5, 8, 13, 21, 34, 55]
   - Secuencia matemática famosa

🔹 Potencias de 2: [1, 2, 4, 8, 16, 32, 64, 128]
   - Secuencia exponencial

🔹 Números Primos: [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
   - Secuencia de números primos

🔹 Secuencia Mixta: [50, 25, 75, 12, 37, 62, 87, 6, 18, 31, 43, 56, 68, 81, 93]
   - Secuencia compleja con muchas rotaciones

🔹 Secuencia Pequeña: [5, 3, 7, 1, 4, 6, 8]
   - Secuencia corta para pruebas rápidas

🔹 Secuencia Balanceada: [8, 4, 12, 2, 6, 10, 14, 1, 3, 5, 7, 9, 11, 13, 15]
   - Secuencia que produce un árbol muy balanceado

💡 TIP: Usa secuencias personalizadas para experimentar con tus propios datos."""
        
        # Crear ventana de ayuda
        ventana_ayuda = tk.Toplevel(self.root)
        ventana_ayuda.title("Ayuda - Secuencias Predefinidas")
        ventana_ayuda.geometry("600x500")
        ventana_ayuda.configure(bg='#f0f0f0')
        
        # Frame con scroll
        frame_ayuda = ttk.Frame(ventana_ayuda, padding="10")
        frame_ayuda.pack(fill=tk.BOTH, expand=True)
        
        text_ayuda = tk.Text(frame_ayuda, wrap=tk.WORD, font=('Consolas', 10), 
                           bg='#f8f8f8', padx=10, pady=10)
        scrollbar_ayuda = ttk.Scrollbar(frame_ayuda, orient=tk.VERTICAL, command=text_ayuda.yview)
        text_ayuda.configure(yscrollcommand=scrollbar_ayuda.set)
        
        text_ayuda.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar_ayuda.pack(side=tk.RIGHT, fill=tk.Y)
        
        text_ayuda.insert(tk.END, ayuda_texto)
        text_ayuda.config(state=tk.DISABLED)
        
        # Botón cerrar
        btn_cerrar = ttk.Button(ventana_ayuda, text="Cerrar", command=ventana_ayuda.destroy)
        btn_cerrar.pack(pady=10)
        
    def actualizar_display(self):
        """Actualiza toda la visualización."""
        self.actualizar_controles()
        self.dibujar_arbol()
        self.actualizar_informacion()
        
    def actualizar_controles(self):
        """Actualiza el estado de los controles."""
        self.btn_anterior.config(state=tk.NORMAL if self.paso_actual > 0 else tk.DISABLED)
        self.btn_siguiente.config(state=tk.NORMAL if self.paso_actual < len(self.secuencia) else tk.DISABLED)
        
        self.label_paso.config(text=f"Paso {self.paso_actual} de {len(self.secuencia)}")
        
        if self.paso_actual > 0:
            elemento = self.secuencia[self.paso_actual - 1]
            self.label_elemento.config(text=f"Elemento insertado: {elemento}")
        else:
            self.label_elemento.config(text="Árbol vacío")
            
    def dibujar_arbol(self):
        """Dibuja el árbol en el canvas."""
        self.canvas.delete("all")
        
        if self.paso_actual == 0:
            self.canvas.create_text(300, 250, text="Árbol vacío", 
                                  font=('Arial', 16), fill='gray')
            return
            
        # Obtener el árbol del paso actual
        raiz = self.historial_arboles[self.paso_actual - 1]
        
        if raiz is None:
            return
            
        # Calcular posiciones de los nodos
        posiciones = self.calcular_posiciones(raiz)
        
        # Dibujar conexiones primero (para que queden detrás de los nodos)
        self.dibujar_conexiones(raiz, posiciones)
        
        # Dibujar nodos
        self.dibujar_nodos(posiciones)
        
        # Ajustar scroll
        self.ajustar_scroll(posiciones)
        
    def calcular_posiciones(self, raiz: Nodo) -> dict:
        """Calcula las posiciones de todos los nodos."""
        posiciones = {}
        nivel_ancho = {}
        
        # Primera pasada: calcular anchos por nivel
        def calcular_anchos(nodo: Optional[Nodo], nivel: int):
            if nodo is None:
                return 0
                
            ancho_izq = calcular_anchos(nodo.izq, nivel + 1)
            ancho_der = calcular_anchos(nodo.der, nivel + 1)
            ancho_total = ancho_izq + ancho_der + 1
            
            if nivel not in nivel_ancho:
                nivel_ancho[nivel] = 0
            nivel_ancho[nivel] = max(nivel_ancho[nivel], ancho_total)
            
            return ancho_total
            
        calcular_anchos(raiz, 0)
        
        # Segunda pasada: asignar posiciones
        def asignar_posiciones(nodo: Optional[Nodo], nivel: int, x_inicio: int, x_fin: int):
            if nodo is None:
                return
                
            x_centro = (x_inicio + x_fin) // 2
            y = 50 + nivel * 80
            
            posiciones[nodo.clave] = (x_centro, y)
            
            # Calcular posiciones de hijos
            if nodo.izq or nodo.der:
                ancho_total = x_fin - x_inicio
                if nodo.izq and nodo.der:
                    # Ambos hijos
                    mitad = ancho_total // 2
                    asignar_posiciones(nodo.izq, nivel + 1, x_inicio, x_inicio + mitad)
                    asignar_posiciones(nodo.der, nivel + 1, x_inicio + mitad, x_fin)
                elif nodo.izq:
                    # Solo hijo izquierdo
                    asignar_posiciones(nodo.izq, nivel + 1, x_inicio, x_centro)
                else:
                    # Solo hijo derecho
                    asignar_posiciones(nodo.der, nivel + 1, x_centro, x_fin)
                    
        asignar_posiciones(raiz, 0, 50, 550)
        return posiciones
        
    def dibujar_conexiones(self, nodo: Optional[Nodo], posiciones: dict):
        """Dibuja las líneas que conectan los nodos."""
        if nodo is None:
            return
            
        x_nodo, y_nodo = posiciones[nodo.clave]
        
        # Conectar con hijo izquierdo
        if nodo.izq:
            x_izq, y_izq = posiciones[nodo.izq.clave]
            self.canvas.create_line(x_nodo, y_nodo + 15, x_izq, y_izq - 15, 
                                  fill='#666', width=2)
            self.dibujar_conexiones(nodo.izq, posiciones)
            
        # Conectar con hijo derecho
        if nodo.der:
            x_der, y_der = posiciones[nodo.der.clave]
            self.canvas.create_line(x_nodo, y_nodo + 15, x_der, y_der - 15, 
                                  fill='#666', width=2)
            self.dibujar_conexiones(nodo.der, posiciones)
            
    def dibujar_nodos(self, posiciones: dict):
        """Dibuja los nodos del árbol."""
        for clave, (x, y) in posiciones.items():
            # Círculo del nodo
            self.canvas.create_oval(x-20, y-15, x+20, y+15, 
                                  fill='#4CAF50', outline='#2E7D32', width=2)
            
            # Texto del nodo
            self.canvas.create_text(x, y, text=str(clave), 
                                  font=('Arial', 12, 'bold'), fill='white')
                                  
    def ajustar_scroll(self, posiciones: dict):
        """Ajusta el área de scroll del canvas."""
        if not posiciones:
            return
            
        # Calcular bounding box
        x_coords = [pos[0] for pos in posiciones.values()]
        y_coords = [pos[1] for pos in posiciones.values()]
        
        min_x, max_x = min(x_coords) - 50, max(x_coords) + 50
        min_y, max_y = min(y_coords) - 50, max(y_coords) + 50
        
        self.canvas.configure(scrollregion=(min_x, min_y, max_x, max_y))
        
    def actualizar_informacion(self):
        """Actualiza el panel de información."""
        self.text_info.delete(1.0, tk.END)
        
        if self.paso_actual == 0:
            self.text_info.insert(tk.END, "=== Árbol AVL Vacío ===\n\n")
            self.text_info.insert(tk.END, "Presiona 'Siguiente' para comenzar la inserción.\n\n")
            self.text_info.insert(tk.END, f"Secuencia a insertar ({len(self.secuencia)} elementos):\n")
            
            # Mostrar la secuencia en columnas si es muy larga
            if len(self.secuencia) <= 10:
                for i, elem in enumerate(self.secuencia, 1):
                    self.text_info.insert(tk.END, f"{i}. {elem}\n")
            else:
                # Mostrar en columnas
                for i in range(0, len(self.secuencia), 5):
                    linea = ""
                    for j in range(5):
                        if i + j < len(self.secuencia):
                            elem = self.secuencia[i + j]
                            linea += f"{i+j+1:2d}. {elem:3d}  "
                    self.text_info.insert(tk.END, linea + "\n")
            return
            
        # Información del paso actual
        elemento = self.secuencia[self.paso_actual - 1]
        self.text_info.insert(tk.END, f"=== Paso {self.paso_actual}: Insertar {elemento} ===\n\n")
        
        # Mostrar logs de rotaciones
        logs = self.historial_logs[self.paso_actual - 1]
        if logs:
            self.text_info.insert(tk.END, "Operaciones realizadas:\n")
            for log in logs:
                self.text_info.insert(tk.END, f"• {log}\n")
            self.text_info.insert(tk.END, "\n")
        else:
            self.text_info.insert(tk.END, "Inserción simple (sin rotaciones)\n\n")
            
        # Mostrar árbol en ASCII
        arbol_temp = AVLTree()
        arbol_temp.raiz = self.historial_arboles[self.paso_actual - 1]
        self.text_info.insert(tk.END, "Estructura del árbol:\n")
        self.text_info.insert(tk.END, arbol_temp.ascii_simple())
        self.text_info.insert(tk.END, "\n\n")
        
        # Mostrar recorrido en orden
        recorrido = arbol_temp.recorrido_inorden()
        self.text_info.insert(tk.END, f"Recorrido en-orden: {recorrido}\n")
        
        # Mostrar información de balance
        self.text_info.insert(tk.END, "\nInformación de balance:\n")
        self.mostrar_info_balance(arbol_temp.raiz, 0)
        
    def mostrar_info_balance(self, nodo: Optional[Nodo], nivel: int):
        """Muestra información de balance de cada nodo."""
        if nodo is None:
            return
            
        indent = "  " * nivel
        fb = AVLTree.fb_estatico(nodo)
        estado = "✓ Balanceado" if abs(fb) <= 1 else "⚠ Desbalanceado"
        
        self.text_info.insert(tk.END, f"{indent}Nodo {nodo.clave}: altura={nodo.altura}, FB={fb} {estado}\n")
        
        self.mostrar_info_balance(nodo.izq, nivel + 1)
        self.mostrar_info_balance(nodo.der, nivel + 1)


def main():
    root = tk.Tk()
    app = AVLVisualizer(root)
    root.mainloop()


if __name__ == "__main__":
    main()
