#!/bin/sh

chmod -R 777 *
echo "chmod -R 777 *"

#lancaigang240401：启动脚本
cp /home/mks/klipper/klippy/extras/phrozen_dev/KlipperScreen-start.sh /home/mks/KlipperScreen/scripts
#lancaigang240401：phrozen安装脚本
cp /home/mks/klipper/klippy/extras/phrozen_dev/phrozen_install.sh /home/mks/phrozen_dir
#lancaigang240401：升级的zip压缩包
cp -rf /tmp/phrozen_dev/* /home/mks/klipper/klippy/extras/phrozen_dev
#lancaigang240402：
cp /home/mks/klipper/klippy/extras/phrozen_dev/DriveCodeFile.dat /home/mks/hdlDat
#lancaigang231124：ifconfig获取网卡eth0的物理地址，转换为frp端口
#如4e:4a:21:32:fe:2b取fe:2b为65067

exit
