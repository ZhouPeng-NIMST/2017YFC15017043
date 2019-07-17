clear;close all;
load norain2017_18.mat
path_in = 'F:\data\beijing2018\ÃΩø’\Œ¥≤Â÷µ\201718(Œ¥≤Â÷µ).xlsx';
path_out = 'F:\data\beijing2018\ÃΩø’\≤Â÷µ∫Û';
[num,date,~]=xlsread(path_in);
out_1={1};
k=1;
m=1;
for i=1:4:size(num,2)
    %if  ismember(date{1,i}(1:10),raindate2011)
    %disp(date{1,i}(1:10))
    %end
    if  ismember(date{1,i}(1:10),norain2017_18)%%%%%%%%%%%%%%%%%%%%%%%%%%
        disp (m);
        m=m+1;
        PRES=num(1:end,i);
        PRES=PRES(~any(isnan(PRES),2),:);
        if length(PRES) < 25
            continue
        end
        HGHT=num(1:end,i+1);
        HGHT(1) = 0;
        TEMP=num(1:end,i+2);
        RELH=num(1:end,i+3);
        any(~isnan(HGHT));
        HGHT=HGHT(~any(isnan(HGHT),2),:);
        TEMP=TEMP(~any(isnan(TEMP),2),:);
        RELH=RELH(~any(isnan(RELH),2),:);
        HGHT_1=[0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1,1.25,1.5,1.75,2,2.25,2.5,2.75,3,3.25,3.5,3.75,4,4.25,4.5,4.75,5,5.25,5.5,5.75,6,6.25,6.5,6.75,7,7.25,7.5,7.75,8,8.25,8.5,8.75,9,9.25,9.5,9.75,10];
        PRES_1=abs(interp1(HGHT,PRES,HGHT_1*1000,'spline','extrap'));
        PRES_1=PRES_1';
        if isnan(PRES_1(end))
            continue
        end
        RELH_1=abs(interp1(HGHT,RELH,HGHT_1*1000,'pchip','extrap'));
        RELH_1=RELH_1';
        TEMP_1=interp1(HGHT,TEMP,HGHT_1*1000,'spline','extrap');
        TEMP_1=TEMP_1';
        HGHT_1=HGHT_1'*1000;
        a=size(HGHT_1,1);
        out_1{1,k}=date{1,i};
        for i_1=2:a+1
            out_1{i_1,k}=PRES_1(i_1-1,1);
            out_1{i_1,k+1}=HGHT_1(i_1-1,1);
            out_1{i_1,k+2}=TEMP_1(i_1-1,1);
            out_1{i_1,k+3}=RELH_1(i_1-1,1);
        end
            k=k+4;
    end
end
if ~exist(path_out,'dir')
    mkdir(path_out)
end
pathsplit_cell = strsplit(path_in,'\');
filename_1 = pathsplit_cell{end};
filename_cell = strsplit(filename_1,'(');
filename_2 = filename_cell{1};
xlswrite([path_out,'\',filename_2,'(≤Â÷µ∫Û)_long.xlsx'],out_1)