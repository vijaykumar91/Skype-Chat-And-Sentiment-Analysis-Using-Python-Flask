# Simple Linear Regression

# Importing the libraries
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from array import array


from sklearn.cross_validation import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
from sklearn import tree

import sys
# Importing the dataset
dataset = pd.read_csv('DataSet.csv')
X = dataset.iloc[:20, 15].values.reshape(-1,1)
y = dataset.iloc[:20, 13].values.reshape(-1,1)
new=[]
new2=[]
for line in y:
    new3=[]
    new3.append(float(line))
    new.append(new3)
    # for line2 in line:
    #     print(line2.replace("'", ""))
    #     new2.append(float(line2.replace("'", "")))
y=new
# Splitting the dataset into the Training set and Test set
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y,  test_size=0.33, random_state = 0)


# Feature Scaling
"""from sklearn.preprocessing import StandardScaler
sc_X = StandardScaler()
X_train = sc_X.fit_transform(X_train)
X_test = sc_X.transform(X_test)
sc_y = StandardScaler()
y_train = sc_y.fit_transform(y_train)"""

# Fitting Simple Linear Regression to the Training set
from sklearn.linear_model import LinearRegression
regressor = LinearRegression()
regressor.fit(X_train, y_train)

# Predicting the Test set results
y_pred = regressor.predict(X_test)

# Visualising the Training set results
#plt.scatter(X_train, y_train, color = 'red')
plt.plot(X_train, regressor.predict(X_train), color = 'blue')

# Visualising the Test set results
plt.scatter(X_train, y_train,marker='*', color = 'red')
plt.plot(X_train, regressor.predict(X_train), color = 'blue')
plt.title('Travel Time vs Fare (Test set)')
plt.xlabel('Delivery Fare')
plt.ylabel('Travel Time')
plt.show()


