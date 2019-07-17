clear;fclose all;
path_in_sounding ='F:\data\beijing2018\探空\插值后\201718(插值后)_long.xlsx';
path_in_tape7 = 'F:\data\beijing2018\tape7_ori\outtape7\';
path_out_tape7 = 'F:\data\beijing2018\tape7_out\201718\';
[num,txt]=xlsread(path_in_sounding);
list_1=dir([path_in_tape7,'*.txt']);
L=length(list_1);
k=4;
for i_1=1:L
    fid_1=fopen([path_in_tape7,list_1(i_1).name]);
    if ~exist(path_out_tape7,'dir')
        mkdir(path_out_tape7)
    end
    fid_2=fopen([path_out_tape7,list_1(i_1).name],'w+');
    fgetl(fid_1);
    line_in=fgetl(fid_1);
    line_out=line_in;
    fprintf(fid_2,'%s\n',line_out);
    for i_2=1:47
        line_in=fgetl(fid_1);
        if line_in == -1    
            break
        end
        if i_2<=10
            if num(i_2+1,k)>=95
                line_out=[line_in, ' 0.05'];%0.5g/m3
            end
            if num(i_2+1,k)>85&&num(i_2+1,k)<95
                line_out=[line_in,' ',num2str(roundn(0.1*(0.05*num(i_2+1,k)-4.25),-4))];
            end
            if num(i_2+1,k)<=85
                line_out=line_in;
            end
            fprintf(fid_2,'%s\n',line_out);
            line_in=fgetl(fid_1);
            if line_in == -1
                break
            end
        end
        if i_2>10&&i_2<=21
            if num(i_2+1,k)>=95
                line_out=[line_in, ' 0.125'];
            end
            if num(i_2+1,k)>88&&num(i_2+1,k)<95
                line_out=[line_in,' ',num2str(roundn(0.25*(0.05*num(i_2+1,k)-4.25),-4))];%0.5 
            end
            if num(i_2+1,k)<=88
                line_out=line_in;
            end
            fprintf(fid_2,'%s\n',line_out);
            line_in=fgetl(fid_1);
            if line_in == -1
                break
            end
        end
        if i_2>21
            line_out=line_in;
            fprintf(fid_2,'%s\n',line_out);
            line_in=fgetl(fid_1);
            if line_in == -1
                break
            end
        end
        line_out=line_in;
        fprintf(fid_2,'%s\n',line_out);
    end
    k=k+4;
    fclose all;
end
