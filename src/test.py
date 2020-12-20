import numpy as np
import pandas as pd

from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.neural_network import MLPClassifier
import pickle

def confusion(true, pred, classes):
    cm = pd.DataFrame(confusion_matrix(true, pred), index = classes, columns = classes)
    cm.index.name = 'Actual'
    cm.columns.name = 'Predicted'
    return cm


file = open("model_1.pickle", 'rb')
model = pickle.load(file)

data = pd.read_csv("data/processed/data1.csv", header=0, delimiter=',')

X_test = data.loc[:, 'sex':]

X_real = data['covid'].tolist()

pred = model.predict(X_test)

print('Confusion matrix for ill children c:')
print(confusion(X_real, pred, ['covid', 'no_covid']))
print('--------------------------------------------')

print('Confusion matrix for healthy children :c')

file = open("model_2.1.pickle", 'rb')
model = pickle.load(file)

data = pd.read_csv("data/processed/data_nBC.csv", header=0, delimiter=',')
X_test = data.loc[:, 'sex':]
X_real = data['covid'].tolist()

pred = model.predict(X_test)
print(confusion(X_real, pred, ['covid', 'no_covid']))
