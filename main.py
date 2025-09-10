from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, List, Tuple
import time
import sys

# Convenciones usadas en todo el código:
# - Altura(árbol vacío) = 0; Altura(hoja) = 1.
# - FB(n) = altura(der) - altura(izq).
# - Se imprimen alturas y FB en el ASCII-art.

@dataclass
class Nodo:
    clave: int
    izq: Optional["Nodo"] = None
    der: Optional["Nodo"] = None
    altura: int = 1  # hoja = 1

    def __str__(self) -> str:
        return f"{self.clave}[h={self.altura},FB={AVLTree.fb_estatico(self)}]"


class AVLTree:
    def __init__(self) -> None:
        self.raiz: Optional[Nodo] = None
        self._log: List[str] = []  # guarda mensajes de rotaciones/apuntes por inserción

    # -------- Utilitarios de altura / FB --------
    @staticmethod
    def altura(n: Optional[Nodo]) -> int:
        return n.altura if n else 0

    @staticmethod
    def fb_estatico(n: Optional[Nodo]) -> int:
        if not n:
            return 0
        return AVLTree.altura(n.der) - AVLTree.altura(n.izq)

    def _actualizar_altura(self, n: Nodo) -> None:
        n.altura = 1 + max(self.altura(n.izq), self.altura(n.der))

    # -------- Rotaciones --------
    def _rotacion_der(self, a: Nodo) -> Nodo:
        """Rotación simple a la derecha (caso LL)."""
        b = a.izq
        assert b is not None
        a.izq = b.der
        b.der = a
        self._actualizar_altura(a)
        self._actualizar_altura(b)
        return b

    def _rotacion_izq(self, a: Nodo) -> Nodo:
        """Rotación simple a la izquierda (caso RR)."""
        c = a.der
        assert c is not None
        a.der = c.izq
        c.izq = a
        self._actualizar_altura(a)
        self._actualizar_altura(c)
        return c

    # -------- Inserción con reequilibrado --------
    def insertar(self, clave: int) -> None:
        """Inserta 'clave' y reequilibra si es necesario."""
        self._log.clear()
        self.raiz = self._insertar(self.raiz, clave)
    
    def insertar_sin_balancear(self, clave: int) -> None:
        """Inserta 'clave' sin reequilibrar (para mostrar estados intermedios)."""
        self._log.clear()
        self.raiz = self._insertar_sin_balancear(self.raiz, clave)

    def _insertar(self, n: Optional[Nodo], clave: int) -> Nodo:
        if n is None:
            return Nodo(clave)

        if clave < n.clave:
            n.izq = self._insertar(n.izq, clave)
        elif clave > n.clave:
            n.der = self._insertar(n.der, clave)
        else:
            # Claves duplicadas: no insertamos (o podríamos contar frecuencia)
            self._log.append(f"Clave {clave} duplicada: se ignora.")
            return n

        # Actualizar altura y chequear balance
        self._actualizar_altura(n)
        fb = self.fb_estatico(n)

        # Desbalance a la izquierda (LL o LR)
        if fb < -1:
            fb_izq = self.fb_estatico(n.izq)
            if fb_izq <= 0:
                self._log.append(
                    f"Desbalance en {n.clave} (FB={fb}). Patrón LL → Rotación simple a la derecha en {n.clave}."
                )
                return self._rotacion_der(n)  # LL
            else:
                self._log.append(
                    f"Desbalance en {n.clave} (FB={fb}). Patrón LR → "
                    f"Rotación simple a la izquierda en {n.izq.clave} y luego a la derecha en {n.clave}."
                )
                n.izq = self._rotacion_izq(n.izq)  # primera parte (en hijo izq)
                return self._rotacion_der(n)       # segunda parte (en nodo)

        # Desbalance a la derecha (RR o RL)
        if fb > 1:
            fb_der = self.fb_estatico(n.der)
            if fb_der >= 0:
                self._log.append(
                    f"Desbalance en {n.clave} (FB={fb}). Patrón RR → Rotación simple a la izquierda en {n.clave}."
                )
                return self._rotacion_izq(n)  # RR
            else:
                self._log.append(
                    f"Desbalance en {n.clave} (FB={fb}). Patrón RL → "
                    f"Rotación simple a la derecha en {n.der.clave} y luego a la izquierda en {n.clave}."
                )
                n.der = self._rotacion_der(n.der)  # primera parte (en hijo der)
                return self._rotacion_izq(n)       # segunda parte (en nodo)

        return n  # ya balanceado

    def _insertar_sin_balancear(self, n: Optional[Nodo], clave: int) -> Nodo:
        """Inserta sin reequilibrar (solo para mostrar estados intermedios)."""
        if n is None:
            return Nodo(clave)

        if clave < n.clave:
            n.izq = self._insertar_sin_balancear(n.izq, clave)
        elif clave > n.clave:
            n.der = self._insertar_sin_balancear(n.der, clave)
        else:
            # Claves duplicadas: no insertamos
            self._log.append(f"Clave {clave} duplicada: se ignora.")
            return n

        # Solo actualizar altura, sin verificar balance
        self._actualizar_altura(n)
        return n

    # -------- Visualización ASCII --------
    def ascii(self, mostrar_detalles: bool = True) -> str:
        """Retorna string con el árbol en ASCII.
        
        Args:
            mostrar_detalles: Si True, muestra alturas y FB. Si False, solo las claves.
        """
        if not self.raiz:
            return "(árbol vacío)"
        lineas: List[str] = []
        self._render_ascii(self.raiz, "", True, lineas, mostrar_detalles)
        return "\n".join(lineas)

    def _render_ascii(self, n: Optional[Nodo], prefijo: str, es_izq: bool, out: List[str], mostrar_detalles: bool = True) -> None:
        if n is None:
            return
        if n.der:
            nuevo_pref = prefijo + ("│   " if es_izq else "    ")
            self._render_ascii(n.der, nuevo_pref, False, out, mostrar_detalles)
        
        # Elegir qué mostrar en el nodo
        contenido_nodo = str(n) if mostrar_detalles else str(n.clave)
        out.append(prefijo + ("└── " if es_izq else "┌── ") + contenido_nodo)
        
        if n.izq:
            nuevo_pref = prefijo + ("    " if es_izq else "│   ")
            self._render_ascii(n.izq, nuevo_pref, True, out, mostrar_detalles)

    def ascii_simple(self) -> str:
        """Retorna string con el árbol en ASCII mostrando solo las claves."""
        return self.ascii(mostrar_detalles=False)
    
    def arbol_tradicional(self) -> str:
        """Retorna string con el árbol en formato tradicional usando / y \\."""
        if not self.raiz:
            return "(árbol vacío)"
        
        # Construir el árbol por niveles
        lineas = self._construir_arbol_con_ramas(self.raiz)
        return "\n".join(lineas) if lineas else ""
    
    def _construir_arbol_con_ramas(self, nodo: Optional[Nodo]) -> List[str]:
        """Construye el árbol con formato de ramas / y \\."""
        if not nodo:
            return []
        
        # Para árboles simples, usar un enfoque directo
        return self._arbol_con_ramas_recursivo(nodo, 0)
    
    def _arbol_con_ramas_recursivo(self, nodo: Optional[Nodo], nivel: int) -> List[str]:
        """Construye recursivamente el árbol con ramas."""
        if not nodo:
            return []
        
        # Si es una hoja
        if not nodo.izq and not nodo.der:
            return [str(nodo.clave)]
        
        valor = str(nodo.clave)
        resultado = []
        
        # Obtener subárboles
        sub_izq = self._arbol_con_ramas_recursivo(nodo.izq, nivel + 1)
        sub_der = self._arbol_con_ramas_recursivo(nodo.der, nivel + 1)
        
        # Calcular anchos
        ancho_izq = max(len(linea.rstrip()) for linea in sub_izq) if sub_izq else 0
        ancho_der = max(len(linea) for linea in sub_der) if sub_der else 0
        
        # Posición del valor
        pos_valor = ancho_izq + 1
        
        # Línea del nodo
        if sub_izq and sub_der:
            # Ambos hijos
            linea_nodo = " " * ancho_izq + valor
            resultado.append(linea_nodo)
            
            # Línea de conexiones
            linea_conexiones = " " * (ancho_izq - 1) + "/" + " " + "\\"
            resultado.append(linea_conexiones)
            
        elif sub_izq:
            # Solo hijo izquierdo
            linea_nodo = " " * ancho_izq + valor
            resultado.append(linea_nodo)
            linea_conexion = " " * (ancho_izq - 1) + "/"
            resultado.append(linea_conexion)
            
        elif sub_der:
            # Solo hijo derecho
            linea_nodo = valor + "\\"
            resultado.append(linea_nodo)
            linea_conexion = " " * len(valor) + "\\"
            resultado.append(linea_conexion)
        
        # Combinar subárboles
        max_lineas = max(len(sub_izq), len(sub_der))
        
        for i in range(max_lineas):
            linea_izq = sub_izq[i] if i < len(sub_izq) else " " * ancho_izq
            linea_der = sub_der[i] if i < len(sub_der) else ""
            
            if sub_izq and sub_der:
                linea_completa = linea_izq + " " + linea_der
            elif sub_izq:
                linea_completa = linea_izq
            else:
                linea_completa = " " * (len(valor) + 1) + linea_der
                
            resultado.append(linea_completa)
        
        return resultado

    # -------- Utilitarios --------
    def consumir_log(self) -> List[str]:
        logs = list(self._log)
        self._log.clear()
        return logs

    def recorrido_inorden(self) -> List[int]:
        res: List[int] = []
        def _in(n: Optional[Nodo]):
            if not n: return
            _in(n.izq); res.append(n.clave); _in(n.der)
        _in(self.raiz)
        return res


