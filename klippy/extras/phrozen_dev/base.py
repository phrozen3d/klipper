####################################
#项目名称：
#芯片类型: 
#功能: 
#研发人员：蓝才刚
#开发时间: 20230830
####################################

import time

# prz版本
#lancaigang240416: 
#lancaigang240417: 
#lancaigang240423: 
#lancaigang240427: 24040
#lancaigang240428: 24040
#lancaigang240506: 24050
FW_VERSION = "25384"# 如5x30+10=160 25年5月10号 如果1天内连续发布多个版本，则累加，正常情况下不会每天都发布新版本，大概能追踪到日期
HW_VERSION = "16"
IMAGE_VERSION = "16"
# DRIVER_CODE //如Linux主板+多个完全相同固件的MCU，需要协议通过SN号区分
#格式：V-H1-I1-F24045-SN1
#格式：V-H1-I1-F24045-SN2
#格式：V-H1-I1-F24045-SN3
#格式：V-H1-I1-F24045-SN4
#格式：V-H16-I16-F24045
#IMAGEID HWID FW版本
# // AMS主板1固件-1 1 25164
# // AMS主板2固件-1 1 25164
# // AMS主板3固件-1 1 25164
# // AMS主板4固件-1 1 25164
# // 缓冲器板固件-6 6 25164 保留
# // 16色HUB板固件-7 7 25164
#  // 调平板固件-8 8 25164 保留
# // 陶晶池串口屏前台HMI固件-11 11 25164
# // ARCO300-MKS-RK3328-陶晶池串口屏虚拟App-12 12  25164保留
# // ARCO300-MKS-RK3328-klipper-phrozen插件-16 16 25164
# // ARCO300-MKS-RK3328-OTA子程序-AMS串口升级程序-5 5 25164
# // ARCO300-MKS-RK3328-陶晶池串口屏后台程序-10 10 25164 作为整个phrozen_dev.zip的镜像版本做比较，跟云端版本检查
# // ARCO300-MKS-RK3328-OTA主程序-15 15 25164
# // DLP2K-YO2下沉机-STM32F401-Marlin-17 17 25164
# // AMS断码屏新主板-STM32F103VET6-18 18 25164
# // 14K-13.5寸-SSD202-UI-LVGL-21 21 25164 #21表示是14K-13.5寸的光固化自研主板-SSD202-FPGA高云-STM32F407上的SSD202的LVGL固件
# // 14K-13.5寸-高云FPGA-22 22 25164 #22表示是14K-13.5寸的光固化自研主板-SSD202-FPGA高云-STM32F407上的FPGA高云的固件
# // 14K-13.5寸-STM32F4-MCU-23 23 25164#23表示是14K-13.5寸的光固化自研主板-SSD202-FPGA高云-STM32F407上的STM32F407的固件
# // 14K-17寸-SSD202-UI-LVGL-24 24 25164
# // 14K-17寸-高云FPGA-25 25 25164
# // 14K-17寸-STM32F4-MCU-26 26 25164
# // 16KMax-13.5寸-SSD202-UI-LVGL-27 27 25164   #27表示是16KMAX-13.5寸的光固化自研主板-SSD202-FPGA高云-STM32F407上的SSD202的LVGL固件
# // 16KMax-13.5寸-高云FPGA-28 28 25164
# // 16KMax-13.5寸-STM32F4-MCU-28 29 25164
# // 烟雾净化器-30 30 25164
# // ARCO300-phrozen-RK3308-klipper-phrozen插件-31 31 25164
# // ARCO300-phrozen-RK3308-OTA子程序-AMS串口升级程序-32 32 25164
# // ARCO300-phrozen-RK3308-陶晶池串口屏后台程序-33 33 25164 作为整个phrozen_dev.zip的镜像版本做比较，跟云端版本检查
# // ARCO300-phrozen-RK3308-OTA主程序-34 34 25164
# // ARCO300-phrozen-RK3308-下位机STM32F407VET6-35 35 25164
# // ARCO300-phrozen-RK3308-喷头板STM32F103CBT6-36 36 25164
# // ARCO300-MKS-RK3328-下位机STM32F407VET6-37 37 25164
# // ARCO300-MKS-RK3328-喷头板STM32F103CBT6-38 38 25164
# // ARCO300-phrozen-RK3308-LVGL程序-KLIPPER-39 39 25164 phrozen自研LVGL-UI控制klipper


#=====DriveCodeFile.dat
#0，95，版本返回信息；
# 1 , 18 , 24053 , 18 , 0# // AMS主板1固件-18
# 2 , 18 , 24053 , 18 , 0# // AMS主板2固件-18
# 3 , 18 , 24053 , 18 , 0# // AMS主板3固件-18
# 4 , 18 , 24053 , 18 , 0# // AMS主板4固件-18
# 5 , 5 , 24046 , 5 , 0# // ARCO300-MKS-RK3328-STM32F407VET6-OTA子程序-AMS串口升级程序-5 5
# 6 , 0 , 0 , 0 , 0# // 缓冲器板固件-6 6 保留
# 7 , 7 , 24051 , 7 , 0# // 16色HUB板固件-7 7 保留
# 8 , 0 , 0 , 0 , 0 保留
# 9 , 0 , 0 , 0 , 0 保留
# 10 , 10 , 24054 , 10 , 0# // ARCO300-MKS-RK3328-STM32F407VET6-OTA子程序-陶晶池串口屏后台程序-10
# 11 , 11 , 24047 , 11 , 0# // 陶晶池串口屏前台HMI固件-11
# 12 , 0 , 0 , 0 , 0 保留
# 13 , 0 , 0 , 0 , 0 保留
# 14 , 0 , 0 , 0 , 0 保留
# 15 , 15 , 25042 , 15 , 0 # // ARCO300-MKS-RK3328-STM32F407VET6-OTA主程序-15 15 25164
# 16 , 16 , 25042 , 16 , 0 # // ARCO300-MKS-RK3328-STM32F407VET6-klipper-phrozen插件-16 16 25164
# 17 , ? , 25042 , ? , 0 保留
# 18 , ? , 25042 , ? , 0 保留
# 19 , ? , 25042 , ? , 0 保留
# 20 , ? , 25042 , ? , 0 保留


