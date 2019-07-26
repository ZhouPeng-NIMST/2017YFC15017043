# coding: utf-8

import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

def match_retrieved_soundings(path_souding, path_retrieved, path_out):
    '''
    匹配再反演数据与探空数据
    '''
    data_soundings = pd.read_excel(path_souding)

    #     索引温、湿度所对应的列
    index_d = list(range(0, data_soundings.shape[1], 4))
    index_t = list(range(2, data_soundings.shape[1], 4))
    index_h = list(range(3, data_soundings.shape[1], 4))

    date = data_soundings.columns.values[index_d]
    data_soundings_t = data_soundings.values[:,index_t]
    data_soundings_h = data_soundings.values[:,index_h]
    # 合并&调换位置
    data_soundings = pd.DataFrame(np.r_[date.reshape(1, -1), data_soundings_t, data_soundings_h].T)
    # 反演值
    data_retrieved = pd.read_csv(path_retrieved, header=None)

    # 求交集
    a = set(data_retrieved[0])
    b = set(data_soundings[0])
    bothIn = list(a&b)
    bothIn.sort()

    # 索引交集，匹配
    datelist_soundings = data_soundings[0].values.tolist()
    datelist_retrieved = data_retrieved[0].values.tolist()
    data_matched = []
    for o in bothIn:
        idx_soundings = datelist_soundings.index(o)
        idx_retrieved = datelist_retrieved.index(o)
        data_matched.append(data_retrieved.iloc[idx_retrieved,:].values.tolist() + data_soundings.iloc[idx_soundings,:].values.tolist())
    data_matched = pd.DataFrame(data_matched)

    data_matched.to_csv(path_out,header= None, index= None)

if __name__ == '__main__':
    stationNum = '54399'
    path_souding = r'F:/data/beijing2018/探空/插值后/201718(插值后)_long.xlsx'
    path_retrieved = r'F:/data/beijing2018/LV/project_2018_all/profile/' + stationNum + '_retrieved.csv'
    path_out = r'F:/data/beijing2018/LV/project_2018_all/soundings_r_matched/' + stationNum +  '_soundings_r_matched.csv'
    match_retrieved_soundings(path_souding, path_retrieved, path_out)

