%读取全年插值后数据并写出
clear;
path_in = 'F:\data\beijing2018\探空\插值后\201718(插值后)_long.xlsx';
path_out = 'F:\data\beijing2018\NOSCALE\201718\';
[~,~,in_1]=xlsread(path_in);
[a,b]=size(in_1);
for k=1:4:b
    if ~exist(path_out,'dir')
        mkdir(path_out)
    end
    fid_1=fopen('MONORTM.txt','r');
    fid_2=fopen([path_out,in_1{1,k},'.txt'],'w+');
    i=1;
    i_3=2;
    line{1,1}='';
    for i_1=1:13;
        line{i,1}=fgetl(fid_1);
        i=i+1;
    end
    i=i-1;
    for i_1=1:6
        line{i,1}=fgetl(fid_1);
        fprintf(fid_2,[line{i,1},'\n']);
        i=i+1;
    end
    i=i-1;
    fprintf(fid_2,'14\n');
    fprintf(fid_2,'0.7416\n0.7683\n0.7950\n0.8506\n0.8751\n0.9173\n1.0007\n1.7094\n1.7438\n1.7961\n1.8326\n1.8899\n1.9109\n1.9613\n');
    fprintf(fid_2,'0.000     0.000\n');
    fprintf(fid_2,'    0    2   47    1    0    7    1\n');
    fprintf(fid_2,'     0.007    10.000     0.000\n');
    fprintf(fid_2,'     0.055     0.100     0.200     0.300     0.400     0.500     0.600     0.700\n');
    fprintf(fid_2,'     0.800     0.900     1.000     1.250     1.500     1.750     2.000     2.250\n');
    fprintf(fid_2,'     2.500     2.750     3.000     3.250     3.500     3.750     4.000     4.250\n');
    fprintf(fid_2,'     4.500     4.750     5.000     5.250     5.500     5.750     6.000     6.250\n');
    fprintf(fid_2,'     6.500     6.750     7.000     7.250     7.500     7.750     8.000     8.250\n');
    fprintf(fid_2,'     8.500     8.750     9.000     9.250     9.500     9.750    10.000\n');
    fprintf(fid_2,'   47 TEST\n');
    for i_1=1:18
        line{i,1}=fgetl(fid_1);
        i=i+1;
    end
    i=i-1;
    for i_1=1:2000
        data_1=textscan(line{i,1},'%f%f%f%s%s',1);
        if strcmp(data_1{1,4},'AA')==1
            if isnan(in_1{i_3,k})~=1;
                data_1{1,1}=(in_1{i_3,k+1}/1000);
                data_1{1,2}=in_1{i_3,k};
                data_1{1,3}=in_1{i_3,k+2}+273.15;
            else
                i_3=i_3+1;
                if i_3>a
                    break
                end
                data_1{1,1}=(in_1{i_3,k+1}/1000);
                data_1{1,2}=in_1{i_3,k};
                data_1{1,3}=in_1{i_3,k+2}+273.15;
            end
        end
        fprintf(fid_2,'    %6.3f',data_1{1,1});
        fprintf(fid_2,'  %8.3f',data_1{1,2});
        fprintf(fid_2,'   %7.3f',data_1{1,3});
        fprintf(fid_2,'     %s',data_1{1,4}{1,1});
        fprintf(fid_2,'   %s\n',data_1{1,5}{1,1});
        i=i+1;
        line{i,1}=fgetl(fid_1);
        if line{i,1} ==-1
            break
        end
        data_1=textscan(line{i,1},'%f%f%f%f%f%f%f',1);
        if  strcmp(line{i,1}(end-3:end),'0.00')==1
            data_1{1,1}=in_1{i_3,k+3};
        end
        fprintf(fid_2,'%6.4e',data_1{1,1});
        fprintf(fid_2,'     %5.3f',data_1{1,2});
        fprintf(fid_2,'  %8.6f',data_1{1,3});
        fprintf(fid_2,'  %8.6f',data_1{1,4});
        fprintf(fid_2,'  %8.6f',data_1{1,5});
        fprintf(fid_2,'  %8.6f',data_1{1,4});
        fprintf(fid_2,'      %4.2f\n',data_1{1,5});
        i_3=i_3+1;
        if i_3>a
            break
        end
        i=i+1;
        line{i,1}=fgetl(fid_1);
        if line{i,1} ==-1
            break
        end
    end
    fclose(fid_1);
    fprintf(fid_2,'%s\n','-1.');
    fprintf(fid_2,'%s\n','%%%');
    fclose(fid_2);
end
