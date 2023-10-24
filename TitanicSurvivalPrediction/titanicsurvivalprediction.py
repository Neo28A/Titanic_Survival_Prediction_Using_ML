# -*- coding: utf-8 -*-
"""TitanicSurvivalPrediction.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Ijwkwa2WjoHvZ42G5wJ-dZ4gaPIBpLgu
"""

# @title *Importing Libraries*
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import pyplot

from warnings import filterwarnings
filterwarnings(action='ignore')

# @title *Choose Dataset from Local Directory*"""
from google.colab import files
uploaded = files.upload()

# @title *Load Dataset*"""
dataset = pd.read_csv('titanicsurvival.csv')

# @title *Summarize Dataset*"""
print(dataset.shape)
print(dataset.head(5))

# @title Analyzing the dataset
male_psg = len(dataset[dataset['Sex'] == 'male'])
print("No of Males on Titanic:",male_psg)

female_psg = len(dataset[dataset['Sex'] == 'female'])
print("No of Females on Titanic:",female_psg)

fig = plt.figure()
ax = fig.add_axes([0,0,1,1])
gender = ['Male','Female']
index = [577,314]
ax.bar(gender,index)
plt.xlabel("Gender")
plt.ylabel("No of cruiser onboarding Titanic")
plt.show()

survived = len(dataset[dataset['Survived'] == 1])
dead = len(dataset[dataset['Survived'] == 0])

fig = plt.figure()
ax = fig.add_axes([0,0,1,1])
status = ['Survived','Dead']
ind = [survived,dead]
ax.bar(status,ind)
plt.xlabel("Status")
plt.show()

dataset.groupby('Sex')[['Survived']].mean()

"""Female Passsengers survived more than male passengers acc to above data"""

dataset[["Pclass", "Survived"]].groupby(['Pclass'], as_index=False).mean().sort_values(by='Survived', ascending=False)

"""Pclass 1 as more survivel rate then other two Pclass acc above data"""

plt.figure(1)
dataset.loc[dataset['Survived'] == 1, 'Pclass'].value_counts().sort_index().plot.bar()
plt.title('Bar graph of cruiser who survived accrding to ticket class ')

plt.figure(2)
dataset.loc[dataset['Survived'] == 0, 'Pclass'].value_counts().sort_index().plot.bar()
plt.title("Bar graph of cruiser who couldn't survive accrding to ticket class")

# @title *Mapping Text Data to Binary Value*"""
income_set = set(dataset['Sex'])
dataset['Sex'] = dataset['Sex'].map({'female' : 0, 'male' : 1}).astype(int)
print(dataset.head(5))

# @title *Segregate Dataset into X(Input/IndependentVariable) & Y(Output/DependentVariable)*"""
X = dataset.drop('Survived', axis = 'columns')
X

# @title Y(Output/DependentVariable)
Y = dataset.Survived
Y

# @title Finding & Removing NA values from our Features X
X.columns[X.isna().any()]

"""Age column as NaN/Null values"""

X.Age = X.Age.fillna(X.Age.mean())

"""Repalce NaN with mean of that column"""

# @title Test again to check any na value
X.columns[X.isna().any()]

"""No other Null values found"""



# @title Splitting Dataset into Train & Test
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, Y, train_size=0.25, random_state=0)

# @title *Validating some ML algorithm by its accuracy - Model Score*
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC

from sklearn.model_selection import cross_val_score
from sklearn.model_selection import StratifiedKFold

models = []
models.append(('LR', LogisticRegression(solver='liblinear', multi_class='ovr')))
models.append(('KNN', KNeighborsClassifier()))
models.append(('CART', DecisionTreeClassifier()))
models.append(('NB', GaussianNB()))
models.append(('SVM', SVC(gamma='auto')))

results = []
names = []
res = []
for name, model in models:
    kfold = StratifiedKFold(n_splits=10, random_state=None)
    cv_results = cross_val_score(model, X_train, y_train, cv=kfold, scoring='accuracy')
    results.append(cv_results)
    names.append(name)
    res.append(cv_results.mean())
    print('%s: %f' % (name, cv_results.mean()))

pyplot.ylim(.600, .999)
pyplot.bar(names, res, color ='maroon', width = 0.6)

pyplot.title('Algorithm Comparison')
pyplot.show()

# @title *Training & Prediction using the algorithm with high accuracy*
from sklearn.linear_model import LogisticRegression
model = LogisticRegression()
model.fit(X_train, y_train)
y_pred = model.predict(X_test)

from sklearn.metrics import accuracy_score,confusion_matrix
print("Accuracy Score:",accuracy_score(y_test,y_pred))
cn = confusion_matrix(y_test, y_pred)
print("Confusion Matrix")
print(cn)

pclassNo = int(input("Enter Person's Pclass number: "))
gender = int(input("Enter Person's Gender 0-female 1-male(0 or 1): "))
age = int(input("Enter Person's Age: "))
fare = float(input("Enter Person's Fare: "))
person = [[pclassNo,gender,age,fare]]
result = model.predict(person)
print(result)

if result == 1:
  print("Person might be Survived")
else:
  print("Person might not be Survived")

"""#Hence I will use LogisticRegression algorithms for training my model."""
