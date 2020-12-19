import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.neural_network import MLPClassifier
import pickle

data = pd.read_csv("data/processed/data_BC.csv", header=0, delimiter=',')

# Suposarem que la primera columna es el covid result
# camps a omplir
X_train, X_test, y_train, y_test = train_test_split(data.loc[:, 'omplir segona columna'], data.covid,
                                                    test_size=0.33)

sizes = [2*i for i in range(1, 25)]

decays = [10*i for i in np.arange(-3, 0, 0.05)]

model_net = MLPClassifier(alpha=0, activation='logistic', max_iter=500, solver='lbfgs')

trc = GridSearchCV(estimator=model_net, param_grid={'hidden_layer_size': sizes, 'alpha': decays},
                   cv=10, return_train_score=True)

model_10CV = trc.fit(X_train, y_train)

pickle.dump(model_10CV, open("model.pickle", 'wb'))