def escribir_lento(texto: str, velocidad: float = 0.03) -> None:
    """Escribe el texto carácter por carácter con efecto de máquina de escribir."""
    for char in texto:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(velocidad)
    print()  # Nueva línea al final


def mostrar_con_pausa(texto: str, pausa: float = 1.0) -> None:
    """Muestra el texto y hace una pausa."""
    print(texto)
    time.sleep(pausa)


def mostrar_arbol_con_efecto(arbol_texto: str, velocidad_linea: float = 0.5) -> None:
    """Muestra el árbol línea por línea con efecto de revelado."""
    lineas = arbol_texto.split('\n')
    for linea in lineas:
        print(linea)
        time.sleep(velocidad_linea)


def main() -> None:
    # Secuencia exacta pedida por la consigna
    secuencia = [10, 20, 30, 40, 50, 25]
    arbol = AVLTree()

    print("=== Inserción paso a paso en AVL (FB = altura(der) - altura(izq)) ===\n")
    for paso, x in enumerate(secuencia, start=1):
        print(f"\nPaso {paso}: insertar {x}")
        arbol.insertar(x)

        # Mostrar si hubo rotaciones o avisos
        logs = arbol.consumir_log()
        for msg in logs:
            print("  ->", msg)

        # Imprimir el árbol en formato simple
        print(arbol.ascii_simple())

    print("\nRecorrido en-orden:", arbol.recorrido_inorden())
    print("\nFin. El árbol resultante es AVL (|FB| ≤ 1 en todos los nodos).")


if __name__ == "__main__":
    main()