#下行
# {"Cluster_ID":0,"Command":95,"Data":{}}
#上行
# {
#     "Data_ID": 95,
#     "Data": {
#         "GwId": "000000000000",
#         "GwMac": "000000000000",
#         "GwIP": "169.254.17.112",
#         "Mask": 0,
#         "GwName": "Gateway-000000000000",
#         "StartTime": 1700683341,
#         "JoinMode": 1,
#         "RouteESSID": "",
#         "DNSServer": "",
#         "DriveCodeList": [
#             {
#                 "DriveCode": 16,
#                 "DriveImageType": 0,
#                 "DriveHwVersion": 0,
#                 "DriveFwVersion": 0,
#                 "DriveId": 0
#             },
#             {
#                 "DriveCode": 15,
#                 "DriveImageType": 0,
#                 "DriveHwVersion": 0,
#                 "DriveFwVersion": 0,
#                 "DriveId": 0
#             },
#             {
#                 "DriveCode": 14,
#                 "DriveImageType": 0,
#                 "DriveHwVersion": 0,
#                 "DriveFwVersion": 0,
#                 "DriveId": 0
#             },
#             {
#                 "DriveCode": 13,
#                 "DriveImageType": 0,
#                 "DriveHwVersion": 0,
#                 "DriveFwVersion": 0,
#                 "DriveId": 0
#             },
#             {
#                 "DriveCode": 12,
#                 "DriveImageType": 0,
#                 "DriveHwVersion": 0,
#                 "DriveFwVersion": 0,
#                 "DriveId": 0
#             },
#             {
#                 "DriveCode": 11,
#                 "DriveImageType": 0,
#                 "DriveHwVersion": 0,
#                 "DriveFwVersion": 0,
#                 "DriveId": 0
#             },
#             {
#                 "DriveCode": 10,
#                 "DriveImageType": 10,
#                 "DriveHwVersion": 10,
#                 "DriveFwVersion": 24045,
#                 "DriveId": 0
#             },
#             {
#                 "DriveCode": 9,
#                 "DriveImageType": 0,
#                 "DriveHwVersion": 0,
#                 "DriveFwVersion": 0,
#                 "DriveId": 0
#             },
#             {
#                 "DriveCode": 8,
#                 "DriveImageType": 0,
#                 "DriveHwVersion": 0,
#                 "DriveFwVersion": 0,
#                 "DriveId": 0
#             },
#             {
#                 "DriveCode": 7,
#                 "DriveImageType": 0,
#                 "DriveHwVersion": 0,
#                 "DriveFwVersion": 0,
#                 "DriveId": 0
#             },
#             {
#                 "DriveCode": 6,
#                 "DriveImageType": 0,
#                 "DriveHwVersion": 0,
#                 "DriveFwVersion": 0,
#                 "DriveId": 0
#             },
#             {
#                 "DriveCode": 5,
#                 "DriveImageType": 5,
#                 "DriveHwVersion": 5,
#                 "DriveFwVersion": 24046,
#                 "DriveId": 0
#             },
#             {
#                 "DriveCode": 4,
#                 "DriveImageType": 0,
#                 "DriveHwVersion": 0,
#                 "DriveFwVersion": 0,
#                 "DriveId": 0
#             },
#             {
#                 "DriveCode": 3,
#                 "DriveImageType": 0,
#                 "DriveHwVersion": 0,
#                 "DriveFwVersion": 0,
#                 "DriveId": 0
#             },
#             {
#                 "DriveCode": 2,
#                 "DriveImageType": 0,
#                 "DriveHwVersion": 0,
#                 "DriveFwVersion": 0,
#                 "DriveId": 0
#             },
#             {
#                 "DriveCode": 1,
#                 "DriveImageType": 1,
#                 "DriveHwVersion": 1,
#                 "DriveFwVersion": 24042,
#                 "DriveId": 0
#             }
#         ],
#         "ProductId": "ARCO",
#         "MainImage": 3,
#         "MainHWVersion": 3,
#         "MainFWVersion": 24041,
#         "Gw_Ram": 334560,
#         "Gw_Rom": 346508
#     }
# }
#网关透传串口字节数给节点，节点再转发给另一个MCU进行控制或升级
# {"DeviceAddr":"0000000000000000","Epoint":8,"Cluster_ID":64513,"Command":0,"SendMode":2,
#"Data":{"PassData":"B5C305D51669B239C6A52397937A40D3FE8319ABC503004B1200"}}

