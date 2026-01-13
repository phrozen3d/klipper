#!/bin/bash

#lancaigang240401：创建phrozen文件夹
#mkdir /home/linaro/phrozen_dir
#lancaigang240401：添加权限
#chmod -R 777 /home/linaro/phrozen_dir/*
#touch /home/linaro/hdlDat/DriveCodeFile.dat
#lancaigang231124：暂时使用mks自带的串口屏
#systemctl stop makerbase-client.service
#chmod -R 777 /home/linaro/klipper/klippy/extras/phrozen_dev
#chmod -R 777 /home/linaro/hdlDat
#chmod -R 777 /home/linaro/klipper/klippy/extras/phrozen_dev/serial-screen
sleep 1

#lancaigang250809:
rm -rf /home/prz/moonraker-obico
rm -rf /home/prz/moonraker-obico-env


#lancaigang231121：AMS多色主板IAP升级
#lancaigang240401：开机不启动slave_ota
#/home/linaro/klipper/klippy/extras/phrozen_dev/frp-oms/phrozen_slave_ota >/dev/null 2>&1 &
#sleep 1
sleep 15
#lancaigang231121：AMS多色主板IAP升级
/home/prz/klipper/klippy/extras/phrozen_dev/frp-oms/phrozen_master-arm-prz >/dev/null 2>&1 &
sleep 1
#lancaigang231211：陶晶池串口屏
/home/prz/klipper/klippy/extras/phrozen_dev/serial-screen/voronFDM-arm-prz >/dev/null 2>&1 &
sleep 5
#lancaigang240110：frp
/home/prz/klipper/klippy/extras/phrozen_dev/frp-oms/frp/frpc_script-ARCO300-phrozen-RK3308-STM32F407VET6-I31 &
#sleep 1
#/home/prz/klipper/klippy/extras/phrozen_dev/lcg-test-dev-fb0-ok/dev-fb0-test &
#sleep 1

#lancaigang241215:
#/usr/sbin/ntpdate ntp1.aliyun.com &


while true
do
	sleep 1
done





