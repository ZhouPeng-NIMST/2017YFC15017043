%读取所有探空数据并按照不同时刻写出
clear;
fclose all;
close all;
k=0;
out_3={1};
path = 'F:\data\beijing2018\探空\2018\';
path_out = 'F:\data\beijing2018\探空\未插值\';
list=dir([path,'*.txt']);
L=length(list);
for i_1=1:L
    clear a data filename i_2 i_3 i_4 i_5 nextline out_1 n judge out_2
    filename=[path,list(i_1).name];
    fid = fopen(filename,'r');
    if fid == -1
        disp('can not open file!');
    end
    nextline=fgetl(fid);
    out_1{1,1}='PRES';
    out_1{1,2}='HGHT';
    out_1{1,3}='TEMP';
    out_1{1,4}='RELH';
    i_2=2;
    a=2;
    judge=[];
    for i_3=1:10000
        while strcmp(nextline,'')==1
            nextline=fgetl(fid);
            if nextline==-1
                break
            end
        end
        if nextline==-1
            break
        end
        data=textscan(nextline,'%f%f%f%f%f%f%f%f%f%f%f',1);
        while isempty(data{1,2})&&~ isempty(data{1,1})
            if strcmp(nextline(1:5),'54511')==1
                out_1{a,1}=funmonth(nextline);
                judge(end+1)=a;
                a=a+1;
                i_2=i_2+1;
            end
            nextline=fgetl(fid);
            if nextline~=-1
                data=textscan(nextline,'%f%f%f%f%f%f%f%f%f%f%f',1);
            else
                break
            end
        end
        if data{1,2}<=11000 & ~isempty(data{1,11}) & data{1,1}>100
            out_1{i_2,1}=data{1,1};
            out_1{i_2,2}=data{1,2};
            out_1{i_2,3}=data{1,3};
            out_1{i_2,4}=data{1,5};
            i_2=i_2+1;
            a=a+1;
%         else
%             disp(data{1,2})
%             disp(data{1,11})
%             disp(data{1,1})
        end
        nextline=fgetl(fid);
        if nextline==-1
            break
        end
    end
    fclose(fid);
    %if ~exist(['..\按月份'],'dir')
    %    mkdir('..\按月份')
    %end
    %xlswrite(['..\按月份\',filename(1:end-4),'.xlsx'],out_1)
    %     if ~exist('F:\data\北京\探空\2017\按时刻','dir')
    %         mkdir('F:\data\北京\探空\2017\按时刻')
    %     end
    n=1;
    out_2(1,1)=1;
    judge=[judge 941108];
    while n<size(judge,2)
        m=1;
        while (judge(1,n)+m)<judge(1,n+1)
            out_2(m,1)=out_1{judge(1,n)+m,1};
            out_2(m,2)=out_1{judge(1,n)+m,2};
            out_2(m,3)=out_1{judge(1,n)+m,3};
            out_2(m,4)=out_1{judge(1,n)+m,4};
            m=m+1;
            if (judge(1,n)+m)>size(out_1,1)
                break
            end
        end
        %xlswrite(['..\按时刻\',out_1{judge(1,n),1},'.xlsx'],out_2)
        out_3{1,k+1}=out_1{judge(1,n),1};
        for i_4=1:size(out_2,1)
            for i_5=1:4
                out_3{i_4+1,i_5+k}=out_2(i_4,i_5);
            end
        end
        k=k+4;
        out_2=[];
        n=n+1;
    end
end
if ~exist(path_out,'dir')
    mkdir(path_out)
end
xlswrite([path_out,'\201718(未插值).xlsx'],out_3)