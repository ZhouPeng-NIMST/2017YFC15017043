# coding: utf-8
#get 00UTC & 12UTC bt 

import pandas as pd
import os,re

#change '/' to '-' & 08 to 00 UTC,20 to 12 UTC
def transform(matched):
    if matched.group() in [' 08:00',' 08:01']:
        return '-00'
    elif matched.group() in [' 20:00',' 20:01']:
        return '-12'
    else:
        return '-' + matched.group()[1:]
def format_date(date):
    date = re.sub(r'/',r'-',date)
    date = re.sub(r' \d*:\d*',transform,date)
    date = re.sub(r' \d*:\d*',transform,date)
    return date

def get_0012_FromLV1_Prettify(pathIn,pathOut):
    #creat new folder if pathOut not exsits
    if not os.path.isdir(pathOut):
        os.makedirs(pathOut)
    # get filenames
    filenames = os.listdir(pathIn)
    # def an empty arr to save bt_00_12
    btOut = []
    for filename in filenames:
    #     to aviod 00/01 being appended in btOut togther
        time_judge = []
        path = os.path.join(pathIn,filename)
        f = pd.read_csv(path)
        for i,time in enumerate(f.iloc[:,0]):
    #       get bt of time chosed
            if re.search(r'08:00|20:00|08:01|20:01',time):
                date_formated = format_date(time)
                f.iloc[i,0] = date_formated
                if date_formated not in time_judge:
                    time_judge.append(date_formated)
                    btOut.append(f.iloc[i].values)
    btOut = pd.DataFrame(np.array(btOut))
    # save     
    btOut.to_csv(os.path.join(pathOut,pathIn.split('\\')[-1]+ '_00_12.csv'),index= None,header= None)

if __name__ == '__main__':
    pathIn = r'F:\data\beijing2018\LV\LV1\prettify\54419'
    pathOut = r'F:\data\beijing2018\LV\LV1\prettify_00_12'
    get_0012_FromLV1_Prettify(pathIn,pathOut)

