# coding: utf-8

import pandas as pd
import tensorflow as tf

def retrival(data_lv1, model_T, model_H):
    '''
    return: profile of T & H
    '''
    lv1_corrected = data_lv1.values[:,1:]
    dates = data_lv1.values[:,0]
    T = model_T.predict(lv1_corrected)
    H = model_H.predict(lv1_corrected)
    return np.c_[dates, T, H]


if __name__ == '__main__':
    stationNum = '54399'
    pathLv1 = r'F:/data/beijing2018/LV/LV1/lv1_corrected/' + stationNum + '_corrected.csv'
    pathModel_T = r'model/T.hdf'
    pathModel_H = r'model/H.hdf'
    pathOut = r'F:/data/beijing2018/LV/LV1/profile/' + stationNum + '_retrieved.csv'
    model_T = tf.keras.models.load_model(pathModel_T)
    model_H = tf.keras.models.load_model(pathModel_H)
    lv1_corrected = pd.read_csv(pathLv1,header= None)
    profile = retrival(lv1_corrected, model_T, model_H)
    pd.DataFrame(profile, columns= None).to_csv(pathOut, index = None, header = None)

