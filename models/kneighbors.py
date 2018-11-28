import pandas
import numpy as np
from sklearn.neighbors import KNeighborsClassifier as knn

### Import data
myData = pandas.read_csv("datasets/AAPLhistory_withTargets.csv")
myData = np.array(myData)
dataFeatures = myData[:, 1:-1]  # All but the first and last column
dataTargets = myData[:, -1]  # Only last column

### Run knn on data (full data set, no reduction of features)
model = knn(n_neighbors=5)
model.fit(dataFeatures, dataTargets)
print(model.predict(dataFeatures[1]))


### Repeat with reduced feature set to see if the reduction helps
