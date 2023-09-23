import graphviz
import datetime
from utils.arbol.nodo import Nodo


class ArbolN:
    def __init__(self, raiz_data):
        self.raiz = Nodo(raiz_data)

    def agregar_hijo(self,  nodo_padre, hijo_data):
        new_nodo = Nodo(hijo_data)
        nodo_padre.hijos.append(new_nodo)

    def visualizar(self):
        def generar_grafo(node, dot=None):
            if dot is None:
                dot = graphviz.Digraph( format='png')

            dot.node(str(node.data))
            for child in node.hijos:
                dot.edge( str( node.data), str(child.data))
                generar_grafo( child, dot)

            return dot

        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")  # Obtener una marca de tiempo única
        archivo_salida = f"output/arbol_nario_{timestamp}"

        dot = generar_grafo(self.raiz)
        dot.render( "grafico/arbol", view=False)


if __name__ == '__main__':
    print(f'Hola, soy el archivo {__name__} y estoy ejecutando como programa principal')


# Crear un árbol n-ario
my_tree = ArbolN("Raíz")

# Agregar hijos
my_tree.agregar_hijo(my_tree.raiz, "Hijo 1")
my_tree.agregar_hijo(my_tree.raiz, 'hijo 2')
my_tree.agregar_hijo(my_tree.raiz, 'hijo 3')

my_tree.agregar_hijo(my_tree.raiz.hijos[0], 'A')
my_tree.agregar_hijo(my_tree.raiz.hijos[1], 'B')
my_tree.agregar_hijo(my_tree.raiz.hijos[2], 'C')

my_tree.agregar_hijo(my_tree.raiz.hijos[2], 'F')

my_tree.agregar_hijo(my_tree.raiz.hijos[2], 'g')
# Imprimir el árbol
my_tree.visualizar()

