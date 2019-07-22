# chose data both in lv1 &mono

# coding: utf-8
import pandas as pd
import os

def lv1_mono_process(path_lv1, path_mono):
    '''
    return: date,T,P,H,&14channel's bt
    '''
    lv1 = pd.read_csv(path_lv1,header=None)
    mono = pd.read_excel(path_mono,header=None,index_col= None).T
    # delete the 'rain' column of lv1
    lv1.drop(4, axis= 1, inplace= True)
    # change the location of columns T P H tips:
    mono.insert(1,'T',mono.iloc[:,15])
    mono.insert(2,'H',mono.iloc[:,18])
    mono.insert(3,'P',mono.iloc[:,18])
    mono.drop([15,16,17], axis= 1, inplace= True)
    # delete the first row
    mono.drop(0, axis= 0, inplace= True)
    mono.iloc[:,1] = mono.iloc[:,1].values - 273.15
    #same the columns
    lv1.columns = mono.columns
    return lv1, mono

def match_lv1_mono(lv1, mono):
    '''
    return: data both in lv1 & mono
    '''
    data_matched = []
    for i, date in enumerate(lv1.iloc[:,0]):
        if date in mono.iloc[:,0].values:
            idx = np.where(mono.iloc[:,0] == date)[0][0]
            data_matched.append(lv1.iloc[i,:].tolist() + mono.iloc[idx,:].tolist())
    return pd.DataFrame(np.array(data_matched))

if __name__ == '__main__':
    stationNum = '54511'
    path_lv1 = 'F:/data/beijing2018/LV/LV1/prettify_00_12/' + stationNum + r'_00_12.csv'
    path_mono = 'F:/data/beijing2018/LV/LV1/mono/201718(BT_mono).xlsx'
    path_out = r'F:/data/beijing2018/LV/LV1/lv1_mono_matched'
    if not os.path.isdir(path_out):
        os.makedirs(path_out)
    lv1, mono = lv1_mono_process(path_lv1, path_mono)
    lv1_mono_matched = match_lv1_mono(lv1, mono)
#     save
    lv1_mono_matched.to_csv(os.path.join(path_out,stationNum+'_matched.csv'), index= None, header= None)

