import pandas as pd #for manipulating the csv data
import numpy as np #for mathematical calculation

train_data_m = pd.read_excel("../datos/prestamos_bancarios_alemanes_1994.xls") #importing the dataset from the disk
train_data_m = train_data_m.dropna()

categorias_elegidas = ["Account Balance","Duration of Credit (month)", "Payment Status of Previous Credit", "Purpose", "Sex & Marital Status"]
train_data_m = train_data_m[['Creditability'] + categorias_elegidas].copy()

def calc_total_entropy(train_data, label, class_list):
    total_row = train_data.shape[0]  # the total size of the dataset
    total_entr = 0

    for c in class_list:  # for each class in the label
        total_class_count = train_data[train_data[label] == c].shape[0]  # number of the class
        total_class_entr = - (total_class_count / total_row) * np.log2(
            total_class_count / total_row)  # entropy of the class
        total_entr += total_class_entr  # adding the class entropy to the total entropy of the dataset

    return total_entr


def calc_entropy(feature_value_data, label, class_list):
    class_count = feature_value_data.shape[0]
    entropy = 0

    for c in class_list:
        label_class_count = feature_value_data[feature_value_data[label] == c].shape[0]  # row count of class c
        entropy_class = 0
        if label_class_count != 0:
            probability_class = label_class_count / class_count  # probability of the class
            entropy_class = - probability_class * np.log2(probability_class)  # entropy
        entropy += entropy_class
    return entropy


def calc_info_gain(feature_name, train_data, label, class_list):
    feature_value_list = train_data[feature_name].unique()  # unqiue values of the feature
    total_row = train_data.shape[0]
    feature_info = 0.0

    for feature_value in feature_value_list:
        feature_value_data = train_data[
            train_data[feature_name] == feature_value]  # filtering rows with that feature_value
        feature_value_count = feature_value_data.shape[0]
        feature_value_entropy = calc_entropy(feature_value_data, label,
                                             class_list)  # calculcating entropy for the feature value
        feature_value_probability = feature_value_count / total_row
        feature_info += feature_value_probability * feature_value_entropy  # calculating information of the feature value

    return calc_total_entropy(train_data, label, class_list) - feature_info  # calcula


def find_most_informative_feature(train_data, label, class_list):
    feature_list = train_data.columns.drop(label)  # finding the feature names in the dataset
    # N.B. label is not a feature, so dropping it
    max_info_gain = -1
    max_info_feature = None

    for feature in feature_list:  # for each feature in the dataset
        feature_info_gain = calc_info_gain(feature, train_data, label, class_list)
        if max_info_gain < feature_info_gain:  # selecting feature name with highest information gain
            max_info_gain = feature_info_gain
            max_info_feature = feature

    return max_info_feature


def generate_sub_tree(feature_name, train_data, label, class_list):
    feature_value_count_dict = train_data[feature_name].value_counts(sort=False)  # dictionary of the count of unqiue feature value
    tree = {}  # sub tree or node

    for feature_value, count in feature_value_count_dict.items():
        feature_value_data = train_data[
            train_data[feature_name] == feature_value]  # dataset with only feature_name = feature_value

        assigned_to_node = False  # flag for tracking feature_value is pure class or not
        for c in class_list:  # for each class
            class_count = feature_value_data[feature_value_data[label] == c].shape[0]  # count of class c

            if class_count == count:  # count of (feature_value = count) of class (pure class)
                tree[feature_value] = c  # adding node to the tree
                train_data = train_data[train_data[feature_name] != feature_value]  # removing rows with feature_value
                assigned_to_node = True
        if not assigned_to_node:  # not pure class
            tree[feature_value] = "?"  # as feature_value is not a pure class, it should be expanded further,
            # so the branch is marking with ?

    return tree, train_data


def make_tree(root, prev_feature_value, train_data, label, class_list):
    if train_data.shape[0] != 0:  # if dataset becomes enpty after updating
        max_info_feature = find_most_informative_feature(train_data, label, class_list)  # most informative feature
        tree, train_data = generate_sub_tree(max_info_feature, train_data, label,class_list)  # getting tree node and updated dataset
        next_root = None

        if prev_feature_value != None:  # add to intermediate node of the tree
            root[prev_feature_value] = dict()
            root[prev_feature_value][max_info_feature] = tree
            next_root = root[prev_feature_value][max_info_feature]
        else:  # add to root of the tree
            root[max_info_feature] = tree
            next_root = root[max_info_feature]

        for node, branch in list(next_root.items()):  # iterating the tree node
            if branch == "?":  # if it is expandable
                feature_value_data = train_data[train_data[max_info_feature] == node]  # using the updated dataset
                make_tree(next_root, node, feature_value_data, label, class_list)  # recur


def id3(train_data_m, label):
    train_data = train_data_m.copy() #getting a copy of the dataset
    tree = {} #tree which will be updated
    class_list = train_data[label].unique() #getting unqiue classes of the label
    make_tree(tree, None, train_data, label, class_list) #start calling recursion
    return tree


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


train_data_m = cuantificar_variable(train_data_m, 'Duration of Credit (month)', num_grupos=4)


tree = id3(train_data_m, 'Creditability')
print(tree)
