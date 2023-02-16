from operator import truth
import numpy as np
import pandas as pd

from elasticsearch_dsl import Search
from sklearn.metrics import *


# Creating function for read data from Elasticsearch
def read_from_elastic(index, es):
    s = Search().using(es).index(index)
    s_fields = s.source(["timestamp", "systemcall", "process_id", "argc", "args_length", "value"])   
    df_from_elastic = pd.DataFrame([hit.to_dict() for hit in s_fields.scan()])
    # Sorting dataframe by timestamp field
    df_from_elastic.sort_values(by='timestamp', inplace=True, ignore_index=True)
    # Reordering dataframe columns
    df_from_elastic = df_from_elastic[['timestamp', 'systemcall', 'process_id', 'argc', "args_length", 'value']]
    #df_from_elastic[['systemcall', 'args_length', 'value']] = df_from_elastic[['systemcall', 'args_length', 'value']].apply(pd.to_numeric)
    return df_from_elastic


# Defining function to create array with sliding windows
def sliding_window(X, window_size):
    X1 = []
    for i in range(len(X) - window_size+1):     #Range(9)   --> print de 0 a 8
        t = X.iloc[i:(i + window_size)].values  #iloc(0:9)  --> seleciona de 0 a 8
        X1.append(t) 
    return np.array(X1)


# Defining function to create array with sliding windows with steps = window_size
def sliding_window_fast(X, window_size):
    X1 = []
    i = 0
    j = int(len(X) / window_size)                   # Qtd de windows
    r = (len(X) % window_size)                      # Resto
    if (r == 0):                                    
        for k in range(j):                          # Range(9)   --> print de 0 a 8
            t = X.iloc[i:(i + window_size)].values  # iloc(0:9)  --> seleciona de 0 a 8
            X1.append(t)
            i = i + window_size                     # Steps do tamanho do window_size
    else:                                           # Se qtd de windows não for inteira (resto != 0)
        for k in range(int((j))):                     
            t = X.iloc[i:(i + window_size)].values  
            X1.append(t)
            i = i + window_size                   
        t = X.iloc[(i - (window_size - r)):((i - (window_size - r)) + window_size)].values    # Repete valores na última janela até completar window_size
        X1.append(t)   
    return np.array(X1)



# Defining function to create dataframe with windows losses
def window_loss(w, threshold):
    wt = pd.DataFrame(columns = ['window_number', 'loss', 'anomaly', 'real'])
    window_number = []
    anomalies = []
    for i in range(len(w)):
        window_number.append(i)
        anomalies.append(w['Loss_mae'][i] > threshold)
    wt['window_number'] = window_number
    wt['loss'] = w['Loss_mae']
    wt['anomaly'] = anomalies
    wt['real'] = w['real']
    return (wt)


# Defining function for tunable threshold 
# Originally proposed by: Cui, P., Umphress, D. (2020). Towards unsupervised introspection of containerized application. ACM International Conference Proceeding Series, 42–51. https://doi.org/10.1145/3442520.3442530
def tunable_threshold(df_train_loss, confidence_levels):
    T = pd.DataFrame(columns=confidence_levels)
    Tmax = np.round(df_train_loss['Loss_mae'].max(), 4)
    for i in confidence_levels:
        Tc = Tmax
        while  (np.round(df_train_loss[df_train_loss['Loss_mae'] < Tc]['Loss_mae'].count() / df_train_loss['Loss_mae'].count(), 3) > i):
            Tc = Tc * 0.99
        T.at[0,i] = np.round(Tc, 4)
    return T

def metrics(df_results):
    # Confusion Matrix
    cm = confusion_matrix(df_results['real'], df_results['anomaly'])
    
   # Primary Results
    #TP = sum(df_results[df_results['real'] == True]['anomaly'] == df_results[df_results['real'] == True]['real'])
    #TN = sum(df_results[df_results['real'] == False]['anomaly'] == df_results[df_results['real'] == False]['real'])
    #FP = sum(df_results[df_results['real'] == False]['anomaly'] != df_results[df_results['real'] == False]['real'])
    #FN = sum(df_results[df_results['real'] == True]['anomaly'] != df_results[df_results['real'] == True]['real'])
    
    tn = cm[0,0]
    fp = cm[0,1]
    fn = cm[1,0]
    tp = cm[1,1]

    # Accuracy
    accuracy = (tp + tn) / (tp + tn + fp + fn)
    
    # Precision = tp / (tp + fp)
    precision = precision_score(df_results['real'], df_results['anomaly'])
        
    # TPR ou Recall =  tp / (tp + fn)
    tpr = recall_score(df_results['real'], df_results['anomaly'])
    
    # NPV = tn / (tn + fn)
    npv = tn / (tn + fn)

    # TNR ou Especificidade = tn / (tn + fp)
    tnr = tn / (tn + fp)

    # FPR ou FAR = fp / (tn + fp)
    fpr = fp / (tn + fp)

    # F1 Score = 2 * (precision * tpr) / (precision + tpr)
    f1 = f1_score(df_results['real'], df_results['anomaly'])

    # AUC (ROC Curve)
    fpr_roc, tpr_roc, thresholds_roc = roc_curve(df_results['real'], df_results['anomaly'])
    roc_auc = auc(fpr_roc, tpr_roc)
    
    return cm, accuracy, precision, tpr, npv, tnr, fpr, f1, roc_auc
