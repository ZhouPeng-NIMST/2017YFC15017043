
# coding: utf-8


import numpy as np
import pandas as pd
import os 


def get_correct(data):
    '''
    calculate correct w/b by data of lv1&mono
    return: a dict of months' w/b
    '''
    idx_mon_1 = {'2018-01':-1,'2018-02':-1,'2018-03':-1,'2018-04':-1,'2018-05':-1,
                 '2018-06':-1,'2018-07':-1,'2018-08':-1,'2018-09':-1,'2018-10':-1}

    ewb_mon = {'2018-01':[-1,-1,-1],'2018-02':[-1,-1,-1],'2018-03':[-1,-1,-1],'2018-04':[-1,-1,-1],'2018-05':[-1,-1,-1],
              '2018-06':[-1,-1,-1],'2018-07':[-1,-1,-1],'2018-08':[-1,-1,-1],'2018-09':[-1,-1,-1],'2018-10':[-1,-1,-1]}

    # record ids of every month
    for i , date in enumerate(data.iloc[:,0]):
        if date[:7] in idx_mon_1:
            if idx_mon_1[date[:7]] == -1:
                idx_mon_1[date[:7]] = i
            else:
                continue
    # calculate correct w/b
    last_mon = ''
    for o in idx_mon_1:
        e = []
        w = []
        b = []
        idx = idx_mon_1[o]
        if idx != -1:
            lv1, mono = data.iloc[idx-60:idx,1:18].values, data.iloc[idx-60:idx,19:].values
#             lv1, mono = data.iloc[:,1:18].values, data.iloc[:,19:].values
            # delete some error data
            abs_err = abs(lv1[:,9] - mono[:,9])
            idx_del = np.where(abs_err >= 0.95*(abs_err.max()))[0]
            lv1 = np.delete(lv1,idx_del,axis = 0)
            mono = np.delete(mono,idx_del,axis = 0)
            for j in range(17):
                e_j = mono[:,j].mean() - lv1[:,j].mean()
                f = np.polyfit(lv1[:,j] + e_j, mono[:,j],1)
                e.append(e_j)
                w.append(f[0])
                b.append(f[1])
            ewb_mon[o][0] = e
            ewb_mon[o][1] = w
            ewb_mon[o][2] = b
            last_mon = o
        elif last_mon != '':
            ewb_mon[o][0] = ewb_mon[last_mon][0]
            ewb_mon[o][1] = ewb_mon[last_mon][1]
            ewb_mon[o][2] = ewb_mon[last_mon][2]
        elif last_mon == '':
            ewb_mon[o][0] = 0
            ewb_mon[o][1] = 0
            ewb_mon[o][2] = 0
    return ewb_mon

def correct(data, ewb_mon):
    '''
    基于得到的wb_mon对观测数据进行偏差订正
    return: datafram of lv1 corrected
    '''
    out = []
    for i, date in enumerate(data.iloc[:,0]):
        data_thistime = []
        mon = date[:7]
        if mon in ewb_mon:
            data_thistime.append(date)
            e = ewb_mon[mon][0]
            w = ewb_mon[mon][1]
            b = ewb_mon[mon][2]
            for j in range(1,18):
                data_thistime.append(np.round(w[j - 1]*(data.iloc[i,j] + e[j - 1]) + b[j - 1], 2))
            out.append(data_thistime)
    return pd.DataFrame(out,columns= None)

if __name__ == '__main__':
    stationNum = '54511'
    path_in = r'F:/data/beijing2018/LV/LV1/lv1_mono_matched/'+ stationNum + '_matched.csv'
    pathout = 'F:/data/beijing2018/LV/LV1/lv1_corrected/'+ stationNum + '_corrected.csv'
    data = pd.read_csv(path_in, index_col= None, header= None)
    ewb_mon = get_correct(data)
    lv1_corrected = correct(data, ewb_mon)
    lv1_corrected.to_csv(pathout, index= None, header= None)

