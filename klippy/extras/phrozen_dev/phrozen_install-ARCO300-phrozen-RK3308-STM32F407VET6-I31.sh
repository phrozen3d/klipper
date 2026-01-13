#!/bin/sh


#lancaigang240401：启动脚本
cp /home/prz/klipper/klippy/extras/phrozen_dev/KlipperScreen-start.sh /home/prz/KlipperScreen/scripts
#lancaigang240401：phrozen安装脚本
cp /home/prz/klipper/klippy/extras/phrozen_dev/phrozen_install.sh /home/prz/phrozen_dir
#lancaigang240401：升级的zip压缩包
cp -rf /tmp/phrozen_dev/* /home/prz/klipper/klippy/extras/phrozen_dev
#lancaigang240402：
cp /home/prz/klipper/klippy/extras/phrozen_dev/DriveCodeFile.dat /home/prz/hdlDat
#lancaigang231124：ifconfig获取网卡eth0的物理地址，转换为frp端口
#如4e:4a:21:32:fe:2b取fe:2b为65067

chmod -R 777 /home/prz/klipper/klippy/extras/phrozen_dev/
echo "chmod -R 777 /home/prz/klipper/klippy/extras/phrozen_dev/"

exit
