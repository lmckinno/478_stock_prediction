import pandas
import numpy as np
from sklearn.neighbors import KNeighborsClassifier as knn
from sklearn.metrics import confusion_matrix as cm

### Import data
myData = pandas.read_csv("datasets/AAPLhistory_with_t+1_targets.csv")
myData = np.array(myData)
dataFeatures = myData[:, 1:-1]  # All but the first and last column
dataTargets = myData[:, -1].astype('int')  # Only last column

### Run knn on data (full data set, no reduction of features)
model = knn(n_neighbors=5)
model.fit(dataFeatures, dataTargets)
preds = model.predict(dataFeatures)
diff = dataTargets - preds
misclassified = len(diff[diff != 0])
confusion = cm(dataTargets, preds) 
print('confusion matrix:', confusion)
#0,0 = true negatives
#0,1 = false positives
#1,0 = false negatives
#1,1 = true positives

### Repeat with reduced feature set to see if the reduction helps
# .8 * (1 - .8) #Adjust threshold to remove more/less features
sel = VarianceThreshold(threshold=5)
reducedFeatures = sel.fit_transform(dataFeatures)