# /*
#       STM32<->LinuxSOC数据包协议
#       波特率：115200bps;起始位：1;数据位：8;奇偶校验位：None;停止位：1，总位：11
#       编号	备注		Bytes	值	描述
#       1	引导码			2	0xaaaa	引导码为数据包开始标志
#       2	数据包长度 2	Datalen	帧长度是指不包括自己之后的数据的长度(包含CRC16)
#       3	序列号ID		1		串口通信序列号，用来防止重放攻击
#                   发送方主动发送消息时将此序列号顺序增加，回应消息时序列号保持和接收序列号一致。接收方收到消息后在解析数据之前校验此Byte，
#                   如果连续超过10次序列号没有改变，则认为遇到重放攻击，将丢弃此消息不做任何处理，也不发送应答
#       4	数据类型ID
#                 根据ID号来区分具体应用，具体数据内容可以兼容不同的串口协议
#                 0x01:stm32升级包；0xFE+字节数+命令码+载荷
#                 0x02:zigbee协议；操作码+字节数+zigbee协调器串口协议
#                 0x03:虚拟App数据协议；操作码+字节数+Json数据
#                 0x04:modbus-RTU；操作码+字节数+modbus(起始位	设备地址	功能代码	数据	CRC校验	结束符)
#                 0x05:可扩展
#                 0x06:可扩展
#                 0x07:可扩展
#                 ...
#       5	具体数据内容	根据数据类型具体来区分；如操作码+附加数据
#       6	CRC-16			2
#     */
#     /*
#   // f8 01 0400 09000100
#   // f8 00 1200 fe0f000000000000020100fc000100b40000
#   //=====网关程序发送到外部程序的数据格式
#   //  数据结构：
#   //  Head	1	0xF8	协议头
#   //  DataId	1		数据包标识
#             // 0x00：Zigbee协调器串口协议数据
#             // 0x01：下发驱动代号
#             // 0x02： 错误反馈
#             // 0x03：发送心跳包
#             // 0x04：虚拟客户端上线通知回复
#             // 0x05：虚拟App数据json格式数据
#             // 0x06：升级数据
#             // 0x07：接收虚拟驱动信息上报反馈
#   //  Data_len	2		数据长度
#   //  Data		Data_len
#   //=====外部程序发送到网关程序的数据格式
#   //  数据结构：
#   //  Head	1	0xF9	协议头
#   //  DataId	1		数据包标识
#             //  0x00：Zigbee协调器串口协议数据
#             //  0x01：虚拟驱动上线通知（通知网关驱动启动了，如果是虚拟zigbee3.0设备则向网关发送的第一条数据应该为这个，声明该驱动为虚拟zigbee3.0设备驱动）
#             //  0x03：响应心跳包
#             //  0x04：虚拟App上线通知（如果虚拟app通过json格式控制网关的客户端程序（如魔镜），声明该驱动为虚拟app客户端，用json格式通信）
#             //  0x05：虚拟App数据json格式数据
#             //  0x06：升级数据
#             //  0x07：虚拟驱动信息上报。虚拟驱动上报驱动信息，包括硬件版本、软件版本、ImageType和驱动标识号。
#   //  Data_len	2		数据长度
#   //  Data		Data_len
#  */





#lancaigang240509：如果16色HUB热插拔或者AMS热插拔，会导致/tty/USB0编程/tty/USB1
# 默认串口
SERIAL_PORT1 = "/dev/ttyACM1"
SERIAL_PORT2 = "/dev/ttyACM2"  
# 最大换色数量
AMS_MAX_CHANNEL = 32  
# 用于循环事件, 串口查询时间间隔(S)
SERIAL_PORT_POLL_INTERVAL = 5.0  
# usb转ttl串口波特率
SERIAL_PORT_BAUD = 19200  





# 工作模式
AMS_WORK_MODE_UNKNOW = 0  # 未知模式；不开启断料检测功能
AMS_WORK_MODE_MC = 1  # 多色打印模式
AMS_WORK_MODE_MA = 2  # 多色中单色自动续料模式
AMS_WORK_MODE_FILA_RUNOUT = 3  # 单色断料模式



#lancaigang240115：默认不自动连接
# 默认不会设备自动连接
AMS_AUTO_CONNECT = False  
# 默认切断线材的X坐标值
AMS_FILA_CUT_X_POSITION = 313
#lancaigang240325：切线Y坐标
AMS_FILA_CUT_Y_POSITION = 307
# 默认切断线材的Z坐标抬升值 1.2
#lancaigang240603：新版热床不抬高
AMS_FILA_CUT_Z_POSITION_LIFTING = 0.2
AMS_FILA_CUT_Z_POSITION_UP = 0.2
# 默认喷头插入线材时ADC值
AMS_TOOLHEAD_FILA_EXIST_ADC_VALUE = 0.3  
# 默认喷头拔出线材时ADC值
AMS_TOOLHEAD_FILA_EMPTY_ADC_VALUE = 0.5  




# 等待时喷头的最大移动速度(mmpm)
CHANGE_CHANNEL_WAIT_MAX_MOVEMENT_SPEED = 180  
# 等待时画线的线宽(mm)
CHANGE_CHANNEL_WAIT_LINE_WIDTH = 0.5  
#lancaigang20231016：120秒
 # 等待换线的默认时间(s)
 #lancaigang240912：新AMS，改为100秒
 #lancaigang250111：改为90秒
  #lancaigang250113：改为50秒
CHANGE_CHANNEL_WAIT_TIMEOUT = 80


# 换色时Z轴抬升由gcode代码控制高度
# 0=切线前默认由内部gcode执行
CHANGE_CHANNEL_IF_Z_LIFTING_UP_BY_GCODE = 0  




