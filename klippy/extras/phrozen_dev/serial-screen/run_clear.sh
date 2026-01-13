#!/bin/bash
# Script: run_clear.sh
# Purpose: Clear system cache and restart udp_server

PASSWORD="makerbase"

# 同步数据到磁盘
echo "$PASSWORD" | sudo -S sync

# 清除系统缓存
echo "$PASSWORD" | sudo -S sh -c 'echo 3 > /proc/sys/vm/drop_caches'

# 终止旧的 udp_server 进程
echo "$PASSWORD" | sudo -S killall udp_server 2>/dev/null || true

# 延迟片刻，确保进程完全退出
sleep 1

# 启动新的 udp_server（后台运行）
echo "$PASSWORD" | sudo -S nohup /root/udp_server &>/dev/null &

# 检查是否成功执行
if [ $? -eq 0 ]; then
    echo "Cache cleared and udp_server restarted successfully."
else
    echo "Failed to clear cache or restart udp_server."
fi