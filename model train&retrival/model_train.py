# coding: utf-8

import pandas as pd
import tensorflow as tf
from tensorflow.keras import layers
import numpy as np
from sklearn.model_selection import train_test_split
from matplotlib import pyplot as plt
np.set_printoptions(suppress = True)

def get_valloss(model,x,y,flag = 0):
    pred = model.predict(x)
    if flag:
        return ((pred - y)**2).mean(axis = 0)**0.5
    else:
        return ((pred - y)**2).mean()**0.5
    
def get_mean_err(model,x,y,flag = 0):
    pred = model.predict(x)
    if flag:
        return (pred - y).mean(axis = 0)
    else:
        return (pred - y).mean()
    
def deleteBigErr(model,samples,modelname, maxerr = 5):
    pred = model.predict(samples[:,0:17])
    if modelname == 'T':
        result = abs(pred - samples[:,17:64]).mean(axis = 1)
    elif modelname == 'H':
        result = abs(pred - samples[:,64:111]).mean(axis = 1)
    idx = np.where(result > maxerr)[0]
    samples = np.delete(samples,idx,axis=0)
    return samples

def get_train_samples(path_bt_mono, path_soundings, test_size = 0.2):
    '''
    traindata是之前准备好的
    bt_mono: 14 channels & T(K) P H
    '''
    data_bt_mono = pd.read_excel(path_bt_mono,index_col=0)
    data_soundings = pd.read_excel(path_soundings)
#     索引温、湿度所对应的列
    index_t = list(range(2, data_soundings.shape[1], 4))
    index_h = list(range(3, data_soundings.shape[1], 4))

    data_soundings_t = data_soundings.values[:,index_t]
    data_soundings_h = data_soundings.values[:,index_h]
    # 合并&调换位置
    samples = np.r_[data_bt_mono, data_soundings_t, data_soundings_h].T
#     T(°C) H P & 14 channels
    samples = samples[:,[14,16,15] + list(range(14)) + list(range(17,111))]
    samples[:,0] -= 273.15 
    # 去掉 nan
    idx = np.where(np.isnan(samples[:,3]))[0][0]
    samples = np.delete(samples, idx,axis= 0)
    # 交叉检验
    data_train, data_test = train_test_split(samples, test_size = test_size, random_state = 10, shuffle = True)
    return data_train, data_test


def train(data_train, data_test, name, loss = 'mean_absolute_error'):
    '''
    train model T or H
    '''
    if name == 'T':
        idx = list(range(17,64))
    elif name == 'H':
        idx = list(range(64,111))
    else:
        print('name error')
        return None
    # 建模
    inputs = layers.Input(shape=(17,),name = 'inputs')
    hidden_1 = layers.Dense(24,activation= 'linear',name = 'hidden_1')(inputs)
    dropout_1 = layers.Dropout(0.2,seed= 10,name = 'dropout_1')(hidden_1)
    outputs = layers.Dense(47,activation='linear',name = 'outputs')(dropout_1)

    model = tf.keras.Model(inputs= inputs,outputs= outputs,name = name)
    # 模型摘要
    model.summary()
    # 模型编译
    model.compile(optimizer= tf.keras.optimizers.Adam(learning_rate= 0.001),
                  loss= loss,
                  metrics= [])
    # 训练记录
    history = model.fit(x = data_train[:,:17],
                        y = data_train[:,idx],
                        batch_size = None,
                        validation_data= (data_test[:,:17],data_test[:,idx]),
                        epochs= 5000,
                        verbose= 1,
                        callbacks= [tf.keras.callbacks.EarlyStopping(monitor= 'val_loss',
                                                                     patience= 10,
                                                                     restore_best_weights= True)])
    return model


if __name__ == '__main__':
    path_bt_mono = r'traindata/1317(BT_mono).xlsx'
    path_soundings = r'traindata/1317_54511(插值后)_long.xlsx'
    modelname = 'H'
    maxerr = 25
    pathOut = r'model/' + modelname + '.hdf'
    data_train, data_test = get_train_samples(path_bt_mono, path_soundings, test_size= 0.2)
#     for i in range(3):
#         model = train(data_train, data_test, name= 'model_T', loss = 'mean_absolute_error')
#         data_train = deleteBigErr(model, data_train, modelname= 'T')
    model = train(data_train, data_test, name= modelname, loss = 'mean_absolute_error')
    data_train = deleteBigErr(model, data_train, modelname= modelname,maxerr= maxerr)
    data_test = deleteBigErr(model, data_test, modelname= modelname, maxerr= maxerr)
    model = train(data_train, data_test, name= modelname, loss= 'mean_squared_error')
    model.save(pathOut)

