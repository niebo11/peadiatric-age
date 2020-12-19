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

    '''
    for no comorbity:
        n: 38
        alpha: 0.011220184543019538
    '''

data = pd.read_csv("data/processed/data1.csv", header=0, delimiter=',')

# Suposarem que la primera columna es el covid result
# camps a omplir
X_train, X_test, y_train, y_test = train_test_split(data.loc[:, 'sex':], data.covid,
                                                    test_size=0.33)

sizes = [2*i for i in range(1, 25)]

decays = [10**i for i in np.arange(-3, 0, 0.05)]

model_net = MLPClassifier(alpha=0, activation='logistic', max_iter=500, solver='lbfgs')

trc = GridSearchCV(estimator=model_net, param_grid={'hidden_layer_sizes': sizes},
                   cv=10, return_train_score=True)

model_10CV = trc.fit(X_train, y_train)

hidden_layer_size = model_10CV.best_params_['hidden_layer_sizes']

model_net2 = MLPClassifier(alpha=0, activation='logistic', hidden_layer_sizes=hidden_layer_size, max_iter=1000,
                           solver='lbfgs')

trc = GridSearchCV(estimator=model_net2, param_grid={'alpha': decays}, cv=10, return_train_score=True)

model_10CV_final = trc.fit(X_train, y_train)

pred = model_10CV_final.predict(X_test)

print((1 - accuracy_score(y_test, pred))*100)

print(confusion(y_test, pred, ['covid', 'no_covid']))

pickle.dump(model_10CV_final, open("model_1.pickle", 'wb'))
