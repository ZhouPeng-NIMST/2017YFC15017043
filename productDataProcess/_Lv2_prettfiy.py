# coding: utf-8
import pandas as pd
import os, re

def transform(date):
    date = re.sub(r'/',r'-',date) 
    s = re.search(r' .*$',date)
    if s.group() == ' 08:00':
        date = re.sub(r' .*$','-00',date)
        return date
    elif s.group() == ' 20:00':
        date = re.sub(r' .*$','-12',date)
        return date
    else:
        return 'None'

def get_lv2_all(pathIn,pathOut):
    '''
    获取所有时刻lv2数据
    每天输出一个文件
    '''
    if not os.path.isdir(pathOut):
        os.makedirs(pathOut)
    
    filenames = os.listdir(pathIn)
    for filename in filenames:
        data_lv2 = []
        print(filename)
        filepath = os.path.join(pathIn,filename)
        #有些文件里面没有数据，pass
        if os.path.getsize(filepath) < 1024*100:
            continue
        data = pd.read_csv(filepath, header= 0, index_col= 0)  
        for i,o in enumerate(data.values):
            #删除一些日期格式   
            if re.match(r'\d{4}/\d{2}/\d{2} \d{2}:\d{2}',o[0]):
            #             只提取温度和相对湿度
                if o[1] == 11 and data.values[i + 2,1] == 13:
                    data_lv2.append([re.sub(r'/',r'-',o[0])] + o[10:].tolist() + data.values[i + 2,10:].tolist())
                else:
                    continue
            else:
                continue
        pd.DataFrame(data_lv2).to_csv(os.path.join(pathOut,filename))

def get_lv2_0012(pathIn):
    '''
    只获取00UTC时刻和12UTC时刻的lv2数据
    '''
    filenames = os.listdir(pathIn)
    data_lv2_0012 = []
    for filename in filenames:
        filepath = os.path.join(pathIn,filename)
        #有些文件里面没有数据，pass
        if os.path.getsize(filepath) < 1024*100:
            continue
        data = pd.read_csv(filepath, header= 0, index_col= 0)  
        for i,o in enumerate(data.values):
            #删除一些日期格式   
            if re.match(r'\d{4}/\d{2}/\d{2} \d{2}:\d{2}',o[0]):
                s = transform(o[0])
            #             只提取温度和相对湿度
                if s[-2:] in ['00','12'] and o[1] == 11 and data.values[i + 2,1] == 13:
                    data_lv2_0012.append([s] + o[10:].tolist() + data.values[i + 2,10:].tolist())
                else:
                    continue
            else:
                continue
    return pd.DataFrame(data_lv2_0012)

if __name__ == '__main__':
    stationNum = '54399'
    pathIn = r'F:/data/beijing2018/LV/LV2/' + stationNum
    pathOut_0012 = r'F:/data/beijing2018/LV/project_2018_all/prettify_lv2 _00_12/' + stationNum + '_0012.csv'
    lv2_0012 = get_lv2_0012(pathIn)
    lv2_0012.to_csv(pathOut_0012, index= None, header= None)
#     lv2_all = get_lv2_all(pathIn)

