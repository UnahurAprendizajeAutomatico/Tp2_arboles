from matplotlib import pyplot as plt

from utils.arbol.arbol import Arbol


def __main__():
    arbol = Arbol(1)
    arbol.agregar_nodo(1, 3)
    arbol.agregar_nodo(1, 5)
    arbol.agregar_nodo(3, 7)
    arbol.agregar_nodo(1, 9)

    arbol.imprimir_arbol()


if __name__ == '__main__':
    __main__()
