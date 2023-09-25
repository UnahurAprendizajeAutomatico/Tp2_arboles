import graphviz
import datetime
from utils.arbol.nodo import Nodo


class ArbolN:
    def __init__(self, raiz_data):
        self.raiz = Nodo(raiz_data)

    def agregar_hijo(self,  nodo_padre, hijo_data):
        new_nodo = Nodo(hijo_data)
        nodo_padre.hijos.append(new_nodo)

    def construir_arbol( self, nodo, hijos):
        if not hijos:
            return
        for nombre_hijo in hijos:
            self.agregar_hijo(nodo, nombre_hijo)

        for i, hijo in enumerate(nodo.hijos):
            self.construir_arbol(hijo, hijos[i + 1:])

    def visualizar(self):
        def generar_grafo(node, dot=None):
            if dot is None:
                dot = graphviz.Digraph( format='png')

            dot.node(str(node.data))
            for child in node.hijos:
                dot.edge( str( node.data), str(child.data))
                generar_grafo( child, dot)

            return dot

        timestamp = datetime.datetime.now().strftime("%H%M")  # Obtener una marca de tiempo única
        archivo_salida = f"grafico/arbol_{timestamp}"

        dot = generar_grafo(self.raiz)
        dot.render( archivo_salida, view=False)


if __name__ == '__main__':
    print(f'Hola, soy el archivo {__name__} y estoy ejecutando como programa principal')


# Crear un árbol de ejemplo
mi_arbol = ArbolN("Raíz")

# Definir una lista de nombres de hijos para cada nodo
nombres_hijos = [
    ['H1', 'H2', 'H3', 'H4'],    # Nodos hijos del nodo raíz
    ['1m', '2m', '3m'],         # Nodos hijos de H1
    ['1m', '2m', '3m'],         # Nodos hijos de H2
    ['Unico'],                  # Nodos hijo de H3
    [],                         # H4 no tiene hijos
]

# Construir el árbol de forma recursiva
# Agregar hijos directos a la raíz (h1, h2, h3, h4)
# Crear un árbol de ejemplo
mi_arbol = ArbolN("Raíz")

# Agregar hijos directos a la raíz (h1, h2, h3, h4)
hijos_raiz = ["H1", "H2", "H3", "H4"]
mi_arbol.construir_arbol(mi_arbol.raiz, hijos_raiz)

# Agregar hijos a H1 (1m, 2m, 3m)
hijos_h1 = ["1m", "2m", "3m"]
mi_arbol.construir_arbol(mi_arbol.raiz.hijos[0], hijos_h1)

# Agregar hijos a H2 (1m, 2m, 3m)
hijos_h2 = ["1m", "2m", "3m"]
mi_arbol.construir_arbol(mi_arbol.raiz.hijos[1], hijos_h2)

# Agregar un hijo a H3 (Unico)
hijo_h3 = ["Unico"]
mi_arbol.construir_arbol(mi_arbol.raiz.hijos[2], hijo_h3)


# Imprimir el árbol
mi_arbol.visualizar()

