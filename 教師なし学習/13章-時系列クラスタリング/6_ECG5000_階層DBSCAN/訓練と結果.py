'''Main'''
import numpy as np
import pandas as pd
import os, time, re
import pickle, gzip, datetime
from os import listdir, walk
from os.path import isfile, join

'''Data Viz'''
import matplotlib.pyplot as plt
import seaborn as sns
color = sns.color_palette()
import matplotlib as mpl
from mpl_toolkits.axes_grid1 import Grid

'''Data Prep and Model Evaluation'''
from sklearn import preprocessing as pp
from sklearn.model_selection import train_test_split
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import log_loss, accuracy_score
from sklearn.metrics import precision_recall_curve, average_precision_score
from sklearn.metrics import adjusted_rand_score
import random

'''Algos'''
import tslearn
from tslearn.utils import to_time_series_dataset
from tslearn.clustering import KShape, TimeSeriesScalerMeanVariance
from tslearn.clustering import TimeSeriesKMeans
import hdbscan


# Load the datasets
current_path = os.getcwd()
file = os.path.sep.join(['', 'datasets', 'UCRArchive_2018', ''])
data_train = np.loadtxt(current_path + file + "ECG5000\\ECG5000_TRAIN.tsv")
data_test = np.loadtxt(current_path + file + "ECG5000\\ECG5000_TEST.tsv")

# trainとtestを80%, 20%に分けなおす
data_joined = np.concatenate((data_train, data_test), axis=0)
data_train, data_test = train_test_split(data_joined, test_size=0.20, random_state=2019)

X_train = to_time_series_dataset(data_train[:, 1:])
y_train = data_train[:, 0].astype(np.int)
X_test = to_time_series_dataset(data_test[:, 1:])
y_test = data_test[:, 0].astype(np.int)
file_name = "教師なし教科書\\13章-時系列クラスタリング\\6_ECG5000_階層DBSCAN\\"


# Prepare the data - Scale
X_train = TimeSeriesScalerMeanVariance(mu=0., std=1.).fit_transform(X_train)
X_test = TimeSeriesScalerMeanVariance(mu=0., std=1.).fit_transform(X_test)


# Train using k-Shape

# HDBSCAN

# Train model and evaluate on training set
min_cluster_size = 5
min_samples = None
alpha = 1.0
cluster_selection_method = 'eom'
prediction_data = True

hdb = hdbscan.HDBSCAN(min_cluster_size=min_cluster_size,
                      min_samples=min_samples, alpha=alpha,
                      cluster_selection_method=cluster_selection_method,
                      prediction_data=prediction_data)


with open(file_name + 'result.txt', 'w') as f:
    # Predict on train set and calculate adjusted Rand index
    preds = hdb.fit_predict(X_train.reshape(4000, 140))
    ars = adjusted_rand_score(data_train[:, 0], preds)
    print("Adjusted Rand Index on Training Set:", ars, file=f)

# Predict on test set and evaluate
    preds_test = hdbscan.prediction.approximate_predict(hdb, X_test.reshape(1000, 140))
    ars = adjusted_rand_score(data_test[:, 0], preds_test[0])
    print("Adjusted Rand Index on Test Set:", ars, file=f)
