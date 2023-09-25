import math
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)
import treelib
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def cuantificar_variable(dataframe, nombreVar, num_grupos=4):
    # Ordenar el DataFrame según la columna a cuantificar
    dataframe = dataframe.sort_values(by=nombreVar, ascending=True).reset_index(drop=True)
    n = len(dataframe)

    # Calcular los límites de los cuartiles
    cuartiles = [dataframe[nombreVar].quantile(i / num_grupos) for i in range(1, num_grupos)]

    for i in range(len(dataframe)):
        for j, limite in enumerate(cuartiles):
            if dataframe.at[i, nombreVar] <= limite:
                dataframe.at[i, nombreVar] = j
                break
        else:
            dataframe.at[i, nombreVar] = num_grupos - 1

    return dataframe


dataset = pd.read_excel('../datos/prestamos_bancarios_alemanes_1994.xls')
categorias_elegidas = ["Account Balance","Duration of Credit (month)", "Payment Status of Previous Credit", "Purpose", "Sex & Marital Status"]
dataset = dataset[['Creditability'] + categorias_elegidas].copy()
dataset = dataset.dropna()
dataset = cuantificar_variable(dataset, 'Duration of Credit (month)',num_grupos=4)


def entropia_shannon(data, target_atributo):
    entropia = 0
    total_records = len(data)

    unique_classes = data[target_atributo].unique()

    for unique_class in unique_classes:
        class_records = data[data[target_atributo] == unique_class]
        class_count = len(class_records)
        probabilidad = class_count / total_records
        entropia -= round(probabilidad * math.log2(probabilidad), 4)
    return entropia


def calculo_ganancia(data, target_atributo, atributo):
    # Calculamos la entropia inicial
    entropia_s = entropia_shannon(data, target_atributo)

    # Obtener los valores unico del atributo
    valores_unicos = data[atributo].unique()

    # Calculo de la suma ponderada de las entropias despues de la division
    suma_entropia = 0
    total_registro = len(data)

    for value in valores_unicos:
        subset = data[data[atributo] == value]
        subset_size = len(subset)
        entropia_subset = entropia_shannon(subset, target_atributo)
        suma_entropia += (subset_size / total_registro) * entropia_subset

    # Calculo de la ganancia
    informacion_ganancia = entropia_s - suma_entropia
    return informacion_ganancia


def buscar_mayor_ganancia(dataset, target_atributo):
    atributos = dataset.columns[1:]

    # Inicia las variables
    mejor_carateristica = None
    mejor_ganancia = -1  # inicia en valor muy bajo

    # Calcula la ganancia de informacion para cada atributo y encuentra al mejor
    for atributo in atributos:
        ganancia = calculo_ganancia(dataset, target_atributo, atributo)
    #    print(f'Ganancia de informacion para {atributo}: {ganancia}')

        if ganancia > mejor_ganancia:
            mejor_ganancia = ganancia
            mejor_carateristica = atributo

    return mejor_carateristica


class Prediction(object):
        def __init__(self, prediction):
            self.prediction = prediction

"""
GENERA SUBARBOL DE UN ATRIBUTO

dataset -> pd array, to be cropped
target_atributo -> atributo el cual queremos predecir
atributo -> atributo a expandir
atributos_restantes -> numero de atributos que no se van a usar, 0 utiliza todos los atributos, 1 utiliza todos los atributos menos 1.... tiene que ser minimo 1
:return subarbol (Tree) y DataFrame reducido (sin el atributo)
"""
def generar_subarbol(dataset: pd.DataFrame, target_atributo, atributo, atributos_restantes=1):
    #print(atributo)
    clases_restantes = list(dataset.columns)
    clases_restantes.remove(target_atributo)
    subarbol = treelib.Tree()
    nodo_atributo = subarbol.create_node(atributo,data=Prediction("?"))

    # creamos hijos para las opciones
    try:
        unique_classes = dataset[atributo].unique()
    except Exception as ex:
        #print(ex)
        if len(dataset[dataset[target_atributo] == 1]) > len(dataset[dataset[target_atributo] == 0]):
            nodo_atributo.data.prediction = "1"
        else:
            nodo_atributo.data.prediction = "0"
        return subarbol
    for c in unique_classes:
    #    print("\t ", c)
        arbol_hijo = None
        prediccion = "?"
        # calcular si resultado es positivo o negativo

        # conseguimos dataframe despues de realizar movimiento
        dataframe_parcial = dataset[dataset[atributo] == c]

        # numero de 1 en dataframe parcial
        nPositivos = len(dataframe_parcial[dataframe_parcial[target_atributo] == 1])

        # numero de 0 en dataframe parcial
        nNegativos = len(dataframe_parcial[dataframe_parcial[target_atributo] == 0])


        if len(dataframe_parcial) == nPositivos:
            prediccion = "1"
        elif len(dataframe_parcial) == nNegativos:
            prediccion = "0"
        # condiciones para parar
        elif len(clases_restantes) <= atributos_restantes:
            if nNegativos > nPositivos:
                prediccion = "0"
            else:
                prediccion = "1"
        else:
            prediccion = "?" # habrá que desarrollar el árbol
            arbol_hijo = generar_subarbol(dataframe_parcial.drop(columns=atributo), target_atributo, buscar_mayor_ganancia(dataframe_parcial, target_atributo))
            if arbol_hijo.get_node(arbol_hijo.root).data.prediction != "?":
                prediccion = arbol_hijo.get_node(arbol_hijo.root).data.prediction
                arbol_hijo = None

        nuevo_nodo = subarbol.create_node(c, data=Prediction(prediccion), parent=nodo_atributo.identifier)
        if arbol_hijo is not None:
            subarbol.paste(nuevo_nodo.identifier, arbol_hijo)

    return subarbol

def list_to_dict(lst):
    if len(lst) % 2 != 0:
        print(lst)
        raise ValueError("The list must have an even number of elements")
    result = {}
    for i in range(0, len(lst), 2):
        key = lst[i]
        value = lst[i + 1]
        result[key] = value

    return result



def predict(arbol:treelib.Tree, instancia):
    for path in arbol.paths_to_leaves():
        node_path = [arbol.get_node(n) for n in path]
        name_path = [n.tag for n in node_path]
        data_path = [n.data.prediction for n in node_path]

        instancia_path = list_to_dict(name_path)
        print(instancia_path)
        print(instancia)
        print()
        for v in instancia_path.keys():
            if instancia_path[v] != instancia[v]:
                break
        else:
            return "LOGRADO"

    return "ERROR"



def main():
    # buscamos mayor ganancía:
    target_atributo = "Creditability"


    mejor_atributo = buscar_mayor_ganancia(dataset,target_atributo)
    arbol = generar_subarbol(dataset, target_atributo, mejor_atributo)

    print(arbol.show(stdout=False, data_property="prediction"))
    print(arbol.show(stdout=False))
    #print(arbol.depth())

    # ahora que tenemos nuestro arbol, es hora de hacer predicciones

    elemento_nuevo = {
        "Account Balance": 2.0,
        "Duration of Credit (month)": 2.0,
        "Payment Status of Previous Credit": 1.0,
        "Purpose": 9.0,
        "Sex & Marital Status": 1.0
        }

    print(predict(arbol, elemento_nuevo))


import sys
import threading

main()
# if __name__ == '__main__':
#     sys.setrecursionlimit(100000)
#     threading.stack_size(200000000)
#     thread = threading.Thread(target=main)
#     thread.start()