# ADC 检测配置
#喷头ADC主动上报时间；15ms
#TOOLHEAD_ADC_REPORT_TIME = 0.015
#TOOLHEAD_ADC_DEBOUNCE_TIME = 0.025
#lancaigang250409：更改ADC上报时间
TOOLHEAD_ADC_REPORT_TIME = 0.50
TOOLHEAD_ADC_DEBOUNCE_TIME = 0.70
#喷头ADC采样时间
TOOLHEAD_ADC_SAMPLE_TIME = 0.100
#喷头ADC采样数目
TOOLHEAD_ADC_SAMPLE_COUNT = 4



AMS_MC_MODE = 0  # 多色运行模式
AMS_MA_MODE = 1  # 续料运行模式



MC_STANDBY = 0  # 待机阶段
MC_PREPARTION = 1  # 备料阶段
MC_CHANGING_P1 = 2  # 换料阶段1
MC_CHANGING_P2 = 3  # 换料阶段2
MC_FORCE_FEED = 4  # 换料阶段强制补料
MC_PRINTING = 5  # 打印阶段补料
MC_ROLLBACK = 6  # 完全退料
MC_PARKBACK = 7  # 退料到停靠位
MC_PARKALL = 8  # 全部退料到停靠位
MC_CLEANING = 9  # 清空所有线料
MC_ERR_TIMEOUT = 10  # 超时出错状态
MC_ERR_RUNOUT = 11  # 断料出错状态
MC_ERR_BLOCKUP = 12  # 堵料出错状态



MA_STANDBY = 0  # 待机阶段
MA_FIND_WORK_CHAN = 1  # 查找主进线通道
MA_FAST_FEED = 2  # 快速补料
MA_FORCE_FEED = 3  # 强制补料
MA_PRINTING_FEED = 4  # 打印阶段
MA_MANUAL_ADD_FILA = 5  # 手动加线材
MA_AUTO_CHANGE_FILA = 6  # 断料自动换料
MA_ROLLBACK = 7  # 完全退料
MA_CLEANING = 8  # 清空所有线料
MA_ERR_TIMEOUT = 9  # 超时出错状态




#lancaigang231104：1改3
# 断料检测周期时间(S)
#lancaigang230104：3改为6
AMS_FILA_RUNOUT_TIMER = 2.0
# 串口接收周周期时间(S)
#lancaigang240104:0.2改为
#lancaigang240104:0.2改为0.1
AMS_SERIALPORT_RECV_TIMER = 0.1 #100ms
#lancaigang231104：8改为15
# 暂停时间计数上限值(S)
RUNOUT_MAX_PAUSE_TIME_COUNT = 15

#CS 00 N0 M03 T04 C0
# // 串口报告给缓冲板和打印机
# // CS设备id   运行模式 前个mc状态   当前mc状态  通道号
# // CS00       N0      M09         T09         C5
# // CS00       N0      M02         T03         C0
# // CS00       N0      M08         T10         C1
#    deviceid   mode    pre_state   state       chan
# 串口接收字符串正则匹配表达式
AMS_SERIALPORT_RECEIV_PARSE_PATTERN = r"CS(?P<id>\d{2})N(?P<mode>\d{1})M(?P<pre_state>\d{2})T(?P<state>\d{2})C(?P<chan>\d{1})"




G_EmptyString = ""  # 空字符串



# 查询设备标准状态
G_DictPhrozenCmdP114 = {#python字典key-value
    "cmd": "P114",#websocket命令
    "params": [G_EmptyString],#参数
    "mcu_cmd": ["SD"],#多色主板命令SD
    "desc": "查询多色主板传感器状态",
}



# 查询设备基础状态
G_DictPhrozenCmdP104 = {#python字典key-value
    "cmd": "P104",
    "params": [G_EmptyString],#python数组列表
    "mcu_cmd": ["SB"],#python数组列表
    "desc": "查询多色主板基础状态",
}



# 连接设备
G_DictPhrozenCmdP28 = {#python字典key-value
    "cmd": "P28",
    "params": [G_EmptyString],#python数组列表
    "mcu_cmd": [G_EmptyString],#python数组列表
    "desc": "连接多色主板",
}



# 断开连接
G_DictPhrozenCmdP29 = {#python字典key-value
    "cmd": "P29",
    "params": [G_EmptyString],#python数组列表
    "mcu_cmd": [G_EmptyString],#python数组列表
    "desc": "断开连接多色主板",
}



# 自动编排设备ID(用于多设备自动组网)
G_DictPhrozenCmdP30 = {#python字典key-value
    "cmd": "P30",
    "params": [G_EmptyString],#python数组列表
    "mcu_cmd": ["I"],#数组
    "desc": "多个多色主板自动编排设备Id",
}



# 设备工作模式
G_DictPhrozenP0 = {#python字典key-value
    "cmd": "P0",
    "params": ["M","B"],#数组
    "mcu_cmd": ["MC", "MA"],#python数组列表
    "desc": "设置多色主板工作模式",
}



# 线料退线处理
G_DictPhrozenCmdP2 = {#python字典key-value
    "cmd": "P2",
    "params": ["A","B"],#数组
    "mcu_cmd": ["AP", "CL"],#python数组列表
    "desc": "多色主板退线相关命令",
}



# 紧急停止设备
G_DictPhrozenCmdP4 = {#python字典key-value
    "cmd": "P4",
    "params": [G_EmptyString],#python数组列表
    "mcu_cmd": ["SP"],#数组
    "desc": "多色主板紧急停止",
}


