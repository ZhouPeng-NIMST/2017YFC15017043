
# coding: utf-8

# In[ ]:


'''
获取亮温数据，按照相应格式写好
'''


# In[ ]:


import pandas as pd
import os
import re


# In[ ]:


def getBtfromLV1(pathIn,pathOut):
    #   if pathOut not exists,build new one.mikdir/makedirs
    if not os.path.isdir(pathOut):
        os.makedirs(pathOut)
    elif not os.path.isdir(pathIn):
        print('pathIn not exsits!')
        return 'error!'
    # get bt & P T H Time of every file
    filenames = os.listdir(pathIn)
    index = [1,2,3,4,6,8,11,13,17,19,22,27,28,30,33,35,38,39,41]
    for filename in filenames:
        path = os.path.join(pathIn,filename)
#           if file size < 100kb,continue
        if os.path.getsize(path) < 1024*100:
            continue
        btOut = []
        f = pd.read_csv(os.path.join(pathIn,filename))
#             rule out some worng file
        if len(f.columns) != 42:
            continue
        for i,time in enumerate(f.iloc[:,1]):
            if (f.iloc[i,index].values[5:12] == 0).any():
                continue
            elif f.iloc[i,6] == 1:
                continue
            else:
                btOut.append(f.iloc[i,index].values)
        btOut = np.array(btOut)
#         to ensure btOut is not an empty array
        if btOut.size > 0:
            bt_all = pd.DataFrame(btOut,columns=f.columns[index])
            bt_all.to_csv(os.path.join(pathOut,filename),index= None,header=None)
        else:
            continue


# In[ ]:


if __name__ == '__main__':
    pathIn = r'F:\data\beijing2018\LV\LV1\54511'
    pathOut = r'F:\data\beijing2018\LV\LV1\prettify\54511'
    getBtfromLV1(pathIn,pathOut)

