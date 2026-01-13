#!/bin/sh
#lancaigang240328：先重启klipper，释放ttyUSB0
#lancaigang240401：stop klipper
systemctl stop klipper

killall phrozen_slave_ota
#sleep 1
/home/prz/klipper/klippy/extras/phrozen_dev/frp-oms/phrozen_slave_ota >/dev/null 2>&1 &

sleep 1

exit