# P1 T[n]n:1 ~32(设备无组网,取1 ~4)手动换到指定通道,仅换线(用于测试)；====="T"；
# P1 B[n]n:1 ~32(设备无组网,取1 ~4)指定通道线料完全退出 Yes；====="B"；
# P1 D[n]；n:1~32(设备无组网,取1~4)；指定通道的线料后退停泊在停靠位待命状态 Yes；====="P"；
# P1 C[n] n:1~32(设备无组网,取1~4) 自动换到指定通道(多动作命令,包含切线, 换线, 等待)；====="T"；
#lancaigang231202:
# P1 E[n]；n:1~32(设备无组网,取1~4)；指定通道的线料强制前转，需要注意取出喷头上的料管 Yes；====="E?"；
# lancaigang240228：喷头回抽一段距离，需要stm32先回退一段距离
# P1 G[n]；n:1~32(设备无组网,取1~4)；指定通道的线料回退一段距离 Yes；====="G?"；
# lancaigang240319：进入特殊补料阶段，缓冲器不满就补料
# =====P1 H[n]；n:1~32(设备无组网,取1~4)；进入特殊补料阶段，缓冲器不满就补料 Yes；====="H?"；
#lancaigang240329：备用
# =====P1 I[n]；手动挤料时stm32需要补料；====="I?"；
# =====P1 J[n]；多色手动吐料；缓冲器不满时补料；
# =====P1 K[n]；
# =====P1 L[n]；
# =====P1 M[n]；
# =====P1 N[n]；
# =====P1 O[n]；
# =====P1 Q[n]；
# =====P1 U[n]；
# =====P1 V[n]；
# =====P1 W[n]；
# =====P1 X[n]；
# =====P1 Y[n]；
# =====P1 Z[n]；
# 设备多色模式下换线处理
G_DictPhrozenCmdP1 = {#python字典key-value
    "cmd": "P1",
    "params": ["S","C","T","B","D","E","G","I","J","K","L","M","N","O","Q","U","V","W","X","Y","Z"],#python数组列表
    "mcu_cmd": ["RD","Tn","Bn","Pn","En","Gn","In","Jn","Kn","Ln","Mn","Nn","On","Qn","Un","Vn","Wn","Xn","Yn","Zn"],#python数组列表
    "desc": "多色主板通道命令",
}



# 换线等待区域处理
G_DictPhrozenCmdP9 = {#python字典key-value
    "cmd": "P9",
    "params": ["X", "Y", "W", "H", "D", "T", "A"],#python数组列表
    "mcu_cmd": [G_EmptyString],#python数组列表
    "desc": "换线喷头等待区域命令",
}


# 吐料次数控制
G_DictPhrozenCmdP10 = {#python字典key-value
    "cmd": "P10",
    "params": ["S"],#python数组列表
    "mcu_cmd": [G_EmptyString],#python数组列表
    "desc": "吐料次数控制",
}


# 执行自动续料
G_DictPhrozenCmdP8 = {#python字典key-value
    "cmd": "P8",
    "params": [G_EmptyString],#python数组列表
    "mcu_cmd": ["FA"],#python数组列表
    "desc": "自动续料命令",
}

G_DictPhrozenCmdTn = {#python字典key-value
    "cmd": "T",
    "params": [G_EmptyString],#python数组列表
    "mcu_cmd": [G_EmptyString],#python数组列表
    "desc": "orca切片换色",
}



# 查询打印头线材传感器ADC值
G_DictPhrozenCmdToolheadAdc = {#python字典key-value
    "cmd": "PRZ_ADC",
    "params": [G_EmptyString],#python数组列表
    "mcu_cmd": [G_EmptyString],#python数组列表
    "desc": "获取喷头是否有线材ADC值",
}

# 1、python ()表示元组，元组是一种不可变序列
#  1）创建如：tuple = (1,2,3) 取数据 tuple[0]......  tuple[0,2].....tuple[1,2]......
# 2)修改元祖：元组是不可修改的
# 3）删除元祖 del tuple
# 4）内置函数：
# cmp（tuple1，tuple2）：比较两个元祖
# len(tuple):计算元组的长度
# max（tuple）：最大值
# min（tuple）：最小值
# tuple（seq）：将列表转为元祖
# 2、python []表示列表，列表是可变的序列
# 1）创建列表l = [1,2,3,4]取数据l[0]........
# 2)列表可修改
# 3）内置函数
# cmp（list1，list2）：比较两个元祖
# len(list):计算元祖的长度
# max（list）：最大值
# min（list）：最小值
# list（seq）：将元祖转为列表
# list.append(obj):在列表末尾新增对象
# list.pop():移除某个数据
# list.remove:移除某个列表中匹配的第一个值
# list.sort():排序
# list.reverse():反转列表
# list.count(bj):计算对象在列表中出现的次数
# list.insert(index,obj) :在某个位置插入对象
# 3、python {} 字典；字典是可变的容器，使用比较灵活
# 1）创建字典：dict = {"a":1,"b":2}. 字典是一对：key， value的键值对 取数据dict['a'],
# 2）可修改
# 3）删除：del dict["a"] 删除某对数据  del dict 删除字典 dict.clear()清除字典所有条目
# 4）内置函数
# cmp（dict1，dict2）：比较两个元祖
# len(dict):计算元祖的长度
# dict.clear():删除字典数据
# dict.get(key, default=None):返回指定值，如果没有返回指定默认值
# dict.has_key(key):判断值是否存在，返回true，false
# dict.item（）以列表值返回返回可遍历的（键，值）的元祖
# dict.key（）返回字典所有的key值

