
% % 创建一个示例 timetable 变量
% timeStamps = datetime('now') + seconds(1:5)';
% data = rand(5, 3);
% variableNames = {'Sensor1', 'Sensor2', 'Sensor3'};
% tt = timetable(timeStamps, data, 'VariableNames', variableNames);

% % 读取timetable 变量
% timeStamps = datetime(Acceleration.Timestamp);
% data = Acceleration.X;

% 将 timetable 保存为 CSV 文件
% writetimetable(Acceleration, 'acc.csv');
% writetimetable(AngularVelocity, 'ang.csv');
% writetimetable(Orientation, 'att.csv');
% writetimetable(MagneticField, 'mag.csv');
% writetimetable(Position, 'pos.csv');
%%
a=fopen('acc2.csv','w');
tt = Acceleration.Timestamp;
% 将 timetable 的时间戳转换为 ROS 时间戳格式
% rosTimeStamps = zeros(height(tt), 1);
for i = 1:height(tt)
    posixTime = posixtime(tt(i));
    sec = floor(posixTime);
    nsec = round((posixTime - sec) * 1e9);
%     rosTimeStamps(i) = rosmessage('std_msgs/Header').stamp;
%     rosTimeStamps(i).Sec = sec;
%     rosTimeStamps(i).Nsec = nsec;
    fprintf(a,'%10d,%9d,%.6f,%.6f,%.6f\n',[sec,nsec,Acceleration.X(i),Acceleration.Y(i),Acceleration.Z(i)]);
end
fclose(a);
%%
b=fopen('ang.csv','w');
tt = AngularVelocity.Timestamp;
for i = 1:height(tt)
    posixTime = posixtime(tt(i));
    sec = floor(posixTime);
    nsec = round((posixTime - sec) * 1e9);
    fprintf(b,'%10d,%9d,%.6f,%.6f,%.6f\n',[sec,nsec,AngularVelocity.X(i),AngularVelocity.Y(i),AngularVelocity.Z(i)]);
end
fclose(b);
%%
c=fopen('mag.csv','w');
tt = MagneticField.Timestamp;
for i = 1:height(tt)
    posixTime = posixtime(tt(i));
    sec = floor(posixTime);
    nsec = round((posixTime - sec) * 1e9);
    fprintf(c,'%10d,%9d,%.6f,%.6f,%.6f\n',[sec,nsec,MagneticField.X(i),MagneticField.Y(i),MagneticField.Z(i)]);
end
fclose(c);
%%
d=fopen('att.csv','w');
tt = Orientation.Timestamp;
for i = 1:height(tt)
    posixTime = posixtime(tt(i));
    sec = floor(posixTime);
    nsec = round((posixTime - sec) * 1e9);
    fprintf(d,'%10d,%9d,%.6f,%.6f,%.6f\n',[sec,nsec,Orientation.X(i),Orientation.Y(i),Orientation.Z(i)]);
end
fclose(d);
%%
e=fopen('pos.csv','w');
tt = Position.Timestamp;
for i = 1:height(tt)
    posixTime = posixtime(tt(i));
    sec = floor(posixTime);
    nsec = round((posixTime - sec) * 1e9);
    fprintf(e,'%10d,%9d,%.13f,%.13f,%.4f,%.4f,%.4f,%.4f\n',[sec,nsec,Position.latitude(i),Position.longitude(i),Position.altitude(i),Position.speed(i),Position.course(i),Position.hacc(i)]);
end
fclose(e);