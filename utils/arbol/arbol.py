from matplotlib.patches import FancyArrowPatch

from utils.arbol import nodo
from utils.arbol.nodo import NodoArbol
import matplotlib.pyplot as plt


class Arbol:
    def __init__ ( self,valor_raiz ):
        # Creacion del nodo raiz
        self.raiz = NodoArbol ( valor_raiz )

    def agregar_nodo ( self,nodo_padre,nodo_hijo ):
        nuevo_nodo = NodoArbol ( nodo_hijo )
        nodo_padre = self.buscar_nodo ( nodo_padre )
        if nodo_padre:
            nodo_padre.hijos.append ( nuevo_nodo )
        else:
            print ( f'No se encontro el nodo con el valor {nodo_padre}' )

    def buscar_nodo ( self,valor,nodo=None ):

        if nodo is None:
            nodo = self.raiz
        if nodo.valor == valor:
            return nodo
        for hijo in nodo.hijos:
            nodo_encontrado = self.buscar_nodo ( valor,hijo )
            if nodo_encontrado:
                return nodo_encontrado
        return nodo_encontrado

    def imprimir_arbol( self, nodo=None, nivel=0 ):
        if nodo is None:
            nodo = self.raiz
        print ( " " * nivel,str ( nodo.valor ) )
        for hijo in nodo.hijos:
            self.imprimir_arbol ( hijo,nivel + 1 )