# 1、数组定义和赋值
# Python定义一个数组很简单，直接 arr = [];就可以了，arr就被定义成了一个空数组，只不过这个数组是没有任何值的，我们接下来给arr这个数组赋值看看，
# arr = [ ‘今天’, ‘双11’, ‘你剁手了吗’]; 现在arr数组已经被赋值了三个元素，其实这一步把数组定义和赋值都完成了，在开发中通常也是定义和赋值一步到位的。
# 2、获取数组元素
# 当给一个数组赋值了之后，我们通常需要获取数组中某个指定元素，比如获取arr数组中第一个元素 arr[0]，通过元素下标可获取对应元素的值，
# 注意下标是从0开始的，arr[2]即表示数组中第三个元素，arr[len(arr)-1] 表示数组最后一个元素，len(arr)是指数组的总长度，即一共有多少个元素。
# 3、遍历数组
# 在实际开发中，我们通常是用一个for循环来遍历数组中的元素，如果还不知道for循环是什么的话，可以暂时先跳过这一小部分，后面的文章会再详细讲for循环，
# 关于数组遍历请参考下面这段代码。
# 4、数组元素追加和删除
# 当定义好了一个数组后，我们还可以继续对数组元素进行追加和删除，追加主要有两种方式，分别是 append 和 insert，append是指从数组末尾追加即被添加的元素会
# 放到数组的末尾，insert 可以从指定位置插入元素，比如 arr.insert(2,’我是被插进来的第三个元素哦’)，即arr变成 [ ‘昨天’, ‘今天’, ‘我是被插进来的第二个元
# 素哦’,’你剁手了吗’]。其实数组元素删除也有三种方式，在这里只介绍一种，免得让大家搞混了，使用 arr.pop(2)即可删除数组中第三个元素，注意这个2是指数组
# 下标(索引)，具体的可以参考下面的代码。
# 5、判断某元素是否在数组中
# 我们每天都会重复着“昨天””今天“”明天“，那么 arr = [‘昨天’, ‘今天’, ‘明天’]，现在用Python来判断 “昨天”我还记得做什事情了吗，一个 “in” 就能搞定，
# 具体请看下面的代码。
# 6、数组排序
# 我对这三天的价值进行一下评估，price = [207,1400,50];现在我想用Python帮我把这三个价值分别按从低到高和从高到低排列，并告诉我哪个最高，哪个最低，
# 具体还是看下面的代码吧。

####################################
#类名：
#功能描述：蓝才刚-20230830
####################################
class error(Exception):
    pass

