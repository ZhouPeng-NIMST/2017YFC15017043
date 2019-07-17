clear
path_in_bt = 'F:\data\beijing2018\BT\BT_2018_456_mono\';
path_out_bt =  'F:\data\beijing2018\BT\btxlsx\';
if ~exist(path_out_bt,'dir')
    mkdir(path_out_bt)
end
path_in_surface = 'F:\data\beijing2018\探空\插值后\2018_456(插值后)_long.xlsx';
list=dir([path_in_bt,'*txt']);
L=length(list);
out_1{1,1}='频率';
out_1{2,1}=22.20;
out_1{3,1}=23.035;
out_1{4,1}=23.835;
out_1{5,1}=25.5;
out_1{6,1}=26.235;
out_1{7,1}=27.5;
out_1{8,1}=30;
out_1{9,1}=51.25;
out_1{10,1}=52.28;
out_1{11,1}=53.85;
out_1{12,1}=54.94;
out_1{13,1}=56.66; 
out_1{14,1}=57.29;
out_1{15,1}=58.8;
out_1{16,1}='T';
out_1{17,1}='P';
out_1{18,1}='H';
[num,date,~]=xlsread(path_in_surface);
for i=1:L
    filename=[path_in_bt,list(i).name];
    out_1{1,i+1}=list(i).name(1:end-4);
    fid=fopen(filename);
    textscan(fid,'%[^\n]',4);
    for i_1=1:14
    raw=textscan(fid,'%f%6.3f%7.4f%[^\n]',1);
    out_1{i_1+1,i+1}=raw{1,3};
    end
    out_1{16,i+1}=num(1,4*i-1)+273.15;
    out_1{17,i+1}=num(1,4*i-3);
    out_1{18,i+1}=num(1,4*i);
    fclose(fid);
end
xlswrite([path_out_bt,list(1).name(1:4),'(BT_mono).xlsx'],out_1)
