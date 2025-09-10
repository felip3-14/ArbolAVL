# Visualizador de Árbol AVL (Tkinter)

Aplicación de escritorio en Python para visualizar paso a paso la construcción de un Árbol AVL durante inserciones. Permite elegir secuencias predefinidas o ingresar una secuencia personalizada, navegar por cada paso, ver el árbol dibujado y consultar información detallada (rotaciones, árbol en ASCII, recorrido en-orden y factores de balance).

> Repositorio remoto: [felip3-14/ArbolAVL](https://github.com/felip3-14/ArbolAVL)

---

## Características

- **Visualización paso a paso**: Navega por cada inserción para entender el proceso de balanceado.
- **10 secuencias predefinidas**: Casos educativos desde básicos hasta complejos.
- **Secuencias personalizadas**: Experimenta con tus propios datos.
- **Navegación interactiva**: Anterior / Siguiente / Reiniciar para estudiar a tu ritmo.
- **Visualización gráfica**: Dibujo del árbol en `Canvas` con scroll automático.
- **Panel informativo detallado**:
  - Operaciones realizadas (rotaciones LL, LR, RR, RL).
  - Representación ASCII del árbol.
  - Recorrido en-orden.
  - Altura y factor de balance por nodo.
  - Estado de balance (✓ Balanceado / ⚠ Desbalanceado).

## Requisitos

- Python 3.8+
- Tkinter (incluido en la mayoría de distribuciones de Python de Windows y macOS). En Linux suele requerir paquete del sistema:
  - Debian/Ubuntu: `sudo apt-get install python3-tk`
  - Fedora: `sudo dnf install python3-tkinter`
  - Arch: `sudo pacman -S tk`

No hay dependencias de terceros vía `pip`.

## Estructura del proyecto

```
.
├── avl_visualizer.py   # GUI de visualización (Tkinter)
└── main.py             # Debe definir `AVLTree` y `Nodo`
```

Este repositorio incluye `avl_visualizer.py`. Debes proveer un `main.py` con la implementación del Árbol AVL que exponga al menos:

- Clase `AVLTree` con:
  - Atributo `raiz`
  - Método `insertar(clave: int) -> None`
  - Método `consumir_log() -> list[str]` (retorna y vacía logs de la última inserción)
  - Método `ascii_simple() -> str` (representación ASCII del árbol)
  - Método `recorrido_inorden() -> list[int]`
  - Método/función estática `fb_estatico(nodo: Nodo) -> int` (factor de balance)
- Clase `Nodo` con atributos: `clave`, `altura`, `izq`, `der`

Ajusta nombres/firmas si tu implementación difiere, o modifica el `import` en `avl_visualizer.py` (`from main import AVLTree, Nodo`).

## Instalación y ejecución

1. Asegúrate de tener Python 3 y Tkinter.
2. Coloca `main.py` junto a `avl_visualizer.py`.
3. Ejecuta:

```bash
python3 avl_visualizer.py
```

En macOS/Windows puedes hacer doble clic si tu asociación de archivos `.py` lo permite, pero se recomienda la terminal para ver errores si ocurren.

## Uso

- "Secuencia": selecciona una de las secuencias predefinidas o elige "Personalizada" y escribe números separados por coma o espacio (ej.: `1,2,3,4` o `1 2 3 4`).
- "Aplicar": carga la secuencia personalizada.
- "❓": abre un resumen de las secuencias predefinidas.
- Botones:
  - "◀ Anterior": vuelve un paso.
  - "Siguiente ▶": avanza un paso e inserta el siguiente elemento.
  - "🔄 Reiniciar": vuelve al paso 0 (árbol vacío).
- Panel derecho "Información": muestra operaciones (rotaciones), árbol ASCII, recorrido en-orden y factores de balance por nodo.

Notas:
- Números negativos no están permitidos en la entrada.
- Para secuencias con más de 20 elementos se pedirá confirmación.
- Soporte de duplicados depende de tu implementación de `AVLTree`. El ejemplo incluye Fibonacci `[1, 1, 2, 3, ...]`.

## Secuencias predefinidas

Cada secuencia está diseñada para enseñar aspectos específicos de los árboles AVL:

- **Secuencia Original**: `[10, 20, 30, 40, 50, 25]` - Básica con rotaciones RR y RL
- **Números Aleatorios**: `[15, 8, 22, 4, 12, 18, 25, 2, 6, 10, 14, 20, 24, 1, 3, 5, 7, 9, 11, 13]` - Secuencia larga con múltiples rebalanceos
- **Secuencia Creciente**: `[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]` - Caso extremo: solo rotaciones RR
- **Secuencia Decreciente**: `[10, 9, 8, 7, 6, 5, 4, 3, 2, 1]` - Caso extremo: solo rotaciones LL  
- **Fibonacci**: `[1, 1, 2, 3, 5, 8, 13, 21, 34, 55]` - Secuencia matemática famosa
- **Potencias de 2**: `[1, 2, 4, 8, 16, 32, 64, 128]` - Crecimiento exponencial
- **Números Primos**: `[2, 3, 5, 7, 11, 13, 17, 19, 23, 29]` - Distribución irregular
- **Secuencia Mixta**: `[50, 25, 75, 12, 37, 62, 87, 6, 18, 31, 43, 56, 68, 81, 93]` - Rotaciones complejas
- **Secuencia Pequeña**: `[5, 3, 7, 1, 4, 6, 8]` - Ideal para pruebas rápidas
- **Secuencia Balanceada**: `[8, 4, 12, 2, 6, 10, 14, 1, 3, 5, 7, 9, 11, 13, 15]` - Árbol perfectamente balanceado

## Solución de problemas

- `ModuleNotFoundError: No module named 'main'`:
  - Crea `main.py` junto a `avl_visualizer.py` con `AVLTree` y `Nodo`.
  - Verifica que el `import` sea `from main import AVLTree, Nodo`.
- Tkinter no está disponible:
  - Instala el paquete `tk`/`tkinter` para tu sistema (ver Requisitos).
- La ventana no entra en pantalla:
  - Modifica `self.root.geometry("1200x800")` en `avl_visualizer.py`.

## Publicar en GitHub

Si ya clonaste el repositorio vacío `ArbolAVL`, o quieres inicializar y subir este proyecto:

```bash
cd "/Users/felipe/Library/Mobile Documents/com~apple~CloudDocs/TERCER AÑO SIGLO 21/arbolAVL_Facu"

git init
# Opcional: usar "main" como rama por defecto
git branch -m main

# Agrega el remoto (si ya existe, usa set-url)
git remote add origin https://github.com/felip3-14/ArbolAVL.git || git remote set-url origin https://github.com/felip3-14/ArbolAVL.git

git add .
git commit -m "feat: visualizador de Árbol AVL con Tkinter"
git push -u origin main
```

Si el remoto requiere autenticación, inicia sesión con GitHub CLI o configura tus credenciales.

## Casos de uso educativos

Esta herramienta es ideal para:

- **Estudiantes de estructuras de datos**: Visualizar cómo funcionan las rotaciones AVL
- **Profesores**: Demostrar el algoritmo paso a paso en clase
- **Desarrolladores**: Depurar implementaciones de árboles AVL
- **Investigadores**: Analizar comportamiento con diferentes patrones de datos

## Contribuciones

Las contribuciones son bienvenidas. Algunas mejoras posibles:

- Soporte para eliminación de nodos
- Animaciones entre pasos
- Exportar visualizaciones como imagen
- Comparación con otros tipos de árboles (BST, Red-Black)
- Métricas de rendimiento (comparaciones, rotaciones)

## Licencia

Sin licencia explícita. Añade una si lo deseas (por ejemplo, MIT).
