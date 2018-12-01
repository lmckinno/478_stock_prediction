#! /usr/bin/env python
import pandas
import numpy as np
from sklearn.feature_selection import VarianceThreshold
from sklearn.feature_selection import SelectPercentile, f_classif

print("Feature reduction")
myData = pandas.read_csv("datasets/AAPLhistory_with_t+1_targets.csv")
myData = np.array(myData)
dataFeatures = myData[:,1:-1] #All but the first and last column
dataTargets = myData[:,-1] #Only last column


###############This reduces the data using variance, meaning that it removes features based on if the data points have a low amount of variance.
print("Num features: ", dataFeatures.shape)
sel = VarianceThreshold(threshold=5) #.8 * (1 - .8) #Adjust threshold to remove more/less features
reducedFeatures = sel.fit_transform(dataFeatures)
print("Num reduced features: ", reducedFeatures.shape)


################This reduces the data by calculating ANOVA tests for each feature and the label, and keeping only the features with the smallest p-values.
X, y = reducedFeatures, dataTargets
#print(X.shape)
selector = SelectPercentile(f_classif, percentile=10)
selector.fit(X, y)
print(selector.pvalues_)
smallest = np.argpartition(selector.pvalues_, 10)[:10] #Adjust this number for how many features we want to keep.
print(smallest)
#print(reducedFeatures[smallest])
superReducedFeatures = reducedFeatures[smallest]


