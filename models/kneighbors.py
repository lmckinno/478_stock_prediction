import pandas
import numpy as np
from sklearn.neighbors import KNeighborsClassifier as knn
from sklearn.metrics import confusion_matrix as cm
from sklearn.feature_selection import VarianceThreshold
from sklearn.feature_selection import SelectPercentile, f_classif

### Import data
myData = pandas.read_csv("datasets/AAPLhistory_with_t+1_targets.csv")
myData = np.array(myData)
dataFeatures = myData[:, 1:-1]  # All but the first and last column
dataTargets = myData[:, -1].astype('int')  # Only last column
n = 30
print('------------------------------ n_neighbors = {0}: ------------------------------'.format(n))
model = knn(n_neighbors=n)

def runKnn(x, y, model):
  model.fit(x, y)
  preds = model.predict(x)
  confusion = cm(y, preds)
  print('confusion matrix:\n', confusion)
  tn, fp, fn, tp = confusion.ravel()
  accuracy = (tn + tp) / len(x)
  recall = tp / (fn+tp)
  precision = tp / (tp+fp)
  print('accuracy:', accuracy)
  print('recall:', recall)
  print('precision:', precision)
  print('F-measure:', 2*precision*recall/(precision + recall))
  '''
  [[true negatives, false negatives]
  [false positives, true positives]]
  '''
  return preds


### Run knn on data (full data set, no reduction of features)
print('------ unreduced, unnormalized --------')
runKnn(dataFeatures, dataTargets, model)


### Repeat with reduced feature set to see if the reduction helps
def featureVarianceReduction(x):
  print("Original x shape: ", x.shape)
  # .8 * (1 - .8) #Adjust threshold to remove more/less features
  sel = VarianceThreshold(threshold=5)
  reduced_x = sel.fit_transform(x)
  print("Reduced x shape: ", reduced_x.shape)
  return reduced_x


################This reduces the data by calculating ANOVA tests for each feature and the label, and keeping only the features with the smallest p-values.
def anovaReduction(x, y):
  print("Original x shape: ", x.shape)
  selector = SelectPercentile(f_classif, percentile=10)
  selector.fit(x, y)
  print('P values', selector.pvalues_)
  # Adjust this number for how many features we want to keep.
  smallest = np.argpartition(selector.pvalues_, 10)[:10]
  print('Smallest p values', smallest)
  reduced_x = x[:,smallest]
  print("Reduced x shape: ", reduced_x.shape)
  return reduced_x


### Repeat with reduced feature set to see if the reduction helps
print('------ feature variance reduction, unnormalized --------')
reducedFeatures = featureVarianceReduction(dataFeatures)
runKnn(reducedFeatures, dataTargets, model)
print('------ ANOVA reduction, unnormalized --------')
reducedFeatures = anovaReduction(dataFeatures, dataTargets)
runKnn(reducedFeatures, dataTargets, model)
