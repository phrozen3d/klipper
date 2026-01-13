#!/bin/sh

sleep 10
while true
do
	/etc/frp/frpc -c /etc/frp/frpc.ini > /etc/frp/frpc.log
	sleep 1
done	