####################################
#类名：
#功能描述：蓝才刚-20230830
####################################
class Base(object):
    ####################################
    #函数名称：
    #输入参数：
    #返 回 值:
    #功能描述：蓝才刚-20230830
    ####################################
    #构造函数初始化
    def __init__(self, config):
        if type(self) is Base:
            raise error("Base类不能创建实例")
        #命令锁令牌
        self.G_AMSSerialCmdLock = False
        #默认喷头没有线材
        self.G_ToolheadIfHaveFilaFlag = False

        # 断线处理定时器
        self.G_FilaRunoutTimmer = None

        # 串口接收定时器
        self.G_SerialPort1RecvTimmer = None
        # 串口接收定时器
        self.G_SerialPort2RecvTimmer = None
        
        #printer.cfg配置文件
        self.G_PhrozenConfig = config
        self.G_PhrozenPrinter = config.get_printer()
        self.G_PhrozenReactor = self.G_PhrozenPrinter.get_reactor()
        #暂停恢复命令
        self.G_PhrozenPrinterCancelPauseResume = self.G_PhrozenPrinter.load_object(config, "pause_resume")
        #gcode命令
        self.G_PhrozenGCode = self.G_PhrozenPrinter.lookup_object("gcode")
        #响应fluidd信息
        self.G_PhrozenFluiddRespondInfo = self.G_PhrozenGCode.respond_info

        #lancaigang241105:
        self.G_AMS1DeviceState = {}
        self.G_AMS2DeviceState = {}


        #usb转ttl串口
        self.G_Serialport1Define = self.G_PhrozenConfig.get("dev_port", SERIAL_PORT1)
        self.G_Serialport2Define = self.G_PhrozenConfig.get("dev_port2",SERIAL_PORT2)

        #printer.cfg;是否自动连接
        self.G_AMSIfAutoConnectFlag = self.G_PhrozenConfig.getboolean("auto_connect", AMS_AUTO_CONNECT)
        #printer.cfg;切线默认x位置
        self.G_AMSFilaCutXPosition = self.G_PhrozenConfig.getfloat("fila_cut_x_pos", AMS_FILA_CUT_X_POSITION)
        #lancaigang240409：y坐标
        self.G_AMSFilaCutYPosition = self.G_PhrozenConfig.getfloat("fila_cut_y_pos", AMS_FILA_CUT_Y_POSITION)
        #printer.cfg;切线默认z抬升位置
        self.G_AMSFilaCutZPositionLiftingUp = self.G_PhrozenConfig.getfloat("fila_cut_x_pos_up", AMS_FILA_CUT_Z_POSITION_UP)
        
        

        
        #printer.cfg;默认喷头线材插入ADC值
        self.G_ToolheadFilaExistAdcValueDefault = self.G_PhrozenConfig.getfloat("fila_exist_value", AMS_TOOLHEAD_FILA_EXIST_ADC_VALUE)
        #printer.cfg;默认喷头线材空ADC值
        self.G_ToolheadFilaEmptyAdcValueDefault = self.G_PhrozenConfig.getfloat("fila_empty_value", AMS_TOOLHEAD_FILA_EMPTY_ADC_VALUE)
        #printer.cfg;喷头线材ADC阈值；(exist+empty)/2
        self.G_ToolheadFilaAdcThresholdValue = (self.G_ToolheadFilaExistAdcValueDefault + self.G_ToolheadFilaEmptyAdcValueDefault) / 2.  # ADC电压基准
        
        #喷头：fila_sensor_pin: _THR:PA2
        #printer.cfg;喷头ADC检测引脚
        self.G_ToolheadFilaSensorPin = self.G_PhrozenConfig.get("fila_sensor_pin", None)
        #喷头ADC值
        Lo_ToolheadAdcPins = self.G_PhrozenPrinter.lookup_object("pins")
        #喷头：fila_sensor_pin: _THR:PA2
        self.G_ToolheadAdc = Lo_ToolheadAdcPins.setup_pin("adc", self.G_ToolheadFilaSensorPin)
        self.G_ToolheadAdc.setup_minmax(TOOLHEAD_ADC_SAMPLE_TIME, TOOLHEAD_ADC_SAMPLE_COUNT)
        #注册回调函数
        self.G_ToolheadAdc.setup_adc_callback(TOOLHEAD_ADC_REPORT_TIME, self.Base_ToolheadAdcCallback)
        Lo_ToolheadQueryAdc = self.G_PhrozenPrinter.lookup_object("query_adc")
        Lo_ToolheadQueryAdc.register_adc("prz_adc", self.G_ToolheadAdc)





        # printer.cfg;换线等待喷头最大移动速度
        self.G_ChangeChannelWaitMaxMovementSpeed = self.G_PhrozenConfig.getint("wait_max_velocity", CHANGE_CHANNEL_WAIT_MAX_MOVEMENT_SPEED)
        #printer.cfg;换线等待划线宽度
        self.G_ChangeChannelWaitLineWidth = self.G_PhrozenConfig.getfloat("wait_line_width", CHANGE_CHANNEL_WAIT_LINE_WIDTH)
        #printer.cfg;换线超时时间，可通过printer.cfg文件设置或默认时间
        self.G_ChangeChannelTimeout = self.G_PhrozenConfig.getint("wait_timeout", CHANGE_CHANNEL_WAIT_TIMEOUT)
        #printer.cfg;换线是否由gcode代码抬升z轴高度
        self.G_ChangeChannelIfZLiftingUpByGcode = self.G_PhrozenConfig.getint("switch_fila_zup_by_gcode", CHANGE_CHANNEL_IF_Z_LIFTING_UP_BY_GCODE)




        #lancaigang231207：换料过程中，如果进料用完卡料，需要从喷头上料管取出，不能回退线材
        self.G_IfInFilaBlockFlag = False

        #lancaigang231207：stm32暂停数据
        self.G_SerialRxASCIIStr = None

        #lancaigang231207：是否时换料过程
        self.G_IfChangeFilaOngoing= False

        #lancaigang231215：stm32暂停主动上报，是否马上暂停还是计数重试几次后再暂停
        self.G_STM32PauseCount= 0


        #lancaigang231212：主动暂停标志位，如果打印过程中暂停，即喷头有检测到线材情况下暂停，恢复后不用回退再进料
        self.G_IfToolheadHaveFilaInitiativePauseFlag = False

        #lancaigang240108：单色续料恢复标志位，用于断线续打挤料完成后的恢复打印
        self.G_M2MAModeResumeFlag = False

        #lancaigang240108：
        self.P0M3FilaRunoutSpittingFinished = True  # 单色模式断料处理完成标志

        #lancaigang240113：手动进料T?过滤smt32上报的超时
        self.ManualCmdFlag = False

        #lancaigang240123：MA自动续料超时处理
        self.AMSRunoutPauseTimeCount = 0
        self.AMSRunoutPauseTimeoutFlag = 0

        #lancaigang240124：stm32主动上报暂停，只能暂停1次
        self.STM32ReprotPauseFlag = 0

        #lancaigang240223：喷头切线失败标记
        self.ToolheadCutFlag = False

        #lancaigang240229：PG101
        self.IfDoPG102Flag = False

        #lancaigang240320：PG102
        self.PG102Flag = False

        #lancaigang240320：PG102
        self.PG102DelayPauseFlag = False

        #lancaigang240325：MC模式可以恢复标签
        self.G_MCModeCanResumeFlag = False

        #lancaigang240325：断线进料暂停的通道号
        self.G_Pause1Channel = -1
        #lancaigang240325：
        self.G_PauseTriggerWhileChangeChannelFlag = False

        #lancaigang240325：
        self.G_ResumeProcessCheckPauseStatus = False

        #lancaigang240325：
        self.G_PauseToLCDString = ""

        #lancaigang240410：
        self.G_CancelFlag = False

        #lancaigang240411：如果没有收到P0 M3命令，不使用断料检测机制
        self.G_P0M3Flag = False

        #lancaigang240412:AMS多色标签
        self.G_AMSDevice1IfNormal=False

        #lancaigang241029:AMS多色标签
        self.G_AMSDevice2IfNormal=False

        #lancaigang240415：喷头有线材，第一次不用吐料
        self.G_P0M3ToolheadHaveFilaNotSpittingFlag = False

        #lancaigang240427：AMS异常重启，需要记录
        self.G_AMS1ErrorRestartFlag = False
        self.G_AMS1ErrorRestartCount = 0
        #lancaigang240521：恢复的时候，如果发现AMS异常重启，可以认为是热插拔AMS，执行完整的退料换料过程
        self.G_ResumeCheckAMS1ErrorRestartFlag = False

        #lancaigang241030:
        self.G_AMS2ErrorRestartFlag = False
        self.G_AMS2ErrorRestartCount = 0
        self.G_ResumeCheckAMS2ErrorRestartFlag = False


        #lancaigang240528：P114运行标签
        self.G_P114RunFlag = 0


        #lancaigang241101：吐料次数控制
        self.G_P10SpitNum = 0

        #lancaigang241106：单色续料MA进入打印标志
        self.G_P0M2MAStartPrintFlag = 0

        #lancaigang250102：打印换料次数计算
        self.G_PrintCountNum = 0

        #lancaigang250104：P2A3标志位
        self.G_P2A3Flag = 0

        #lancaigang250514：解析串口屏配置数据
        self.G_P0M1MCNoneAMS = -1

        self.G_AutoReplaceState = -1
        self.G_ChromaKitNum = -1
        self.G_ChromaKitAccessT0 = -1
        self.G_ChromaKitAccessT1 = -1
        self.G_ChromaKitAccessT2 = -1
        self.G_ChromaKitAccessT3 = -1
        self.G_ChromaKitAccessT4 = -1
        self.G_ChromaKitAccessT5 = -1
        self.G_ChromaKitAccessT6 = -1
        self.G_ChromaKitAccessT7 = -1
        self.G_ChromaKitAccessT8 = -1
        self.G_ChromaKitAccessT9 = -1
        self.G_ChromaKitAccessT10 = -1
        self.G_ChromaKitAccessT11 = -1
        self.G_ChromaKitAccessT12 = -1
        self.G_ChromaKitAccessT13 = -1
        self.G_ChromaKitAccessT14 = -1
        self.G_ChromaKitAccessT15 = -1

        #lancaigang250526：暂停中，不允许新的gcode命令，需等待暂停完成
        self.G_KlipperInPausing = False

        #lancaigang250527：暂停快速执行
        self.G_KlipperQuickPause = False

        #lancaigang250607：打印状态；1-退料中；2-进料中；3-打印中；4-暂停
        self.G_KlipperPrintStatus= -1

        #lancaigang250619：
        self.G_PauseToUSBConnectString = ""

        #lancaigang250724:镜像id
        self.G_ImageId= -1
        self.G_HwId= -1

        #lancaigang250805:切刀测试
        self.G_CutCheckTest = False

        #lancaigang250812:单色断料检测，补充回到暂停区
        self.G_RetryToPauseAreaFlag = False
        self.G_RetryToPauseAreaCount = 0


        #lancaigang251120：PG108执行标志位；
        self.G_PG108Ingoing=0


    ####################################
    #函数名称：
    #输入参数：
    #返 回 值:
    #功能描述：蓝才刚-20230830
    ####################################
    # 获取命令锁
    def Base_AMSSerialCmdLock(self):
        self.G_PhrozenFluiddRespondInfo("[(base.python)Base_AMSSerialCmdLock]")
        for _ in range(8):
            if self.G_AMSSerialCmdLock==False:
                #获取命令锁令牌
                #上锁
                self.G_AMSSerialCmdLock = True
                return True
            #延时0.2s循环
            time.sleep(0.2)
        return False
    ####################################
    #函数名称：
    #输入参数：
    #返 回 值:
    #功能描述：蓝才刚-20230830
    ####################################
    # 释放命令锁
    def Base_AMSSerialCmdUnlock(self):
        self.G_PhrozenFluiddRespondInfo("[(base.python)Base_AMSSerialCmdUnlock]")
        #解锁
        self.G_AMSSerialCmdLock = False
    ####################################
    #函数名称：
    #输入参数：
    #返 回 值:
    #功能描述：蓝才刚-20230830
    ####################################
    # 串口接收周期任务, 用于被重写
    def Device_TimmerUart1Recv(self, eventtime):
        self.G_PhrozenFluiddRespondInfo("[(base.python)Device_TimmerUart1Recv]串口1接收线程")
        pass

    ####################################
    #函数名称：
    #输入参数：
    #返 回 值:
    #功能描述：蓝才刚-20230830
    ####################################
    def Device_TimmerUart2Recv(self, eventtime):
        self.G_PhrozenFluiddRespondInfo("[(base.python)Device_TimmerUart2Recv]串口2接收线程")
        pass


    ####################################
    #函数名称：
    #输入参数：
    #返 回 值:
    #功能描述：蓝才刚-20230830
    ####################################
    #喷头检测线材ADC；ms回调
    #250ms
    def Base_ToolheadAdcCallback(self, read_time, read_value):
        #self.G_PhrozenFluiddRespondInfo("[(base.python)Base_ToolheadAdcCallback]")
        _ = read_time
        #喷头是否有线材，ADC值小于阈值代表喷头有线材
        #lancaigang231213：(空+存在)/2
        self.G_ToolheadIfHaveFilaFlag = read_value < self.G_ToolheadFilaAdcThresholdValue
        #self.G_PhrozenFluiddRespondInfo("[(base.python)Base_ToolheadAdcCallback]self.G_ToolheadIfHaveFilaFlag=%d" % (self.G_ToolheadIfHaveFilaFlag))
        #print(read_value)
        #print(self.G_ToolheadFilaAdcThresholdValue)
