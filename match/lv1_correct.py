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

    wb_mon = {'2018-01':[-1,-1],'2018-02':[-1,-1],'2018-03':[-1,-1],'2018-04':[-1,-1],'2018-05':[-1,-1],
              '2018-06':[-1,-1],'2018-07':[-1,-1],'2018-08':[-1,-1],'2018-09':[-1,-1],'2018-10':[-1,-1]}

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
        w = []
        b = []
        idx = idx_mon_1[o]
        if idx != -1:
            lv1, mono = data.iloc[idx-60:idx,1:18].values, data.iloc[idx-60:idx,19:].values
            # delete some error data
            abs_err = abs(lv1[:,9] - mono[:,9])
            idx_del = np.where(abs_err >= 0.8*(abs_err.max()))[0]
            lv1 = np.delete(lv1,idx_del,axis = 0)
            mono = np.delete(mono,idx_del,axis = 0)
            for j in range(17):
                f = np.polyfit(lv1[:,j],mono[:,j],1)
                w.append(f[0])
                b.append(f[1])
            wb_mon[o][0] = w
            wb_mon[o][1] = b
            last_mon = o
        else:
            wb_mon[o][0] = wb_mon[last_mon][0]
            wb_mon[o][1] = wb_mon[last_mon][1]

    return wb_mon

if __name__ == '__main__':
    stationNum = '54511'
    path_in = r'F:\data\beijing2018\LV\LV1\lv1_mono_matched'
    data = pd.read_csv(os.path.join(path_in,stationNum + '_matched.csv'), index_col= None, header= None)
    wb_mon = get_correct(data)

