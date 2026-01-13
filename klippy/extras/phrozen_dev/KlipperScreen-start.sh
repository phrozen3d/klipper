#!/bin/bash

#lancaigang240401：创建phrozen文件夹
mkdir /home/mks/phrozen_dir
#lancaigang240401：添加权限
chmod -R 777 /home/mks/phrozen_dir/*
#touch /home/mks/hdlDat/DriveCodeFile.dat
#lancaigang231124：暂时使用mks自带的串口屏
systemctl stop makerbase-client.service
chmod -R 777 /home/mks/klipper/klippy/extras/phrozen_dev
chmod -R 777 /home/mks/hdlDat
chmod -R 777 /home/mks/klipper/klippy/extras/phrozen_dev/serial-screen
sleep 1


#lancaigang250809:
rm -rf /home/mks/moonraker-obico
rm -rf /home/mks/moonraker-obico-env


#lancaigang231121：AMS多色主板IAP升级
#lancaigang240401：开机不启动slave_ota
#/home/mks/klipper/klippy/extras/phrozen_dev/frp-oms/phrozen_slave_ota >/dev/null 2>&1 &
#sleep 1
#lancaigang231121：AMS多色主板IAP升级
/home/mks/klipper/klippy/extras/phrozen_dev/frp-oms/phrozen_master >/dev/null 2>&1 &
sleep 1
#lancaigang231211：陶晶池串口屏
/home/mks/klipper/klippy/extras/phrozen_dev/serial-screen/voronFDM >/dev/null 2>&1 &
sleep 1
#lancaigang240110：frp
/home/mks/klipper/klippy/extras/phrozen_dev/frp-oms/frp/frpc_script &
sleep 1


#lancaigang241215:
/usr/sbin/ntpdate ntp1.aliyun.com &


while true
do
	sleep 1
done	