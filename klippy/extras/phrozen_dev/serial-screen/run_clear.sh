#!/bin/bash
# Script: run_clear.sh
# Purpose: Clear system cache, clear /var/log files, clean apt package cache, and restart udp_server

PASSWORD="makerbase"

# 同步数据到磁盘
echo "$PASSWORD" | sudo -S sync

# 清除系统缓存
echo "$PASSWORD" | sudo -S sh -c 'echo 3 > /proc/sys/vm/drop_caches'

# 停止旧的 udp_server 进程
echo "$PASSWORD" | sudo -S killall udp_server 2>/dev/null || true

# 延迟片刻，确保进程安全退出
sleep 1

# 安全清空 /var/log 目录下所有普通日志文件的内容（不删除文件本身）
# 不删除特殊文件（如 socket、fifo 等），只清空 regular files
echo "Clearing log files in /var/log..."
echo "$PASSWORD" | sudo -S find /var/log -type f -exec sh -c 'echo -n "" > "$1"' _ {} \;

# 可选：如果使用 systemd-journal，则压缩 journal 日志（防止占用大量空间）
if command -v journalctl &> /dev/null; then
    echo "Vacuuming systemd journal logs..."
    echo "$PASSWORD" | sudo -S journalctl --vacuum-size=10M 2>/dev/null || true
fi

# Clean apt package cache to free disk space
echo "Cleaning apt package cache..."
echo "$PASSWORD" | sudo -S apt-get clean 2>/dev/null || true

# 启动新的 udp_server（后台运行）
echo "$PASSWORD" | sudo -S nohup /root/udp_server &>/dev/null &

# 检查是否成功执行（注意：nohup 命令通常返回 0，更可靠的检查方式是确认进程是否存在）
sleep 1
if pgrep -x "udp_server" > /dev/null; then
    echo "Cache cleared, logs cleared, and udp_server restarted successfully."
else
    echo "Failed to restart udp_server. Please check manually."
    exit 1
fi