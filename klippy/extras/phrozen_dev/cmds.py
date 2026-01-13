####################################
#项目名称：
#芯片类型: 
#功能: 
#研发人员：蓝才刚
#开发时间: 20230830
####################################

import os
import numpy as np

import logging
import json
import time
import serial
from .base import *




#c语言类型二进制流数据
from ctypes import *


# （2）python中的类实际上就可以用来当做结构体使用，因为结构体体现的就是一种面向对象编程思想中抽象类集合以及对象的互相映射关系，代码示例如下所示：
# class item:
#     def __init__(self):
#         self.name = ''
#         self.size = 10
#         self.list = []
# 从上面的示例就可以看出来类是一个自成一体的完全封闭结构，而在类里面定义了三个变量，这三个变量就是类的成员。并且这三个变量的数据类型分别为字符串、整数以及列表，这也正好就是符合了结构体多种不同数据类型成员集合的定义。
# 类还可以通过传递不同的数值将这个结构体实例化成具有不同意义和作用的对象，代码示例如下所示：
# a = item()
# a.name = 'cup'
# a.size = 8
# a.list.append('water')


# 结构体数组
# 在C语言中我们可以通过struct关键字定义结构类型，结构中的字段占据连续的内存空间，每个结构体占用的内存大小都相同，因此可以很容易地定义结构数组。和C语言一样，在NumPy中也很容易对这种结构数组进行操作。只要NumPy中的结构定义和C语言中的定义相同，NumPy就可以很方便地读取C语言的结构数组的二进制数据，转换为NumPy的结构数组。假设我们需要定义一个结构数组，它的每个元素都有name, age和salary字段。在NumPy中可以如下定义：
# import numpy as np
# MyType=np.dtype({
#     'names':['name','age','salary'],
#     'formats':['S32','i','f']#必须加s，且S大写
# })
# a=np.array([("tang",23,130.2),("wang",22,100.2)],
# dtype=MyType)
# #或者Data=np.array([(‘zero’,0.,0.)]*10,dtype=MyType) #创建Data[2]
# #Date[0]['name']="tang"

# 在python中使用c_type时出现little-endian的问题
# 项目中需要组装与解析底层通信协议中定义的数据包，为此使用了python中的c_type类来定义一个协议包的具体内容，例如，协议中数据包的描述如下，
# 字段名称	长度(bytes)
# 命令字	2
# 类型	1
# 数据1	4
# 数据2	2
# python中的定义，
# class EProfile(Structure):
#     _pack_ = 1
#     _fields_ = [('command_id', c_short),
#                 ('type', c_ubyte),
#                 ('data1', c_int),
#                 ('data2', c_short)]
# 其中c_short为2字节，c_ubyte为1字节，c_int为4字节。但是组装好数据，转换为字节流之后却发现，多字节的字段是用little-endian格式存储的。比如，命令字值如果是1000的话，那么转换成2字节十六进制数为0x03E8，然而字节流中输出的却是0xE803。
# 解决方案：把基类Structure换成BigEndianStructure即可解决。


# union在内存中只占有一块内存空间，空间大小由union中占位最多的数据类型决定，union在初始化的时候，union的值，由最后一个有效参数决定
# from ctypes import *
# print "aaa:"
# value = raw_input()
# v=int(value)
# vv=long(value)
# vvv=value
# class aaa(Union):
#     _fields_=[
#        ("aaa",c_int),
#        ("bbb",c_long),
#        ("ccc",c_char),       ]
# print "aaaaaaa:%s" %value
# a=aaa(v,vv,vvv)
# print "aaa: %d" %a.aaa
# print "bbb: %ld" %a.bbb
# print "ccc: %s" %a.ccc
# test1
# c:\Python27>python D:\jincheng\workspace\GrayHatPython\chapter1.py
# aaa:
# 6
# aaaaaaa:6
# aaa: 54
# bbb: 54
# ccc: 6
# test2
# c:\Python27>python D:\jincheng\workspace\GrayHatPython\chapter1.py
# aaa:
# 66
# aaaaaaa:66
# aaa: 13878
# bbb: 13878
# ccc: 66
# 修改
# from ctypes import *
# print "aaa:"
# value = raw_input()
# v=int(value)
# print "v %d" %v
# print "bbb:"
# val=raw_input()
# vv=long(val)
# vvv=value
# class aaa(Union):
#     _fields_=[
#        ("aaa",c_int),
#        ("bbb",c_long),
#        ("ccc",c_char * 6),       ]
# print "aaaaaaa:%s" %value
# a=aaa(v,vv)
# s=a.aaa
# ss=int(s)
# print "ss %d" %ss
# print "aaa: %d" %a.aaa
# print "bbb: %ld" %a.bbb
# print "ccc: %s" %a.ccc
# test
# D:\Python27>python d:\demo.py
# aaa:
# 66
# v 66
# bbb:
# 55
# aaaaaaa:66
# ss 55
# aaa: 55
# bbb: 55
# ccc: 7


# // 简要信息结构
# typedef struct St_SystemSimpleStatus {
#     // 消息标志(固定CMD_RSP_SYSTEM_STATE)
#     uint8_t InfoFlag;
#     // 当前设备ID
#     int CurrentDeviceId;
#     // 最后设备ID, 说明有？台设备组网
#     int EndDeviceId;
#     // 运行模式(多色模式：00  续料模式：01)
#     uint8_t DeviceMode;
#     // 多色模式下状态码
#     uint8_t MCStateMachine : 4;
#     // 续料模式下状态码
#     uint8_t MAStateMachine : 4;
# } St_SystemSimpleStatus;
####################################
#类名：
#功能描述：蓝才刚-20230830
####################################
class AMSSimpleInfoSt(LittleEndianStructure):#小端模式
    _pack_ = 1
    _fields_ = [
        ("info_flag", c_uint8),#8bit；flag标签
        ("dev_id", c_uint8),#8bit；多色设备id
        ("end_dev_id", c_uint8),#8bit；最后多色设备id
        ("dev_mode", c_uint8),#8bit；多色设备模式
        ("mc_state", c_uint8, 4),#4bit；mc状态
        ("ma_state", c_uint8, 4),#4bit；ma状态
    ]

####################################
#类名：
#功能描述：蓝才刚-20230830
####################################
class AMSSimpleInfoBytes(Union):#多色主板简单状态
    _fields_ = [
        ("field", AMSSimpleInfoSt),
        ("whole", c_uint8 * sizeof(AMSSimpleInfoSt)),
    ]

# // 详细信息结构
# typedef struct St_SystemDetailStatus {
#     // 消息标志(固定CMD_RSP_SYSTEM_STATE)
#     uint8_t InfoFlag;
#     // 当前设备ID
#     int8_t CurrentDeviceId;
#     // 最后设备ID, 说明有？台设备组网
#     int8_t EndDeviceId;
#     //  活动的设备ID, 说明第？台设备是当前活动设备
#     int8_t ActiveDeviceId;
#     // 目标设备ID，说明第？台设备是需要切换到的设备
#     int8_t TargetDeviceId;
#     // 其它(用于占位保留)
#     uint8_t Others;
#     // 运行模式(多色模式：00  续料模式：01)
#     uint8_t DeviceMode : 2;
#     // 任一电机在运行(全部都停止：0)
#     uint8_t IfAnyMotorRuning : 1;
#     // 缓冲器线空(触发：1  不触发：0)
#     uint8_t CacheEmptyIfTrigger : 1;
#     // 缓冲器线满(触发：1  不触发：0)
#     uint8_t CacheFullIfTrigger : 1;
#     // 缓冲器线存在(触发：1  不触发：0)
#     uint8_t CacheExistIfTrigger : 1;
#     // 保留
#     uint8_t Reserve : 2;
#     // 多色模式下状态码
#     uint8_t MCStateMachine : 4;
#     // 续料模式下状态码
#     uint8_t MAStateMachine : 4;
#     // 入口传感器状态(以bit为单位代表触状态, 触发：1  不触发：0)
#     uint32_t EntryPositionIfTriggerBitMask;
#     // 停靠位传感器状态(以bit为单位代表触状态, 触发：1  不触发：0)
#     uint32_t ParkPositionIfTriggerBitMask;
# } St_SystemDetailStatus;
####################################
#类名：
#功能描述：蓝才刚-20230830
####################################
class AMSDetailInfoSt(LittleEndianStructure):#小端模式
    _pack_ = 1
    _fields_ = [
        ("info_flag", c_uint8),#8bit；flag标签
        ("dev_id", c_uint8),#8bit；
        ("end_dev_id", c_int8),#8bit；
        ("active_dev_id", c_int8),#8bit；
        ("target_dev_id", c_int8),#8bit；
        ("others", c_uint8),#8bit；

        ("dev_mode", c_uint8, 2),#2bit；多色设备模式
        ("any_motor_runing", c_uint8, 1),#1bit；#是否有电机在运行
        ("cache_empty", c_uint8, 1),#1bit；#缓冲器空状态
        ("cache_full", c_uint8, 1),#1bit；#缓冲器满状态
        ("cache_exist", c_uint8, 1),#1bit；#缓冲器线存在状态
        ("reserve", c_uint8, 2),#2bit；

        ("mc_state", c_uint8, 4),#4bit；#mc状态
        ("ma_state", c_uint8, 4),#4bit；#ma状态

        ("entry_state", c_uint32),#32bit；#进料入口位状态
        ("park_state", c_uint32),#32bit；#停靠位状态
    ]

####################################
#类名：
#功能描述：蓝才刚-20230830
####################################
class AMSDetailInfoBytes(Union):#多色主板详细状态
    _fields_ = [
        ("field", AMSDetailInfoSt),
        ("whole", c_uint8 * sizeof(AMSDetailInfoSt)),
    ]

####################################
#类名：
#功能描述：蓝才刚-20230830
####################################
class Commands(Base):
    ####################################
    #函数名称：
    #输入参数：
    #返 回 值:
    #功能描述：蓝才刚-20230830
    ####################################
    #构造函数初始化
    def __init__(self, config):
        super(Commands, self).__init__(config)

        #tty串口是否连接
        self.G_SerialPort1OpenFlag = False

        #tty串口是否连接
        self.G_SerialPort2OpenFlag = False


        #MC换料首次换线
        self.G_ChangeChannelFirstFilaFlag = True
        #喷头首次进料
        self.G_ToolheadFirstInputFila = False  # 首次供料
        #klipper是否暂停
        self.G_KlipperIfPaused = False
        #移动速度因子
        self.G_MovementSpeedFactor = 1.0 / 60
        #喷头最后的位置
        self.G_ToolheadLastPosition = None
        #AMS工作模式
        self.G_AMSDeviceWorkMode = AMS_WORK_MODE_UNKNOW  # 默认工作模式未知模式

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

        #python字典
        #P9 X190.290 Y238.700 W2.010 H11.200 D1
        # 喷头在换线材期间等待参数
        self.G_DictChangeChannelWaitAreaParam = {#python {} 字典 key-value键值对
            "T": self.G_ChangeChannelTimeout,     #换料超时时间(秒)，默认120秒
            "A": 0,         # 动作Action
            "D": 0,         # 默认方向X方向或Y方向
            "X": 0.0,       # 等待区基点X坐标
            #lancaigang20231020：
            "Y": 20.0,      # 等待区基点Y坐标
            "W": 0.0,       # 等待区基点X方向宽度
            "H": 0.0,       # 等待区基点Y方向高度
        }



        # 以下参数在connect中被赋值
        #喷头
        self.G_ProzenToolhead = None
        #喷头手动移动
        self.G_ToolheadManualMovement = None
        #等待喷头移动结束
        self.G_ToolheadWaitMovementEnd = None


        #lancaigang231115：打印换料超时，添加续打功能
        #lancaigang231216：默认使用通道0，未知通道
        self.G_ChangeChannelTimeoutOldChan=-1
        self.G_ChangeChannelTimeoutOldGcmd=None
        #lancaigang240912:新AMS，使用新旧通道记录
        self.G_ChangeChannelTimeoutNewChan=-1
        self.G_ChangeChannelTimeoutNewGcmd=None


        #lancaigang231206：恢复过程中不允许暂停
        self.G_ChangeChannelResumeFlag = False

        # 准备生成路径
        self.ChangeWaitMoveArea = []  # 路径队列


        #lancaigang231216：换料等待区域XY基坐标
        self.G_XBasePosition=0
        self.G_YBasePosition=0

        #lancaigang231216：如果换料期间点击暂停，刚好换料期间抬升了z轴，到执行暂停时，把z轴高度也保存了，导致整体高度异常
        self.G_IfZPositionLiftUpFlag = False

        #lancaigang231219:
        self.G_SerialPort1Obj=None

        #lancaigang241029:
        self.G_SerialPort2Obj=None

        #lancaigang241030:
        self.G_SerialPortHaveOpenedCount=0
        self.G_SerialPortIsOpenCount=0







    ####################################
    #函数名称：
    #输入参数：
    #返 回 值:
    #功能描述：蓝才刚-20230830
    ####################################
    def Cmds_MoveTo(self, pos, velocity):
        #无法获取喷头对象
        if self.G_ProzenToolhead is None:
            return

        #等待喷头移动
        self.G_ProzenToolhead.wait_moves()
        #获取喷头最后的位置
        self.G_ToolheadLastPosition = self.G_ProzenToolhead.get_position()

        for index, p in enumerate(pos):
            self.G_ToolheadLastPosition[index] = p

        #喷头手动移动
        self.G_ProzenToolhead.manual_move(self.G_ToolheadLastPosition, velocity * self.G_MovementSpeedFactor)
        #等待喷头移动
        self.G_ProzenToolhead.wait_moves()
    ####################################
    #函数名称：
    #输入参数：
    #返 回 值:
    #功能描述：蓝才刚-20230830
    ####################################
    #串口发送不等待响应
    def Cmds_AMSSerial1Send(self, cmd):
        if self.G_SerialPort1OpenFlag==False:
            self.G_PhrozenFluiddRespondInfo("[(cmds.py)Cmds_AMSSerial1Send]tty1串口发送失败；AMS1多色未连接，请先发送P28")
            try:
                self.G_PhrozenFluiddRespondInfo("[(cmds.py)Cmds_AMSSerial1Send]重新初始化串口1")
                self.G_SerialPort1Obj = serial.Serial(self.G_Serialport1Define, SERIAL_PORT_BAUD, timeout=3)
                #串口打开成功
                if self.G_SerialPort1Obj is not None:
                    if self.G_SerialPort1Obj.is_open:
                        self.G_SerialPort1OpenFlag = True
                        self.G_PhrozenFluiddRespondInfo("重新初始化串口1成功")
                        #lancaigang231213：打开串口
                        self.G_SerialPort1Obj.flushInput()  # clean serial write cache
                        self.G_SerialPort1Obj.flush()
                        self.G_PhrozenFluiddRespondInfo("串口1清空")
                        self.G_PhrozenFluiddRespondInfo("重新注册串口1回调函数")
                        self.G_SerialPort1RecvTimmer = self.G_PhrozenReactor.register_timer(self.Device_TimmerUart1Recv, self.G_PhrozenReactor.NOW)
            except:
                self.G_PhrozenFluiddRespondInfo("未能打开tty1口，请检查USB口或重启尝试")
            return

        self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_AMSSerial1Send]发送命令: cmd=%s" % cmd)

        try:
            self.G_PhrozenFluiddRespondInfo("发送前，重新初始化串口1")
            self.G_SerialPort1Obj = serial.Serial(self.G_Serialport1Define, SERIAL_PORT_BAUD, timeout=3)
            #串口打开成功
            if self.G_SerialPort1Obj is not None:
                if self.G_SerialPort1Obj.is_open:
                    #tty1串口发送命令锁
                    #上锁
                    if self.Base_AMSSerialCmdLock():
                        self.G_SerialPort1Obj.flush()
                        #tty1串口发送
                        self.G_SerialPort1Obj.write(cmd.encode())#.encode()
                        self.G_PhrozenFluiddRespondInfo("self.G_SerialPort1Obj.write")
                        self.G_SerialPort1Obj.flush()
                        #解锁
                        self.Base_AMSSerialCmdUnlock()
                        
        except:
            self.G_PhrozenFluiddRespondInfo("未能打开tty1口，请检查USB口或重启尝试")
            #解锁
            self.Base_AMSSerialCmdUnlock()



    ####################################
    #函数名称：
    #输入参数：
    #返 回 值:
    #功能描述：蓝才刚-20230830
    ####################################
    def Cmds_AMSSerial2Send(self, cmd):
        if self.G_SerialPort2OpenFlag==False:
            self.G_PhrozenFluiddRespondInfo("[(cmds.py)Cmds_AMSSerial2Send]tty2串口发送失败；AMS2多色未连接，请先发送P28")
            try:
                self.G_PhrozenFluiddRespondInfo("[(cmds.py)Cmds_AMSSerial2Send]重新初始化串口2")
                self.G_SerialPort2Obj = serial.Serial(self.G_Serialport2Define, SERIAL_PORT_BAUD, timeout=3)
                #串口打开成功
                if self.G_SerialPort2Obj is not None:
                    if self.G_SerialPort2Obj.is_open:
                        self.G_SerialPort2OpenFlag = True
                        self.G_PhrozenFluiddRespondInfo("重新初始化串口2成功")
                        self.G_SerialPort2Obj.flushInput()  # clean serial write cache
                        self.G_SerialPort2Obj.flush()
                        self.G_PhrozenFluiddRespondInfo("串口2清空")
                        self.G_PhrozenFluiddRespondInfo("重新注册串口2回调函数")
                        self.G_SerialPort2RecvTimmer = self.G_PhrozenReactor.register_timer(self.Device_TimmerUart2Recv, self.G_PhrozenReactor.NOW)
            except:
                self.G_PhrozenFluiddRespondInfo("未能打开tty2口，请检查USB口或重启尝试")
            return
        
        self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_AMSSerial2Send]发送命令: cmd=%s" % cmd)


        try:
            self.G_PhrozenFluiddRespondInfo("发送前，重新初始化串口2")
            self.G_SerialPort2Obj = serial.Serial(self.G_Serialport2Define, SERIAL_PORT_BAUD, timeout=3)
            #串口打开成功
            if self.G_SerialPort2Obj is not None:
                if self.G_SerialPort2Obj.is_open:
                    #tty1串口发送命令锁
                    #上锁
                    if self.Base_AMSSerialCmdLock():
                        self.G_SerialPort2Obj.flush()
                        #tty1串口发送
                        self.G_SerialPort2Obj.write(cmd.encode())#.encode()
                        self.G_PhrozenFluiddRespondInfo("self.G_SerialPort2Obj.write")
                        self.G_SerialPort2Obj.flush()
                        #解锁
                        self.Base_AMSSerialCmdUnlock()
                        self.G_PhrozenFluiddRespondInfo("self.G_SerialPort2Obj.write")
        except:
            self.G_PhrozenFluiddRespondInfo("未能打开tty2口，请检查USB口或重启尝试")
            #解锁
            self.Base_AMSSerialCmdUnlock()




    ####################################
    #函数名称：
    #输入参数：
    #返 回 值:
    #功能描述：蓝才刚-20230830
    ####################################
    #串口发送并等待响应
    def Cmds_AMSSerialPort1SendWaitRsp(self, cmd, res_len):
        if self.G_SerialPort1OpenFlag==False:
                self.G_PhrozenFluiddRespondInfo("tty1串口发送失败；AMS1多色未连接，请先发送P28")
                return
        
        self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_AMSSerialPort1SendWaitRsp]发送命令: cmd=%s" % cmd)
        
            
        try:
            #串口打开成功
            if self.G_SerialPort1Obj is not None:
                if self.G_SerialPort1Obj.is_open:
                    #获取命令锁令牌
                    #上锁
                    if self.Base_AMSSerialCmdLock():
                        #tty1串口发送字节流
                        self.G_SerialPort1Obj.write(cmd.encode())
                        self.G_PhrozenFluiddRespondInfo("self.G_SerialPort1Obj.write")
                        self.G_SerialPort1Obj.flush()
                        #tty1串口读取字节流
                        resp = self.G_SerialPort1Obj.read(res_len)
                        #解锁
                        self.Base_AMSSerialCmdUnlock()
                        return resp
        except:
            self.G_PhrozenFluiddRespondInfo("未能打开tty1口，请检查USB口或重启尝试")
            #解锁
            self.Base_AMSSerialCmdUnlock()
        
    
    ####################################
    #函数名称：
    #输入参数：
    #返 回 值:
    #功能描述：蓝才刚-20230830
    ####################################
    #串口发送并等待响应
    def Cmds_AMSSerialPort2SendWaitRsp(self, cmd, res_len):
        if self.G_SerialPort2OpenFlag==False:
                self.G_PhrozenFluiddRespondInfo("tty2串口发送失败；AMS2多色未连接，请先发送P28")
                return
        
        self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_AMSSerialPort2SendWaitRsp]发送命令: cmd=%s" % cmd)

        # #获取命令锁令牌
        # #上锁
        # if self.Base_AMSSerialCmdLock():
        #     #tty2串口发送字节流
        #     self.G_SerialPort2Obj.write(cmd.encode())
        #     self.G_SerialPort2Obj.flush()
        #     #tty2串口读取字节流
        #     resp = self.G_SerialPort2Obj.read(res_len)
        #     #解锁
        #     self.Base_AMSSerialCmdUnlock()
        #     return resp
        try:
            #串口打开成功
            if self.G_SerialPort2Obj is not None:
                if self.G_SerialPort2Obj.is_open:
                    #获取命令锁令牌
                    #上锁
                    if self.Base_AMSSerialCmdLock():
                        #tty2串口发送字节流
                        self.G_SerialPort2Obj.write(cmd.encode())
                        self.G_PhrozenFluiddRespondInfo("self.G_SerialPort2Obj.write")
                        self.G_SerialPort2Obj.flush()
                        #tty2串口读取字节流
                        resp = self.G_SerialPort2Obj.read(res_len)
                        #解锁
                        self.Base_AMSSerialCmdUnlock()
                        return resp
        except:
            self.G_PhrozenFluiddRespondInfo("未能打开tty2口，请检查USB口或重启尝试")
            #解锁
            self.Base_AMSSerialCmdUnlock()
    
    

    ####################################
    #函数名称：
    #输入参数：
    #返 回 值:
    #功能描述：蓝才刚-20230830
    ####################################
    # P1 E[n]；n:1~32(设备无组网,取1~4)；指定通道的线料强制前转，需要注意取出喷头上的料管 Yes；====="E?"；
    def Cmds_P1EnForceForward(self, chan, gcmd):
        self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_P1EnForceForward]发送命令: E%d" % chan)

        #lancaigang240524：用于UIUX动态界面
        self.G_PhrozenFluiddRespondInfo("+E:0,%d" % self.G_ChangeChannelTimeoutNewChan)
        #lancaigang250619:检查AMS是否重新连接成功
        self.Cmds_USBConnectErrorCheck()
        #lancaigang241030:
        if chan in range(1, 5):
            self.Cmds_AMSSerial1Send("E%d" % chan)
            self.G_PhrozenFluiddRespondInfo("串口1发送命令：E%d" % chan)
        elif chan in range(5, 9):
            self.Cmds_AMSSerial2Send("E%d" % (chan-4))
            self.G_PhrozenFluiddRespondInfo("串口2发送命令：E%d" % (chan-4))


        #lancaigang240524：用于UIUX动态界面
        self.G_PhrozenFluiddRespondInfo("+E:1,%d" % self.G_ChangeChannelTimeoutNewChan)

    ####################################
    #函数名称：
    #输入参数：
    #返 回 值:
    #功能描述：蓝才刚-20230830
    ####################################
    # lancaigang240228：喷头回抽一段距离，需要stm32先回退一段距离
    # P1 G[n]；n:1~32(设备无组网,取1~4)；指定通道的线料回退一段距离 Yes；====="G?"；
    def Cmds_P1GnExtruderBack(self, chan, gcmd):
        self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_P1EnForceForward]发送命令: G%d" % chan)

        #lancaigang240524：用于UIUX动态界面
        self.G_PhrozenFluiddRespondInfo("+G:0,%d" % self.G_ChangeChannelTimeoutNewChan)
        #lancaigang250619:检查AMS是否重新连接成功
        self.Cmds_USBConnectErrorCheck()
        #lancaigang241030:
        if chan in range(1, 5):
            self.Cmds_AMSSerial1Send("G%d" % chan)
            self.G_PhrozenFluiddRespondInfo("串口1发送命令：G%d" % chan)
        elif chan in range(5, 9):
            self.Cmds_AMSSerial2Send("G%d" % (chan-4))
            self.G_PhrozenFluiddRespondInfo("串口2发送命令：G%d" % (chan-4))


        #lancaigang240524：用于UIUX动态界面
        self.G_PhrozenFluiddRespondInfo("+G:1,%d" % self.G_ChangeChannelTimeoutNewChan)
    ####################################
    #函数名称：
    #输入参数：
    #返 回 值:
    #功能描述：蓝才刚-20230830
    ####################################
    def Cmds_P1HnSpecialInfila(self, chan, gcmd):
        self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_P1HnSpecialInfila]发送命令: H%d" % chan)

         #lancaigang240524：用于UIUX动态界面
        self.G_PhrozenFluiddRespondInfo("+H:0,%d" % self.G_ChangeChannelTimeoutNewChan)
        #lancaigang250619:检查AMS是否重新连接成功
        self.Cmds_USBConnectErrorCheck()
        #lancaigang241030:
        if chan in range(1, 5):
            self.Cmds_AMSSerial1Send("H%d" % chan)
            self.G_PhrozenFluiddRespondInfo("串口1发送命令：H%d" % chan)
        elif chan in range(5, 9):
            self.Cmds_AMSSerial2Send("H%d" % (chan-4))
            self.G_PhrozenFluiddRespondInfo("串口2发送命令：H%d" % (chan-4))


        #lancaigang240524：用于UIUX动态界面
        self.G_PhrozenFluiddRespondInfo("+H:1,%d" % self.G_ChangeChannelTimeoutNewChan)

    ####################################
    #函数名称：
    #输入参数：
    #返 回 值:
    #功能描述：蓝才刚-20230830
    ####################################
    def Cmds_P1InExtrudeManualIn(self, value):
        command_string = """
                        M106 S0
                        M83
                        G92 E0
                        G1 E%f F300
                        """ % (
                        value,
                    )
        self.G_PhrozenGCode.run_script_from_command(command_string)
        self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_P1InExtrudeManualIn]GCODE命令: %s" % command_string)


    ####################################
    #函数名称：
    #输入参数：
    #返 回 值:
    #功能描述：蓝才刚-20230830
    ####################################
    # =====P1 J[n]；多色手动吐料；缓冲器不满时补料；
    def Cmds_P1JnManualSpitFila(self,chan, gcmd):
        self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_P1JnManualSpitFila]发送命令P1J?")
        self.G_PhrozenFluiddRespondInfo("chan=%d;" % chan)
        self.G_PhrozenFluiddRespondInfo("+J:0,%d" % self.G_ChangeChannelTimeoutNewChan)


        #lancaigang250619:检查AMS是否重新连接成功
        self.Cmds_USBConnectErrorCheck()
        #lancaigang241030:
        if chan in range(1, 5):
            self.Cmds_AMSSerial1Send("J%d" % chan)
            self.G_PhrozenFluiddRespondInfo("串口1发送命令：J%d" % chan)
        elif chan in range(5, 9):
            self.Cmds_AMSSerial2Send("J%d" % (chan-4))
            self.G_PhrozenFluiddRespondInfo("串口2发送命令：J%d" % (chan-4))




        self.G_PhrozenFluiddRespondInfo("+J:1,%d" % self.G_ChangeChannelTimeoutNewChan)

    ####################################
    #函数名称：
    #输入参数：
    #返 回 值:
    #功能描述：蓝才刚-20230830
    ####################################
    # =====P1 I[n]；手动挤料时stm32需要补料；====="I?"；?-挤料多少或回抽多少
    #I2表示挤料，I3表示回抽，I0表示idle
    def Cmds_P1InExtruderBack(self, value, gcmd):
        self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_P1InExtruderBack]发送命令I?")
        #lancaigang250619:检查AMS是否重新连接成功
        self.Cmds_USBConnectErrorCheck()
         #lancaigang240524：用于UIUX动态界面
        self.G_PhrozenFluiddRespondInfo("+I:0,%d" % self.G_ChangeChannelTimeoutNewChan)

        #lancaigang0415：I2表示挤料，I3表示回抽
        if value>0:
            self.G_PhrozenFluiddRespondInfo("发送命令: I2；挤料")

            #lancaigang241031:
            if self.G_SerialPort1OpenFlag == True:
                self.Cmds_AMSSerial1Send("I2")
                self.G_PhrozenFluiddRespondInfo("串口1发送命令：I2")
            elif self.G_SerialPort2OpenFlag == True:
                self.Cmds_AMSSerial2Send("I2")
                self.G_PhrozenFluiddRespondInfo("串口2发送命令：I2")

            #lancaigang240516：防止time too close
            #lancaigang240705：防止多次连击粘包；或time too close
            self.G_ProzenToolhead.dwell(0.5)

            #time.sleep(2)
            self.G_PhrozenFluiddRespondInfo("time.sleep(2)")
        elif value<0:
            self.G_PhrozenFluiddRespondInfo("发送命令: I3；回抽")

            #lancaigang241031:
            if self.G_SerialPort1OpenFlag == True:
                self.Cmds_AMSSerial1Send("I3")
                self.G_PhrozenFluiddRespondInfo("串口1发送命令：I3")
            elif self.G_SerialPort2OpenFlag == True:
                self.Cmds_AMSSerial2Send("I3")
                self.G_PhrozenFluiddRespondInfo("串口2发送命令：I3")

            #lancaigang240516：防止time too close
            #lancaigang240705：防止多次连击粘包；或time too close
            self.G_ProzenToolhead.dwell(0.52)

            #time.sleep(2)
            self.G_PhrozenFluiddRespondInfo("time.sleep(2)")
        elif value==0:
            self.G_PhrozenFluiddRespondInfo("发送命令: AT+IDLE；IDLE状态")

            #lancaigang241031:
            if self.G_SerialPort1OpenFlag == True:
                self.Cmds_AMSSerial1Send("AT+IDLE")
                self.G_PhrozenFluiddRespondInfo("串口1发送命令：AT+IDLE")
            elif self.G_SerialPort2OpenFlag == True:
                self.Cmds_AMSSerial2Send("AT+IDLE")
                self.G_PhrozenFluiddRespondInfo("串口2发送命令：AT+IDLE")

            #lancaigang240516：防止time too close
            #lancaigang240705：防止多次连击粘包；或time too close
            self.G_ProzenToolhead.dwell(0.5)

            #time.sleep(2)
            self.G_PhrozenFluiddRespondInfo("time.sleep(2)")
        else:
            self.G_PhrozenFluiddRespondInfo("发送命令: 无")


        self.Cmds_P1InExtrudeManualIn(value)


        #self.Cmds_AMSSerial1Send("AT+IDLE")
        #self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_P1EnForceForward]发送命令: AT+IDLE；IDLE状态")
        #lancaigang240524：用于UIUX动态界面
        self.G_PhrozenFluiddRespondInfo("+I:1,%d" % self.G_ChangeChannelTimeoutNewChan)




    ####################################
    #函数名称：
    #输入参数：
    #返 回 值:
    #功能描述：蓝才刚-20230830
    ####################################
    #P1 B?;线材回退
    def Cmds_P1BnWholeRollbackAction(self, chan, gcmd):
        self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_P1BnWholeRollbackAction]发送命令: B%d" % chan)
        #lancaigang250619:检查AMS是否重新连接成功
        self.Cmds_USBConnectErrorCheck()
         #lancaigang240524：用于UIUX动态界面
        self.G_PhrozenFluiddRespondInfo("+B:0,%d" % self.G_ChangeChannelTimeoutNewChan)


        #lancaigang241030:
        if chan in range(1, 5):
            self.Cmds_AMSSerial1Send("B%d" % chan)
            self.G_PhrozenFluiddRespondInfo("串口1发送命令：B%d" % chan)
        elif chan in range(5, 9):
            self.Cmds_AMSSerial2Send("B%d" % (chan-4))
            self.G_PhrozenFluiddRespondInfo("串口2发送命令：B%d" % (chan-4))



        #lancaigang240115：如果当前通道不是料管里面的通道，可以不检查喷头切线回退
        if self.G_ChangeChannelTimeoutNewChan == chan:
            #lancaigang240113：喷头有线材才检测
            if self.G_ToolheadIfHaveFilaFlag == True:
                self.G_ProzenToolhead.dwell(6.0)
                #lancaigang231201：检查切线后是否正常退料，不正常则暂停
                self.Cmds_CutFilaIfNormalCheck()

        #lancaigang240524：用于UIUX动态界面
        self.G_PhrozenFluiddRespondInfo("+B:1,%d" % self.G_ChangeChannelTimeoutNewChan)

    ####################################
    #函数名称：
    #输入参数：
    #返 回 值:
    #功能描述：蓝才刚-20230830
    ####################################
    #P1 D?;线材到停靠位
    def Cmds_P1DnMoveToParkPositonAction(self, chan, gcmd):
        self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_P1DnMoveToParkPositonAction]发送命令: P%d" % chan)
        #lancaigang250619:检查AMS是否重新连接成功
        self.Cmds_USBConnectErrorCheck()
         #lancaigang240524：用于UIUX动态界面
        self.G_PhrozenFluiddRespondInfo("+D:0,%d" % self.G_ChangeChannelTimeoutNewChan)

         #lancaigang241030:
        if chan in range(1, 5):
            self.Cmds_AMSSerial1Send("P%d" % chan)
            self.G_PhrozenFluiddRespondInfo("串口1发送命令：P%d" % chan)
        elif chan in range(5, 9):
            self.Cmds_AMSSerial2Send("P%d" % (chan-4))
            self.G_PhrozenFluiddRespondInfo("串口2发送命令：P%d" % (chan-4))


        #lancaigang240115：如果当前通道不是料管里面的通道，可以不检查喷头切线回退
        if self.G_ChangeChannelTimeoutNewChan == chan:
            #lancaigang240113：喷头有线材才检测
            if self.G_ToolheadIfHaveFilaFlag == True:
                self.G_ProzenToolhead.dwell(6.0)
                #lancaigang231201：检查切线后是否正常退料，不正常则暂停
                self.Cmds_CutFilaIfNormalCheck()

        #lancaigang240524：用于UIUX动态界面
        self.G_PhrozenFluiddRespondInfo("+D:1,%d" % self.G_ChangeChannelTimeoutNewChan)

    ####################################
    #函数名称：
    #输入参数：
    #返 回 值:
    #功能描述：蓝才刚-20230830
    ####################################
    def Cmds_MoveToCutFilaPrepare(self):
        self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_MoveToCutFilaPrepare]切线前准备")

        # self.Cmds_AMSSerial1Send("H%d" % self.G_ChangeChannelTimeoutNewChan)
        # self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_P1CnAutoChangeChannel]切线之前特殊补料状态: H%d" % self.G_ChangeChannelTimeoutNewChan)
        # time.sleep(1)

        # #lancaigang240319：切完后，先吐掉残留喷头的线材，防止切成米粒
        # self.G_PhrozenFluiddRespondInfo("[(cmds.python)]外部宏命令-PG102；切线之前，先吐掉残留喷头的线材，防止切成米粒")
        # self.PG102Flag=True
        # self.G_PhrozenFluiddRespondInfo("[(dev.python)]self.Flag=True")
        # command_string = """
        # PG102
        # """
        # self.G_PhrozenGCode.run_script_from_command(command_string)
        # self.G_PhrozenFluiddRespondInfo("[(cmds.python)]command_string='%s'" % command_string)
        
        # # for i in range(15):
        # #     self.G_PhrozenFluiddRespondInfo("[(dev.python)]吐料中，等待")
        # #     #lancaigang20231013：改为4秒延时
        # #     #lancaigang231115：改为1s
        # #     self.G_ProzenToolhead.dwell(1.0)
        # #     #lancaigang240125：不能用sleep，会阻塞主线程
        # #     #time.sleep(1)
        # self.PG102Flag=False
        # self.G_PhrozenFluiddRespondInfo("[(dev.python)]self.Flag=False")

    ####################################
    #函数名称：
    #输入参数：
    #返 回 值:
    #功能描述：蓝才刚-20230830
    ####################################
    #移动到切线位置
    def Cmds_MoveToCutFilaAction(self, gcmd):
        # // [(cmds.python)Cmds_MoveToCutFilaAction]切线;gcode命令=
        # // G91
        # // G1 Z1.200000 F3000
        # // [(cmds.python)Cmds_MoveToCutFilaAction]切线;gcode命令=
        # // G90
        # // G1 X301.500000 Y0.000000 F24000
        # // G1 X308.500000 F600
        # // G1 X301.500000 F7200
        self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_MoveToCutFilaAction]切线;发送命令")

        #lancaigang240524：用于UIUX动态界面
        self.G_PhrozenFluiddRespondInfo("+Cut:0,%d" % self.G_ChangeChannelTimeoutNewChan)

        # #lancaigang231208：暂停恢复异常，先屏蔽
        # # # 0=切线前默认由内部gcode执行
        # #lancaigang231208：z轴+正数会往上
        # #lancaigang231215：Z轴上升后必须记得下降
        # #if self.G_ChangeChannelIfZLiftingUpByGcode == 0:
        # command_string = """
        #     G91
        #     G1 Z%f F500
        #     """ % (
        #     self.G_AMSFilaCutZPositionLiftingUp,
        # )
        # self.G_PhrozenGCode.run_script_from_command(command_string)
        # #lancaigang231216：如果换料期间点击暂停，刚好换料期间抬升了z轴，到执行暂停时，把z轴高度也保存了，导致整体高度异常
        # self.G_IfZPositionLiftUpFlag = True
        # self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_MoveToCutFilaAction]切线；Z轴上拉升高;gcode命令=%s" % command_string)
        # self.G_ProzenToolhead.wait_moves()
        # self.G_ProzenToolhead.dwell(1.0)



        # self.Cmds_AMSSerial1Send("H%d" % self.G_ChangeChannelTimeoutNewChan)
        # self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_P1CnAutoChangeChannel]切线之前特殊补料状态: H%d" % self.G_ChangeChannelTimeoutNewChan)
        # time.sleep(1)



        #跑到切线X Y位置，快速切线，再返回一些
        # // G91
        # // G1 Z5.000000 F5000
        # // G90
        # // G1 X302.000000 Y244.100000 F5000
        # // G1 X309.000000 F500
        # // G1 X302.000000 F5000
        # // G1 X290 F5000
        command_string = """
            G91
            G1 Z%f F8000
            G90
            G1 X%f Y%f F10000
            G1 X%f Y%f F500
            G4 P500
            G1 X%f Y%f F8000
            G1 X%f F5000
            G91
            G1 Z-%f F8000
            """ % (
            self.G_AMSFilaCutZPositionLiftingUp,
            self.G_AMSFilaCutXPosition-7,
            self.G_AMSFilaCutYPosition,#lancaigang240409：
            self.G_AMSFilaCutXPosition,
            self.G_AMSFilaCutYPosition,
            self.G_AMSFilaCutXPosition-7,
            self.G_AMSFilaCutYPosition,#lancaigang241217：
            self.G_AMSFilaCutXPosition-30,#lancaigang250807:
            self.G_AMSFilaCutZPositionLiftingUp,
        )
        self.G_PhrozenGCode.run_script_from_command(command_string)
        self.G_PhrozenFluiddRespondInfo("Z轴上拉升高并切线;gcode命令=%s" % command_string)
        self.G_ProzenToolhead.wait_moves()

        #self.G_IfZPositionLiftUpFlag = True


        # #lancaigang240110：等待区域等待之前，先执行外部宏命令，移动到特定位置进行等待
        # command_string = """
        #     PG101
        #     """
        # self.G_PhrozenGCode.run_script_from_command(command_string)
        # self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_MoveToCutFilaAction]外部宏命令-到指定位置待吐料；command_string='%s'" % command_string)
        # self.IfDoPG102Flag=True

        #lancaigang240524：用于UIUX动态界面
        self.G_PhrozenFluiddRespondInfo("+Cut:1,%d" % self.G_ChangeChannelTimeoutNewChan)

        # #lancaigang231207：防止切线顶住切刀，往下挤0.5；导致暂停恢复时速度特别慢，屏蔽
        # command = """
        #     G92 E0
        #     G1 E0.5 F300
        #     G92 E0
        # """
        # self.G_PhrozenGCode.run_script_from_command(command)
        # self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_MoveToCutFilaAction]切线;gcode命令=%s" % command)
        # self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_MoveToCutFilaAction]防止切线顶住切刀，往下挤0.5")

    ####################################
    #函数名称：
    #输入参数：
    #返 回 值:
    #功能描述：蓝才刚-20230830
    ####################################
    def Cmds_MoveToCutFilaAbsolutePositionNotReset(self, gcmd):
        self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_MoveToCutFilaAbsolutePositionNotReset]不复位切线，绝对位置;发送命令=%s" % (gcmd.get_commandline()))

        # #lancaigang231208：z轴+正数会往上
        # # command_string = """
        # #     G91
        # #     G1 Z10 F3000
        # #     """
        # # self.G_PhrozenGCode.run_script_from_command(command_string)
        # #lancaigang231215：Z轴上升后必须记得下降
        # command_string = """
        #     G91
        #     G1 Z%f F500
        #     """ % (
        #     self.G_AMSFilaCutZPositionLiftingUp,
        # )
        # self.G_PhrozenGCode.run_script_from_command(command_string)
        # #lancaigang231216：如果换料期间点击暂停，刚好换料期间抬升了z轴，到执行暂停时，把z轴高度也保存了，导致整体高度异常
        # self.G_IfZPositionLiftUpFlag = True
        # self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_MoveToCutFilaAbsolutePositionNotReset]Z轴上升10mm=%s" % command_string)
        # self.G_ProzenToolhead.wait_moves()
        # self.G_ProzenToolhead.dwell(1.0)


        # self.Cmds_AMSSerial1Send("H%d" % self.G_ChangeChannelTimeoutNewChan)
        # self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_P1CnAutoChangeChannel]切线之前特殊补料状态: H%d" % self.G_ChangeChannelTimeoutNewChan)
        # time.sleep(1)

        #lancaigang240524：用于UIUX动态界面
        self.G_PhrozenFluiddRespondInfo("+Cut:0,%d" % self.G_ChangeChannelTimeoutNewChan)

        #跑到切线X Y位置，快速切线，再返回一些
        # // G91
        # // G1 Z5.000000 F5000
        # // G90
        # // G1 X302.000000 Y244.100000 F5000
        # // G1 X309.000000 F500
        # // G1 X302.000000 F5000
        # // G1 X290 F5000
        command_string = """
            G91
            G1 Z%f F8000
            G90
            G1 X%f Y%f F10000
            G1 X%f Y%f F500
            G4 P500
            G1 X%f Y%f F8000
            G1 X%f F5000
            G91
            G1 Z-%f F8000
            """ % (
            self.G_AMSFilaCutZPositionLiftingUp,
            self.G_AMSFilaCutXPosition-7,
            self.G_AMSFilaCutYPosition,#lancaigang240409：
            self.G_AMSFilaCutXPosition,
            self.G_AMSFilaCutYPosition,
            self.G_AMSFilaCutXPosition-7,
            self.G_AMSFilaCutYPosition,#lancaigang241217：
            self.G_AMSFilaCutXPosition-30,#lancaigang250807:
            self.G_AMSFilaCutZPositionLiftingUp,
        )
        self.G_PhrozenGCode.run_script_from_command(command_string)
        self.G_PhrozenFluiddRespondInfo("Z轴上拉升高并切线;gcode命令=%s" % command_string)
        self.G_ProzenToolhead.wait_moves()

        #self.G_IfZPositionLiftUpFlag = True
        
        # #lancaigang240110：等待区域等待之前，先执行外部宏命令，擦嘴
        # command_string = """
        #     PG107
        #     """
        # self.G_PhrozenGCode.run_script_from_command(command_string)
        # self.G_PhrozenFluiddRespondInfo("外部宏命令-擦嘴；command_string='%s'" % command_string)
        # self.IfDoPG102Flag=True

        #lancaigang240524：用于UIUX动态界面
        self.G_PhrozenFluiddRespondInfo("+Cut:1,%d" % self.G_ChangeChannelTimeoutNewChan)

        # #lancaigang231207：防止切线顶住切刀，往下挤0.5；导致暂停恢复时速度特别慢，屏蔽
        # command = """
        #     G92 E0
        #     G1 E0.5 F300
        #     G92 E0
        # """
        # self.G_PhrozenGCode.run_script_from_command(command)
        # self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_MoveToCutFilaAction]切线;gcode命令=%s" % command)
        # self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_MoveToCutFilaAction]防止切线顶住切刀，往下挤0.5")

    ####################################
    #函数名称：
    #输入参数：
    #返 回 值:
    #功能描述：蓝才刚-20230830
    ####################################
    def Cmds_MoveToCutFilaAbsolutePositionNotResetAndRollback(self, gcmd):
        self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_MoveToCutFilaAbsolutePositionNotResetAndRollback]不复位切线，绝对位置;发送命令=%s" % (gcmd.get_commandline()))
        #lancaigang250619:检查AMS是否重新连接成功
        self.Cmds_USBConnectErrorCheck()
        # #lancaigang231208：z轴+正数会往上
        # # command_string = """
        # #     G91
        # #     G1 Z10 F3000
        # #     """
        # # self.G_PhrozenGCode.run_script_from_command(command_string)
        # #lancaigang231215：Z轴上升后必须记得下降
        # command_string = """
        #     G91
        #     G1 Z%f F500
        #     """ % (
        #     self.G_AMSFilaCutZPositionLiftingUp,
        # )
        # self.G_PhrozenGCode.run_script_from_command(command_string)
        # #lancaigang231216：如果换料期间点击暂停，刚好换料期间抬升了z轴，到执行暂停时，把z轴高度也保存了，导致整体高度异常
        # self.G_IfZPositionLiftUpFlag = True
        # self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_MoveToCutFilaAbsolutePositionNotReset]Z轴上升10mm=%s" % command_string)
        # self.G_ProzenToolhead.wait_moves()
        # self.G_ProzenToolhead.dwell(1.0)

        # self.Cmds_AMSSerial1Send("H%d" % self.G_ChangeChannelTimeoutNewChan)
        # self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_P1CnAutoChangeChannel]切线之前特殊补料状态: H%d" % self.G_ChangeChannelTimeoutNewChan)
        # time.sleep(1)

        #lancaigang240524：用于UIUX动态界面
        self.G_PhrozenFluiddRespondInfo("+Cut:0,%d" % self.G_ChangeChannelTimeoutNewChan)

       #跑到切线X Y位置，快速切线，再返回一些
        # // G91
        # // G1 Z5.000000 F5000
        # // G90
        # // G1 X302.000000 Y244.100000 F5000
        # // G1 X309.000000 F500
        # // G1 X302.000000 F5000
        # // G1 X290 F5000
        command_string = """
            G91
            G1 Z%f F8000
            G90
            G1 X%f Y%f F10000
            G1 X%f Y%f F500
            G4 P500
            G1 X%f Y%f F8000
            G1 X%f F5000
            G91
            G1 Z-%f F8000
            """ % (
            self.G_AMSFilaCutZPositionLiftingUp,
            self.G_AMSFilaCutXPosition-7,
            self.G_AMSFilaCutYPosition,#lancaigang240409：
            self.G_AMSFilaCutXPosition,
            self.G_AMSFilaCutYPosition,
            self.G_AMSFilaCutXPosition-7,
            self.G_AMSFilaCutYPosition,#lancaigang241217：
            self.G_AMSFilaCutXPosition-30,#lancaigang250807:
            self.G_AMSFilaCutZPositionLiftingUp,
        )
        self.G_PhrozenGCode.run_script_from_command(command_string)
        self.G_PhrozenFluiddRespondInfo("Z轴上拉升高并切线;gcode命令=%s" % command_string)
        self.G_ProzenToolhead.wait_moves()

        # #self.G_IfZPositionLiftUpFlag = True
        # #lancaigang240110：等待区域等待之前，先执行外部宏命令，擦嘴
        # command_string = """
        #     PG107
        #     """
        # self.G_PhrozenGCode.run_script_from_command(command_string)
        # self.G_PhrozenFluiddRespondInfo("外部宏命令-擦嘴；command_string='%s'" % command_string)
        # self.IfDoPG102Flag=True


        #lancaigang240524：用于UIUX动态界面
        self.G_PhrozenFluiddRespondInfo("+Cut:1,%d" % self.G_ChangeChannelTimeoutNewChan)


        # #lancaigang231207：防止切线顶住切刀，往下挤0.5；导致暂停恢复时速度特别慢，屏蔽
        # command = """
        #     G92 E0
        #     G1 E0.5 F300
        #     G92 E0
        # """
        # self.G_PhrozenGCode.run_script_from_command(command)
        # self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_MoveToCutFilaAction]切线;gcode命令=%s" % command)
        # self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_MoveToCutFilaAction]防止切线顶住切刀，往下挤0.5")


        #lancaigang241031:
        if self.G_SerialPort1OpenFlag == True:
            self.G_PhrozenFluiddRespondInfo("串口1发送命令: AP，全部后退到停靠位")
            #// 全部后退到停靠位；//===== P2 A1 所有线料退到停靠位待打印 Yes；"AP"；
            self.Cmds_AMSSerial1Send("AP")
        #lancaigang241030:
        if self.G_SerialPort2OpenFlag == True:
            self.G_PhrozenFluiddRespondInfo("串口2发送命令: AP，全部后退到停靠位")
            #// 全部后退到停靠位；//===== P2 A1 所有线料退到停靠位待打印 Yes；"AP"；
            self.Cmds_AMSSerial2Send("AP")

        #lancaigang240913：把延時放到外面
        self.G_ProzenToolhead.dwell(6.0)
        #lancaigang231201：检查切线后是否正常退料，不正常则暂停
        self.Cmds_CutFilaIfNormalCheck()

    ####################################
    #函数名称：
    #输入参数：
    #返 回 值:
    #功能描述：蓝才刚-20230830
    ####################################
    def Cmds_MoveToCutFilaAndNotRollback(self, gcmd):
        self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_MoveToCutFilaAndNotRollback]切线;发送命令=%s" % (gcmd.get_commandline()))
        #lancaigang240524：用于UIUX动态界面
        self.G_PhrozenFluiddRespondInfo("+Zero:0,%d" % self.G_ChangeChannelTimeoutNewChan)
        #lancaigang20231019：打印机异常断电，自动换料如果发现第1个通道喷头残留上次线材，需要切料并退回所有线材
        #lancaigang20231020：先不检测喷头有料
        #if self.G_ToolheadIfHaveFilaFlag:
        # 0=切线前默认由内部gcode执行
        #lancaigang231128：G28改为PG28
        #if self.G_ChangeChannelIfZLiftingUpByGcode == 0:
        self.G_PhrozenFluiddRespondInfo("全部归位并切线")
        command_string = """
        G28
        """
        self.G_PhrozenGCode.run_script_from_command(command_string)
        self.G_PhrozenFluiddRespondInfo("复位=%s" % command_string)
        #lancaigang20231020：挤出头回抽gcode，回抽前需要升温喷头，时间比较久，这里不处理，自动换料才升温并切线
        # G92 E0
        # G1 E0.0000 F600
        # G91
        # G1 E-0.385 F8000
        #lancaigang240524：用于UIUX动态界面
        self.G_PhrozenFluiddRespondInfo("+Zero:1,%d" % self.G_ChangeChannelTimeoutNewChan)

        self.G_PhrozenFluiddRespondInfo("切线")


        #lancaigang20231013：切线
        self.Cmds_MoveToCutFilaAction(gcmd)

####################################
    #函数名称：
    #输入参数：
    #返 回 值:
    #功能描述：蓝才刚-20230830
    ####################################
    def Cmds_MoveToCutFilaAndHomingXY(self, gcmd):
        self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_MoveToCutFilaAndHomingXY]切线;XY复位")
        #lancaigang240524：用于UIUX动态界面
        self.G_PhrozenFluiddRespondInfo("+Zero:0,%d" % self.G_ChangeChannelTimeoutNewChan)
        #lancaigang20231019：打印机异常断电，自动换料如果发现第1个通道喷头残留上次线材，需要切料并退回所有线材
        #lancaigang20231020：先不检测喷头有料
        #if self.G_ToolheadIfHaveFilaFlag:
        # 0=切线前默认由内部gcode执行
        #lancaigang231128：G28改为PG28
        #if self.G_ChangeChannelIfZLiftingUpByGcode == 0:
        self.G_PhrozenFluiddRespondInfo("G28归位Y并切线")
        command_string = """
        G28 Y0
        """
        self.G_PhrozenGCode.run_script_from_command(command_string)
        self.G_PhrozenFluiddRespondInfo("Y0复位=%s" % command_string)
        self.G_PhrozenFluiddRespondInfo("G28归位X并切线")
        command_string = """
        G28 X0
        """
        self.G_PhrozenGCode.run_script_from_command(command_string)
        self.G_PhrozenFluiddRespondInfo("X0复位=%s" % command_string)
        #lancaigang20231020：挤出头回抽gcode，回抽前需要升温喷头，时间比较久，这里不处理，自动换料才升温并切线
        # G92 E0
        # G1 E0.0000 F600
        # G91
        # G1 E-0.385 F8000
        #lancaigang240524：用于UIUX动态界面
        self.G_PhrozenFluiddRespondInfo("+Zero:1,%d" % self.G_ChangeChannelTimeoutNewChan)

        self.G_PhrozenFluiddRespondInfo("切线")


        #lancaigang20231013：切线
        self.Cmds_MoveToCutFilaAction(gcmd)


    ####################################
    #函数名称：
    #输入参数：
    #返 回 值:
    #功能描述：蓝才刚-20230830
    ####################################
    def Cmds_MoveToCutFilaAndRollback(self, gcmd):
        number=50;
        self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_MoveToCutFilaAndRollback]切线;发送命令")

        #lancaigang250619:检查AMS是否重新连接成功
        self.Cmds_USBConnectErrorCheck()

        #lancaigang20231019：打印机异常断电，自动换料如果发现第1个通道喷头残留上次线材，需要切料并退回所有线材
        #lancaigang20231020：先不检测喷头有料
        #if self.G_ToolheadIfHaveFilaFlag:
        # # 0=切线前默认由内部gcode执行
        #lancaigang231128：G28改为PG28
        #lancaigang240319：GCODE里面有PG28，这里不用PG28了
        #lancaigang240323：第一层掉落残料，先屏蔽
        # if self.G_ChangeChannelIfZLiftingUpByGcode == 0:
        #     self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_MoveToCutFilaAndRollback]全部归位并切线")
        #     command_string = """
        #     PG28
        #     """
        #     self.G_PhrozenGCode.run_script_from_command(command_string)
        #     #lancaigang20231020：挤出头回抽gcode，回抽前需要升温喷头，时间比较久，这里不处理，自动换料才升温并切线
        #     # G92 E0
        #     # G1 E0.0000 F600
        #     # G91
        #     # G1 E-0.385 F8000

        self.G_PhrozenFluiddRespondInfo("切线")
        #lancaigang20231013：切线
        self.Cmds_MoveToCutFilaAction(gcmd)


        self.G_ProzenToolhead.dwell(2.0)


        #lancaigang241031:
        if self.G_SerialPort1OpenFlag == True:
            self.G_PhrozenFluiddRespondInfo("串口1发送命令: AP，全部后退到停靠位")
            #// 全部后退到停靠位；//===== P2 A1 所有线料退到停靠位待打印 Yes；"AP"；
            self.Cmds_AMSSerial1Send("AP")
        #lancaigang241030:
        if self.G_SerialPort2OpenFlag == True:
            self.G_PhrozenFluiddRespondInfo("串口2发送命令: AP，全部后退到停靠位")
            #// 全部后退到停靠位；//===== P2 A1 所有线料退到停靠位待打印 Yes；"AP"；
            self.Cmds_AMSSerial2Send("AP")




        #lancaigang240913：把延時放到外面
        self.G_ProzenToolhead.dwell(6.0)
        #lancaigang231201：检查切线后是否正常退料，不正常则暂停
        self.Cmds_CutFilaIfNormalCheck()



        # if self.G_ToolheadIfHaveFilaFlag:
        #     for i in range(number):
        #             time.sleep(1)
        #             i += 1
        #             self.G_PhrozenFluiddRespondInfo('喷头中有线，AP命令退线中;i=%d' % i)

        #             if i >= number:
        #                 self.G_PhrozenFluiddRespondInfo('AP命令超时;number=%d' % number)
        #                 break

    

    
    
    

    ####################################
    #函数名称：
    #输入参数：
    #返 回 值:
    #功能描述：蓝才刚-20230830
    ####################################
    def Cmds_PhrozenKlipperPauseCommon(self):
        self.G_PhrozenFluiddRespondInfo("=====[(cmds.python)Cmds_PhrozenKlipperPauseCommon]klipper暂停")
        self.G_PhrozenFluiddRespondInfo("=====PAUSE=====")
        self.G_PhrozenFluiddRespondInfo("=====PAUSE=====self.G_ChangeChannelTimeoutOldChan=%d" % self.G_ChangeChannelTimeoutOldChan)
        self.G_PhrozenFluiddRespondInfo("=====PAUSE=====self.G_ChangeChannelTimeoutNewChan=%d" % self.G_ChangeChannelTimeoutNewChan)

        # #cancel取消命令
        # self.G_PhrozenPrinterCancelPauseResume.cmd_CANCEL_PRINT(None)
        #lancaigang250517：
        Lo_PauseStatus=self.G_PhrozenPrinterCancelPauseResume.get_status(None)
        self.G_PhrozenFluiddRespondInfo("当前暂停状态-Lo_PauseStatus='%s'" % Lo_PauseStatus)

        #lancaigang250526：暂停中，不允许新的gcode命令，需等待暂停完成
        self.G_KlipperInPausing = True
        self.G_PhrozenFluiddRespondInfo("暂停中，不允许新的gcode命令，需等待暂停完成")

        #lancaigang240229:
        if self.IfDoPG102Flag==True:
            self.G_PhrozenFluiddRespondInfo("self.IfDoPG102Flag==True")
            self.IfDoPG102Flag=False

            # self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_PhrozenKlipperPauseCommon]外部宏命令-PG104")
            # command_string = """
            # PG104
            # """
            # self.G_PhrozenGCode.run_script_from_command(command_string)
            # self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_PhrozenKlipperPauseCommon]外部宏命令-排废料；command_string='%s'" % command_string)
            # command = """
            #     G91
            #     G1 Z5 F5000
            #     G90
            #     G1 X240 Y280 F8000
            #     G91
            #     G1 Z-5 F5000
            #     G90
            # """
            # self.G_PhrozenGCode.run_script_from_command(command)
            # self.G_PhrozenFluiddRespondInfo("[(cmds.python)]command=%s" % (command))


        #lancaigang241030：只有在打印状态下才能暂停
        if self.G_AMSDeviceWorkMode == AMS_WORK_MODE_UNKNOW:#0
            self.G_PhrozenFluiddRespondInfo("不在打印模式，不执行暂停PAUSE宏命令")
        else:
            Lo_PauseStatus=self.G_PhrozenPrinterCancelPauseResume.get_status(None)
            self.G_PhrozenFluiddRespondInfo("当前暂停状态-Lo_PauseStatus='%s'" % Lo_PauseStatus)
            self.G_PhrozenFluiddRespondInfo("Lo_PauseStatus['is_paused']='%s'" % Lo_PauseStatus['is_paused'])
            #// 当前暂停状态-Lo_PauseStatus='{'is_paused': True}'
            if Lo_PauseStatus['is_paused'] == True:
                self.G_PhrozenFluiddRespondInfo("已是暂停状态")
            else:
                self.G_PhrozenFluiddRespondInfo("未暂停状态")

                # #lancaigang250527：暂停待料区
                # self.G_PhrozenFluiddRespondInfo("开始调用外部宏命令-PRZ_PAUSE_WAITINGAREA")
                # command = """
                # PRZ_PAUSE_WAITINGAREA
                # """
                # self.G_PhrozenGCode.run_script_from_command(command)
                # self.G_PhrozenFluiddRespondInfo("结束调用外部宏命令:command=%s" % (command))

                #lancaigang250527：暂停快速执行
                if self.G_KlipperQuickPause == True:
                    self.G_KlipperQuickPause = False

                    
                    self.G_PhrozenFluiddRespondInfo("开始调用外部宏命令-PRZ_PAUSE_WAITINGAREA")
                    command = """
                    PRZ_PAUSE_WAITINGAREA
                    """
                    self.G_PhrozenGCode.run_script_from_command(command)

                    #lancaigang240119：暂停改用cfg配置表宏命令
                    self.G_PhrozenFluiddRespondInfo("开始调用外部宏命令-PAUSE_PRINTING")
                    command = """
                    PAUSE_PRINTING
                    """
                    self.G_PhrozenGCode.run_script_from_command(command)
                    self.G_PhrozenFluiddRespondInfo("self.G_ProzenToolhead.wait_moves()")
                    self.G_ProzenToolhead.wait_moves()
                    self.G_PhrozenFluiddRespondInfo("结束调用外部宏命令:command=%s" % (command))
                    #self.G_PhrozenFluiddRespondInfo("防止暂停不住，多加命令；send_pause_command")
                    #self.G_PhrozenPrinterCancelPauseResume.send_pause_command()
                else:
                    self.G_KlipperQuickPause = False

                    # #lancaigang250716：都需要先到暂停区
                    # self.G_PhrozenFluiddRespondInfo("开始调用外部宏命令-PRZ_PAUSE_WAITINGAREA")
                    # command = """
                    # PRZ_PAUSE_WAITINGAREA
                    # """
                    # self.G_PhrozenGCode.run_script_from_command(command)

                    #lancaigang240119：暂停改用cfg配置表宏命令
                    self.G_PhrozenFluiddRespondInfo("开始调用外部宏命令-PAUSE")
                    command = """
                    PAUSE
                    """
                    self.G_PhrozenGCode.run_script_from_command(command)
                    self.G_PhrozenFluiddRespondInfo("self.G_ProzenToolhead.wait_moves()")
                    self.G_ProzenToolhead.wait_moves()
                    self.G_PhrozenFluiddRespondInfo("结束调用外部宏命令:command=%s" % (command))
                    #self.G_PhrozenFluiddRespondInfo("防止暂停不住，多加命令；send_pause_command")
                    #self.G_PhrozenPrinterCancelPauseResume.send_pause_command()

                # #lancaigang250527：暂停待料区
                # self.G_PhrozenFluiddRespondInfo("开始调用外部宏命令-PRZ_PAUSE_WAITINGAREA")
                # command = """
                # PRZ_PAUSE_WAITINGAREA
                # """
                # self.G_PhrozenGCode.run_script_from_command(command)
                # self.G_PhrozenFluiddRespondInfo("结束调用外部宏命令:command=%s" % (command))

                #lancaigang240125：暂停了，就不允许stm23主动上报再次暂停
                self.STM32ReprotPauseFlag=1
                self.G_PhrozenFluiddRespondInfo("self.STM32ReprotPauseFlag=1")

                self.G_KlipperIfPaused = True
                self.G_PhrozenFluiddRespondInfo("self.G_KlipperIfPaused = True")
                self.G_PhrozenFluiddRespondInfo("klipper暂停；")




        #lancaigang240325：换料失败，不能执行恢复
        self.G_MCModeCanResumeFlag = False

        # #cancel取消命令
        # self.G_PhrozenPrinterCancelPauseResume.cmd_CANCEL_PRINT(None)
        #lancaigang250517：
        Lo_PauseStatus=self.G_PhrozenPrinterCancelPauseResume.get_status(None)
        self.G_PhrozenFluiddRespondInfo("当前暂停状态-Lo_PauseStatus='%s'" % Lo_PauseStatus)

         #lancaigang250526：
        self.G_KlipperInPausing = False
        self.G_PhrozenFluiddRespondInfo("暂停完成，允许新的gcode命令")


        #lancaigang250607：打印状态；1-退料中；2-进料中；3-打印中；4-暂停
        self.G_KlipperPrintStatus= 4

        # # #移动到前面方便客户操作
        # # command = """
        # #     G90
        # #     G1 X150 Y10 F5400
        # # """
        # # self.G_PhrozenGCode.run_script_from_command(command)
        # # self.G_PhrozenFluiddRespondInfo("[(cmds.python)]command=%s" % (command))
        # # #每个gcode命令之后都要加一下wait_moves函数
        # # #lancaigang231202：wait_moves可能导致klipper无法暂停
        # # #lancaigang231207：不能用wait_moves，否则导致保存的gcode命令异常
        # # self.G_ProzenToolhead.wait_moves()
        # # self.G_PhrozenFluiddRespondInfo("[(cmds.python)]移动到前面方便客户操作")
        # #self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_MoveToCutFilaAction]切线;gcode命令=%s" % command)
        # #klipper暂停命令；保存当前的x y z坐标
        # #lancaigang240108：要考虑多次暂停保存的数据是否正常，后续要验证
        # self.G_PhrozenGCode.run_script_from_command("SAVE_GCODE_STATE NAME=PRZ_PAUSE_STATE")
        # self.G_PhrozenFluiddRespondInfo("[(cmds.python)]SAVE_GCODE_STATE")
        # self.G_PhrozenPrinterCancelPauseResume.send_pause_command()
        # #self.G_ProzenToolhead.wait_moves()
        # self.G_ProzenToolhead.dwell(1.0)

        # #time.sleep(1)
        # #self.G_ProzenToolhead.wait_moves()
        # #self.G_PhrozenFluiddRespondInfo("[(cmds.python)]wait_moves")
        # #lancaigang231219：不确定是不是暂停移动导致klipper异常崩溃
        # #lancaigang230103：暂停有时候停不住
        # #移动到前面方便客户操作
        # # G91
        # # G1 Z10 F7000
        # # G90
        # command = """
        # G91
        # G1 X150 Y10 F6000
        # G90
        # """
        # self.G_PhrozenGCode.run_script_from_command(command)
        # self.G_PhrozenFluiddRespondInfo("[(cmds.python)]command=%s" % (command))
        # self.G_ProzenToolhead.dwell(1.0)

    ####################################
    #函数名称：
    #输入参数：
    #返 回 值:
    #功能描述：蓝才刚-20230830
    ####################################
    def Cmds_PhrozenKlipperPauseM2M3ToSTM32(self, gcmd):
        _ = gcmd

        #lancaigang231115：一定要先判断gcmd命令是否为空，否则会导致klipper异常关掉
        if gcmd is None:
            self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_PhrozenKlipperPauseM2M3ToSTM32]self.G_PhrozenFluiddRespondInfo;gcmd对象为空")
            self.G_PhrozenFluiddRespondInfo("self.G_PhrozenFluiddRespondInfo;klipper暂停")
            #pass
        if gcmd is not None:
            self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_PhrozenKlipperPauseM2M3ToSTM32]命令='%s'" % (gcmd.get_commandline(),))
            self.G_PhrozenFluiddRespondInfo("klipper暂停")
            #pass
        #self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_PhrozenKlipperPauseM2M3ToSTM32]命令='%s'" % (gcmd.get_commandline(),))

        #lancaigang250619:检查AMS是否重新连接成功
        self.Cmds_USBConnectErrorCheck()

        #lancaigang250526：暂停中，不允许新的gcode命令，需等待暂停完成
        self.G_KlipperInPausing = True
        self.G_PhrozenFluiddRespondInfo("暂停中，不允许新的gcode命令，需等待暂停完成")

        #lancaigang231129：暂停时喷头移动到指定位置
        # self.G_PhrozenGCode.run_script_from_command("SAVE_GCODE_STATE NAME=PRZ_PAUSE_STATE")
        # self.G_KlipperIfPaused = True
        # #喷头等待移动
        #lancaigang231202：wait_moves可能导致klipper无法暂停
        #lancaigang231207：不能用wait_moves，否则导致保存的gcode命令异常
        # self.G_ProzenToolhead.wait_moves()


        #time.sleep(1)
        #lancaigang231201：klipper暂停时，暂停stm32电机
        #// AT+PAUSE
        #// AT+PAUSE=8
        #// AT+PAUSE=9


        #lancaigang241031:
        if self.G_SerialPort1OpenFlag == True:
            self.Cmds_AMSSerial1Send("AT+PAUSE")
            self.G_PhrozenFluiddRespondInfo("串口1发送AT+PAUSE暂停stm32电机")
        #lancaigang241030:
        if self.G_SerialPort2OpenFlag == True:
            self.Cmds_AMSSerial2Send("AT+PAUSE")
            self.G_PhrozenFluiddRespondInfo("串口2发送AT+PAUSE暂停stm32电机")


        #lancaigang240125：封装函数
        self.Cmds_PhrozenKlipperPauseCommon()

     
        self.G_KlipperIfPaused = True
        self.G_PhrozenFluiddRespondInfo("self.G_KlipperIfPaused = True")
        self.G_PhrozenFluiddRespondInfo("klipper暂停；")

        #lancaigang250526：
        self.G_KlipperInPausing = False
        self.G_PhrozenFluiddRespondInfo("暂停完成，允许新的gcode命令")

    ####################################
    #函数名称：
    #输入参数：
    #返 回 值:
    #功能描述：蓝才刚-20230830
    ####################################
    def Cmds_PhrozenKlipperPauseMAToSTM32(self, gcmd):
        _ = gcmd

        #lancaigang231115：一定要先判断gcmd命令是否为空，否则会导致klipper异常关掉
        if gcmd is None:
            self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_PhrozenKlipperPauseMAToSTM32]self.G_PhrozenFluiddRespondInfo;gcmd对象为空")
            self.G_PhrozenFluiddRespondInfo("self.G_PhrozenFluiddRespondInfo;klipper暂停")
            #pass
        if gcmd is not None:
            self.G_PhrozenFluiddRespondInfo("命令='%s'" % (gcmd.get_commandline(),))
            self.G_PhrozenFluiddRespondInfo("klipper暂停")
            #pass
        #self.G_PhrozenFluiddRespondInfo("命令='%s'" % (gcmd.get_commandline(),))

        #lancaigang250526：暂停中，不允许新的gcode命令，需等待暂停完成
        self.G_KlipperInPausing = True
        self.G_PhrozenFluiddRespondInfo("暂停中，不允许新的gcode命令，需等待暂停完成")


        #time.sleep(1)

        # #lancaigang241031:
        # if self.G_SerialPort1OpenFlag == True:
        #     self.Cmds_AMSSerial1Send("AT+PAUSE")
        #     self.G_PhrozenFluiddRespondInfo("串口1发送AT+PAUSE暂停stm32电机")
        # #lancaigang241030:
        # if self.G_SerialPort2OpenFlag == True:
        #     self.Cmds_AMSSerial2Send("AT+PAUSE")
        #     self.G_PhrozenFluiddRespondInfo("串口2发送AT+PAUSE暂停stm32电机")

        #lancaigang240229:
        if self.IfDoPG102Flag==True:
            self.G_PhrozenFluiddRespondInfo("self.IfDoPG102Flag==True")
            self.IfDoPG102Flag=False

        Lo_PauseStatus=self.G_PhrozenPrinterCancelPauseResume.get_status(None)
        self.G_PhrozenFluiddRespondInfo("当前暂停状态-Lo_PauseStatus='%s'" % Lo_PauseStatus)
        self.G_PhrozenFluiddRespondInfo("Lo_PauseStatus['is_paused']='%s'" % Lo_PauseStatus['is_paused'])
        #// 当前暂停状态-Lo_PauseStatus='{'is_paused': True}'
        if Lo_PauseStatus['is_paused'] == True:
            self.G_PhrozenFluiddRespondInfo("已是暂停状态")
        else:
            self.G_PhrozenFluiddRespondInfo("未暂停状态")

        #lancaigang241030：只有在打印状态下才能暂停
        if self.G_AMSDeviceWorkMode == AMS_WORK_MODE_UNKNOW:#0
            self.G_PhrozenFluiddRespondInfo("不在打印模式，不执行暂停PAUSE宏命令")
        else:
 
            #lancaigang240119：暂停改用cfg配置表宏命令
            self.G_PhrozenFluiddRespondInfo("开始调用外部宏命令-PAUSEMA")
            command = """
            PAUSEMA
            """
            self.G_PhrozenGCode.run_script_from_command(command)
            self.G_PhrozenFluiddRespondInfo("调用宏命令:command=%s" % (command))
            #self.G_PhrozenFluiddRespondInfo("防止暂停不住，多加命令；send_pause_command")
            #self.G_PhrozenPrinterCancelPauseResume.send_pause_command()
            self.G_PhrozenFluiddRespondInfo("结束调用外部宏命令-PAUSEMA")

            #lancaigang240125：暂停了，就不允许stm23主动上报再次暂停
            self.STM32ReprotPauseFlag=1
            self.G_PhrozenFluiddRespondInfo("self.STM32ReprotPauseFlag=1")
            self.G_KlipperIfPaused = True
            self.G_PhrozenFluiddRespondInfo("self.G_KlipperIfPaused = True")
            self.G_PhrozenFluiddRespondInfo("klipper暂停；")


        Lo_PauseStatus=self.G_PhrozenPrinterCancelPauseResume.get_status(None)
        self.G_PhrozenFluiddRespondInfo("当前暂停状态-Lo_PauseStatus='%s'" % Lo_PauseStatus)
        self.G_PhrozenFluiddRespondInfo("Lo_PauseStatus['is_paused']='%s'" % Lo_PauseStatus['is_paused'])
        #// 当前暂停状态-Lo_PauseStatus='{'is_paused': True}'
        if Lo_PauseStatus['is_paused'] == True:
            self.G_PhrozenFluiddRespondInfo("已是暂停状态")
        else:
            self.G_PhrozenFluiddRespondInfo("未暂停状态")


        #lancaigang240325：换料失败，不能执行恢复
        self.G_MCModeCanResumeFlag = False

        self.G_PhrozenFluiddRespondInfo("=====self.G_ChangeChannelTimeoutOldChan=%d" % self.G_ChangeChannelTimeoutOldChan)
        self.G_PhrozenFluiddRespondInfo("=====self.G_ChangeChannelTimeoutNewChan=%d" % self.G_ChangeChannelTimeoutNewChan)

        #lancaigang250526：
        self.G_KlipperInPausing = False
        self.G_PhrozenFluiddRespondInfo("暂停完成，允许新的gcode命令")
    

    ####################################
    #函数名称：
    #输入参数：
    #返 回 值:
    #功能描述：蓝才刚-20230830
    ####################################
    def Cmds_PhrozenKlipperPauseM2M3NoneCmdToSTM32(self, gcmd):
        _ = gcmd

        #lancaigang231115：一定要先判断gcmd命令是否为空，否则会导致klipper异常关掉
        if gcmd is None:
            self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_PhrozenKlipperPauseM2M3NoneCmdToSTM32]self.G_PhrozenFluiddRespondInfo;gcmd对象为空")
            self.G_PhrozenFluiddRespondInfo("self.G_PhrozenFluiddRespondInfo;klipper暂停")
            #pass
        if gcmd is not None:
            self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_PhrozenKlipperPauseM2M3NoneCmdToSTM32]命令='%s'" % (gcmd.get_commandline(),))
            self.G_PhrozenFluiddRespondInfo("klipper暂停")
            #pass
        #self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_PhrozenKlipperPauseM2M3NoneCmdToSTM32]命令='%s'" % (gcmd.get_commandline(),))


        #lancaigang231129：暂停时喷头移动到指定位置
        # self.G_PhrozenGCode.run_script_from_command("SAVE_GCODE_STATE NAME=PRZ_PAUSE_STATE")
        # self.G_KlipperIfPaused = True
        # #喷头等待移动
        #lancaigang231202：wait_moves可能导致klipper无法暂停
        #lancaigang231207：不能用wait_moves，否则导致保存的gcode命令异常
        # self.G_ProzenToolhead.wait_moves()

        #lancaigang250526：暂停中，不允许新的gcode命令，需等待暂停完成
        self.G_KlipperInPausing = True
        self.G_PhrozenFluiddRespondInfo("暂停中，不允许新的gcode命令，需等待暂停完成")


        #lancaigang240125：封装函数
        self.Cmds_PhrozenKlipperPauseCommon()


        self.G_KlipperIfPaused = True
        self.G_PhrozenFluiddRespondInfo("self.G_KlipperIfPaused = True")
        self.G_PhrozenFluiddRespondInfo("klipper暂停；")

        #lancaigang250526：
        self.G_KlipperInPausing = False
        self.G_PhrozenFluiddRespondInfo("暂停完成，允许新的gcode命令")

    ####################################
    #函数名称：
    #输入参数：
    #返 回 值:
    #功能描述：蓝才刚-20230830
    ####################################
    # PRZ_PAUSE暂停打印(该命令暂停动作并非系统自带暂停,一般在换线时使用)
    # AT+PAUSE
    def Cmds_PhrozenKlipperPauseNoneCmdToSTM32(self, gcmd):
        _ = gcmd

        #lancaigang231130：屏蔽，每次暂停都执行以下
        # if self.G_KlipperIfPaused == True:
        #     self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_PhrozenKlipperPauseNoneCmdToSTM32]已处在klipper暂停状态")
        #     return


        #lancaigang231115：一定要先判断gcmd命令是否为空，否则会导致klipper异常关掉
        if gcmd is None:
            self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_PhrozenKlipperPauseNoneCmdToSTM32]self.G_PhrozenFluiddRespondInfo;gcmd对象为空")
            self.G_PhrozenFluiddRespondInfo("self.G_PhrozenFluiddRespondInfo;klipper暂停")
            #pass
        if gcmd is not None:
            self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_PhrozenKlipperPauseNoneCmdToSTM32]命令='%s'" % (gcmd.get_commandline(),))
            self.G_PhrozenFluiddRespondInfo("klipper暂停")
            #pass
        #self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_PhrozenKlipperPauseNoneCmdToSTM32]命令='%s'" % (gcmd.get_commandline(),))


        #lancaigang231129：暂停时喷头移动到指定位置
        # self.G_PhrozenGCode.run_script_from_command("SAVE_GCODE_STATE NAME=PRZ_PAUSE_STATE")
        # self.G_KlipperIfPaused = True
        # #喷头等待移动
        #lancaigang231202：wait_moves可能导致klipper无法暂停
        #lancaigang231207：不能用wait_moves，否则导致保存的gcode命令异常
        # self.G_ProzenToolhead.wait_moves()

        #lancaigang250526：暂停中，不允许新的gcode命令，需等待暂停完成
        self.G_KlipperInPausing = True
        self.G_PhrozenFluiddRespondInfo("暂停中，不允许新的gcode命令，需等待暂停完成")


        #lancaigang240125：封装函数
        self.Cmds_PhrozenKlipperPauseCommon()


        self.G_KlipperIfPaused = True
        self.G_PhrozenFluiddRespondInfo("self.G_KlipperIfPaused = True")
        self.G_PhrozenFluiddRespondInfo("klipper暂停；")

        #lancaigang250526：
        self.G_KlipperInPausing = False
        self.G_PhrozenFluiddRespondInfo("暂停完成，允许新的gcode命令")



    ####################################
    #函数名称：
    #输入参数：
    #返 回 值:
    #功能描述：蓝才刚-20230830
    ####################################
    def Cmds_PhrozenKlipperPauseToolheadCutFailsure(self, gcmd):
        _ = gcmd

        #lancaigang231115：一定要先判断gcmd命令是否为空，否则会导致klipper异常关掉
        if gcmd is None:
            self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_PhrozenKlipperPauseToolheadCutFailsure]self.G_PhrozenFluiddRespondInfo;gcmd对象为空")
            self.G_PhrozenFluiddRespondInfo("self.G_PhrozenFluiddRespondInfo;klipper暂停")
            #pass
        if gcmd is not None:
            self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_PhrozenKlipperPauseToolheadCutFailsure]命令='%s'" % (gcmd.get_commandline(),))
            self.G_PhrozenFluiddRespondInfo("klipper暂停")
            #pass
        #self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_PhrozenKlipperPauseToolheadCutFailsure]命令='%s'" % (gcmd.get_commandline(),))
        

        #lancaigang231129：暂停时喷头移动到指定位置
        # self.G_PhrozenGCode.run_script_from_command("SAVE_GCODE_STATE NAME=PRZ_PAUSE_STATE")
        # self.G_KlipperIfPaused = True
        # #喷头等待移动
        #lancaigang231207：不能用wait_moves，否则导致保存的gcode命令异常
        # self.G_ProzenToolhead.wait_moves()


        #lancaigang250526：暂停中，不允许新的gcode命令，需等待暂停完成
        self.G_KlipperInPausing = True
        self.G_PhrozenFluiddRespondInfo("暂停中，不允许新的gcode命令，需等待暂停完成")


        #lancaigang240125：封装函数
        self.Cmds_PhrozenKlipperPauseCommon()

        self.G_KlipperIfPaused = True
        self.G_PhrozenFluiddRespondInfo("self.G_KlipperIfPaused = True")
        self.G_PhrozenFluiddRespondInfo("klipper暂停；")

        #lancaigang250526：
        self.G_KlipperInPausing = False
        self.G_PhrozenFluiddRespondInfo("暂停完成，允许新的gcode命令")


    ####################################
    #函数名称：
    #输入参数：
    #返 回 值:
    #功能描述：蓝才刚-20230830
    ####################################
    def Cmds_PhrozenKlipperPauseChangeChannelTimeout(self, gcmd):
        _ = gcmd


        #lancaigang231115：一定要先判断gcmd命令是否为空，否则会导致klipper异常关掉
        if gcmd is None:
            self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_PhrozenKlipperPauseChangeChannelTimeout]self.G_PhrozenFluiddRespondInfo;gcmd对象为空")
            self.G_PhrozenFluiddRespondInfo("self.G_PhrozenFluiddRespondInfo;klipper暂停")
            #pass
        if gcmd is not None:
            self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_PhrozenKlipperPauseChangeChannelTimeout]命令='%s'" % (gcmd.get_commandline(),))
            self.G_PhrozenFluiddRespondInfo("klipper暂停")
            #pass
        #self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_PhrozenKlipperPauseChangeChannelTimeout]命令='%s'" % (gcmd.get_commandline(),))
        

        #lancaigang231129：暂停时喷头移动到指定位置
        # self.G_PhrozenGCode.run_script_from_command("SAVE_GCODE_STATE NAME=PRZ_PAUSE_STATE")
        # self.G_KlipperIfPaused = True
        # #喷头等待移动
        #lancaigang231207：不能用wait_moves，否则导致保存的gcode命令异常
        # self.G_ProzenToolhead.wait_moves()


        #lancaigang250526：暂停中，不允许新的gcode命令，需等待暂停完成
        self.G_KlipperInPausing = True
        self.G_PhrozenFluiddRespondInfo("暂停中，不允许新的gcode命令，需等待暂停完成")


        #lancaigang240125：封装函数
        self.Cmds_PhrozenKlipperPauseCommon()

        self.G_KlipperIfPaused = True
        self.G_PhrozenFluiddRespondInfo("self.G_KlipperIfPaused = True")
        self.G_PhrozenFluiddRespondInfo("klipper暂停；")

        #lancaigang250526：
        self.G_KlipperInPausing = False
        self.G_PhrozenFluiddRespondInfo("暂停完成，允许新的gcode命令")


    ####################################
    #函数名称：
    #输入参数：
    #返 回 值:
    #功能描述：蓝才刚-20230830
    ####################################
    # PRZ_PAUSE暂停打印(该命令暂停动作并非系统自带暂停,一般在换线时使用)
    # AT+PAUSE
    def Cmds_PhrozenKlipperPause(self, gcmd):
        _ = gcmd
        self.G_PhrozenFluiddRespondInfo("=====[(cmds.python)Cmds_PhrozenKlipperPause]klipper暂停")
        #lancaigang231130：屏蔽，每次暂停都执行以下
        # if self.G_KlipperIfPaused == True:
        #     self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_PhrozenKlipperPause]已处在klipper暂停状态")
        #     return

        # if self.G_ChangeChannelResumeFlag:
        #     self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_PhrozenKlipperPause]正在恢复上次动作，不允许暂停了")
        #     return


        # #lancaigang231216：
        # eventtime = self.G_PhrozenReactor.monotonic()
        # # Determine "printing" status
        # idle_timeout = self.G_PhrozenPrinter.lookup_object("idle_timeout")
        # is_printing = idle_timeout.get_status(eventtime)["state"] == "Printing"
        # if is_printing:
        #     self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_PhrozenKlipperPause]正在打印中；命令='%s'" % (gcmd.get_commandline(),))
        # else:
        #     self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_PhrozenKlipperPause]未在打印中；命令='%s；return'" % (gcmd.get_commandline(),))
        #     return


        #lancaigang231115：一定要先判断gcmd命令是否为空，否则会导致klipper异常关掉
        if gcmd is None:
            self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_PhrozenKlipperPause]self.G_PhrozenFluiddRespondInfo;gcmd对象为空")
            self.G_PhrozenFluiddRespondInfo("self.G_PhrozenFluiddRespondInfo;klipper暂停")
            #pass
        if gcmd is not None:
            self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_PhrozenKlipperPause]命令='%s'" % (gcmd.get_commandline(),))
            self.G_PhrozenFluiddRespondInfo("klipper暂停")
            #pass
        #self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_PhrozenKlipperPause]命令='%s'" % (gcmd.get_commandline(),))
        
        self.G_PhrozenFluiddRespondInfo("当前模式")
        if self.G_AMSDeviceWorkMode == AMS_WORK_MODE_UNKNOW:
            self.G_PhrozenFluiddRespondInfo("+Mode:0,unkown")
        elif self.G_AMSDeviceWorkMode == AMS_WORK_MODE_MC:
            self.G_PhrozenFluiddRespondInfo("+Mode:1,MC")
        elif self.G_AMSDeviceWorkMode == AMS_WORK_MODE_MA:
            self.G_PhrozenFluiddRespondInfo("+Mode:2,MA")
        elif self.G_AMSDeviceWorkMode == AMS_WORK_MODE_FILA_RUNOUT:
            self.G_PhrozenFluiddRespondInfo("+Mode:3,RUNOUT")
        else:
            self.G_PhrozenFluiddRespondInfo("+Mode:-1,error")

        #lancaigang250619:检查AMS是否重新连接成功
        self.Cmds_USBConnectErrorCheck()

        #lancaigang250526：暂停中，不允许新的gcode命令，需等待暂停完成
        self.G_KlipperInPausing = True
        self.G_PhrozenFluiddRespondInfo("暂停中，不允许新的gcode命令，需等待暂停完成")



        #lancaigang250526：暂停中，不允许新的gcode命令，需等待暂停完成
        self.G_KlipperInPausing = True



        #time.sleep(1)

        #lancaigang231201：klipper暂停时，暂停stm32电机
        #// AT+PAUSE
        #// AT+PAUSE=8
        #// AT+PAUSE=9
        

        #lancaigang241031:
        if self.G_SerialPort1OpenFlag == True:
            self.Cmds_AMSSerial1Send("AT+PAUSE")
            self.G_PhrozenFluiddRespondInfo("串口1发送AT+PAUSE暂停stm32电机")
        #lancaigang241030:
        if self.G_SerialPort2OpenFlag == True:
            self.Cmds_AMSSerial2Send("AT+PAUSE")
            self.G_PhrozenFluiddRespondInfo("串口2发送AT+PAUSE暂停stm32电机")

        #lancaigang231129：暂停时喷头移动到指定位置
        # self.G_PhrozenGCode.run_script_from_command("SAVE_GCODE_STATE NAME=PRZ_PAUSE_STATE")
        # self.G_KlipperIfPaused = True
        # #喷头等待移动
        #lancaigang231207：不能用wait_moves，否则导致保存的gcode命令异常
        # self.G_ProzenToolhead.wait_moves()





        #lancaigang240125：封装函数
        self.Cmds_PhrozenKlipperPauseCommon()


        self.G_KlipperIfPaused = True
        self.G_PhrozenFluiddRespondInfo("self.G_KlipperIfPaused = True")
        self.G_PhrozenFluiddRespondInfo("klipper暂停；")

        #lancaigang250526：
        self.G_KlipperInPausing = False
        self.G_PhrozenFluiddRespondInfo("暂停完成，允许新的gcode命令")

    
    ####################################
    #函数名称：
    #输入参数：
    #返 回 值:
    #功能描述：蓝才刚-20230830
    ####################################
    # PRZ_RESUME 恢复打印(与PRZ_PAUSE对应使用)
    def Cmds_PhrozenKlipperResumeCommon(self):
        self.G_PhrozenFluiddRespondInfo("=====[(cmds.python)Cmds_PhrozenKlipperResumeCommon]klipper恢复")
        
        # #lancaigang240103：延时再恢复
        # #self.G_ProzenToolhead.dwell(3.0)
        # velocity = 2400
        # self.G_PhrozenGCode.run_script_from_command(
        #     "RESTORE_GCODE_STATE NAME=PRZ_PAUSE_STATE MOVE=1 MOVE_SPEED=%.4f"
        #     % (velocity)
        # )
        # self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_PhrozenKlipperResumeCommon]RESTORE_GCODE_STATE")
        # self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_PhrozenKlipperResumeCommon]NAME=PRZ_PAUSE_STATE")
        # self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_PhrozenKlipperResumeCommon]send_resume_command")
        # #klipper恢复命令
        # self.G_PhrozenPrinterCancelPauseResume.send_resume_command()
        # #self.G_ProzenToolhead.wait_moves()
        # self.G_ProzenToolhead.dwell(2.0)
        # # #lancaigang240103：Z轴上升后必须记得下降，对应暂停时的上升高度
        # # command_string = """
        # #     G90
        # #     G91
        # #     G1 Z-10 F3000
        # #     """
        # # self.G_PhrozenGCode.run_script_from_command(command_string)


        self.G_PhrozenFluiddRespondInfo("当前模式")
        if self.G_AMSDeviceWorkMode == AMS_WORK_MODE_UNKNOW:
            self.G_PhrozenFluiddRespondInfo("+Mode:0,unkown")
        elif self.G_AMSDeviceWorkMode == AMS_WORK_MODE_MC:
            self.G_PhrozenFluiddRespondInfo("+Mode:1,MC")
        elif self.G_AMSDeviceWorkMode == AMS_WORK_MODE_MA:
            self.G_PhrozenFluiddRespondInfo("+Mode:2,MA")
        elif self.G_AMSDeviceWorkMode == AMS_WORK_MODE_FILA_RUNOUT:
            self.G_PhrozenFluiddRespondInfo("+Mode:3,RUNOUT")
        else:
            self.G_PhrozenFluiddRespondInfo("+Mode:-1,error")


        Lo_PauseStatus=self.G_PhrozenPrinterCancelPauseResume.get_status(None)
        self.G_PhrozenFluiddRespondInfo("当前暂停状态-Lo_PauseStatus='%s'" % Lo_PauseStatus)
        self.G_PhrozenFluiddRespondInfo("Lo_PauseStatus['is_paused']='%s'" % Lo_PauseStatus['is_paused'])
        #// 当前暂停状态-Lo_PauseStatus='{'is_paused': True}'
        if Lo_PauseStatus['is_paused'] == True:
            self.G_PhrozenFluiddRespondInfo("是暂停状态，需要恢复")
            #lancaigang240119：暂停改用cfg配置表宏命令
            self.G_PhrozenFluiddRespondInfo("外部宏命令-RESUME")
            command = """
            RESUME
            """
            self.G_PhrozenGCode.run_script_from_command(command)
            self.G_PhrozenFluiddRespondInfo("调用宏命令:command=%s" % (command))

            self.G_PauseToLCDString=""
        else:
            self.G_PhrozenFluiddRespondInfo("未暂停状态，不用再恢复")

        self.G_PhrozenFluiddRespondInfo("当前暂停状态-Lo_PauseStatus='%s'" % Lo_PauseStatus)
        self.G_PhrozenFluiddRespondInfo("Lo_PauseStatus['is_paused']='%s'" % Lo_PauseStatus['is_paused'])





        #lancaigang240325：恢复数据之后，需要初始标志位
        self.G_MCModeCanResumeFlag == False
        #lancaigang240108：暂停状态
        self.G_KlipperIfPaused = False
        #lancaigang240124：stm32主动上报，开启可以暂停1次
        self.STM32ReprotPauseFlag=0

        #lancaigang250607：打印状态；1-退料中；2-进料中；3-打印中；4-暂停
        self.G_KlipperPrintStatus= 3

        #lancaigang250619：如果usb连接超过10s，则报错暂停
        self.G_ASM1DisconnectErrorCount= 0




    ####################################
    #函数名称：
    #输入参数：
    #返 回 值:
    #功能描述：蓝才刚-20230830
    ####################################
    # PRZ_RESUME 恢复打印(与PRZ_PAUSE对应使用)
    def Cmds_PhrozenKlipperResume(self, gcmd):
        _ = gcmd
        self.G_PhrozenFluiddRespondInfo("=====[(cmds.py)Cmds_PhrozenKlipperResume]")
        self.G_PhrozenFluiddRespondInfo("+RESUME:1,%d" % self.G_ChangeChannelTimeoutNewChan)
        self.G_PhrozenFluiddRespondInfo("=====RESUME=====")
        self.G_PhrozenFluiddRespondInfo("=====RESUME=====self.G_ChangeChannelTimeoutOldChan=%d" % self.G_ChangeChannelTimeoutOldChan)
        self.G_PhrozenFluiddRespondInfo("=====RESUME=====self.G_ChangeChannelTimeoutNewChan=%d" % self.G_ChangeChannelTimeoutNewChan)

        # #cancel取消命令
        # self.G_PhrozenPrinterCancelPauseResume.cmd_CANCEL_PRINT(None)
        #lancaigang250517：
        Lo_PauseStatus=self.G_PhrozenPrinterCancelPauseResume.get_status(None)
        self.G_PhrozenFluiddRespondInfo("当前暂停状态-Lo_PauseStatus='%s'" % Lo_PauseStatus)
        self.G_PhrozenFluiddRespondInfo("Lo_PauseStatus['is_paused']='%s'" % Lo_PauseStatus['is_paused'])
        #// 当前暂停状态-Lo_PauseStatus='{'is_paused': True}'
        if Lo_PauseStatus['is_paused'] == True:
            self.G_PhrozenFluiddRespondInfo("已是暂停状态")
        else:
            self.G_PhrozenFluiddRespondInfo("未暂停状态")




        #lancaigang240511：恢复的时候，都初始化一下串口，防止热插拔AMS导致的串口通讯异常
        try:
            self.G_PhrozenFluiddRespondInfo("[(cmds.py)Cmds_PhrozenKlipperResume]重新初始化串口1")
            self.G_SerialPort1Obj = serial.Serial(self.G_Serialport1Define, SERIAL_PORT_BAUD, timeout=3)
            #串口打开成功
            if self.G_SerialPort1Obj is not None:
                if self.G_SerialPort1Obj.is_open:
                    self.G_SerialPort1OpenFlag = True
                    self.G_PhrozenFluiddRespondInfo("重新初始化串口1成功")
                    #lancaigang231213：打开串口
                    self.G_SerialPort1Obj.flushInput()  # clean serial write cache
                    self.G_SerialPort1Obj.flush()
                    self.G_PhrozenFluiddRespondInfo("串口1清空")
                    self.G_PhrozenFluiddRespondInfo("重新注册串口1回调函数")
                    self.G_SerialPort1RecvTimmer = self.G_PhrozenReactor.register_timer(self.Device_TimmerUart1Recv, self.G_PhrozenReactor.NOW)
        except:
            self.G_PhrozenFluiddRespondInfo("未能打开tty1口，请检查USB口或重启尝试")

        try:
            self.G_PhrozenFluiddRespondInfo("[(cmds.py)Cmds_PhrozenKlipperResume]重新初始化串口2")
            self.G_SerialPort2Obj = serial.Serial(self.G_Serialport2Define, SERIAL_PORT_BAUD, timeout=3)
            #串口打开成功
            if self.G_SerialPort2Obj is not None:
                if self.G_SerialPort2Obj.is_open:
                    self.G_SerialPort2OpenFlag = True
                    self.G_PhrozenFluiddRespondInfo("重新初始化串口2成功")
                    self.G_SerialPort2Obj.flushInput()  # clean serial write cache
                    self.G_SerialPort2Obj.flush()
                    self.G_PhrozenFluiddRespondInfo("串口2清空")
                    self.G_PhrozenFluiddRespondInfo("重新注册串口2回调函数")
                    self.G_SerialPort2RecvTimmer = self.G_PhrozenReactor.register_timer(self.Device_TimmerUart2Recv, self.G_PhrozenReactor.NOW)
        except:
            self.G_PhrozenFluiddRespondInfo("未能打开tty2口，请检查USB口或重启尝试")




        self.G_PhrozenFluiddRespondInfo("当前模式")
        if self.G_AMSDeviceWorkMode == AMS_WORK_MODE_UNKNOW:
            self.G_PhrozenFluiddRespondInfo("+Mode:0,unkown")
        elif self.G_AMSDeviceWorkMode == AMS_WORK_MODE_MC:
            self.G_PhrozenFluiddRespondInfo("+Mode:1,MC")
        elif self.G_AMSDeviceWorkMode == AMS_WORK_MODE_MA:
            self.G_PhrozenFluiddRespondInfo("+Mode:2,MA")
        elif self.G_AMSDeviceWorkMode == AMS_WORK_MODE_FILA_RUNOUT:
            self.G_PhrozenFluiddRespondInfo("+Mode:3,RUNOUT")
        else:
            self.G_PhrozenFluiddRespondInfo("+Mode:-1,error")


        #lancaigang241108：只有在打印状态下才能暂停
        if self.G_AMSDeviceWorkMode == AMS_WORK_MODE_UNKNOW:#0
            self.G_PhrozenFluiddRespondInfo("不在打印模式，不执行恢复,return")
            self.G_PhrozenFluiddRespondInfo("+RESUME:2,%d" % self.G_ChangeChannelTimeoutNewChan)
            return


        #lancaigang250510：
        if self.PG102Flag==True:
            self.G_PhrozenFluiddRespondInfo("正在吐料中，不允许恢复")
            self.G_PhrozenFluiddRespondInfo("+RESUME:2,%d" % self.G_ChangeChannelTimeoutNewChan)
            return


        # #lancaigang231216：
        # eventtime = self.G_PhrozenReactor.monotonic()
        # # Determine "printing" status
        # idle_timeout = self.G_PhrozenPrinter.lookup_object("idle_timeout")
        # is_printing = idle_timeout.get_status(eventtime)["state"] == "Printing"
        # if is_printing:
        #     self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_PhrozenKlipperResume]正在打印中；命令='%s'")
        # else:
        #     self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_PhrozenKlipperResume]未在打印中；命令='%s；return'")
        #     return
        self.G_PhrozenFluiddRespondInfo("klipper恢复")

        #lancaigang240325：MC模式特殊处理，涉及多次暂停多次进出料
        if self.G_AMSDeviceWorkMode == AMS_WORK_MODE_MC:
            self.G_PhrozenFluiddRespondInfo("多色模式特殊恢复，以第1次暂停为准，后续进出料多次暂停不执行恢复")
        
            #lancaigang241011：先不处理恢复期间的AMS主动上报暂停
            self.STM32ReprotPauseFlag=0

        else:
            self.G_PhrozenFluiddRespondInfo("单色、单色续料恢复")
            #lancaigang240108：暂停状态
            self.G_KlipperIfPaused = False
            #lancaigang240124：stm32主动上报，开启可以暂停1次
            self.STM32ReprotPauseFlag=0

            #lancaigang241106：
            #self.G_P0M2MAStartPrintFlag=0


        #lancaigang240325:
        #lancaigang240426：恢复后置位false
        self.G_ResumeProcessCheckPauseStatus=False
        #lancaigang231207:+PAUSE:1进料卡料标签
        self.G_IfInFilaBlockFlag=False
        #lancaigang240321：PG102过程中暂停标签
        self.PG102DelayPauseFlag=False
        #lancaigang240325：恢复过程状态
        self.G_ChangeChannelResumeFlag=True
        #lancaigang231207：P1 C?自动换料时，如果要恢复，也继续从第1次通道开始
        self.G_ChangeChannelFirstFilaFlag=True
        #self.G_PhrozenFluiddRespondInfo("+RESUME:1,%d" % self.G_ChangeChannelTimeoutNewChan)
        
        #lancaigang250812:单色断料检测，补充回到暂停区
        self.G_RetryToPauseAreaFlag = False
        self.G_RetryToPauseAreaCount = 0





        #=====lancaigang231212：串口屏或网页主动暂停恢复，如果喷头有检测到线材，则直接恢复，不用stm32回退再进料
        #lancaigang240108：主动暂停也需要考虑喷头是否有线材的情况，后续要处理
        if self.G_IfToolheadHaveFilaInitiativePauseFlag  == True:
            self.G_IfToolheadHaveFilaInitiativePauseFlag=False

            #lancaigang240103：单色M2MA续料模式，需要发送stm32恢复状态，防止stm32异常而无法进行补料
            if self.G_AMSDeviceWorkMode == AMS_WORK_MODE_MA:
                self.G_PhrozenFluiddRespondInfo("M2MA模式恢复，主动暂停恢复")
                #lancaigang240122：
                self.AMSRunoutPauseTimeCount = 0
                #lancaigang240123：
                self.AMSRunoutPauseTimeoutFlag=0

                #有线材才可以恢复打印
                if self.G_ToolheadIfHaveFilaFlag:
                    self.G_M2MAModeResumeFlag=True
                    #lancaigang240412：单色模式，如果有AMS多色，需要恢复AMS
                    if self.G_AMSDevice1IfNormal==True or self.G_AMSDevice2IfNormal==True:
                        self.G_PhrozenFluiddRespondInfo("喷头有线材，有AMS多色，不用回退线材，需要发送命令给STM32恢复最后状态")
                        # #self.Cmds_CmdP8(gcmd)
                        # if self.G_SerialPort1OpenFlag == True:
                        #     self.Cmds_AMSSerial1Send("FA")
                        #     self.G_PhrozenFluiddRespondInfo("串口1发送FA")
                        # elif self.G_SerialPort2OpenFlag == True:
                        #     self.Cmds_AMSSerial2Send("FA")
                        #     self.G_PhrozenFluiddRespondInfo("串口2发送FA")

                        #lancaigang250607:
                        self.G_PhrozenFluiddRespondInfo("可以恢复，STM32打印中快速报错")
                        self.G_KlipperQuickPause = True
                        # #lancaigang250427：
                        # if self.G_SerialPort1OpenFlag == True:
                        #     self.Cmds_AMSSerial1Send("AT+EBLOCKEND")
                        #     self.G_PhrozenFluiddRespondInfo("串口1-AMS结束计时缓冲器满时间")
                        # if self.G_SerialPort2OpenFlag == True:
                        #     self.Cmds_AMSSerial2Send("AT+EBLOCKEND")
                        #     self.G_PhrozenFluiddRespondInfo("串口2-AMS结束计时缓冲器满时间")
                        # self.G_ProzenToolhead.dwell(1.5)

                        #lancaigang250522：
                        self.G_PhrozenFluiddRespondInfo("外部宏命令-PG109-升温")
                        command_string = """
                            PG109
                            """
                        self.G_PhrozenGCode.run_script_from_command(command_string)
                        self.G_PhrozenFluiddRespondInfo("外部宏命令-PG109-升温；command_string='%s'" % command_string)
                        if self.G_SerialPort1OpenFlag == True:
                            self.Cmds_AMSSerial1Send("AT+RESTORE")
                            self.G_PhrozenFluiddRespondInfo("串口1-恢复")
                        if self.G_SerialPort2OpenFlag == True:
                            self.Cmds_AMSSerial2Send("AT+RESTORE")
                            self.G_PhrozenFluiddRespondInfo("串口2-恢复")
                        # #lancaigang250611：
                        # self.G_PhrozenFluiddRespondInfo("外部宏命令-PG108-升温吐料擦嘴")
                        # command_string = """
                        #     PG108
                        #     """
                        # self.G_PhrozenGCode.run_script_from_command(command_string)
                        # self.G_PhrozenFluiddRespondInfo("串口屏或网页主动暂停恢复，喷头有线材，恢复不用回退再进料")
                        #lancaigang240125：封装函数
                        self.Cmds_PhrozenKlipperResumeCommon()
                        self.G_ChangeChannelResumeFlag=False
                        self.G_PhrozenFluiddRespondInfo("+RESUME:2,%d" % self.G_ChangeChannelTimeoutNewChan)
                    else:
                        self.G_KlipperQuickPause = False
                        self.G_PhrozenFluiddRespondInfo("喷头有线材，没有有AMS多色，直接恢复")
                        self.G_PhrozenFluiddRespondInfo("串口屏或网页主动暂停恢复，喷头有线材，恢复不用回退再进料")

                        #lancaigang250522：
                        self.G_PhrozenFluiddRespondInfo("外部宏命令-PG109-升温")
                        command_string = """
                            PG109
                            """
                        self.G_PhrozenGCode.run_script_from_command(command_string)
                        self.G_PhrozenFluiddRespondInfo("外部宏命令-PG109-升温；command_string='%s'" % command_string)
                        # #lancaigang250611：
                        # self.G_PhrozenFluiddRespondInfo("外部宏命令-PG108-升温吐料擦嘴")
                        # command_string = """
                        #     PG108
                        #     """
                        # self.G_PhrozenGCode.run_script_from_command(command_string)
                        #lancaigang240125：封装函数
                        self.Cmds_PhrozenKlipperResumeCommon()
                        self.G_ChangeChannelResumeFlag=False
                        self.G_PhrozenFluiddRespondInfo("+RESUME:2,%d" % self.G_ChangeChannelTimeoutNewChan)
                else:
                    if self.G_AMSDevice1IfNormal==True or self.G_AMSDevice2IfNormal==True:
                        self.G_PhrozenFluiddRespondInfo("喷头无线材，有AMS多色，执行P8完整进料过程")
                        #lancaigang241106：
                        self.G_P0M2MAStartPrintFlag=0

                        #lancaigang250522：不允许M3断料检测
                        self.G_IfChangeFilaOngoing = True

                        #lancaigang241106：
                        self.Cmds_CmdP8(gcmd)
                        #lancaigang250619:检查AMS是否重新连接成功
                        self.Cmds_USBConnectErrorCheck()
                        #lancaigang241106:喷头成功进料
                        if self.G_P0M2MAStartPrintFlag==1:
                            #lancaigang250607:
                            self.G_PhrozenFluiddRespondInfo("可以恢复，STM32打印中快速报错")
                            self.G_KlipperQuickPause = True
                            # #lancaigang250427：
                            # if self.G_SerialPort1OpenFlag == True:
                            #     self.Cmds_AMSSerial1Send("AT+EBLOCKEND")
                            #     self.G_PhrozenFluiddRespondInfo("串口1-AMS结束计时缓冲器满时间")
                            # if self.G_SerialPort2OpenFlag == True:
                            #     self.Cmds_AMSSerial2Send("AT+EBLOCKEND")
                            #     self.G_PhrozenFluiddRespondInfo("串口2-AMS结束计时缓冲器满时间")
                            # self.G_ProzenToolhead.dwell(1.5)
                            #lancaigang250423：进料成功，开始吐料，通知AMS开始计时，如果吐料超过5秒缓冲器还是慢状态，说明堵头了
                            #self.Cmds_AMSSerial2Send("AT+EBLOCKCHECK")
                            #self.G_PhrozenFluiddRespondInfo("AMS开始计时缓冲器满时间")
                            if self.G_SerialPort1OpenFlag == True:
                                self.Cmds_AMSSerial1Send("AT+EBLOCKCHECK")
                                self.G_PhrozenFluiddRespondInfo("串口1-AMS开始计时缓冲器满时间")
                            if self.G_SerialPort2OpenFlag == True:
                                self.Cmds_AMSSerial2Send("AT+EBLOCKCHECK")
                                self.G_PhrozenFluiddRespondInfo("串口2-AMS开始计时缓冲器满时间")
                            #self.G_ProzenToolhead.dwell(1)
                            #lancaigang251120：进入吐料，添加标志位，防止PG108吐料过程中喷头霍尔没有线材暂停，导致暂停位置在吐料区，恢复的时候会撞到吐料盒；
                            self.G_PG108Ingoing=1
                            #lancaigang250611：
                            self.G_PhrozenFluiddRespondInfo("外部宏命令-PG108-升温吐料擦嘴")
                            command_string = """
                                PG108
                                """
                            self.G_PhrozenGCode.run_script_from_command(command_string)
                            self.G_PG108Ingoing=0
                            #lancaigang250427：
                            if self.G_SerialPort1OpenFlag == True:
                                self.Cmds_AMSSerial1Send("AT+EBLOCKEND")
                                self.G_PhrozenFluiddRespondInfo("串口1-AMS结束计时缓冲器满时间")
                            if self.G_SerialPort2OpenFlag == True:
                                self.Cmds_AMSSerial2Send("AT+EBLOCKEND")
                                self.G_PhrozenFluiddRespondInfo("串口2-AMS结束计时缓冲器满时间")
                            
                            if self.STM32ReprotPauseFlag == 1:
                                self.G_PhrozenFluiddRespondInfo("STM32上报已暂停，不能恢复")
                                #lancaigang240125：封装函数
                                #self.Cmds_PhrozenKlipperResumeCommon()
                                self.G_ChangeChannelResumeFlag=False
                                self.G_PhrozenFluiddRespondInfo("+RESUME:0,%d" % self.G_ChangeChannelTimeoutNewChan)
                            else:
                                self.G_PhrozenFluiddRespondInfo("喷头有线材，恢复")
                                #lancaigang240125：封装函数
                                self.Cmds_PhrozenKlipperResumeCommon()
                                self.G_ChangeChannelResumeFlag=False
                                self.G_PhrozenFluiddRespondInfo("+RESUME:2,%d" % self.G_ChangeChannelTimeoutNewChan)
                        else:
                            self.G_KlipperQuickPause = False
                            self.G_PhrozenFluiddRespondInfo("喷头无线材，单色续料继续暂停")
                            if self.G_KlipperIfPaused == False:
                                self.G_PhrozenGCode.run_script_from_command("SAVE_GCODE_STATE NAME=PAUSE")
                                self.G_PhrozenFluiddRespondInfo("[(cmds.python)]PAUSE")
                                self.G_PhrozenPrinterCancelPauseResume.send_pause_command()
                                self.G_ProzenToolhead.wait_moves()
                                self.G_KlipperIfPaused=True
                                #self.G_PhrozenFluiddRespondInfo("+PAUSE:b,%d" % self.G_ChangeChannelTimeoutNewChan)
                                self.G_PhrozenFluiddRespondInfo("+PAUSE:4,%d,%d" % (self.G_ChangeChannelTimeoutOldChan,self.G_ChangeChannelTimeoutNewChan))
                            else:
                                self.G_PhrozenFluiddRespondInfo("已经暂停，不用重复暂停")
                            self.G_ChangeChannelResumeFlag=False
                            self.G_PhrozenFluiddRespondInfo("+RESUME:0,%d" % self.G_ChangeChannelTimeoutNewChan)
                    else:
                        self.G_PhrozenFluiddRespondInfo("喷头无线材，没有AMS多色，单色续料继续暂停")
                        if self.G_KlipperIfPaused == False:
                            self.G_PhrozenGCode.run_script_from_command("SAVE_GCODE_STATE NAME=PAUSE")
                            self.G_PhrozenFluiddRespondInfo("[(cmds.python)]PAUSE")
                            self.G_PhrozenPrinterCancelPauseResume.send_pause_command()
                            self.G_ProzenToolhead.wait_moves()
                            self.G_KlipperIfPaused=True
                            #self.G_PhrozenFluiddRespondInfo("+PAUSE:b,%d" % self.G_ChangeChannelTimeoutNewChan)
                            self.G_PhrozenFluiddRespondInfo("+PAUSE:4,%d,%d" % (self.G_ChangeChannelTimeoutOldChan,self.G_ChangeChannelTimeoutNewChan))
                        else:
                            self.G_PhrozenFluiddRespondInfo("已经暂停，不用重复暂停")
                        self.G_ChangeChannelResumeFlag=False
                        self.G_PhrozenFluiddRespondInfo("+RESUME:0,%d" % self.G_ChangeChannelTimeoutNewChan)

                return


            if self.G_AMSDeviceWorkMode == AMS_WORK_MODE_FILA_RUNOUT:
                self.G_PhrozenFluiddRespondInfo("M3模式恢复，主动暂停恢复")
                # #lancaigang241106:有AMS多色
                # if self.G_AMSDevice1IfNormal==True or self.G_AMSDevice2IfNormal==True:
                #     self.G_PhrozenFluiddRespondInfo("单色M3模式，有AMS多色，需要发送stm32恢复状态")
                #     # #lancaigang240416:
                #     # if self.G_SerialPort1OpenFlag == True:
                #     #     self.Cmds_AMSSerial1Send("MA")
                #     #     self.G_PhrozenFluiddRespondInfo("串口1-MA")
                #     # #lancaigang241030:
                #     # elif self.G_SerialPort2OpenFlag == True:
                #     #     self.Cmds_AMSSerial2Send("MA")
                #     #     self.G_PhrozenFluiddRespondInfo("串口2-MA")

                #     # time.sleep(2)

                #     # #lancaigang240416:
                #     # if self.G_SerialPort1OpenFlag == True:
                #     #     self.Cmds_AMSSerial1Send("FA")
                #     #     self.G_PhrozenFluiddRespondInfo("串口1-FA")
                #     # #lancaigang241030:
                #     # elif self.G_SerialPort2OpenFlag == True:
                #     #     self.Cmds_AMSSerial2Send("FA")
                #     #     self.G_PhrozenFluiddRespondInfo("串口2-FA")

                #     #lancaigang241106：
                #     self.Cmds_CmdP8(gcmd)
                #     #lancaigang241106:喷头成功进料
                #     if self.G_P0M2MAStartPrintFlag==1:
                #         self.G_PhrozenFluiddRespondInfo("串口屏或网页主动暂停恢复，喷头有线材，恢复不用回退再进料")
                #         #lancaigang240125：封装函数
                #         self.Cmds_PhrozenKlipperResumeCommon()
                #     else:
                #         self.G_PhrozenFluiddRespondInfo("喷头无线材，单色续料继续暂停")
                #         self.G_PhrozenPrinterCancelPauseResume.send_pause_command()
                #         self.G_PhrozenFluiddRespondInfo("send_pause_command")
                #         #无线材继续暂停
                #         self.G_KlipperIfPaused=True
                #         self.G_PhrozenFluiddRespondInfo("+PAUSE:b,%d" % self.G_ChangeChannelTimeoutNewChan)
                # else:
                #     if self.G_ToolheadIfHaveFilaFlag==True:
                #         self.G_PhrozenFluiddRespondInfo("单色M3模式，没有AMS多色，klipper直接恢复")
                #         self.G_PhrozenFluiddRespondInfo("串口屏或网页主动暂停恢复，喷头有线材，恢复不用回退再进料")
                #         #lancaigang240125：封装函数
                #         self.Cmds_PhrozenKlipperResumeCommon()
                #     else:
                #         self.G_PhrozenFluiddRespondInfo("喷头无线材，单色续料继续暂停")
                #         self.G_PhrozenPrinterCancelPauseResume.send_pause_command()
                #         self.G_PhrozenFluiddRespondInfo("send_pause_command")
                #         #无线材继续暂停
                #         self.G_KlipperIfPaused=True
                #         self.G_PhrozenFluiddRespondInfo("+PAUSE:b,%d" % self.G_ChangeChannelTimeoutNewChan)

                #有线材才可以恢复打印
                if self.G_ToolheadIfHaveFilaFlag:
                    #lancaigang240412：M3模式，如果有AMS多色，需要恢复AMS
                    if self.G_AMSDevice1IfNormal==True or self.G_AMSDevice2IfNormal==True:
                        self.G_PhrozenFluiddRespondInfo("喷头有线材，有AMS多色，不用回退线材，需要发送命令给STM32恢复最后状态")
                        # #self.Cmds_CmdP8(gcmd)
                        # if self.G_SerialPort1OpenFlag == True:
                        #     self.Cmds_AMSSerial1Send("FA")
                        #     self.G_PhrozenFluiddRespondInfo("串口1发送FA")
                        # elif self.G_SerialPort2OpenFlag == True:
                        #     self.Cmds_AMSSerial2Send("FA")
                        #     self.G_PhrozenFluiddRespondInfo("串口2发送FA")
                        #lancaigang250607:
                        self.G_PhrozenFluiddRespondInfo("可以恢复，STM32打印中快速报错")
                        self.G_KlipperQuickPause = True
                        # #lancaigang250427：
                        # if self.G_SerialPort1OpenFlag == True:
                        #     self.Cmds_AMSSerial1Send("AT+EBLOCKEND")
                        #     self.G_PhrozenFluiddRespondInfo("串口1-AMS结束计时缓冲器满时间")
                        # if self.G_SerialPort2OpenFlag == True:
                        #     self.Cmds_AMSSerial2Send("AT+EBLOCKEND")
                        #     self.G_PhrozenFluiddRespondInfo("串口2-AMS结束计时缓冲器满时间")
                        # self.G_ProzenToolhead.dwell(1.5)

                        #lancaigang250522：
                        self.G_PhrozenFluiddRespondInfo("外部宏命令-PG109-升温")
                        command_string = """
                            PG109
                            """
                        self.G_PhrozenGCode.run_script_from_command(command_string)
                        self.G_PhrozenFluiddRespondInfo("外部宏命令-PG109-升温；command_string='%s'" % command_string)
                        if self.G_SerialPort1OpenFlag == True:
                            self.Cmds_AMSSerial1Send("AT+RESTORE")
                            self.G_PhrozenFluiddRespondInfo("串口1-恢复")
                        if self.G_SerialPort2OpenFlag == True:
                            self.Cmds_AMSSerial2Send("AT+RESTORE")
                            self.G_PhrozenFluiddRespondInfo("串口2-恢复")

                        # #lancaigang250611：
                        # self.G_PhrozenFluiddRespondInfo("外部宏命令-PG108-升温吐料擦嘴")
                        # command_string = """
                        #     PG108
                        #     """
                        # self.G_PhrozenGCode.run_script_from_command(command_string)
                        # self.G_PhrozenFluiddRespondInfo("串口屏或网页主动暂停恢复，喷头有线材，恢复不用回退再进料")
                        #lancaigang240125：封装函数
                        self.Cmds_PhrozenKlipperResumeCommon()
                        self.G_ChangeChannelResumeFlag=False
                        self.G_PhrozenFluiddRespondInfo("+RESUME:2,%d" % self.G_ChangeChannelTimeoutNewChan)
                    else:
                        self.G_KlipperQuickPause = False
                        self.G_PhrozenFluiddRespondInfo("喷头有线材，没有有AMS多色，直接恢复")
                        #lancaigang250522：
                        self.G_PhrozenFluiddRespondInfo("外部宏命令-PG109-升温")
                        command_string = """
                            PG109
                            """
                        self.G_PhrozenGCode.run_script_from_command(command_string)
                        self.G_PhrozenFluiddRespondInfo("外部宏命令-PG109-升温；command_string='%s'" % command_string)
                        # self.G_PhrozenFluiddRespondInfo("串口屏或网页主动暂停恢复，喷头有线材，恢复不用回退再进料")
                        # #lancaigang250409：恢复的时候再吐料
                        # command_string = """
                        # PG108
                        # """
                        # self.G_PhrozenGCode.run_script_from_command(command_string)
                        # self.G_PhrozenFluiddRespondInfo("command_string='%s'" % command_string)
                        # self.G_PhrozenFluiddRespondInfo("吐料完成，喷头检测到有线材恢复打印")
                        #lancaigang240125：封装函数
                        self.Cmds_PhrozenKlipperResumeCommon()
                        self.G_ChangeChannelResumeFlag=False
                        self.G_PhrozenFluiddRespondInfo("+RESUME:2,%d" % self.G_ChangeChannelTimeoutNewChan)
                else:
                    if self.G_AMSDevice1IfNormal==True or self.G_AMSDevice2IfNormal==True:
                        self.G_PhrozenFluiddRespondInfo("喷头无线材，有AMS多色，执行P8完整进料过程")
                        #lancaigang241106：
                        self.G_P0M2MAStartPrintFlag=0

                        #lancaigang250522：不允许M3断料检测
                        self.G_IfChangeFilaOngoing = True

                        #lancaigang241106：
                        self.Cmds_CmdP8(gcmd)
                        #lancaigang250619:检查AMS是否重新连接成功
                        self.Cmds_USBConnectErrorCheck()
                        #lancaigang241106:喷头成功进料
                        if self.G_P0M2MAStartPrintFlag==1:
                            #lancaigang250607:
                            self.G_PhrozenFluiddRespondInfo("可以恢复，STM32打印中快速报错")
                            self.G_KlipperQuickPause = True
                            # #lancaigang250427：
                            # if self.G_SerialPort1OpenFlag == True:
                            #     self.Cmds_AMSSerial1Send("AT+EBLOCKEND")
                            #     self.G_PhrozenFluiddRespondInfo("串口1-AMS结束计时缓冲器满时间")
                            # if self.G_SerialPort2OpenFlag == True:
                            #     self.Cmds_AMSSerial2Send("AT+EBLOCKEND")
                            #     self.G_PhrozenFluiddRespondInfo("串口2-AMS结束计时缓冲器满时间")
                            # self.G_ProzenToolhead.dwell(1.5)
                            if self.G_SerialPort1OpenFlag == True:
                                self.Cmds_AMSSerial1Send("AT+EBLOCKCHECK")
                                self.G_PhrozenFluiddRespondInfo("串口1-AMS开始计时缓冲器满时间")
                            if self.G_SerialPort2OpenFlag == True:
                                self.Cmds_AMSSerial2Send("AT+EBLOCKCHECK")
                                self.G_PhrozenFluiddRespondInfo("串口2-AMS开始计时缓冲器满时间")
                            #self.G_ProzenToolhead.dwell(1)
                            #lancaigang251120：进入吐料，添加标志位，防止PG108吐料过程中喷头霍尔没有线材暂停，导致暂停位置在吐料区，恢复的时候会撞到吐料盒；
                            self.G_PG108Ingoing=1
                            #lancaigang250611：
                            self.G_PhrozenFluiddRespondInfo("外部宏命令-PG108-升温吐料擦嘴")
                            command_string = """
                                PG108
                                """
                            self.G_PhrozenGCode.run_script_from_command(command_string)
                            self.G_PG108Ingoing=0
                            #lancaigang250427：
                            if self.G_SerialPort1OpenFlag == True:
                                self.Cmds_AMSSerial1Send("AT+EBLOCKEND")
                                self.G_PhrozenFluiddRespondInfo("串口1-AMS结束计时缓冲器满时间")
                            if self.G_SerialPort2OpenFlag == True:
                                self.Cmds_AMSSerial2Send("AT+EBLOCKEND")
                                self.G_PhrozenFluiddRespondInfo("串口2-AMS结束计时缓冲器满时间")
                            if self.STM32ReprotPauseFlag == 1:
                                self.G_PhrozenFluiddRespondInfo("STM32上报已暂停，不能恢复")
                                #lancaigang240125：封装函数
                                #self.Cmds_PhrozenKlipperResumeCommon()
                                self.G_ChangeChannelResumeFlag=False
                                self.G_PhrozenFluiddRespondInfo("+RESUME:0,%d" % self.G_ChangeChannelTimeoutNewChan)
                            else:
                                self.G_PhrozenFluiddRespondInfo("喷头有线材，恢复")
                                #lancaigang240125：封装函数
                                self.Cmds_PhrozenKlipperResumeCommon()
                                self.G_ChangeChannelResumeFlag=False
                                self.G_PhrozenFluiddRespondInfo("+RESUME:2,%d" % self.G_ChangeChannelTimeoutNewChan)
                        else:
                            self.G_KlipperQuickPause = False
                            self.G_PhrozenFluiddRespondInfo("喷头无线材，M3模式续料继续暂停")
                            if self.G_KlipperIfPaused == False:
                                self.G_PhrozenGCode.run_script_from_command("SAVE_GCODE_STATE NAME=PAUSE")
                                self.G_PhrozenFluiddRespondInfo("[(cmds.python)]PAUSE")
                                self.G_PhrozenPrinterCancelPauseResume.send_pause_command()
                                self.G_ProzenToolhead.wait_moves()
                                self.G_KlipperIfPaused=True
                                #self.G_PhrozenFluiddRespondInfo("+PAUSE:b,%d" % self.G_ChangeChannelTimeoutNewChan)
                                self.G_PhrozenFluiddRespondInfo("+PAUSE:4,%d,%d" % (self.G_ChangeChannelTimeoutOldChan,self.G_ChangeChannelTimeoutNewChan))
                            else:
                                self.G_PhrozenFluiddRespondInfo("已经暂停，不用重复暂停")
                            self.G_ChangeChannelResumeFlag=False
                            self.G_PhrozenFluiddRespondInfo("+RESUME:0,%d" % self.G_ChangeChannelTimeoutNewChan)
                    else:
                        self.G_KlipperQuickPause = False
                        self.G_PhrozenFluiddRespondInfo("喷头无线材，没有AMS多色，M3模式继续暂停")
                        self.G_PhrozenGCode.run_script_from_command("SAVE_GCODE_STATE NAME=PAUSE")
                        self.G_PhrozenFluiddRespondInfo("[(cmds.python)]PAUSE")
                        self.G_PhrozenPrinterCancelPauseResume.send_pause_command()
                        self.G_ProzenToolhead.wait_moves()
                        #无线材继续暂停
                        self.G_KlipperIfPaused=True
                        #self.G_PhrozenFluiddRespondInfo("+PAUSE:b,%d" % self.G_ChangeChannelTimeoutNewChan)
                        self.G_PhrozenFluiddRespondInfo("+PAUSE:b,%d,%d" % (self.G_ChangeChannelTimeoutOldChan,self.G_ChangeChannelTimeoutNewChan))
                        self.G_ChangeChannelResumeFlag=False
                        self.G_PhrozenFluiddRespondInfo("+RESUME:0,%d" % self.G_ChangeChannelTimeoutNewChan)

                        


                return


            #lancaigang240115：主动暂停的恢复，恢复stm32状态到慢速打印补料状态
            if self.G_AMSDeviceWorkMode == AMS_WORK_MODE_MC:
                self.G_PhrozenFluiddRespondInfo("M1MC模式恢复")
                #lancaigang240521：恢复的时候，如果发现AMS异常重启，可以认为是热插拔AMS，执行完整的退料换料过程
                if self.G_ResumeCheckAMS1ErrorRestartFlag == True:
                    self.G_ResumeCheckAMS1ErrorRestartFlag=False
                    self.G_PhrozenFluiddRespondInfo("串口屏或网页主动暂停恢复;多色MC模式；发现AMS异常重启，执行恢复换料过程")
                else:
                    self.G_PhrozenFluiddRespondInfo("串口屏或网页主动暂停恢复;多色MC模式，stm32恢复慢速打印补料状态")
                    #self.Cmds_AMSSerial1Send("AT+MCRS=F")
                    #self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_PhrozenKlipperResume]AT+MCRS=F")
                    #lancaigang240115：如果屏幕主动暂停期间，操作了手动命令，stm32状态会变来变去，无法知道暂停前的状态了，只能重新执行P1 C?命令
                    #如果喷头有线材，说明stm32可以直接转换到慢速补料状态
                    if self.G_ToolheadIfHaveFilaFlag==True:
                        # #lancaigang241030:
                        # if self.G_ChangeChannelTimeoutNewChan in range(1, 4):
                        #     #lancaigang0427：不管中间是否有了手动命令，恢复stm32的时候，强制改为慢速补料状态
                        #     self.Cmds_AMSSerial1Send("AT+MCRS=5,%d" % self.G_ChangeChannelTimeoutNewChan)#05=慢速补料状态
                        #     self.G_PhrozenFluiddRespondInfo("AT+MCRS=5,%d" % self.G_ChangeChannelTimeoutNewChan)
                        # elif self.G_ChangeChannelTimeoutNewChan in range(5, 8):
                        #     self.Cmds_AMSSerial2Send("AT+MCRS=5,%d" % self.G_ChangeChannelTimeoutNewChan-4)#05=慢速补料状态
                        #     self.G_PhrozenFluiddRespondInfo("AT+MCRS=5,%d" % self.G_ChangeChannelTimeoutNewChan-4)

                        self.G_PhrozenFluiddRespondInfo("多色MC模式，发送stm32恢复慢速打印补料状态")
                        self.G_PhrozenFluiddRespondInfo("串口屏或网页主动暂停恢复，喷头有线材")
                        
                        # if self.G_SerialPort1OpenFlag == True:
                        #     self.Cmds_AMSSerial1Send("AT+RESTORE")
                        #     self.G_PhrozenFluiddRespondInfo("串口1-恢复")
                        # if self.G_SerialPort2OpenFlag == True:
                        #     self.Cmds_AMSSerial2Send("AT+RESTORE")
                        #     self.G_PhrozenFluiddRespondInfo("串口2-恢复")

                        # #lancaigang241012：主动暂停也需要重新进料，防止AMS状态切换异常

                        # #lancaigang240125：封装函数
                        # self.Cmds_PhrozenKlipperResumeCommon()
                        # self.G_ChangeChannelResumeFlag=False
                        # self.G_PhrozenFluiddRespondInfo("+RESUME:2,%d" % self.G_ChangeChannelTimeoutNewChan)
                        # return
                    
                    else:
                        self.G_PhrozenFluiddRespondInfo("串口屏或网页主动暂停恢复;喷头没有线材，执行恢复换料过程")




        #=====lancaigang231229：MA单色续料单独处理，与单机单色区别
        if self.G_AMSDeviceWorkMode == AMS_WORK_MODE_MA:
            self.G_PhrozenFluiddRespondInfo("M2MA模式恢复")
            #lancaigang240122：
            self.AMSRunoutPauseTimeCount = 0
            #lancaigang240123：
            self.AMSRunoutPauseTimeoutFlag=0

            # # #lancaigang240416:
            # # if self.G_SerialPort1OpenFlag == True:
            # #     self.Cmds_AMSSerial1Send("MA")
            # #     self.G_PhrozenFluiddRespondInfo("串口1-MA")
            # # #lancaigang241030:
            # # elif self.G_SerialPort2OpenFlag == True:
            # #     self.Cmds_AMSSerial2Send("MA")
            # #     self.G_PhrozenFluiddRespondInfo("串口2-MA")

            # # #lancaigang240115:延时1秒，防止粘包
            # # time.sleep(2)

            # #有线材才可以恢复打印
            # if self.G_ToolheadIfHaveFilaFlag:
            #     # #lancaigang231228：恢复之后，发送命令给stm32恢复上一次状态机状态
            #     # #恢复状态RS=F,即恢复上一次状态
            #     # #恢复状态RS=0,即恢复上MASTATEMACHINE_IDLE_STANDBY状态
            #     # #恢复状态RS=X,...
            #     # #恢复状态RS=Y,...
            #     # #恢复状态RS=Z,...
            #     # #lancaigang240108：先不发送
            #     # #self.Cmds_AMSSerial1Send("AT+MARS=F")
            #     # #self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_PhrozenKlipperResume]AT+MARS=F")
            #     # #lancaigang240108：重新选择旧工作通道进行打印，避免料管里面的线材是断料导致异常
            #     # #lancaigang240226：喷头有线材，不用发送FA
            #     # #lancaigang240416:
            #     # if self.G_SerialPort1OpenFlag == True:
            #     #     self.Cmds_AMSSerial1Send("FA")
            #     #     self.G_PhrozenFluiddRespondInfo("串口1-FA")
            #     # #lancaigang241030:
            #     # elif self.G_SerialPort2OpenFlag == True:
            #     #     self.Cmds_AMSSerial2Send("FA")
            #     #     self.G_PhrozenFluiddRespondInfo("串口2-FA")

            #     # self.G_PhrozenFluiddRespondInfo("单色M2MA续料模式，喷头有线材直接恢复")
            #     # #lancaigang240108：挤料完成再恢复
            #     # #if self.P0M3FilaRunoutSpittingFinished == True:
            #     # #self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_PhrozenKlipperResume]挤料完成，可以恢复")


            #     #lancaigang241106：
            #     self.Cmds_CmdP8(gcmd)
            #     #lancaigang241106:喷头成功进料
            #     if self.G_P0M2MAStartPrintFlag==1:
            #         self.G_PhrozenFluiddRespondInfo("喷头有线材，回退再进料")
            #         #lancaigang240125：封装函数
            #         self.Cmds_PhrozenKlipperResumeCommon()
            #     else:
            #         self.G_PhrozenFluiddRespondInfo("喷头无线材，单色续料继续暂停")
            #         self.G_PhrozenPrinterCancelPauseResume.send_pause_command()
            #         self.G_PhrozenFluiddRespondInfo("send_pause_command")
            #         #无线材继续暂停
            #         self.G_KlipperIfPaused=True
            #         self.G_PhrozenFluiddRespondInfo("+PAUSE:4,%d" % self.G_ChangeChannelTimeoutNewChan)

            #     #lancaigang241106：
            #     #self.Cmds_CmdP8(gcmd)
            #     #self.Cmds_PhrozenKlipperResumeCommon()


            #     #lancaigang240108：喷头有线材，可以恢复
            #     self.G_M2MAModeResumeFlag=True

            #     self.G_ChangeChannelResumeFlag=False
            #     self.G_PhrozenFluiddRespondInfo("+RESUME:2,%d" % self.G_ChangeChannelTimeoutNewChan)

            #     return
            # #没有线材需要重新进料
            # else:
            #     #lancaigang240108：恢复的时候，允许断线挤料
            #     self.P0M3FilaRunoutSpittingFinished = False
            #     self.G_ToolheadFirstInputFila=False
            #     #lancaigang240108：喷头有线材，可以恢复
            #     #lancaigang240109：不管进料是否超时只要喷头检测到线材，就可以进行恢复操作
            #     self.G_M2MAModeResumeFlag=True

            #     self.G_PhrozenFluiddRespondInfo("单色M2MA续料模式，喷头无线材需要重新进新料")



            #     # #lancaigang240103：喷头无线材，需要重新进料，重新编排进料顺序，执行单色自动续料F8
            #     # #ttyUSB0串口发送：FA
            #     # #lancaigang240108：先不发送FA
            #     # #lancaigang240416:
            #     # if self.G_SerialPort1OpenFlag == True:
            #     #     self.Cmds_AMSSerial1Send("FA")
            #     #     self.G_PhrozenFluiddRespondInfo("串口1-FA")
            #     # #lancaigang241030:
            #     # elif self.G_SerialPort2OpenFlag == True:
            #     #     self.Cmds_AMSSerial2Send("FA")
            #     #     self.G_PhrozenFluiddRespondInfo("串口2-FA")
            #     # #lancaigang231229:封装函数
            #     # self.Cmds_MARetryInFila(gcmd)

            #     #lancaigang241106：
            #     self.Cmds_CmdP8(gcmd)
            #     #lancaigang241106:喷头成功进料
            #     if self.G_P0M2MAStartPrintFlag==1:
            #         self.G_PhrozenFluiddRespondInfo("喷头有线材，回退再进料")
            #         #lancaigang240125：封装函数
            #         self.Cmds_PhrozenKlipperResumeCommon()
            #     else:
            #         self.G_PhrozenFluiddRespondInfo("喷头无线材，单色续料继续暂停")
            #         self.G_PhrozenPrinterCancelPauseResume.send_pause_command()
            #         self.G_PhrozenFluiddRespondInfo("send_pause_command")
            #         #无线材继续暂停
            #         self.G_KlipperIfPaused=True
            #         self.G_PhrozenFluiddRespondInfo("+PAUSE:4,%d" % self.G_ChangeChannelTimeoutNewChan)

            #有线材才可以恢复打印
            if self.G_ToolheadIfHaveFilaFlag:
                self.G_M2MAModeResumeFlag=True
                #lancaigang240412：M2MA模式，如果有AMS多色，需要恢复AMS
                if self.G_AMSDevice1IfNormal==True or self.G_AMSDevice2IfNormal==True:
                    self.G_PhrozenFluiddRespondInfo("喷头有线材，有AMS多色，但還是执行P8完整进料过程，防止切綫異常情況")
                    self.G_P0M2MAStartPrintFlag=0

                    #lancaigang250522：不允许M3断料检测
                    self.G_IfChangeFilaOngoing = True

                    self.Cmds_CmdP8(gcmd)
                    #lancaigang250619:检查AMS是否重新连接成功
                    self.Cmds_USBConnectErrorCheck()
                    # if self.G_SerialPort1OpenFlag == True:
                    #     self.Cmds_AMSSerial1Send("FA")
                    #     self.G_PhrozenFluiddRespondInfo("串口1发送FA")
                    # elif self.G_SerialPort2OpenFlag == True:
                    #     self.Cmds_AMSSerial2Send("FA")
                    #     self.G_PhrozenFluiddRespondInfo("串口2发送FA")
                    #lancaigang241106:喷头成功进料
                    if self.G_P0M2MAStartPrintFlag==1:
                        #lancaigang250607:
                        self.G_PhrozenFluiddRespondInfo("可以恢复，STM32打印中快速报错")
                        self.G_KlipperQuickPause = True
                        # #lancaigang250427：
                        # if self.G_SerialPort1OpenFlag == True:
                        #     self.Cmds_AMSSerial1Send("AT+EBLOCKEND")
                        #     self.G_PhrozenFluiddRespondInfo("串口1-AMS结束计时缓冲器满时间")
                        # if self.G_SerialPort2OpenFlag == True:
                        #     self.Cmds_AMSSerial2Send("AT+EBLOCKEND")
                        #     self.G_PhrozenFluiddRespondInfo("串口2-AMS结束计时缓冲器满时间")
                        # self.G_ProzenToolhead.dwell(1.5)
                        #lancaigang250522：
                        # self.G_PhrozenFluiddRespondInfo("外部宏命令-PG109-升温")
                        # command_string = """
                        #     PG109
                        #     """
                        # self.G_PhrozenGCode.run_script_from_command(command_string)
                        # self.G_PhrozenFluiddRespondInfo("外部宏命令-PG109-升温；command_string='%s'" % command_string)
                        # if self.G_SerialPort1OpenFlag == True:
                        #     self.Cmds_AMSSerial1Send("AT+RESTORE")
                        #     self.G_PhrozenFluiddRespondInfo("串口1-恢复")
                        # if self.G_SerialPort2OpenFlag == True:
                        #     self.Cmds_AMSSerial2Send("AT+RESTORE")
                        #     self.G_PhrozenFluiddRespondInfo("串口2-恢复")
                        # self.G_PhrozenFluiddRespondInfo("喷头有线材，恢复")
                        # #lancaigang250611：
                        # self.G_PhrozenFluiddRespondInfo("外部宏命令-PG108-升温吐料擦嘴")
                        # command_string = """
                        #     PG108
                        #     """
                        # self.G_PhrozenGCode.run_script_from_command(command_string)
                        # #lancaigang240125：封装函数
                        # self.Cmds_PhrozenKlipperResumeCommon()
                        if self.G_SerialPort1OpenFlag == True:
                            self.Cmds_AMSSerial1Send("AT+EBLOCKCHECK")
                            self.G_PhrozenFluiddRespondInfo("串口1-AMS开始计时缓冲器满时间")
                        if self.G_SerialPort2OpenFlag == True:
                            self.Cmds_AMSSerial2Send("AT+EBLOCKCHECK")
                            self.G_PhrozenFluiddRespondInfo("串口2-AMS开始计时缓冲器满时间")
                        #self.G_ProzenToolhead.dwell(1)
                        #lancaigang250522：
                        self.G_PhrozenFluiddRespondInfo("外部宏命令-PG109-升温")
                        command_string = """
                            PG109
                            """
                        self.G_PhrozenGCode.run_script_from_command(command_string)
                        self.G_PhrozenFluiddRespondInfo("外部宏命令-PG109-升温；command_string='%s'" % command_string)
                        #lancaigang251120：进入吐料，添加标志位，防止PG108吐料过程中喷头霍尔没有线材暂停，导致暂停位置在吐料区，恢复的时候会撞到吐料盒；
                        self.G_PG108Ingoing=1
                        #lancaigang250611：
                        self.G_PhrozenFluiddRespondInfo("外部宏命令-PG108-升温吐料擦嘴")
                        command_string = """
                            PG108
                            """
                        self.G_PhrozenGCode.run_script_from_command(command_string)
                        self.G_PG108Ingoing=0
                        #lancaigang250427：
                        if self.G_SerialPort1OpenFlag == True:
                            self.Cmds_AMSSerial1Send("AT+EBLOCKEND")
                            self.G_PhrozenFluiddRespondInfo("串口1-AMS结束计时缓冲器满时间")
                        if self.G_SerialPort2OpenFlag == True:
                            self.Cmds_AMSSerial2Send("AT+EBLOCKEND")
                            self.G_PhrozenFluiddRespondInfo("串口2-AMS结束计时缓冲器满时间")
                        if self.STM32ReprotPauseFlag == 1:
                            self.G_PhrozenFluiddRespondInfo("STM32上报已暂停，不能恢复")
                            #lancaigang240125：封装函数
                            #self.Cmds_PhrozenKlipperResumeCommon()
                            self.G_ChangeChannelResumeFlag=False
                            self.G_PhrozenFluiddRespondInfo("+RESUME:0,%d" % self.G_ChangeChannelTimeoutNewChan)
                        else:
                            self.G_PhrozenFluiddRespondInfo("喷头有线材，恢复")
                            #lancaigang240125：封装函数
                            self.Cmds_PhrozenKlipperResumeCommon()
                            self.G_ChangeChannelResumeFlag=False
                            self.G_PhrozenFluiddRespondInfo("+RESUME:2,%d" % self.G_ChangeChannelTimeoutNewChan)
                    else:
                        self.G_KlipperQuickPause = False
                        self.G_PhrozenFluiddRespondInfo("喷头无线材，M2MA模式继续暂停")
                        if self.G_KlipperIfPaused == False:
                            self.G_PhrozenGCode.run_script_from_command("SAVE_GCODE_STATE NAME=PAUSE")
                            self.G_PhrozenFluiddRespondInfo("[(cmds.python)]PAUSE")
                            self.G_PhrozenPrinterCancelPauseResume.send_pause_command()
                            self.G_ProzenToolhead.wait_moves()
                            #无线材继续暂停
                            self.G_KlipperIfPaused=True
                            #self.G_PhrozenFluiddRespondInfo("+PAUSE:b,%d" % self.G_ChangeChannelTimeoutNewChan)
                            self.G_PhrozenFluiddRespondInfo("+PAUSE:4,%d,%d" % (self.G_ChangeChannelTimeoutOldChan,self.G_ChangeChannelTimeoutNewChan))
                        else:
                            self.G_PhrozenFluiddRespondInfo("已经暂停，不用重复暂停")
                        self.G_ChangeChannelResumeFlag=False
                        self.G_PhrozenFluiddRespondInfo("+RESUME:0,%d" % self.G_ChangeChannelTimeoutNewChan)
                else:
                    self.G_KlipperQuickPause = False
                    self.G_PhrozenFluiddRespondInfo("喷头有线材，没有有AMS多色，直接恢复")
                    self.G_PhrozenFluiddRespondInfo("喷头有线材，恢复不用回退再进料")

                    #lancaigang250522：
                    self.G_PhrozenFluiddRespondInfo("外部宏命令-PG109-升温")
                    command_string = """
                        PG109
                        """
                    self.G_PhrozenGCode.run_script_from_command(command_string)
                    self.G_PhrozenFluiddRespondInfo("外部宏命令-PG109-升温；command_string='%s'" % command_string)
                    #lancaigang251120：进入吐料，添加标志位，防止PG108吐料过程中喷头霍尔没有线材暂停，导致暂停位置在吐料区，恢复的时候会撞到吐料盒；
                    self.G_PG108Ingoing=1
                    #lancaigang250611：
                    self.G_PhrozenFluiddRespondInfo("外部宏命令-PG108-升温吐料擦嘴")
                    command_string = """
                        PG108
                        """
                    self.G_PhrozenGCode.run_script_from_command(command_string)
                    self.G_PG108Ingoing=0
                    #lancaigang240125：封装函数
                    self.Cmds_PhrozenKlipperResumeCommon()
                    self.G_ChangeChannelResumeFlag=False
                    self.G_PhrozenFluiddRespondInfo("+RESUME:2,%d" % self.G_ChangeChannelTimeoutNewChan)
            else:
                if self.G_AMSDevice1IfNormal==True or self.G_AMSDevice2IfNormal==True:
                    self.G_PhrozenFluiddRespondInfo("喷头无线材，有AMS多色，执行P8完整进料过程")
                    #lancaigang241106：
                    self.G_P0M2MAStartPrintFlag=0

                    #lancaigang250522：不允许M3断料检测
                    self.G_IfChangeFilaOngoing = True

                    #lancaigang241106：
                    self.Cmds_CmdP8(gcmd)
                    #lancaigang250619:检查AMS是否重新连接成功
                    self.Cmds_USBConnectErrorCheck()
                    #lancaigang241106:喷头成功进料
                    if self.G_P0M2MAStartPrintFlag==1:
                        #lancaigang250607:
                        self.G_PhrozenFluiddRespondInfo("可以恢复，STM32打印中快速报错")
                        self.G_KlipperQuickPause = True
                        # #lancaigang250427：
                        # if self.G_SerialPort1OpenFlag == True:
                        #     self.Cmds_AMSSerial1Send("AT+EBLOCKEND")
                        #     self.G_PhrozenFluiddRespondInfo("串口1-AMS结束计时缓冲器满时间")
                        # if self.G_SerialPort2OpenFlag == True:
                        #     self.Cmds_AMSSerial2Send("AT+EBLOCKEND")
                        #     self.G_PhrozenFluiddRespondInfo("串口2-AMS结束计时缓冲器满时间")
                        # self.G_ProzenToolhead.dwell(1.5)
                        if self.G_SerialPort1OpenFlag == True:
                            self.Cmds_AMSSerial1Send("AT+EBLOCKCHECK")
                            self.G_PhrozenFluiddRespondInfo("串口1-AMS开始计时缓冲器满时间")
                        if self.G_SerialPort2OpenFlag == True:
                            self.Cmds_AMSSerial2Send("AT+EBLOCKCHECK")
                            self.G_PhrozenFluiddRespondInfo("串口2-AMS开始计时缓冲器满时间")
                        #self.G_ProzenToolhead.dwell(1)
                        #lancaigang250522：
                        self.G_PhrozenFluiddRespondInfo("外部宏命令-PG109-升温")
                        command_string = """
                            PG109
                            """
                        self.G_PhrozenGCode.run_script_from_command(command_string)
                        self.G_PhrozenFluiddRespondInfo("外部宏命令-PG109-升温；command_string='%s'" % command_string)
                        #lancaigang251120：进入吐料，添加标志位，防止PG108吐料过程中喷头霍尔没有线材暂停，导致暂停位置在吐料区，恢复的时候会撞到吐料盒；
                        self.G_PG108Ingoing=1
                        #lancaigang250611：
                        self.G_PhrozenFluiddRespondInfo("外部宏命令-PG108-升温吐料擦嘴")
                        command_string = """
                            PG108
                            """
                        self.G_PhrozenGCode.run_script_from_command(command_string)
                        self.G_PG108Ingoing=0
                        #lancaigang250427：
                        if self.G_SerialPort1OpenFlag == True:
                            self.Cmds_AMSSerial1Send("AT+EBLOCKEND")
                            self.G_PhrozenFluiddRespondInfo("串口1-AMS结束计时缓冲器满时间")
                        if self.G_SerialPort2OpenFlag == True:
                            self.Cmds_AMSSerial2Send("AT+EBLOCKEND")
                            self.G_PhrozenFluiddRespondInfo("串口2-AMS结束计时缓冲器满时间")
                        if self.STM32ReprotPauseFlag == 1:
                            self.G_PhrozenFluiddRespondInfo("STM32上报已暂停，不能恢复")
                            #lancaigang240125：封装函数
                            #self.Cmds_PhrozenKlipperResumeCommon()
                            self.G_ChangeChannelResumeFlag=False
                            self.G_PhrozenFluiddRespondInfo("+RESUME:0,%d" % self.G_ChangeChannelTimeoutNewChan)
                        else:
                            self.G_PhrozenFluiddRespondInfo("喷头有线材，恢复")
                            #lancaigang240125：封装函数
                            self.Cmds_PhrozenKlipperResumeCommon()
                            self.G_ChangeChannelResumeFlag=False
                            self.G_PhrozenFluiddRespondInfo("+RESUME:2,%d" % self.G_ChangeChannelTimeoutNewChan)
                    else:
                        self.G_KlipperQuickPause = False
                        self.G_PhrozenFluiddRespondInfo("喷头无线材，M2MA模式继续暂停")
                        if self.G_KlipperIfPaused == False:
                            self.G_PhrozenGCode.run_script_from_command("SAVE_GCODE_STATE NAME=PAUSE")
                            self.G_PhrozenFluiddRespondInfo("[(cmds.python)]PAUSE")
                            self.G_PhrozenPrinterCancelPauseResume.send_pause_command()
                            self.G_ProzenToolhead.wait_moves()
                            self.G_KlipperIfPaused=True
                            #self.G_PhrozenFluiddRespondInfo("+PAUSE:b,%d" % self.G_ChangeChannelTimeoutNewChan)
                            self.G_PhrozenFluiddRespondInfo("+PAUSE:4,%d,%d" % (self.G_ChangeChannelTimeoutOldChan,self.G_ChangeChannelTimeoutNewChan))
                        else:
                            self.G_PhrozenFluiddRespondInfo("已经暂停，不用重复暂停")
                        self.G_ChangeChannelResumeFlag=False
                        self.G_PhrozenFluiddRespondInfo("+RESUME:0,%d" % self.G_ChangeChannelTimeoutNewChan)
                else:
                    self.G_KlipperQuickPause = False
                    self.G_PhrozenFluiddRespondInfo("喷头无线材，没有AMS多色，M2MA继续暂停")
                    self.G_PhrozenGCode.run_script_from_command("SAVE_GCODE_STATE NAME=PAUSE")
                    self.G_PhrozenFluiddRespondInfo("[(cmds.python)]PAUSE")
                    self.G_PhrozenPrinterCancelPauseResume.send_pause_command()
                    self.G_ProzenToolhead.wait_moves()
                    self.G_KlipperIfPaused=True
                    #self.G_PhrozenFluiddRespondInfo("+PAUSE:4,%d" % self.G_ChangeChannelTimeoutNewChan)
                    self.G_PhrozenFluiddRespondInfo("+PAUSE:4,%d,%d" % (self.G_ChangeChannelTimeoutOldChan,self.G_ChangeChannelTimeoutNewChan))
                    self.G_ChangeChannelResumeFlag=False
                    self.G_PhrozenFluiddRespondInfo("+RESUME:0,%d" % self.G_ChangeChannelTimeoutNewChan)







            return
            




        #=====lancaigang231220：M3单色，需要手动续料，只有喷头检测到线材才可以恢复打印
        # 单机M3断线处理模式
        if self.G_AMSDeviceWorkMode == AMS_WORK_MODE_FILA_RUNOUT:
            self.G_PhrozenFluiddRespondInfo("M3模式恢复")
            # #有线材才可以恢复打印
            # if self.G_ToolheadIfHaveFilaFlag:
            #     #lancaigang240412：单色模式，如果有AMS多色，需要恢复AMS
            #     if self.G_AMSDevice1IfNormal==True or self.G_AMSDevice2IfNormal==True:
            #         # #lancaigang240416:
            #         # if self.G_SerialPort1OpenFlag == True:
            #         #     self.Cmds_AMSSerial1Send("MA")
            #         #     self.G_PhrozenFluiddRespondInfo("串口1-MA")
            #         # #lancaigang241030:
            #         # elif self.G_SerialPort2OpenFlag == True:
            #         #     self.Cmds_AMSSerial2Send("MA")
            #         #     self.G_PhrozenFluiddRespondInfo("串口2-MA")

            #         # #lancaigang240115:延时1秒，防止粘包
            #         # time.sleep(2)

            #         # #lancaigang241030:FA用于
            #         # if self.G_SerialPort1OpenFlag == True:
            #         #     self.Cmds_AMSSerial1Send("FA")
            #         #     self.G_PhrozenFluiddRespondInfo("串口1-FA")
            #         # #lancaigang241030:
            #         # elif self.G_SerialPort2OpenFlag == True:
            #         #     self.Cmds_AMSSerial2Send("FA")
            #         #     self.G_PhrozenFluiddRespondInfo("串口2-FA")

            #         #lancaigang241106：执行P8全新进料过程，防止AMS异常断电或其他原因重启
            #         self.Cmds_CmdP8(gcmd)
            #         #lancaigang241106:喷头成功进料
            #         if self.G_P0M2MAStartPrintFlag==1:
            #             self.G_PhrozenFluiddRespondInfo("单色M3模式，AMS多色喷头有线材恢复")
            #             #lancaigang240125：封装函数
            #             self.Cmds_PhrozenKlipperResumeCommon()
            #         else:
            #             self.G_PhrozenFluiddRespondInfo("单机M3模式，有AMS多色喷头无线材继续暂停，请手动加料")
            #             self.G_PhrozenPrinterCancelPauseResume.send_pause_command()
            #             self.G_PhrozenFluiddRespondInfo("send_pause_command")
            #             #无线材继续暂停
            #             self.G_KlipperIfPaused=True
            #             self.G_PhrozenFluiddRespondInfo("+PAUSE:b,%d" % self.G_ChangeChannelTimeoutNewChan)
            #     else:
            #         self.G_PhrozenFluiddRespondInfo("单机M3模式，没有AMS多色喷头有线材恢复")
            #         # #lancaigang240411：手动挤料再恢复
            #         # command = """
            #         #     G90
            #         #     G1 X250 Y10 F10000 
            #         #     G91
            #         #     G1 Z10 F500
            #         #     G92 E0
            #         #     G1 E100 F500
            #         #     G92 E0
            #         #     G0
            #         # """
            #         # self.G_PhrozenGCode.run_script_from_command(command)
            #         # self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_PhrozenKlipperResume]command=%s" % command)
            #         self.G_PhrozenFluiddRespondInfo("调用外部宏-PG108-单色M3模式开始吐料")
            #         #lancaigang240407：调用了吐料功能，放在吐料之前，防止喷头进料又马上出料，导致执行多次命令报错
            #         self.P0M3FilaRunoutSpittingFinished = True#吐料完成，防止多次调用命令
            #         # command = """
            #         #     G90
            #         #     G1 X250 Y10 F10000 
            #         #     G91
            #         #     G1 Z10 F500
            #         #     G92 E0
            #         #     G1 E100 F500
            #         #     G92 E0
            #         #     G0
            #         # """
            #         # self.G_PhrozenGCode.run_script_from_command(command)
            #         # self.G_PhrozenFluiddRespondInfo("[(dev.python)Cmds_PhrozenKlipperResume]command=%s" % command)
            #         command_string = """
            #         PG108
            #         """
            #         self.G_PhrozenGCode.run_script_from_command(command_string)
            #         self.G_PhrozenFluiddRespondInfo("command_string='%s'" % command_string)


            #         #lancaigang240125：封装函数
            #         self.Cmds_PhrozenKlipperResumeCommon()

            #     # #lancaigang241106：
            #     # self.Cmds_CmdP8(gcmd)
            #     # self.Cmds_PhrozenKlipperResumeCommon()

            #     self.G_ChangeChannelResumeFlag=False
            #     self.G_PhrozenFluiddRespondInfo("+RESUME:2,%d" % self.G_ChangeChannelTimeoutNewChan)


            #     return
            

            # #没有线材继续暂停
            # else:
            #     #lancaigang240412：单色模式，如果有AMS多色，需要恢复AMS
            #     if self.G_AMSDevice1IfNormal==True or self.G_AMSDevice2IfNormal==True:
            #         # #lancaigang240416:
            #         # if self.G_SerialPort1OpenFlag == True:
            #         #     self.Cmds_AMSSerial1Send("MA")
            #         #     self.G_PhrozenFluiddRespondInfo("串口1-MA")
            #         # #lancaigang241030:
            #         # elif self.G_SerialPort2OpenFlag == True:
            #         #     self.Cmds_AMSSerial2Send("MA")
            #         #     self.G_PhrozenFluiddRespondInfo("串口2-MA")

            #         # #lancaigang240115:延时1秒，防止粘包
            #         # time.sleep(2)

            #         # self.G_PhrozenFluiddRespondInfo("单色M3模式，有AMS多色喷头无线材需要重新进新料")
            #         # #lancaigang240103：喷头无线材，需要重新进料，重新编排进料顺序，执行单色自动续料F8
            #         # #ttyUSB0串口发送：FA
            #         # #lancaigang240108：先不发送FA
            #         # #lancaigang240416:
            #         # if self.G_SerialPort1OpenFlag == True:
            #         #     self.Cmds_AMSSerial1Send("FA")
            #         #     self.G_PhrozenFluiddRespondInfo("串口1-FA")
            #         # #lancaigang241030:
            #         # elif self.G_SerialPort2OpenFlag == True:
            #         #     self.Cmds_AMSSerial2Send("FA")
            #         #     self.G_PhrozenFluiddRespondInfo("串口2-FA")

            #         # #lancaigang231229:封装函数
            #         # self.Cmds_MARetryInFila(gcmd)

            #         #lancaigang241106：执行P8全新进料过程，防止AMS异常断电或其他原因重启
            #         self.Cmds_CmdP8(gcmd)
            #         #lancaigang241106:喷头成功进料
            #         if self.G_P0M2MAStartPrintFlag==1:
            #             self.G_PhrozenFluiddRespondInfo("单色M3模式，AMS多色喷头有线材恢复")
            #             #lancaigang240125：封装函数
            #             self.Cmds_PhrozenKlipperResumeCommon()
            #         else:
            #             self.G_PhrozenFluiddRespondInfo("单机M3模式，有AMS多色喷头无线材继续暂停，请手动加料")
            #             self.G_PhrozenPrinterCancelPauseResume.send_pause_command()
            #             self.G_PhrozenFluiddRespondInfo("send_pause_command")
            #             #无线材继续暂停
            #             self.G_KlipperIfPaused=True
            #             self.G_PhrozenFluiddRespondInfo("+PAUSE:b,%d" % self.G_ChangeChannelTimeoutNewChan)

            #     else:
            #         self.G_PhrozenFluiddRespondInfo("单机M3模式，没有AMS多色喷头无线材继续暂停，请手动加料")
            #         self.G_PhrozenPrinterCancelPauseResume.send_pause_command()
            #         self.G_PhrozenFluiddRespondInfo("send_pause_command")
            #         #无线材继续暂停
            #         self.G_KlipperIfPaused=True
            #         self.G_PhrozenFluiddRespondInfo("+PAUSE:b,%d" % self.G_ChangeChannelTimeoutNewChan)



            #有线材才可以恢复打印
            if self.G_ToolheadIfHaveFilaFlag:
                #lancaigang240412：M3模式，如果有AMS多色，需要恢复AMS
                if self.G_AMSDevice1IfNormal==True or self.G_AMSDevice2IfNormal==True:
                    # self.G_PhrozenFluiddRespondInfo("喷头有线材，有AMS多色，不用回退线材，需要发送命令给STM32恢复最后状态")
                    # #self.Cmds_CmdP8(gcmd)
                    # if self.G_SerialPort1OpenFlag == True:
                    #     self.Cmds_AMSSerial1Send("FA")
                    #     self.G_PhrozenFluiddRespondInfo("串口1发送FA")
                    # elif self.G_SerialPort2OpenFlag == True:
                    #     self.Cmds_AMSSerial2Send("FA")
                    #     self.G_PhrozenFluiddRespondInfo("串口2发送FA")
                    # self.G_PhrozenFluiddRespondInfo("喷头有线材，恢复不用回退再进料")
                    self.G_PhrozenFluiddRespondInfo("喷头有线材，有AMS多色，但還是执行P8完整进料过程，防止切綫異常情況")
                    self.G_P0M2MAStartPrintFlag=0

                    #lancaigang250522：不允许M3断料检测
                    self.G_IfChangeFilaOngoing = True

                    self.Cmds_CmdP8(gcmd)
                    #lancaigang250619:检查AMS是否重新连接成功
                    self.Cmds_USBConnectErrorCheck()
                    # if self.G_SerialPort1OpenFlag == True:
                    #     self.Cmds_AMSSerial1Send("FA")
                    #     self.G_PhrozenFluiddRespondInfo("串口1发送FA")
                    # elif self.G_SerialPort2OpenFlag == True:
                    #     self.Cmds_AMSSerial2Send("FA")
                    #     self.G_PhrozenFluiddRespondInfo("串口2发送FA")
                    #lancaigang241106:喷头成功进料
                    if self.G_P0M2MAStartPrintFlag==1:
                        #lancaigang250607:
                        self.G_PhrozenFluiddRespondInfo("可以恢复，STM32打印中快速报错")
                        self.G_KlipperQuickPause = True
                        # #lancaigang250427：
                        # if self.G_SerialPort1OpenFlag == True:
                        #     self.Cmds_AMSSerial1Send("AT+EBLOCKEND")
                        #     self.G_PhrozenFluiddRespondInfo("串口1-AMS结束计时缓冲器满时间")
                        # if self.G_SerialPort2OpenFlag == True:
                        #     self.Cmds_AMSSerial2Send("AT+EBLOCKEND")
                        #     self.G_PhrozenFluiddRespondInfo("串口2-AMS结束计时缓冲器满时间")
                        # self.G_ProzenToolhead.dwell(1.5)
                        #lancaigang250522：
                        # self.G_PhrozenFluiddRespondInfo("外部宏命令-PG109-升温")
                        # command_string = """
                        #     PG109
                        #     """
                        # self.G_PhrozenGCode.run_script_from_command(command_string)
                        # self.G_PhrozenFluiddRespondInfo("外部宏命令-PG109-升温；command_string='%s'" % command_string)
                        # if self.G_SerialPort1OpenFlag == True:
                        #     self.Cmds_AMSSerial1Send("AT+RESTORE")
                        #     self.G_PhrozenFluiddRespondInfo("串口1-恢复")
                        # if self.G_SerialPort2OpenFlag == True:
                        #     self.Cmds_AMSSerial2Send("AT+RESTORE")
                        #     self.G_PhrozenFluiddRespondInfo("串口2-恢复")
                        # self.G_PhrozenFluiddRespondInfo("喷头有线材，恢复")
                        # #lancaigang250611：
                        # self.G_PhrozenFluiddRespondInfo("外部宏命令-PG108-升温吐料擦嘴")
                        # command_string = """
                        #     PG108
                        #     """
                        # self.G_PhrozenGCode.run_script_from_command(command_string)
                        # #lancaigang240125：封装函数
                        # self.Cmds_PhrozenKlipperResumeCommon()
                        if self.G_SerialPort1OpenFlag == True:
                            self.Cmds_AMSSerial1Send("AT+EBLOCKCHECK")
                            self.G_PhrozenFluiddRespondInfo("串口1-AMS开始计时缓冲器满时间")
                        if self.G_SerialPort2OpenFlag == True:
                            self.Cmds_AMSSerial2Send("AT+EBLOCKCHECK")
                            self.G_PhrozenFluiddRespondInfo("串口2-AMS开始计时缓冲器满时间")
                        #self.G_ProzenToolhead.dwell(1)
                        #lancaigang250522：
                        self.G_PhrozenFluiddRespondInfo("外部宏命令-PG109-升温")
                        command_string = """
                            PG109
                            """
                        self.G_PhrozenGCode.run_script_from_command(command_string)
                        self.G_PhrozenFluiddRespondInfo("外部宏命令-PG109-升温；command_string='%s'" % command_string)
                        #lancaigang251120：进入吐料，添加标志位，防止PG108吐料过程中喷头霍尔没有线材暂停，导致暂停位置在吐料区，恢复的时候会撞到吐料盒；
                        self.G_PG108Ingoing=1
                        #lancaigang250611：
                        self.G_PhrozenFluiddRespondInfo("外部宏命令-PG108-升温吐料擦嘴")
                        command_string = """
                            PG108
                            """
                        self.G_PhrozenGCode.run_script_from_command(command_string)
                        self.G_PG108Ingoing=0
                        #lancaigang250427：
                        if self.G_SerialPort1OpenFlag == True:
                            self.Cmds_AMSSerial1Send("AT+EBLOCKEND")
                            self.G_PhrozenFluiddRespondInfo("串口1-AMS结束计时缓冲器满时间")
                        if self.G_SerialPort2OpenFlag == True:
                            self.Cmds_AMSSerial2Send("AT+EBLOCKEND")
                            self.G_PhrozenFluiddRespondInfo("串口2-AMS结束计时缓冲器满时间")
                        if self.STM32ReprotPauseFlag == 1:
                            self.G_PhrozenFluiddRespondInfo("STM32上报已暂停，不能恢复")
                            #lancaigang240125：封装函数
                            #self.Cmds_PhrozenKlipperResumeCommon()
                            self.G_ChangeChannelResumeFlag=False
                            self.G_PhrozenFluiddRespondInfo("+RESUME:0,%d" % self.G_ChangeChannelTimeoutNewChan)
                        else:
                            self.G_PhrozenFluiddRespondInfo("喷头有线材，恢复")
                            #lancaigang240125：封装函数
                            self.Cmds_PhrozenKlipperResumeCommon()
                            self.G_ChangeChannelResumeFlag=False
                            self.G_PhrozenFluiddRespondInfo("+RESUME:2,%d" % self.G_ChangeChannelTimeoutNewChan)
                    else:
                        self.G_KlipperQuickPause = False
                        self.G_PhrozenFluiddRespondInfo("喷头无线材，M3模式继续暂停")
                        if self.G_KlipperIfPaused == False:
                            self.G_PhrozenGCode.run_script_from_command("SAVE_GCODE_STATE NAME=PAUSE")
                            self.G_PhrozenFluiddRespondInfo("[(cmds.python)]PAUSE")
                            self.G_PhrozenPrinterCancelPauseResume.send_pause_command()
                            self.G_ProzenToolhead.wait_moves()
                            self.G_KlipperIfPaused=True
                            #self.G_PhrozenFluiddRespondInfo("+PAUSE:b,%d" % self.G_ChangeChannelTimeoutNewChan)
                            self.G_PhrozenFluiddRespondInfo("+PAUSE:4,%d,%d" % (self.G_ChangeChannelTimeoutOldChan,self.G_ChangeChannelTimeoutNewChan))
                        else:
                            self.G_PhrozenFluiddRespondInfo("已经暂停，不用重复暂停")
                        self.G_ChangeChannelResumeFlag=False
                        self.G_PhrozenFluiddRespondInfo("+RESUME:0,%d" % self.G_ChangeChannelTimeoutNewChan)
                else:
                    self.G_KlipperQuickPause = False
                    self.G_PhrozenFluiddRespondInfo("喷头有线材，没有有AMS多色，直接恢复")
                    self.G_PhrozenFluiddRespondInfo("喷头有线材，恢复不用回退再进料")
                    #lancaigang250522：
                    self.G_PhrozenFluiddRespondInfo("外部宏命令-PG109-升温")
                    command_string = """
                        PG109
                        """
                    self.G_PhrozenGCode.run_script_from_command(command_string)
                    self.G_PhrozenFluiddRespondInfo("外部宏命令-PG109-升温；command_string='%s'" % command_string)
                    #lancaigang251120：进入吐料，添加标志位，防止PG108吐料过程中喷头霍尔没有线材暂停，导致暂停位置在吐料区，恢复的时候会撞到吐料盒；
                    self.G_PG108Ingoing=1
                    #lancaigang250409：恢复的时候再吐料
                    command_string = """
                    PG108
                    """
                    self.G_PhrozenGCode.run_script_from_command(command_string)
                    self.G_PG108Ingoing=0
                    self.G_PhrozenFluiddRespondInfo("command_string='%s'" % command_string)
                    self.G_PhrozenFluiddRespondInfo("吐料完成，喷头检测到有线材恢复打印")
                    #lancaigang240125：封装函数
                    self.Cmds_PhrozenKlipperResumeCommon()
                    self.G_ChangeChannelResumeFlag=False
                    self.G_PhrozenFluiddRespondInfo("+RESUME:2,%d" % self.G_ChangeChannelTimeoutNewChan)
            else:
                if self.G_AMSDevice1IfNormal==True or self.G_AMSDevice2IfNormal==True:
                    self.G_PhrozenFluiddRespondInfo("喷头无线材，有AMS多色，执行P8完整进料过程")
                    #lancaigang241106：
                    self.G_P0M2MAStartPrintFlag=0

                    #lancaigang250522：不允许M3断料检测
                    self.G_IfChangeFilaOngoing = True

                    #lancaigang241106：
                    self.Cmds_CmdP8(gcmd)
                    #lancaigang250619:检查AMS是否重新连接成功
                    self.Cmds_USBConnectErrorCheck()
                    #lancaigang241106:喷头成功进料
                    if self.G_P0M2MAStartPrintFlag==1:
                        #lancaigang250607:
                        self.G_PhrozenFluiddRespondInfo("可以恢复，STM32打印中快速报错")
                        self.G_KlipperQuickPause = True
                        # #lancaigang250427：
                        # if self.G_SerialPort1OpenFlag == True:
                        #     self.Cmds_AMSSerial1Send("AT+EBLOCKEND")
                        #     self.G_PhrozenFluiddRespondInfo("串口1-AMS结束计时缓冲器满时间")
                        # if self.G_SerialPort2OpenFlag == True:
                        #     self.Cmds_AMSSerial2Send("AT+EBLOCKEND")
                        #     self.G_PhrozenFluiddRespondInfo("串口2-AMS结束计时缓冲器满时间")
                        # self.G_ProzenToolhead.dwell(1.5)
                        if self.G_SerialPort1OpenFlag == True:
                            self.Cmds_AMSSerial1Send("AT+EBLOCKCHECK")
                            self.G_PhrozenFluiddRespondInfo("串口1-AMS开始计时缓冲器满时间")
                        if self.G_SerialPort2OpenFlag == True:
                            self.Cmds_AMSSerial2Send("AT+EBLOCKCHECK")
                            self.G_PhrozenFluiddRespondInfo("串口2-AMS开始计时缓冲器满时间")
                        #self.G_ProzenToolhead.dwell(1)
                        #lancaigang250522：
                        self.G_PhrozenFluiddRespondInfo("外部宏命令-PG109-升温")
                        command_string = """
                            PG109
                            """
                        self.G_PhrozenGCode.run_script_from_command(command_string)
                        self.G_PhrozenFluiddRespondInfo("外部宏命令-PG109-升温；command_string='%s'" % command_string)
                        #lancaigang251120：进入吐料，添加标志位，防止PG108吐料过程中喷头霍尔没有线材暂停，导致暂停位置在吐料区，恢复的时候会撞到吐料盒；
                        self.G_PG108Ingoing=1
                        #lancaigang250611：
                        self.G_PhrozenFluiddRespondInfo("外部宏命令-PG108-升温吐料擦嘴")
                        command_string = """
                            PG108
                            """
                        self.G_PhrozenGCode.run_script_from_command(command_string)
                        self.G_PG108Ingoing=0
                        #lancaigang250427：
                        if self.G_SerialPort1OpenFlag == True:
                            self.Cmds_AMSSerial1Send("AT+EBLOCKEND")
                            self.G_PhrozenFluiddRespondInfo("串口1-AMS结束计时缓冲器满时间")
                        if self.G_SerialPort2OpenFlag == True:
                            self.Cmds_AMSSerial2Send("AT+EBLOCKEND")
                            self.G_PhrozenFluiddRespondInfo("串口2-AMS结束计时缓冲器满时间")
                        if self.STM32ReprotPauseFlag == 1:
                            self.G_PhrozenFluiddRespondInfo("STM32上报已暂停，不能恢复")
                            #lancaigang240125：封装函数
                            #self.Cmds_PhrozenKlipperResumeCommon()
                            self.G_ChangeChannelResumeFlag=False
                            self.G_PhrozenFluiddRespondInfo("+RESUME:0,%d" % self.G_ChangeChannelTimeoutNewChan)
                        else:
                            self.G_PhrozenFluiddRespondInfo("喷头有线材，恢复")
                            #lancaigang240125：封装函数
                            self.Cmds_PhrozenKlipperResumeCommon()
                            self.G_ChangeChannelResumeFlag=False
                            self.G_PhrozenFluiddRespondInfo("+RESUME:2,%d" % self.G_ChangeChannelTimeoutNewChan)
                    else:
                        self.G_KlipperQuickPause = False
                        self.G_PhrozenFluiddRespondInfo("喷头无线材，M3模式继续暂停")
                        if self.G_KlipperIfPaused == False:
                            self.G_PhrozenGCode.run_script_from_command("SAVE_GCODE_STATE NAME=PAUSE")
                            self.G_PhrozenFluiddRespondInfo("[(cmds.python)]PAUSE")
                            self.G_PhrozenPrinterCancelPauseResume.send_pause_command()
                            self.G_ProzenToolhead.wait_moves()
                            #无线材继续暂停
                            self.G_KlipperIfPaused=True
                            #self.G_PhrozenFluiddRespondInfo("+PAUSE:b,%d" % self.G_ChangeChannelTimeoutNewChan)
                            self.G_PhrozenFluiddRespondInfo("+PAUSE:4,%d,%d" % (self.G_ChangeChannelTimeoutOldChan,self.G_ChangeChannelTimeoutNewChan))
                        else:
                            self.G_PhrozenFluiddRespondInfo("已经暂停，不用重复暂停")
                        self.G_ChangeChannelResumeFlag=False
                        self.G_PhrozenFluiddRespondInfo("+RESUME:0,%d" % self.G_ChangeChannelTimeoutNewChan)
                            
                else:
                    self.G_KlipperQuickPause = False
                    self.G_PhrozenFluiddRespondInfo("喷头无线材，没有AMS多色，M3继续暂停")
                    self.G_PhrozenGCode.run_script_from_command("SAVE_GCODE_STATE NAME=PAUSE")
                    self.G_PhrozenFluiddRespondInfo("[(cmds.python)]PAUSE")
                    self.G_PhrozenPrinterCancelPauseResume.send_pause_command()
                    self.G_ProzenToolhead.wait_moves()
                    #无线材继续暂停
                    self.G_KlipperIfPaused=True
                    #self.G_PhrozenFluiddRespondInfo("+PAUSE:b,%d" % self.G_ChangeChannelTimeoutNewChan)
                    self.G_PhrozenFluiddRespondInfo("+PAUSE:b,%d,%d" % (self.G_ChangeChannelTimeoutOldChan,self.G_ChangeChannelTimeoutNewChan))
                    self.G_ChangeChannelResumeFlag=False
                    self.G_PhrozenFluiddRespondInfo("+RESUME:0,%d" % self.G_ChangeChannelTimeoutNewChan)




            # self.G_ChangeChannelResumeFlag=False
            # self.G_PhrozenFluiddRespondInfo("+RESUME:2,%d" % self.G_ChangeChannelTimeoutNewChan)


            return






        # #lancaigang240319：喷头上有线材才特殊补料H?
        # if self.G_ToolheadIfHaveFilaFlag:
        #     self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_PhrozenKlipperResume]喷头上有线材")
        #     #lancaigang240319：切线之前准备动作
        #     #self.Cmds_MoveToCutFilaPrepare()
        #     self.Cmds_AMSSerial1Send("H%d" % self.G_ChangeChannelTimeoutNewChan)
        #     self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_PhrozenKlipperResume]切线之前特殊补料状态: H%d" % self.G_ChangeChannelTimeoutNewChan)
        #     time.sleep(1)


        # #lancaigang240423：恢复的时候，先回抽线材
        # self.Cmds_AMSSerial1Send("G%d" % self.G_ChangeChannelTimeoutNewChan)
        # self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_PhrozenKlipperResume]G%d" % self.G_ChangeChannelTimeoutNewChan)
        # self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_PhrozenKlipperResume]AMS先回退一段距离，然后喷头再回抽mm: G%d" % self.G_ChangeChannelTimeoutNewChan)
        # self.G_PauseTriggerWhileChangeChannelFlag=False




        self.G_PhrozenFluiddRespondInfo("外部宏命令-PG104-获取换线之前全局变量")
        command_string = """
            PG104
            """
        self.G_PhrozenGCode.run_script_from_command(command_string)
        self.G_PhrozenFluiddRespondInfo("外部宏命令-PG104-获取换线之前全局变量；command_string='%s'" % command_string)
        self.IfDoPG102Flag=True


        self.G_PhrozenFluiddRespondInfo("外部宏命令-PG101-回抽")
        command_string = """
            PG101
            """
        self.G_PhrozenGCode.run_script_from_command(command_string)
        self.G_PhrozenFluiddRespondInfo("外部宏命令-到指定待料区位置等待吐料；command_string='%s'" % command_string)
        self.IfDoPG102Flag=True





        #lancaigang240328：手动命令不执行吐料
        if self.ManualCmdFlag==True:
            self.G_PhrozenFluiddRespondInfo("外部宏命令-PG106；手动命令，不执行吐料功能")
        else:
            #lancaigang240319：切完后，先吐掉残留喷头的线材，防止切成米粒
            self.G_PhrozenFluiddRespondInfo("外部宏命令-PG106；切线之前，先吐掉残留喷头的线材，防止切成米粒")
            self.PG102Flag=True
            self.G_PhrozenFluiddRespondInfo("self.Flag=True")
            command_string = """
            PG106
            """
            self.G_PhrozenGCode.run_script_from_command(command_string)
            self.G_PhrozenFluiddRespondInfo("command_string='%s'" % command_string)
            self.PG102Flag=False
            self.G_PhrozenFluiddRespondInfo("self.Flag=False")

        #lancaigang241012：执行后面的PG102
        self.IfDoPG102Flag=True

        #lancaigang250717:先吐掉残料，缓冲器并惯性下压一小节
        self.G_ProzenToolhead.dwell(8)

        #lancaigang250519:
        self.G_PhrozenFluiddRespondInfo("外部宏命令-PRZ_WIPEMOUTH")
        command_string = """
            PRZ_WIPEMOUTH
            """
        self.G_PhrozenGCode.run_script_from_command(command_string)
        self.G_PhrozenFluiddRespondInfo("外部宏命令-到指定待料区位置；command_string='%s'" % command_string)




        #lancaigang20231205：切刀切线
        #lancaigang231215：Z轴上升后必须记得下降
        self.Cmds_MoveToCutFilaAction(gcmd)




        #lancaigang231216：如果z轴抬升没有被降下，需要降下再暂停
        if self.G_IfZPositionLiftUpFlag==True:
            command_string = """
                G90
                G91
                G1 Z-%f F8000
                """ % (
                self.G_AMSFilaCutZPositionLiftingUp,
            )
            self.G_PhrozenGCode.run_script_from_command(command_string)
            self.G_IfZPositionLiftUpFlag = False
            self.G_PhrozenFluiddRespondInfo("Z轴下拉降低；command_string='%s'" % command_string)




        #lancaigang240226：切线后AMS主板回退线材，延时后喷头回抽20mm
        #time.sleep(2)
        self.G_ProzenToolhead.dwell(0.5)



        # #lancaigang240328：手动命令不执行吐料
        # if self.ManualCmdFlag==True:
        #     self.G_PhrozenFluiddRespondInfo("外部宏命令-PG106；手动命令，不执行吐料功能")
        # else:
        #     #lancaigang240319：切完后，先吐掉残留喷头的线材，防止切成米粒
        #     self.G_PhrozenFluiddRespondInfo("外部宏命令-PG106；切线之前，先吐掉残留喷头的线材，防止切成米粒")
        #     self.PG102Flag=True
        #     self.G_PhrozenFluiddRespondInfo("self.Flag=True")
        #     command_string = """
        #     PG106
        #     """
        #     self.G_PhrozenGCode.run_script_from_command(command_string)
        #     self.G_PhrozenFluiddRespondInfo("command_string='%s'" % command_string)
        #     self.PG102Flag=False
        #     self.G_PhrozenFluiddRespondInfo("self.Flag=False")

        # #lancaigang241012：执行后面的PG102
        # self.IfDoPG102Flag=True

        # #lancaigang240906：新的AMS，切线后，回退上一次通道一段距离
        # #lancaigang20231013：stm32换料
        # #lancaigang231129：stm32内部换料跟klipper换料分开，导致stm32内部强制换料，而klipper如果喷头切线异常而无法退料，导致klipper异常空打印
        # self.Cmds_AMSSerial1Send("G%d" % self.G_ChangeChannelTimeoutOldChan)
        # self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_PhrozenKlipperResume]G%d" % self.G_ChangeChannelTimeoutOldChan)
        # self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_PhrozenKlipperResume]AMS旧通道先回退一段距离: G%d" % self.G_ChangeChannelTimeoutOldChan)
        
        # # #lancaigang240906：在上位机延时等待，stm32只负责单纯的换通道和打印补料
        # # for i in range(5):#
        # #     self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_P1TnManualChangeChannel]等待旧通道回退")
        # #     self.G_ProzenToolhead.dwell(1.0)
        # #     self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_P1TnManualChangeChannel]i=%d;T=%d" % (i,chan))

        #lancaigang250619:检查AMS是否重新连接成功
        self.Cmds_USBConnectErrorCheck()
        #lancaigang240416:
        if self.G_SerialPort1OpenFlag == True:
            #lancaigang240913：恢复的时候，目的是重复进线，可以全部回退所有线一段距离，防止旧通道回退异常，新通道进料异常
            self.Cmds_AMSSerial1Send("AP")
            self.G_PhrozenFluiddRespondInfo("串口1发送命令: AP；所有通道线材回退一段距离")
        #lancaigang241030:
        if self.G_SerialPort2OpenFlag == True:
            self.Cmds_AMSSerial2Send("AP")
            self.G_PhrozenFluiddRespondInfo("串口2发送命令: AP；所有通道线材回退一段距离")


        # self.Cmds_AMSSerial1Send("G%d" % self.G_ChangeChannelTimeoutOldChan)
        # self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_PhrozenKlipperResume]G%d" % self.G_ChangeChannelTimeoutOldChan)
        # self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_PhrozenKlipperResume]AMS旧通道先回退一段距离: G%d" % self.G_ChangeChannelTimeoutOldChan)
        
        # self.G_ProzenToolhead.dwell(5)


        # self.Cmds_AMSSerial1Send("G%d" % self.G_ChangeChannelTimeoutNewChan)
        # self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_PhrozenKlipperResume]G%d" % self.G_ChangeChannelTimeoutNewChan)
        # self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_PhrozenKlipperResume]AMS新通道先回退一段距离: G%d" % self.G_ChangeChannelTimeoutNewChan)
        
        # self.G_ProzenToolhead.dwell(5)


        # self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_PhrozenKlipperResume]外部宏命令-PG101")
        # command_string = """
        #     PG101
        #     """
        # self.G_PhrozenGCode.run_script_from_command(command_string)
        # self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_PhrozenKlipperResume]外部宏命令-到指定待料区位置等待吐料；command_string='%s'" % command_string)
        # self.IfDoPG102Flag=True



        #lancaigang231216：如果换料期间点击暂停，刚好换料期间抬升了z轴，到执行暂停时，把z轴高度也保存了，导致整体高度异常
        #lancaigang231216：如果z轴抬升没有被降下，需要降下再暂停
        if self.G_IfZPositionLiftUpFlag==True:
            command_string = """
                G90
                G91
                G1 Z-%f F8000
                """ % (
                self.G_AMSFilaCutZPositionLiftingUp,
            )
            self.G_PhrozenGCode.run_script_from_command(command_string)
            self.G_IfZPositionLiftUpFlag = False
            self.G_PhrozenFluiddRespondInfo("Z轴下拉降低；command_string='%s'" % command_string)

        #lancaigang240920：恢复回退线材后，清标志位
        #self.ToolheadCutFlag=False

        #lancaigang250519:
        self.G_PhrozenFluiddRespondInfo("外部宏命令-PRZ_CUT_WAITINGAREA")
        command_string = """
            PRZ_CUT_WAITINGAREA
            """
        self.G_PhrozenGCode.run_script_from_command(command_string)
        self.G_PhrozenFluiddRespondInfo("外部宏命令-到指定待料区位置；command_string='%s'" % command_string)


        #lancaigang240913：把延時放到外面
        self.G_ProzenToolhead.dwell(6)
        #lancaigang240911：G命令之后延时5秒检查喷头是否有线材
        #lancaigang231201：检查切线后旧通道线材是否正常退料，不正常则暂停
        self.Cmds_CutFilaIfNormalCheck()
        #lancaigang240912：本身就是暂停了，恢复的时候会检测到就是暂停，这里会导致直接返回
        #lancaigang250109:因为多色MC恢复需要重新进料。所以不能暂停返回
        # if self.G_KlipperIfPaused == True:
        #     self.G_PhrozenFluiddRespondInfo("[(cmds.python)]切线6秒了喷头还检测到线材，切刀异常了，请检查切刀，暂停klipper打印")
        #     #Lo_ChangeChannelIfSuccess = False
        #     return
        Lo_PauseStatus=self.G_PhrozenPrinterCancelPauseResume.get_status(None)
        self.G_PhrozenFluiddRespondInfo("当前暂停状态-Lo_PauseStatus='%s'" % Lo_PauseStatus)
        self.G_PhrozenFluiddRespondInfo("Lo_PauseStatus['is_paused']='%s'" % Lo_PauseStatus['is_paused'])
        #// 当前暂停状态-Lo_PauseStatus='{'is_paused': True}'
        if Lo_PauseStatus['is_paused'] == True:
            self.G_PhrozenFluiddRespondInfo("已是暂停状态")
        else:
            self.G_PhrozenFluiddRespondInfo("未暂停状态")


        #lancaigang250712：
        if self.G_ChangeChannelTimeoutOldChan==-1 and self.G_ChangeChannelTimeoutNewChan==-1:
            self.G_PhrozenFluiddRespondInfo("多色打印，准备打印的时候暂停，没法记录新旧通道，如果P2A1正常，则直接恢复，等待下一个换色命令")
            if self.G_ToolheadIfHaveFilaFlag == False:
                self.G_PhrozenFluiddRespondInfo("喷头回退过了5秒喷头未检测到线材，说明线材已经回退了，特殊情况恢复；")
                #lancaigang240125：封装函数
                self.Cmds_PhrozenKlipperResumeCommon()
                self.G_ChangeChannelResumeFlag=False
                self.G_ChangeChannelFirstFilaFlag=True
                self.G_IfChangeFilaOngoing= False

                self.G_PhrozenFluiddRespondInfo("return")
                return



        #lancaigang250102：恢复的时候，开启风扇，防止风扇不转情况
        #self.G_ProzenToolhead.dwell(0.5)
        self.G_PrintCountNum=self.G_PrintCountNum-1


        #lancaigang231115：更改业务逻辑；恢复并续打之前通道
        #喷头有线材
        if self.G_ToolheadIfHaveFilaFlag:
            self.G_PhrozenFluiddRespondInfo("喷头有线材，可以恢复打印")
            #lancaigang240323：先换线，再恢复成第1次通道处理
            self.Cmds_P1CnAutoChangeChannel(self.G_ChangeChannelTimeoutNewChan, self.G_ChangeChannelTimeoutNewGcmd)
            #lancaigang240325：换料成功，可以进行数据恢复
            if self.G_MCModeCanResumeFlag == True:
                self.G_PhrozenFluiddRespondInfo("换料成功，可以恢复数据")
                #lancaigang240125：封装函数
                self.Cmds_PhrozenKlipperResumeCommon()

                self.G_ProzenToolhead.dwell(1)
                self.G_ChangeChannelResumeFlag=False
                self.G_PhrozenFluiddRespondInfo("+RESUME:2,%d" % self.G_ChangeChannelTimeoutNewChan)
            else:
                self.G_PhrozenFluiddRespondInfo("换料不成功，不可以恢复数据")

                #lancaigang250527：暂停待料区
                self.G_PhrozenFluiddRespondInfo("开始调用外部宏命令-PRZ_PAUSE_WAITINGAREA")
                command = """
                PRZ_PAUSE_WAITINGAREA
                """
                self.G_PhrozenGCode.run_script_from_command(command)
                self.G_PhrozenFluiddRespondInfo("结束调用外部宏命令:command=%s" % (command))
                
                self.G_ProzenToolhead.dwell(1)
                self.G_ChangeChannelResumeFlag=False
                self.G_PhrozenFluiddRespondInfo("+RESUME:0,%d" % self.G_ChangeChannelTimeoutNewChan)

        #喷头没有线材
        else:
            self.G_PhrozenFluiddRespondInfo("喷头没有线材，重新执行换料操作")
            #lancaigang240323：先换线，再恢复成第1次通道处理
            self.Cmds_P1CnAutoChangeChannel(self.G_ChangeChannelTimeoutNewChan, self.G_ChangeChannelTimeoutNewGcmd)
            #lancaigang240325：换料成功，可以进行数据恢复
            if self.G_MCModeCanResumeFlag == True:
                self.G_PhrozenFluiddRespondInfo("换料成功，可以恢复数据")
                #lancaigang240125：封装函数
                self.Cmds_PhrozenKlipperResumeCommon()

                self.G_ProzenToolhead.dwell(1)
                self.G_ChangeChannelResumeFlag=False
                self.G_PhrozenFluiddRespondInfo("+RESUME:2,%d" % self.G_ChangeChannelTimeoutNewChan)

            else:
                self.G_PhrozenFluiddRespondInfo("换料不成功，不可以恢复数据")

                #lancaigang250527：暂停待料区
                self.G_PhrozenFluiddRespondInfo("开始调用外部宏命令-PRZ_PAUSE_WAITINGAREA")
                command = """
                PRZ_PAUSE_WAITINGAREA
                """
                self.G_PhrozenGCode.run_script_from_command(command)
                self.G_PhrozenFluiddRespondInfo("结束调用外部宏命令:command=%s" % (command))

                #lancaigang240509：屏蔽
                # #lancaigang240426：恢复失败，需要上报暂停
                # if len(self.G_PauseToLCDString)==0:
                #     #lancaigang0429：防止多次报暂停
                #     #self.G_PhrozenFluiddRespondInfo(self.G_PauseToLCDString)
                #     self.G_PhrozenFluiddRespondInfo("+PAUSE:4,%d" % self.G_ChangeChannelTimeoutNewChan)
                self.G_ProzenToolhead.dwell(1)
                self.G_ChangeChannelResumeFlag=False
                self.G_PhrozenFluiddRespondInfo("+RESUME:0,%d" % self.G_ChangeChannelTimeoutNewChan)




        #lancaigang250102：恢复的时候，开启风扇，防止风扇不转情况
        #self.G_ProzenToolhead.dwell(0.5)
        self.G_PrintCountNum=self.G_PrintCountNum-1
        #lancaigang250102:打印换料次数计算；第1次换料不开风扇
        if self.G_PrintCountNum<=0:
            self.G_PrintCountNum=0
            self.G_PhrozenFluiddRespondInfo("恢复结束，第1次换料不开风扇")
        else:
            command_string = """
                M106 S255
                """
            self.G_PhrozenGCode.run_script_from_command(command_string)
            self.G_PhrozenFluiddRespondInfo("恢复结束，开启风扇；command_string='%s'" % command_string)
            self.G_PhrozenFluiddRespondInfo("self.G_PrintCountNum='%d'" % self.G_PrintCountNum)
        #self.G_ProzenToolhead.dwell(0.5)


    ####################################
    #函数名称：
    #输入参数：
    #返 回 值:
    #功能描述：蓝才刚-20230830
    ####################################
    def Cmds_PhrozenKlipperPauseScreen(self, gcmd):
        _ = gcmd

        self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_PhrozenKlipperPauseScreen]")
            # // lancaigang231202:+PAUSE:1,ch;1-进料用完卡线，暂停
            # // lancaigang231202:+PAUSE:2,ch;2-暂停ACK
            # // lancaigang231204:+PAUSE:3,ch;3-新通道打印过程中慢速补料超时10s，暂停
            # // lancaigang231205:+PAUSE:4,ch;4-新通道进料超时50s，暂停
            # // lancaigang231205:+PAUSE:5,ch;5-新通道打印过程中快速补料超时10s，暂停
            # // lancaigang231205:+PAUSE:6,ch;6-入口位到停靠位超时10s，暂停
            # // lancaigang231205:+PAUSE:7,ch;7-缓冲器满状态超时30s，暂停
            # // lancaigang231205:+PAUSE:8,ch;8-喷头切刀或传感器异常，暂停
            # // lancaigang231205:+PAUSE:9,ch;9-换料超时120s，暂停
            # // lancaigang231202:+PAUSE:a,ch;a-停靠位到缓冲器入口超时10s，暂停
            # // lancaigang231202:+PAUSE:b,ch;b-预留
            # // lancaigang231202:+PAUSE:c,ch;c-预留
            # // lancaigang231202:+PAUSE:d,ch;d-预留
            # // lancaigang231202:+PAUSE:10,ch;10-触摸屏或fluidd网页主动暂停
        #klipper主动暂停
        self.G_PhrozenFluiddRespondInfo("=====PAUSE=====")
        self.G_PhrozenFluiddRespondInfo("=====PAUSE=====self.G_ChangeChannelTimeoutOldChan=%d" % self.G_ChangeChannelTimeoutOldChan)
        self.G_PhrozenFluiddRespondInfo("=====PAUSE=====self.G_ChangeChannelTimeoutNewChan=%d" % self.G_ChangeChannelTimeoutNewChan)

        #lancaigang250527：暂停快速执行
        self.G_KlipperQuickPause = False
        
        #lancaigang250516：吐料中不让暂停
        if self.PG102Flag==True:
            self.G_PhrozenFluiddRespondInfo("吐料中，不让暂停")
            #self.G_PhrozenFluiddRespondInfo("+PAUSE:10,%d,%d" % (self.G_ChangeChannelTimeoutOldChan,self.G_ChangeChannelTimeoutNewChan))
            return



        #lancaigang231228：只有MC模式才允许Z轴动作
        if self.G_AMSDeviceWorkMode == AMS_WORK_MODE_MC:
            #lancaigang231216：如果换料期间点击暂停，刚好换料期间抬升了z轴，到执行暂停时，把z轴高度也保存了，导致整体高度异常
            #lancaigang231216：如果z轴抬升没有被降下，需要降下再暂停
            if self.G_IfZPositionLiftUpFlag==True:
                command_string = """
                    G90
                    G91
                    G1 Z-%f F8000
                    """ % (
                    self.G_AMSFilaCutZPositionLiftingUp,
                )
                self.G_PhrozenGCode.run_script_from_command(command_string)
                self.G_IfZPositionLiftUpFlag = False
                self.G_PhrozenFluiddRespondInfo("Z轴下拉降低；command_string='%s'" % command_string)


        if self.G_ToolheadIfHaveFilaFlag==True:
            self.G_PhrozenFluiddRespondInfo("喷头有线材，设置恢复不用回退再进料")
            #lancaigang240116：MA模式需要暂停stm32
            if self.G_AMSDeviceWorkMode == AMS_WORK_MODE_MA:#MA
                if self.G_KlipperInPausing == False:
                    self.G_PhrozenFluiddRespondInfo("不在暂停中，允许新的暂停")
                    #lancaigang250607:
                    self.G_PhrozenFluiddRespondInfo("启用快速暂停")
                    self.G_KlipperQuickPause = True
                    #lancaigang241012：暂时不暂停AMS
                    self.Cmds_PhrozenKlipperPause(None)
                    #self.Cmds_PhrozenKlipperPauseNoneCmdToSTM32(None)
                else:
                    self.G_PhrozenFluiddRespondInfo("暂停中，不允许新的暂停")
                
            #lancaigang240412：单色模式，如果有AMS多色进料，需要暂停AMS
            elif self.G_AMSDeviceWorkMode == AMS_WORK_MODE_FILA_RUNOUT:#M3
                if self.G_AMSDevice1IfNormal==True:
                    self.G_PhrozenFluiddRespondInfo("喷头有线材，单色M3模式有AMS多色，需要stm32也暂停")
                    if self.G_KlipperInPausing == False:
                        self.G_PhrozenFluiddRespondInfo("不在暂停中，允许新的暂停")
                        #lancaigang250607:
                        self.G_PhrozenFluiddRespondInfo("启用快速暂停")
                        self.G_KlipperQuickPause = True
                        #lancaigang241012：暂时不暂停AMS
                        self.Cmds_PhrozenKlipperPause(None)
                        #self.Cmds_PhrozenKlipperPauseNoneCmdToSTM32(None)
                    else:
                        self.G_PhrozenFluiddRespondInfo("暂停中，不允许新的暂停")
                else:
                    self.G_PhrozenFluiddRespondInfo("喷头有线材，单色M3模式没有AMS多色，不需要stm32暂停")
                    if self.G_KlipperInPausing == False:
                        self.G_PhrozenFluiddRespondInfo("不在暂停中，允许新的暂停")
                        #lancaigang250607:
                        self.G_PhrozenFluiddRespondInfo("启用快速暂停")
                        self.G_KlipperQuickPause = True
                        self.Cmds_PhrozenKlipperPauseNoneCmdToSTM32(None)
                    else:
                        self.G_PhrozenFluiddRespondInfo("暂停中，不允许新的暂停")
                    
            else:#MC
                #lancaigang240427：屏蔽
                #self.Cmds_PhrozenKlipperPauseNoneCmdToSTM32(None)
                #lancaigang240427：屏幕主动暂停，也需要stm32暂停
                self.G_PhrozenFluiddRespondInfo("喷头有线材，MC多色模式有AMS多色，需要stm32暂停")
                if self.G_KlipperInPausing == False:
                    self.G_PhrozenFluiddRespondInfo("不在暂停中，允许新的暂停")
                    #lancaigang250607:
                    self.G_PhrozenFluiddRespondInfo("启用快速暂停")
                    self.G_KlipperQuickPause = True
                    #lancaigang241012：暂时不暂停AMS
                    self.Cmds_PhrozenKlipperPause(None)
                    #self.Cmds_PhrozenKlipperPauseNoneCmdToSTM32(None)
                else:
                    self.G_PhrozenFluiddRespondInfo("暂停中，不允许新的暂停")

                
            self.G_IfToolheadHaveFilaInitiativePauseFlag  = True
        else:
            #lancaigang231216：如果正在换料过程中主动暂停，因为换料过程中已经抬升了z轴，恢复的时候无法恢复这部分的z轴高度
            self.G_PhrozenFluiddRespondInfo("喷头没有线材，设置恢复需要STM32回退再进料")
            if self.G_KlipperInPausing == False:
                self.G_PhrozenFluiddRespondInfo("不在暂停中，允许新的暂停")
                #lancaigang250607:
                self.G_PhrozenFluiddRespondInfo("启用快速暂停")
                self.G_KlipperQuickPause = True
                #lancaigang241012：暂时不暂停AMS
                self.Cmds_PhrozenKlipperPause(None)
                #self.Cmds_PhrozenKlipperPauseNoneCmdToSTM32(None)
            else:
                self.G_PhrozenFluiddRespondInfo("暂停中，不允许新的暂停")

            

        #lancaigang250527：暂停待料区
        self.G_PhrozenFluiddRespondInfo("开始调用外部宏命令-PRZ_PAUSE_WAITINGAREA")
        command = """
        PRZ_PAUSE_WAITINGAREA
        """
        self.G_PhrozenGCode.run_script_from_command(command)
        self.G_PhrozenFluiddRespondInfo("结束调用外部宏命令:command=%s" % (command))

        self.G_PhrozenFluiddRespondInfo("触摸屏或fluidd网页主动暂停，暂停")
        #self.G_PhrozenFluiddRespondInfo("+PAUSE:10,%d" % self.G_ChangeChannelTimeoutNewChan)
        self.G_PhrozenFluiddRespondInfo("+PAUSE:10,%d,%d" % (self.G_ChangeChannelTimeoutOldChan,self.G_ChangeChannelTimeoutNewChan))



    ####################################
    #函数名称：
    #输入参数：
    #返 回 值:
    #功能描述：蓝才刚-20230830
    ####################################
    # PRZ_CANCEL 取消打印
    def Cmds_PhrozenKlipperCancel(self, gcmd):
        self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_PhrozenKlipperCancel]klipper取消打印；")

        self.G_PhrozenFluiddRespondInfo("+CANCEL:0,%d" % self.G_ChangeChannelTimeoutNewChan)

        self.G_PhrozenFluiddRespondInfo("=====CANCEL=====")
        self.G_PhrozenFluiddRespondInfo("=====CANCEL=====self.G_ChangeChannelTimeoutOldChan=%d" % self.G_ChangeChannelTimeoutOldChan)
        self.G_PhrozenFluiddRespondInfo("=====CANCEL=====self.G_ChangeChannelTimeoutNewChan=%d" % self.G_ChangeChannelTimeoutNewChan)




        self.G_PhrozenFluiddRespondInfo("外部宏命令：CANCEL_PRINT")
        #lancaigang240120：暂停改用cfg配置表宏命令
        command = """
        CANCEL_PRINT
        """
        self.G_PhrozenGCode.run_script_from_command(command)
        self.G_PhrozenFluiddRespondInfo("调用宏命令:command=%s" % (command))


        #解锁
        self.Base_AMSSerialCmdUnlock()


        # #lancaigang231216：
        # eventtime = self.G_PhrozenReactor.monotonic()
        # # Determine "printing" status
        # idle_timeout = self.G_PhrozenPrinter.lookup_object("idle_timeout")
        # is_printing = idle_timeout.get_status(eventtime)["state"] == "Printing"
        # if is_printing:
        #     self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_PhrozenKlipperCancel]正在打印中；命令='%s'")
        # else:
        #     self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_PhrozenKlipperCancel]未在打印中；命令='%s；return'")
        #     return


        #lancaigang231207:+PAUSE:1进料卡料标签
        self.G_IfInFilaBlockFlag=False
        #lancaigang240321：PG102过程中暂停标签
        self.PG102DelayPauseFlag=False
        #lancaigang240426：恢复后置位false
        self.G_ResumeProcessCheckPauseStatus=False
        #lancaigang240410：
        self.G_CancelFlag=True
        #lancaigang240411：如果没有收到P0 M3命令，不使用断料检测机制
        self.G_P0M3Flag = False

        self.ManualCmdFlag=False
        #lancaigang250805:切刀测试
        self.G_CutCheckTest=False

        #lancaigang240427：AMS异常重启，需要记录
        self.G_AMS1ErrorRestartFlag = False
        self.G_AMS1ErrorRestartCount = 0

        #lancaigang241030:
        self.G_AMS2ErrorRestartFlag = False
        self.G_AMS2ErrorRestartCount = 0

        #lancaigang240124：stm32主动上报，开启可以暂停1次
        self.STM32ReprotPauseFlag=0

        #lancaigang250526：
        self.G_IfToolheadHaveFilaInitiativePauseFlag=False
        #lancaigang250526：暂停中，不允许新的gcode命令，需等待暂停完成
        self.G_KlipperInPausing = False
        #lancaigang250527：暂停快速执行
        self.G_KlipperQuickPause = False
        #lancaigang250607：打印状态；1-退料中；2-进料中；3-打印中；4-暂停
        self.G_KlipperPrintStatus= -1
        self.G_ASM1DisconnectErrorCount=0
        #lancaigang250812:单色断料检测，补充回到暂停区
        self.G_RetryToPauseAreaFlag = False
        self.G_RetryToPauseAreaCount = 0
        self.G_P10SpitNum=0
        self.G_IfChangeFilaOngoing= False
        #lancaigang240223：喷头切线失败标记
        self.ToolheadCutFlag = False





        #lancaigang250515：
        self.G_P0M1MCNoneAMS=0
        self.G_PhrozenFluiddRespondInfo("self.G_P0M1MCNoneAMS=0")

        #lancaigang250515:清空串口屏配置数据
        self.Cmds_GetUartScreenCfgClear()


        #lancaigang250807:取消再清空暂停状态
        self.G_PhrozenPrinterCancelPauseResume.cmd_CLEAR_PAUSE(None)
        self.G_PhrozenFluiddRespondInfo("清空暂停状态")





        #lancaigang241016:
        #self.ToolheadCutFlag=False

        # #AMS多色紧急停止
        # #self.Cmds_CmdP4(None)
        # #lancaigang240125：
        # #lancaigang240507：不发送暂停命令，发送M0命令
        # #lancaigang240516：取消了，不执行续打功能
        # self.Cmds_AMSSerial1Send("AT+PAUSE")
        # self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_PhrozenKlipperCancel]AT+PAUSE暂停stm32电机")

        # #klipper主动暂停
        # self.Cmds_PhrozenKlipperPause(None)
        # #cancel取消命令
        # self.G_PhrozenPrinterCancelPauseResume.cmd_CANCEL_PRINT(None)

        self.G_ProzenToolhead.dwell(1.0)

        #lancaigang240416:
        #lancaigang240516：取消了，不执行续打功能
        # if self.G_SerialPort1OpenFlag == True:
        #     self.Cmds_AMSSerial1Send("M0")
        #     self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_PhrozenKlipperCancel]发送命令：M0")

        # #AMS多色紧急停止
        # #self.Cmds_CmdP4(None)
        # #lancaigang240125：
        # #lancaigang240507：不发送暂停命令，发送M0命令
        # #lancaigang240516：取消了，不执行续打功能
        # self.Cmds_AMSSerial1Send("AT+PAUSE")
        # self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_PhrozenKlipperCancel]AT+PAUSE暂停stm32电机")

        #lancaigang250619:检查AMS是否重新连接成功
        self.Cmds_USBConnectErrorCheck()

        if self.G_AMSDeviceWorkMode == AMS_WORK_MODE_MC:
            self.G_PhrozenFluiddRespondInfo("发送命令:MA多色模式-MC-AMS空闲模式")
            #lancaigang241031:
            if self.G_SerialPort1OpenFlag == True:
                self.Cmds_AMSSerial1Send("MC")
                self.G_PhrozenFluiddRespondInfo("串口1发送命令：MC")
            #lancaigang241030:
            if self.G_SerialPort2OpenFlag == True:
                self.Cmds_AMSSerial2Send("MC")
                self.G_PhrozenFluiddRespondInfo("串口2发送命令：MC")
        elif self.G_AMSDeviceWorkMode == AMS_WORK_MODE_MA:
            self.G_PhrozenFluiddRespondInfo("发送命令:M2单色续料模式-MA-AMS空闲模式")
            #lancaigang241031:
            if self.G_SerialPort1OpenFlag == True:
                self.Cmds_AMSSerial1Send("MA")
                self.G_PhrozenFluiddRespondInfo("串口1发送命令：MA")
            #lancaigang241030:
            if self.G_SerialPort2OpenFlag == True:
                self.Cmds_AMSSerial2Send("MA")
                self.G_PhrozenFluiddRespondInfo("串口2发送命令：MA")
        elif self.G_AMSDeviceWorkMode == AMS_WORK_MODE_FILA_RUNOUT:
            self.G_PhrozenFluiddRespondInfo("发送命令:M3单色模式-MA-AMS空闲模式")
            #lancaigang241031:
            if self.G_SerialPort1OpenFlag == True:
                self.Cmds_AMSSerial1Send("MA")
                self.G_PhrozenFluiddRespondInfo("串口1发送命令：MA")
            #lancaigang241030:
            if self.G_SerialPort2OpenFlag == True:
                self.Cmds_AMSSerial2Send("MA")
                self.G_PhrozenFluiddRespondInfo("串口2发送命令：MA")
        else:
            self.G_PhrozenFluiddRespondInfo("未知模式，暂停AMS")
            
            #lancaigang241031:
            if self.G_SerialPort1OpenFlag == True:
                #lancaigang240516：未知模式，暂停AMS
                self.Cmds_AMSSerial1Send("AT+PAUSE")
                self.G_PhrozenFluiddRespondInfo("串口1发送AT+PAUSE暂停stm32电机")
            #lancaigang241030:
            if self.G_SerialPort2OpenFlag == True:
                self.Cmds_AMSSerial2Send("AT+PAUSE")
                self.G_PhrozenFluiddRespondInfo("串口2发送AT+PAUSE暂停stm32电机")


        #lancaigang241106：
        self.G_P0M2MAStartPrintFlag=0
        #lancaigang250104：P2A3标志位
        self.G_P2A3Flag = 0

        #lancaigang250102:打印层数计算
        self.G_PrintCountNum=0


        #lancaigang20231013：断开连接
        #self.Device_DisconnectAMSDevice()
        #lancaigang250712:屏蔽，不用断开连接
        #lancaigang250815：不屏蔽，防止取消后串口异常
        self.Cmds_CmdP29(None)

        #lancaigang250815:模式设置为未知模式
        self.G_AMSDeviceWorkMode = AMS_WORK_MODE_UNKNOW



        self.G_PhrozenFluiddRespondInfo("+CANCEL:1,%d" % self.G_ChangeChannelTimeoutNewChan)


    ####################################
    #函数名称：
    #输入参数：
    #返 回 值:
    #功能描述：蓝才刚-20230830
    ####################################
    def Cmds_USBConnectErrorCheck(self):
        self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_USBConnectErrorCheck]")


        self.G_PhrozenFluiddRespondInfo("self.G_CancelFlag='%s'" % self.G_CancelFlag)
        self.G_PhrozenFluiddRespondInfo("当前模式")
        if self.G_AMSDeviceWorkMode == AMS_WORK_MODE_UNKNOW:
            self.G_PhrozenFluiddRespondInfo("+Mode:0,unkown")
        elif self.G_AMSDeviceWorkMode == AMS_WORK_MODE_MC:
            self.G_PhrozenFluiddRespondInfo("+Mode:1,MC")
        elif self.G_AMSDeviceWorkMode == AMS_WORK_MODE_MA:
            self.G_PhrozenFluiddRespondInfo("+Mode:2,MA")
        elif self.G_AMSDeviceWorkMode == AMS_WORK_MODE_FILA_RUNOUT:
            self.G_PhrozenFluiddRespondInfo("+Mode:3,RUNOUT")
        else:
            self.G_PhrozenFluiddRespondInfo("+Mode:-1,error")

        try:
            self.G_PhrozenFluiddRespondInfo("[(cmds.py)Cmds_USBConnectErrorCheck]重新初始化串口1")
            self.G_SerialPort1Obj = serial.Serial(self.G_Serialport1Define, SERIAL_PORT_BAUD, timeout=3)
            #串口打开成功
            if self.G_SerialPort1Obj is not None:
                if self.G_SerialPort1Obj.is_open:
                    self.G_SerialPort1OpenFlag = True
                    self.G_PhrozenFluiddRespondInfo("重新初始化串口1成功")
                    #lancaigang231213：打开串口
                    self.G_SerialPort1Obj.flushInput()  # clean serial write cache
                    self.G_SerialPort1Obj.flush()
                    self.G_PhrozenFluiddRespondInfo("串口1清空")
                    self.G_PhrozenFluiddRespondInfo("重新注册串口1回调函数")
                    self.G_SerialPort1RecvTimmer = self.G_PhrozenReactor.register_timer(self.Device_TimmerUart1Recv, self.G_PhrozenReactor.NOW)
                    
                    if "+PAUSE:g" in self.G_PauseToLCDString:
                        self.G_PhrozenFluiddRespondInfo("如果是USB断料错误，清空报错信息")
                        #lancaigang250902：不能为空，防止后面暂停报错信息为空而无法弹出暂停框
                        #self.G_PauseToLCDString=""
                        self.G_PauseToLCDString="+PAUSE:4,%d,%d" % (self.G_ChangeChannelTimeoutOldChan,self.G_ChangeChannelTimeoutNewChan)
                        self.G_PhrozenFluiddRespondInfo("len(self.G_PauseToLCDString)='%d'" % len(self.G_PauseToLCDString))

        except:
            self.G_PhrozenFluiddRespondInfo("未能打开tty1口，请检查USB口或重启尝试")
            self.G_SerialPort1OpenFlag = False

            if self.G_AMSDeviceWorkMode == AMS_WORK_MODE_UNKNOW or self.G_AMSDeviceWorkMode == AMS_WORK_MODE_FILA_RUNOUT:
                self.G_PhrozenFluiddRespondInfo("单色M3或未知模式，不用更新暂停信息")
            else:
                if len(self.G_PauseToLCDString)==0:
                    self.G_PhrozenFluiddRespondInfo("更新暂停信息")
                    self.G_PhrozenFluiddRespondInfo("暂停:+PAUSE:g")
                    self.G_PauseToLCDString="+PAUSE:g,%d,%d" % (self.G_ChangeChannelTimeoutOldChan,self.G_ChangeChannelTimeoutNewChan)
                else:
                    #self.G_PhrozenFluiddRespondInfo(self.G_PauseToLCDString)
                    self.G_PhrozenFluiddRespondInfo("更新暂停信息")
                    self.G_PauseToLCDString="+PAUSE:g,%d,%d" % (self.G_ChangeChannelTimeoutOldChan,self.G_ChangeChannelTimeoutNewChan)
                    self.G_PhrozenFluiddRespondInfo("暂停:+PAUSE:g")

        try:
            self.G_PhrozenFluiddRespondInfo("[(cmds.py)Cmds_USBConnectErrorCheck]重新初始化串口2")
            self.G_SerialPort2Obj = serial.Serial(self.G_Serialport2Define, SERIAL_PORT_BAUD, timeout=3)
            #串口打开成功
            if self.G_SerialPort2Obj is not None:
                if self.G_SerialPort2Obj.is_open:
                    self.G_SerialPort2OpenFlag = True
                    self.G_PhrozenFluiddRespondInfo("重新初始化串口2成功")
                    self.G_SerialPort2Obj.flushInput()  # clean serial write cache
                    self.G_SerialPort2Obj.flush()
                    self.G_PhrozenFluiddRespondInfo("串口2清空")
                    self.G_PhrozenFluiddRespondInfo("重新注册串口2回调函数")
                    self.G_SerialPort2RecvTimmer = self.G_PhrozenReactor.register_timer(self.Device_TimmerUart2Recv, self.G_PhrozenReactor.NOW)
                    # if "+PAUSE:g" in self.G_PauseToLCDString:
                    #     self.G_PauseToLCDString=""
        except:
            self.G_PhrozenFluiddRespondInfo("未能打开tty2口，请检查USB口或重启尝试")
            self.G_SerialPort2OpenFlag = False

    ####################################
    #函数名称：
    #输入参数：
    #返 回 值:
    #功能描述：蓝才刚-20230830
    ####################################
    def Cmds_CutFilaIfNormalCheck(self):
        self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_CutFilaIfNormalCheck]")

        #lancaigang241016:
        self.ToolheadCutFlag=False

        #lancaigang250527：暂停快速执行
        self.G_KlipperQuickPause = False
        
        # 发送命令8S后检查线材是否停留在喷头，正常回退8s喷头不应该有线材
        #lancaigang20231013：改为8s延时
        #lancaigang231201：改为5秒
        #lancaigang240912：klipper的延时必须要大于stm32旧通道回退的时间
        #self.G_ProzenToolhead.dwell(6.0)

        self.G_PhrozenFluiddRespondInfo("秒延时检测到是否有线材???")
        #lancaigang240125：不能用sleep，会阻塞主线程
        #time.sleep(5)
        #回退线材8s后，喷头是否有线材，正常是不会有线材的了
        if self.G_ToolheadIfHaveFilaFlag:
            #raise self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_P1TnManualChangeChannel]换料检查喷头是否有线材，但回退过了几秒喷头上还检测到线材；cmd='%s'" % (gcmd.get_commandline()))
            self.G_PhrozenFluiddRespondInfo("喷头回退过了5秒喷头还检测到线材，请检查切刀是否异常，手动换料失败;klipper暂停")
            # // lancaigang231202:+PAUSE:1,ch;1-进料用完卡线，暂停
            # // lancaigang231202:+PAUSE:2,ch;2-暂停ACK
            # // lancaigang231204:+PAUSE:3,ch;3-新通道打印过程中慢速补料超时10s，暂停
            # // lancaigang231205:+PAUSE:4,ch;4-新通道进料超时50s，暂停
            # // lancaigang231205:+PAUSE:5,ch;5-新通道打印过程中快速补料超时10s，暂停
            # // lancaigang231205:+PAUSE:6,ch;6-入口位到停靠位超时10s，暂停
            # // lancaigang231205:+PAUSE:7,ch;7-缓冲器满状态超时30s，暂停
            # // lancaigang231205:+PAUSE:8,ch;8-喷头切刀或传感器异常，暂停
            # // lancaigang231205:+PAUSE:9,ch;9-换料超时120s，暂停
            # // lancaigang231202:+PAUSE:a,ch;a-停靠位到缓冲器入口超时10s，暂停
            # // lancaigang231202:+PAUSE:b,ch;b-预留
            # // lancaigang231202:+PAUSE:c,ch;c-预留
            # // lancaigang231202:+PAUSE:d,ch;d-预留
            # // lancaigang231202:+PAUSE:10,ch;10-触摸屏或fluidd网页主动暂停
            #lancaigang240223：之前Z抬升切线已经失败，暂停之前先要Z下降
            if self.G_IfZPositionLiftUpFlag==True:
                command_string = """
                    G90
                    G91
                    G1 Z-%f F8000
                    """ % (
                    self.G_AMSFilaCutZPositionLiftingUp,
                )
                self.G_PhrozenGCode.run_script_from_command(command_string)
                self.G_IfZPositionLiftUpFlag = False
                self.G_PhrozenFluiddRespondInfo("Z轴下拉降低；command_string='%s'" % command_string)
                

            #lancaigang240223:
            self.ToolheadCutFlag=True

            #lancaigang240322：如果前面已经暂停了，不用再报异常
            if self.STM32ReprotPauseFlag==1:
                self.G_PhrozenFluiddRespondInfo("已经暂停了，不用重复暂停")
                self.G_PhrozenFluiddRespondInfo("喷头切刀或传感器异常，暂停")
                #self.G_PhrozenFluiddRespondInfo("+PAUSE:8,%d" % self.G_ChangeChannelTimeoutOldChan)
                #lancaigang250414:
                #self.G_PhrozenFluiddRespondInfo("+PAUSE:8,%d,%d" % (self.G_ChangeChannelTimeoutOldChan,self.G_ChangeChannelTimeoutNewChan))
                
                #lancaigang250619:检查AMS是否重新连接成功
                self.Cmds_USBConnectErrorCheck()
                
                
                #lancaigang250721：
                if len(self.G_PauseToLCDString)==0:
                    self.G_PhrozenFluiddRespondInfo("+PAUSE:8,%d,%d" % (self.G_ChangeChannelTimeoutOldChan,self.G_ChangeChannelTimeoutNewChan))
                else:
                    #self.G_PhrozenFluiddRespondInfo(self.G_PauseToLCDString)
                    self.G_PhrozenFluiddRespondInfo("更新暂停信息")
                    #lancaigang250721：如果AMS回拉异常，都是异常暂停8作为最后的暂停
                    self.G_PauseToLCDString="+PAUSE:8,%d,%d" % (self.G_ChangeChannelTimeoutOldChan,self.G_ChangeChannelTimeoutNewChan)
                    self.G_PhrozenFluiddRespondInfo(self.G_PauseToLCDString)

                

                
            else:
                #lancaigang240328：如果是手动命令，不暂停
                if self.ManualCmdFlag==True:
                    self.G_PhrozenFluiddRespondInfo("手动命令，klipper不执行暂停")
                    #lancaigang241031:
                    if self.G_SerialPort1OpenFlag == True:
                        self.Cmds_AMSSerial1Send("AT+PAUSE")
                        self.G_PhrozenFluiddRespondInfo("串口1发送AT+PAUSE暂停stm32电机")
                    #lancaigang241030:
                    if self.G_SerialPort2OpenFlag == True:
                        self.Cmds_AMSSerial2Send("AT+PAUSE")
                        self.G_PhrozenFluiddRespondInfo("串口2发送AT+PAUSE暂停stm32电机")

                    #lancaigang250805:
                    #self.G_PhrozenFluiddRespondInfo("+PAUSE:8,%d,%d" % (self.G_ChangeChannelTimeoutOldChan,self.G_ChangeChannelTimeoutNewChan))
                    if len(self.G_PauseToLCDString)==0:
                        self.G_PhrozenFluiddRespondInfo("+PAUSE:8,%d,%d" % (self.G_ChangeChannelTimeoutOldChan,self.G_ChangeChannelTimeoutNewChan))
                    else:
                        #self.G_PhrozenFluiddRespondInfo(self.G_PauseToLCDString)
                        self.G_PhrozenFluiddRespondInfo("更新暂停信息")
                        #lancaigang250721：如果AMS回拉异常，都是异常暂停8作为最后的暂停
                        self.G_PauseToLCDString="+PAUSE:8,%d,%d" % (self.G_ChangeChannelTimeoutOldChan,self.G_ChangeChannelTimeoutNewChan)
                        self.G_PhrozenFluiddRespondInfo(self.G_PauseToLCDString)
                elif self.G_CutCheckTest==True:
                    self.G_PhrozenFluiddRespondInfo("切刀测试，klipper不执行暂停")
                    #lancaigang241031:
                    if self.G_SerialPort1OpenFlag == True:
                        self.Cmds_AMSSerial1Send("AT+PAUSE")
                        self.G_PhrozenFluiddRespondInfo("串口1发送AT+PAUSE暂停stm32电机")
                    #lancaigang241030:
                    if self.G_SerialPort2OpenFlag == True:
                        self.Cmds_AMSSerial2Send("AT+PAUSE")
                        self.G_PhrozenFluiddRespondInfo("串口2发送AT+PAUSE暂停stm32电机")

                    #lancaigang250805:
                    #self.G_PhrozenFluiddRespondInfo("+PAUSE:8,%d,%d" % (self.G_ChangeChannelTimeoutOldChan,self.G_ChangeChannelTimeoutNewChan))
                    if len(self.G_PauseToLCDString)==0:
                        self.G_PhrozenFluiddRespondInfo("+PAUSE:8,%d,%d" % (self.G_ChangeChannelTimeoutOldChan,self.G_ChangeChannelTimeoutNewChan))
                    else:
                        #self.G_PhrozenFluiddRespondInfo(self.G_PauseToLCDString)
                        self.G_PhrozenFluiddRespondInfo("更新暂停信息")
                        #lancaigang250721：如果AMS回拉异常，都是异常暂停8作为最后的暂停
                        self.G_PauseToLCDString="+PAUSE:8,%d,%d" % (self.G_ChangeChannelTimeoutOldChan,self.G_ChangeChannelTimeoutNewChan)
                        self.G_PhrozenFluiddRespondInfo(self.G_PauseToLCDString)
                else:
                    self.G_PhrozenFluiddRespondInfo("喷头切刀或传感器异常，暂停")


                    if self.G_KlipperInPausing == False:
                        self.G_PhrozenFluiddRespondInfo("不在暂停中，允许新的暂停")
                        #lancaigang250607:
                        self.G_PhrozenFluiddRespondInfo("启用快速暂停")
                        self.G_KlipperQuickPause = True
                        #klipper主动暂停
                        self.Cmds_PhrozenKlipperPause(None)
                    else:
                        self.G_PhrozenFluiddRespondInfo("暂停中，不允许新的暂停")
                
                    #self.G_PhrozenFluiddRespondInfo("+PAUSE:8,%d" % self.G_ChangeChannelTimeoutOldChan)
                    #lancaigang250619:检查AMS是否重新连接成功
                    self.Cmds_USBConnectErrorCheck()
                    
                    #lancaigang250414:
                    #self.G_PhrozenFluiddRespondInfo("+PAUSE:8,%d,%d" % (self.G_ChangeChannelTimeoutOldChan,self.G_ChangeChannelTimeoutNewChan))
                    if len(self.G_PauseToLCDString)==0:
                        self.G_PhrozenFluiddRespondInfo("+PAUSE:8,%d,%d" % (self.G_ChangeChannelTimeoutOldChan,self.G_ChangeChannelTimeoutNewChan))
                    else:
                        #self.G_PhrozenFluiddRespondInfo(self.G_PauseToLCDString)
                        self.G_PhrozenFluiddRespondInfo("更新暂停信息")
                        #lancaigang250721：如果AMS回拉异常，都是异常暂停8作为最后的暂停
                        self.G_PauseToLCDString="+PAUSE:8,%d,%d" % (self.G_ChangeChannelTimeoutOldChan,self.G_ChangeChannelTimeoutNewChan)
                        self.G_PhrozenFluiddRespondInfo(self.G_PauseToLCDString)

            

    ####################################
    #函数名称：
    #输入参数：
    #返 回 值:
    #功能描述：蓝才刚-20230830
    ####################################
    #换料通道
    def Cmds_P1TnManualChangeChannel(self, chan, gcmd):
        self.G_PhrozenFluiddRespondInfo("=====[(cmds.python)Cmds_P1TnManualChangeChannel]")

        if gcmd is None:
            self.G_PhrozenFluiddRespondInfo("gcmd is None")
            #self.G_PhrozenFluiddRespondInfo("return")
            #return
            #pass
        if gcmd is not None:
            self.G_PhrozenFluiddRespondInfo("gcmd is not None:")
            self.G_PhrozenFluiddRespondInfo("=====[(cmds.python)Cmds_P1TnManualChangeChannel]cmd='%s'" % (gcmd.get_commandline()))

        # #lancaigang20231101：先判断喷头是否有线材，有则先退料
        # if self.G_ToolheadIfHaveFilaFlag:
        #     self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_P1TnManualChangeChannel]喷头有线材，防止堵料先退料；cmd='%s'" % (gcmd.get_commandline()))
        #     #// 全部后退到停靠位；//===== P2 A1 所有线料退到停靠位待打印 Yes；"AP"；
        #     self.Cmds_AMSSerial1Send("AP")
        #     self.G_PhrozenFluiddRespondInfo("发送命令: AP，全部后退到停靠位")


        #lancaigang231216：手动换料也记录gcode通道和命令
        #获取通道号和gcmd对象
        #self.G_ChangeChannelTimeoutOldChan=chan
        #self.G_ChangeChannelTimeoutOldGcmd=gcmd


        self.G_IfChangeFilaOngoing= True

        self.G_PhrozenFluiddRespondInfo("self.G_ToolheadIfHaveFilaFlag=%d" % (self.G_ToolheadIfHaveFilaFlag))



        #lancaigang240229：防止发送命令粘包
        #time.sleep(1)
        self.G_ProzenToolhead.dwell(0.5)

        #lancaigang250619:检查AMS是否重新连接成功
        self.Cmds_USBConnectErrorCheck()

        #lancaigang240223：如果切线失败，上个函数已经Z轴下降了
        if self.ToolheadCutFlag==True:
            self.ToolheadCutFlag=False
            self.G_PhrozenFluiddRespondInfo("之前切线异常，换线失败")
            self.G_ChangeChannelFirstFilaFlag=True
            self.G_IfChangeFilaOngoing= False

            #stm32上报暂停只能暂停1次，不能重复暂停
            self.STM32ReprotPauseFlag=1
            #lancaigang231202：P1 C?自动换料时，如果第1次通道就进料异常暂停，如果要恢复，也继续从第1次通道开始
            self.G_ChangeChannelFirstFilaFlag=True

            # #lancaigang250308：恢复本身已经切线异常了，这里也报切线异常
            # #self.G_PhrozenFluiddRespondInfo("+PAUSE:8,%d" % self.G_ChangeChannelTimeoutNewChan)
            # #self.G_PhrozenFluiddRespondInfo("+PAUSE:8,%d,%d" % (self.G_ChangeChannelTimeoutOldChan,self.G_ChangeChannelTimeoutNewChan))
            # if len(self.G_PauseToLCDString)==0:
            #     self.G_PhrozenFluiddRespondInfo("+PAUSE:8,%d,%d" % (self.G_ChangeChannelTimeoutOldChan,self.G_ChangeChannelTimeoutNewChan))
            # else:
            #     self.G_PhrozenFluiddRespondInfo(self.G_PauseToLCDString)

            self.G_PauseToLCDString="+PAUSE:8,%d,%d" % (self.G_ChangeChannelTimeoutOldChan,self.G_ChangeChannelTimeoutNewChan)

            #lancaigang240416:
            if self.G_SerialPort1OpenFlag == True:
                #lancaigang240603：防止AMS一直停不了
                self.Cmds_AMSSerial1Send("AT+PAUSE")
                self.G_PhrozenFluiddRespondInfo("串口1-AT+PAUSE暂停stm32电机")
            #lancaigang241030:
            if self.G_SerialPort2OpenFlag == True:
                self.Cmds_AMSSerial2Send("AT+PAUSE")
                self.G_PhrozenFluiddRespondInfo("串口2-AT+PAUSE暂停stm32电机")

            if self.G_KlipperInPausing == False:
                self.G_PhrozenFluiddRespondInfo("不在暂停中，允许新的暂停")
                #lancaigang250607:
                self.G_PhrozenFluiddRespondInfo("启用快速暂停")
                self.G_KlipperQuickPause = True
                #klipper主动暂停
                self.Cmds_PhrozenKlipperPause(None)
            else:
                self.G_PhrozenFluiddRespondInfo("暂停中，不允许新的暂停")

            self.G_KlipperIfPaused = True

            #lancaigang240325：换料失败，不能执行恢复
            self.G_MCModeCanResumeFlag = False

            #lancaigang240524：用于UIUX动态界面
            self.G_PhrozenFluiddRespondInfo("+T:1,%d" % self.G_ChangeChannelTimeoutNewChan)
            
            #lancaigang250529:
            if len(self.G_PauseToLCDString)==0:
                self.G_PhrozenFluiddRespondInfo("+PAUSE:8,%d,%d" % (self.G_ChangeChannelTimeoutOldChan,self.G_ChangeChannelTimeoutNewChan))
            else:
                self.G_PhrozenFluiddRespondInfo(self.G_PauseToLCDString)

            self.G_PhrozenFluiddRespondInfo("return")
            return

        self.G_PhrozenFluiddRespondInfo("self.G_ToolheadIfHaveFilaFlag=%d" % (self.G_ToolheadIfHaveFilaFlag))

        #lancaigang241030:
        if self.G_ChangeChannelTimeoutNewChan in range(1, 5):
            #lancaigang240911：新的AMS段码屏，T?命令单纯进料
            #发送手动换料命令
            self.Cmds_AMSSerial1Send("T%d" % self.G_ChangeChannelTimeoutNewChan)
            self.G_PhrozenFluiddRespondInfo("串口1换料发送命令: T%d" % self.G_ChangeChannelTimeoutNewChan)
            #lancaigang240524：用于UIUX动态界面
            self.G_PhrozenFluiddRespondInfo("+T:0,%d" % self.G_ChangeChannelTimeoutNewChan)
        elif self.G_ChangeChannelTimeoutNewChan in range(5, 9):
            self.Cmds_AMSSerial2Send("T%d" % self.G_ChangeChannelTimeoutNewChan-4)
            self.G_PhrozenFluiddRespondInfo("串口2换料发送命令: T%d" % self.G_ChangeChannelTimeoutNewChan-4)
            self.G_PhrozenFluiddRespondInfo("+T:0,%d" % self.G_ChangeChannelTimeoutNewChan-4)

        #lancaigang250322：
        if self.ManualCmdFlag==True:
            self.G_PhrozenFluiddRespondInfo("外部宏命令-PG105；手动命令，不执行吐料功能")
            self.IfDoPG102Flag=True
        #lancaigang250805:切刀测试
        elif self.G_CutCheckTest == True:
            #lancaigang240319：切完后，先吐掉残留喷头的线材，防止切成米粒
            self.G_PhrozenFluiddRespondInfo("外部宏命令-PG105；切线之后，喷头升温同时AMS进线")
            self.PG102Flag=True
            self.IfDoPG102Flag=True
            self.G_PhrozenFluiddRespondInfo("self.Flag=True")
            command_string = """
            PG105
            """
            self.G_PhrozenGCode.run_script_from_command(command_string)
            self.G_PhrozenFluiddRespondInfo("command_string='%s'" % command_string)
            self.PG102Flag=False
            self.G_PhrozenFluiddRespondInfo("self.Flag=False")
        else:
            #lancaigang240319：切完后，先吐掉残留喷头的线材，防止切成米粒
            self.G_PhrozenFluiddRespondInfo("外部宏命令-PG105；切线之后，喷头升温同时AMS进线")
            self.PG102Flag=True
            self.IfDoPG102Flag=True
            self.G_PhrozenFluiddRespondInfo("self.Flag=True")
            command_string = """
            PG105
            """
            self.G_PhrozenGCode.run_script_from_command(command_string)
            self.G_PhrozenFluiddRespondInfo("command_string='%s'" % command_string)
            self.PG102Flag=False
            self.G_PhrozenFluiddRespondInfo("self.Flag=False")

        self.G_PhrozenFluiddRespondInfo("self.G_ToolheadIfHaveFilaFlag=%d" % (self.G_ToolheadIfHaveFilaFlag))

        #lancaigang240328：手动命令不执行吐料
        if self.ManualCmdFlag==True:
            self.G_PhrozenFluiddRespondInfo("外部宏命令-PG110；手动命令，不执行")
            self.IfDoPG102Flag=True
        #lancaigang250805:切刀测试
        elif self.G_CutCheckTest == True:
            #lancaigang240319：切完后，先吐掉残留喷头的线材，防止切成米粒
            self.G_PhrozenFluiddRespondInfo("外部宏命令-PG110；STM32进料之后，klipper开始吐料接住进料")
            self.PG102Flag=True
            self.IfDoPG102Flag=True
            self.G_PhrozenFluiddRespondInfo("self.Flag=True")
            command_string = """
            PG110
            """
            self.G_PhrozenGCode.run_script_from_command(command_string)
            self.G_PhrozenFluiddRespondInfo("command_string='%s'" % command_string)
            self.PG102Flag=False
            self.G_PhrozenFluiddRespondInfo("self.Flag=False")
        else:
            #lancaigang240319：切完后，先吐掉残留喷头的线材，防止切成米粒
            self.G_PhrozenFluiddRespondInfo("外部宏命令-PG110；STM32进料之后，klipper开始吐料接住进料")
            self.PG102Flag=True
            self.IfDoPG102Flag=True
            self.G_PhrozenFluiddRespondInfo("self.Flag=True")
            command_string = """
            PG110
            """
            self.G_PhrozenGCode.run_script_from_command(command_string)
            self.G_PhrozenFluiddRespondInfo("command_string='%s'" % command_string)
            self.PG102Flag=False
            self.G_PhrozenFluiddRespondInfo("self.Flag=False")

        self.G_PhrozenFluiddRespondInfo("self.G_ToolheadIfHaveFilaFlag=%d" % (self.G_ToolheadIfHaveFilaFlag))
        # #lancaigang240328：手动命令不执行吐料
        # if self.ManualCmdFlag==True:
        #     self.G_PhrozenFluiddRespondInfo("[(cmds.python)]外部宏命令-PG110；手动命令，不执行")
        # else:
        #     #lancaigang240319：切完后，先吐掉残留喷头的线材，防止切成米粒
        #     self.G_PhrozenFluiddRespondInfo("[(cmds.python)]外部宏命令-PG110；STM32进料之后，klipper马上开始吐料")
        #     self.PG102Flag=True
        #     self.G_PhrozenFluiddRespondInfo("[(dev.python)]self.Flag=True")
        #     command_string = """
        #     PG110
        #     """
        #     self.G_PhrozenGCode.run_script_from_command(command_string)
        #     self.G_PhrozenFluiddRespondInfo("[(cmds.python)]command_string='%s'" % command_string)
        #     self.PG102Flag=False
        #     self.G_PhrozenFluiddRespondInfo("[(dev.python)]self.Flag=False")

        

        # #lancaigang240226：切线后AMS主板回退线材，延时后喷头回抽20mm
        # time.sleep(2)
        # #lancaigang231208：E头-负数回退，挤出头回抽线材
        # command_string = """
        # G92 E0
        # G1 E0.0000 F600
        # G91
        # G1 E-50 F8000
        # """
        # self.G_PhrozenGCode.run_script_from_command(command_string)
        # self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_P1TnManualChangeChannel]延时2s；E负数喷头回抽线材50mm;GCODE命令:command_string='%s'" % command_string)


        #lancaigang20231013：8
        #lancaigang231115：暂时不使用printer.cfg配置的超时时间，使用python内部默认定义超时时间
        timeout = self.G_DictChangeChannelWaitAreaParam["T"] - 8

        # #lancaigang240125：等待换料期间，z轴抬升后再下降
        # #lancaigang231208：z轴+正数会往上
        # command_string = """
        #     G91
        #     G1 Z%f F8000
        #     """ % (
        #     self.G_AMSFilaCutZPositionLiftingUp,
        # )
        # self.G_PhrozenGCode.run_script_from_command(command_string)
        # self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_P1TnManualChangeChannel]Z轴上拉升高;gcode命令=%s" % command_string)


        #lancaigang240619：
        # #lancaigang240306：移动到切线代码中
        # #lancaigang240110：等待区域等待之前，先执行外部宏命令，移动到特定位置进行等待
        # self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_P1TnManualChangeChannel]外部宏命令-PG101")
        # command_string = """
        #     PG101
        #     """
        # self.G_PhrozenGCode.run_script_from_command(command_string)
        # self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_P1TnManualChangeChannel]外部宏命令；command_string='%s'" % command_string)
        # self.IfDoPG102Flag=True


        #lancaigang240223：因为恢复的时候，直接跑到P9等待区，不抬升可能会导致刮到模型
        command_string = """
                        G90
                        G91
                        G1 Z%f F8000
                        """ % (
                        self.G_AMSFilaCutZPositionLiftingUp,
                    )
        self.G_PhrozenGCode.run_script_from_command(command_string)
        self.Lo_ThisIfZPositionLiftUpFlag = True
        self.G_PhrozenFluiddRespondInfo("Z轴临时抬升；command_string='%s'" % command_string)

        #lancaigang240325:
        #self.G_ResumeProcessCheckPauseStatus=False


        #lancaigang250519:
        self.G_PhrozenFluiddRespondInfo("外部宏命令-PRZ_SPITTING_SCRAPE")
        command_string = """
            PRZ_SPITTING_SCRAPE
            """
        self.G_PhrozenGCode.run_script_from_command(command_string)
        self.G_PhrozenFluiddRespondInfo("外部宏命令-刮料；command_string='%s'" % command_string)

        self.G_PhrozenFluiddRespondInfo("self.G_ToolheadIfHaveFilaFlag=%d" % (self.G_ToolheadIfHaveFilaFlag))
        #置位标签
        Lo_ChangeChannelIfSuccess = False
        #lancaigang250607：打印状态；1-退料中；2-进料中；3-打印中；4-暂停
        self.G_KlipperPrintStatus= 2
        #lancaigang20231013：超时时间
        #lancaigang231114：不在printer.cfg配置文件更改换料超时时间，这里直接更改timeout
        #循环检测第2次进料的线材是否到喷头
        for i in range(CHANGE_CHANNEL_WAIT_TIMEOUT):
            # self.G_XBasePosition+=2
            # self.G_YBasePosition+=2
            #lancaigang240325：如果在恢复状态，可以不判断上报暂停状态
            #self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_P1TnManualChangeChannel]self.G_ResumeProcessCheckPauseStatus='%d'" % self.G_ResumeProcessCheckPauseStatus)
            if self.G_ChangeChannelResumeFlag==True:
                if self.STM32ReprotPauseFlag==1:
                    self.G_PhrozenFluiddRespondInfo("在恢复状态期间，检测到上次暂停")
                    if self.G_ResumeProcessCheckPauseStatus==True:
                        #lancaigang240430：挪到后面失败处理
                        #self.G_ResumeProcessCheckPauseStatus=False
                        self.G_PhrozenFluiddRespondInfo("有本次暂停状态上报，退出恢复过程")
                        self.G_ChangeChannelFirstFilaFlag=True
                        Lo_ChangeChannelIfSuccess = False


                        Lo_PauseStatus=self.G_PhrozenPrinterCancelPauseResume.get_status(None)
                        self.G_PhrozenFluiddRespondInfo("当前暂停状态-Lo_PauseStatus='%s'" % Lo_PauseStatus)
                        self.G_PhrozenFluiddRespondInfo("Lo_PauseStatus['is_paused']='%s'" % Lo_PauseStatus['is_paused'])
                        #// 当前暂停状态-Lo_PauseStatus='{'is_paused': True}'
                        if Lo_PauseStatus['is_paused'] == True:
                            self.G_PhrozenFluiddRespondInfo("已是暂停状态")
                        else:
                            self.G_PhrozenFluiddRespondInfo("未暂停状态")

                        break
                    #else:
                        #self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_P1TnManualChangeChannel]没有本次暂停状态上报，继续恢复过程")

            else:
                #lancaigang231202：如果STM32主动上报暂停，需要klipper暂停
                if self.STM32ReprotPauseFlag==1:
                    self.G_ChangeChannelFirstFilaFlag=True
                    self.G_PhrozenFluiddRespondInfo("等待换料期间，stm32主动上报了暂停")
                    Lo_ChangeChannelIfSuccess = False


                    Lo_PauseStatus=self.G_PhrozenPrinterCancelPauseResume.get_status(None)
                    self.G_PhrozenFluiddRespondInfo("当前暂停状态-Lo_PauseStatus='%s'" % Lo_PauseStatus)
                    self.G_PhrozenFluiddRespondInfo("Lo_PauseStatus['is_paused']='%s'" % Lo_PauseStatus['is_paused'])
                    #// 当前暂停状态-Lo_PauseStatus='{'is_paused': True}'
                    if Lo_PauseStatus['is_paused'] == True:
                        self.G_PhrozenFluiddRespondInfo("已是暂停状态")
                    else:
                        self.G_PhrozenFluiddRespondInfo("未暂停状态")

                    break
            

            # #lancaigang231216：
            # if self.G_XBasePosition==0 and self.G_YBasePosition==0:
            #     self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_P1TnManualChangeChannel]等待换料期间，基坐标XY为0")
            #     command_string = """
            #         G90
            #         G1 X%.03f Y%.03f F5000
            #         """ % (
            #         150+(i%2),
            #         260+(i%2)
            #     )
            #     #lancaigang231129：缓慢来回移动
            #     self.G_PhrozenGCode.run_script_from_command(command_string)
            # else:
            #     #lancaigang231216：恢复的时候，需要来回运动防止漏料生成一个坑
            #     #lancaigang231214：等待区域基点X Y以W H长方形步长来回移动，实现吐料功能
            #     command_string = """
            #         G90
            #         G1 X%.03f Y%.03f F5000
            #         """ % (
            #         self.G_XBasePosition+(i%2),
            #         self.G_YBasePosition+(i%2)
            #     )
            #     #lancaigang231129：缓慢来回移动
            #     self.G_PhrozenGCode.run_script_from_command(command_string)
            #     self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_P1TnManualChangeChannel]等待换料期间，基坐标XY为P9配置")
            #     #self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_P1TnManualChangeChannel]等待来回运动；command_string='%s'" % command_string)
            
            
            #self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_P1TnManualChangeChannel]等待换料期间，使用外部宏命令")


            #lancaigang240223：因为恢复的时候，直接跑到P9等待区，不抬升可能会导致刮到模型，只抬升一次和下降一次
            if self.Lo_ThisIfZPositionLiftUpFlag == True:
                command_string = """
                                G90
                                G91
                                G1 Z-%f F8000
                                """ % (
                                self.G_AMSFilaCutZPositionLiftingUp,
                            )
                self.G_PhrozenGCode.run_script_from_command(command_string)
                self.Lo_ThisIfZPositionLiftUpFlag = False
                self.G_PhrozenFluiddRespondInfo("Z轴临时下降；command_string='%s'" % command_string)

            #lancaigang20231013：改为4秒延时
            #lancaigang231115：改为1s
            self.G_ProzenToolhead.dwell(1)
            #lancaigang240125：不能用sleep，会阻塞主线程
            #time.sleep(1)


            self.G_PhrozenFluiddRespondInfo("self.G_ToolheadIfHaveFilaFlag=%d" % (self.G_ToolheadIfHaveFilaFlag))

            self.G_PhrozenFluiddRespondInfo("外部宏命令-PG110；STM32进料之后，klipper开始吐料接住进料")
            command_string = """
            PG110
            """
            self.G_PhrozenGCode.run_script_from_command(command_string)
            self.G_PhrozenFluiddRespondInfo("command_string='%s'" % command_string)


            
            self.G_PhrozenFluiddRespondInfo("当前模式")
            if self.G_AMSDeviceWorkMode == AMS_WORK_MODE_UNKNOW:
                self.G_PhrozenFluiddRespondInfo("+Mode:0,unkown")
            elif self.G_AMSDeviceWorkMode == AMS_WORK_MODE_MC:
                self.G_PhrozenFluiddRespondInfo("+Mode:1,MC")
            elif self.G_AMSDeviceWorkMode == AMS_WORK_MODE_MA:
                self.G_PhrozenFluiddRespondInfo("+Mode:2,MA")
            elif self.G_AMSDeviceWorkMode == AMS_WORK_MODE_FILA_RUNOUT:
                self.G_PhrozenFluiddRespondInfo("+Mode:3,RUNOUT")
            else:
                self.G_PhrozenFluiddRespondInfo("+Mode:-1,error")


            Lo_PauseStatus=self.G_PhrozenPrinterCancelPauseResume.get_status(None)
            self.G_PhrozenFluiddRespondInfo("当前暂停状态-Lo_PauseStatus='%s'" % Lo_PauseStatus)
            self.G_PhrozenFluiddRespondInfo("Lo_PauseStatus['is_paused']='%s'" % Lo_PauseStatus['is_paused'])
            #// 当前暂停状态-Lo_PauseStatus='{'is_paused': True}'
            if Lo_PauseStatus['is_paused'] == True:
                self.G_PhrozenFluiddRespondInfo("已是暂停状态")
            else:
                self.G_PhrozenFluiddRespondInfo("未暂停状态")



            #self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_P1TnManualChangeChannel]i=%d;T=%d" % (i,self.G_ChangeChannelTimeoutNewChan))

            #检测新通道线材进料，是否有线材到喷头
            if self.G_ToolheadIfHaveFilaFlag:
                Lo_ChangeChannelIfSuccess = True
                break

        # #lancaigang240125：等待换料期间，z轴抬升后再下降
        # command_string = """
        #     G91
        #     G1 -Z%f F8000
        #     """ % (
        #     self.G_AMSFilaCutZPositionLiftingUp,
        # )
        # self.G_PhrozenGCode.run_script_from_command(command_string)
        # self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_P1TnManualChangeChannel]Z轴下降;gcode命令=%s" % command_string)




        #lancaigang240318：防止异常上升没下降
        if self.Lo_ThisIfZPositionLiftUpFlag == True:
            command_string = """
                            G90
                            G91
                            G1 Z-%f F8000
                            """ % (
                            self.G_AMSFilaCutZPositionLiftingUp,
                        )
            self.G_PhrozenGCode.run_script_from_command(command_string)
            self.Lo_ThisIfZPositionLiftUpFlag = False
            self.G_PhrozenFluiddRespondInfo("Z轴临时下降；command_string='%s'" % command_string)


        self.G_PhrozenFluiddRespondInfo("self.G_ToolheadIfHaveFilaFlag=%d" % (self.G_ToolheadIfHaveFilaFlag))

        #正常换料；换料成功
        if Lo_ChangeChannelIfSuccess:
            self.G_PhrozenFluiddRespondInfo("换料成功: T%d" % self.G_ChangeChannelTimeoutNewChan)
            self.G_IfChangeFilaOngoing= False

            #lancaigang250424：防止AMS缓冲器还么有顶满
            self.G_ProzenToolhead.dwell(0.5)

            #lancaigang250619:检查AMS是否重新连接成功
            self.Cmds_USBConnectErrorCheck()
            #lancaigang250423：进料成功，开始吐料，通知AMS开始计时，如果吐料超过5秒缓冲器还是慢状态，说明堵头了
            #self.Cmds_AMSSerial2Send("AT+EBLOCKCHECK")
            #self.G_PhrozenFluiddRespondInfo("AMS开始计时缓冲器满时间")
            if self.G_SerialPort1OpenFlag == True:
                self.Cmds_AMSSerial1Send("AT+EBLOCKCHECK")
                self.G_PhrozenFluiddRespondInfo("串口1-AMS开始计时缓冲器满时间")
            if self.G_SerialPort2OpenFlag == True:
                self.Cmds_AMSSerial2Send("AT+EBLOCKCHECK")
                self.G_PhrozenFluiddRespondInfo("串口2-AMS开始计时缓冲器满时间")
            self.G_ProzenToolhead.dwell(1)

            #lancaigang240229:
            if self.IfDoPG102Flag==True:
                self.IfDoPG102Flag=False

                self.G_PhrozenFluiddRespondInfo("吐料开始")
                self.G_PhrozenFluiddRespondInfo("+MSG:1,0,%d,%d" % (self.G_ChangeChannelTimeoutOldChan,self.G_ChangeChannelTimeoutNewChan))

                #lancaigang240328：手动命令不执行吐料
                if self.ManualCmdFlag==True:
                    self.G_PhrozenFluiddRespondInfo("外部宏命令-PG102；手动命令，不执行吐料功能")
                    #lancaigang250409：手動進料則讀取AMS狀態
                    self.Cmds_CmdP114(None)
                else:
                    # self.G_PhrozenFluiddRespondInfo("外部宏命令-PG102")
                    # self.PG102Flag=True
                    # self.G_PhrozenFluiddRespondInfo("self.Flag=True")
                    # command_string = """
                    # PG102
                    # """
                    # self.G_PhrozenGCode.run_script_from_command(command_string)
                    # self.G_PhrozenFluiddRespondInfo("外部宏命令-排废料；command_string='%s'" % command_string)

                    #lancaigang241031：控制吐料次数
                    if self.G_P10SpitNum==0:
                        self.G_PhrozenFluiddRespondInfo("外部宏命令-PG113")
                        self.PG102Flag=True
                        self.G_PhrozenFluiddRespondInfo("self.Flag=True")
                        command_string = """
                        PG114
                        """
                        self.G_PhrozenGCode.run_script_from_command(command_string)
                        self.G_PhrozenFluiddRespondInfo("外部宏命令-排废料；command_string='%s'" % command_string)
                    elif self.G_P10SpitNum==1:
                        self.G_PhrozenFluiddRespondInfo("外部宏命令-PG111")
                        self.PG102Flag=True
                        self.G_PhrozenFluiddRespondInfo("self.Flag=True")
                        command_string = """
                        PG114
                        """
                        self.G_PhrozenGCode.run_script_from_command(command_string)
                        self.G_PhrozenFluiddRespondInfo("外部宏命令-排废料；command_string='%s'" % command_string)
                    elif self.G_P10SpitNum==2:
                        self.G_PhrozenFluiddRespondInfo("外部宏命令-PG112")
                        self.PG102Flag=True
                        self.G_PhrozenFluiddRespondInfo("self.Flag=True")
                        command_string = """
                        PG113
                        """
                        self.G_PhrozenGCode.run_script_from_command(command_string)
                        self.G_PhrozenFluiddRespondInfo("外部宏命令-排废料；command_string='%s'" % command_string)
                    elif self.G_P10SpitNum==3:
                        self.G_PhrozenFluiddRespondInfo("外部宏命令-PG113")
                        self.PG102Flag=True
                        self.G_PhrozenFluiddRespondInfo("self.Flag=True")
                        command_string = """
                        PG113
                        """
                        self.G_PhrozenGCode.run_script_from_command(command_string)
                        self.G_PhrozenFluiddRespondInfo("外部宏命令-排废料；command_string='%s'" % command_string)
                    elif self.G_P10SpitNum==4:
                        self.G_PhrozenFluiddRespondInfo("外部宏命令-PG114")
                        self.PG102Flag=True
                        self.G_PhrozenFluiddRespondInfo("self.Flag=True")
                        command_string = """
                        PG114
                        """
                        self.G_PhrozenGCode.run_script_from_command(command_string)
                        self.G_PhrozenFluiddRespondInfo("外部宏命令-排废料；command_string='%s'" % command_string)
                    elif self.G_P10SpitNum==5:
                        self.G_PhrozenFluiddRespondInfo("外部宏命令-PG115")
                        self.PG102Flag=True
                        self.G_PhrozenFluiddRespondInfo("self.Flag=True")
                        command_string = """
                        PG115
                        """
                        self.G_PhrozenGCode.run_script_from_command(command_string)
                        self.G_PhrozenFluiddRespondInfo("外部宏命令-排废料；command_string='%s'" % command_string)
                    #lancaigang250528：
                    elif self.G_P10SpitNum==6:
                        self.G_PhrozenFluiddRespondInfo("外部宏命令-PG116")
                        self.PG102Flag=True
                        self.G_PhrozenFluiddRespondInfo("self.Flag=True")
                        command_string = """
                        PG116
                        """
                        self.G_PhrozenGCode.run_script_from_command(command_string)
                        self.G_PhrozenFluiddRespondInfo("外部宏命令-排废料；command_string='%s'" % command_string)
                    elif self.G_P10SpitNum==7:
                        self.G_PhrozenFluiddRespondInfo("外部宏命令-PG117")
                        self.PG102Flag=True
                        self.G_PhrozenFluiddRespondInfo("self.Flag=True")
                        command_string = """
                        PG117
                        """
                        self.G_PhrozenGCode.run_script_from_command(command_string)
                        self.G_PhrozenFluiddRespondInfo("外部宏命令-排废料；command_string='%s'" % command_string)
                    elif self.G_P10SpitNum==8:
                        self.G_PhrozenFluiddRespondInfo("外部宏命令-PG118")
                        self.PG102Flag=True
                        self.G_PhrozenFluiddRespondInfo("self.Flag=True")
                        command_string = """
                        PG118
                        """
                        self.G_PhrozenGCode.run_script_from_command(command_string)
                        self.G_PhrozenFluiddRespondInfo("外部宏命令-排废料；command_string='%s'" % command_string)
                    elif self.G_P10SpitNum==9:
                        self.G_PhrozenFluiddRespondInfo("外部宏命令-PG119")
                        self.PG102Flag=True
                        self.G_PhrozenFluiddRespondInfo("self.Flag=True")
                        command_string = """
                        PG119
                        """
                        self.G_PhrozenGCode.run_script_from_command(command_string)
                        self.G_PhrozenFluiddRespondInfo("外部宏命令-排废料；command_string='%s'" % command_string)


                    self.PG102Flag=False
                    self.G_PhrozenFluiddRespondInfo("self.Flag=False")

                self.G_PhrozenFluiddRespondInfo("吐料结束")
                self.G_PhrozenFluiddRespondInfo("+MSG:1,1,%d,%d" % (self.G_ChangeChannelTimeoutOldChan,self.G_ChangeChannelTimeoutNewChan))


                #lancaigang240323：导致第一层掉落残料，先屏蔽
                # #lancaigang240321：吐料完成后，移动到热床中央，防止恢复的时候从Y305位置直接到暂停点，导致喷头MCU心跳包异常崩溃
                # self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_P1TnManualChangeChannel]外部宏命令-PG105；移动到热床中央，防止恢复路径过长")
                # command_string = """
                # PG105
                # """
                # self.G_PhrozenGCode.run_script_from_command(command_string)
                # self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_P1TnManualChangeChannel]外部宏命令-PG105；移动到热床中央，防止恢复路径过长；command_string='%s'" % command_string)
                


                # for i in range(15):
                #     self.G_PhrozenFluiddRespondInfo("[(dev.python)]吐料中，等待")
                #     #lancaigang20231013：改为4秒延时
                #     #lancaigang231115：改为1s
                #     self.G_ProzenToolhead.dwell(1.0)
                #     #lancaigang240125：不能用sleep，会阻塞主线程
                #     #time.sleep(1)
                if self.PG102DelayPauseFlag==True:
                    self.PG102DelayPauseFlag=False

                    #lancaigang250619:检查AMS是否重新连接成功
                    self.Cmds_USBConnectErrorCheck()
                    #lancaigang250427：
                    if self.G_SerialPort1OpenFlag == True:
                        self.Cmds_AMSSerial1Send("AT+EBLOCKEND")
                        self.G_PhrozenFluiddRespondInfo("串口1-AMS结束计时缓冲器满时间")
                    if self.G_SerialPort2OpenFlag == True:
                        self.Cmds_AMSSerial2Send("AT+EBLOCKEND")
                        self.G_PhrozenFluiddRespondInfo("串口2-AMS结束计时缓冲器满时间")

                    self.G_PhrozenFluiddRespondInfo("启用快速暂停")
                    self.G_KlipperQuickPause = True
                    self.G_PhrozenFluiddRespondInfo("吐料过程中，STM32触发了断料暂停")
                    #lancaigang231209：定时器中处理业务，会导致业务异常，后面要用线程处理中断业务
                    self.G_PhrozenFluiddRespondInfo("stm32主动暂停上报，暂停1次")


                    

                    if self.G_KlipperInPausing == False:
                        self.G_PhrozenFluiddRespondInfo("不在暂停中，允许新的暂停")
                        #lancaigang250607:
                        self.G_PhrozenFluiddRespondInfo("启用快速暂停")
                        self.G_KlipperQuickPause = True
                        #klipper主动暂停
                        self.Cmds_PhrozenKlipperPauseNoneCmdToSTM32(None)
                    else:
                        self.G_PhrozenFluiddRespondInfo("暂停中，不允许新的暂停")




                    self.G_KlipperIfPaused = True
                    #stm32主动暂停只能暂停1次，不能重复暂停
                    self.STM32ReprotPauseFlag=1
                    #lancaigang231202：P1 C?自动换料时，如果第1次通道就进料异常暂停，如果要恢复，也继续从第1次通道开始
                    self.G_ChangeChannelFirstFilaFlag=True
                    
                    self.G_ProzenToolhead.dwell(1.5)
                    self.G_PhrozenFluiddRespondInfo("+MSG:1,1,%d,%d" % (self.G_ChangeChannelTimeoutOldChan,self.G_ChangeChannelTimeoutNewChan))
                    #lancaigang240524：用于UIUX动态界面
                    self.G_PhrozenFluiddRespondInfo("+C:1,%d" % self.G_ChangeChannelTimeoutNewChan)
                    
                    #self.G_PhrozenFluiddRespondInfo(self.G_PauseToLCDString)

                    #lancaigang250529:
                    if len(self.G_PauseToLCDString)==0:
                        self.G_PhrozenFluiddRespondInfo("+PAUSE:4,%d,%d" % (self.G_ChangeChannelTimeoutOldChan,self.G_ChangeChannelTimeoutNewChan))
                    else:
                        self.G_PhrozenFluiddRespondInfo(self.G_PauseToLCDString)


                    #lancaigang250607：打印状态；1-退料中；2-进料中；3-打印中；4-暂停
                    self.G_KlipperPrintStatus= 3
                    self.G_PauseToLCDString=""
                    
                    self.G_PhrozenFluiddRespondInfo("return")
                    return
                else:
                    #lancaigang240325:为了兼容暂停，统一使用暂停1
                    if self.G_PauseTriggerWhileChangeChannelFlag==True:
                        #lancaigang231209：定时器中处理业务，会导致业务异常，后面要用线程处理中断业务
                        self.G_PhrozenFluiddRespondInfo("吐料过程中，STM32触发了暂停")
                        #self.G_PhrozenFluiddRespondInfo("+PAUSE:1,%d" % self.G_ChangeChannelTimeoutNewChan)
                        #self.G_PhrozenFluiddRespondInfo(self.G_PauseToLCDString)
                        #lancaigang250529:
                        if len(self.G_PauseToLCDString)==0:
                            self.G_PhrozenFluiddRespondInfo("+PAUSE:4,%d,%d" % (self.G_ChangeChannelTimeoutOldChan,self.G_ChangeChannelTimeoutNewChan))
                        else:
                            self.G_PhrozenFluiddRespondInfo(self.G_PauseToLCDString)
                        #lancaigang240325：换料失败，不能执行恢复
                        self.G_MCModeCanResumeFlag = False
                        #lancaigang250527：暂停快速执行
                        self.G_KlipperQuickPause = False
                    else:
                        #lancaigang240325：换料成功，能执行恢复
                        self.G_MCModeCanResumeFlag = True
                        self.G_PhrozenFluiddRespondInfo("吐料过程正常，进入打印")
                        #lancaigang250527：暂停快速执行
                        self.G_KlipperQuickPause = True
            else:
                #lancaigang240325：换料成功，能执行恢复
                self.G_MCModeCanResumeFlag = True
                #lancaigang250527：暂停快速执行
                #self.G_KlipperQuickPause = True
            #lancaigang250619:检查AMS是否重新连接成功
            self.Cmds_USBConnectErrorCheck()
            #lancaigang250427：
            if self.G_SerialPort1OpenFlag == True:
                self.Cmds_AMSSerial1Send("AT+EBLOCKEND")
                self.G_PhrozenFluiddRespondInfo("串口1-AMS结束计时缓冲器满时间")
            if self.G_SerialPort2OpenFlag == True:
                self.Cmds_AMSSerial2Send("AT+EBLOCKEND")
                self.G_PhrozenFluiddRespondInfo("串口2-AMS结束计时缓冲器满时间")
            self.G_ProzenToolhead.dwell(1.5)
            
            # #lancaigang240318：防止异常上升没下降
            # if self.Lo_ThisIfZPositionLiftUpFlag == True:
            #     command_string = """
            #                     G90
            #                     G91
            #                     G1 Z-%f F8000
            #                     """ % (
            #                     self.G_AMSFilaCutZPositionLiftingUp,
            #                 )
            #     self.G_PhrozenGCode.run_script_from_command(command_string)
            #     self.Lo_ThisIfZPositionLiftUpFlag = False
            #     self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_P1TnManualChangeChannel]Z轴临时下降；command_string='%s'" % command_string)

            self.G_ResumeProcessCheckPauseStatus=False
            #lancaigang240524：用于UIUX动态界面
            self.G_PhrozenFluiddRespondInfo("+T:1,%d" % self.G_ChangeChannelTimeoutNewChan)

            #lancaigang250607：打印状态；1-退料中；2-进料中；3-打印中；4-暂停
            self.G_KlipperPrintStatus= 3

            self.G_PauseToLCDString=""

            return
        

        self.G_PhrozenFluiddRespondInfo("self.G_ToolheadIfHaveFilaFlag=%d" % (self.G_ToolheadIfHaveFilaFlag))

        # 换料失败
        if self.G_DictChangeChannelWaitAreaParam["A"] == 0:
            #lancaigang250619:检查AMS是否重新连接成功
            self.Cmds_USBConnectErrorCheck()

            # self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_P1TnManualChangeChannel]换料失败；线材进料到喷头超时；cmd='%s', 全部回退线材，klipper暂停" % (gcmd.get_commandline()))
            # #// 全部后退到停靠位；//===== P2 A1 所有线料退到停靠位待打印 Yes；"AP"；
            # self.Cmds_AMSSerial1Send("AP")
            # self.G_PhrozenFluiddRespondInfo("发送命令: AP，全部后退到停靠位")
            #lancaigang231209：stm32主动上报则不上报9
            if self.G_KlipperIfPaused==False:
                #lancaigang240328：如果是手动命令，不暂停
                if self.ManualCmdFlag==True:
                    self.G_PhrozenFluiddRespondInfo("手动命令，klipper不执行暂停")
                    #lancaigang250409：手動進料則讀取AMS狀態
                    self.Cmds_CmdP114(None)
                elif self.G_CutCheckTest==True:
                    self.G_PhrozenFluiddRespondInfo("切刀测试命令，klipper不执行暂停")
                    #lancaigang250409：手動進料則讀取AMS狀態
                    self.Cmds_CmdP114(None)
                else:
                    #lancaigang250702：
                    if self.G_KlipperInPausing == False:
                        self.G_PhrozenFluiddRespondInfo("不在暂停中，允许新的暂停")
                        self.STM32ReprotPauseFlag=1
                        #lancaigang231202：P1 C?自动换料时，如果第1次通道就进料异常暂停，如果要恢复，也继续从第1次通道开始
                        self.G_ChangeChannelFirstFilaFlag=True

                        self.G_PhrozenFluiddRespondInfo("换料超时60s，暂停")
                        #self.G_PhrozenFluiddRespondInfo("+PAUSE:4,%d,%d" % (self.G_ChangeChannelTimeoutOldChan,self.G_ChangeChannelTimeoutNewChan))
                        
                        #lancaigang240416:
                        if self.G_SerialPort1OpenFlag == True:
                            #lancaigang240603：防止AMS一直停不了
                            self.Cmds_AMSSerial1Send("AT+PAUSE")
                            self.G_PhrozenFluiddRespondInfo("串口1-AT+PAUSE暂停stm32电机")
                        #lancaigang241030:
                        if self.G_SerialPort2OpenFlag == True:
                            self.Cmds_AMSSerial2Send("AT+PAUSE")
                            self.G_PhrozenFluiddRespondInfo("串口2-AT+PAUSE暂停stm32电机")

                        self.G_PhrozenFluiddRespondInfo("启用快速暂停")
                        self.G_KlipperQuickPause = True
                        #klipper主动暂停
                        self.Cmds_PhrozenKlipperPause(None)
                        self.G_KlipperIfPaused = True

                        #lancaigang250529:
                        if len(self.G_PauseToLCDString)==0:
                            self.G_PhrozenFluiddRespondInfo("+PAUSE:4,%d,%d" % (self.G_ChangeChannelTimeoutOldChan,self.G_ChangeChannelTimeoutNewChan))
                        else:
                            self.G_PhrozenFluiddRespondInfo(self.G_PauseToLCDString)

                        #lancaigang240325：换料失败，不能执行恢复
                        self.G_MCModeCanResumeFlag = False
                        #lancaigang250527：暂停快速执行
                        self.G_KlipperQuickPause = False
                    else:
                        self.G_PhrozenFluiddRespondInfo("暂停中，不允许新的暂停")
            #lancaigang240124：不能重复暂停
            else:
                self.G_PhrozenFluiddRespondInfo("已经暂停了，不用重复暂停")
                #lancaigang240509：屏蔽
                # #lancaigang240326：上报暂停
                # #self.G_PhrozenFluiddRespondInfo(self.G_PauseToLCDString)
                # if len(self.G_PauseToLCDString)==0:
                #     self.G_PhrozenFluiddRespondInfo("+PAUSE:4,%d" % self.G_ChangeChannelTimeoutNewChan)
                #lancaigang240417：防止stm32没上报时G_PauseToLCDString为空的情况
                #self.G_PhrozenFluiddRespondInfo("+PAUSE:4,%d" % self.G_ChangeChannelTimeoutNewChan)
                #lancaigang240325：换料失败，不能执行恢复
                self.G_MCModeCanResumeFlag = False
                #lancaigang250527：暂停快速执行
                self.G_KlipperQuickPause = False

                #lancaigang240429：如果恢复过程中stm32并没有上报暂停状态，这里需要上报暂停
                if self.G_ResumeProcessCheckPauseStatus==False:
                    self.G_PhrozenFluiddRespondInfo("AMS没有上报暂停，klipper重复暂停，需要上报暂停")
                    #lancaigang250529:
                    if len(self.G_PauseToLCDString)==0:
                        self.G_PhrozenFluiddRespondInfo("+PAUSE:4,%d,%d" % (self.G_ChangeChannelTimeoutOldChan,self.G_ChangeChannelTimeoutNewChan))
                    else:
                        self.G_PhrozenFluiddRespondInfo(self.G_PauseToLCDString)
                    #lancaigang240416:
                    if self.G_SerialPort1OpenFlag == True:
                        #lancaigang240603：防止AMS一直停不了
                        self.Cmds_AMSSerial1Send("AT+PAUSE")
                        self.G_PhrozenFluiddRespondInfo("串口1-AT+PAUSE暂停stm32电机")
                    #lancaigang241030:
                    if self.G_SerialPort2OpenFlag == True:
                        self.Cmds_AMSSerial2Send("AT+PAUSE")
                        self.G_PhrozenFluiddRespondInfo("串口2-AT+PAUSE暂停stm32电机")
                else:#True
                    self.G_PhrozenFluiddRespondInfo("AMS有上报暂停，klipper不需要需要上报暂停")
                    self.G_ResumeProcessCheckPauseStatus=False

                    #lancaigang250529:
                    if len(self.G_PauseToLCDString)==0:
                        self.G_PhrozenFluiddRespondInfo("+PAUSE:4,%d,%d" % (self.G_ChangeChannelTimeoutOldChan,self.G_ChangeChannelTimeoutNewChan))
                    else:
                        self.G_PhrozenFluiddRespondInfo(self.G_PauseToLCDString)


                # self.G_PhrozenFluiddRespondInfo("已经暂停了，再暂停1次，防止之前暂停异常")
                # #lancaigang250423：为了防止异常暂停不住，多暂停1次
                # #klipper主动暂停
                # self.Cmds_PhrozenKlipperPause(None)

            #lancaigang231202：P1 C?自动换料时，如果第1次通道就进料异常暂停，如果要恢复，也继续从第1次通道开始
            self.G_ChangeChannelFirstFilaFlag=True

            self.G_IfChangeFilaOngoing= False

            self.G_ResumeProcessCheckPauseStatus=False
            #lancaigang240524：用于UIUX动态界面
            self.G_PhrozenFluiddRespondInfo("+T:1,%d" % self.G_ChangeChannelTimeoutNewChan)

            #lancaigang250607：打印状态；1-退料中；2-进料中；3-打印中；4-暂停
            self.G_KlipperPrintStatus= -1

            return

        #正常换料；Action正常
        if self.G_DictChangeChannelWaitAreaParam["A"] == 1:
            pass


    ####################################
    #函数名称：
    #输入参数：
    #返 回 值:
    #功能描述：蓝才刚-20230830
    ####################################
   # P1 C[n] n:1~32(设备无组网,取1~4) 自动换到指定通道(多动作命令,包含切线, 换线, 等待)
    def Cmds_P1CnAutoChangeChannel(self, chan, gcmd):
            #lancaigang241030：一般是P1 C1到P1 C32，范围在1到32
            #第1台：1 2 3 4
            #第2台：5 6 7 8
            #第3台：9 10 11 12
            #第4台：13 14 15 16
            #第5台：17 18 19 20
            #第6台：21 22 23 24
            #第7台：25 26 27 28
            #第8台：29 30 31 32
        self.G_PhrozenFluiddRespondInfo("=====[(cmds.python)Cmds_P1CnAutoChangeChannel]")
        self.G_PhrozenFluiddRespondInfo("=====上一次换料self.G_ChangeChannelTimeoutOldChan=%d" % self.G_ChangeChannelTimeoutOldChan)
        self.G_PhrozenFluiddRespondInfo("=====上一次换料self.G_ChangeChannelTimeoutNewChan=%d" % self.G_ChangeChannelTimeoutNewChan)
        if gcmd is None:
            self.G_PhrozenFluiddRespondInfo("gcmd is None")
            #self.G_PhrozenFluiddRespondInfo("return")
            #return
            #pass
        if gcmd is not None:
            self.G_PhrozenFluiddRespondInfo("gcmd is not None:")
            self.G_PhrozenFluiddRespondInfo("=====上一次换料'%s';self.G_ChangeChannelTimeoutOldChan=%d" % (gcmd.get_commandline(),self.G_ChangeChannelTimeoutOldChan))
            self.G_PhrozenFluiddRespondInfo("=====上一次换料'%s';self.G_ChangeChannelTimeoutNewChan=%d" % (gcmd.get_commandline(),self.G_ChangeChannelTimeoutNewChan))
        
        self.G_PhrozenFluiddRespondInfo("self.G_ToolheadIfHaveFilaFlag=%d" % (self.G_ToolheadIfHaveFilaFlag))




        #lancaigang250824:
        self.G_PhrozenFluiddRespondInfo("self.G_ProzenToolhead.wait_moves()")
        self.G_ProzenToolhead.wait_moves()





        # #cancel取消命令
        # self.G_PhrozenPrinterCancelPauseResume.cmd_CANCEL_PRINT(None)
        #lancaigang250517：
        Lo_PauseStatus=self.G_PhrozenPrinterCancelPauseResume.get_status(None)
        self.G_PhrozenFluiddRespondInfo("当前暂停状态-Lo_PauseStatus='%s'" % Lo_PauseStatus)
        self.G_PhrozenFluiddRespondInfo("Lo_PauseStatus['is_paused']='%s'" % Lo_PauseStatus['is_paused'])
        #// 当前暂停状态-Lo_PauseStatus='{'is_paused': True}'
        if Lo_PauseStatus['is_paused'] == True:
            self.G_PhrozenFluiddRespondInfo("已是暂停状态")
        else:
            self.G_PhrozenFluiddRespondInfo("未暂停状态")

        self.G_PhrozenFluiddRespondInfo("当前模式")
        if self.G_AMSDeviceWorkMode == AMS_WORK_MODE_UNKNOW:
            self.G_PhrozenFluiddRespondInfo("+Mode:0,unkown")
        elif self.G_AMSDeviceWorkMode == AMS_WORK_MODE_MC:
            self.G_PhrozenFluiddRespondInfo("+Mode:1,MC")
        elif self.G_AMSDeviceWorkMode == AMS_WORK_MODE_MA:
            self.G_PhrozenFluiddRespondInfo("+Mode:2,MA")
        elif self.G_AMSDeviceWorkMode == AMS_WORK_MODE_FILA_RUNOUT:
            self.G_PhrozenFluiddRespondInfo("+Mode:3,RUNOUT")
        else:
            self.G_PhrozenFluiddRespondInfo("+Mode:-1,error")


        #解锁
        self.Base_AMSSerialCmdUnlock()


        #lancaigang250605:
        if self.G_AMSDeviceWorkMode == AMS_WORK_MODE_UNKNOW:
            self.G_PhrozenFluiddRespondInfo("如果收到T?命令，但模式是未知模式，强制转换为MC多色模式")
            self.G_AMSDeviceWorkMode = AMS_WORK_MODE_MC

        self.G_PhrozenFluiddRespondInfo("当前模式")
        if self.G_AMSDeviceWorkMode == AMS_WORK_MODE_UNKNOW:
            self.G_PhrozenFluiddRespondInfo("+Mode:0,unkown")
        elif self.G_AMSDeviceWorkMode == AMS_WORK_MODE_MC:
            self.G_PhrozenFluiddRespondInfo("+Mode:1,MC")
        elif self.G_AMSDeviceWorkMode == AMS_WORK_MODE_MA:
            self.G_PhrozenFluiddRespondInfo("+Mode:2,MA")
        elif self.G_AMSDeviceWorkMode == AMS_WORK_MODE_FILA_RUNOUT:
            self.G_PhrozenFluiddRespondInfo("+Mode:3,RUNOUT")
        else:
            self.G_PhrozenFluiddRespondInfo("+Mode:-1,error")


        #lancaigang250526：暂停中，不允许新的gcode命令，需等待暂停完成
        if self.G_KlipperInPausing == True:
            self.G_PhrozenFluiddRespondInfo("暂停过程中，不允许新的gcode命令，需等待暂停完成")
            for num in range(30):
                #lancaigang231115：改为1s
                self.G_PhrozenFluiddRespondInfo("self.G_ProzenToolhead.dwell(1)")
                self.G_ProzenToolhead.dwell(1)
                self.G_PhrozenFluiddRespondInfo("暂停过程中，不允许新的gcode命令，需等待暂停完成")
                Lo_PauseStatus=self.G_PhrozenPrinterCancelPauseResume.get_status(None)
                self.G_PhrozenFluiddRespondInfo("当前暂停状态-Lo_PauseStatus='%s'" % Lo_PauseStatus)
                self.G_PhrozenFluiddRespondInfo("Lo_PauseStatus['is_paused']='%s'" % Lo_PauseStatus['is_paused'])
                
                #// 当前暂停状态-Lo_PauseStatus='{'is_paused': True}'
                if Lo_PauseStatus['is_paused'] == True:
                    self.G_PhrozenFluiddRespondInfo("已是暂停状态")
                else:
                    self.G_PhrozenFluiddRespondInfo("未暂停状态")

                if self.G_KlipperInPausing == False:
                    self.G_PhrozenFluiddRespondInfo("暂停结束")
                    Lo_ChangeChannelIfSuccess = True

                    Lo_PauseStatus=self.G_PhrozenPrinterCancelPauseResume.get_status(None)
                    self.G_PhrozenFluiddRespondInfo("当前暂停状态-Lo_PauseStatus='%s'" % Lo_PauseStatus)
                    self.G_PhrozenFluiddRespondInfo("Lo_PauseStatus['is_paused']='%s'" % Lo_PauseStatus['is_paused'])
                    #// 当前暂停状态-Lo_PauseStatus='{'is_paused': True}'
                    if Lo_PauseStatus['is_paused'] == True:
                        self.G_PhrozenFluiddRespondInfo("已是暂停状态")
                    else:
                        self.G_PhrozenFluiddRespondInfo("未暂停状态")
                        #klipper暂停命令；保存当前的x y z坐标
                        #lancaigang240108：要考虑多次暂停保存的数据是否正常，后续要验证
                        self.G_PhrozenGCode.run_script_from_command("SAVE_GCODE_STATE NAME=PAUSE")
                        self.G_PhrozenFluiddRespondInfo("[(cmds.python)]PAUSE")
                        self.G_PhrozenPrinterCancelPauseResume.send_pause_command()
                        self.G_ProzenToolhead.wait_moves()
                        self.G_ProzenToolhead.dwell(1.0)

                    self.G_PhrozenFluiddRespondInfo("break")
                    break

            #lancaigang250725：如果循环结束，还是没有执行完暂停宏，则马上执行暂停
            if self.G_KlipperInPausing == True:
                self.G_PhrozenFluiddRespondInfo("=====暂停过程中，收到了新的换色命令，但暂停还未完成，这里强制暂停")
                Lo_PauseStatus=self.G_PhrozenPrinterCancelPauseResume.get_status(None)
                self.G_PhrozenFluiddRespondInfo("当前暂停状态-Lo_PauseStatus='%s'" % Lo_PauseStatus)
                self.G_PhrozenFluiddRespondInfo("Lo_PauseStatus['is_paused']='%s'" % Lo_PauseStatus['is_paused'])
                #// 当前暂停状态-Lo_PauseStatus='{'is_paused': True}'
                if Lo_PauseStatus['is_paused'] == True:
                    self.G_PhrozenFluiddRespondInfo("已是暂停状态")
                else:
                    self.G_PhrozenFluiddRespondInfo("=====未暂停状态，执行暂停操作")
                    #klipper暂停命令；保存当前的x y z坐标
                    #lancaigang240108：要考虑多次暂停保存的数据是否正常，后续要验证
                    self.G_PhrozenGCode.run_script_from_command("SAVE_GCODE_STATE NAME=PAUSE")
                    self.G_PhrozenFluiddRespondInfo("[(cmds.python)]PAUSE")
                    self.G_PhrozenPrinterCancelPauseResume.send_pause_command()
                    self.G_ProzenToolhead.wait_moves()
                    self.G_ProzenToolhead.dwell(1.0)

        else:
            self.G_PhrozenFluiddRespondInfo("未在暂停中状态")
            self.G_PhrozenFluiddRespondInfo("self.G_KlipperInPausing == False")

        Lo_PauseStatus=self.G_PhrozenPrinterCancelPauseResume.get_status(None)
        self.G_PhrozenFluiddRespondInfo("当前暂停状态-Lo_PauseStatus='%s'" % Lo_PauseStatus)
        self.G_PhrozenFluiddRespondInfo("Lo_PauseStatus['is_paused']='%s'" % Lo_PauseStatus['is_paused'])
        #// 当前暂停状态-Lo_PauseStatus='{'is_paused': True}'
        if Lo_PauseStatus['is_paused'] == True:
            self.G_PhrozenFluiddRespondInfo("已是暂停状态")
        else:
            self.G_PhrozenFluiddRespondInfo("未暂停状态")

        #lancaigang250512：多暂停1次，防止之前没有暂停成功的情况
        if self.G_KlipperIfPaused == True:
            #不是恢复状态
            if self.G_ChangeChannelResumeFlag==False:
                self.G_PhrozenFluiddRespondInfo("不是恢复状态")
                self.G_PhrozenFluiddRespondInfo("klipper暂停了，但还收到命令")
                #lancaigang250508:防止暂停异常
                self.G_PhrozenFluiddRespondInfo("klipper暂停了，但还收到命令，再次暂停")
                self.G_PhrozenFluiddRespondInfo("+PAUSE:4,%d,%d" % (self.G_ChangeChannelTimeoutOldChan,self.G_ChangeChannelTimeoutNewChan))
                self.G_PauseToLCDString="+PAUSE:4,%d,%d" % (self.G_ChangeChannelTimeoutOldChan,self.G_ChangeChannelTimeoutNewChan)
                #self.Cmds_PhrozenKlipperPause(None)

                Lo_PauseStatus=self.G_PhrozenPrinterCancelPauseResume.get_status(None)
                self.G_PhrozenFluiddRespondInfo("当前暂停状态-Lo_PauseStatus='%s'" % Lo_PauseStatus)
                self.G_PhrozenFluiddRespondInfo("Lo_PauseStatus['is_paused']='%s'" % Lo_PauseStatus['is_paused'])
                #// 当前暂停状态-Lo_PauseStatus='{'is_paused': True}'
                if Lo_PauseStatus['is_paused'] == True:
                    self.G_PhrozenFluiddRespondInfo("已是暂停状态")
                else:
                    self.G_PhrozenFluiddRespondInfo("未暂停状态")
                    #klipper暂停命令；保存当前的x y z坐标
                    #lancaigang240108：要考虑多次暂停保存的数据是否正常，后续要验证
                    self.G_PhrozenGCode.run_script_from_command("SAVE_GCODE_STATE NAME=PAUSE")
                    self.G_PhrozenFluiddRespondInfo("[(cmds.python)]PAUSE")
                    self.G_PhrozenPrinterCancelPauseResume.send_pause_command()
                    self.G_ProzenToolhead.wait_moves()
                    self.G_ProzenToolhead.dwell(1.0)

                #lancaigang250524:
                self.G_PhrozenFluiddRespondInfo("暂停过程中，收到了新的gcode命令，也需要记录最新的新旧通道，防止混色")
                self.G_ChangeChannelTimeoutOldChan=self.G_ChangeChannelTimeoutNewChan
                self.G_PhrozenFluiddRespondInfo("=====self.G_ChangeChannelTimeoutOldChan=%d" % self.G_ChangeChannelTimeoutOldChan)
                self.G_ChangeChannelTimeoutOldGcmd=self.G_ChangeChannelTimeoutNewGcmd
                self.G_ChangeChannelTimeoutNewChan=chan
                self.G_PhrozenFluiddRespondInfo("=====self.G_ChangeChannelTimeoutNewChan=%d" % self.G_ChangeChannelTimeoutNewChan)
                self.G_ChangeChannelTimeoutNewGcmd=gcmd
                self.Cmds_PrintMode(self.G_AMSDeviceWorkMode)

                Lo_PauseStatus=self.G_PhrozenPrinterCancelPauseResume.get_status(None)
                self.G_PhrozenFluiddRespondInfo("当前暂停状态-Lo_PauseStatus='%s'" % Lo_PauseStatus)
                self.G_PhrozenFluiddRespondInfo("Lo_PauseStatus['is_paused']='%s'" % Lo_PauseStatus['is_paused'])
                #// 当前暂停状态-Lo_PauseStatus='{'is_paused': True}'
                if Lo_PauseStatus['is_paused'] == True:
                    self.G_PhrozenFluiddRespondInfo("已是暂停状态")
                else:
                    self.G_PhrozenFluiddRespondInfo("未暂停状态")

                self.G_PhrozenFluiddRespondInfo("return")
                return
            

       #lancaigang250619:检查AMS是否重新连接成功
        self.Cmds_USBConnectErrorCheck()
        if self.G_SerialPort1Obj is not None:
            if self.G_SerialPort1Obj.is_open:
                self.G_PhrozenFluiddRespondInfo("串口1已打开")
                #self.G_SerialPort1Obj.flushInput()
                #self.G_PhrozenFluiddRespondInfo("G_SerialPort1Obj.flushInput串口清空")
        if self.G_SerialPort2Obj is not None:
            #lancaigang241030:
            if self.G_SerialPort2Obj.is_open:
                self.G_PhrozenFluiddRespondInfo("串口2已打开")

        self.G_PhrozenFluiddRespondInfo("self.G_ToolheadIfHaveFilaFlag=%d" % (self.G_ToolheadIfHaveFilaFlag))

        #lancaigang240226：切线后AMS主板回退线材，延时后喷头回抽20mm
        #time.sleep(2)
        #self.G_ProzenToolhead.dwell(2.0)

        self.G_PauseTriggerWhileChangeChannelFlag=False
        self.G_PhrozenFluiddRespondInfo("+C:0,%d" % chan)

        self.G_ASM1DisconnectErrorCount=0



        # #lancaigang240322：暂停和换料同时发送，如果G?命令已经发现了断线暂停，直接返回
        # if self.STM32ReprotPauseFlag==1:
        #     self.G_PhrozenFluiddRespondInfo("self.G_ChangeChannelTimeoutNewChan=%d" % self.G_ChangeChannelTimeoutNewChan)
        #     self.G_PhrozenFluiddRespondInfo("self.G_Pause1Channel=%d" % self.G_Pause1Channel)
        #     if self.G_PauseTriggerWhileChangeChannelFlag==True:
        #         self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_P1CnAutoChangeChannel]G?命令发现暂停上报，继续暂停")
        #         #lancaigang240325：为了兼容断线没有取出而连续点击屏幕，统一都用暂停1表示
        #         #self.G_PhrozenFluiddRespondInfo("+PAUSE:1,%d" % self.G_Pause1Channel)
        #         if "+PAUSE:1" in self.G_PauseToLCDString:
        #             self.G_PhrozenFluiddRespondInfo(self.G_PauseToLCDString)
        #         #else:
        #             #self.G_PhrozenFluiddRespondInfo(self.G_PauseToLCDString)
        #         self.G_ChangeChannelFirstFilaFlag=True
        #         self.G_IfChangeFilaOngoing= False
        #         #lancaigang240524：用于UIUX动态界面
        #         self.G_PhrozenFluiddRespondInfo("+C:1,%d" % self.G_ChangeChannelTimeoutNewChan)
        #         return
        #     else:
        #         self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_P1CnAutoChangeChannel]G?命令没有发现暂停上报，需要进料恢复")
        #         self.G_ChangeChannelFirstFilaFlag=True
        #         self.G_IfChangeFilaOngoing= False
        #         #lancaigang240325：没有断线了，可以继续进料
        #         #return


        self.G_IfChangeFilaOngoing= True



        #lancaigang250102:打印换料数计算
        self.G_PrintCountNum=self.G_PrintCountNum+1
        self.G_PhrozenFluiddRespondInfo("换料次数=%d" % self.G_PrintCountNum)


        #换料首次第1个切换的通道线材
        if self.G_ChangeChannelFirstFilaFlag:
            # #lancaigang240314：第一个通道先移动到指定位置
            # self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_P1CnAutoChangeChannel]外部宏命令-PG104")
            # command_string = """
            # PG104
            # """
            # self.G_PhrozenGCode.run_script_from_command(command_string)
            # self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_P1CnAutoChangeChannel]外部宏命令-第1个通道移动到指定位置；command_string='%s'" % command_string)


            #lancaigang240125：
            self.G_PhrozenFluiddRespondInfo("换料首次第1个切换通道;暂停恢复第1个通道")

            # #lancaigang240124：stm32主动上报，开启可以暂停1次
            # self.STM32ReprotPauseFlag=0
            # self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_P1CnAutoChangeChannel]self.STM32ReprotPauseFlag=0")



            
            #lancaigang231202：如果第1个通道进料后klipper异常暂停赋值false，再恢复后就无法进入第1次换料了
            self.G_ChangeChannelFirstFilaFlag = False

            #不是恢复状态，则需要切线
            if self.G_ChangeChannelResumeFlag==False:
                self.G_PhrozenFluiddRespondInfo("首层打印，不是暂停恢复")
                self.G_ChangeChannelTimeoutOldChan=self.G_ChangeChannelTimeoutNewChan
                self.G_PhrozenFluiddRespondInfo("=====本次换料self.G_ChangeChannelTimeoutOldChan=%d" % self.G_ChangeChannelTimeoutOldChan)
                self.G_ChangeChannelTimeoutOldGcmd=self.G_ChangeChannelTimeoutNewGcmd
                self.G_ChangeChannelTimeoutNewChan=chan
                self.G_PhrozenFluiddRespondInfo("=====本次换料self.G_ChangeChannelTimeoutNewChan=%d" % self.G_ChangeChannelTimeoutNewChan)
                self.G_ChangeChannelTimeoutNewGcmd=gcmd
                self.Cmds_PrintMode(self.G_AMSDeviceWorkMode)




                #lancaigang250619:检查AMS是否重新连接成功
                self.Cmds_USBConnectErrorCheck()
                #lancaigang241030:
                if self.G_ChangeChannelTimeoutOldChan in range(1, 5):# 1 2 3 4
                    # #lancaigang241011：换料之前AMS先执行回退小段距离，再执行PG101；要考虑暂停恢复重复回抽切线问题
                    self.G_PhrozenFluiddRespondInfo("+H:0,%d" % self.G_ChangeChannelTimeoutOldChan)
                    self.Cmds_AMSSerial1Send("H%d" % self.G_ChangeChannelTimeoutOldChan)
                    self.G_PhrozenFluiddRespondInfo("串口1发送命令: H%d" % self.G_ChangeChannelTimeoutOldChan)
                    self.G_PhrozenFluiddRespondInfo("串口1换料前AMS回抽")
                    self.G_PhrozenFluiddRespondInfo("+H:1,%d" % self.G_ChangeChannelTimeoutOldChan)
                elif self.G_ChangeChannelTimeoutOldChan in range(5, 9):# 5 6 7 8
                    self.G_PhrozenFluiddRespondInfo("+H:0,%d" % self.G_ChangeChannelTimeoutOldChan-4)
                    self.Cmds_AMSSerial2Send("H%d" % self.G_ChangeChannelTimeoutOldChan-4)
                    self.G_PhrozenFluiddRespondInfo("串口2发送命令: H%d" % self.G_ChangeChannelTimeoutOldChan-4)
                    self.G_PhrozenFluiddRespondInfo("串口2换料前AMS回抽")
                    self.G_PhrozenFluiddRespondInfo("+H:1,%d" % self.G_ChangeChannelTimeoutOldChan-4)
                else:
                    self.G_PhrozenFluiddRespondInfo("回退异常通道，所有通道线材回退一段距离")
                    if self.G_SerialPort1OpenFlag == True:
                        #lancaigang240913：恢复的时候，目的是重复进线，可以全部回退所有线一段距离，防止旧通道回退异常，新通道进料异常
                        self.Cmds_AMSSerial1Send("AP")
                        self.G_PhrozenFluiddRespondInfo("串口1发送命令: AP；所有通道线材回退一段距离")
                    #lancaigang241030:
                    if self.G_SerialPort2OpenFlag == True:
                        self.Cmds_AMSSerial2Send("AP")
                        self.G_PhrozenFluiddRespondInfo("串口2发送命令: AP；所有通道线材回退一段距离")

                    #lancaigang240913：把延時放到外面
                    self.G_ProzenToolhead.dwell(6)







                # #lancaigang241011：PG101之前的G?命令进行回退，后执行PG101喷头回抽操作，在然后执行MC打断G?命令
                # self.Cmds_AMSSerial1Send("MC")
                # self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_P1CnAutoChangeChannel]发送命令：MC")
                # self.G_PhrozenFluiddRespondInfo("强制打断AMS回退距离")


                self.G_PhrozenFluiddRespondInfo("self.G_ToolheadIfHaveFilaFlag=%d" % (self.G_ToolheadIfHaveFilaFlag))

                self.G_PhrozenFluiddRespondInfo("外部宏命令-PG104-获取换线之前全局变量")
                command_string = """
                    PG104
                    """
                self.G_PhrozenGCode.run_script_from_command(command_string)
                self.G_PhrozenFluiddRespondInfo("外部宏命令-PG104-获取换线之前全局变量；command_string='%s'" % command_string)
                self.IfDoPG102Flag=True


                #lancaigang240510：换线之前，先跑到待料区
                #lancaigang240306：移动到切线代码里面
                #lancaigang240110：等待区域等待之前，先执行外部宏命令，移动到特定位置进行等待
                #lancaigang240515：换线之前，首先要到待料区
                self.G_PhrozenFluiddRespondInfo("外部宏命令-PG101-回抽")
                command_string = """
                    PG101
                    """
                self.G_PhrozenGCode.run_script_from_command(command_string)
                self.G_PhrozenFluiddRespondInfo("外部宏命令-到指定待料区位置等待吐料；command_string='%s'" % command_string)
                self.IfDoPG102Flag=True

                #lancaigang250323：
                if self.G_ToolheadIfHaveFilaFlag==True:
                    self.G_PhrozenFluiddRespondInfo("喷头有线材")



                    #lancaigang240909:切线动作放在PG106之前
                    # for i in range(15):
                    #     self.G_PhrozenFluiddRespondInfo("[(dev.python)]吐料中完成")
                    #     #lancaigang20231013：改为4秒延时
                    #     #lancaigang231115：改为1s
                    #     self.G_ProzenToolhead.dwell(1.0)
                    #     #lancaigang240125：不能用sleep，会阻塞主线程
                    #     #time.sleep(1)
                    #lancaigang240319：切线之前准备动作
                    #self.Cmds_MoveToCutFilaPrepare()
                    #lancaigang20231205：切刀切线
                    self.Cmds_MoveToCutFilaAction(gcmd)

                    #lancaigang250519:
                    self.G_PhrozenFluiddRespondInfo("外部宏命令-PRZ_CUT_WAITINGAREA")
                    command_string = """
                        PRZ_CUT_WAITINGAREA
                        """
                    self.G_PhrozenGCode.run_script_from_command(command_string)
                    self.G_PhrozenFluiddRespondInfo("外部宏命令-到指定待料区位置；command_string='%s'" % command_string)


                    #lancaigang240226：切线后AMS主板回退线材，延时后喷头回抽20mm
                    #time.sleep(2)
                    self.G_ProzenToolhead.dwell(0.5)


                    #lancaigang250619:检查AMS是否重新连接成功
                    self.Cmds_USBConnectErrorCheck()
                    #lancaigang241030:
                    if self.G_ChangeChannelTimeoutOldChan in range(1, 5):
                        #lancaigang240906：新的AMS，切线后，回退上一次通道一段距离
                        #lancaigang20231013：stm32换料
                        #lancaigang231129：stm32内部换料跟klipper换料分开，导致stm32内部强制换料，而klipper如果喷头切线异常而无法退料，导致klipper异常空打印
                        self.Cmds_AMSSerial1Send("G%d" % self.G_ChangeChannelTimeoutOldChan)
                        self.G_PhrozenFluiddRespondInfo("G%d" % self.G_ChangeChannelTimeoutOldChan)
                        self.G_PhrozenFluiddRespondInfo("串口1-AMS旧通道先回退一段距离: G%d" % self.G_ChangeChannelTimeoutOldChan)
                    elif self.G_ChangeChannelTimeoutOldChan in range(5, 9):
                        self.Cmds_AMSSerial2Send("G%d" % self.G_ChangeChannelTimeoutOldChan-4)
                        self.G_PhrozenFluiddRespondInfo("G%d" % self.G_ChangeChannelTimeoutOldChan-4)
                        self.G_PhrozenFluiddRespondInfo("串口2-AMS旧通道先回退一段距离: G%d" % self.G_ChangeChannelTimeoutOldChan-4)


                    self.G_PhrozenFluiddRespondInfo("self.G_ToolheadIfHaveFilaFlag=%d" % (self.G_ToolheadIfHaveFilaFlag))



                    #获取通道号和gcmd对象
                    #self.G_ChangeChannelTimeoutOldChan=chan
                    #self.G_ChangeChannelTimeoutOldGcmd=gcmd

                    self.G_ProzenToolhead.dwell(0.5)

                    


                    #lancaigang240913：把延時放到外面
                    self.G_ProzenToolhead.dwell(6.5)
                    #lancaigang240911：G命令之后延时6秒检查喷头是否有线材
                    #lancaigang231201：检查切线后旧通道线材是否正常退料，不正常则暂停
                    self.Cmds_CutFilaIfNormalCheck()
                    if self.G_KlipperIfPaused == True:
                        self.G_PhrozenFluiddRespondInfo("切线？秒了喷头还检测到线材，切刀异常了，请检查切刀，暂停klipper打印")
                        #Lo_ChangeChannelIfSuccess = False
                        return
                # else:
                #     self.G_PhrozenFluiddRespondInfo("外部宏命令-PRZ_WAITINGAREA-等待区")
                #     command_string = """
                #         PRZ_WAITINGAREA
                #         """
                #     self.G_PhrozenGCode.run_script_from_command(command_string)
                #     self.G_PhrozenFluiddRespondInfo("外部宏命令-PRZ_WAITINGAREA；command_string='%s'" % command_string)



                self.G_PhrozenFluiddRespondInfo("self.G_ToolheadIfHaveFilaFlag=%d" % (self.G_ToolheadIfHaveFilaFlag))

                #lancaigang240328：手动命令不执行吐料
                if self.ManualCmdFlag==True:
                    self.G_PhrozenFluiddRespondInfo("外部宏命令-PG106；手动命令，不执行吐料功能")
                else:
                    #lancaigang240319：切完后，先吐掉残留喷头的线材，防止切成米粒
                    self.G_PhrozenFluiddRespondInfo("外部宏命令-PG106；切线之后，喷头升温同时AMS退线")
                    self.PG102Flag=True
                    self.G_PhrozenFluiddRespondInfo("self.Flag=True")
                    command_string = """
                    PG106
                    """
                    self.G_PhrozenGCode.run_script_from_command(command_string)
                    self.G_PhrozenFluiddRespondInfo("command_string='%s'" % command_string)
                    self.PG102Flag=False
                    self.G_PhrozenFluiddRespondInfo("self.Flag=False")


                #lancaigang231216：如果换料期间点击暂停，刚好换料期间抬升了z轴，到执行暂停时，把z轴高度也保存了，导致整体高度异常
                #lancaigang231216：如果z轴抬升没有被降下，需要降下再暂停
                if self.G_IfZPositionLiftUpFlag==True:
                    command_string = """
                        G90
                        G91
                        G1 Z-%f F8000
                        """ % (
                        self.G_AMSFilaCutZPositionLiftingUp,
                    )
                    self.G_PhrozenGCode.run_script_from_command(command_string)
                    self.G_IfZPositionLiftUpFlag = False
                    self.G_PhrozenFluiddRespondInfo("Z轴下拉降低；command_string='%s'" % command_string)
            

                self.G_ProzenToolhead.dwell(0.5)

                #lancaigang20231013：手动换料
                self.Cmds_P1TnManualChangeChannel(self.G_ChangeChannelTimeoutNewChan, self.G_ChangeChannelTimeoutNewGcmd)
            #lancaigang240912:暂停恢复过程，使用旧记录的旧通道和新通道
            else:
                self.G_PhrozenFluiddRespondInfo("不是首层打印，是暂停恢复")
                #lancaigang20231013：手动换料
                self.Cmds_P1TnManualChangeChannel(self.G_ChangeChannelTimeoutNewChan, self.G_ChangeChannelTimeoutNewGcmd)









        #后续第n个切换的通道线材
        else:
            self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_P1CnAutoChangeChannel]换料后面第n个通道切换；else")
            self.G_ChangeChannelTimeoutOldChan=self.G_ChangeChannelTimeoutNewChan
            self.G_PhrozenFluiddRespondInfo("=====本次换料self.G_ChangeChannelTimeoutOldChan=%d" % self.G_ChangeChannelTimeoutOldChan)
            self.G_ChangeChannelTimeoutOldGcmd=self.G_ChangeChannelTimeoutNewGcmd
            self.G_ChangeChannelTimeoutNewChan=chan
            self.G_PhrozenFluiddRespondInfo("=====本次换料self.G_ChangeChannelTimeoutNewChan=%d" % self.G_ChangeChannelTimeoutNewChan)
            self.G_ChangeChannelTimeoutNewGcmd=gcmd
            self.Cmds_PrintMode(self.G_AMSDeviceWorkMode)



            #lancaigang240124：stm32主动上报，开启可以暂停1次
            self.STM32ReprotPauseFlag=0
            self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_P1CnAutoChangeChannel]self.STM32ReprotPauseFlag=0")
            self.G_PhrozenFluiddRespondInfo("self.G_ToolheadIfHaveFilaFlag=%d" % (self.G_ToolheadIfHaveFilaFlag))

            #lancaigang250619:检查AMS是否重新连接成功
            self.Cmds_USBConnectErrorCheck()
            #lancaigang241030:
            if self.G_ChangeChannelTimeoutOldChan in range(1, 5):
                # #lancaigang241011：换料之前AMS先执行回退小段距离，再执行PG101；要考虑暂停恢复重复回抽切线问题
                self.G_PhrozenFluiddRespondInfo("+H:0,%d" % self.G_ChangeChannelTimeoutOldChan)
                self.Cmds_AMSSerial1Send("H%d" % self.G_ChangeChannelTimeoutOldChan)
                self.G_PhrozenFluiddRespondInfo("串口1发送命令: H%d" % self.G_ChangeChannelTimeoutOldChan)
                self.G_PhrozenFluiddRespondInfo("串口1换料前AMS回抽")
                self.G_PhrozenFluiddRespondInfo("+H:1,%d" % self.G_ChangeChannelTimeoutOldChan)
            elif self.G_ChangeChannelTimeoutOldChan in range(5, 9):
                self.G_PhrozenFluiddRespondInfo("+H:0,%d" % self.G_ChangeChannelTimeoutOldChan-4)
                self.Cmds_AMSSerial2Send("H%d" % self.G_ChangeChannelTimeoutOldChan-4)
                self.G_PhrozenFluiddRespondInfo("串口2发送命令: H%d" % self.G_ChangeChannelTimeoutOldChan-4)
                self.G_PhrozenFluiddRespondInfo("串口2换料前AMS回抽")
                self.G_PhrozenFluiddRespondInfo("+H:1,%d" % self.G_ChangeChannelTimeoutOldChan-4)
            else:
                    self.G_PhrozenFluiddRespondInfo("回退异常通道，所有通道线材回退一段距离")
                    if self.G_SerialPort1OpenFlag == True:
                        #lancaigang240913：恢复的时候，目的是重复进线，可以全部回退所有线一段距离，防止旧通道回退异常，新通道进料异常
                        self.Cmds_AMSSerial1Send("AP")
                        self.G_PhrozenFluiddRespondInfo("串口1发送命令: AP；所有通道线材回退一段距离")
                    #lancaigang241030:
                    if self.G_SerialPort2OpenFlag == True:
                        self.Cmds_AMSSerial2Send("AP")
                        self.G_PhrozenFluiddRespondInfo("串口2发送命令: AP；所有通道线材回退一段距离")

                    #lancaigang240913：把延時放到外面
                    self.G_ProzenToolhead.dwell(6)

            


            #lancaigang250824:
            self.G_PhrozenFluiddRespondInfo("self.G_ProzenToolhead.wait_moves()")
            self.G_ProzenToolhead.wait_moves()


            self.G_PhrozenFluiddRespondInfo("外部宏命令-PG104-获取换线之前全局变量")
            command_string = """
                PG104
                """
            self.G_PhrozenGCode.run_script_from_command(command_string)
            self.G_PhrozenFluiddRespondInfo("外部宏命令-PG104-获取换线之前全局变量；command_string='%s'" % command_string)
            self.IfDoPG102Flag=True
            
            
            #lancaigang240510：换线之前，先跑到待料区
            #lancaigang240306：移动到切线代码里面
            #lancaigang240110：等待区域等待之前，先执行外部宏命令，移动到特定位置进行等待
            #lancaigang240515：换线之前，首先要到待料区
            self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_P1CnAutoChangeChannel]外部宏命令-PG101-回抽")
            command_string = """
                PG101
                """
            self.G_PhrozenGCode.run_script_from_command(command_string)
            self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_P1CnAutoChangeChannel]外部宏命令-到指定待料区位置等待吐料；command_string='%s'" % command_string)
            self.IfDoPG102Flag=True


            self.G_PhrozenFluiddRespondInfo("self.G_ToolheadIfHaveFilaFlag=%d" % (self.G_ToolheadIfHaveFilaFlag))



            #lancaigang250824:
            self.G_PhrozenFluiddRespondInfo("self.G_ProzenToolhead.wait_moves()")
            self.G_ProzenToolhead.wait_moves()


            #lancaigang250323：
            #if self.G_ToolheadIfHaveFilaFlag==True:
                #self.G_PhrozenFluiddRespondInfo("喷头有线材")
                #lancaigang20231013：切刀切线，Z抬升跑到X Y切线位置
            self.Cmds_MoveToCutFilaAction(gcmd)
            #else:
            #    self.G_PhrozenFluiddRespondInfo("外部宏命令-PRZ_WAITINGAREA-等待区")
            #    command_string = """
            #        PRZ_WAITINGAREA
            #        """
            #    self.G_PhrozenGCode.run_script_from_command(command_string)
            #    self.G_PhrozenFluiddRespondInfo("外部宏命令-PRZ_WAITINGAREA；command_string='%s'" % command_string)


            #lancaigang250824:
            self.G_PhrozenFluiddRespondInfo("self.G_ProzenToolhead.wait_moves()")
            self.G_ProzenToolhead.wait_moves()



            #lancaigang250519:
            self.G_PhrozenFluiddRespondInfo("外部宏命令-PRZ_CUT_WAITINGAREA")
            command_string = """
                PRZ_CUT_WAITINGAREA
                """
            self.G_PhrozenGCode.run_script_from_command(command_string)
            self.G_PhrozenFluiddRespondInfo("外部宏命令-到指定待料区位置；command_string='%s'" % command_string)


            self.G_ProzenToolhead.dwell(0.5)


            #lancaigang250824:
            self.G_PhrozenFluiddRespondInfo("self.G_ProzenToolhead.wait_moves()")
            self.G_ProzenToolhead.wait_moves()

            self.G_PhrozenFluiddRespondInfo("self.G_ToolheadIfHaveFilaFlag=%d" % (self.G_ToolheadIfHaveFilaFlag))

            #lancaigang250619:检查AMS是否重新连接成功
            self.Cmds_USBConnectErrorCheck()
            #lancaigang241030:
            if self.G_ChangeChannelTimeoutOldChan in range(1, 5):
                #lancaigang240906：切线后，回退上一次通道一段距离
                #lancaigang20231013：stm32换料
                #lancaigang231129：stm32内部换料跟klipper换料分开，导致stm32内部强制换料，而klipper如果喷头切线异常而无法退料，导致klipper异常空打印
                self.Cmds_AMSSerial1Send("G%d" % self.G_ChangeChannelTimeoutOldChan)
                self.G_PhrozenFluiddRespondInfo("G%d" % self.G_ChangeChannelTimeoutOldChan)
                self.G_PhrozenFluiddRespondInfo("串口1-AMS旧通道先回退一段距离: G%d" % self.G_ChangeChannelTimeoutOldChan)
            elif self.G_ChangeChannelTimeoutOldChan in range(5, 9):
                self.Cmds_AMSSerial2Send("G%d" % self.G_ChangeChannelTimeoutOldChan-4)
                self.G_PhrozenFluiddRespondInfo("G%d" % self.G_ChangeChannelTimeoutOldChan-4)
                self.G_PhrozenFluiddRespondInfo("串口2-AMS旧通道先回退一段距离: G%d" % self.G_ChangeChannelTimeoutOldChan-4)


            #lancaigang250824:
            self.G_PhrozenFluiddRespondInfo("self.G_ProzenToolhead.wait_moves()")
            self.G_ProzenToolhead.wait_moves()

            #lancaigang250322：PG106升温要十几秒，这里不用延时，但前提是PG106必须升温
            #lancaigang240913：把延時放到外面
            self.G_ProzenToolhead.dwell(6.5)
            #lancaigang250823：
            self.G_PhrozenFluiddRespondInfo("self.G_ProzenToolhead.wait_moves()")
            self.G_ProzenToolhead.wait_moves()
            #lancaigang231201：检查切线后是否正常退料，不正常则暂停
            #lancaigang231215：Z轴上升后必须记得下降
            #lancaigang231216：等待6秒检查是否切线成功
            self.Cmds_CutFilaIfNormalCheck()
            if self.G_KlipperIfPaused == True:
                self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_P1CnAutoChangeChannel]切线？秒了喷头还检测到线材，切刀异常了，请检查切刀，暂停klipper打印")
                #self.Cmds_PhrozenKlipperPause(None)

                Lo_PauseStatus=self.G_PhrozenPrinterCancelPauseResume.get_status(None)
                self.G_PhrozenFluiddRespondInfo("当前暂停状态-Lo_PauseStatus='%s'" % Lo_PauseStatus)
                self.G_PhrozenFluiddRespondInfo("Lo_PauseStatus['is_paused']='%s'" % Lo_PauseStatus['is_paused'])
                #// 当前暂停状态-Lo_PauseStatus='{'is_paused': True}'
                if Lo_PauseStatus['is_paused'] == True:
                    self.G_PhrozenFluiddRespondInfo("已是暂停状态")
                else:
                    self.G_PhrozenFluiddRespondInfo("未暂停状态")
                    #klipper暂停命令；保存当前的x y z坐标
                    #lancaigang240108：要考虑多次暂停保存的数据是否正常，后续要验证
                    self.G_PhrozenGCode.run_script_from_command("SAVE_GCODE_STATE NAME=PAUSE")
                    self.G_PhrozenFluiddRespondInfo("[(cmds.python)]PAUSE")
                    self.G_PhrozenPrinterCancelPauseResume.send_pause_command()
                    self.G_ProzenToolhead.wait_moves()
                    self.G_ProzenToolhead.dwell(1.0)

                    self.G_PhrozenFluiddRespondInfo("喷头切刀或传感器异常，暂停")
                    #self.G_PhrozenFluiddRespondInfo("+PAUSE:8,%d" % self.G_ChangeChannelTimeoutOldChan)
                    #lancaigang250414:
                    #self.G_PhrozenFluiddRespondInfo("+PAUSE:8,%d,%d" % (self.G_ChangeChannelTimeoutOldChan,self.G_ChangeChannelTimeoutNewChan))
                    if len(self.G_PauseToLCDString)==0:
                        self.G_PhrozenFluiddRespondInfo("+PAUSE:8,%d,%d" % (self.G_ChangeChannelTimeoutOldChan,self.G_ChangeChannelTimeoutNewChan))
                    else:
                        self.G_PhrozenFluiddRespondInfo(self.G_PauseToLCDString)
                # #lancaigang250524:
                # self.G_PhrozenFluiddRespondInfo("暂停过程中，收到了新的gcode命令，也需要记录最新的新旧通道，防止混色")
                # self.G_ChangeChannelTimeoutOldChan=self.G_ChangeChannelTimeoutNewChan
                # self.G_PhrozenFluiddRespondInfo("=====self.G_ChangeChannelTimeoutOldChan=%d" % self.G_ChangeChannelTimeoutOldChan)
                # self.G_ChangeChannelTimeoutOldGcmd=self.G_ChangeChannelTimeoutNewGcmd
                # self.G_ChangeChannelTimeoutNewChan=chan
                # self.G_PhrozenFluiddRespondInfo("=====self.G_ChangeChannelTimeoutNewChan=%d" % self.G_ChangeChannelTimeoutNewChan)
                # self.G_ChangeChannelTimeoutNewGcmd=gcmd

                Lo_PauseStatus=self.G_PhrozenPrinterCancelPauseResume.get_status(None)
                self.G_PhrozenFluiddRespondInfo("当前暂停状态-Lo_PauseStatus='%s'" % Lo_PauseStatus)
                self.G_PhrozenFluiddRespondInfo("Lo_PauseStatus['is_paused']='%s'" % Lo_PauseStatus['is_paused'])
                #// 当前暂停状态-Lo_PauseStatus='{'is_paused': True}'
                if Lo_PauseStatus['is_paused'] == True:
                    self.G_PhrozenFluiddRespondInfo("已是暂停状态")
                else:
                    self.G_PhrozenFluiddRespondInfo("未暂停状态")

                self.G_PhrozenFluiddRespondInfo("return")
                return

            #lancaigang240229：防止发送命令粘包
            #time.sleep(1)
            self.G_ProzenToolhead.dwell(0.5)



            self.G_PhrozenFluiddRespondInfo("self.G_ToolheadIfHaveFilaFlag=%d" % (self.G_ToolheadIfHaveFilaFlag))

            #lancaigang240319：切完后，先吐掉残留喷头的线材，防止切成米粒
            self.G_PhrozenFluiddRespondInfo("[(cmds.python)]外部宏命令-PG106；切线之后，喷头升温同时AMS退线")
            self.PG102Flag=True
            self.G_PhrozenFluiddRespondInfo("[(dev.python)]self.Flag=True")
            command_string = """
            PG106
            """
            self.G_PhrozenGCode.run_script_from_command(command_string)
            self.G_PhrozenFluiddRespondInfo("[(cmds.python)]command_string='%s'" % command_string)
            self.PG102Flag=False
            self.G_PhrozenFluiddRespondInfo("[(dev.python)]self.Flag=False")
            
            #lancaigang250619:检查AMS是否重新连接成功
            self.Cmds_USBConnectErrorCheck()
            #lancaigang241030:
            if self.G_ChangeChannelTimeoutNewChan in range(1, 5):
                #lancaigang240911：新AMS，T命令只负责进料
                #lancaigang20231013：stm32换料
                #lancaigang231129：stm32内部换料跟klipper换料分开，导致stm32内部强制换料，而klipper如果喷头切线异常而无法退料，导致klipper异常空打印
                self.Cmds_AMSSerial1Send("T%d" % self.G_ChangeChannelTimeoutNewChan)
                self.G_PhrozenFluiddRespondInfo("串口1换料发送命令: T%d" % self.G_ChangeChannelTimeoutNewChan)
            elif self.G_ChangeChannelTimeoutNewChan in range(5, 9):
                self.Cmds_AMSSerial2Send("T%d" % self.G_ChangeChannelTimeoutNewChan-4)
                self.G_PhrozenFluiddRespondInfo("串口2换料发送命令: T%d" % self.G_ChangeChannelTimeoutNewChan-4)






            #lancaigang240322：
            self.G_PhrozenFluiddRespondInfo("[(cmds.python)]外部宏命令-PG105；切线之后，喷头升温同时AMS进线")
            self.PG102Flag=True
            self.G_PhrozenFluiddRespondInfo("[(dev.python)]self.Flag=True")
            command_string = """
            PG105
            """
            self.G_PhrozenGCode.run_script_from_command(command_string)
            self.G_PhrozenFluiddRespondInfo("[(cmds.python)]command_string='%s'" % command_string)
            self.PG102Flag=False
            self.G_PhrozenFluiddRespondInfo("[(dev.python)]self.Flag=False")

            self.G_PhrozenFluiddRespondInfo("self.G_ToolheadIfHaveFilaFlag=%d" % (self.G_ToolheadIfHaveFilaFlag))

            #lancaigang240328：手动命令不执行吐料
            if self.ManualCmdFlag==True:
                self.G_PhrozenFluiddRespondInfo("外部宏命令-PG110；手动命令，不执行")
            else:
                #lancaigang240319：切完后，先吐掉残留喷头的线材，防止切成米粒
                self.G_PhrozenFluiddRespondInfo("外部宏命令-PG110；STM32进料之后，klipper开始吐料接住进料")
                self.PG102Flag=True
                self.G_PhrozenFluiddRespondInfo("self.Flag=True")
                command_string = """
                PG110
                """
                self.G_PhrozenGCode.run_script_from_command(command_string)
                self.G_PhrozenFluiddRespondInfo("command_string='%s'" % command_string)
                self.PG102Flag=False
                self.G_PhrozenFluiddRespondInfo("self.Flag=False")


            #lancaigang240229：直接z轴下降，不用到待料区
            if self.G_IfZPositionLiftUpFlag==True:
                command_string = """
                    G90
                    G91
                    G1 Z-%f F8000
                    """ % (
                    self.G_AMSFilaCutZPositionLiftingUp,
                )
                self.G_PhrozenGCode.run_script_from_command(command_string)
                self.G_IfZPositionLiftUpFlag = False
                self.G_PhrozenFluiddRespondInfo("Z轴下拉降低；command_string='%s'" % command_string)



            #lancaigang240223：如果切线失败，上个函数已经Z轴下降了，已经暂停就不执行下面操作
            if self.ToolheadCutFlag==True:
                self.ToolheadCutFlag=False
                self.G_PhrozenFluiddRespondInfo("之前切线异常，换线失败")
                self.G_ChangeChannelFirstFilaFlag=True
                self.G_IfChangeFilaOngoing= False

                #stm32上报暂停只能暂停1次，不能重复暂停
                self.STM32ReprotPauseFlag=1
                #lancaigang231202：P1 C?自动换料时，如果第1次通道就进料异常暂停，如果要恢复，也继续从第1次通道开始
                self.G_ChangeChannelFirstFilaFlag=True

                #lancaigang250308：恢复本身已经切线异常了，这里也报切线异常
                #self.G_PhrozenFluiddRespondInfo("+PAUSE:8,%d" % self.G_ChangeChannelTimeoutNewChan)
                #self.G_PhrozenFluiddRespondInfo("+PAUSE:8,%d,%d" % (self.G_ChangeChannelTimeoutOldChan,self.G_ChangeChannelTimeoutNewChan))
                
                #lancaigang240416:
                if self.G_SerialPort1OpenFlag == True:
                    #lancaigang240603：防止AMS一直停不了
                    self.Cmds_AMSSerial1Send("AT+PAUSE")
                    self.G_PhrozenFluiddRespondInfo("串口1-AT+PAUSE暂停stm32电机")
                #lancaigang241030:
                if self.G_SerialPort2OpenFlag == True:
                    self.Cmds_AMSSerial2Send("AT+PAUSE")
                    self.G_PhrozenFluiddRespondInfo("串口2-AT+PAUSE暂停stm32电机")



                if self.G_KlipperInPausing == False:
                    self.G_PhrozenFluiddRespondInfo("不在暂停中，允许新的暂停")
                    #lancaigang250607:
                    self.G_PhrozenFluiddRespondInfo("启用快速暂停")
                    self.G_KlipperQuickPause = True
                    #klipper主动暂停
                    self.Cmds_PhrozenKlipperPause(None)
                else:
                    self.G_PhrozenFluiddRespondInfo("暂停中，不允许新的暂停")



                self.G_KlipperIfPaused = True

                #lancaigang240325：换料失败，不能执行恢复
                self.G_MCModeCanResumeFlag = False

                if len(self.G_PauseToLCDString)==0:
                    self.G_PhrozenFluiddRespondInfo("+PAUSE:8,%d,%d" % (self.G_ChangeChannelTimeoutOldChan,self.G_ChangeChannelTimeoutNewChan))
                else:
                    self.G_PhrozenFluiddRespondInfo(self.G_PauseToLCDString)

                #lancaigang240524：用于UIUX动态界面
                self.G_PhrozenFluiddRespondInfo("+C:1,%d" % self.G_ChangeChannelTimeoutNewChan)
                
                self.G_PhrozenFluiddRespondInfo("return")
                return

            self.G_PhrozenFluiddRespondInfo("self.G_ToolheadIfHaveFilaFlag=%d" % (self.G_ToolheadIfHaveFilaFlag))

            # #lancaigang231208：z轴-负数会往下
            # #lancaigang231213：F7200改为300
            # #lancaigang231215：Z轴上升后必须记得下降
            # command_string = """
            #     G90
            #     G1 X%.3f Y%.3f F8000
            #     G91
            #     G1 Z-%f F8000
            #     """ % (
            #     self.G_DictChangeChannelWaitAreaParam["X"],
            #     self.G_DictChangeChannelWaitAreaParam["Y"],
            #     self.G_AMSFilaCutZPositionLiftingUp,
            # )
            # self.G_PhrozenGCode.run_script_from_command(command_string)
            # #lancaigang231216：如果换料期间点击暂停，刚好换料期间抬升了z轴，到执行暂停时，把z轴高度也保存了，导致整体高度异常
            # self.G_IfZPositionLiftUpFlag = False
            # self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_P1CnAutoChangeChannel]内部gcode到等待区x y z轴下拉降低；command_string='%s'" % command_string)

            
            #置位标签
            Lo_ChangeChannelIfSuccess = False
            self.G_PhrozenFluiddRespondInfo("Lo_ChangeChannelIfSuccess = False")


            #lancaigang231202：如果P9命令的movepath数组为空，导致len函数异常导致klipper崩溃
            # 为0则按路径运行
            #lancaigang231206：UI界面如果暂停恢复，是没有P9设定区域的，来回运动数组为空，codedump
            if self.ChangeWaitMoveArea is None:
                self.G_PhrozenFluiddRespondInfo("等待区域来回移动异常;klipper暂停")
                Lo_ChangeChannelIfSuccess = False
                pass

            if self.ChangeWaitMoveArea is not None:
                #空列表
                if len(self.ChangeWaitMoveArea) == 0:
                    self.G_PhrozenFluiddRespondInfo("return;等待区域来回移动异常，按路径返回;if len(self.ChangeWaitMoveArea) == 0")
                    #lancaigang231206：往下执行
                    #return
                else:
                    self.G_PhrozenFluiddRespondInfo("for;等待区域来回移动正常，路径队列反复来回，等待换料新线材到达喷头")


                # #lancaigang240306：移动到切线代码里面
                # #lancaigang240110：等待区域等待之前，先执行外部宏命令，移动到特定位置进行等待
                # self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_P1CnAutoChangeChannel]外部宏命令-PG101")
                # command_string = """
                #     PG101
                #     """
                # self.G_PhrozenGCode.run_script_from_command(command_string)
                # self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_P1CnAutoChangeChannel]外部宏命令-到指定位置等待吐料；command_string='%s'" % command_string)
                # self.IfDoPG102Flag=True

                #lancaigang250519:
                self.G_PhrozenFluiddRespondInfo("外部宏命令-PRZ_SPITTING_SCRAPE")
                command_string = """
                    PRZ_SPITTING_SCRAPE
                    """
                self.G_PhrozenGCode.run_script_from_command(command_string)
                self.G_PhrozenFluiddRespondInfo("外部宏命令-刮料；command_string='%s'" % command_string)


                #lancaigang250607：打印状态；1-退料中；2-进料中；3-打印中；4-暂停
                self.G_KlipperPrintStatus= 2
                # Python enumerate() 函数
                # enumerate() 函数用于将一个可遍历的数据对象(如列表、元组或字符串)组合为一个索引序列，同时列出数据和数据下标，一般用在 for 循环当中。
                # Python 2.3. 以上版本可用，2.6 添加 start 参数。
                # for 循环使用 enumerate
                # >>> seq = ['one', 'two', 'three']
                # >>> for i, element in enumerate(seq):
                # ...     print i, element
                # ...
                # 0 one
                # 1 two
                # 2 three
                #等待区域来回运动，大概80秒超时；按照长方形每一步的步长进行移动
                #for i in range(CHANGE_CHANNEL_WAIT_TIMEOUT):#大概120秒
                #for num, point in enumerate(self.ChangeWaitMoveArea):
                for num in range(CHANGE_CHANNEL_WAIT_TIMEOUT):
                    #lancaigang231202：如果STM32主动上报暂停，需要klipper暂停
                    if self.STM32ReprotPauseFlag==1:
                        # Lo_ChangeChannelIfSuccess = False
                        # break
                        #lancaigang231205：如果等待期间有stm32主动上报暂停了，这个时候直接退出，不用往下暂停
                        self.G_PhrozenFluiddRespondInfo("等待换料期间，stm32主动上报了暂停")

                        Lo_PauseStatus=self.G_PhrozenPrinterCancelPauseResume.get_status(None)
                        self.G_PhrozenFluiddRespondInfo("当前暂停状态-Lo_PauseStatus='%s'" % Lo_PauseStatus)
                        self.G_PhrozenFluiddRespondInfo("Lo_PauseStatus['is_paused']='%s'" % Lo_PauseStatus['is_paused'])
                        #// 当前暂停状态-Lo_PauseStatus='{'is_paused': True}'
                        if Lo_PauseStatus['is_paused'] == True:
                            self.G_PhrozenFluiddRespondInfo("已是暂停状态")
                        else:
                            self.G_PhrozenFluiddRespondInfo("未暂停状态")
                        Lo_ChangeChannelIfSuccess = False
                        break


                    # #lancaigang231214：等待区域基点X Y以W H长方形步长来回移动，实现吐料功能
                    # command_string = """
                    #     G90
                    #     G1 X%.03f Y%.03f F%d
                    #     """ % (
                    #     point[0]+(num%2),#X基坐标；lancaigang231215：等待区域x坐标强制右移mm，防止正常打印喷头碰到漏料
                    #     point[1]+(num%2),#Y基坐标
                    #     int(self.G_WaitAreaEachStepDist / self.G_MovementSpeedFactor),#速率
                    #     #500
                    # )
                    # #lancaigang231129：缓慢来回移动
                    # self.G_PhrozenGCode.run_script_from_command(command_string)
                    # self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_P1CnAutoChangeChannel]等待换料期间，基坐标XY为P9配置")
                    
                    
                    #self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_P1CnAutoChangeChannel]等待换料期间，使用外部宏命令")


                    #self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_P1CnAutoChangeChannel]num='%d'" % num)
                    #lancaigang20231014：等待喷头移动到指定位置，会耗一些时间，1秒左右
                    self.G_ProzenToolhead.wait_moves()
                    #self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_P1CnAutoChangeChannel]self.G_ProzenToolhead.wait_moves()")

                    #lancaigang231219：改为dwell
                    #lancaigang231209
                    #time.sleep(2)
                    #lancaigang231115：改为1s
                    self.G_ProzenToolhead.dwell(1)

                    self.G_PhrozenFluiddRespondInfo("self.G_ToolheadIfHaveFilaFlag=%d" % (self.G_ToolheadIfHaveFilaFlag))

                    self.G_PhrozenFluiddRespondInfo("外部宏命令-PG110；STM32进料之后，klipper开始吐料接住进料")
                    command_string = """
                    PG110
                    """
                    self.G_PhrozenGCode.run_script_from_command(command_string)
                    self.G_PhrozenFluiddRespondInfo("command_string='%s'" % command_string)


        
                    self.G_PhrozenFluiddRespondInfo("当前模式")
                    if self.G_AMSDeviceWorkMode == AMS_WORK_MODE_UNKNOW:
                        self.G_PhrozenFluiddRespondInfo("+Mode:0,unkown")
                    elif self.G_AMSDeviceWorkMode == AMS_WORK_MODE_MC:
                        self.G_PhrozenFluiddRespondInfo("+Mode:1,MC")
                    elif self.G_AMSDeviceWorkMode == AMS_WORK_MODE_MA:
                        self.G_PhrozenFluiddRespondInfo("+Mode:2,MA")
                    elif self.G_AMSDeviceWorkMode == AMS_WORK_MODE_FILA_RUNOUT:
                        self.G_PhrozenFluiddRespondInfo("+Mode:3,RUNOUT")
                    else:
                        self.G_PhrozenFluiddRespondInfo("+Mode:-1,error")


                    Lo_PauseStatus=self.G_PhrozenPrinterCancelPauseResume.get_status(None)
                    self.G_PhrozenFluiddRespondInfo("当前暂停状态-Lo_PauseStatus='%s'" % Lo_PauseStatus)
                    self.G_PhrozenFluiddRespondInfo("Lo_PauseStatus['is_paused']='%s'" % Lo_PauseStatus['is_paused'])
                    #// 当前暂停状态-Lo_PauseStatus='{'is_paused': True}'
                    if Lo_PauseStatus['is_paused'] == True:
                        self.G_PhrozenFluiddRespondInfo("已是暂停状态")
                    else:
                        self.G_PhrozenFluiddRespondInfo("未暂停状态")



                    #lancaigang250111:for循环吐料挤出机运动，防止进料卡在挤出轮


                    #lancaigang240125：不能用sleep，会阻塞主线程
                    #time.sleep(1)

                    # #lancaigang231129：如果秒后发现喷头还检测到线材，说明喷头切线异常了，需要暂停klipper
                    # if num == 3 and point[2] and self.G_ToolheadIfHaveFilaFlag:
                    #     self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_P1CnAutoChangeChannel]切线5秒了喷头还检测到线材，切刀异常了，请检查切刀，暂停klipper打印")
                    #     Lo_ChangeChannelIfSuccess = False
                    #     break
                    # elif num > 3:
                    #     self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_P1CnAutoChangeChannel]切线成功，继续等待新线材换入")

                    # 10秒后且点允许检测且检测到线材
                    #lancaigang20231013：10改为8
                    #lancaigang231129：如果切线不成功，stm32会保留上次命令而继续执行换料动作，但实际上线也退不回去，而这里过了几秒如果检测到喷头有线材，会继续klipper打印导致没有线材也空打印
                    #lancaigang231129：改为秒后检测喷头是否有线材，正常换料的时候，5秒内切刀能切线，stm32电机并回退线材，这个时候喷头是无法检测到线材的，30秒后再检测是否有新线材换入
                    if num > 1 and self.G_ToolheadIfHaveFilaFlag:
                        self.G_PhrozenFluiddRespondInfo("检测有新线材，说明换料成功，可以打印")
                        Lo_ChangeChannelIfSuccess = True
                        break



            self.G_PhrozenFluiddRespondInfo("self.G_ToolheadIfHaveFilaFlag=%d" % (self.G_ToolheadIfHaveFilaFlag))

            #如果为true成功，则返回
            if Lo_ChangeChannelIfSuccess:
                self.G_PhrozenFluiddRespondInfo("换料成功；")
                self.G_PhrozenFluiddRespondInfo("换料成功")
                self.G_IfChangeFilaOngoing= False

                #lancaigang250424：防止AMS缓冲器还么有顶满
                self.G_ProzenToolhead.dwell(0.5)

                #lancaigang250619:检查AMS是否重新连接成功
                self.Cmds_USBConnectErrorCheck()
                #lancaigang250423：进料成功，开始吐料，通知AMS开始计时，如果吐料超过5秒缓冲器还是慢状态，说明堵头了
                #self.Cmds_AMSSerial2Send("AT+EBLOCKCHECK")
                #self.G_PhrozenFluiddRespondInfo("AMS开始计时缓冲器满时间")
                if self.G_SerialPort1OpenFlag == True:
                    self.Cmds_AMSSerial1Send("AT+EBLOCKCHECK")
                    self.G_PhrozenFluiddRespondInfo("串口1-AMS开始计时缓冲器满时间")
                if self.G_SerialPort2OpenFlag == True:
                    self.Cmds_AMSSerial2Send("AT+EBLOCKCHECK")
                    self.G_PhrozenFluiddRespondInfo("串口2-AMS开始计时缓冲器满时间")
                self.G_ProzenToolhead.dwell(1)

                #lancaigang240229:
                if self.IfDoPG102Flag==True:
                    self.IfDoPG102Flag=False

                    self.G_PhrozenFluiddRespondInfo("吐料开始")
                    self.G_PhrozenFluiddRespondInfo("+MSG:1,0,%d,%d" % (self.G_ChangeChannelTimeoutOldChan,self.G_ChangeChannelTimeoutNewChan))


                    #lancaigang241031：控制吐料次数
                    #lancaigang250324：默认是PG113，吐料3次
                    if self.G_P10SpitNum==0:
                        self.G_PhrozenFluiddRespondInfo("外部宏命令-PG113")
                        self.PG102Flag=True
                        self.G_PhrozenFluiddRespondInfo("self.Flag=True")
                        command_string = """
                        PG113
                        """
                        self.G_PhrozenGCode.run_script_from_command(command_string)
                        self.G_PhrozenFluiddRespondInfo("外部宏命令-排废料；command_string='%s'" % command_string)
                    elif self.G_P10SpitNum==1:
                        self.G_PhrozenFluiddRespondInfo("外部宏命令-PG111")
                        self.PG102Flag=True
                        self.G_PhrozenFluiddRespondInfo("self.Flag=True")
                        command_string = """
                        PG111
                        """
                        self.G_PhrozenGCode.run_script_from_command(command_string)
                        self.G_PhrozenFluiddRespondInfo("外部宏命令-排废料；command_string='%s'" % command_string)
                    elif self.G_P10SpitNum==2:
                        self.G_PhrozenFluiddRespondInfo("外部宏命令-PG112")
                        self.PG102Flag=True
                        self.G_PhrozenFluiddRespondInfo("self.Flag=True")
                        command_string = """
                        PG112
                        """
                        self.G_PhrozenGCode.run_script_from_command(command_string)
                        self.G_PhrozenFluiddRespondInfo("外部宏命令-排废料；command_string='%s'" % command_string)
                    elif self.G_P10SpitNum==3:
                        self.G_PhrozenFluiddRespondInfo("外部宏命令-PG113")
                        self.PG102Flag=True
                        self.G_PhrozenFluiddRespondInfo("self.Flag=True")
                        command_string = """
                        PG113
                        """
                        self.G_PhrozenGCode.run_script_from_command(command_string)
                        self.G_PhrozenFluiddRespondInfo("外部宏命令-排废料；command_string='%s'" % command_string)
                    elif self.G_P10SpitNum==4:
                        self.G_PhrozenFluiddRespondInfo("外部宏命令-PG114")
                        self.PG102Flag=True
                        self.G_PhrozenFluiddRespondInfo("self.Flag=True")
                        command_string = """
                        PG114
                        """
                        self.G_PhrozenGCode.run_script_from_command(command_string)
                        self.G_PhrozenFluiddRespondInfo("外部宏命令-排废料；command_string='%s'" % command_string)
                    #lancaigang250528：
                    elif self.G_P10SpitNum==5:
                        self.G_PhrozenFluiddRespondInfo("外部宏命令-PG115")
                        self.PG102Flag=True
                        self.G_PhrozenFluiddRespondInfo("self.Flag=True")
                        command_string = """
                        PG115
                        """
                        self.G_PhrozenGCode.run_script_from_command(command_string)
                        self.G_PhrozenFluiddRespondInfo("外部宏命令-排废料；command_string='%s'" % command_string)
                    #lancaigang250528：
                    elif self.G_P10SpitNum==6:
                        self.G_PhrozenFluiddRespondInfo("外部宏命令-PG116")
                        self.PG102Flag=True
                        self.G_PhrozenFluiddRespondInfo("self.Flag=True")
                        command_string = """
                        PG116
                        """
                        self.G_PhrozenGCode.run_script_from_command(command_string)
                        self.G_PhrozenFluiddRespondInfo("外部宏命令-排废料；command_string='%s'" % command_string)
                    elif self.G_P10SpitNum==7:
                        self.G_PhrozenFluiddRespondInfo("外部宏命令-PG117")
                        self.PG102Flag=True
                        self.G_PhrozenFluiddRespondInfo("self.Flag=True")
                        command_string = """
                        PG117
                        """
                        self.G_PhrozenGCode.run_script_from_command(command_string)
                        self.G_PhrozenFluiddRespondInfo("外部宏命令-排废料；command_string='%s'" % command_string)
                    elif self.G_P10SpitNum==8:
                        self.G_PhrozenFluiddRespondInfo("外部宏命令-PG118")
                        self.PG102Flag=True
                        self.G_PhrozenFluiddRespondInfo("self.Flag=True")
                        command_string = """
                        PG118
                        """
                        self.G_PhrozenGCode.run_script_from_command(command_string)
                        self.G_PhrozenFluiddRespondInfo("外部宏命令-排废料；command_string='%s'" % command_string)
                    elif self.G_P10SpitNum==9:
                        self.G_PhrozenFluiddRespondInfo("外部宏命令-PG119")
                        self.PG102Flag=True
                        self.G_PhrozenFluiddRespondInfo("self.Flag=True")
                        command_string = """
                        PG119
                        """
                        self.G_PhrozenGCode.run_script_from_command(command_string)
                        self.G_PhrozenFluiddRespondInfo("外部宏命令-排废料；command_string='%s'" % command_string)

                    self.PG102Flag=False
                    self.G_PhrozenFluiddRespondInfo("self.Flag=False")
                    
                    self.G_PhrozenFluiddRespondInfo("吐料结束")
   
                    # for i in range(15):
                    #     self.G_PhrozenFluiddRespondInfo("[(dev.python)]吐料中，等待")
                    #     #lancaigang20231013：改为4秒延时
                    #     #lancaigang231115：改为1s
                    #     self.G_ProzenToolhead.dwell(1.0)
                    #     #lancaigang240125：不能用sleep，会阻塞主线程
                    #     #time.sleep(1)
                    if self.PG102DelayPauseFlag==True:
                        self.PG102DelayPauseFlag=False

                        #lancaigang250619:检查AMS是否重新连接成功
                        self.Cmds_USBConnectErrorCheck()
                        #lancaigang250427：
                        if self.G_SerialPort1OpenFlag == True:
                            self.Cmds_AMSSerial1Send("AT+EBLOCKEND")
                            self.G_PhrozenFluiddRespondInfo("串口1-AMS结束计时缓冲器满时间")
                        if self.G_SerialPort2OpenFlag == True:
                            self.Cmds_AMSSerial2Send("AT+EBLOCKEND")
                            self.G_PhrozenFluiddRespondInfo("串口2-AMS结束计时缓冲器满时间")

                        self.G_PhrozenFluiddRespondInfo("启用快速暂停")
                        self.G_KlipperQuickPause = True
                        self.G_PhrozenFluiddRespondInfo("吐料过程中，STM32触发了断料暂停")
                        #lancaigang231209：定时器中处理业务，会导致业务异常，后面要用线程处理中断业务

                        if self.G_KlipperInPausing == False:
                            self.G_PhrozenFluiddRespondInfo("不在暂停中，允许新的暂停")
                            #lancaigang250607:
                            self.G_PhrozenFluiddRespondInfo("启用快速暂停")
                            self.G_KlipperQuickPause = True
                            #klipper主动暂停
                            self.G_PhrozenFluiddRespondInfo("stm32主动暂停上报，暂停1次")
                            self.Cmds_PhrozenKlipperPauseNoneCmdToSTM32(None)
                        else:
                            self.G_PhrozenFluiddRespondInfo("暂停中，不允许新的暂停")

                        self.G_KlipperIfPaused = True
                        #stm32主动暂停只能暂停1次，不能重复暂停
                        self.STM32ReprotPauseFlag=1
                        #lancaigang231202：P1 C?自动换料时，如果第1次通道就进料异常暂停，如果要恢复，也继续从第1次通道开始
                        self.G_ChangeChannelFirstFilaFlag=True
                        
                        self.G_ProzenToolhead.dwell(1.5)
                        self.G_PhrozenFluiddRespondInfo("+MSG:1,1,%d,%d" % (self.G_ChangeChannelTimeoutOldChan,self.G_ChangeChannelTimeoutNewChan))
                        #lancaigang240524：用于UIUX动态界面
                        self.G_PhrozenFluiddRespondInfo("+C:1,%d" % self.G_ChangeChannelTimeoutNewChan)
                        

                        #self.G_PhrozenFluiddRespondInfo(self.G_PauseToLCDString)
                        #lancaigang250529:
                        if len(self.G_PauseToLCDString)==0:
                            self.G_PhrozenFluiddRespondInfo("+PAUSE:4,%d,%d" % (self.G_ChangeChannelTimeoutOldChan,self.G_ChangeChannelTimeoutNewChan))
                        else:
                            self.G_PhrozenFluiddRespondInfo(self.G_PauseToLCDString)

                        #lancaigang250607：打印状态；1-退料中；2-进料中；3-打印中；4-暂停
                        self.G_KlipperPrintStatus= 3
                        self.G_PauseToLCDString=""
                        
                        self.G_PhrozenFluiddRespondInfo("return")
                        return

                        #lancaigang240326：吐料期间的暂停，统一使用暂停1表示
                        #self.G_PhrozenFluiddRespondInfo("+PAUSE:1,%d" % self.G_ChangeChannelTimeoutNewChan)
                    else:
                        self.G_PhrozenFluiddRespondInfo("吐料过程正常，进入打印")
                        #lancaigang250527：换料成功并进入gocde文件打印
                        #lancaigang250527：暂停快速执行
                        self.G_KlipperQuickPause = True


                self.G_PhrozenFluiddRespondInfo("+MSG:1,1,%d,%d" % (self.G_ChangeChannelTimeoutOldChan,self.G_ChangeChannelTimeoutNewChan))

                #lancaigang250619:检查AMS是否重新连接成功
                self.Cmds_USBConnectErrorCheck()
                #lancaigang250427：
                if self.G_SerialPort1OpenFlag == True:
                    self.Cmds_AMSSerial1Send("AT+EBLOCKEND")
                    self.G_PhrozenFluiddRespondInfo("串口1-AMS结束计时缓冲器满时间")
                if self.G_SerialPort2OpenFlag == True:
                    self.Cmds_AMSSerial2Send("AT+EBLOCKEND")
                    self.G_PhrozenFluiddRespondInfo("串口2-AMS结束计时缓冲器满时间")
                self.G_ProzenToolhead.dwell(1.5)



                #lancaigang240524：用于UIUX动态界面
                self.G_PhrozenFluiddRespondInfo("+C:1,%d" % self.G_ChangeChannelTimeoutNewChan)


                #lancaigang250607：打印状态；1-退料中；2-进料中；3-打印中；4-暂停
                self.G_KlipperPrintStatus= 3

                self.G_PauseToLCDString=""

                self.G_PhrozenFluiddRespondInfo("正常进入打印")

                return
            





            self.G_PhrozenFluiddRespondInfo("换料失败")
            self.G_PhrozenFluiddRespondInfo("self.G_ToolheadIfHaveFilaFlag=%d" % (self.G_ToolheadIfHaveFilaFlag))
            # 换料失败
            if self.G_DictChangeChannelWaitAreaParam["A"] == 0:
                self.G_PhrozenFluiddRespondInfo("换料失败；线材进料超时；cmd='%s', 全部回退线材，klipper暂停")
                self.G_PhrozenFluiddRespondInfo("换料失败；当前缓存的命令='%s';klipper暂停" % (self.G_ChangeChannelTimeoutOldGcmd.get_commandline()))
                
                #lancaigang250527：暂停快速执行
                self.G_KlipperQuickPause = False

                #lancaigang250619:检查AMS是否重新连接成功
                self.Cmds_USBConnectErrorCheck()

                # #lancaigang231129：klipper暂停时，喷头移动到z=10；x=150；y=10
                # command_string = """
                # G91
                # G1 z10 F600
                # G90
                # G1 X150 F600
                # G1 Y10 F600
                # """
                # self.G_PhrozenGCode.run_script_from_command(command_string)
                
                #lancaigang231201：klipper暂停时stm32电机不能动
                # gcmd.respond_info("发送命令: AP，全部后退到停靠位")
                # #// 全部后退到停靠位；//===== P2 A1 所有线料退到停靠位待打印 Yes；"AP"；
                # self.Cmds_AMSSerial1Send("AP")
                # logging.info("SendCmd: AP")
                if self.G_KlipperIfPaused==False:
                    #lancaigang250702：
                    if self.G_KlipperInPausing == False:
                        self.G_PhrozenFluiddRespondInfo("不在暂停中，允许新的暂停")
                        self.STM32ReprotPauseFlag=1
                        #lancaigang231202：P1 C?自动换料时，如果第1次通道就进料异常暂停，如果要恢复，也继续从第1次通道开始
                        self.G_ChangeChannelFirstFilaFlag=True

                        
                        #lancaigang240416:
                        if self.G_SerialPort1OpenFlag == True:
                            #lancaigang240603：防止AMS一直停不了
                            self.Cmds_AMSSerial1Send("AT+PAUSE")
                            self.G_PhrozenFluiddRespondInfo("串口1-AT+PAUSE暂停stm32电机")
                        #lancaigang241030:
                        if self.G_SerialPort2OpenFlag == True:
                            self.Cmds_AMSSerial2Send("AT+PAUSE")
                            self.G_PhrozenFluiddRespondInfo("串口2-AT+PAUSE暂停stm32电机")

                        self.G_PhrozenFluiddRespondInfo("启用快速暂停")
                        self.G_KlipperQuickPause = True
                        #klipper主动暂停
                        self.Cmds_PhrozenKlipperPause(None)
                        self.G_KlipperIfPaused = True
                        #self.G_PhrozenFluiddRespondInfo("+PAUSE:4,%d" % self.G_ChangeChannelTimeoutNewChan)

                        self.G_PhrozenFluiddRespondInfo("换料超时60s，暂停")
                        #self.G_PhrozenFluiddRespondInfo("+PAUSE:4,%d,%d" % (self.G_ChangeChannelTimeoutOldChan,self.G_ChangeChannelTimeoutNewChan))
                        #self.G_PhrozenFluiddRespondInfo("+PAUSE:4,%d,%d" % (self.G_ChangeChannelTimeoutOldChan,self.G_ChangeChannelTimeoutNewChan))
                        #lancaigang250529:
                        if len(self.G_PauseToLCDString)==0:
                            self.G_PhrozenFluiddRespondInfo("+PAUSE:4,%d,%d" % (self.G_ChangeChannelTimeoutOldChan,self.G_ChangeChannelTimeoutNewChan))
                        else:
                            self.G_PhrozenFluiddRespondInfo(self.G_PauseToLCDString)

                    else:
                        self.G_PhrozenFluiddRespondInfo("暂停中，不允许新的暂停")
                #lancaigang240124：不能重复暂停
                else:
                    self.G_PhrozenFluiddRespondInfo("已经暂停了，不用重复暂停")
                    # #lancaigang250529:
                    # if len(self.G_PauseToLCDString)==0:
                    #     self.G_PhrozenFluiddRespondInfo("+PAUSE:4,%d,%d" % (self.G_ChangeChannelTimeoutOldChan,self.G_ChangeChannelTimeoutNewChan))
                    # else:
                    #     self.G_PhrozenFluiddRespondInfo(self.G_PauseToLCDString)

                    #self.G_PhrozenFluiddRespondInfo(self.G_PauseToLCDString)
                    #lancaigang240417：防止stm32没上报时G_PauseToLCDString为空的情况
                    #if len(self.G_PauseToLCDString)==0:
                    #    self.G_PhrozenFluiddRespondInfo("+PAUSE:4,%d,%d" % (self.G_ChangeChannelTimeoutOldChan,self.G_ChangeChannelTimeoutNewChan))
                    #lancaigang250529:
                    if len(self.G_PauseToLCDString)==0:
                        self.G_PhrozenFluiddRespondInfo("+PAUSE:4,%d,%d" % (self.G_ChangeChannelTimeoutOldChan,self.G_ChangeChannelTimeoutNewChan))
                    else:
                        self.G_PhrozenFluiddRespondInfo(self.G_PauseToLCDString)
                    #lancaigang240416:
                    if self.G_SerialPort1OpenFlag == True:
                        #lancaigang240603：防止AMS一直停不了
                        self.Cmds_AMSSerial1Send("AT+PAUSE")
                        self.G_PhrozenFluiddRespondInfo("串口1-AT+PAUSE暂停stm32电机")
                    #lancaigang241030:
                    if self.G_SerialPort2OpenFlag == True:
                        self.Cmds_AMSSerial2Send("AT+PAUSE")
                        self.G_PhrozenFluiddRespondInfo("串口2-AT+PAUSE暂停stm32电机")
                    #lancaigang240429：如果恢复过程中stm32并没有上报暂停状态，这里需要上报暂停
                    # if self.G_ResumeProcessCheckPauseStatus==False:
                    #     self.G_PhrozenFluiddRespondInfo("+PAUSE:4,%d" % self.G_ChangeChannelTimeoutNewChan)

                    if self.G_ResumeProcessCheckPauseStatus==False:
                        self.G_PhrozenFluiddRespondInfo("AMS没有上报暂停，klipper重复暂停，需要上报暂停")
                        #self.G_PhrozenFluiddRespondInfo("+PAUSE:4,%d,%d" % (self.G_ChangeChannelTimeoutOldChan,self.G_ChangeChannelTimeoutNewChan))
                        #lancaigang250529:
                        if len(self.G_PauseToLCDString)==0:
                            self.G_PhrozenFluiddRespondInfo("+PAUSE:4,%d,%d" % (self.G_ChangeChannelTimeoutOldChan,self.G_ChangeChannelTimeoutNewChan))
                        else:
                            self.G_PhrozenFluiddRespondInfo(self.G_PauseToLCDString)
                        
                        #lancaigang240416:
                        if self.G_SerialPort1OpenFlag == True:
                            #lancaigang240603：防止AMS一直停不了
                            self.Cmds_AMSSerial1Send("AT+PAUSE")
                            self.G_PhrozenFluiddRespondInfo("串口1-AT+PAUSE暂停stm32电机")
                        #lancaigang241030:
                        if self.G_SerialPort2OpenFlag == True:
                            self.Cmds_AMSSerial2Send("AT+PAUSE")
                            self.G_PhrozenFluiddRespondInfo("串口2-AT+PAUSE暂停stm32电机")
                    else:
                        self.G_PhrozenFluiddRespondInfo("AMS有上报暂停，klipper不需要需要上报暂停")
                        self.G_ResumeProcessCheckPauseStatus=False

                    # self.G_PhrozenFluiddRespondInfo("已经暂停了，再暂停1次，防止之前暂停异常")
                    # #lancaigang250423：为了防止异常暂停不住，多暂停1次
                    # #klipper主动暂停
                    # self.Cmds_PhrozenKlipperPause(None)

                #lancaigang231207：P1 C?自动换料时，如果要恢复，也继续从第1次通道开始
                self.G_ChangeChannelFirstFilaFlag=True
                self.G_IfChangeFilaOngoing= False

                #lancaigang240524：用于UIUX动态界面
                self.G_PhrozenFluiddRespondInfo("+C:1,%d" % self.G_ChangeChannelTimeoutNewChan)

                #lancaigang250607：打印状态；1-退料中；2-进料中；3-打印中；4-暂停
                self.G_KlipperPrintStatus= -1

                return
            
            #lancaigang20231013：Action正常换料=1
            if self.G_DictChangeChannelWaitAreaParam["A"] == 1:
                pass



    ####################################
    #函数名称：
    #输入参数：
    #返 回 值:
    #功能描述：蓝才刚-20230830
    ####################################
    def Cmds_CmdOrcaPre(self):
        self.G_PhrozenFluiddRespondInfo("=====[(cmds.python)Cmds_CmdOrcaPre]orca前置动作" )

        #lancaigang250912：测试多喷头；先到指定坐标顶开插销，然后触发GPIO实现多喷头正反转，多喷头正反转到位有光电和电机控制

        #lancaigang250515：单机打多色，不处理T?
        if self.G_P0M1MCNoneAMS == 1:
            self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_CmdOrcaPre]单机打多色，不处理T?")
            #lancaigang250828:
            self.G_PhrozenFluiddRespondInfo("外部宏命令-PRZ_PAUSE_WAITINGAREA")
            command_string = """
                PRZ_PAUSE_WAITINGAREA
                """
            self.G_PhrozenGCode.run_script_from_command(command_string)
            #self.G_PhrozenFluiddRespondInfo("外部宏命令；command_string='%s'" % command_string)

            return
        
        #lancaigang250429：
        if self.G_AMSDeviceWorkMode==AMS_WORK_MODE_FILA_RUNOUT:
            self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_CmdOrcaPre]单色模式，不处理T?")
            #lancaigang250828:
            self.G_PhrozenFluiddRespondInfo("外部宏命令-PRZ_PAUSE_WAITINGAREA")
            command_string = """
                PRZ_PAUSE_WAITINGAREA
                """
            self.G_PhrozenGCode.run_script_from_command(command_string)
            #self.G_PhrozenFluiddRespondInfo("外部宏命令；command_string='%s'" % command_string)
            return
        
        #lancaigang250514：
        if self.G_AMSDeviceWorkMode==AMS_WORK_MODE_MA :
            self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_CmdOrcaPre]单色续料模式，不处理T?")
            #lancaigang250828:
            self.G_PhrozenFluiddRespondInfo("外部宏命令-PRZ_PAUSE_WAITINGAREA")
            command_string = """
                PRZ_PAUSE_WAITINGAREA
                """
            self.G_PhrozenGCode.run_script_from_command(command_string)
            #self.G_PhrozenFluiddRespondInfo("外部宏命令；command_string='%s'" % command_string)
            return

        #lancaigang240527：未知模式，因为要操作手动命令，默认让STM32进入MC多色模式
        if self.G_AMSDeviceWorkMode == AMS_WORK_MODE_UNKNOW:
            self.G_PhrozenFluiddRespondInfo("未知模式，因为要操作手动命令，默认让STM32进入MC多色模式")
            self.G_PhrozenFluiddRespondInfo("如果收到T?命令，但模式是未知模式，强制转换为MC多色模式")
            self.G_AMSDeviceWorkMode = AMS_WORK_MODE_MC
            #lancaigang241030:
            if self.G_SerialPort1OpenFlag == True:
                self.Cmds_AMSSerial1Send("MC")
                self.G_PhrozenFluiddRespondInfo("串口1发送命令：MC")
            #lancaigang241030:
            if self.G_SerialPort2OpenFlag == True:
                self.Cmds_AMSSerial2Send("MC")
                self.G_PhrozenFluiddRespondInfo("串口2发送命令：MC")
        
            self.G_ProzenToolhead.dwell(2)



    ####################################
    #函数名称：
    #输入参数：
    #返 回 值:
    #功能描述：蓝才刚-20230830
    ####################################
    def Cmds_CmdT0(self,gcmd):
        self.G_PhrozenFluiddRespondInfo("=====[(cmds.python)Cmds_CmdT0 +1]orca切片多色换料" )

        self.G_PhrozenFluiddRespondInfo("=====self.G_ChangeChannelTimeoutOldChan=%d" % self.G_ChangeChannelTimeoutOldChan)
        self.G_PhrozenFluiddRespondInfo("=====self.G_ChangeChannelTimeoutNewChan=%d" % self.G_ChangeChannelTimeoutNewChan)

        #lancaigang250515：单机打多色，不处理T?
        if self.G_P0M1MCNoneAMS == 1:
            self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_CmdT1]单机打多色，不处理T?")
            #lancaigang250828:
            self.G_PhrozenFluiddRespondInfo("外部宏命令-PRZ_PAUSE_WAITINGAREA")
            command_string = """
                PRZ_PAUSE_WAITINGAREA
                """
            self.G_PhrozenGCode.run_script_from_command(command_string)
            self.G_PhrozenFluiddRespondInfo("外部宏命令；command_string='%s'" % command_string)
            return
        #lancaigang250429：
        if self.G_AMSDeviceWorkMode==AMS_WORK_MODE_FILA_RUNOUT:
            self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_CmdT1]单色模式，不处理T0")
            #lancaigang250828:
            self.G_PhrozenFluiddRespondInfo("外部宏命令-PRZ_PAUSE_WAITINGAREA")
            command_string = """
                PRZ_PAUSE_WAITINGAREA
                """
            self.G_PhrozenGCode.run_script_from_command(command_string)
            self.G_PhrozenFluiddRespondInfo("外部宏命令；command_string='%s'" % command_string)
            return
        #lancaigang250514：
        if self.G_AMSDeviceWorkMode==AMS_WORK_MODE_MA :
            self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_CmdT1]单色续料模式，不处理T0")
            #lancaigang250828:
            self.G_PhrozenFluiddRespondInfo("外部宏命令-PRZ_PAUSE_WAITINGAREA")
            command_string = """
                PRZ_PAUSE_WAITINGAREA
                """
            self.G_PhrozenGCode.run_script_from_command(command_string)
            self.G_PhrozenFluiddRespondInfo("外部宏命令；command_string='%s'" % command_string)
            return

        #lancaigang240527：未知模式，因为要操作手动命令，默认让STM32进入MC多色模式
        if self.G_AMSDeviceWorkMode == AMS_WORK_MODE_UNKNOW:
            self.G_PhrozenFluiddRespondInfo("未知模式，因为要操作手动命令，默认让STM32进入MC多色模式")
            self.G_PhrozenFluiddRespondInfo("如果收到T?命令，但模式是未知模式，强制转换为MC多色模式")
            self.G_AMSDeviceWorkMode = AMS_WORK_MODE_MC
            #lancaigang241030:
            if self.G_SerialPort1OpenFlag == True:
                self.Cmds_AMSSerial1Send("MC")
                self.G_PhrozenFluiddRespondInfo("串口1发送命令：MC")
            #lancaigang241030:
            if self.G_SerialPort2OpenFlag == True:
                self.Cmds_AMSSerial2Send("MC")
                self.G_PhrozenFluiddRespondInfo("串口2发送命令：MC")

            self.G_ProzenToolhead.dwell(2)


        #lancaigang250912:
        #self.Cmds_CmdOrcaPre()

        
        #self.G_PhrozenFluiddRespondInfo("命令='%s'；自动换料" % (gcmd.get_commandline(),))
        self.G_PhrozenFluiddRespondInfo("自动换料")
        #lancaigang240524：用于UIUX动态界面
        self.G_PhrozenFluiddRespondInfo("+T0:0,%d" % self.G_ChangeChannelTimeoutNewChan)

        # #cancel取消命令
        # self.G_PhrozenPrinterCancelPauseResume.cmd_CANCEL_PRINT(None)
        #lancaigang250517：
        Lo_PauseStatus=self.G_PhrozenPrinterCancelPauseResume.get_status(None)
        self.G_PhrozenFluiddRespondInfo("当前暂停状态-Lo_PauseStatus='%s'" % Lo_PauseStatus)
        self.G_PhrozenFluiddRespondInfo("Lo_PauseStatus['is_paused']='%s'" % Lo_PauseStatus['is_paused'])
        #// 当前暂停状态-Lo_PauseStatus='{'is_paused': True}'
        if Lo_PauseStatus['is_paused'] == True:
            self.G_PhrozenFluiddRespondInfo("已是暂停状态")
        else:
            self.G_PhrozenFluiddRespondInfo("未暂停状态")
        #lancaigang240113：清除手动命令标志
        self.ManualCmdFlag=False
        #lancaigang240221：stm32主动上报，开启可以暂停1次
        self.STM32ReprotPauseFlag=0
        self.G_PhrozenFluiddRespondInfo("self.STM32ReprotPauseFlag=0")

        #lancaigang241030：一般是P1 C1到P1 C32，范围在1到32
        #第1台：1 2 3 4
        #第2台：5 6 7 8
        #第3台：9 10 11 12
        #第4台：13 14 15 16
        #第5台：17 18 19 20
        #第6台：21 22 23 24
        #第7台：25 26 27 28
        #第8台：29 30 31 32
        #自动换料
        chan=0+1
        self.G_PhrozenFluiddRespondInfo("chan=%d" % chan)

        #lancaigang250515:判断串口屏配置的颜色匹对通道
        if self.G_ChromaKitAccessT0 > 0:
            self.G_PhrozenFluiddRespondInfo("self.G_ChromaKitAccessT0=%d" % self.G_ChromaKitAccessT0)
            self.Cmds_P1CnAutoChangeChannel(self.G_ChromaKitAccessT0, gcmd)
        else:
            self.G_PhrozenFluiddRespondInfo("chan=%d" % chan)
            self.Cmds_P1CnAutoChangeChannel(chan, gcmd)

        #lancaigang240524：用于UIUX动态界面
        self.G_PhrozenFluiddRespondInfo("+T0:1,%d" % self.G_ChangeChannelTimeoutNewChan)


    ####################################
    #函数名称：
    #输入参数：
    #返 回 值:
    #功能描述：蓝才刚-20230830
    ####################################
    def Cmds_CmdT1(self,gcmd):
        self.G_PhrozenFluiddRespondInfo("=====[(cmds.python)Cmds_CmdT1 +1]orca切片多色换料" )

        self.G_PhrozenFluiddRespondInfo("=====self.G_ChangeChannelTimeoutOldChan=%d" % self.G_ChangeChannelTimeoutOldChan)
        self.G_PhrozenFluiddRespondInfo("=====self.G_ChangeChannelTimeoutNewChan=%d" % self.G_ChangeChannelTimeoutNewChan)

        #lancaigang250515：单机打多色，不处理T?
        if self.G_P0M1MCNoneAMS == 1:
            self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_CmdT1]单机打多色，不处理T?")
            #lancaigang250828:
            self.G_PhrozenFluiddRespondInfo("外部宏命令-PRZ_PAUSE_WAITINGAREA")
            command_string = """
                PRZ_PAUSE_WAITINGAREA
                """
            self.G_PhrozenGCode.run_script_from_command(command_string)
            self.G_PhrozenFluiddRespondInfo("外部宏命令；command_string='%s'" % command_string)
            return
        #lancaigang250429：
        if self.G_AMSDeviceWorkMode==AMS_WORK_MODE_FILA_RUNOUT:
            self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_CmdT1]单色模式，不处理T1")
            #lancaigang250828:
            self.G_PhrozenFluiddRespondInfo("外部宏命令-PRZ_PAUSE_WAITINGAREA")
            command_string = """
                PRZ_PAUSE_WAITINGAREA
                """
            self.G_PhrozenGCode.run_script_from_command(command_string)
            self.G_PhrozenFluiddRespondInfo("外部宏命令；command_string='%s'" % command_string)
            return
        #lancaigang250514：
        if self.G_AMSDeviceWorkMode==AMS_WORK_MODE_MA :
            self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_CmdT1]单色续料模式，不处理T1")
            #lancaigang250828:
            self.G_PhrozenFluiddRespondInfo("外部宏命令-PRZ_PAUSE_WAITINGAREA")
            command_string = """
                PRZ_PAUSE_WAITINGAREA
                """
            self.G_PhrozenGCode.run_script_from_command(command_string)
            self.G_PhrozenFluiddRespondInfo("外部宏命令；command_string='%s'" % command_string)
            return

        #lancaigang240527：未知模式，因为要操作手动命令，默认让STM32进入MC多色模式
        if self.G_AMSDeviceWorkMode == AMS_WORK_MODE_UNKNOW:
            self.G_PhrozenFluiddRespondInfo("未知模式，因为要操作手动命令，默认让STM32进入MC多色模式")
            self.G_PhrozenFluiddRespondInfo("如果收到T?命令，但模式是未知模式，强制转换为MC多色模式")
            self.G_AMSDeviceWorkMode = AMS_WORK_MODE_MC
            #lancaigang241030:
            if self.G_SerialPort1OpenFlag == True:
                self.Cmds_AMSSerial1Send("MC")
                self.G_PhrozenFluiddRespondInfo("串口1发送命令：MC")
            #lancaigang241030:
            if self.G_SerialPort2OpenFlag == True:
                self.Cmds_AMSSerial2Send("MC")
                self.G_PhrozenFluiddRespondInfo("串口2发送命令：MC")

            self.G_ProzenToolhead.dwell(2)
        
        #lancaigang250912:导致return异常
        #self.Cmds_CmdOrcaPre()



        #self.G_PhrozenFluiddRespondInfo("命令='%s'；自动换料" % (gcmd.get_commandline(),))
        self.G_PhrozenFluiddRespondInfo("自动换料")
        #lancaigang240524：用于UIUX动态界面
        self.G_PhrozenFluiddRespondInfo("+T1:0,%d" % self.G_ChangeChannelTimeoutNewChan)
        # #cancel取消命令
        # self.G_PhrozenPrinterCancelPauseResume.cmd_CANCEL_PRINT(None)
        #lancaigang250517：
        Lo_PauseStatus=self.G_PhrozenPrinterCancelPauseResume.get_status(None)
        self.G_PhrozenFluiddRespondInfo("当前暂停状态-Lo_PauseStatus='%s'" % Lo_PauseStatus)
        self.G_PhrozenFluiddRespondInfo("Lo_PauseStatus['is_paused']='%s'" % Lo_PauseStatus['is_paused'])
        #// 当前暂停状态-Lo_PauseStatus='{'is_paused': True}'
        if Lo_PauseStatus['is_paused'] == True:
            self.G_PhrozenFluiddRespondInfo("已是暂停状态")
        else:
            self.G_PhrozenFluiddRespondInfo("未暂停状态")
        #lancaigang240113：清除手动命令标志
        self.ManualCmdFlag=False
        #lancaigang240221：stm32主动上报，开启可以暂停1次
        self.STM32ReprotPauseFlag=0
        self.G_PhrozenFluiddRespondInfo("self.STM32ReprotPauseFlag=0")

        #lancaigang241030：一般是P1 C1到P1 C32，范围在1到32
        #第1台：1 2 3 4
        #第2台：5 6 7 8
        #第3台：9 10 11 12
        #第4台：13 14 15 16
        #第5台：17 18 19 20
        #第6台：21 22 23 24
        #第7台：25 26 27 28
        #第8台：29 30 31 32
        #自动换料
        chan=1+1
        self.G_PhrozenFluiddRespondInfo("chan=%d" % chan)

        #lancaigang250515:判断串口屏配置的颜色匹对通道
        if self.G_ChromaKitAccessT1 > 0:
            self.G_PhrozenFluiddRespondInfo("self.G_ChromaKitAccessT1=%d" % self.G_ChromaKitAccessT1)
            self.Cmds_P1CnAutoChangeChannel(self.G_ChromaKitAccessT1, gcmd)
        else:
            self.G_PhrozenFluiddRespondInfo("chan=%d" % chan)
            self.Cmds_P1CnAutoChangeChannel(chan, gcmd)

        #lancaigang240524：用于UIUX动态界面
        self.G_PhrozenFluiddRespondInfo("+T1:1,%d" % self.G_ChangeChannelTimeoutNewChan)

    ####################################
    #函数名称：
    #输入参数：
    #返 回 值:
    #功能描述：蓝才刚-20230830
    ####################################
    def Cmds_CmdT2(self,gcmd):
        self.G_PhrozenFluiddRespondInfo("=====[(cmds.python)Cmds_CmdT2 +1]orca切片多色换料" )

        self.G_PhrozenFluiddRespondInfo("=====self.G_ChangeChannelTimeoutOldChan=%d" % self.G_ChangeChannelTimeoutOldChan)
        self.G_PhrozenFluiddRespondInfo("=====self.G_ChangeChannelTimeoutNewChan=%d" % self.G_ChangeChannelTimeoutNewChan)

        #lancaigang250515：单机打多色，不处理T?
        if self.G_P0M1MCNoneAMS == 1:
            self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_CmdT2]单机打多色，不处理T?")
            #lancaigang250828:
            self.G_PhrozenFluiddRespondInfo("外部宏命令-PRZ_PAUSE_WAITINGAREA")
            command_string = """
                PRZ_PAUSE_WAITINGAREA
                """
            self.G_PhrozenGCode.run_script_from_command(command_string)
            self.G_PhrozenFluiddRespondInfo("外部宏命令；command_string='%s'" % command_string)
            return
        #lancaigang250429：
        if self.G_AMSDeviceWorkMode==AMS_WORK_MODE_FILA_RUNOUT:
            self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_CmdT2]单色模式，不处理T2")
            #lancaigang250828:
            self.G_PhrozenFluiddRespondInfo("外部宏命令-PRZ_PAUSE_WAITINGAREA")
            command_string = """
                PRZ_PAUSE_WAITINGAREA
                """
            self.G_PhrozenGCode.run_script_from_command(command_string)
            self.G_PhrozenFluiddRespondInfo("外部宏命令；command_string='%s'" % command_string)
            return
        #lancaigang250514：
        if self.G_AMSDeviceWorkMode==AMS_WORK_MODE_MA :
            self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_CmdT2]单色续料模式，不处理T2")
            #lancaigang250828:
            self.G_PhrozenFluiddRespondInfo("外部宏命令-PRZ_PAUSE_WAITINGAREA")
            command_string = """
                PRZ_PAUSE_WAITINGAREA
                """
            self.G_PhrozenGCode.run_script_from_command(command_string)
            self.G_PhrozenFluiddRespondInfo("外部宏命令；command_string='%s'" % command_string)
            return

        #lancaigang240527：未知模式，因为要操作手动命令，默认让STM32进入MC多色模式
        if self.G_AMSDeviceWorkMode == AMS_WORK_MODE_UNKNOW:
            self.G_PhrozenFluiddRespondInfo("未知模式，因为要操作手动命令，默认让STM32进入MC多色模式")
            self.G_PhrozenFluiddRespondInfo("如果收到T?命令，但模式是未知模式，强制转换为MC多色模式")
            self.G_AMSDeviceWorkMode = AMS_WORK_MODE_MC
            #lancaigang241030:
            if self.G_SerialPort1OpenFlag == True:
                self.Cmds_AMSSerial1Send("MC")
                self.G_PhrozenFluiddRespondInfo("串口1发送命令：MC")
            #lancaigang241030:
            if self.G_SerialPort2OpenFlag == True:
                self.Cmds_AMSSerial2Send("MC")
                self.G_PhrozenFluiddRespondInfo("串口2发送命令：MC")

            self.G_ProzenToolhead.dwell(2)

        #lancaigang250912:导致return异常
        #self.Cmds_CmdOrcaPre()

        
        #self.G_PhrozenFluiddRespondInfo("命令='%s'；自动换料" % (gcmd.get_commandline(),))
        self.G_PhrozenFluiddRespondInfo("自动换料")
        #lancaigang240524：用于UIUX动态界面
        self.G_PhrozenFluiddRespondInfo("+T2:0,%d" % self.G_ChangeChannelTimeoutNewChan)
        # #cancel取消命令
        # self.G_PhrozenPrinterCancelPauseResume.cmd_CANCEL_PRINT(None)
        #lancaigang250517：
        Lo_PauseStatus=self.G_PhrozenPrinterCancelPauseResume.get_status(None)
        self.G_PhrozenFluiddRespondInfo("当前暂停状态-Lo_PauseStatus='%s'" % Lo_PauseStatus)
        self.G_PhrozenFluiddRespondInfo("Lo_PauseStatus['is_paused']='%s'" % Lo_PauseStatus['is_paused'])
        #// 当前暂停状态-Lo_PauseStatus='{'is_paused': True}'
        if Lo_PauseStatus['is_paused'] == True:
            self.G_PhrozenFluiddRespondInfo("已是暂停状态")
        else:
            self.G_PhrozenFluiddRespondInfo("未暂停状态")
        #lancaigang240113：清除手动命令标志
        self.ManualCmdFlag=False
        #lancaigang240221：stm32主动上报，开启可以暂停1次
        self.STM32ReprotPauseFlag=0
        self.G_PhrozenFluiddRespondInfo("self.STM32ReprotPauseFlag=0")

        #lancaigang241030：一般是P1 C1到P1 C32，范围在1到32
        #第1台：1 2 3 4
        #第2台：5 6 7 8
        #第3台：9 10 11 12
        #第4台：13 14 15 16
        #第5台：17 18 19 20
        #第6台：21 22 23 24
        #第7台：25 26 27 28
        #第8台：29 30 31 32
        #自动换料
        chan=2+1
        self.G_PhrozenFluiddRespondInfo("chan=%d" % chan)
        #lancaigang250515:判断串口屏配置的颜色匹对通道
        if self.G_ChromaKitAccessT2 > 0:
            self.G_PhrozenFluiddRespondInfo("self.G_ChromaKitAccessT2=%d" % self.G_ChromaKitAccessT2)
            self.Cmds_P1CnAutoChangeChannel(self.G_ChromaKitAccessT2, gcmd)
        else:
            self.G_PhrozenFluiddRespondInfo("chan=%d" % chan)
            self.Cmds_P1CnAutoChangeChannel(chan, gcmd)

        #lancaigang240524：用于UIUX动态界面
        self.G_PhrozenFluiddRespondInfo("+T2:1,%d" % self.G_ChangeChannelTimeoutNewChan)

    ####################################
    #函数名称：
    #输入参数：
    #返 回 值:
    #功能描述：蓝才刚-20230830
    ####################################
    def Cmds_CmdT3(self,gcmd):
        self.G_PhrozenFluiddRespondInfo("=====[(cmds.python)Cmds_CmdT3 +1]orca切片多色换料" )

        self.G_PhrozenFluiddRespondInfo("=====self.G_ChangeChannelTimeoutOldChan=%d" % self.G_ChangeChannelTimeoutOldChan)
        self.G_PhrozenFluiddRespondInfo("=====self.G_ChangeChannelTimeoutNewChan=%d" % self.G_ChangeChannelTimeoutNewChan)


        #lancaigang250515：单机打多色，不处理T?
        if self.G_P0M1MCNoneAMS == 1:
            self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_CmdT3]单机打多色，不处理T?")
            #lancaigang250828:
            self.G_PhrozenFluiddRespondInfo("外部宏命令-PRZ_PAUSE_WAITINGAREA")
            command_string = """
                PRZ_PAUSE_WAITINGAREA
                """
            self.G_PhrozenGCode.run_script_from_command(command_string)
            self.G_PhrozenFluiddRespondInfo("外部宏命令；command_string='%s'" % command_string)
            return
        #lancaigang250429：
        if self.G_AMSDeviceWorkMode==AMS_WORK_MODE_FILA_RUNOUT:
            self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_CmdT3]单色模式，不处理T3")
            #lancaigang250828:
            self.G_PhrozenFluiddRespondInfo("外部宏命令-PRZ_PAUSE_WAITINGAREA")
            command_string = """
                PRZ_PAUSE_WAITINGAREA
                """
            self.G_PhrozenGCode.run_script_from_command(command_string)
            self.G_PhrozenFluiddRespondInfo("外部宏命令；command_string='%s'" % command_string)
            return
        #lancaigang250514：
        if self.G_AMSDeviceWorkMode==AMS_WORK_MODE_MA :
            self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_CmdT3]单色续料模式，不处理T3")
            #lancaigang250828:
            self.G_PhrozenFluiddRespondInfo("外部宏命令-PRZ_PAUSE_WAITINGAREA")
            command_string = """
                PRZ_PAUSE_WAITINGAREA
                """
            self.G_PhrozenGCode.run_script_from_command(command_string)
            self.G_PhrozenFluiddRespondInfo("外部宏命令；command_string='%s'" % command_string)
            return

        #lancaigang240527：未知模式，因为要操作手动命令，默认让STM32进入MC多色模式
        if self.G_AMSDeviceWorkMode == AMS_WORK_MODE_UNKNOW:
            self.G_PhrozenFluiddRespondInfo("未知模式，因为要操作手动命令，默认让STM32进入MC多色模式")
            self.G_PhrozenFluiddRespondInfo("如果收到T?命令，但模式是未知模式，强制转换为MC多色模式")
            self.G_AMSDeviceWorkMode = AMS_WORK_MODE_MC
            #lancaigang241030:
            if self.G_SerialPort1OpenFlag == True:
                self.Cmds_AMSSerial1Send("MC")
                self.G_PhrozenFluiddRespondInfo("串口1发送命令：MC")
            #lancaigang241030:
            if self.G_SerialPort2OpenFlag == True:
                self.Cmds_AMSSerial2Send("MC")
                self.G_PhrozenFluiddRespondInfo("串口2发送命令：MC")

            self.G_ProzenToolhead.dwell(2)

        #lancaigang250912:
        #self.Cmds_CmdOrcaPre()

        
        
        #self.G_PhrozenFluiddRespondInfo("命令='%s'；自动换料" % (gcmd.get_commandline(),))
        self.G_PhrozenFluiddRespondInfo("自动换料")
        #lancaigang240524：用于UIUX动态界面
        self.G_PhrozenFluiddRespondInfo("+T3:0,%d" % self.G_ChangeChannelTimeoutNewChan)
        # #cancel取消命令
        # self.G_PhrozenPrinterCancelPauseResume.cmd_CANCEL_PRINT(None)
        #lancaigang250517：
        Lo_PauseStatus=self.G_PhrozenPrinterCancelPauseResume.get_status(None)
        self.G_PhrozenFluiddRespondInfo("当前暂停状态-Lo_PauseStatus='%s'" % Lo_PauseStatus)
        self.G_PhrozenFluiddRespondInfo("Lo_PauseStatus['is_paused']='%s'" % Lo_PauseStatus['is_paused'])
        #// 当前暂停状态-Lo_PauseStatus='{'is_paused': True}'
        if Lo_PauseStatus['is_paused'] == True:
            self.G_PhrozenFluiddRespondInfo("已是暂停状态")
        else:
            self.G_PhrozenFluiddRespondInfo("未暂停状态")
        #lancaigang240113：清除手动命令标志
        self.ManualCmdFlag=False
        #lancaigang240221：stm32主动上报，开启可以暂停1次
        self.STM32ReprotPauseFlag=0
        self.G_PhrozenFluiddRespondInfo("self.STM32ReprotPauseFlag=0")

        #lancaigang241030：一般是P1 C1到P1 C32，范围在1到32
        #第1台：1 2 3 4
        #第2台：5 6 7 8
        #第3台：9 10 11 12
        #第4台：13 14 15 16
        #第5台：17 18 19 20
        #第6台：21 22 23 24
        #第7台：25 26 27 28
        #第8台：29 30 31 32
        #自动换料
        chan=3+1
        self.G_PhrozenFluiddRespondInfo("chan=%d" % chan)
        #lancaigang250515:判断串口屏配置的颜色匹对通道
        if self.G_ChromaKitAccessT3 > 0:
            self.G_PhrozenFluiddRespondInfo("self.G_ChromaKitAccessT3=%d" % self.G_ChromaKitAccessT3)
            self.Cmds_P1CnAutoChangeChannel(self.G_ChromaKitAccessT3, gcmd)
        else:
            self.G_PhrozenFluiddRespondInfo("chan=%d" % chan)
            self.Cmds_P1CnAutoChangeChannel(chan, gcmd)

        #lancaigang240524：用于UIUX动态界面
        self.G_PhrozenFluiddRespondInfo("+T3:1,%d" % self.G_ChangeChannelTimeoutNewChan)

    ####################################
    #函数名称：
    #输入参数：
    #返 回 值:
    #功能描述：蓝才刚-20230830
    ####################################
    def Cmds_CmdT4(self,gcmd):
        self.G_PhrozenFluiddRespondInfo("=====[(cmds.python)Cmds_CmdT4 +1]orca切片多色换料" )

        self.G_PhrozenFluiddRespondInfo("=====self.G_ChangeChannelTimeoutOldChan=%d" % self.G_ChangeChannelTimeoutOldChan)
        self.G_PhrozenFluiddRespondInfo("=====self.G_ChangeChannelTimeoutNewChan=%d" % self.G_ChangeChannelTimeoutNewChan)

        #lancaigang250515：单机打多色，不处理T?
        if self.G_P0M1MCNoneAMS == 1:
            self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_CmdT4]单机打多色，不处理T?")
            #lancaigang250828:
            self.G_PhrozenFluiddRespondInfo("外部宏命令-PRZ_PAUSE_WAITINGAREA")
            command_string = """
                PRZ_PAUSE_WAITINGAREA
                """
            self.G_PhrozenGCode.run_script_from_command(command_string)
            self.G_PhrozenFluiddRespondInfo("外部宏命令；command_string='%s'" % command_string)
            return
        #lancaigang250429：
        if self.G_AMSDeviceWorkMode==AMS_WORK_MODE_FILA_RUNOUT:
            self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_CmdT4]单色模式，不处理T4")
            #lancaigang250828:
            self.G_PhrozenFluiddRespondInfo("外部宏命令-PRZ_PAUSE_WAITINGAREA")
            command_string = """
                PRZ_PAUSE_WAITINGAREA
                """
            self.G_PhrozenGCode.run_script_from_command(command_string)
            self.G_PhrozenFluiddRespondInfo("外部宏命令；command_string='%s'" % command_string)
            return
        #lancaigang250514：
        if self.G_AMSDeviceWorkMode==AMS_WORK_MODE_MA :
            self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_CmdT4]单色续料模式，不处理T4")
            #lancaigang250828:
            self.G_PhrozenFluiddRespondInfo("外部宏命令-PRZ_PAUSE_WAITINGAREA")
            command_string = """
                PRZ_PAUSE_WAITINGAREA
                """
            self.G_PhrozenGCode.run_script_from_command(command_string)
            self.G_PhrozenFluiddRespondInfo("外部宏命令；command_string='%s'" % command_string)
            return

        #lancaigang240527：未知模式，因为要操作手动命令，默认让STM32进入MC多色模式
        if self.G_AMSDeviceWorkMode == AMS_WORK_MODE_UNKNOW:
            self.G_PhrozenFluiddRespondInfo("未知模式，因为要操作手动命令，默认让STM32进入MC多色模式")
            self.G_PhrozenFluiddRespondInfo("如果收到T?命令，但模式是未知模式，强制转换为MC多色模式")
            self.G_AMSDeviceWorkMode = AMS_WORK_MODE_MC
            #lancaigang241030:
            if self.G_SerialPort1OpenFlag == True:
                self.Cmds_AMSSerial1Send("MC")
                self.G_PhrozenFluiddRespondInfo("串口1发送命令：MC")
            #lancaigang241030:
            if self.G_SerialPort2OpenFlag == True:
                self.Cmds_AMSSerial2Send("MC")
                self.G_PhrozenFluiddRespondInfo("串口2发送命令：MC")

            self.G_ProzenToolhead.dwell(2)

        #lancaigang250912:导致return异常
        #self.Cmds_CmdOrcaPre()

        
        
        #self.G_PhrozenFluiddRespondInfo("命令='%s'；自动换料" % (gcmd.get_commandline(),))
        self.G_PhrozenFluiddRespondInfo("自动换料")
        #lancaigang240524：用于UIUX动态界面
        self.G_PhrozenFluiddRespondInfo("+T4:0,%d" % self.G_ChangeChannelTimeoutNewChan)
        # #cancel取消命令
        # self.G_PhrozenPrinterCancelPauseResume.cmd_CANCEL_PRINT(None)
        #lancaigang250517：
        Lo_PauseStatus=self.G_PhrozenPrinterCancelPauseResume.get_status(None)
        self.G_PhrozenFluiddRespondInfo("当前暂停状态-Lo_PauseStatus='%s'" % Lo_PauseStatus)
        self.G_PhrozenFluiddRespondInfo("Lo_PauseStatus['is_paused']='%s'" % Lo_PauseStatus['is_paused'])
        #// 当前暂停状态-Lo_PauseStatus='{'is_paused': True}'
        if Lo_PauseStatus['is_paused'] == True:
            self.G_PhrozenFluiddRespondInfo("已是暂停状态")
        else:
            self.G_PhrozenFluiddRespondInfo("未暂停状态")
        #lancaigang240113：清除手动命令标志
        self.ManualCmdFlag=False
        #lancaigang240221：stm32主动上报，开启可以暂停1次
        self.STM32ReprotPauseFlag=0
        self.G_PhrozenFluiddRespondInfo("self.STM32ReprotPauseFlag=0")

        #lancaigang241224：没有第二个AMS，不执行；
        #lancaigang241030:
        if self.G_SerialPort2OpenFlag == True:
            self.G_PhrozenFluiddRespondInfo("有第2个AMS，继续执行命令")
        else:
            self.G_PhrozenFluiddRespondInfo("没有第2个AMS，不执行命令")
            self.G_PhrozenFluiddRespondInfo("+T4:1,%d" % self.G_ChangeChannelTimeoutNewChan)
            return

        #lancaigang241030：一般是P1 C1到P1 C32，范围在1到32
        #第1台：1 2 3 4
        #第2台：5 6 7 8
        #第3台：9 10 11 12
        #第4台：13 14 15 16
        #第5台：17 18 19 20
        #第6台：21 22 23 24
        #第7台：25 26 27 28
        #第8台：29 30 31 32
        #自动换料
        chan=4+1
        self.G_PhrozenFluiddRespondInfo("chan=%d" % chan)
        #lancaigang250515:判断串口屏配置的颜色匹对通道
        if self.G_ChromaKitAccessT4 > 0:
            self.G_PhrozenFluiddRespondInfo("self.G_ChromaKitAccessT4=%d" % self.G_ChromaKitAccessT4)
            self.Cmds_P1CnAutoChangeChannel(self.G_ChromaKitAccessT4, gcmd)
        else:
            self.G_PhrozenFluiddRespondInfo("chan=%d" % chan)
            self.Cmds_P1CnAutoChangeChannel(chan, gcmd)

        #lancaigang240524：用于UIUX动态界面
        self.G_PhrozenFluiddRespondInfo("+T4:1,%d" % self.G_ChangeChannelTimeoutNewChan)

    ####################################
    #函数名称：
    #输入参数：
    #返 回 值:
    #功能描述：蓝才刚-20230830
    ####################################
    def Cmds_CmdT5(self,gcmd):
        self.G_PhrozenFluiddRespondInfo("=====[(cmds.python)Cmds_CmdT5 +1]orca切片多色换料" )

        self.G_PhrozenFluiddRespondInfo("=====self.G_ChangeChannelTimeoutOldChan=%d" % self.G_ChangeChannelTimeoutOldChan)
        self.G_PhrozenFluiddRespondInfo("=====self.G_ChangeChannelTimeoutNewChan=%d" % self.G_ChangeChannelTimeoutNewChan)

        #lancaigang250515：单机打多色，不处理T?
        if self.G_P0M1MCNoneAMS == 1:
            self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_CmdT5]单机打多色，不处理T?")
            #lancaigang250828:
            self.G_PhrozenFluiddRespondInfo("外部宏命令-PRZ_PAUSE_WAITINGAREA")
            command_string = """
                PRZ_PAUSE_WAITINGAREA
                """
            self.G_PhrozenGCode.run_script_from_command(command_string)
            self.G_PhrozenFluiddRespondInfo("外部宏命令；command_string='%s'" % command_string)
            return
        #lancaigang250429：
        if self.G_AMSDeviceWorkMode==AMS_WORK_MODE_FILA_RUNOUT:
            self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_CmdT5]单色模式，不处理T5")
            #lancaigang250828:
            self.G_PhrozenFluiddRespondInfo("外部宏命令-PRZ_PAUSE_WAITINGAREA")
            command_string = """
                PRZ_PAUSE_WAITINGAREA
                """
            self.G_PhrozenGCode.run_script_from_command(command_string)
            self.G_PhrozenFluiddRespondInfo("外部宏命令；command_string='%s'" % command_string)
            return
        #lancaigang250514：
        if self.G_AMSDeviceWorkMode==AMS_WORK_MODE_MA :
            self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_CmdT5]单色续料模式，不处理T5")
            #lancaigang250828:
            self.G_PhrozenFluiddRespondInfo("外部宏命令-PRZ_PAUSE_WAITINGAREA")
            command_string = """
                PRZ_PAUSE_WAITINGAREA
                """
            self.G_PhrozenGCode.run_script_from_command(command_string)
            self.G_PhrozenFluiddRespondInfo("外部宏命令；command_string='%s'" % command_string)
            return

        #lancaigang240527：未知模式，因为要操作手动命令，默认让STM32进入MC多色模式
        if self.G_AMSDeviceWorkMode == AMS_WORK_MODE_UNKNOW:
            self.G_PhrozenFluiddRespondInfo("未知模式，因为要操作手动命令，默认让STM32进入MC多色模式")
            self.G_PhrozenFluiddRespondInfo("如果收到T?命令，但模式是未知模式，强制转换为MC多色模式")
            self.G_AMSDeviceWorkMode = AMS_WORK_MODE_MC
            #lancaigang241030:
            if self.G_SerialPort1OpenFlag == True:
                self.Cmds_AMSSerial1Send("MC")
                self.G_PhrozenFluiddRespondInfo("串口1发送命令：MC")
            #lancaigang241030:
            if self.G_SerialPort2OpenFlag == True:
                self.Cmds_AMSSerial2Send("MC")
                self.G_PhrozenFluiddRespondInfo("串口2发送命令：MC")

            self.G_ProzenToolhead.dwell(2)

        #lancaigang250912:导致return异常
        #self.Cmds_CmdOrcaPre()

        

        
        #self.G_PhrozenFluiddRespondInfo("命令='%s'；自动换料" % (gcmd.get_commandline(),))
        self.G_PhrozenFluiddRespondInfo("自动换料")
        #lancaigang240524：用于UIUX动态界面
        self.G_PhrozenFluiddRespondInfo("+T5:0,%d" % self.G_ChangeChannelTimeoutNewChan)
        # #cancel取消命令
        # self.G_PhrozenPrinterCancelPauseResume.cmd_CANCEL_PRINT(None)
        #lancaigang250517：
        Lo_PauseStatus=self.G_PhrozenPrinterCancelPauseResume.get_status(None)
        self.G_PhrozenFluiddRespondInfo("当前暂停状态-Lo_PauseStatus='%s'" % Lo_PauseStatus)
        self.G_PhrozenFluiddRespondInfo("Lo_PauseStatus['is_paused']='%s'" % Lo_PauseStatus['is_paused'])
        #// 当前暂停状态-Lo_PauseStatus='{'is_paused': True}'
        if Lo_PauseStatus['is_paused'] == True:
            self.G_PhrozenFluiddRespondInfo("已是暂停状态")
        else:
            self.G_PhrozenFluiddRespondInfo("未暂停状态")
        #lancaigang240113：清除手动命令标志
        self.ManualCmdFlag=False
        #lancaigang240221：stm32主动上报，开启可以暂停1次
        self.STM32ReprotPauseFlag=0
        self.G_PhrozenFluiddRespondInfo("self.STM32ReprotPauseFlag=0")

        #lancaigang241224：没有第二个AMS，不执行；
        #lancaigang241030:
        if self.G_SerialPort2OpenFlag == True:
            self.G_PhrozenFluiddRespondInfo("有第2个AMS，继续执行命令")
        else:
            self.G_PhrozenFluiddRespondInfo("没有第2个AMS，不执行命令")
            self.G_PhrozenFluiddRespondInfo("+T5:1,%d" % self.G_ChangeChannelTimeoutNewChan)
            return


        #lancaigang241030：一般是P1 C1到P1 C32，范围在1到32
        #第1台：1 2 3 4
        #第2台：5 6 7 8
        #第3台：9 10 11 12
        #第4台：13 14 15 16
        #第5台：17 18 19 20
        #第6台：21 22 23 24
        #第7台：25 26 27 28
        #第8台：29 30 31 32
        #自动换料
        chan=5+1
        self.G_PhrozenFluiddRespondInfo("chan=%d" % chan)
        #lancaigang250515:判断串口屏配置的颜色匹对通道
        if self.G_ChromaKitAccessT5 > 0:
            self.G_PhrozenFluiddRespondInfo("self.G_ChromaKitAccessT5=%d" % self.G_ChromaKitAccessT5)
            self.Cmds_P1CnAutoChangeChannel(self.G_ChromaKitAccessT5, gcmd)
        else:
            self.G_PhrozenFluiddRespondInfo("chan=%d" % chan)
            self.Cmds_P1CnAutoChangeChannel(chan, gcmd)

        #lancaigang240524：用于UIUX动态界面
        self.G_PhrozenFluiddRespondInfo("+T5:1,%d" % self.G_ChangeChannelTimeoutNewChan)

    ####################################
    #函数名称：
    #输入参数：
    #返 回 值:
    #功能描述：蓝才刚-20230830
    ####################################
    def Cmds_CmdT6(self,gcmd):
        self.G_PhrozenFluiddRespondInfo("=====[(cmds.python)Cmds_CmdT6 +1]orca切片多色换料" )

        self.G_PhrozenFluiddRespondInfo("=====self.G_ChangeChannelTimeoutOldChan=%d" % self.G_ChangeChannelTimeoutOldChan)
        self.G_PhrozenFluiddRespondInfo("=====self.G_ChangeChannelTimeoutNewChan=%d" % self.G_ChangeChannelTimeoutNewChan)

        #lancaigang250515：单机打多色，不处理T?
        if self.G_P0M1MCNoneAMS == 1:
            self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_CmdT6]单机打多色，不处理T?")
            #lancaigang250828:
            self.G_PhrozenFluiddRespondInfo("外部宏命令-PRZ_PAUSE_WAITINGAREA")
            command_string = """
                PRZ_PAUSE_WAITINGAREA
                """
            self.G_PhrozenGCode.run_script_from_command(command_string)
            self.G_PhrozenFluiddRespondInfo("外部宏命令；command_string='%s'" % command_string)
            return
        #lancaigang250429：
        if self.G_AMSDeviceWorkMode==AMS_WORK_MODE_FILA_RUNOUT:
            self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_CmdT6]单色模式，不处理T6")
            #lancaigang250828:
            self.G_PhrozenFluiddRespondInfo("外部宏命令-PRZ_PAUSE_WAITINGAREA")
            command_string = """
                PRZ_PAUSE_WAITINGAREA
                """
            self.G_PhrozenGCode.run_script_from_command(command_string)
            self.G_PhrozenFluiddRespondInfo("外部宏命令；command_string='%s'" % command_string)
            return
        #lancaigang250514：
        if self.G_AMSDeviceWorkMode==AMS_WORK_MODE_MA :
            self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_CmdT6]单色续料模式，不处理T6")
            #lancaigang250828:
            self.G_PhrozenFluiddRespondInfo("外部宏命令-PRZ_PAUSE_WAITINGAREA")
            command_string = """
                PRZ_PAUSE_WAITINGAREA
                """
            self.G_PhrozenGCode.run_script_from_command(command_string)
            self.G_PhrozenFluiddRespondInfo("外部宏命令；command_string='%s'" % command_string)
            return

        #lancaigang240527：未知模式，因为要操作手动命令，默认让STM32进入MC多色模式
        if self.G_AMSDeviceWorkMode == AMS_WORK_MODE_UNKNOW:
            self.G_PhrozenFluiddRespondInfo("未知模式，因为要操作手动命令，默认让STM32进入MC多色模式")
            self.G_PhrozenFluiddRespondInfo("如果收到T?命令，但模式是未知模式，强制转换为MC多色模式")
            self.G_AMSDeviceWorkMode = AMS_WORK_MODE_MC
            #lancaigang241030:
            if self.G_SerialPort1OpenFlag == True:
                self.Cmds_AMSSerial1Send("MC")
                self.G_PhrozenFluiddRespondInfo("串口1发送命令：MC")
            #lancaigang241030:
            if self.G_SerialPort2OpenFlag == True:
                self.Cmds_AMSSerial2Send("MC")
                self.G_PhrozenFluiddRespondInfo("串口2发送命令：MC")

            self.G_ProzenToolhead.dwell(2)

        #lancaigang250912:导致return异常
        #self.Cmds_CmdOrcaPre()

        

        
        #self.G_PhrozenFluiddRespondInfo("命令='%s'；自动换料" % (gcmd.get_commandline(),))
        self.G_PhrozenFluiddRespondInfo("自动换料")
        #lancaigang240524：用于UIUX动态界面
        self.G_PhrozenFluiddRespondInfo("+T6:0,%d" % self.G_ChangeChannelTimeoutNewChan)
        # #cancel取消命令
        # self.G_PhrozenPrinterCancelPauseResume.cmd_CANCEL_PRINT(None)
        #lancaigang250517：
        Lo_PauseStatus=self.G_PhrozenPrinterCancelPauseResume.get_status(None)
        self.G_PhrozenFluiddRespondInfo("当前暂停状态-Lo_PauseStatus='%s'" % Lo_PauseStatus)
        self.G_PhrozenFluiddRespondInfo("Lo_PauseStatus['is_paused']='%s'" % Lo_PauseStatus['is_paused'])
        #// 当前暂停状态-Lo_PauseStatus='{'is_paused': True}'
        if Lo_PauseStatus['is_paused'] == True:
            self.G_PhrozenFluiddRespondInfo("已是暂停状态")
        else:
            self.G_PhrozenFluiddRespondInfo("未暂停状态")
        #lancaigang240113：清除手动命令标志
        self.ManualCmdFlag=False
        #lancaigang240221：stm32主动上报，开启可以暂停1次
        self.STM32ReprotPauseFlag=0
        self.G_PhrozenFluiddRespondInfo("self.STM32ReprotPauseFlag=0")


        #lancaigang241224：没有第二个AMS，不执行；
        #lancaigang241030:
        if self.G_SerialPort2OpenFlag == True:
            self.G_PhrozenFluiddRespondInfo("有第2个AMS，继续执行命令")
        else:
            self.G_PhrozenFluiddRespondInfo("没有第2个AMS，不执行命令")
            self.G_PhrozenFluiddRespondInfo("+T6:1,%d" % self.G_ChangeChannelTimeoutNewChan)
            return



        #lancaigang241030：一般是P1 C1到P1 C32，范围在1到32
        #第1台：1 2 3 4
        #第2台：5 6 7 8
        #第3台：9 10 11 12
        #第4台：13 14 15 16
        #第5台：17 18 19 20
        #第6台：21 22 23 24
        #第7台：25 26 27 28
        #第8台：29 30 31 32
        #自动换料
        chan=6+1
        self.G_PhrozenFluiddRespondInfo("chan=%d" % chan)
        #lancaigang250515:判断串口屏配置的颜色匹对通道
        if self.G_ChromaKitAccessT6 > 0:
            self.G_PhrozenFluiddRespondInfo("self.G_ChromaKitAccessT6=%d" % self.G_ChromaKitAccessT6)
            self.Cmds_P1CnAutoChangeChannel(self.G_ChromaKitAccessT6, gcmd)
        else:
            self.G_PhrozenFluiddRespondInfo("chan=%d" % chan)
            self.Cmds_P1CnAutoChangeChannel(chan, gcmd)

        #lancaigang240524：用于UIUX动态界面
        self.G_PhrozenFluiddRespondInfo("+T6:1,%d" % self.G_ChangeChannelTimeoutNewChan)

    ####################################
    #函数名称：
    #输入参数：
    #返 回 值:
    #功能描述：蓝才刚-20230830
    ####################################
    def Cmds_CmdT7(self,gcmd):
        self.G_PhrozenFluiddRespondInfo("=====[(cmds.python)Cmds_CmdT7 +1]orca切片多色换料" )

        self.G_PhrozenFluiddRespondInfo("=====self.G_ChangeChannelTimeoutOldChan=%d" % self.G_ChangeChannelTimeoutOldChan)
        self.G_PhrozenFluiddRespondInfo("=====self.G_ChangeChannelTimeoutNewChan=%d" % self.G_ChangeChannelTimeoutNewChan)

        #lancaigang250515：单机打多色，不处理T?
        if self.G_P0M1MCNoneAMS == 1:
            self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_CmdT7]单机打多色，不处理T?")
            #lancaigang250828:
            self.G_PhrozenFluiddRespondInfo("外部宏命令-PRZ_PAUSE_WAITINGAREA")
            command_string = """
                PRZ_PAUSE_WAITINGAREA
                """
            self.G_PhrozenGCode.run_script_from_command(command_string)
            self.G_PhrozenFluiddRespondInfo("外部宏命令；command_string='%s'" % command_string)
            return
        #lancaigang250429：
        if self.G_AMSDeviceWorkMode==AMS_WORK_MODE_FILA_RUNOUT:
            self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_CmdT7]单色模式，不处理T7")
            #lancaigang250828:
            self.G_PhrozenFluiddRespondInfo("外部宏命令-PRZ_PAUSE_WAITINGAREA")
            command_string = """
                PRZ_PAUSE_WAITINGAREA
                """
            self.G_PhrozenGCode.run_script_from_command(command_string)
            self.G_PhrozenFluiddRespondInfo("外部宏命令；command_string='%s'" % command_string)
            return
        #lancaigang250514：
        if self.G_AMSDeviceWorkMode==AMS_WORK_MODE_MA :
            self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_CmdT7]单色续料模式，不处理T7")
            #lancaigang250828:
            self.G_PhrozenFluiddRespondInfo("外部宏命令-PRZ_PAUSE_WAITINGAREA")
            command_string = """
                PRZ_PAUSE_WAITINGAREA
                """
            self.G_PhrozenGCode.run_script_from_command(command_string)
            self.G_PhrozenFluiddRespondInfo("外部宏命令；command_string='%s'" % command_string)
            return

        #lancaigang240527：未知模式，因为要操作手动命令，默认让STM32进入MC多色模式
        if self.G_AMSDeviceWorkMode == AMS_WORK_MODE_UNKNOW:
            self.G_PhrozenFluiddRespondInfo("未知模式，因为要操作手动命令，默认让STM32进入MC多色模式")
            self.G_PhrozenFluiddRespondInfo("如果收到T?命令，但模式是未知模式，强制转换为MC多色模式")
            self.G_AMSDeviceWorkMode = AMS_WORK_MODE_MC
            #lancaigang241030:
            if self.G_SerialPort1OpenFlag == True:
                self.Cmds_AMSSerial1Send("MC")
                self.G_PhrozenFluiddRespondInfo("串口1发送命令：MC")
            #lancaigang241030:
            if self.G_SerialPort2OpenFlag == True:
                self.Cmds_AMSSerial2Send("MC")
                self.G_PhrozenFluiddRespondInfo("串口2发送命令：MC")

            self.G_ProzenToolhead.dwell(2)

        #lancaigang250912:导致return异常
        #self.Cmds_CmdOrcaPre()

        

        
        #self.G_PhrozenFluiddRespondInfo("命令='%s'；自动换料" % (gcmd.get_commandline(),))
        self.G_PhrozenFluiddRespondInfo("自动换料")
        #lancaigang240524：用于UIUX动态界面
        self.G_PhrozenFluiddRespondInfo("+T7:0,%d" % self.G_ChangeChannelTimeoutNewChan)
        # #cancel取消命令
        # self.G_PhrozenPrinterCancelPauseResume.cmd_CANCEL_PRINT(None)
        #lancaigang250517：
        Lo_PauseStatus=self.G_PhrozenPrinterCancelPauseResume.get_status(None)
        self.G_PhrozenFluiddRespondInfo("当前暂停状态-Lo_PauseStatus='%s'" % Lo_PauseStatus)
        self.G_PhrozenFluiddRespondInfo("Lo_PauseStatus['is_paused']='%s'" % Lo_PauseStatus['is_paused'])
        #// 当前暂停状态-Lo_PauseStatus='{'is_paused': True}'
        if Lo_PauseStatus['is_paused'] == True:
            self.G_PhrozenFluiddRespondInfo("已是暂停状态")
        else:
            self.G_PhrozenFluiddRespondInfo("未暂停状态")
        #lancaigang240113：清除手动命令标志
        self.ManualCmdFlag=False
        #lancaigang240221：stm32主动上报，开启可以暂停1次
        self.STM32ReprotPauseFlag=0
        self.G_PhrozenFluiddRespondInfo("self.STM32ReprotPauseFlag=0")


        #lancaigang241224：没有第二个AMS，不执行；
        #lancaigang241030:
        if self.G_SerialPort2OpenFlag == True:
            self.G_PhrozenFluiddRespondInfo("有第2个AMS，继续执行命令")
        else:
            self.G_PhrozenFluiddRespondInfo("没有第2个AMS，不执行命令")
            self.G_PhrozenFluiddRespondInfo("+T7:1,%d" % self.G_ChangeChannelTimeoutNewChan)
            return

        #lancaigang241030：一般是P1 C1到P1 C32，范围在1到32
        #第1台：1 2 3 4
        #第2台：5 6 7 8
        #第3台：9 10 11 12
        #第4台：13 14 15 16
        #第5台：17 18 19 20
        #第6台：21 22 23 24
        #第7台：25 26 27 28
        #第8台：29 30 31 32
        #自动换料
        chan=7+1
        self.G_PhrozenFluiddRespondInfo("chan=%d" % chan)
        #lancaigang250515:判断串口屏配置的颜色匹对通道
        if self.G_ChromaKitAccessT7 > 0:
            self.G_PhrozenFluiddRespondInfo("self.G_ChromaKitAccessT7=%d" % self.G_ChromaKitAccessT7)
            self.Cmds_P1CnAutoChangeChannel(self.G_ChromaKitAccessT7, gcmd)
        else:
            self.G_PhrozenFluiddRespondInfo("chan=%d" % chan)
            self.Cmds_P1CnAutoChangeChannel(chan, gcmd)

        #lancaigang240524：用于UIUX动态界面
        self.G_PhrozenFluiddRespondInfo("+T7:1,%d" % self.G_ChangeChannelTimeoutNewChan)

    ####################################
    #函数名称：
    #输入参数：
    #返 回 值:
    #功能描述：蓝才刚-20230830
    ####################################
    def Cmds_CmdT8(self,gcmd):
        self.G_PhrozenFluiddRespondInfo("=====[(cmds.python)Cmds_CmdT8 +1]orca切片多色换料" )

        self.G_PhrozenFluiddRespondInfo("=====self.G_ChangeChannelTimeoutOldChan=%d" % self.G_ChangeChannelTimeoutOldChan)
        self.G_PhrozenFluiddRespondInfo("=====self.G_ChangeChannelTimeoutNewChan=%d" % self.G_ChangeChannelTimeoutNewChan)

        #lancaigang250515：单机打多色，不处理T?
        if self.G_P0M1MCNoneAMS == 1:
            self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_CmdT8]单机打多色，不处理T?")
            #lancaigang250828:
            self.G_PhrozenFluiddRespondInfo("外部宏命令-PRZ_PAUSE_WAITINGAREA")
            command_string = """
                PRZ_PAUSE_WAITINGAREA
                """
            self.G_PhrozenGCode.run_script_from_command(command_string)
            self.G_PhrozenFluiddRespondInfo("外部宏命令；command_string='%s'" % command_string)
            return
        #lancaigang250429：
        if self.G_AMSDeviceWorkMode==AMS_WORK_MODE_FILA_RUNOUT:
            self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_CmdT8]单色模式，不处理T8")
            #lancaigang250828:
            self.G_PhrozenFluiddRespondInfo("外部宏命令-PRZ_PAUSE_WAITINGAREA")
            command_string = """
                PRZ_PAUSE_WAITINGAREA
                """
            self.G_PhrozenGCode.run_script_from_command(command_string)
            self.G_PhrozenFluiddRespondInfo("外部宏命令；command_string='%s'" % command_string)
            return
        #lancaigang250514：
        if self.G_AMSDeviceWorkMode==AMS_WORK_MODE_MA :
            self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_CmdT8]单色续料模式，不处理T8")
            #lancaigang250828:
            self.G_PhrozenFluiddRespondInfo("外部宏命令-PRZ_PAUSE_WAITINGAREA")
            command_string = """
                PRZ_PAUSE_WAITINGAREA
                """
            self.G_PhrozenGCode.run_script_from_command(command_string)
            self.G_PhrozenFluiddRespondInfo("外部宏命令；command_string='%s'" % command_string)
            return
        
        #lancaigang240527：未知模式，因为要操作手动命令，默认让STM32进入MC多色模式
        if self.G_AMSDeviceWorkMode == AMS_WORK_MODE_UNKNOW:
            self.G_PhrozenFluiddRespondInfo("未知模式，因为要操作手动命令，默认让STM32进入MC多色模式")
            self.G_PhrozenFluiddRespondInfo("如果收到T?命令，但模式是未知模式，强制转换为MC多色模式")
            self.G_AMSDeviceWorkMode = AMS_WORK_MODE_MC
            #lancaigang241030:
            if self.G_SerialPort1OpenFlag == True:
                self.Cmds_AMSSerial1Send("MC")
                self.G_PhrozenFluiddRespondInfo("串口1发送命令：MC")
            #lancaigang241030:
            if self.G_SerialPort2OpenFlag == True:
                self.Cmds_AMSSerial2Send("MC")
                self.G_PhrozenFluiddRespondInfo("串口2发送命令：MC")

            self.G_ProzenToolhead.dwell(2)

        #lancaigang250912:导致return异常
        #self.Cmds_CmdOrcaPre()

        

        
        #self.G_PhrozenFluiddRespondInfo("命令='%s'；自动换料" % (gcmd.get_commandline(),))
        self.G_PhrozenFluiddRespondInfo("自动换料")
        #lancaigang240524：用于UIUX动态界面
        self.G_PhrozenFluiddRespondInfo("+T8:0,%d" % self.G_ChangeChannelTimeoutNewChan)
        # #cancel取消命令
        # self.G_PhrozenPrinterCancelPauseResume.cmd_CANCEL_PRINT(None)
        #lancaigang250517：
        Lo_PauseStatus=self.G_PhrozenPrinterCancelPauseResume.get_status(None)
        self.G_PhrozenFluiddRespondInfo("当前暂停状态-Lo_PauseStatus='%s'" % Lo_PauseStatus)
        self.G_PhrozenFluiddRespondInfo("Lo_PauseStatus['is_paused']='%s'" % Lo_PauseStatus['is_paused'])
        #// 当前暂停状态-Lo_PauseStatus='{'is_paused': True}'
        if Lo_PauseStatus['is_paused'] == True:
            self.G_PhrozenFluiddRespondInfo("已是暂停状态")
        else:
            self.G_PhrozenFluiddRespondInfo("未暂停状态")
        #lancaigang240113：清除手动命令标志
        self.ManualCmdFlag=False
        #lancaigang240221：stm32主动上报，开启可以暂停1次
        self.STM32ReprotPauseFlag=0
        self.G_PhrozenFluiddRespondInfo("self.STM32ReprotPauseFlag=0")


        #lancaigang241224：没有第3个AMS，不执行；
        #lancaigang241030:
        if self.G_SerialPort2OpenFlag == True:
            self.G_PhrozenFluiddRespondInfo("有第3个AMS，继续执行命令")
        else:
            self.G_PhrozenFluiddRespondInfo("没有第3个AMS，不执行命令")
            self.G_PhrozenFluiddRespondInfo("+T8:1,%d" % self.G_ChangeChannelTimeoutNewChan)
            return

        #lancaigang241030：一般是P1 C1到P1 C32，范围在1到32
        #第1台：1 2 3 4
        #第2台：5 6 7 8
        #第3台：9 10 11 12
        #第4台：13 14 15 16
        #第5台：17 18 19 20
        #第6台：21 22 23 24
        #第7台：25 26 27 28
        #第8台：29 30 31 32
        #自动换料
        chan=8+1
        self.G_PhrozenFluiddRespondInfo("chan=%d" % chan)
        #lancaigang250515:判断串口屏配置的颜色匹对通道
        if self.G_ChromaKitAccessT8 > 0:
            self.G_PhrozenFluiddRespondInfo("self.G_ChromaKitAccessT8=%d" % self.G_ChromaKitAccessT8)
            self.Cmds_P1CnAutoChangeChannel(self.G_ChromaKitAccessT8, gcmd)
        else:
            self.G_PhrozenFluiddRespondInfo("chan=%d" % chan)
            self.Cmds_P1CnAutoChangeChannel(chan, gcmd)

        #lancaigang240524：用于UIUX动态界面
        self.G_PhrozenFluiddRespondInfo("+T8:1,%d" % self.G_ChangeChannelTimeoutNewChan)

    ####################################
    #函数名称：
    #输入参数：
    #返 回 值:
    #功能描述：蓝才刚-20230830
    ####################################
    def Cmds_CmdT9(self,gcmd):
        self.G_PhrozenFluiddRespondInfo("=====[(cmds.python)Cmds_CmdT9 +1]orca切片多色换料" )

        self.G_PhrozenFluiddRespondInfo("=====self.G_ChangeChannelTimeoutOldChan=%d" % self.G_ChangeChannelTimeoutOldChan)
        self.G_PhrozenFluiddRespondInfo("=====self.G_ChangeChannelTimeoutNewChan=%d" % self.G_ChangeChannelTimeoutNewChan)

        #lancaigang250515：单机打多色，不处理T?
        if self.G_P0M1MCNoneAMS == 1:
            self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_CmdT9]单机打多色，不处理T?")
            #lancaigang250828:
            self.G_PhrozenFluiddRespondInfo("外部宏命令-PRZ_PAUSE_WAITINGAREA")
            command_string = """
                PRZ_PAUSE_WAITINGAREA
                """
            self.G_PhrozenGCode.run_script_from_command(command_string)
            self.G_PhrozenFluiddRespondInfo("外部宏命令；command_string='%s'" % command_string)
            return
        #lancaigang250429：
        if self.G_AMSDeviceWorkMode==AMS_WORK_MODE_FILA_RUNOUT:
            self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_CmdT9]单色模式，不处理T9")
            #lancaigang250828:
            self.G_PhrozenFluiddRespondInfo("外部宏命令-PRZ_PAUSE_WAITINGAREA")
            command_string = """
                PRZ_PAUSE_WAITINGAREA
                """
            self.G_PhrozenGCode.run_script_from_command(command_string)
            self.G_PhrozenFluiddRespondInfo("外部宏命令；command_string='%s'" % command_string)
            return
        #lancaigang250514：
        if self.G_AMSDeviceWorkMode==AMS_WORK_MODE_MA :
            self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_CmdT9]单色续料模式，不处理T9")
            #lancaigang250828:
            self.G_PhrozenFluiddRespondInfo("外部宏命令-PRZ_PAUSE_WAITINGAREA")
            command_string = """
                PRZ_PAUSE_WAITINGAREA
                """
            self.G_PhrozenGCode.run_script_from_command(command_string)
            self.G_PhrozenFluiddRespondInfo("外部宏命令；command_string='%s'" % command_string)
            return
        
        #lancaigang240527：未知模式，因为要操作手动命令，默认让STM32进入MC多色模式
        if self.G_AMSDeviceWorkMode == AMS_WORK_MODE_UNKNOW:
            self.G_PhrozenFluiddRespondInfo("未知模式，因为要操作手动命令，默认让STM32进入MC多色模式")
            self.G_PhrozenFluiddRespondInfo("如果收到T?命令，但模式是未知模式，强制转换为MC多色模式")
            self.G_AMSDeviceWorkMode = AMS_WORK_MODE_MC
            #lancaigang241030:
            if self.G_SerialPort1OpenFlag == True:
                self.Cmds_AMSSerial1Send("MC")
                self.G_PhrozenFluiddRespondInfo("串口1发送命令：MC")
            #lancaigang241030:
            if self.G_SerialPort2OpenFlag == True:
                self.Cmds_AMSSerial2Send("MC")
                self.G_PhrozenFluiddRespondInfo("串口2发送命令：MC")

            self.G_ProzenToolhead.dwell(2)


        # #lancaigang250912:
        # self.Cmds_CmdOrcaPre()

        



        
        #self.G_PhrozenFluiddRespondInfo("命令='%s'；自动换料" % (gcmd.get_commandline(),))
        self.G_PhrozenFluiddRespondInfo("自动换料")
        #lancaigang240524：用于UIUX动态界面
        self.G_PhrozenFluiddRespondInfo("+T9:0,%d" % self.G_ChangeChannelTimeoutNewChan)
        # #cancel取消命令
        # self.G_PhrozenPrinterCancelPauseResume.cmd_CANCEL_PRINT(None)
        #lancaigang250517：
        Lo_PauseStatus=self.G_PhrozenPrinterCancelPauseResume.get_status(None)
        self.G_PhrozenFluiddRespondInfo("当前暂停状态-Lo_PauseStatus='%s'" % Lo_PauseStatus)
        self.G_PhrozenFluiddRespondInfo("Lo_PauseStatus['is_paused']='%s'" % Lo_PauseStatus['is_paused'])
        #// 当前暂停状态-Lo_PauseStatus='{'is_paused': True}'
        if Lo_PauseStatus['is_paused'] == True:
            self.G_PhrozenFluiddRespondInfo("已是暂停状态")
        else:
            self.G_PhrozenFluiddRespondInfo("未暂停状态")
        #lancaigang240113：清除手动命令标志
        self.ManualCmdFlag=False
        #lancaigang240221：stm32主动上报，开启可以暂停1次
        self.STM32ReprotPauseFlag=0
        self.G_PhrozenFluiddRespondInfo("self.STM32ReprotPauseFlag=0")


        #lancaigang241224：没有第3个AMS，不执行；
        #lancaigang241030:
        if self.G_SerialPort2OpenFlag == True:
            self.G_PhrozenFluiddRespondInfo("有第3个AMS，继续执行命令")
        else:
            self.G_PhrozenFluiddRespondInfo("没有第3个AMS，不执行命令")
            self.G_PhrozenFluiddRespondInfo("+T9:1,%d" % self.G_ChangeChannelTimeoutNewChan)
            return


        #lancaigang241030：一般是P1 C1到P1 C32，范围在1到32
        #第1台：1 2 3 4
        #第2台：5 6 7 8
        #第3台：9 10 11 12
        #第4台：13 14 15 16
        #第5台：17 18 19 20
        #第6台：21 22 23 24
        #第7台：25 26 27 28
        #第8台：29 30 31 32
        #自动换料
        chan=9+1
        self.G_PhrozenFluiddRespondInfo("chan=%d" % chan)
        #lancaigang250515:判断串口屏配置的颜色匹对通道
        if self.G_ChromaKitAccessT9 > 0:
            self.G_PhrozenFluiddRespondInfo("self.G_ChromaKitAccessT9=%d" % self.G_ChromaKitAccessT9)
            self.Cmds_P1CnAutoChangeChannel(self.G_ChromaKitAccessT9, gcmd)
        else:
            self.G_PhrozenFluiddRespondInfo("chan=%d" % chan)
            self.Cmds_P1CnAutoChangeChannel(chan, gcmd)

        #lancaigang240524：用于UIUX动态界面
        self.G_PhrozenFluiddRespondInfo("+T9:1,%d" % self.G_ChangeChannelTimeoutNewChan)

    ####################################
    #函数名称：
    #输入参数：
    #返 回 值:
    #功能描述：蓝才刚-20230830
    ####################################
    def Cmds_CmdT10(self,gcmd):
        self.G_PhrozenFluiddRespondInfo("=====[(cmds.python)Cmds_CmdT10 +1]orca切片多色换料" )

        self.G_PhrozenFluiddRespondInfo("=====self.G_ChangeChannelTimeoutOldChan=%d" % self.G_ChangeChannelTimeoutOldChan)
        self.G_PhrozenFluiddRespondInfo("=====self.G_ChangeChannelTimeoutNewChan=%d" % self.G_ChangeChannelTimeoutNewChan)

        #lancaigang250515：单机打多色，不处理T?
        if self.G_P0M1MCNoneAMS == 1:
            self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_CmdT10]单机打多色，不处理T?")
            #lancaigang250828:
            self.G_PhrozenFluiddRespondInfo("外部宏命令-PRZ_PAUSE_WAITINGAREA")
            command_string = """
                PRZ_PAUSE_WAITINGAREA
                """
            self.G_PhrozenGCode.run_script_from_command(command_string)
            self.G_PhrozenFluiddRespondInfo("外部宏命令；command_string='%s'" % command_string)
            return
        #lancaigang250429：
        if self.G_AMSDeviceWorkMode==AMS_WORK_MODE_FILA_RUNOUT:
            self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_CmdT10]单色模式，不处理T10")
            #lancaigang250828:
            self.G_PhrozenFluiddRespondInfo("外部宏命令-PRZ_PAUSE_WAITINGAREA")
            command_string = """
                PRZ_PAUSE_WAITINGAREA
                """
            self.G_PhrozenGCode.run_script_from_command(command_string)
            self.G_PhrozenFluiddRespondInfo("外部宏命令；command_string='%s'" % command_string)
            return
        #lancaigang250514：
        if self.G_AMSDeviceWorkMode==AMS_WORK_MODE_MA :
            self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_CmdT10]单色续料模式，不处理T10")
            #lancaigang250828:
            self.G_PhrozenFluiddRespondInfo("外部宏命令-PRZ_PAUSE_WAITINGAREA")
            command_string = """
                PRZ_PAUSE_WAITINGAREA
                """
            self.G_PhrozenGCode.run_script_from_command(command_string)
            self.G_PhrozenFluiddRespondInfo("外部宏命令；command_string='%s'" % command_string)
            return
        
        #lancaigang240527：未知模式，因为要操作手动命令，默认让STM32进入MC多色模式
        if self.G_AMSDeviceWorkMode == AMS_WORK_MODE_UNKNOW:
            self.G_PhrozenFluiddRespondInfo("未知模式，因为要操作手动命令，默认让STM32进入MC多色模式")
            self.G_PhrozenFluiddRespondInfo("如果收到T?命令，但模式是未知模式，强制转换为MC多色模式")
            self.G_AMSDeviceWorkMode = AMS_WORK_MODE_MC
            #lancaigang241030:
            if self.G_SerialPort1OpenFlag == True:
                self.Cmds_AMSSerial1Send("MC")
                self.G_PhrozenFluiddRespondInfo("串口1发送命令：MC")
            #lancaigang241030:
            if self.G_SerialPort2OpenFlag == True:
                self.Cmds_AMSSerial2Send("MC")
                self.G_PhrozenFluiddRespondInfo("串口2发送命令：MC")

            self.G_ProzenToolhead.dwell(2)

        #lancaigang250912:导致return异常
        #self.Cmds_CmdOrcaPre()

        

        
        #self.G_PhrozenFluiddRespondInfo("命令='%s'；自动换料" % (gcmd.get_commandline(),))
        self.G_PhrozenFluiddRespondInfo("自动换料")
        #lancaigang240524：用于UIUX动态界面
        self.G_PhrozenFluiddRespondInfo("+T10:0,%d" % self.G_ChangeChannelTimeoutNewChan)
        # #cancel取消命令
        # self.G_PhrozenPrinterCancelPauseResume.cmd_CANCEL_PRINT(None)
        #lancaigang250517：
        Lo_PauseStatus=self.G_PhrozenPrinterCancelPauseResume.get_status(None)
        self.G_PhrozenFluiddRespondInfo("当前暂停状态-Lo_PauseStatus='%s'" % Lo_PauseStatus)
        self.G_PhrozenFluiddRespondInfo("Lo_PauseStatus['is_paused']='%s'" % Lo_PauseStatus['is_paused'])
        #// 当前暂停状态-Lo_PauseStatus='{'is_paused': True}'
        if Lo_PauseStatus['is_paused'] == True:
            self.G_PhrozenFluiddRespondInfo("已是暂停状态")
        else:
            self.G_PhrozenFluiddRespondInfo("未暂停状态")
        #lancaigang240113：清除手动命令标志
        self.ManualCmdFlag=False
        #lancaigang240221：stm32主动上报，开启可以暂停1次
        self.STM32ReprotPauseFlag=0
        self.G_PhrozenFluiddRespondInfo("self.STM32ReprotPauseFlag=0")

        #lancaigang241224：没有第3个AMS，不执行；
        #lancaigang241030:
        if self.G_SerialPort2OpenFlag == True:
            self.G_PhrozenFluiddRespondInfo("有第3个AMS，继续执行命令")
        else:
            self.G_PhrozenFluiddRespondInfo("没有第3个AMS，不执行命令")
            self.G_PhrozenFluiddRespondInfo("+T10:1,%d" % self.G_ChangeChannelTimeoutNewChan)
            return

        #lancaigang241030：一般是P1 C1到P1 C32，范围在1到32
        #第1台：1 2 3 4
        #第2台：5 6 7 8
        #第3台：9 10 11 12
        #第4台：13 14 15 16
        #第5台：17 18 19 20
        #第6台：21 22 23 24
        #第7台：25 26 27 28
        #第8台：29 30 31 32
        #自动换料
        chan=10+1
        self.G_PhrozenFluiddRespondInfo("chan=%d" % chan)
        #lancaigang250515:判断串口屏配置的颜色匹对通道
        if self.G_ChromaKitAccessT10 > 0:
            self.G_PhrozenFluiddRespondInfo("self.G_ChromaKitAccessT10=%d" % self.G_ChromaKitAccessT10)
            self.Cmds_P1CnAutoChangeChannel(self.G_ChromaKitAccessT10, gcmd)
        else:
            self.G_PhrozenFluiddRespondInfo("chan=%d" % chan)
            self.Cmds_P1CnAutoChangeChannel(chan, gcmd)

        #lancaigang240524：用于UIUX动态界面
        self.G_PhrozenFluiddRespondInfo("+T10:1,%d" % self.G_ChangeChannelTimeoutNewChan)

    ####################################
    #函数名称：
    #输入参数：
    #返 回 值:
    #功能描述：蓝才刚-20230830
    ####################################
    def Cmds_CmdT11(self,gcmd):
        self.G_PhrozenFluiddRespondInfo("=====[(cmds.python)Cmds_CmdT11 +1]orca切片多色换料" )

        self.G_PhrozenFluiddRespondInfo("=====self.G_ChangeChannelTimeoutOldChan=%d" % self.G_ChangeChannelTimeoutOldChan)
        self.G_PhrozenFluiddRespondInfo("=====self.G_ChangeChannelTimeoutNewChan=%d" % self.G_ChangeChannelTimeoutNewChan)

        #lancaigang250515：单机打多色，不处理T?
        if self.G_P0M1MCNoneAMS == 1:
            self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_CmdT11]单机打多色，不处理T?")
            #lancaigang250828:
            self.G_PhrozenFluiddRespondInfo("外部宏命令-PRZ_PAUSE_WAITINGAREA")
            command_string = """
                PRZ_PAUSE_WAITINGAREA
                """
            self.G_PhrozenGCode.run_script_from_command(command_string)
            self.G_PhrozenFluiddRespondInfo("外部宏命令；command_string='%s'" % command_string)
            return
        #lancaigang250429：
        if self.G_AMSDeviceWorkMode==AMS_WORK_MODE_FILA_RUNOUT:
            self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_CmdT11]单色模式，不处理T11")
            #lancaigang250828:
            self.G_PhrozenFluiddRespondInfo("外部宏命令-PRZ_PAUSE_WAITINGAREA")
            command_string = """
                PRZ_PAUSE_WAITINGAREA
                """
            self.G_PhrozenGCode.run_script_from_command(command_string)
            self.G_PhrozenFluiddRespondInfo("外部宏命令；command_string='%s'" % command_string)
            return
        #lancaigang250514：
        if self.G_AMSDeviceWorkMode==AMS_WORK_MODE_MA :
            self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_CmdT11]单色续料模式，不处理T11")
            #lancaigang250828:
            self.G_PhrozenFluiddRespondInfo("外部宏命令-PRZ_PAUSE_WAITINGAREA")
            command_string = """
                PRZ_PAUSE_WAITINGAREA
                """
            self.G_PhrozenGCode.run_script_from_command(command_string)
            self.G_PhrozenFluiddRespondInfo("外部宏命令；command_string='%s'" % command_string)
            return
        
        #lancaigang240527：未知模式，因为要操作手动命令，默认让STM32进入MC多色模式
        if self.G_AMSDeviceWorkMode == AMS_WORK_MODE_UNKNOW:
            self.G_PhrozenFluiddRespondInfo("未知模式，因为要操作手动命令，默认让STM32进入MC多色模式")
            self.G_PhrozenFluiddRespondInfo("如果收到T?命令，但模式是未知模式，强制转换为MC多色模式")
            self.G_AMSDeviceWorkMode = AMS_WORK_MODE_MC
            #lancaigang241030:
            if self.G_SerialPort1OpenFlag == True:
                self.Cmds_AMSSerial1Send("MC")
                self.G_PhrozenFluiddRespondInfo("串口1发送命令：MC")
            #lancaigang241030:
            if self.G_SerialPort2OpenFlag == True:
                self.Cmds_AMSSerial2Send("MC")
                self.G_PhrozenFluiddRespondInfo("串口2发送命令：MC")

            self.G_ProzenToolhead.dwell(2)

        #lancaigang250912:导致return异常
        #self.Cmds_CmdOrcaPre()

        

        
        #self.G_PhrozenFluiddRespondInfo("命令='%s'；自动换料" % (gcmd.get_commandline(),))
        self.G_PhrozenFluiddRespondInfo("自动换料")
        #lancaigang240524：用于UIUX动态界面
        self.G_PhrozenFluiddRespondInfo("+T11:0,%d" % self.G_ChangeChannelTimeoutNewChan)
        # #cancel取消命令
        # self.G_PhrozenPrinterCancelPauseResume.cmd_CANCEL_PRINT(None)
        #lancaigang250517：
        Lo_PauseStatus=self.G_PhrozenPrinterCancelPauseResume.get_status(None)
        self.G_PhrozenFluiddRespondInfo("当前暂停状态-Lo_PauseStatus='%s'" % Lo_PauseStatus)
        self.G_PhrozenFluiddRespondInfo("Lo_PauseStatus['is_paused']='%s'" % Lo_PauseStatus['is_paused'])
        #// 当前暂停状态-Lo_PauseStatus='{'is_paused': True}'
        if Lo_PauseStatus['is_paused'] == True:
            self.G_PhrozenFluiddRespondInfo("已是暂停状态")
        else:
            self.G_PhrozenFluiddRespondInfo("未暂停状态")
        #lancaigang240113：清除手动命令标志
        self.ManualCmdFlag=False
        #lancaigang240221：stm32主动上报，开启可以暂停1次
        self.STM32ReprotPauseFlag=0
        self.G_PhrozenFluiddRespondInfo("self.STM32ReprotPauseFlag=0")

        #lancaigang241224：没有第3个AMS，不执行；
        #lancaigang241030:
        if self.G_SerialPort2OpenFlag == True:
            self.G_PhrozenFluiddRespondInfo("有第3个AMS，继续执行命令")
        else:
            self.G_PhrozenFluiddRespondInfo("没有第3个AMS，不执行命令")
            self.G_PhrozenFluiddRespondInfo("+T11:1,%d" % self.G_ChangeChannelTimeoutNewChan)
            return


        #lancaigang241030：一般是P1 C1到P1 C32，范围在1到32
        #第1台：1 2 3 4
        #第2台：5 6 7 8
        #第3台：9 10 11 12
        #第4台：13 14 15 16
        #第5台：17 18 19 20
        #第6台：21 22 23 24
        #第7台：25 26 27 28
        #第8台：29 30 31 32
        #自动换料
        chan=11+1
        self.G_PhrozenFluiddRespondInfo("chan=%d" % chan)
        #lancaigang250515:判断串口屏配置的颜色匹对通道
        if self.G_ChromaKitAccessT11 > 0:
            self.G_PhrozenFluiddRespondInfo("self.G_ChromaKitAccessT11=%d" % self.G_ChromaKitAccessT11)
            self.Cmds_P1CnAutoChangeChannel(self.G_ChromaKitAccessT11, gcmd)
        else:
            self.G_PhrozenFluiddRespondInfo("chan=%d" % chan)
            self.Cmds_P1CnAutoChangeChannel(chan, gcmd)

        #lancaigang240524：用于UIUX动态界面
        self.G_PhrozenFluiddRespondInfo("+T11:1,%d" % self.G_ChangeChannelTimeoutNewChan)

    ####################################
    #函数名称：
    #输入参数：
    #返 回 值:
    #功能描述：蓝才刚-20230830
    ####################################
    def Cmds_CmdT12(self,gcmd):
        self.G_PhrozenFluiddRespondInfo("=====[(cmds.python)Cmds_CmdT12 +1]orca切片多色换料" )

        self.G_PhrozenFluiddRespondInfo("=====self.G_ChangeChannelTimeoutOldChan=%d" % self.G_ChangeChannelTimeoutOldChan)
        self.G_PhrozenFluiddRespondInfo("=====self.G_ChangeChannelTimeoutNewChan=%d" % self.G_ChangeChannelTimeoutNewChan)

        #lancaigang250515：单机打多色，不处理T?
        if self.G_P0M1MCNoneAMS == 1:
            self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_CmdT12]单机打多色，不处理T?")
            #lancaigang250828:
            self.G_PhrozenFluiddRespondInfo("外部宏命令-PRZ_PAUSE_WAITINGAREA")
            command_string = """
                PRZ_PAUSE_WAITINGAREA
                """
            self.G_PhrozenGCode.run_script_from_command(command_string)
            self.G_PhrozenFluiddRespondInfo("外部宏命令；command_string='%s'" % command_string)
            return
        #lancaigang250429：
        if self.G_AMSDeviceWorkMode==AMS_WORK_MODE_FILA_RUNOUT:
            self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_CmdT12]单色模式，不处理T12")
            #lancaigang250828:
            self.G_PhrozenFluiddRespondInfo("外部宏命令-PRZ_PAUSE_WAITINGAREA")
            command_string = """
                PRZ_PAUSE_WAITINGAREA
                """
            self.G_PhrozenGCode.run_script_from_command(command_string)
            self.G_PhrozenFluiddRespondInfo("外部宏命令；command_string='%s'" % command_string)
            return
        #lancaigang250514：
        if self.G_AMSDeviceWorkMode==AMS_WORK_MODE_MA :
            self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_CmdT12]单色续料模式，不处理T12")
            #lancaigang250828:
            self.G_PhrozenFluiddRespondInfo("外部宏命令-PRZ_PAUSE_WAITINGAREA")
            command_string = """
                PRZ_PAUSE_WAITINGAREA
                """
            self.G_PhrozenGCode.run_script_from_command(command_string)
            self.G_PhrozenFluiddRespondInfo("外部宏命令；command_string='%s'" % command_string)
            return
        
        #lancaigang240527：未知模式，因为要操作手动命令，默认让STM32进入MC多色模式
        if self.G_AMSDeviceWorkMode == AMS_WORK_MODE_UNKNOW:
            self.G_PhrozenFluiddRespondInfo("未知模式，因为要操作手动命令，默认让STM32进入MC多色模式")
            self.G_PhrozenFluiddRespondInfo("如果收到T?命令，但模式是未知模式，强制转换为MC多色模式")
            self.G_AMSDeviceWorkMode = AMS_WORK_MODE_MC
            #lancaigang241030:
            if self.G_SerialPort1OpenFlag == True:
                self.Cmds_AMSSerial1Send("MC")
                self.G_PhrozenFluiddRespondInfo("串口1发送命令：MC")
            #lancaigang241030:
            if self.G_SerialPort2OpenFlag == True:
                self.Cmds_AMSSerial2Send("MC")
                self.G_PhrozenFluiddRespondInfo("串口2发送命令：MC")

            self.G_ProzenToolhead.dwell(2)

        #lancaigang250912:导致return异常
        #self.Cmds_CmdOrcaPre()

        

        
        #self.G_PhrozenFluiddRespondInfo("命令='%s'；自动换料" % (gcmd.get_commandline(),))
        self.G_PhrozenFluiddRespondInfo("自动换料")
        #lancaigang240524：用于UIUX动态界面
        self.G_PhrozenFluiddRespondInfo("+T12:0,%d" % self.G_ChangeChannelTimeoutNewChan)
        # #cancel取消命令
        # self.G_PhrozenPrinterCancelPauseResume.cmd_CANCEL_PRINT(None)
        #lancaigang250517：
        Lo_PauseStatus=self.G_PhrozenPrinterCancelPauseResume.get_status(None)
        self.G_PhrozenFluiddRespondInfo("当前暂停状态-Lo_PauseStatus='%s'" % Lo_PauseStatus)
        self.G_PhrozenFluiddRespondInfo("Lo_PauseStatus['is_paused']='%s'" % Lo_PauseStatus['is_paused'])
        #// 当前暂停状态-Lo_PauseStatus='{'is_paused': True}'
        if Lo_PauseStatus['is_paused'] == True:
            self.G_PhrozenFluiddRespondInfo("已是暂停状态")
        else:
            self.G_PhrozenFluiddRespondInfo("未暂停状态")
        #lancaigang240113：清除手动命令标志
        self.ManualCmdFlag=False
        #lancaigang240221：stm32主动上报，开启可以暂停1次
        self.STM32ReprotPauseFlag=0
        self.G_PhrozenFluiddRespondInfo("self.STM32ReprotPauseFlag=0")

        #lancaigang241224：没有第4个AMS，不执行；
        #lancaigang241030:
        if self.G_SerialPort2OpenFlag == True:
            self.G_PhrozenFluiddRespondInfo("有第4个AMS，继续执行命令")
        else:
            self.G_PhrozenFluiddRespondInfo("没有第4个AMS，不执行命令")
            self.G_PhrozenFluiddRespondInfo("+T12:1,%d" % self.G_ChangeChannelTimeoutNewChan)
            return


        #lancaigang241030：一般是P1 C1到P1 C32，范围在1到32
        #第1台：1 2 3 4
        #第2台：5 6 7 8
        #第3台：9 10 11 12
        #第4台：13 14 15 16
        #第5台：17 18 19 20
        #第6台：21 22 23 24
        #第7台：25 26 27 28
        #第8台：29 30 31 32
        #自动换料
        chan=12+1
        self.G_PhrozenFluiddRespondInfo("chan=%d" % chan)
        #lancaigang250515:判断串口屏配置的颜色匹对通道
        if self.G_ChromaKitAccessT12 > 0:
            self.G_PhrozenFluiddRespondInfo("self.G_ChromaKitAccessT12=%d" % self.G_ChromaKitAccessT12)
            self.Cmds_P1CnAutoChangeChannel(self.G_ChromaKitAccessT12, gcmd)
        else:
            self.G_PhrozenFluiddRespondInfo("chan=%d" % chan)
            self.Cmds_P1CnAutoChangeChannel(chan, gcmd)

        #lancaigang240524：用于UIUX动态界面
        self.G_PhrozenFluiddRespondInfo("+T12:1,%d" % self.G_ChangeChannelTimeoutNewChan)

    ####################################
    #函数名称：
    #输入参数：
    #返 回 值:
    #功能描述：蓝才刚-20230830
    ####################################
    def Cmds_CmdT13(self,gcmd):
        self.G_PhrozenFluiddRespondInfo("=====[(cmds.python)Cmds_CmdT13 +1]orca切片多色换料" )

        self.G_PhrozenFluiddRespondInfo("=====self.G_ChangeChannelTimeoutOldChan=%d" % self.G_ChangeChannelTimeoutOldChan)
        self.G_PhrozenFluiddRespondInfo("=====self.G_ChangeChannelTimeoutNewChan=%d" % self.G_ChangeChannelTimeoutNewChan)

        #lancaigang250515：单机打多色，不处理T?
        if self.G_P0M1MCNoneAMS == 1:
            self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_CmdT13]单机打多色，不处理T?")
            #lancaigang250828:
            self.G_PhrozenFluiddRespondInfo("外部宏命令-PRZ_PAUSE_WAITINGAREA")
            command_string = """
                PRZ_PAUSE_WAITINGAREA
                """
            self.G_PhrozenGCode.run_script_from_command(command_string)
            self.G_PhrozenFluiddRespondInfo("外部宏命令；command_string='%s'" % command_string)
            return
        #lancaigang250429：
        if self.G_AMSDeviceWorkMode==AMS_WORK_MODE_FILA_RUNOUT:
            self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_CmdT13]单色模式，不处理T13")
            #lancaigang250828:
            self.G_PhrozenFluiddRespondInfo("外部宏命令-PRZ_PAUSE_WAITINGAREA")
            command_string = """
                PRZ_PAUSE_WAITINGAREA
                """
            self.G_PhrozenGCode.run_script_from_command(command_string)
            self.G_PhrozenFluiddRespondInfo("外部宏命令；command_string='%s'" % command_string)
            return
        #lancaigang250514：
        if self.G_AMSDeviceWorkMode==AMS_WORK_MODE_MA :
            self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_CmdT13]单色续料模式，不处理T13")
            #lancaigang250828:
            self.G_PhrozenFluiddRespondInfo("外部宏命令-PRZ_PAUSE_WAITINGAREA")
            command_string = """
                PRZ_PAUSE_WAITINGAREA
                """
            self.G_PhrozenGCode.run_script_from_command(command_string)
            self.G_PhrozenFluiddRespondInfo("外部宏命令；command_string='%s'" % command_string)
            return
        
        #lancaigang240527：未知模式，因为要操作手动命令，默认让STM32进入MC多色模式
        if self.G_AMSDeviceWorkMode == AMS_WORK_MODE_UNKNOW:
            self.G_PhrozenFluiddRespondInfo("未知模式，因为要操作手动命令，默认让STM32进入MC多色模式")
            self.G_PhrozenFluiddRespondInfo("如果收到T?命令，但模式是未知模式，强制转换为MC多色模式")
            self.G_AMSDeviceWorkMode = AMS_WORK_MODE_MC
            #lancaigang241030:
            if self.G_SerialPort1OpenFlag == True:
                self.Cmds_AMSSerial1Send("MC")
                self.G_PhrozenFluiddRespondInfo("串口1发送命令：MC")
            #lancaigang241030:
            if self.G_SerialPort2OpenFlag == True:
                self.Cmds_AMSSerial2Send("MC")
                self.G_PhrozenFluiddRespondInfo("串口2发送命令：MC")

            self.G_ProzenToolhead.dwell(2)

        #lancaigang250912:导致return异常
        #self.Cmds_CmdOrcaPre()

        

        
        #self.G_PhrozenFluiddRespondInfo("命令='%s'；自动换料" % (gcmd.get_commandline(),))
        self.G_PhrozenFluiddRespondInfo("自动换料")
        #lancaigang240524：用于UIUX动态界面
        self.G_PhrozenFluiddRespondInfo("+T13:0,%d" % self.G_ChangeChannelTimeoutNewChan)
        # #cancel取消命令
        # self.G_PhrozenPrinterCancelPauseResume.cmd_CANCEL_PRINT(None)
        #lancaigang250517：
        Lo_PauseStatus=self.G_PhrozenPrinterCancelPauseResume.get_status(None)
        self.G_PhrozenFluiddRespondInfo("当前暂停状态-Lo_PauseStatus='%s'" % Lo_PauseStatus)
        self.G_PhrozenFluiddRespondInfo("Lo_PauseStatus['is_paused']='%s'" % Lo_PauseStatus['is_paused'])
        #// 当前暂停状态-Lo_PauseStatus='{'is_paused': True}'
        if Lo_PauseStatus['is_paused'] == True:
            self.G_PhrozenFluiddRespondInfo("已是暂停状态")
        else:
            self.G_PhrozenFluiddRespondInfo("未暂停状态")
        #lancaigang240113：清除手动命令标志
        self.ManualCmdFlag=False
        #lancaigang240221：stm32主动上报，开启可以暂停1次
        self.STM32ReprotPauseFlag=0
        self.G_PhrozenFluiddRespondInfo("self.STM32ReprotPauseFlag=0")

        #lancaigang241224：没有第4个AMS，不执行；
        #lancaigang241030:
        if self.G_SerialPort2OpenFlag == True:
            self.G_PhrozenFluiddRespondInfo("有第4个AMS，继续执行命令")
        else:
            self.G_PhrozenFluiddRespondInfo("没有第4个AMS，不执行命令")
            self.G_PhrozenFluiddRespondInfo("+T13:1,%d" % self.G_ChangeChannelTimeoutNewChan)
            return


        #lancaigang241030：一般是P1 C1到P1 C32，范围在1到32
        #第1台：1 2 3 4
        #第2台：5 6 7 8
        #第3台：9 10 11 12
        #第4台：13 14 15 16
        #第5台：17 18 19 20
        #第6台：21 22 23 24
        #第7台：25 26 27 28
        #第8台：29 30 31 32
        #自动换料
        chan=13+1
        self.G_PhrozenFluiddRespondInfo("chan=%d" % chan)
        #lancaigang250515:判断串口屏配置的颜色匹对通道
        if self.G_ChromaKitAccessT13 > 0:
            self.G_PhrozenFluiddRespondInfo("self.G_ChromaKitAccessT13=%d" % self.G_ChromaKitAccessT13)
            self.Cmds_P1CnAutoChangeChannel(self.G_ChromaKitAccessT13, gcmd)
        else:
            self.G_PhrozenFluiddRespondInfo("chan=%d" % chan)
            self.Cmds_P1CnAutoChangeChannel(chan, gcmd)

        #lancaigang240524：用于UIUX动态界面
        self.G_PhrozenFluiddRespondInfo("+T13:1,%d" % self.G_ChangeChannelTimeoutNewChan)

    ####################################
    #函数名称：
    #输入参数：
    #返 回 值:
    #功能描述：蓝才刚-20230830
    ####################################
    def Cmds_CmdT14(self,gcmd):
        self.G_PhrozenFluiddRespondInfo("=====[(cmds.python)Cmds_CmdT14 +1]orca切片多色换料" )

        self.G_PhrozenFluiddRespondInfo("=====self.G_ChangeChannelTimeoutOldChan=%d" % self.G_ChangeChannelTimeoutOldChan)
        self.G_PhrozenFluiddRespondInfo("=====self.G_ChangeChannelTimeoutNewChan=%d" % self.G_ChangeChannelTimeoutNewChan)

        #lancaigang250515：单机打多色，不处理T?
        if self.G_P0M1MCNoneAMS == 1:
            self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_CmdT14]单机打多色，不处理T?")
            #lancaigang250828:
            self.G_PhrozenFluiddRespondInfo("外部宏命令-PRZ_PAUSE_WAITINGAREA")
            command_string = """
                PRZ_PAUSE_WAITINGAREA
                """
            self.G_PhrozenGCode.run_script_from_command(command_string)
            self.G_PhrozenFluiddRespondInfo("外部宏命令；command_string='%s'" % command_string)
            return
        #lancaigang250429：
        if self.G_AMSDeviceWorkMode==AMS_WORK_MODE_FILA_RUNOUT:
            self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_CmdT14]单色模式，不处理T14")
            #lancaigang250828:
            self.G_PhrozenFluiddRespondInfo("外部宏命令-PRZ_PAUSE_WAITINGAREA")
            command_string = """
                PRZ_PAUSE_WAITINGAREA
                """
            self.G_PhrozenGCode.run_script_from_command(command_string)
            self.G_PhrozenFluiddRespondInfo("外部宏命令；command_string='%s'" % command_string)
            return
        #lancaigang250514：
        if self.G_AMSDeviceWorkMode==AMS_WORK_MODE_MA :
            self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_CmdT14]单色续料模式，不处理T14")
            #lancaigang250828:
            self.G_PhrozenFluiddRespondInfo("外部宏命令-PRZ_PAUSE_WAITINGAREA")
            command_string = """
                PRZ_PAUSE_WAITINGAREA
                """
            self.G_PhrozenGCode.run_script_from_command(command_string)
            self.G_PhrozenFluiddRespondInfo("外部宏命令；command_string='%s'" % command_string)
            return
        
        #lancaigang240527：未知模式，因为要操作手动命令，默认让STM32进入MC多色模式
        if self.G_AMSDeviceWorkMode == AMS_WORK_MODE_UNKNOW:
            self.G_PhrozenFluiddRespondInfo("未知模式，因为要操作手动命令，默认让STM32进入MC多色模式")
            self.G_PhrozenFluiddRespondInfo("如果收到T?命令，但模式是未知模式，强制转换为MC多色模式")
            self.G_AMSDeviceWorkMode = AMS_WORK_MODE_MC
            #lancaigang241030:
            if self.G_SerialPort1OpenFlag == True:
                self.Cmds_AMSSerial1Send("MC")
                self.G_PhrozenFluiddRespondInfo("串口1发送命令：MC")
            #lancaigang241030:
            if self.G_SerialPort2OpenFlag == True:
                self.Cmds_AMSSerial2Send("MC")
                self.G_PhrozenFluiddRespondInfo("串口2发送命令：MC")

            self.G_ProzenToolhead.dwell(2)

        #lancaigang250912:导致return异常
        #self.Cmds_CmdOrcaPre()

        

        
        #self.G_PhrozenFluiddRespondInfo("命令='%s'；自动换料" % (gcmd.get_commandline(),))
        self.G_PhrozenFluiddRespondInfo("自动换料")
        #lancaigang240524：用于UIUX动态界面
        self.G_PhrozenFluiddRespondInfo("+T14:0,%d" % self.G_ChangeChannelTimeoutNewChan)
        # #cancel取消命令
        # self.G_PhrozenPrinterCancelPauseResume.cmd_CANCEL_PRINT(None)
        #lancaigang250517：
        Lo_PauseStatus=self.G_PhrozenPrinterCancelPauseResume.get_status(None)
        self.G_PhrozenFluiddRespondInfo("当前暂停状态-Lo_PauseStatus='%s'" % Lo_PauseStatus)
        self.G_PhrozenFluiddRespondInfo("Lo_PauseStatus['is_paused']='%s'" % Lo_PauseStatus['is_paused'])
        #// 当前暂停状态-Lo_PauseStatus='{'is_paused': True}'
        if Lo_PauseStatus['is_paused'] == True:
            self.G_PhrozenFluiddRespondInfo("已是暂停状态")
        else:
            self.G_PhrozenFluiddRespondInfo("未暂停状态")
        #lancaigang240113：清除手动命令标志
        self.ManualCmdFlag=False
        #lancaigang240221：stm32主动上报，开启可以暂停1次
        self.STM32ReprotPauseFlag=0
        self.G_PhrozenFluiddRespondInfo("self.STM32ReprotPauseFlag=0")

        #lancaigang241224：没有第4个AMS，不执行；
        #lancaigang241030:
        if self.G_SerialPort2OpenFlag == True:
            self.G_PhrozenFluiddRespondInfo("有第4个AMS，继续执行命令")
        else:
            self.G_PhrozenFluiddRespondInfo("没有第4个AMS，不执行命令")
            self.G_PhrozenFluiddRespondInfo("+T14:1,%d" % self.G_ChangeChannelTimeoutNewChan)
            return


        #lancaigang241030：一般是P1 C1到P1 C32，范围在1到32
        #第1台：1 2 3 4
        #第2台：5 6 7 8
        #第3台：9 10 11 12
        #第4台：13 14 15 16
        #第5台：17 18 19 20
        #第6台：21 22 23 24
        #第7台：25 26 27 28
        #第8台：29 30 31 32
        #自动换料
        chan=14+1
        self.G_PhrozenFluiddRespondInfo("chan=%d" % chan)
        #lancaigang250515:判断串口屏配置的颜色匹对通道
        if self.G_ChromaKitAccessT14 > 0:
            self.G_PhrozenFluiddRespondInfo("self.G_ChromaKitAccessT14=%d" % self.G_ChromaKitAccessT14)
            self.Cmds_P1CnAutoChangeChannel(self.G_ChromaKitAccessT14, gcmd)
        else:
            self.G_PhrozenFluiddRespondInfo("chan=%d" % chan)
            self.Cmds_P1CnAutoChangeChannel(chan, gcmd)

        #lancaigang240524：用于UIUX动态界面
        self.G_PhrozenFluiddRespondInfo("+T14:1,%d" % self.G_ChangeChannelTimeoutNewChan)

    ####################################
    #函数名称：
    #输入参数：
    #返 回 值:
    #功能描述：蓝才刚-20230830
    ####################################
    def Cmds_CmdT15(self,gcmd):
        self.G_PhrozenFluiddRespondInfo("=====[(cmds.python)Cmds_CmdT15 +1]orca切片多色换料" )

        self.G_PhrozenFluiddRespondInfo("=====self.G_ChangeChannelTimeoutOldChan=%d" % self.G_ChangeChannelTimeoutOldChan)
        self.G_PhrozenFluiddRespondInfo("=====self.G_ChangeChannelTimeoutNewChan=%d" % self.G_ChangeChannelTimeoutNewChan)

        #lancaigang250515：单机打多色，不处理T?
        if self.G_P0M1MCNoneAMS == 1:
            self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_CmdT15]单机打多色，不处理T?")
            #lancaigang250828:
            self.G_PhrozenFluiddRespondInfo("外部宏命令-PRZ_PAUSE_WAITINGAREA")
            command_string = """
                PRZ_PAUSE_WAITINGAREA
                """
            self.G_PhrozenGCode.run_script_from_command(command_string)
            self.G_PhrozenFluiddRespondInfo("外部宏命令；command_string='%s'" % command_string)
            return
        #lancaigang250429：
        if self.G_AMSDeviceWorkMode==AMS_WORK_MODE_FILA_RUNOUT:
            self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_CmdT15]单色模式，不处理T15")
            #lancaigang250828:
            self.G_PhrozenFluiddRespondInfo("外部宏命令-PRZ_PAUSE_WAITINGAREA")
            command_string = """
                PRZ_PAUSE_WAITINGAREA
                """
            self.G_PhrozenGCode.run_script_from_command(command_string)
            self.G_PhrozenFluiddRespondInfo("外部宏命令；command_string='%s'" % command_string)
            return
        #lancaigang250514：
        if self.G_AMSDeviceWorkMode==AMS_WORK_MODE_MA :
            self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_CmdT15]单色续料模式，不处理T15")
            #lancaigang250828:
            self.G_PhrozenFluiddRespondInfo("外部宏命令-PRZ_PAUSE_WAITINGAREA")
            command_string = """
                PRZ_PAUSE_WAITINGAREA
                """
            self.G_PhrozenGCode.run_script_from_command(command_string)
            self.G_PhrozenFluiddRespondInfo("外部宏命令；command_string='%s'" % command_string)
            return
        
        #lancaigang240527：未知模式，因为要操作手动命令，默认让STM32进入MC多色模式
        if self.G_AMSDeviceWorkMode == AMS_WORK_MODE_UNKNOW:
            self.G_PhrozenFluiddRespondInfo("未知模式，因为要操作手动命令，默认让STM32进入MC多色模式")
            self.G_PhrozenFluiddRespondInfo("如果收到T?命令，但模式是未知模式，强制转换为MC多色模式")
            self.G_AMSDeviceWorkMode = AMS_WORK_MODE_MC
            #lancaigang241030:
            if self.G_SerialPort1OpenFlag == True:
                self.Cmds_AMSSerial1Send("MC")
                self.G_PhrozenFluiddRespondInfo("串口1发送命令：MC")
            #lancaigang241030:
            if self.G_SerialPort2OpenFlag == True:
                self.Cmds_AMSSerial2Send("MC")
                self.G_PhrozenFluiddRespondInfo("串口2发送命令：MC")

            self.G_ProzenToolhead.dwell(2)

        #lancaigang250912:
        #self.Cmds_CmdOrcaPre()

        

        
        #self.G_PhrozenFluiddRespondInfo("命令='%s'；自动换料" % (gcmd.get_commandline(),))
        self.G_PhrozenFluiddRespondInfo("自动换料")
        #lancaigang240524：用于UIUX动态界面
        self.G_PhrozenFluiddRespondInfo("+T15:0,%d" % self.G_ChangeChannelTimeoutNewChan)
        # #cancel取消命令
        # self.G_PhrozenPrinterCancelPauseResume.cmd_CANCEL_PRINT(None)
        #lancaigang250517：
        Lo_PauseStatus=self.G_PhrozenPrinterCancelPauseResume.get_status(None)
        self.G_PhrozenFluiddRespondInfo("当前暂停状态-Lo_PauseStatus='%s'" % Lo_PauseStatus)
        self.G_PhrozenFluiddRespondInfo("Lo_PauseStatus['is_paused']='%s'" % Lo_PauseStatus['is_paused'])
        #// 当前暂停状态-Lo_PauseStatus='{'is_paused': True}'
        if Lo_PauseStatus['is_paused'] == True:
            self.G_PhrozenFluiddRespondInfo("已是暂停状态")
        else:
            self.G_PhrozenFluiddRespondInfo("未暂停状态")
        #lancaigang240113：清除手动命令标志
        self.ManualCmdFlag=False
        #lancaigang240221：stm32主动上报，开启可以暂停1次
        self.STM32ReprotPauseFlag=0
        self.G_PhrozenFluiddRespondInfo("self.STM32ReprotPauseFlag=0")

        #lancaigang241224：没有第4个AMS，不执行；
        #lancaigang241030:
        if self.G_SerialPort2OpenFlag == True:
            self.G_PhrozenFluiddRespondInfo("有第4个AMS，继续执行命令")
        else:
            self.G_PhrozenFluiddRespondInfo("没有第4个AMS，不执行命令")
            self.G_PhrozenFluiddRespondInfo("+T15:1,%d" % self.G_ChangeChannelTimeoutNewChan)
            return

        #lancaigang241030：一般是P1 C1到P1 C32，范围在1到32
        #第1台：1 2 3 4
        #第2台：5 6 7 8
        #第3台：9 10 11 12
        #第4台：13 14 15 16
        #第5台：17 18 19 20
        #第6台：21 22 23 24
        #第7台：25 26 27 28
        #第8台：29 30 31 32
        #自动换料
        chan=15+1
        self.G_PhrozenFluiddRespondInfo("chan=%d" % chan)
        #lancaigang250515:判断串口屏配置的颜色匹对通道
        if self.G_ChromaKitAccessT15 > 0:
            self.G_PhrozenFluiddRespondInfo("self.G_ChromaKitAccessT15=%d" % self.G_ChromaKitAccessT15)
            self.Cmds_P1CnAutoChangeChannel(self.G_ChromaKitAccessT15, gcmd)
        else:
            self.G_PhrozenFluiddRespondInfo("chan=%d" % chan)
            self.Cmds_P1CnAutoChangeChannel(chan, gcmd)

        #lancaigang240524：用于UIUX动态界面
        self.G_PhrozenFluiddRespondInfo("+T15:1,%d" % self.G_ChangeChannelTimeoutNewChan)




    ####################################
    #函数名称：
    #输入参数：
    #返 回 值:
    #功能描述：蓝才刚-20230830
    ####################################
    # PRZ_VERSION 查询版本
    def Cmds_PhrozenVersion(self, gcmd):
        # ASCII字符集共计有128个字符(见上表)，码点编号(即字符编号)从0到127(二进制为从0000 0000到0111 1111，
        #十六进制为从0x00到0x7F)，二进制最高位都是0。其中：
        # 0~31：不可显示不可打印的控制字符或通讯专用字符，如0x07(BEL响铃)会让计算机发出哔的一声、0x00(NUL空，注意不是空格)
        #通常用于指示字符串的结束、0x0D(CR回车)和0x0A(LF换行)用于指示打印机的打印针头退到行首(即回车)并移到下一行(即换行)等；
        # 注： 将这些用于控制或通讯的控制字符或通讯专用字符称之为“字符”，感觉上似乎有点怪，实际上这些所谓的“字符”表示的其实是一种动作或行为，
        #因此才既不可显示也不可打印。
        # 32：可显示但不可打印的空格字符；
        # 33~126：可显示可打印字符，其中48~57为0-9的阿拉伯数字，65~90为26个大写英文字母，97~122为26个小写英文字母，
        #其余的是一些标点符号、运算符号等；
        # 127：不可显示不可打印的控制字符DEL。


        self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_PhrozenVersion]命令='%s'" % (gcmd.get_commandline(),))


        self.G_PhrozenFluiddRespondInfo("当前模式")
        if self.G_AMSDeviceWorkMode == AMS_WORK_MODE_UNKNOW:
            self.G_PhrozenFluiddRespondInfo("+Mode:0,unkown")
        elif self.G_AMSDeviceWorkMode == AMS_WORK_MODE_MC:
            self.G_PhrozenFluiddRespondInfo("+Mode:1,MC")
        elif self.G_AMSDeviceWorkMode == AMS_WORK_MODE_MA:
            self.G_PhrozenFluiddRespondInfo("+Mode:2,MA")
        elif self.G_AMSDeviceWorkMode == AMS_WORK_MODE_FILA_RUNOUT:
            self.G_PhrozenFluiddRespondInfo("+Mode:3,RUNOUT")
        else:
            self.G_PhrozenFluiddRespondInfo("+Mode:-1,error")



        self.G_PhrozenFluiddRespondInfo("%s" % (gcmd.get_commandline(),))
        # #lancaigang240224：测试
        # command = """
        # PAUSE
        # """
        # self.G_PhrozenGCode.run_script_from_command(command)
        # self.G_PhrozenFluiddRespondInfo("[(cmds.Cmds_PhrozenVersion)]调用宏命令:command=%s" % (command))
        # self.G_PhrozenFluiddRespondInfo("[(cmds.Cmds_PhrozenVersion)]防止暂停不住，多加命令；send_pause_command")
        # self.G_PhrozenPrinterCancelPauseResume.send_pause_command()
        #lancaigang250619:检查AMS是否重新连接成功
        self.Cmds_USBConnectErrorCheck()
        #lancaigang241031:
        if self.G_SerialPort1OpenFlag == True:
            #lancaigang240524：读取AMS主板版本、16HUB主板版本
            self.Cmds_AMSSerial1Send("AT+SB=0")
            self.G_PhrozenFluiddRespondInfo("串口1发送命令: AT+SB=0；获取AMS主板版本、16色HUB主板版本")
        #lancaigang241030:
        if self.G_SerialPort2OpenFlag == True:
            self.Cmds_AMSSerial2Send("AT+SB=0")
            self.G_PhrozenFluiddRespondInfo("串口2发送命令: AT+SB=0；获取AMS主板版本、16色HUB主板版本")

        #lancaigang240529：phrozen插件版本
        self.G_PhrozenFluiddRespondInfo("V-H%s-I%s-F%s" % (HW_VERSION,IMAGE_VERSION,FW_VERSION))


        #emb_filename = "/home/prz/hdlDat/DriveCodeJson.dat"
        #json_data = json.load(emb_filename)
        # self.G_PhrozenFluiddRespondInfo("json_data=%s" % json_data)
        # DriveCode = json_data['DriveCode']
        # DriveImageType = json_data['DriveImageType']
        # DriveHwVersion = json_data['DriveHwVersion']
        # DriveFwVersion = json_data['DriveFwVersion']
        # DriveId = json_data['DriveId']
        # self.G_PhrozenFluiddRespondInfo("DriveCode=%s" % DriveCode)
        # self.G_PhrozenFluiddRespondInfo("DriveImageType=%s" % DriveImageType)
        # self.G_PhrozenFluiddRespondInfo("DriveHwVersion=%s" % DriveHwVersion)
        # self.G_PhrozenFluiddRespondInfo("DriveFwVersion=%s" % DriveFwVersion)
        # self.G_PhrozenFluiddRespondInfo("DriveId=%s" % DriveId)



        #self.G_ProzenToolhead.dwell(1.5)


        #=====DriveCodeFile.dat
        # 1 , 18 , 24053 , 18 , 0# // AMS主板1固件-18
        # 2 , 18 , 24053 , 18 , 0# // AMS主板2固件-18
        # 3 , 18 , 24053 , 18 , 0# // AMS主板3固件-18
        # 4 , 18 , 24053 , 18 , 0# // AMS主板4固件-18
        # 5 , 5 , 24046 , 5 , 0# // OTA子程序-AMS串口升级程序-5 5
        # 6 , 0 , 0 , 0 , 0# // 缓冲器板固件-6 6 保留
        # 7 , 7 , 24051 , 7 , 0# // 16色HUB板固件-7 7
        # 8 , 0 , 0 , 0 , 0
        # 9 , 0 , 0 , 0 , 0
        # 10 , 10 , 24054 , 10 , 0# // OTA子程序-陶晶池串口屏后台程序-10
        # 11 , 11 , 24047 , 11 , 0# // 陶晶池串口屏前台HMI固件-11
        # 12 , 0 , 0 , 0 , 0
        # 13 , 0 , 0 , 0 , 0
        # 14 , 0 , 0 , 0 , 0
        # 15 , 15 , 25042 , 15 , 0
        # 16 , 16 , 25042 , 16 , 0
        # 17 , ? , 25042 , ? , 0
        # 18 , ? , 25042 , ? , 0
        # 19 , ? , 25042 , ? , 0
        # 20 , ? , 25042 , ? , 0
        #lancaigang240530：版本写到dat文件；DriveCodeJson.dat
               #lancaigang250724：读取系统镜像id，区分不同产品不同主板不同固件
        #lancaigang250724:读取镜像id
        self.Cmds_GetImageId()
        if self.G_ImageId==16:
            self.G_PhrozenFluiddRespondInfo("镜像Id==16：ARCO300-MKS-RK3328-STM32F407VET6-I16")
            filename='/home/mks/hdlDat/DriveCodeFile.dat'
            self.G_PhrozenFluiddRespondInfo("filename=%s" % filename)
        elif self.G_ImageId==31:
            self.G_PhrozenFluiddRespondInfo("镜像Id==31：ARCO300-phrozen-RK3308-STM32F407VET6-I31")
            filename='/home/prz/hdlDat/DriveCodeFile.dat'
            self.G_PhrozenFluiddRespondInfo("filename=%s" % filename)
        elif self.G_ImageId==-1:
            self.G_PhrozenFluiddRespondInfo("镜像Id==-1，默认：ARCO300-MKS-RK3328-STM32F407VET6-I16")
            filename='/home/mks/hdlDat/DriveCodeFile.dat'
            self.G_PhrozenFluiddRespondInfo("filename=%s" % filename)
        else:
            self.G_PhrozenFluiddRespondInfo("镜像Id读不到，默认：ARCO300-MKS-RK3328-STM32F407VET6-I16")
            filename='/home/mks/hdlDat/DriveCodeFile.dat'
            self.G_PhrozenFluiddRespondInfo("filename=%s" % filename)

        Lo_AllLine=""
        #data = [{"DriveCode":16,"DriveImageType":0,"DriveHwVersion":0,"DriveFwVersion":0,"DriveId":0},{"DriveCode":15,"DriveImageType":0,"DriveHwVersion":0,"DriveFwVersion":0,"DriveId":0},{"DriveCode":14,"DriveImageType":0,"DriveHwVersion":0,"DriveFwVersion":0,"DriveId":0},{"DriveCode":13,"DriveImageType":0,"DriveHwVersion":0,"DriveFwVersion":0,"DriveId":0},{"DriveCode":12,"DriveImageType":0,"DriveHwVersion":0,"DriveFwVersion":0,"DriveId":0},{"DriveCode":11,"DriveImageType":0,"DriveHwVersion":0,"DriveFwVersion":0,"DriveId":0},{"DriveCode":10,"DriveImageType":10,"DriveHwVersion":10,"DriveFwVersion":24045,"DriveId":0},{"DriveCode":9,"DriveImageType":0,"DriveHwVersion":0,"DriveFwVersion":0,"DriveId":0},{"DriveCode":8,"DriveImageType":0,"DriveHwVersion":0,"DriveFwVersion":0,"DriveId":0},{"DriveCode":7,"DriveImageType":0,"DriveHwVersion":0,"DriveFwVersion":0,"DriveId":0},{"DriveCode":6,"DriveImageType":0,"DriveHwVersion":0,"DriveFwVersion":0,"DriveId":0},{"DriveCode":5,"DriveImageType":5,"DriveHwVersion":5,"DriveFwVersion":24046,"DriveId":0},{"DriveCode":4,"DriveImageType":0,"DriveHwVersion":0,"DriveFwVersion":0,"DriveId":0},{"DriveCode":3,"DriveImageType":0,"DriveHwVersion":0,"DriveFwVersion":0,"DriveId":0},{"DriveCode":2,"DriveImageType":0,"DriveHwVersion":0,"DriveFwVersion":0,"DriveId":0},{"DriveCode":1,"DriveImageType":1,"DriveHwVersion":1,"DriveFwVersion":24042,"DriveId":0}]
        #f = open(filename, 'a')
        #json.dump(data, f)  #对象序列号为字节流
        #f.close()
        with open(filename,'r') as file:
            #for line in file:
            # # realine() 读取整行内容，包括 "\n" 字符
            # self.G_PhrozenFluiddRespondInfo(file.readline().strip())
            # #time.sleep(1)
            Lo_FileDataList=file.readlines()
            for line in Lo_FileDataList:
                #split = [i[:-1].split(',') for i in file.readlines()]
                #self.G_PhrozenFluiddRespondInfo(type(split))
                #self.G_PhrozenFluiddRespondInfo(split[1])
                #self.G_PhrozenFluiddRespondInfo(split[2])
                #self.G_PhrozenFluiddRespondInfo(split[3])
                #line_strip=line.strip()
                #self.G_PhrozenFluiddRespondInfo(line)
                #self.G_PhrozenFluiddRespondInfo("line.count=%d" % line.count)
                split=line.split(',')
                #self.G_PhrozenFluiddRespondInfo(type(split))
                #self.G_PhrozenFluiddRespondInfo("".join(split))
                #self.G_PhrozenFluiddRespondInfo(split[0])
                split[0]=split[0].strip()#驱动号
                split[1]=split[1].strip()#硬件id
                split[2]=split[2].strip()#固件版本
                split[3]=split[3].strip()#镜像id
                split[4]=split[4].strip()#是否在线

                #lancaigang240617：先把镜像id=1和7的在线状态置位0离线，如果AMS有响应，再置位1在线

                if split[0]=="16":
                    self.G_PhrozenFluiddRespondInfo(split[0])
                    self.G_PhrozenFluiddRespondInfo(split[1])
                    self.G_PhrozenFluiddRespondInfo(split[2])
                    self.G_PhrozenFluiddRespondInfo(split[3])
                    self.G_PhrozenFluiddRespondInfo(split[4])
                    #line=("%d,%d,%d," % (HW_VERSION,,))
                    line_modify=split[0]+','+'16'+','+str(FW_VERSION)+','+'16'+','+'1'
                    self.G_PhrozenFluiddRespondInfo(line_modify)
                    Lo_AllLine=Lo_AllLine+line_modify+"\r\n"#0x0D 0x0A
                elif split[0]=="1":
                    self.G_PhrozenFluiddRespondInfo(split[0])
                    self.G_PhrozenFluiddRespondInfo(split[1])
                    self.G_PhrozenFluiddRespondInfo(split[2])
                    self.G_PhrozenFluiddRespondInfo(split[3])
                    self.G_PhrozenFluiddRespondInfo(split[4])
                    line_modify=split[0]+','+'1'+','+"00000"+','+'1'+','+'0'
                    self.G_PhrozenFluiddRespondInfo(line_modify)
                    Lo_AllLine=Lo_AllLine+line_modify+"\r\n"#0x0D 0x0A
                elif split[0]=="2":
                    self.G_PhrozenFluiddRespondInfo(split[0])
                    self.G_PhrozenFluiddRespondInfo(split[1])
                    self.G_PhrozenFluiddRespondInfo(split[2])
                    self.G_PhrozenFluiddRespondInfo(split[3])
                    self.G_PhrozenFluiddRespondInfo(split[4])
                    line_modify=split[0]+','+'1'+','+"00000"+','+'1'+','+'0'
                    self.G_PhrozenFluiddRespondInfo(line_modify)
                    Lo_AllLine=Lo_AllLine+line_modify+"\r\n"#0x0D 0x0A
                elif split[0]=="3":
                    self.G_PhrozenFluiddRespondInfo(split[0])
                    self.G_PhrozenFluiddRespondInfo(split[1])
                    self.G_PhrozenFluiddRespondInfo(split[2])
                    self.G_PhrozenFluiddRespondInfo(split[3])
                    self.G_PhrozenFluiddRespondInfo(split[4])
                    line_modify=split[0]+','+'1'+','+"00000"+','+'1'+','+'0'
                    self.G_PhrozenFluiddRespondInfo(line_modify)
                    Lo_AllLine=Lo_AllLine+line_modify+"\r\n"#0x0D 0x0A
                elif split[0]=="4":
                    self.G_PhrozenFluiddRespondInfo(split[0])
                    self.G_PhrozenFluiddRespondInfo(split[1])
                    self.G_PhrozenFluiddRespondInfo(split[2])
                    self.G_PhrozenFluiddRespondInfo(split[3])
                    self.G_PhrozenFluiddRespondInfo(split[4])
                    line_modify=split[0]+','+'1'+','+"00000"+','+'1'+','+'0'
                    self.G_PhrozenFluiddRespondInfo(line_modify)
                    Lo_AllLine=Lo_AllLine+line_modify+"\r\n"#0x0D 0x0A
                elif split[0]=="5":
                    self.G_PhrozenFluiddRespondInfo(split[0])
                    self.G_PhrozenFluiddRespondInfo(split[1])
                    self.G_PhrozenFluiddRespondInfo(split[2])
                    self.G_PhrozenFluiddRespondInfo(split[3])
                    self.G_PhrozenFluiddRespondInfo(split[4])
                    line_modify=split[0]+','+split[1]+','+split[2]+','+split[3]+','+'1'
                    self.G_PhrozenFluiddRespondInfo(line_modify)
                    Lo_AllLine=Lo_AllLine+line_modify+"\r\n"#0x0D 0x0A
                elif split[0]=="10":
                    self.G_PhrozenFluiddRespondInfo(split[0])
                    self.G_PhrozenFluiddRespondInfo(split[1])
                    self.G_PhrozenFluiddRespondInfo(split[2])
                    self.G_PhrozenFluiddRespondInfo(split[3])
                    self.G_PhrozenFluiddRespondInfo(split[4])
                    line_modify=split[0]+','+split[1]+','+split[2]+','+split[3]+','+'1'
                    self.G_PhrozenFluiddRespondInfo(line_modify)
                    Lo_AllLine=Lo_AllLine+line_modify+"\r\n"#0x0D 0x0A
                elif split[0]=="7":
                    self.G_PhrozenFluiddRespondInfo(split[0])
                    self.G_PhrozenFluiddRespondInfo(split[1])
                    self.G_PhrozenFluiddRespondInfo(split[2])
                    self.G_PhrozenFluiddRespondInfo(split[3])
                    self.G_PhrozenFluiddRespondInfo(split[4])
                    line_modify=split[0]+','+'7'+','+"00000"+','+'7'+','+'0'
                    self.G_PhrozenFluiddRespondInfo(line_modify)
                    Lo_AllLine=Lo_AllLine+line_modify+"\r\n"#0x0D 0x0A

                elif split[0]=="17":
                    self.G_PhrozenFluiddRespondInfo(split[0])
                    self.G_PhrozenFluiddRespondInfo(split[1])
                    self.G_PhrozenFluiddRespondInfo(split[2])
                    self.G_PhrozenFluiddRespondInfo(split[3])
                    self.G_PhrozenFluiddRespondInfo(split[4])
                    #line=("%d,%d,%d," % (HW_VERSION,,))
                    line_modify=split[0]+','+'18'+','+"00000"+','+'18'+','+'0'
                    self.G_PhrozenFluiddRespondInfo(line_modify)
                    Lo_AllLine=Lo_AllLine+line_modify+"\r\n"#0x0D 0x0A
                elif split[0]=="18":
                    self.G_PhrozenFluiddRespondInfo(split[0])
                    self.G_PhrozenFluiddRespondInfo(split[1])
                    self.G_PhrozenFluiddRespondInfo(split[2])
                    self.G_PhrozenFluiddRespondInfo(split[3])
                    self.G_PhrozenFluiddRespondInfo(split[4])
                    #line=("%d,%d,%d," % (HW_VERSION,,))
                    line_modify=split[0]+','+'18'+','+"00000"+','+'18'+','+'0'
                    self.G_PhrozenFluiddRespondInfo(line_modify)
                    Lo_AllLine=Lo_AllLine+line_modify+"\r\n"#0x0D 0x0A
                elif split[0]=="19":
                    self.G_PhrozenFluiddRespondInfo(split[0])
                    self.G_PhrozenFluiddRespondInfo(split[1])
                    self.G_PhrozenFluiddRespondInfo(split[2])
                    self.G_PhrozenFluiddRespondInfo(split[3])
                    self.G_PhrozenFluiddRespondInfo(split[4])
                    #line=("%d,%d,%d," % (HW_VERSION,,))
                    line_modify=split[0]+','+'18'+','+"00000"+','+'18'+','+'0'
                    self.G_PhrozenFluiddRespondInfo(line_modify)
                    Lo_AllLine=Lo_AllLine+line_modify+"\r\n"#0x0D 0x0A
                elif split[0]=="20":
                    self.G_PhrozenFluiddRespondInfo(split[0])
                    self.G_PhrozenFluiddRespondInfo(split[1])
                    self.G_PhrozenFluiddRespondInfo(split[2])
                    self.G_PhrozenFluiddRespondInfo(split[3])
                    self.G_PhrozenFluiddRespondInfo(split[4])
                    #line=("%d,%d,%d," % (HW_VERSION,,))
                    line_modify=split[0]+','+'18'+','+"00000"+','+'18'+','+'0'
                    self.G_PhrozenFluiddRespondInfo(line_modify)
                    Lo_AllLine=Lo_AllLine+line_modify+"\r\n"#0x0D 0x0A


                else:
                    Lo_AllLine=Lo_AllLine+line
        #self.G_PhrozenFluiddRespondInfo(Lo_AllLine)
        with open(filename,"w+") as file_w:
	        file_w.write(Lo_AllLine)




        #self.G_PhrozenFluiddRespondInfo("PRZ_DEV_VER: %s" % FW_VERSION)
        #self.G_PhrozenFluiddRespondInfo("V-H'%s'-I'%s'-F'%s'" % (HW_VERSION,IMAGE_VERSION,FW_VERSION))




    ####################################
    #函数名称：
    #输入参数：
    #返 回 值:
    #功能描述：# PRZ_ADC 查询打印头线线材传感器值(用于测试)
    ####################################
    #lancaigang251020：
    def Cmds_PhrozenAdc(self,gcmd):
        self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_PhrozenAdc]命令=PRZ_ADC")

        self.G_PhrozenFluiddRespondInfo("=====self.G_ChangeChannelTimeoutOldChan=%d" % self.G_ChangeChannelTimeoutOldChan)
        self.G_PhrozenFluiddRespondInfo("=====self.G_ChangeChannelTimeoutNewChan=%d" % self.G_ChangeChannelTimeoutNewChan)
       
        # 读取喷头最后的ADC值
        value, timestamp = self.G_ToolheadAdc.get_last_value()
        
        self.G_PhrozenFluiddRespondInfo("PRZ_ADC:读取ADC值 %.6f (timestamp %.3f)  fila_exist:%r" % (value, timestamp, self.G_ToolheadIfHaveFilaFlag))
        self.G_PhrozenFluiddRespondInfo("self.G_ToolheadIfHaveFilaFlag=%d" % (self.G_ToolheadIfHaveFilaFlag))
        self.G_PhrozenFluiddRespondInfo("self.G_AMS1ErrorRestartCount=%d" % (self.G_AMS1ErrorRestartCount))

        self.G_PhrozenFluiddRespondInfo("当前模式")
        if self.G_AMSDeviceWorkMode == AMS_WORK_MODE_UNKNOW:
            self.G_PhrozenFluiddRespondInfo("+Mode:0,unkown")
        elif self.G_AMSDeviceWorkMode == AMS_WORK_MODE_MC:
            self.G_PhrozenFluiddRespondInfo("+Mode:1,MC")
        elif self.G_AMSDeviceWorkMode == AMS_WORK_MODE_MA:
            self.G_PhrozenFluiddRespondInfo("+Mode:2,MA")
        elif self.G_AMSDeviceWorkMode == AMS_WORK_MODE_FILA_RUNOUT:
            self.G_PhrozenFluiddRespondInfo("+Mode:3,RUNOUT")
        else:
            self.G_PhrozenFluiddRespondInfo("+Mode:-1,error")


        self.G_PhrozenFluiddRespondInfo("self.G_P0M3Flag=%d" % (self.G_P0M3Flag))
        self.G_PhrozenFluiddRespondInfo("self.G_KlipperIfPaused=%d" % (self.G_KlipperIfPaused))
        self.G_PhrozenFluiddRespondInfo("self.G_CancelFlag=%d" % (self.G_CancelFlag))
        self.G_PhrozenFluiddRespondInfo("self.G_IfChangeFilaOngoing=%d" % (self.G_IfChangeFilaOngoing))
        self.G_PhrozenFluiddRespondInfo("self.G_SerialPort1OpenFlag=%d" % (self.G_SerialPort1OpenFlag))
        self.G_PhrozenFluiddRespondInfo("self.G_P0M2MAStartPrintFlag=%d" % (self.G_P0M2MAStartPrintFlag))
        self.G_PhrozenFluiddRespondInfo("self.G_M2MAModeResumeFlag=%d" % (self.G_M2MAModeResumeFlag))
        self.G_PhrozenFluiddRespondInfo("self.G_KlipperPrintStatus=%d" % (self.G_KlipperPrintStatus))
        self.G_PhrozenFluiddRespondInfo("self.G_SerialPort1OpenFlag=%d" % (self.G_SerialPort1OpenFlag))
        self.G_PhrozenFluiddRespondInfo("self.G_SerialPort2OpenFlag=%d" % (self.G_SerialPort2OpenFlag))
        self.G_PhrozenFluiddRespondInfo("self.ManualCmdFlag=%d" % (self.ManualCmdFlag))
        self.G_PhrozenFluiddRespondInfo("self.STM32ReprotPauseFlag=%d" % (self.STM32ReprotPauseFlag))
        self.G_PhrozenFluiddRespondInfo("self.PG102Flag=%d" % (self.PG102Flag))
        self.G_PhrozenFluiddRespondInfo("self.G_IfInFilaBlockFlag=%d" % (self.G_IfInFilaBlockFlag))
        self.G_PhrozenFluiddRespondInfo("self.PG102DelayPauseFlag=%d" % (self.PG102DelayPauseFlag))
        self.G_PhrozenFluiddRespondInfo("self.G_KlipperQuickPause=%d" % (self.G_KlipperQuickPause))
        self.G_PhrozenFluiddRespondInfo("self.G_PauseToLCDString=%s" % (self.G_PauseToLCDString))






        Lo_PauseStatus=self.G_PhrozenPrinterCancelPauseResume.get_status(None)
        self.G_PhrozenFluiddRespondInfo("当前暂停状态-Lo_PauseStatus='%s'" % Lo_PauseStatus)

        self.G_PhrozenFluiddRespondInfo("Lo_PauseStatus['is_paused']='%s'" % Lo_PauseStatus['is_paused'])
        #// 当前暂停状态-Lo_PauseStatus='{'is_paused': True}'
        if Lo_PauseStatus['is_paused'] == True:
            self.G_PhrozenFluiddRespondInfo("已是暂停状态")
        else:
            self.G_PhrozenFluiddRespondInfo("未暂停状态")


        #lancaigang250619:检查AMS是否重新连接成功
        self.Cmds_USBConnectErrorCheck()
        #lancaigang241031:
        if self.G_SerialPort1OpenFlag == True:
            #lancaigang240524：读取AMS主板版本、16HUB主板版本
            self.Cmds_AMSSerial1Send("AT+SB=0")
            self.G_PhrozenFluiddRespondInfo("串口1发送命令: AT+SB=0；获取AMS主板版本、16色HUB主板版本")
        #lancaigang241030:
        if self.G_SerialPort2OpenFlag == True:
            #lancaigang240524：读取AMS主板版本、16HUB主板版本
            self.Cmds_AMSSerial2Send("AT+SB=0")
            self.G_PhrozenFluiddRespondInfo("串口2发送命令: AT+SB=0；获取AMS主板版本、16色HUB主板版本")


        #lancaigang240529：phrozen插件版本
        self.G_PhrozenFluiddRespondInfo("V-H%s-I%s-F%s-SN1" % (HW_VERSION,IMAGE_VERSION,FW_VERSION))

        #time.sleep(1)

        #self.Cmds_AMSSerial1Send("AT+SB=1")
        #self.G_PhrozenFluiddRespondInfo("发送命令: AT+SB=1；获取AMS主板状态")



        #PRZ_PwrDownResumePrint
        try:
            self.G_PhrozenFluiddRespondInfo("try")
            #lancaigang240530：版本写到dat文件；DriveCodeJson.dat

            #lancaigang250724：读取系统镜像id，区分不同产品不同主板不同固件
            #lancaigang250724:读取镜像id
            self.Cmds_GetImageId()
            if self.G_ImageId==16:
                self.G_PhrozenFluiddRespondInfo("镜像Id==16：ARCO300-MKS-RK3328-STM32F407VET6-I16")
                with open('/home/mks/hdlDat/Phrozen_Dev.json', 'r', encoding='utf-8') as file:
                    FileRead = file.read()
                    self.G_PhrozenFluiddRespondInfo("读取json文件")
                    # 解析JSON数据
                    json_data = json.loads(FileRead)
                    self.G_PhrozenFluiddRespondInfo("json_data['mode']=%d" % (json_data['mode']))
                    self.G_PhrozenFluiddRespondInfo("json_data['nc1']=%d" % (json_data['nc1']))
            elif self.G_ImageId==31:
                self.G_PhrozenFluiddRespondInfo("镜像Id==31：ARCO300-phrozen-RK3308-STM32F407VET6-I31")
                with open('/home/prz/hdlDat/Phrozen_Dev.json', 'r', encoding='utf-8') as file:
                    FileRead = file.read()
                    self.G_PhrozenFluiddRespondInfo("读取json文件")
                    # 解析JSON数据
                    json_data = json.loads(FileRead)
                    self.G_PhrozenFluiddRespondInfo("json_data['mode']=%d" % (json_data['mode']))
                    self.G_PhrozenFluiddRespondInfo("json_data['nc1']=%d" % (json_data['nc1']))
            elif self.G_ImageId==-1:
                self.G_PhrozenFluiddRespondInfo("镜像Id==-1，默认：ARCO300-MKS-RK3328-STM32F407VET6-I16")
                with open('/home/mks/hdlDat/Phrozen_Dev.json', 'r', encoding='utf-8') as file:
                    FileRead = file.read()
                    self.G_PhrozenFluiddRespondInfo("读取json文件")
                    # 解析JSON数据
                    json_data = json.loads(FileRead)
                    self.G_PhrozenFluiddRespondInfo("json_data['mode']=%d" % (json_data['mode']))
                    self.G_PhrozenFluiddRespondInfo("json_data['nc1']=%d" % (json_data['nc1']))
            else:
                self.G_PhrozenFluiddRespondInfo("镜像Id读不到，默认：ARCO300-MKS-RK3328-STM32F407VET6-I16")
                with open('/home/mks/hdlDat/Phrozen_Dev.json', 'r', encoding='utf-8') as file:
                    FileRead = file.read()
                    self.G_PhrozenFluiddRespondInfo("读取json文件")
                    # 解析JSON数据
                    json_data = json.loads(FileRead)
                    self.G_PhrozenFluiddRespondInfo("json_data['mode']=%d" % (json_data['mode']))
                    self.G_PhrozenFluiddRespondInfo("json_data['nc1']=%d" % (json_data['nc1']))
        except:
            self.G_PhrozenFluiddRespondInfo("except")



    ####################################
    #函数名称：
    #输入参数：
    #返 回 值:
    #功能描述：蓝才刚-20230830
    ####################################
    def Cmds_PhrozenBM1(self, gcmd):
        self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_PhrozenBM1]命令='%s'" % (gcmd.get_commandline(),))

        self.G_PhrozenFluiddRespondInfo("%s" % (gcmd.get_commandline(),))

        #lancaigang250327：进入多色换料之前，不允许AMS多色暂停
        self.ManualCmdFlag=True
        self.G_PhrozenFluiddRespondInfo("self.ManualCmdFlag=True")

        #  #lancaigang250514：读取json文件，获取单色续料配置和通道线材颜色配对
        # #/home/prz/klipper/klippy/extras/phrozen_dev/serial-screen/test.json
        # self.Cmds_GetUartScreenCfg()

    ####################################
    #函数名称：
    #输入参数：
    #返 回 值:
    #功能描述：蓝才刚-20230830
    ####################################
    def Cmds_PhrozenBM0(self, gcmd):
        self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_PhrozenBM0]命令='%s'" % (gcmd.get_commandline(),))

        self.G_PhrozenFluiddRespondInfo("%s" % (gcmd.get_commandline(),))
        #lancaigang250327：进入多色换料之前，不允许AMS多色暂停
        self.ManualCmdFlag=True
        self.G_PhrozenFluiddRespondInfo("self.ManualCmdFlag=True")

        #  #lancaigang250514：读取json文件，获取单色续料配置和通道线材颜色配对
        # #/home/prz/klipper/klippy/extras/phrozen_dev/serial-screen/test.json
        # self.Cmds_GetUartScreenCfg()
    ####################################
    #函数名称：
    #输入参数：
    #返 回 值:
    #功能描述：蓝才刚-20230830
    ####################################
    #PRZ_PRINT_START
    def Cmds_PrzPrintStart(self, gcmd):
        self.G_PhrozenFluiddRespondInfo("[(cmds.python)CmdsPrzPrintStart]命令='%s'" % (gcmd.get_commandline(),))

        self.G_PhrozenFluiddRespondInfo("%s" % (gcmd.get_commandline(),))

        # #lancaigang250514：读取json文件，获取单色续料配置和通道线材颜色配对
        # #/home/prz/klipper/klippy/extras/phrozen_dev/serial-screen/test.json
        # self.Cmds_GetUartScreenCfg()

    ####################################
    #函数名称：
    #输入参数：
    #返 回 值:
    #功能描述：蓝才刚-20230830
    ####################################
    def Cmds_HomingOverrideEnd(self, gcmd):
        self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_HomingOverrideEnd]命令='%s'" % (gcmd.get_commandline(),))

        self.G_PhrozenFluiddRespondInfo("%s" % (gcmd.get_commandline(),))

        # #lancaigang250514：读取json文件，获取单色续料配置和通道线材颜色配对
        # #/home/prz/klipper/klippy/extras/phrozen_dev/serial-screen/test.json
        # self.Cmds_GetUartScreenCfg()


    ####################################
    #函数名称：
    #输入参数：
    #返 回 值:
    #功能描述：蓝才刚-20230830
    ####################################
    def Cmds_PrzPrintEnd(self, gcmd):
        self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_PrzPrintEnd]命令='%s'" % (gcmd.get_commandline(),))

        self.G_PhrozenFluiddRespondInfo("%s" % (gcmd.get_commandline(),))

####################################
    #函数名称：
    #输入参数：
    #返 回 值:
    #功能描述：蓝才刚-20230830
    ####################################
    def Cmds_PrintMode(self,mode):
        self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_PrintMode]发送命令: self.G_AMSDeviceWorkMode=%d" % self.G_AMSDeviceWorkMode)
        self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_PrintMode]发送命令: mode=%d" % mode)

        try:
            self.G_PhrozenFluiddRespondInfo("try")
            Phrozen_Dev = {"mode": self.G_AMSDeviceWorkMode, "nc1": self.G_ChangeChannelTimeoutOldChan, "nc2": self.G_ChangeChannelTimeoutNewChan,"nc3":0,"nc4":0,"nc5":0,"nc6":0}
            
            #lancaigang250724：读取系统镜像id，区分不同产品不同主板不同固件
            #lancaigang250724:读取镜像id
            self.Cmds_GetImageId()
            if self.G_ImageId==16:
                self.G_PhrozenFluiddRespondInfo("镜像Id==16：ARCO300-MKS-RK3328-STM32F407VET6-I16")
                with open('/home/mks/hdlDat/Phrozen_Dev.json', 'w') as file:
                    json.dump(Phrozen_Dev, file)
                    self.G_PhrozenFluiddRespondInfo("写入json文件")
                with open('/home/mks/hdlDat/Phrozen_Dev.json', 'r', encoding='utf-8') as file:
                    FileRead = file.read()
                    self.G_PhrozenFluiddRespondInfo("读取json文件")
                    # 解析JSON数据
                    json_data = json.loads(FileRead)
                    self.G_PhrozenFluiddRespondInfo("json_data['mode']=%d" % (json_data['mode']))
                    self.G_PhrozenFluiddRespondInfo("json_data['nc1']=%d" % (json_data['nc1']))
                    self.G_PhrozenFluiddRespondInfo("json_data['nc2']=%d" % (json_data['nc2']))
                    self.G_PhrozenFluiddRespondInfo("json_data['nc3']=%d" % (json_data['nc3']))
                    self.G_PhrozenFluiddRespondInfo("json_data['nc4']=%d" % (json_data['nc4']))
                    self.G_PhrozenFluiddRespondInfo("json_data['nc5']=%d" % (json_data['nc5']))
                    self.G_PhrozenFluiddRespondInfo("json_data['nc6']=%d" % (json_data['nc6']))
            elif self.G_ImageId==31:
                self.G_PhrozenFluiddRespondInfo("镜像Id==31：ARCO300-phrozen-RK3308-STM32F407VET6-I31")
                with open('/home/prz/hdlDat/Phrozen_Dev.json', 'w') as file:
                    json.dump(Phrozen_Dev, file)
                    self.G_PhrozenFluiddRespondInfo("写入json文件")
                with open('/home/prz/hdlDat/Phrozen_Dev.json', 'r', encoding='utf-8') as file:
                    FileRead = file.read()
                    self.G_PhrozenFluiddRespondInfo("读取json文件")
                    # 解析JSON数据
                    json_data = json.loads(FileRead)
                    self.G_PhrozenFluiddRespondInfo("json_data['mode']=%d" % (json_data['mode']))
                    self.G_PhrozenFluiddRespondInfo("json_data['nc1']=%d" % (json_data['nc1']))
                    self.G_PhrozenFluiddRespondInfo("json_data['nc2']=%d" % (json_data['nc2']))
                    self.G_PhrozenFluiddRespondInfo("json_data['nc3']=%d" % (json_data['nc3']))
                    self.G_PhrozenFluiddRespondInfo("json_data['nc4']=%d" % (json_data['nc4']))
                    self.G_PhrozenFluiddRespondInfo("json_data['nc5']=%d" % (json_data['nc5']))
                    self.G_PhrozenFluiddRespondInfo("json_data['nc6']=%d" % (json_data['nc6']))
            elif self.G_ImageId==-1:
                self.G_PhrozenFluiddRespondInfo("镜像Id==-1，默认：ARCO300-MKS-RK3328-STM32F407VET6-I16")
                with open('/home/mks/hdlDat/Phrozen_Dev.json', 'w') as file:
                    json.dump(Phrozen_Dev, file)
                    self.G_PhrozenFluiddRespondInfo("写入json文件")
                with open('/home/mks/hdlDat/Phrozen_Dev.json', 'r', encoding='utf-8') as file:
                    FileRead = file.read()
                    self.G_PhrozenFluiddRespondInfo("读取json文件")
                    # 解析JSON数据
                    json_data = json.loads(FileRead)
                    self.G_PhrozenFluiddRespondInfo("json_data['mode']=%d" % (json_data['mode']))
                    self.G_PhrozenFluiddRespondInfo("json_data['nc1']=%d" % (json_data['nc1']))
                    self.G_PhrozenFluiddRespondInfo("json_data['nc2']=%d" % (json_data['nc2']))
                    self.G_PhrozenFluiddRespondInfo("json_data['nc3']=%d" % (json_data['nc3']))
                    self.G_PhrozenFluiddRespondInfo("json_data['nc4']=%d" % (json_data['nc4']))
                    self.G_PhrozenFluiddRespondInfo("json_data['nc5']=%d" % (json_data['nc5']))
                    self.G_PhrozenFluiddRespondInfo("json_data['nc6']=%d" % (json_data['nc6']))
            else:
                self.G_PhrozenFluiddRespondInfo("镜像Id读不到，默认：ARCO300-MKS-RK3328-STM32F407VET6-I16")
                with open('/home/mks/hdlDat/Phrozen_Dev.json', 'w') as file:
                    json.dump(Phrozen_Dev, file)
                    self.G_PhrozenFluiddRespondInfo("写入json文件")
                with open('/home/mks/hdlDat/Phrozen_Dev.json', 'r', encoding='utf-8') as file:
                    FileRead = file.read()
                    self.G_PhrozenFluiddRespondInfo("读取json文件")
                    # 解析JSON数据
                    json_data = json.loads(FileRead)
                    self.G_PhrozenFluiddRespondInfo("json_data['mode']=%d" % (json_data['mode']))
                    self.G_PhrozenFluiddRespondInfo("json_data['nc1']=%d" % (json_data['nc1']))
                    self.G_PhrozenFluiddRespondInfo("json_data['nc2']=%d" % (json_data['nc2']))
                    self.G_PhrozenFluiddRespondInfo("json_data['nc3']=%d" % (json_data['nc3']))
                    self.G_PhrozenFluiddRespondInfo("json_data['nc4']=%d" % (json_data['nc4']))
                    self.G_PhrozenFluiddRespondInfo("json_data['nc5']=%d" % (json_data['nc5']))
                    self.G_PhrozenFluiddRespondInfo("json_data['nc6']=%d" % (json_data['nc6']))
        except:
            self.G_PhrozenFluiddRespondInfo("except")


    ####################################
    #函数名称：
    #输入参数：
    #返 回 值:
    #功能描述：蓝才刚-20230830
    ####################################
    #PRZ_RESTORE
    def Cmds_PrzATRestore(self, gcmd):
        self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_PrzATRestore]")

        #self.G_PhrozenFluiddRespondInfo("%s" % (gcmd.get_commandline(),))

        self.G_PhrozenFluiddRespondInfo("当前模式")
        if self.G_AMSDeviceWorkMode == AMS_WORK_MODE_UNKNOW:
            self.G_PhrozenFluiddRespondInfo("+Mode:0,unkown")
        elif self.G_AMSDeviceWorkMode == AMS_WORK_MODE_MC:
            self.G_PhrozenFluiddRespondInfo("+Mode:1,MC")
        elif self.G_AMSDeviceWorkMode == AMS_WORK_MODE_MA:
            self.G_PhrozenFluiddRespondInfo("+Mode:2,MA")
        elif self.G_AMSDeviceWorkMode == AMS_WORK_MODE_FILA_RUNOUT:
            self.G_PhrozenFluiddRespondInfo("+Mode:3,RUNOUT")
        else:
            self.G_PhrozenFluiddRespondInfo("+Mode:-1,error")


        

        #PRZ_PwrDownResumePrint
        try:
            self.G_PhrozenFluiddRespondInfo("try")

            #lancaigang250724：读取系统镜像id，区分不同产品不同主板不同固件
            #lancaigang250724:读取镜像id
            self.Cmds_GetImageId()
            if self.G_ImageId==16:
                self.G_PhrozenFluiddRespondInfo("镜像Id==16：ARCO300-MKS-RK3328-STM32F407VET6-I16")
                with open('/home/mks/hdlDat/Phrozen_Dev.json', 'r', encoding='utf-8') as file:
                    FileRead = file.read()
                    self.G_PhrozenFluiddRespondInfo("读取json文件")
                    # 解析JSON数据
                    json_data = json.loads(FileRead)
                    self.G_PhrozenFluiddRespondInfo("json_data['mode']=%d" % (json_data['mode']))
                    self.G_AMSDeviceWorkMode = json_data['mode']
                    self.G_PhrozenFluiddRespondInfo("self.G_AMSDeviceWorkMode=%d" % (self.G_AMSDeviceWorkMode))
                    self.G_PhrozenFluiddRespondInfo("json_data['nc1']=%d" % (json_data['nc1']))
                    self.G_ChangeChannelTimeoutOldChan=json_data['nc1']
                    self.G_PhrozenFluiddRespondInfo("self.G_ChangeChannelTimeoutOldChan=%d" % (self.G_ChangeChannelTimeoutOldChan))
                    self.G_PhrozenFluiddRespondInfo("json_data['nc2']=%d" % (json_data['nc2']))
                    self.G_ChangeChannelTimeoutNewChan=json_data['nc2']
                    self.G_PhrozenFluiddRespondInfo("self.G_ChangeChannelTimeoutNewChan=%d" % (self.G_ChangeChannelTimeoutNewChan))
                    self.G_PhrozenFluiddRespondInfo("json_data['nc3']=%d" % (json_data['nc3']))
                    self.G_PhrozenFluiddRespondInfo("json_data['nc4']=%d" % (json_data['nc4']))
                    self.G_PhrozenFluiddRespondInfo("json_data['nc5']=%d" % (json_data['nc5']))
                    self.G_PhrozenFluiddRespondInfo("json_data['nc6']=%d" % (json_data['nc6']))
            elif self.G_ImageId==31:
                self.G_PhrozenFluiddRespondInfo("镜像Id==31：ARCO300-phrozen-RK3308-STM32F407VET6-I31")
                with open('/home/prz/hdlDat/Phrozen_Dev.json', 'r', encoding='utf-8') as file:
                    FileRead = file.read()
                    self.G_PhrozenFluiddRespondInfo("读取json文件")
                    # 解析JSON数据
                    json_data = json.loads(FileRead)
                    self.G_PhrozenFluiddRespondInfo("json_data['mode']=%d" % (json_data['mode']))
                    self.G_AMSDeviceWorkMode = json_data['mode']
                    self.G_PhrozenFluiddRespondInfo("self.G_AMSDeviceWorkMode=%d" % (self.G_AMSDeviceWorkMode))
                    self.G_PhrozenFluiddRespondInfo("json_data['nc1']=%d" % (json_data['nc1']))
                    self.G_ChangeChannelTimeoutOldChan=json_data['nc1']
                    self.G_PhrozenFluiddRespondInfo("self.G_ChangeChannelTimeoutOldChan=%d" % (self.G_ChangeChannelTimeoutOldChan))
                    self.G_PhrozenFluiddRespondInfo("json_data['nc2']=%d" % (json_data['nc2']))
                    self.G_ChangeChannelTimeoutNewChan=json_data['nc2']
                    self.G_PhrozenFluiddRespondInfo("self.G_ChangeChannelTimeoutNewChan=%d" % (self.G_ChangeChannelTimeoutNewChan))
                    self.G_PhrozenFluiddRespondInfo("json_data['nc3']=%d" % (json_data['nc3']))
                    self.G_PhrozenFluiddRespondInfo("json_data['nc4']=%d" % (json_data['nc4']))
                    self.G_PhrozenFluiddRespondInfo("json_data['nc5']=%d" % (json_data['nc5']))
                    self.G_PhrozenFluiddRespondInfo("json_data['nc6']=%d" % (json_data['nc6']))
            elif self.G_ImageId==-1:
                self.G_PhrozenFluiddRespondInfo("镜像Id==-1，默认：ARCO300-MKS-RK3328-STM32F407VET6-I16")
                with open('/home/mks/hdlDat/Phrozen_Dev.json', 'r', encoding='utf-8') as file:
                    FileRead = file.read()
                    self.G_PhrozenFluiddRespondInfo("读取json文件")
                    # 解析JSON数据
                    json_data = json.loads(FileRead)
                    self.G_PhrozenFluiddRespondInfo("json_data['mode']=%d" % (json_data['mode']))
                    self.G_AMSDeviceWorkMode = json_data['mode']
                    self.G_PhrozenFluiddRespondInfo("self.G_AMSDeviceWorkMode=%d" % (self.G_AMSDeviceWorkMode))
                    self.G_PhrozenFluiddRespondInfo("json_data['nc1']=%d" % (json_data['nc1']))
                    self.G_ChangeChannelTimeoutOldChan=json_data['nc1']
                    self.G_PhrozenFluiddRespondInfo("self.G_ChangeChannelTimeoutOldChan=%d" % (self.G_ChangeChannelTimeoutOldChan))
                    self.G_PhrozenFluiddRespondInfo("json_data['nc2']=%d" % (json_data['nc2']))
                    self.G_ChangeChannelTimeoutNewChan=json_data['nc2']
                    self.G_PhrozenFluiddRespondInfo("self.G_ChangeChannelTimeoutNewChan=%d" % (self.G_ChangeChannelTimeoutNewChan))
                    self.G_PhrozenFluiddRespondInfo("json_data['nc3']=%d" % (json_data['nc3']))
                    self.G_PhrozenFluiddRespondInfo("json_data['nc4']=%d" % (json_data['nc4']))
                    self.G_PhrozenFluiddRespondInfo("json_data['nc5']=%d" % (json_data['nc5']))
                    self.G_PhrozenFluiddRespondInfo("json_data['nc6']=%d" % (json_data['nc6']))
            else:
                self.G_PhrozenFluiddRespondInfo("镜像Id读不到，默认：ARCO300-MKS-RK3328-STM32F407VET6-I16")
                with open('/home/mks/hdlDat/Phrozen_Dev.json', 'r', encoding='utf-8') as file:
                    FileRead = file.read()
                    self.G_PhrozenFluiddRespondInfo("读取json文件")
                    # 解析JSON数据
                    json_data = json.loads(FileRead)
                    self.G_PhrozenFluiddRespondInfo("json_data['mode']=%d" % (json_data['mode']))
                    self.G_AMSDeviceWorkMode = json_data['mode']
                    self.G_PhrozenFluiddRespondInfo("self.G_AMSDeviceWorkMode=%d" % (self.G_AMSDeviceWorkMode))
                    self.G_PhrozenFluiddRespondInfo("json_data['nc1']=%d" % (json_data['nc1']))
                    self.G_ChangeChannelTimeoutOldChan=json_data['nc1']
                    self.G_PhrozenFluiddRespondInfo("self.G_ChangeChannelTimeoutOldChan=%d" % (self.G_ChangeChannelTimeoutOldChan))
                    self.G_PhrozenFluiddRespondInfo("json_data['nc2']=%d" % (json_data['nc2']))
                    self.G_ChangeChannelTimeoutNewChan=json_data['nc2']
                    self.G_PhrozenFluiddRespondInfo("self.G_ChangeChannelTimeoutNewChan=%d" % (self.G_ChangeChannelTimeoutNewChan))
                    self.G_PhrozenFluiddRespondInfo("json_data['nc3']=%d" % (json_data['nc3']))
                    self.G_PhrozenFluiddRespondInfo("json_data['nc4']=%d" % (json_data['nc4']))
                    self.G_PhrozenFluiddRespondInfo("json_data['nc5']=%d" % (json_data['nc5']))
                    self.G_PhrozenFluiddRespondInfo("json_data['nc6']=%d" % (json_data['nc6']))

            


            try:
                self.G_PhrozenFluiddRespondInfo("[(cmds.py)Cmds_PrzATRestore]重新初始化串口1")
                self.G_SerialPort1Obj = serial.Serial(self.G_Serialport1Define, SERIAL_PORT_BAUD, timeout=3)
                #串口打开成功
                if self.G_SerialPort1Obj is not None:
                    if self.G_SerialPort1Obj.is_open:
                        self.G_SerialPort1OpenFlag = True
                        self.G_PhrozenFluiddRespondInfo("重新初始化串口1成功")
                        #lancaigang231213：打开串口
                        self.G_SerialPort1Obj.flushInput()  # clean serial write cache
                        self.G_SerialPort1Obj.flush()
                        self.G_PhrozenFluiddRespondInfo("串口1清空")
                        self.G_PhrozenFluiddRespondInfo("重新注册串口1回调函数")
                        self.G_SerialPort1RecvTimmer = self.G_PhrozenReactor.register_timer(self.Device_TimmerUart1Recv, self.G_PhrozenReactor.NOW)
            except:
                self.G_PhrozenFluiddRespondInfo("未能打开tty1口，请检查USB口或重启尝试")
                self.G_SerialPort1OpenFlag = False

            try:
                self.G_PhrozenFluiddRespondInfo("[(cmds.py)Cmds_PrzATRestore]重新初始化串口2")
                self.G_SerialPort2Obj = serial.Serial(self.G_Serialport2Define, SERIAL_PORT_BAUD, timeout=3)
                #串口打开成功
                if self.G_SerialPort2Obj is not None:
                    if self.G_SerialPort2Obj.is_open:
                        self.G_SerialPort2OpenFlag = True
                        self.G_PhrozenFluiddRespondInfo("重新初始化串口2成功")
                        self.G_SerialPort2Obj.flushInput()  # clean serial write cache
                        self.G_SerialPort2Obj.flush()
                        self.G_PhrozenFluiddRespondInfo("串口2清空")
                        self.G_PhrozenFluiddRespondInfo("重新注册串口2回调函数")
                        self.G_SerialPort2RecvTimmer = self.G_PhrozenReactor.register_timer(self.Device_TimmerUart2Recv, self.G_PhrozenReactor.NOW)
            except:
                self.G_PhrozenFluiddRespondInfo("未能打开tty2口，请检查USB口或重启尝试")
                self.G_SerialPort2OpenFlag = False


            #lancaigang250619:检查AMS是否重新连接成功
            self.Cmds_USBConnectErrorCheck()
            #lancaigang240416:
            if self.G_SerialPort1OpenFlag == True:
                self.G_PhrozenFluiddRespondInfo("串口1发送命令：AT+RESTORE")
                self.Cmds_AMSSerial1Send("AT+RESTORE")
                
            #lancaigang241030:
            if self.G_SerialPort2OpenFlag == True:
                self.G_PhrozenFluiddRespondInfo("串口2发送命令：AT+RESTORE")
                self.Cmds_AMSSerial2Send("AT+RESTORE")
                

            self.G_ProzenToolhead.dwell(2)


            

            self.G_PhrozenFluiddRespondInfo("当前模式")
            if self.G_AMSDeviceWorkMode == AMS_WORK_MODE_UNKNOW:
                self.G_PhrozenFluiddRespondInfo("+Mode:0,unkown")



            elif self.G_AMSDeviceWorkMode == AMS_WORK_MODE_MC:
                self.G_PhrozenFluiddRespondInfo("+Mode:1,MC")
                #lancaigang250607：打印状态；1-退料中；2-进料中；3-打印中；4-暂停
                #self.G_KlipperPrintStatus = 3
                if self.G_SerialPort1OpenFlag == False and self.G_SerialPort2OpenFlag == False:
                    self.G_PhrozenFluiddRespondInfo("无法连接AMS，暂停")
                    if self.G_KlipperInPausing == False:
                        self.G_PhrozenFluiddRespondInfo("不在暂停中，允许新的暂停")
                        self.Cmds_PhrozenKlipperPauseNoneCmdToSTM32(None)
                        self.G_KlipperIfPaused = True
                        #self.Cmds_PhrozenKlipperPauseNoneCmdToSTM32(None)
                        self.STM32ReprotPauseFlag=1
                        #lancaigang231202：P1 C?自动换料时，如果第1次通道就进料异常暂停，如果要恢复，也继续从第1次通道开始
                        self.G_ChangeChannelFirstFilaFlag=True
                        self.G_PhrozenFluiddRespondInfo("+PAUSE:g,%d,%d" % (self.G_ChangeChannelTimeoutOldChan,self.G_ChangeChannelTimeoutNewChan))
                        self.G_PauseToLCDString="+PAUSE:g,%d,%d" % (self.G_ChangeChannelTimeoutOldChan,self.G_ChangeChannelTimeoutNewChan)
                    else:
                        self.G_PhrozenFluiddRespondInfo("暂停中，不允许新的暂停")


            elif self.G_AMSDeviceWorkMode == AMS_WORK_MODE_MA:
                self.G_PhrozenFluiddRespondInfo("+Mode:2,MA")
                self.G_P0M2MAStartPrintFlag=1
                #self.G_ToolheadFirstInputFila=False
                #self.P0M3FilaRunoutSpittingFinished=True
                if self.G_ToolheadIfHaveFilaFlag:
                    self.G_PhrozenFluiddRespondInfo("有线材，可以继续打印")
                    #lancaigang250607：打印状态；1-退料中；2-进料中；3-打印中；4-暂停
                    self.G_KlipperPrintStatus= 3
                    #lancaigang250522：
                    self.G_PhrozenFluiddRespondInfo("外部宏命令-PG108")
                    #lancaigang251120：进入吐料，添加标志位，防止PG108吐料过程中喷头霍尔没有线材暂停，导致暂停位置在吐料区，恢复的时候会撞到吐料盒；
                    self.G_PG108Ingoing=1
                    command_string = """
                        PG108
                        """
                    self.G_PhrozenGCode.run_script_from_command(command_string)
                    self.G_PG108Ingoing=0
                    self.G_PhrozenFluiddRespondInfo("外部宏命令-PG108；command_string='%s'" % command_string)

                    #lancaigang250607:
                    self.G_PhrozenFluiddRespondInfo("可以恢复，STM32打印中快速报错")
                    self.G_KlipperQuickPause = True
                    # #lancaigang250427：
                    # if self.G_SerialPort1OpenFlag == True:
                    #     self.Cmds_AMSSerial1Send("AT+EBLOCKEND")
                    #     self.G_PhrozenFluiddRespondInfo("串口1-AMS结束计时缓冲器满时间")
                    # if self.G_SerialPort2OpenFlag == True:
                    #     self.Cmds_AMSSerial2Send("AT+EBLOCKEND")
                    #     self.G_PhrozenFluiddRespondInfo("串口2-AMS结束计时缓冲器满时间")
                    # #self.G_ProzenToolhead.dwell(1.5)
                else:
                    self.G_PhrozenFluiddRespondInfo("无线材，需要暂停等待")
                    # self.G_PhrozenFluiddRespondInfo("外部宏命令-RESUME")
                    # command = """
                    # RESUME
                    # """
                    # self.G_PhrozenGCode.run_script_from_command(command)
                    # self.G_PhrozenFluiddRespondInfo("调用宏命令:command=%s" % (command))
                    #lancaigang240125：封装函数
                    self.Cmds_PhrozenKlipperResumeCommon()

                    #lancaigang250522：
                    self.G_PhrozenFluiddRespondInfo("外部宏命令-PG109-升温")
                    command_string = """
                        PG109
                        """
                    self.G_PhrozenGCode.run_script_from_command(command_string)
                    self.G_PhrozenFluiddRespondInfo("外部宏命令-PG109-升温；command_string='%s'" % command_string)

                    


                    

                    if self.G_KlipperInPausing == False:
                        self.G_PhrozenFluiddRespondInfo("不在暂停中，允许新的暂停")
                        #lancaigang250607:
                        #self.G_PhrozenFluiddRespondInfo("启用快速暂停")
                        #self.G_KlipperQuickPause = True
                        #klipper主动暂停
                        self.Cmds_PhrozenKlipperPauseMAToSTM32(None)
                    else:
                        self.G_PhrozenFluiddRespondInfo("暂停中，不允许新的暂停")




                    self.G_PhrozenFluiddRespondInfo("+PAUSE:4,%d,%d" % (self.G_ChangeChannelTimeoutOldChan,self.G_ChangeChannelTimeoutNewChan))

                    # if self.G_SerialPort1OpenFlag==True or self.G_SerialPort2OpenFlag==True:
                    #     self.G_PhrozenFluiddRespondInfo("喷头无线材，有AMS多色，执行P8完整进料过程")
                    #     #lancaigang241106：
                    #     self.G_P0M2MAStartPrintFlag=0

                    #     #lancaigang250522：不允许M3断料检测
                    #     self.G_IfChangeFilaOngoing = True

                    #     #lancaigang241106：
                    #     self.Cmds_CmdP8(gcmd)
                    #     #lancaigang241106:喷头成功进料
                    #     if self.G_P0M2MAStartPrintFlag==1:
                    #         #lancaigang250607:
                    #         self.G_PhrozenFluiddRespondInfo("可以恢复，STM32打印中快速报错")
                    #         self.G_KlipperQuickPause = True
                    #         self.G_PhrozenFluiddRespondInfo("喷头有线材，恢复")
                    #         #lancaigang240125：封装函数
                    #         self.Cmds_PhrozenKlipperResumeCommon()
                    #     else:
                    #         self.G_KlipperQuickPause = False
                    #         self.G_PhrozenFluiddRespondInfo("喷头无线材，续料继续暂停")
                    #         if self.G_KlipperIfPaused == False:
                    #             self.Cmds_PhrozenKlipperPauseMAToSTM32(None)
                    #             self.G_KlipperIfPaused=True
                    #             #self.G_PhrozenFluiddRespondInfo("+PAUSE:b,%d" % self.G_ChangeChannelTimeoutNewChan)
                    #             self.G_PhrozenFluiddRespondInfo("+PAUSE:4,%d,%d" % (self.G_ChangeChannelTimeoutOldChan,self.G_ChangeChannelTimeoutNewChan))
                    #         else:
                    #             self.G_PhrozenFluiddRespondInfo("已经暂停，不用重复暂停")
                    # else:
                    #     self.G_KlipperQuickPause = False
                    #     self.G_PhrozenFluiddRespondInfo("喷头无线材，没有AMS多色，继续暂停")
                    #     self.Cmds_PhrozenKlipperPauseMAToSTM32(None)
                    #     #无线材继续暂停
                    #     self.G_KlipperIfPaused=True
                    #     #lancaigang250521:有AMS多色
                    #     #if self.G_AMSDevice1IfNormal==True or self.G_AMSDevice2IfNormal==True:
                    #     self.G_PhrozenFluiddRespondInfo("+PAUSE:4,%d,%d" % (self.G_ChangeChannelTimeoutOldChan,self.G_ChangeChannelTimeoutNewChan))
                    #     #else:
                    #     #self.G_PhrozenFluiddRespondInfo("+PAUSE:b,%d,%d" % (self.G_ChangeChannelTimeoutOldChan,self.G_ChangeChannelTimeoutNewChan))




            elif self.G_AMSDeviceWorkMode == AMS_WORK_MODE_FILA_RUNOUT:
                self.G_PhrozenFluiddRespondInfo("+Mode:3,RUNOUT")
                self.G_P0M3Flag = True
                #self.G_ToolheadFirstInputFila = True
                #lancaigang240415：喷头有线材，第一次不用吐料
                #self.G_P0M3ToolheadHaveFilaNotSpittingFlag = True
                #self.P0M3FilaRunoutSpittingFinished==True:#吐料完成

                if self.G_ToolheadIfHaveFilaFlag:
                    self.G_PhrozenFluiddRespondInfo("有线材，可以继续打印")
                    self.G_PhrozenFluiddRespondInfo("外部宏命令-PG108")
                    #lancaigang251120：进入吐料，添加标志位，防止PG108吐料过程中喷头霍尔没有线材暂停，导致暂停位置在吐料区，恢复的时候会撞到吐料盒；
                    self.G_PG108Ingoing=1
                    command_string = """
                        PG108
                        """
                    self.G_PhrozenGCode.run_script_from_command(command_string)
                    self.G_PG108Ingoing=0
                    self.G_PhrozenFluiddRespondInfo("外部宏命令-PG108；command_string='%s'" % command_string)

                    #lancaigang250607:
                    self.G_PhrozenFluiddRespondInfo("可以恢复，STM32打印中快速报错")
                    #self.G_KlipperQuickPause = True
                    # #lancaigang250427：
                    # if self.G_SerialPort1OpenFlag == True:
                    #     self.Cmds_AMSSerial1Send("AT+EBLOCKEND")
                    #     self.G_PhrozenFluiddRespondInfo("串口1-AMS结束计时缓冲器满时间")
                    # if self.G_SerialPort2OpenFlag == True:
                    #     self.Cmds_AMSSerial2Send("AT+EBLOCKEND")
                    #     self.G_PhrozenFluiddRespondInfo("串口2-AMS结束计时缓冲器满时间")
                    # #self.G_ProzenToolhead.dwell(1.5)
                else:
                    self.G_PhrozenFluiddRespondInfo("无线材，需要暂停等待")
                    # self.G_PhrozenFluiddRespondInfo("外部宏命令-RESUME")
                    # command = """
                    # RESUME
                    # """
                    # self.G_PhrozenGCode.run_script_from_command(command)
                    # self.G_PhrozenFluiddRespondInfo("调用宏命令:command=%s" % (command))
                    #lancaigang240125：封装函数
                    self.Cmds_PhrozenKlipperResumeCommon()

                    #lancaigang250522：
                    self.G_PhrozenFluiddRespondInfo("外部宏命令-PG109-升温")
                    command_string = """
                        PG109
                        """
                    self.G_PhrozenGCode.run_script_from_command(command_string)
                    self.G_PhrozenFluiddRespondInfo("外部宏命令-PG109-升温；command_string='%s'" % command_string)


                    if self.G_KlipperInPausing == False:
                        self.G_PhrozenFluiddRespondInfo("不在暂停中，允许新的暂停")
                        #lancaigang250607:
                        #self.G_PhrozenFluiddRespondInfo("启用快速暂停")
                        #self.G_KlipperQuickPause = True
                        #klipper主动暂停
                        self.Cmds_PhrozenKlipperPauseMAToSTM32(None)
                    else:
                        self.G_PhrozenFluiddRespondInfo("暂停中，不允许新的暂停")
                    



                    self.G_PhrozenFluiddRespondInfo("+PAUSE:b,%d,%d" % (self.G_ChangeChannelTimeoutOldChan,self.G_ChangeChannelTimeoutNewChan))

                    # if self.G_SerialPort1OpenFlag==True or self.G_SerialPort2OpenFlag==True:
                    #     self.G_PhrozenFluiddRespondInfo("喷头无线材，有AMS多色，执行P8完整进料过程")
                    #     #lancaigang241106：
                    #     self.G_P0M2MAStartPrintFlag=0

                    #     #lancaigang250522：不允许M3断料检测
                    #     self.G_IfChangeFilaOngoing = True

                    #     #lancaigang241106：
                    #     self.Cmds_CmdP8(gcmd)
                    #     #lancaigang241106:喷头成功进料
                    #     if self.G_P0M2MAStartPrintFlag==1:
                    #         #lancaigang250607:
                    #         self.G_PhrozenFluiddRespondInfo("可以恢复，STM32打印中快速报错")
                    #         self.G_KlipperQuickPause = True
                    #         self.G_PhrozenFluiddRespondInfo("喷头有线材，恢复")
                    #         #lancaigang240125：封装函数
                    #         self.Cmds_PhrozenKlipperResumeCommon()
                    #     else:
                    #         self.G_KlipperQuickPause = False
                    #         self.G_PhrozenFluiddRespondInfo("喷头无线材，续料继续暂停")
                    #         if self.G_KlipperIfPaused == False:
                    #             self.Cmds_PhrozenKlipperPauseMAToSTM32(None)
                    #             self.G_KlipperIfPaused=True
                    #             #self.G_PhrozenFluiddRespondInfo("+PAUSE:b,%d" % self.G_ChangeChannelTimeoutNewChan)
                    #             self.G_PhrozenFluiddRespondInfo("+PAUSE:b,%d,%d" % (self.G_ChangeChannelTimeoutOldChan,self.G_ChangeChannelTimeoutNewChan))
                    #         else:
                    #             self.G_PhrozenFluiddRespondInfo("已经暂停，不用重复暂停")
                    # else:
                    #     self.G_KlipperQuickPause = False
                    #     self.G_PhrozenFluiddRespondInfo("喷头无线材，没有AMS多色，继续暂停")
                    #     self.Cmds_PhrozenKlipperPauseMAToSTM32(None)
                    #     #无线材继续暂停
                    #     self.G_KlipperIfPaused=True
                    #     #lancaigang250521:有AMS多色
                    #     #if self.G_AMSDevice1IfNormal==True or self.G_AMSDevice2IfNormal==True:
                    #     self.G_PhrozenFluiddRespondInfo("+PAUSE:b,%d,%d" % (self.G_ChangeChannelTimeoutOldChan,self.G_ChangeChannelTimeoutNewChan))
                    #     #else:
                    #     #self.G_PhrozenFluiddRespondInfo("+PAUSE:b,%d,%d" % (self.G_ChangeChannelTimeoutOldChan,self.G_ChangeChannelTimeoutNewChan))

            else:
                self.G_PhrozenFluiddRespondInfo("+Mode:-1,error")

        except:
            self.G_PhrozenFluiddRespondInfo("except")





    ####################################
    #函数名称：
    #输入参数：
    #返 回 值:
    #功能描述：蓝才刚-20230830
    ####################################
    def Cmds_PrzATIdle(self, gcmd):
        self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_PrzATIdle]命令='%s'" % (gcmd.get_commandline(),))

        self.G_PhrozenFluiddRespondInfo("%s" % (gcmd.get_commandline(),))
        #lancaigang250619:检查AMS是否重新连接成功
        self.Cmds_USBConnectErrorCheck()
        #lancaigang240416:
        if self.G_SerialPort1OpenFlag == True:
            self.Cmds_AMSSerial1Send("AT+IDLE")
            self.G_PhrozenFluiddRespondInfo("串口1发送命令：AT+IDLE")
        #lancaigang241030:
        if self.G_SerialPort2OpenFlag == True:
            self.Cmds_AMSSerial2Send("AT+IDLE")
            self.G_PhrozenFluiddRespondInfo("串口2发送命令：AT+IDLE")

    ####################################
    #函数名称：
    #输入参数：
    #返 回 值:
    #功能描述：蓝才刚-20230830
    ####################################
    def Cmds_MARetryInFila(self, gcmd):
        self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_MARetryInFila]")


        self.G_IfChangeFilaOngoing= True


        #lancaigang250522：
        self.G_PhrozenFluiddRespondInfo("外部宏命令-PG109-升温")
        command_string = """
            PG109
            """
        self.G_PhrozenGCode.run_script_from_command(command_string)
        self.G_PhrozenFluiddRespondInfo("外部宏命令-PG109-升温；command_string='%s'" % command_string)
        self.IfDoPG102Flag=True


        #lancaigang231228：需等待stm32执行FA后，喷头检测到线材才开始打印
        #置位标签
        Lo_ChangeChannelIfSuccess = False
        #lancaigang250607：打印状态；1-退料中；2-进料中；3-打印中；4-暂停
        self.G_KlipperPrintStatus= 2
        #lancaigang20231013：超时时间
        #lancaigang231114：不在printer.cfg配置文件更改换料超时时间，这里直接更改timeout
        #循环检测第2次进料的线材是否到喷头
        for i in range(CHANGE_CHANNEL_WAIT_TIMEOUT+50):#大概130秒
            # self.G_XBasePosition+=2
            # self.G_YBasePosition+=2
            #lancaigang231202：如果STM32主动上报暂停，需要klipper暂停
            if self.STM32ReprotPauseFlag==1:
                self.G_ChangeChannelFirstFilaFlag=True
                self.G_PhrozenFluiddRespondInfo("等待换料期间，stm32主动上报了暂停")
                Lo_ChangeChannelIfSuccess = False


                Lo_PauseStatus=self.G_PhrozenPrinterCancelPauseResume.get_status(None)
                self.G_PhrozenFluiddRespondInfo("当前暂停状态-Lo_PauseStatus='%s'" % Lo_PauseStatus)
                self.G_PhrozenFluiddRespondInfo("Lo_PauseStatus['is_paused']='%s'" % Lo_PauseStatus['is_paused'])
                #// 当前暂停状态-Lo_PauseStatus='{'is_paused': True}'
                if Lo_PauseStatus['is_paused'] == True:
                    self.G_PhrozenFluiddRespondInfo("已是暂停状态")
                else:
                    self.G_PhrozenFluiddRespondInfo("未暂停状态")

                break
            
            #lancaigang231216：
            if self.G_XBasePosition==0 and self.G_YBasePosition==0:
                self.G_PhrozenFluiddRespondInfo("等待换料期间，基坐标XY为0")
            else:
                #lancaigang231216：恢复的时候，需要来回运动防止漏料生成一个坑
                #lancaigang231214：等待区域基点X Y以W H长方形步长来回移动，实现吐料功能
                command_string = """
                    G90
                    G1 X%.03f Y%.03f F1000
                    """ % (
                    self.G_XBasePosition+(i%2),
                    self.G_YBasePosition+(i%2)
                )
                #lancaigang231129：缓慢来回移动
                self.G_PhrozenGCode.run_script_from_command(command_string)
                self.G_PhrozenFluiddRespondInfo("等待换料期间，基坐标XY为P9配置")


            #lancaigang20231013：改为4秒延时
            #lancaigang231115：改为1s
            self.G_ProzenToolhead.dwell(1)
            #lancaigang240222：不能使用time.sleep，会导致异常codedump
            #time.sleep(1)



            # self.G_PhrozenFluiddRespondInfo("外部宏命令-PG110；STM32进料之后，klipper开始吐料接住进料")
            # command_string = """
            # PG110
            # """
            # self.G_PhrozenGCode.run_script_from_command(command_string)
            # self.G_PhrozenFluiddRespondInfo("command_string='%s'" % command_string)




            #检测新通道线材进料，是否有线材到喷头
            if self.G_ToolheadIfHaveFilaFlag:
                Lo_ChangeChannelIfSuccess = True
                break



        #正常换料
        if Lo_ChangeChannelIfSuccess==True:
            self.G_PhrozenFluiddRespondInfo("换料成功")
            self.G_IfChangeFilaOngoing= False

            #lancaigang240108：喷头有线材，可以恢复
            self.G_M2MAModeResumeFlag=True
            
            #lancaigang241106：成功进料
            self.G_P0M2MAStartPrintFlag=1

            #lancaigang250607：打印状态；1-退料中；2-进料中；3-打印中；4-暂停
            self.G_KlipperPrintStatus= 3

            self.G_PauseToLCDString=""


            # #lancaigang250611：
            # self.G_PhrozenFluiddRespondInfo("外部宏命令-PG108-升温吐料擦嘴")
            # command_string = """
            #     PG108
            #     """
            # self.G_PhrozenGCode.run_script_from_command(command_string)

            #lancaigang250607:
            self.G_PhrozenFluiddRespondInfo("可以恢复，STM32打印中快速报错")
            self.G_KlipperQuickPause = True
            # #lancaigang250427：
            # if self.G_SerialPort1OpenFlag == True:
            #     self.Cmds_AMSSerial1Send("AT+EBLOCKEND")
            #     self.G_PhrozenFluiddRespondInfo("串口1-AMS结束计时缓冲器满时间")
            # if self.G_SerialPort2OpenFlag == True:
            #     self.Cmds_AMSSerial2Send("AT+EBLOCKEND")
            #     self.G_PhrozenFluiddRespondInfo("串口2-AMS结束计时缓冲器满时间")
            # #self.G_ProzenToolhead.dwell(1.5)


            return
        
        self.G_PhrozenFluiddRespondInfo("换料失败")
        # expire:超时时间,
        # 单位秒(默认60)
        # A0:忽略超时,继续打印(默认)
        # A1:超时后终止打印
        #换料超时
        # lancaigang20231013：A0:忽略超时
        if self.G_DictChangeChannelWaitAreaParam["A"] == 0:
            #lancaigang231209：stm32主动上报则不上报9
            if self.G_KlipperIfPaused==False:
                self.G_PhrozenFluiddRespondInfo("换料超时100s，暂停")
                
                #lancaigang250702：
                if self.G_KlipperInPausing == False:
                    self.G_PhrozenFluiddRespondInfo("不在暂停中，允许新的暂停")

                    #lancaigang240104：不用发送stm32暂停
                    #klipper主动暂停
                    self.Cmds_PhrozenKlipperPauseM2M3ToSTM32(None)

                    #self.G_PhrozenFluiddRespondInfo("+PAUSE:4,%d" % self.G_ChangeChannelTimeoutNewChan)
                    self.G_PhrozenFluiddRespondInfo("+PAUSE:4,%d,%d" % (self.G_ChangeChannelTimeoutOldChan,self.G_ChangeChannelTimeoutNewChan))
                else:
                    self.G_PhrozenFluiddRespondInfo("暂停中，不允许新的暂停")

            #lancaigang240123：如果已经是暂停状态，不允许再暂停
            else:
                self.G_PhrozenFluiddRespondInfo("已经暂停了，不允许重复暂停")

            #lancaigang231202：P1 C?自动换料时，如果第1次通道就进料异常暂停，如果要恢复，也继续从第1次通道开始
            self.G_ChangeChannelFirstFilaFlag=True
            self.G_IfChangeFilaOngoing= False

            #lancaigang241106：进料失败
            self.G_P0M2MAStartPrintFlag=0

            #lancaigang250607：打印状态；1-退料中；2-进料中；3-打印中；4-暂停
            self.G_KlipperPrintStatus= -1

            return
        
        #正常换料；Action正常
        if self.G_DictChangeChannelWaitAreaParam["A"] == 1:
            pass

        self.G_IfChangeFilaOngoing= False


    ####################################
    #函数名称：
    #输入参数：
    #返 回 值:
    #功能描述：蓝才刚-20230830
    ####################################
    # P114 S；无参数时查询设备详细状态,有参数S时查询简单状态响应说明见后章节；"SB"；
    # P114 S；无参数时查询设备详细状态,有参数S时查询简单状态响应说明见后章节 ；"SD"；
    def Cmds_CmdP114(self, gcmd):
        _ = gcmd

        if gcmd is None:
            self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_CmdP114]命令P114-None")
        if gcmd is not None:
            self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_CmdP114]命令='%s'" % (gcmd.get_commandline(),))

            #获取P114命令参数
            params = gcmd.get_command_parameters()

        self.G_PhrozenFluiddRespondInfo("=====self.G_ChangeChannelTimeoutOldChan=%d" % self.G_ChangeChannelTimeoutOldChan)
        self.G_PhrozenFluiddRespondInfo("=====self.G_ChangeChannelTimeoutNewChan=%d" % self.G_ChangeChannelTimeoutNewChan)

        #lancaigang240510：
        self.G_PhrozenFluiddRespondInfo("+P114:0")
        
        self.G_PhrozenFluiddRespondInfo("当前模式")
        if self.G_AMSDeviceWorkMode == AMS_WORK_MODE_UNKNOW:
            self.G_PhrozenFluiddRespondInfo("+Mode:0,unkown")
        elif self.G_AMSDeviceWorkMode == AMS_WORK_MODE_MC:
            self.G_PhrozenFluiddRespondInfo("+Mode:1,MC")
        elif self.G_AMSDeviceWorkMode == AMS_WORK_MODE_MA:
            self.G_PhrozenFluiddRespondInfo("+Mode:2,MA")
        elif self.G_AMSDeviceWorkMode == AMS_WORK_MODE_FILA_RUNOUT:
            self.G_PhrozenFluiddRespondInfo("+Mode:3,RUNOUT")
        else:
            self.G_PhrozenFluiddRespondInfo("+Mode:-1,error")


        #解锁
        self.Base_AMSSerialCmdUnlock()




        self.G_PhrozenFluiddRespondInfo("self.G_CancelFlag='%s'" % self.G_CancelFlag)
        #lancaigang250712:
        #self.Cmds_CmdP29(None)


        #lancaigang240511：恢复的时候，都初始化一下串口，防止热插拔AMS导致的串口通讯异常
        try:
            self.G_PhrozenFluiddRespondInfo("[(cmds.py)Cmds_CmdP114]重新初始化串口1")
            self.G_SerialPort1Obj = serial.Serial(self.G_Serialport1Define, SERIAL_PORT_BAUD, timeout=3)
            #串口打开成功
            if self.G_SerialPort1Obj is not None:
                if self.G_SerialPort1Obj.is_open:
                    self.G_SerialPort1OpenFlag = True
                    self.G_PhrozenFluiddRespondInfo("重新初始化串口1成功")
                    #lancaigang231213：打开串口
                    self.G_SerialPort1Obj.flushInput()  # clean serial write cache
                    self.G_SerialPort1Obj.flush()
                    self.G_PhrozenFluiddRespondInfo("串口1清空")
                    self.G_PhrozenFluiddRespondInfo("重新注册串口1回调函数")
                    self.G_SerialPort1RecvTimmer = self.G_PhrozenReactor.register_timer(self.Device_TimmerUart1Recv, self.G_PhrozenReactor.NOW)
        except:
            self.G_PhrozenFluiddRespondInfo("未能打开tty1口，请检查USB口或重启尝试")

        try:
            self.G_PhrozenFluiddRespondInfo("[(cmds.py)Cmds_CmdP114]重新初始化串口2")
            self.G_SerialPort2Obj = serial.Serial(self.G_Serialport2Define, SERIAL_PORT_BAUD, timeout=3)
            #串口打开成功
            if self.G_SerialPort2Obj is not None:
                if self.G_SerialPort2Obj.is_open:
                    self.G_SerialPort2OpenFlag = True
                    self.G_PhrozenFluiddRespondInfo("重新初始化串口2成功")
                    self.G_SerialPort2Obj.flushInput()  # clean serial write cache
                    self.G_SerialPort2Obj.flush()
                    self.G_PhrozenFluiddRespondInfo("串口2清空")
                    self.G_PhrozenFluiddRespondInfo("重新注册串口2回调函数")
                    self.G_SerialPort2RecvTimmer = self.G_PhrozenReactor.register_timer(self.Device_TimmerUart2Recv, self.G_PhrozenReactor.NOW)
        except:
            self.G_PhrozenFluiddRespondInfo("未能打开tty2口，请检查USB口或重启尝试")


        #lancaigang240524：防止粘包；清空串口数据
        self.G_ProzenToolhead.dwell(0.5)

        if self.G_SerialPort1OpenFlag==True:
            if self.G_SerialPort1Obj.is_open:
                #self.G_SerialPort1Obj.flushInput()  # clean serial write cache
                #self.G_SerialPort1Obj.flush()
                self.G_PhrozenFluiddRespondInfo("串口1已打开")

        if self.G_SerialPort2OpenFlag==True:
            if self.G_SerialPort2Obj.is_open:
                self.G_PhrozenFluiddRespondInfo("串口2已打开")

        # # 参数是S，即读取多色主板简单参数
        # if "S" in params:
        #     # #ttyUSB0串口发送并等待响应
        #     # Lo_AMSDeviceStateRspInfo = self.Cmds_AMSSerialPort1SendWaitRsp("SB", sizeof(AMSSimpleInfoBytes))
        #     # if len(Lo_AMSDeviceStateRspInfo) != sizeof(AMSSimpleInfoBytes):
        #     #     self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_CmdP114]无效响应命令 '%s'" % (gcmd.get_commandline(),))
        #     #     return

        #     # Lo_AMSDeviceStateInfo = AMSSimpleInfoBytes()
        #     # Lo_AMSDeviceStateInfo.whole[:] = bytearray(Lo_AMSDeviceStateRspInfo)
        #     # #python空字典
        #     # Lo_AMSSimpleState = {}
        #     # self.G_AMS1DeviceState["dev_id"] = Lo_AMSSimpleState["dev_id"] = Lo_AMSDeviceStateInfo.field.dev_id
        #     # self.G_AMS1DeviceState["dev_mode"] = Lo_AMSSimpleState["dev_mode"] = Lo_AMSDeviceStateInfo.field.dev_mode
        #     # self.G_AMS1DeviceState["mc_state"] = Lo_AMSSimpleState["mc_state"] = Lo_AMSDeviceStateInfo.field.mc_state
        #     # if int(Lo_AMSDeviceStateInfo.field.mc_state) is MC_STANDBY:
        #     #     self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_CmdP114]当前状态state==待机阶段==%d" % MC_STANDBY)
        #     # if int(Lo_AMSDeviceStateInfo.field.mc_state) is MC_PREPARTION:
        #     #     self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_CmdP114]当前状态state==备料停靠阶段==%d" % MC_STANDBY)
        #     # if int(Lo_AMSDeviceStateInfo.field.mc_state) is MC_CHANGING_P1:
        #     #     self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_CmdP114]当前状态state==换料阶段1==%d" % MC_CHANGING_P1)
        #     # if int(Lo_AMSDeviceStateInfo.field.mc_state) is MC_CHANGING_P2:
        #     #     self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_CmdP114]当前状态state==换料阶段2==%d" % MC_CHANGING_P2)
        #     # if int(Lo_AMSDeviceStateInfo.field.mc_state) is MC_FORCE_FEED:
        #     #     self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_CmdP114]当前状态state==换料阶段强制补料==%d" % MC_FORCE_FEED)
        #     # if int(Lo_AMSDeviceStateInfo.field.mc_state) is MC_PRINTING:
        #     #     self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_CmdP114]当前状态state==打印阶段补料==%d" % MC_PRINTING)
        #     # if int(Lo_AMSDeviceStateInfo.field.mc_state) is MC_ROLLBACK:
        #     #     self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_CmdP114]当前状态state==完全退料==%d" % MC_ROLLBACK)
        #     # if int(Lo_AMSDeviceStateInfo.field.mc_state) is MC_PARKBACK:
        #     #     self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_CmdP114]当前状态state==退料到停靠位==%d" % MC_PARKBACK)
        #     # if int(Lo_AMSDeviceStateInfo.field.mc_state) is MC_PARKALL:
        #     #     self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_CmdP114]当前状态state==全部退料到停靠位==%d" % MC_PARKALL)
        #     # if int(Lo_AMSDeviceStateInfo.field.mc_state) is MC_CLEANING:
        #     #     self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_CmdP114]当前状态state==所有线料清空==%d" % MC_CLEANING)
        #     # if int(Lo_AMSDeviceStateInfo.field.mc_state) is MC_ERR_TIMEOUT:
        #     #     self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_CmdP114]当前状态state==超时出错状态==%d" % MC_ERR_TIMEOUT)
        #     # if int(Lo_AMSDeviceStateInfo.field.mc_state) is MC_ERR_RUNOUT:
        #     #     self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_CmdP114]当前状态state==断料出错状态==%d" % MC_ERR_RUNOUT)
        #     # if int(Lo_AMSDeviceStateInfo.field.mc_state) is MC_ERR_BLOCKUP:
        #     #     self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_CmdP114]当前状态state==堵料出错状态==%d" % MC_ERR_BLOCKUP)
        #     # self.G_AMS1DeviceState["ma_state"] = Lo_AMSSimpleState["ma_state"] = Lo_AMSDeviceStateInfo.field.ma_state
        #     # # 响应数据json转换
        #     # self.G_PhrozenFluiddRespondInfo(json.dumps(Lo_AMSSimpleState))

        #     self.G_PhrozenFluiddRespondInfo("+P114:1")
        #     #self.G_P114RunFlag=0
        #     return
        
        #lancaigang250619:检查AMS是否重新连接成功
        #self.Cmds_USBConnectErrorCheck()

        #获取多色主板详细状态
        #lancaigang240430：stm32会延时上报，这里使用了withrsp，会导致time too close；所以打印过程中不允许发送P114
        #Lo_AMSDeviceStateRspInfo = self.Cmds_AMSSerialPort1SendWaitRsp("SD", sizeof(AMSDetailInfoBytes))
        #self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_CmdP114]P114阻塞串口接收: %s" % Lo_AMSDeviceStateRspInfo)
         #lancaigang240524：改为发送后异步接收
        if self.G_SerialPort1OpenFlag == True:
            self.Cmds_AMSSerial1Send("SD")
            self.G_PhrozenFluiddRespondInfo("串口1发送命令：SD")

        #lancaigang241030:
        if self.G_SerialPort2OpenFlag == True:
            self.Cmds_AMSSerial2Send("SD")
            self.G_PhrozenFluiddRespondInfo("串口2发送命令：SD")


        # if len(Lo_AMSDeviceStateRspInfo) != sizeof(AMSDetailInfoBytes):
        #     self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_CmdP114]AMS未响应，请检查AMS '%s'" % (gcmd.get_commandline(),))
        #     #lancaigang240510：
        #     self.G_PhrozenFluiddRespondInfo("+P114:-1")
        #     #self.G_P114RunFlag=0
        #     #lancaigang240412:AMS多色标签
        #     self.G_AMSDevice1IfNormal=False
        #     return
        
        # self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_CmdP114]AMS有响应")


        # #lancaigang240412:AMS多色标签
        # self.G_AMSDevice1IfNormal=True

        # Lo_AMSDeviceStateInfo = AMSDetailInfoBytes()
        # Lo_AMSDeviceStateInfo.whole[:] = bytearray(Lo_AMSDeviceStateRspInfo)
        # #python空字典
        # Lo_AMSDetailState = {}
        # self.G_AMSG_AMS1DeviceStateDeviceState["dev_id"] = Lo_AMSDetailState["dev_id"] = Lo_AMSDeviceStateInfo.field.dev_id
        # self.G_AMS1DeviceState["dev_mode"] = Lo_AMSDetailState["dev_mode"] = Lo_AMSDeviceStateInfo.field.dev_mode
        # #self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_CmdP114]缓冲器传感器线材状态(bool)==%d" % Lo_AMSDeviceStateInfo.field.cache_exist)
        # self.G_AMS1DeviceState["mc_state"] = Lo_AMSDetailState["mc_state"] = Lo_AMSDeviceStateInfo.field.mc_state
        # self.G_AMS1DeviceState["ma_state"] = Lo_AMSDetailState["ma_state"] = Lo_AMSDeviceStateInfo.field.ma_state
        # #lancaigang240524：不使用，赋值-1
        # self.G_AMS1DeviceState["active_dev_id"] = Lo_AMSDetailState["active_dev_id"] = Lo_AMSDeviceStateInfo.field.dev_id
        # self.G_AMS1DeviceState["cache_empty"] = Lo_AMSDetailState["cache_empty"] = Lo_AMSDeviceStateInfo.field.cache_empty
        # #self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_CmdP114]缓冲器传感器空状态(bool)==%d" % Lo_AMSDeviceStateInfo.field.cache_empty)
        # self.G_AMS1DeviceState["cache_full"] = Lo_AMSDetailState["cache_full"] = Lo_AMSDeviceStateInfo.field.cache_full
        # #self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_CmdP114]缓冲器传感器满状态(bool)==%d" % Lo_AMSDeviceStateInfo.field.cache_full)
        # self.G_AMS1DeviceState["cache_exist"] = Lo_AMSDetailState["cache_exist"] = Lo_AMSDeviceStateInfo.field.cache_exist
        # self.G_AMS1DeviceState["entry_state"] = Lo_AMSDetailState["entry_state"] = Lo_AMSDeviceStateInfo.field.entry_state
        # #self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_CmdP114]入口位传感器状态(bit位)==%d" % Lo_AMSDeviceStateInfo.field.entry_state)
        # self.G_AMS1DeviceState["park_state"] = Lo_AMSDetailState["park_state"] = Lo_AMSDeviceStateInfo.field.park_state
        # #self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_CmdP114]停靠位传感器状态(bit位)==%d" % Lo_AMSDeviceStateInfo.field.park_state)
        
        # # 响应数据json转换
        # self.G_PhrozenFluiddRespondInfo(json.dumps(Lo_AMSDetailState))

        #lancaigang240123：防止切片软件读取太快导致stm32粘包
        #time.sleep(1)
        #lancaigang240229：不能用time.sleep，会导致time to close
        #self.G_ProzenToolhead.dwell(0.5)
        #lancaigang240510：
        #self.G_PhrozenFluiddRespondInfo("+P114:1")
        #self.G_P114RunFlag=False

        self.G_P114RunFlag=1

        return


    ####################################
    #函数名称：
    #输入参数：
    #返 回 值:
    #功能描述：蓝才刚-20230830
    ####################################
    # P30 自动编排设备ID(用于多设备自动组网)；"I";处理自动编排设备ID命令
    def Cmds_CmdP30(self, gcmd):
        if not self.G_SerialPort1OpenFlag:
            self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_CmdP30]AMS多色未连接，请先发送P28")
            return
        
        self.G_PhrozenFluiddRespondInfo("命令='%s'" % (gcmd.get_commandline(),))

        mcu_cmd = G_DictPhrozenCmdP30["mcu_cmd"][0] + "0"
        self.Cmds_AMSSerial1Send(mcu_cmd)
        self.G_PhrozenFluiddRespondInfo("发送命令: %s" % mcu_cmd)

        logging.info("SendCmd: %s" % mcu_cmd)

    


    ####################################
    #函数名称：
    #输入参数：
    #返 回 值:
    #功能描述：蓝才刚-20230830
    ####################################
    # P29 断开连接
    def Cmds_CmdP29(self, gcmd):
        self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_CmdP29]命令")

        try:
            if self.G_SerialPort1Obj is not None:
                if self.G_SerialPort1Obj.is_open:
                    #tty1关闭
                    self.G_SerialPort1Obj.close()
        except:
            self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_CmdP29]AMS1多色未连接")
        self.G_SerialPort1OpenFlag = False
        self.G_PhrozenFluiddRespondInfo("AMS1清空")
        self.G_SerialPort1Obj=None

        try:
            if self.G_SerialPort2Obj is not None:
                if self.G_SerialPort2Obj.is_open:
                    self.G_SerialPort2Obj.close()
        except:
            self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_CmdP29]AMS2多色未连接")
        self.G_SerialPort2OpenFlag = False
        self.G_PhrozenFluiddRespondInfo("AMS2清空")
        self.G_SerialPort2Obj=None


        if self.G_SerialPort1RecvTimmer:
            #取消注册
            self.G_PhrozenReactor.unregister_timer(self.G_SerialPort1RecvTimmer)
            #清空定时器
            self.G_SerialPort1RecvTimmer = None

        #lancaigang241030
        if self.G_SerialPort2RecvTimmer:
            #取消注册
            self.G_PhrozenReactor.unregister_timer(self.G_SerialPort2RecvTimmer)
            #清空定时器
            self.G_SerialPort2RecvTimmer = None

        #lancaigang250515：
        self.G_P0M1MCNoneAMS=0
        self.G_PhrozenFluiddRespondInfo("self.G_P0M1MCNoneAMS=0")



        #lancaigang231122：使用tty之后，需要开启后台IAP升级程序hdl_zigbee_gateway
        #os.system('sh /home/prz/klipper/klippy/extras/phrozen_dev/start.sh &')
        #self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_CmdP29]sh /home/prz/klipper/klippy/extras/phrozen_dev/start.sh &")

        #self.G_ProzenToolhead.dwell(1.0)



    ####################################
    #函数名称：
    #输入参数：
    #返 回 值:
    #功能描述：蓝才刚-20230830
    ####################################
    def Cmds_GetImageId(self):
        self.G_PhrozenFluiddRespondInfo("[(dev.python)Cmds_GetImageId]")

        current_directory = os.getcwd()
        #current_directory=/home/mks/klipper
        #current_directory=/home/prz/klipper
        self.G_PhrozenFluiddRespondInfo("current_directory=%s" % (current_directory))

        #lancaigang250514：读取配置表
        try:
            self.G_PhrozenFluiddRespondInfo("try")
            
            # 打开JSON文件并读取内容
            #with open('.././hdlDat/ImageId.json', 'r', encoding='utf-8') as file:
            self.G_PhrozenFluiddRespondInfo("/etc/ImageId.json")
            with open('/etc/ImageId.json', 'r', encoding='utf-8') as file:
                ImageData = file.read()
            self.G_PhrozenFluiddRespondInfo("with open")
            #self.G_PhrozenFluiddRespondInfo("ImageData=%s" % (ImageData))
            # 解析JSON数据
            json_data = json.loads(ImageData)
            #self.G_PhrozenFluiddRespondInfo("json_data=%s" % (json_data))
            self.G_PhrozenFluiddRespondInfo("json_data['ImageId']=%d" % (json_data['ImageId']))
            self.G_ImageId= json_data['ImageId']
            self.G_PhrozenFluiddRespondInfo("self.G_ImageId=%d" % (self.G_ImageId))
            self.G_PhrozenFluiddRespondInfo("json_data['HwId']=%d" % (json_data['HwId']))
            self.HwId= json_data['HwId']
            self.G_PhrozenFluiddRespondInfo("self.HwId=%d" % (self.HwId))
            self.G_PhrozenFluiddRespondInfo("json_data['FwId']=%d" % (json_data['FwId']))
            self.G_PhrozenFluiddRespondInfo("json_data['NC0']=%d" % (json_data['NC0']))
            self.G_PhrozenFluiddRespondInfo("json_data['NC1']=%d" % (json_data['NC1']))
            self.G_PhrozenFluiddRespondInfo("json_data['NC2']=%d" % (json_data['NC2']))
            self.G_PhrozenFluiddRespondInfo("json_data['NC3']=%d" % (json_data['NC3']))
            self.G_PhrozenFluiddRespondInfo("json_data['NC4']=%d" % (json_data['NC4']))

            if self.G_ImageId==16:
                self.G_PhrozenFluiddRespondInfo("镜像Id==16：ARCO300-MKS-RK3328-STM32F407VET6-I16")
            elif self.G_ImageId==31:
                self.G_PhrozenFluiddRespondInfo("镜像Id==31：ARCO300-phrozen-RK3308-STM32F407VET6-I31")
            elif self.G_ImageId==-1:
                self.G_PhrozenFluiddRespondInfo("镜像Id==-1，默认：ARCO300-MKS-RK3328-STM32F407VET6-I16")
            else:
                self.G_PhrozenFluiddRespondInfo("镜像Id读不到，默认：ARCO300-MKS-RK3328-STM32F407VET6-I16")
        except Exception as e:
            self.G_PhrozenFluiddRespondInfo("读取文件数据异常")
            self.G_PhrozenFluiddRespondInfo("self.G_ImageId=%d" % (self.G_ImageId))
            #self.G_PhrozenFluiddRespondInfo("self.HwId=%d" % (self.HwId))


    ####################################
    #函数名称：
    #输入参数：
    #返 回 值:
    #功能描述：蓝才刚-20230830
    ####################################
    def Cmds_GetUartScreenCfg(self):
        self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_GetUartScreenCfg]")


        #lancaigang250514：读取配置表
        try:
            self.G_PhrozenFluiddRespondInfo("try")

            #lancaigang250724：读取系统镜像id，区分不同产品不同主板不同固件
            #lancaigang250724:读取镜像id
            self.Cmds_GetImageId()
            if self.G_ImageId==16:
                self.G_PhrozenFluiddRespondInfo("镜像Id==16：ARCO300-MKS-RK3328-STM32F407VET6-I16")
                # 打开JSON文件并读取内容
                with open('/home/mks/klipper/klippy/extras/phrozen_dev/serial-screen/plr_print_precfg.json', 'r', encoding='utf-8') as file:
                    UartScreenCfgData = file.read()
            elif self.G_ImageId==31:
                self.G_PhrozenFluiddRespondInfo("镜像Id==31：ARCO300-phrozen-RK3308-STM32F407VET6-I31")
                # 打开JSON文件并读取内容
                with open('/home/prz/klipper/klippy/extras/phrozen_dev/serial-screen/plr_print_precfg.json', 'r', encoding='utf-8') as file:
                    UartScreenCfgData = file.read()
            elif self.G_ImageId==-1:
                self.G_PhrozenFluiddRespondInfo("镜像Id==-1，默认：ARCO300-MKS-RK3328-STM32F407VET6-I16")
                # 打开JSON文件并读取内容
                with open('/home/mks/klipper/klippy/extras/phrozen_dev/serial-screen/plr_print_precfg.json', 'r', encoding='utf-8') as file:
                    UartScreenCfgData = file.read()
            else:
                self.G_PhrozenFluiddRespondInfo("镜像Id读不到，默认：ARCO300-MKS-RK3328-STM32F407VET6-I16")
                # 打开JSON文件并读取内容
                with open('/home/mks/klipper/klippy/extras/phrozen_dev/serial-screen/plr_print_precfg.json', 'r', encoding='utf-8') as file:
                    UartScreenCfgData = file.read()

            self.G_PhrozenFluiddRespondInfo("with open")
            # {
            # 	"Auto_Replace_state":	0,
            # 	"Chroma_Kit_state":	0,
            # 	"Chroma_Kit_num":	4,
            # 	"Chroma_Kit_access":	{
            # 		"T0":	1,
            # 		"T1":	2,
            # 		"T2":	3,
            # 		"T3":	4,
            # 		"T4":	-1,
            # 		"T5":	-1,
            # 		"T6":	-1,
            # 		"T7":	-1,
            # 		"T8":	-1,
            # 		"T9":	-1,
            # 		"T10":	-1,
            # 		"T11":	-1,
            # 		"T12":	-1,
            # 		"T13":	-1,
            # 		"T14":	-1,
            # 		"T15":	-1
            # 	}
            # }
            # 解析JSON数据
            json_data = json.loads(UartScreenCfgData)
            #print(json_data['Auto_Replace_state'])
            #print(json_data['Chroma_Kit_num'])
            self.G_PhrozenFluiddRespondInfo("json_data['Auto_Replace_state']=%d" % (json_data['Auto_Replace_state']))
            self.G_PhrozenFluiddRespondInfo("json_data['Chroma_Kit_num']=%d" % (json_data['Chroma_Kit_num']))
            self.G_PhrozenFluiddRespondInfo("json_data['Chroma_Kit_access']['T0']=%d" % (json_data['Chroma_Kit_access']['T0']))
            self.G_PhrozenFluiddRespondInfo("json_data['Chroma_Kit_access']['T1']=%d" % (json_data['Chroma_Kit_access']['T1']))
            self.G_PhrozenFluiddRespondInfo("json_data['Chroma_Kit_access']['T2']=%d" % (json_data['Chroma_Kit_access']['T2']))
            self.G_PhrozenFluiddRespondInfo("json_data['Chroma_Kit_access']['T3']=%d" % (json_data['Chroma_Kit_access']['T3']))
            self.G_PhrozenFluiddRespondInfo("json_data['Chroma_Kit_access']['T4']=%d" % (json_data['Chroma_Kit_access']['T4']))
            self.G_PhrozenFluiddRespondInfo("json_data['Chroma_Kit_access']['T5']=%d" % (json_data['Chroma_Kit_access']['T5']))
            self.G_PhrozenFluiddRespondInfo("json_data['Chroma_Kit_access']['T6']=%d" % (json_data['Chroma_Kit_access']['T6']))
            self.G_PhrozenFluiddRespondInfo("json_data['Chroma_Kit_access']['T7']=%d" % (json_data['Chroma_Kit_access']['T7']))
            self.G_PhrozenFluiddRespondInfo("json_data['Chroma_Kit_access']['T8']=%d" % (json_data['Chroma_Kit_access']['T8']))
            self.G_PhrozenFluiddRespondInfo("json_data['Chroma_Kit_access']['T9']=%d" % (json_data['Chroma_Kit_access']['T9']))
            self.G_PhrozenFluiddRespondInfo("json_data['Chroma_Kit_access']['T10']=%d" % (json_data['Chroma_Kit_access']['T10']))
            self.G_PhrozenFluiddRespondInfo("json_data['Chroma_Kit_access']['T11']=%d" % (json_data['Chroma_Kit_access']['T11']))
            self.G_PhrozenFluiddRespondInfo("json_data['Chroma_Kit_access']['T12']=%d" % (json_data['Chroma_Kit_access']['T12']))
            self.G_PhrozenFluiddRespondInfo("json_data['Chroma_Kit_access']['T13']=%d" % (json_data['Chroma_Kit_access']['T13']))
            self.G_PhrozenFluiddRespondInfo("json_data['Chroma_Kit_access']['T14']=%d" % (json_data['Chroma_Kit_access']['T14']))
            self.G_PhrozenFluiddRespondInfo("json_data['Chroma_Kit_access']['T15']=%d" % (json_data['Chroma_Kit_access']['T15']))


            self.G_AutoReplaceState = json_data['Auto_Replace_state']
            self.G_ChromaKitNum = json_data['Chroma_Kit_num']
            self.G_ChromaKitAccessT0 = json_data['Chroma_Kit_access']['T0']
            self.G_ChromaKitAccessT1 = json_data['Chroma_Kit_access']['T1']
            self.G_ChromaKitAccessT2 = json_data['Chroma_Kit_access']['T2']
            self.G_ChromaKitAccessT3 = json_data['Chroma_Kit_access']['T3']
            self.G_ChromaKitAccessT4 = json_data['Chroma_Kit_access']['T4']
            self.G_ChromaKitAccessT5 = json_data['Chroma_Kit_access']['T5']
            self.G_ChromaKitAccessT6 = json_data['Chroma_Kit_access']['T6']
            self.G_ChromaKitAccessT7 = json_data['Chroma_Kit_access']['T7']
            self.G_ChromaKitAccessT8 = json_data['Chroma_Kit_access']['T8']
            self.G_ChromaKitAccessT9 = json_data['Chroma_Kit_access']['T9']
            self.G_ChromaKitAccessT10 = json_data['Chroma_Kit_access']['T10']
            self.G_ChromaKitAccessT11 = json_data['Chroma_Kit_access']['T11']
            self.G_ChromaKitAccessT12 = json_data['Chroma_Kit_access']['T12']
            self.G_ChromaKitAccessT13 = json_data['Chroma_Kit_access']['T13']
            self.G_ChromaKitAccessT14 = json_data['Chroma_Kit_access']['T14']
            self.G_ChromaKitAccessT15 = json_data['Chroma_Kit_access']['T15']

            self.G_PhrozenFluiddRespondInfo("self.G_AutoReplaceState=%d" % (self.G_AutoReplaceState))
            self.G_PhrozenFluiddRespondInfo("self.G_ChromaKitNum=%d" % (self.G_ChromaKitNum))
            self.G_PhrozenFluiddRespondInfo("self.G_ChromaKitAccessT0=%d" % (self.G_ChromaKitAccessT0))
            self.G_PhrozenFluiddRespondInfo("self.G_ChromaKitAccessT1=%d" % (self.G_ChromaKitAccessT1))
            self.G_PhrozenFluiddRespondInfo("self.G_ChromaKitAccessT2=%d" % (self.G_ChromaKitAccessT2))
            self.G_PhrozenFluiddRespondInfo("self.G_ChromaKitAccessT3=%d" % (self.G_ChromaKitAccessT3))
            self.G_PhrozenFluiddRespondInfo("self.G_ChromaKitAccessT4=%d" % (self.G_ChromaKitAccessT4))
            self.G_PhrozenFluiddRespondInfo("self.G_ChromaKitAccessT5=%d" % (self.G_ChromaKitAccessT5))
            self.G_PhrozenFluiddRespondInfo("self.G_ChromaKitAccessT6=%d" % (self.G_ChromaKitAccessT6))
            self.G_PhrozenFluiddRespondInfo("self.G_ChromaKitAccessT7=%d" % (self.G_ChromaKitAccessT7))
            self.G_PhrozenFluiddRespondInfo("self.G_ChromaKitAccessT8=%d" % (self.G_ChromaKitAccessT8))
            self.G_PhrozenFluiddRespondInfo("self.G_ChromaKitAccessT9=%d" % (self.G_ChromaKitAccessT9))
            self.G_PhrozenFluiddRespondInfo("self.G_ChromaKitAccessT10=%d" % (self.G_ChromaKitAccessT10))
            self.G_PhrozenFluiddRespondInfo("self.G_ChromaKitAccessT11=%d" % (self.G_ChromaKitAccessT11))
            self.G_PhrozenFluiddRespondInfo("self.G_ChromaKitAccessT12=%d" % (self.G_ChromaKitAccessT12))
            self.G_PhrozenFluiddRespondInfo("self.G_ChromaKitAccessT13=%d" % (self.G_ChromaKitAccessT13))
            self.G_PhrozenFluiddRespondInfo("self.G_ChromaKitAccessT14=%d" % (self.G_ChromaKitAccessT14))
            self.G_PhrozenFluiddRespondInfo("self.G_ChromaKitAccessT15=%d" % (self.G_ChromaKitAccessT15))
            
        except:
            self.G_PhrozenFluiddRespondInfo("解析数据异常，但不影响数据获取")

####################################
    #函数名称：
    #输入参数：
    #返 回 值:
    #功能描述：蓝才刚-20230830
    ####################################
    def Cmds_GetUartScreenCfgClear(self):
        self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_GetUartScreenCfgClear]")


        #lancaigang250514：读取配置表
        try:
            self.G_PhrozenFluiddRespondInfo("try")
            # {
            # 	"Auto_Replace_state":	0,
            # 	"Chroma_Kit_state":	0,
            # 	"Chroma_Kit_num":	4,
            # 	"Chroma_Kit_access":	{
            # 		"T0":	1,
            # 		"T1":	2,
            # 		"T2":	3,
            # 		"T3":	4,
            # 		"T4":	-1,
            # 		"T5":	-1,
            # 		"T6":	-1,
            # 		"T7":	-1,
            # 		"T8":	-1,
            # 		"T9":	-1,
            # 		"T10":	-1,
            # 		"T11":	-1,
            # 		"T12":	-1,
            # 		"T13":	-1,
            # 		"T14":	-1,
            # 		"T15":	-1
            # 	}
            # }
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

            self.G_PhrozenFluiddRespondInfo("self.G_AutoReplaceState=%d" % (self.G_AutoReplaceState))
            self.G_PhrozenFluiddRespondInfo("self.G_ChromaKitNum=%d" % (self.G_ChromaKitNum))
            self.G_PhrozenFluiddRespondInfo("self.G_ChromaKitAccessT0=%d" % (self.G_ChromaKitAccessT0))
            self.G_PhrozenFluiddRespondInfo("self.G_ChromaKitAccessT1=%d" % (self.G_ChromaKitAccessT1))
            self.G_PhrozenFluiddRespondInfo("self.G_ChromaKitAccessT2=%d" % (self.G_ChromaKitAccessT2))
            self.G_PhrozenFluiddRespondInfo("self.G_ChromaKitAccessT3=%d" % (self.G_ChromaKitAccessT3))
            self.G_PhrozenFluiddRespondInfo("self.G_ChromaKitAccessT4=%d" % (self.G_ChromaKitAccessT4))
            self.G_PhrozenFluiddRespondInfo("self.G_ChromaKitAccessT5=%d" % (self.G_ChromaKitAccessT5))
            self.G_PhrozenFluiddRespondInfo("self.G_ChromaKitAccessT6=%d" % (self.G_ChromaKitAccessT6))
            self.G_PhrozenFluiddRespondInfo("self.G_ChromaKitAccessT7=%d" % (self.G_ChromaKitAccessT7))
            self.G_PhrozenFluiddRespondInfo("self.G_ChromaKitAccessT8=%d" % (self.G_ChromaKitAccessT8))
            self.G_PhrozenFluiddRespondInfo("self.G_ChromaKitAccessT9=%d" % (self.G_ChromaKitAccessT9))
            self.G_PhrozenFluiddRespondInfo("self.G_ChromaKitAccessT10=%d" % (self.G_ChromaKitAccessT10))
            self.G_PhrozenFluiddRespondInfo("self.G_ChromaKitAccessT11=%d" % (self.G_ChromaKitAccessT11))
            self.G_PhrozenFluiddRespondInfo("self.G_ChromaKitAccessT12=%d" % (self.G_ChromaKitAccessT12))
            self.G_PhrozenFluiddRespondInfo("self.G_ChromaKitAccessT13=%d" % (self.G_ChromaKitAccessT13))
            self.G_PhrozenFluiddRespondInfo("self.G_ChromaKitAccessT14=%d" % (self.G_ChromaKitAccessT14))
            self.G_PhrozenFluiddRespondInfo("self.G_ChromaKitAccessT15=%d" % (self.G_ChromaKitAccessT15))
            
        except:
            self.G_PhrozenFluiddRespondInfo("情况串口屏配置数据异常")

    ####################################
    #函数名称：
    #输入参数：
    #返 回 值:
    #功能描述：蓝才刚-20230830
    ####################################
    # P0 M1；多色模式模式(需连接外部设备) Yes；"MC";P0 M1;P28;P2 A1;
    # P0 M2；多色中单色续料模式(需连接外部设备)；"MA";P0 M2;P28;P8;
    # P0 M3; 单色断料模式;P0 M3;
    # P28 连接设备
    def Cmds_CmdP28(self, gcmd):
        self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_CmdP28]命令='%s'" % (gcmd.get_commandline(),))

        self.G_PhrozenFluiddRespondInfo("self.G_CancelFlag='%s'" % self.G_CancelFlag)
        # #lancaigang250712：
        # self.G_CancelFlag=False
        # self.G_PhrozenFluiddRespondInfo("self.G_CancelFlag='%s'" % self.G_CancelFlag)


        # #cancel取消命令
        # self.G_PhrozenPrinterCancelPauseResume.cmd_CANCEL_PRINT(None)
        #lancaigang250517：
        #self.G_PhrozenPrinterCancelPauseResume.cmd_CLEAR_PAUSE
        # #cancel取消命令
        # self.G_PhrozenPrinterCancelPauseResume.cmd_CANCEL_PRINT(None)
        #lancaigang250517：
        Lo_PauseStatus=self.G_PhrozenPrinterCancelPauseResume.get_status(None)
        self.G_PhrozenFluiddRespondInfo("当前暂停状态-Lo_PauseStatus='%s'" % Lo_PauseStatus)

        # #lancaigang250807:千万不能清空暂停状态，方式打印过程中第三方发送P28
        # self.G_PhrozenPrinterCancelPauseResume.cmd_CLEAR_PAUSE(None)
        # self.G_PhrozenFluiddRespondInfo("清空暂停状态")

        Lo_PauseStatus=self.G_PhrozenPrinterCancelPauseResume.get_status(None)
        self.G_PhrozenFluiddRespondInfo("当前暂停状态-Lo_PauseStatus='%s'" % Lo_PauseStatus)
        self.G_PhrozenFluiddRespondInfo("Lo_PauseStatus['is_paused']='%s'" % Lo_PauseStatus['is_paused'])
        #// 当前暂停状态-Lo_PauseStatus='{'is_paused': True}'
        if Lo_PauseStatus['is_paused'] == True:
            self.G_PhrozenFluiddRespondInfo("已是暂停状态")
        else:
            self.G_PhrozenFluiddRespondInfo("未暂停状态")

        self.G_PhrozenFluiddRespondInfo("当前模式")
        if self.G_AMSDeviceWorkMode == AMS_WORK_MODE_UNKNOW:
            self.G_PhrozenFluiddRespondInfo("+Mode:0,unkown")
        elif self.G_AMSDeviceWorkMode == AMS_WORK_MODE_MC:
            self.G_PhrozenFluiddRespondInfo("+Mode:1,MC")
        elif self.G_AMSDeviceWorkMode == AMS_WORK_MODE_MA:
            self.G_PhrozenFluiddRespondInfo("+Mode:2,MA")
        elif self.G_AMSDeviceWorkMode == AMS_WORK_MODE_FILA_RUNOUT:
            self.G_PhrozenFluiddRespondInfo("+Mode:3,RUNOUT")
        else:
            self.G_PhrozenFluiddRespondInfo("+Mode:-1,error")


        #解锁
        self.Base_AMSSerialCmdUnlock()

        #lancaigang250607：打印状态；1-退料中；2-进料中；3-打印中；4-暂停
        if self.G_KlipperPrintStatus == 3:
            self.G_PhrozenFluiddRespondInfo("打印中，不处理P28！！！")
            return

        #lancaigang250724:读取镜像id
        self.Cmds_GetImageId()

        #lancaigang250514：读取json文件，获取单色续料配置和通道线材颜色配对
        #/home/prz/klipper/klippy/extras/phrozen_dev/serial-screen/test.json
        self.Cmds_GetUartScreenCfg()
        


        #lancaigang231220：
        if self.G_AMSDeviceWorkMode==AMS_WORK_MODE_FILA_RUNOUT:
            self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_CmdP28]单色模式，不处理P28")
            self.G_PhrozenFluiddRespondInfo("V-H%s-I%s-F%s" % (HW_VERSION,IMAGE_VERSION,FW_VERSION))
            return

        #lancaigang250610：
        if self.G_AMSDeviceWorkMode==AMS_WORK_MODE_MA:
            self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_CmdP28]单色续料模式，不处理P28")
            self.G_PhrozenFluiddRespondInfo("V-H%s-I%s-F%s" % (HW_VERSION,IMAGE_VERSION,FW_VERSION))
            return


        # #lancaigang231122：使用ttyUSB0之前，需要关掉后台IAP升级程序hdl_zigbee_gateway
        # os.system('sh /home/prz/klipper/klippy/extras/phrozen_dev/stop.sh &')
        # self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_CmdP28]sh /home/prz/klipper/klippy/extras/phrozen_dev/stop.sh &")

        #lancaigang231205：
        self.G_KlipperIfPaused = False
        #lancaigang250526：暂停中，不允许新的gcode命令，需等待暂停完成
        self.G_KlipperInPausing = False
        #lancaigang250526：
        self.G_IfToolheadHaveFilaInitiativePauseFlag=False
        #lancaigang240223：喷头切线失败标记
        self.ToolheadCutFlag = False












        if self.G_SerialPort1Obj is not None:
            #lancaigang231219：如果串口已经打开，不能再往下
            if self.G_SerialPort1Obj.is_open:
                self.G_PhrozenFluiddRespondInfo("重复P28串口1已经打开")
                # self.G_PhrozenFluiddRespondInfo("V-H%s-I%s-F%s" % (HW_VERSION,IMAGE_VERSION,FW_VERSION))
                # #lancaigang240104：返回给触摸屏
                # self.G_PhrozenFluiddRespondInfo("+AMSCONNECT:0")

                #self.G_SerialPort1Obj.flushInput()  # clean serial write cache
                #self.G_SerialPort1Obj.flush()
                #self.G_SerialPort1OpenFlag = True
                #lancaigang240524：不管是不是None，都进行串口定时器注册
                #if self.G_SerialPort1RecvTimmer is None:
                #定时器周期线程
                self.G_PhrozenFluiddRespondInfo("重新注册串口1回调函数")
                self.G_Serial1PortRecvTimmer = self.G_PhrozenReactor.register_timer(self.Device_TimmerUart1Recv, self.G_PhrozenReactor.NOW)

                #lancaigang240511：可能导致前后粘包异常，如MA M0 MA等，导致AMS重启
                # if self.G_AMSDeviceWorkMode == AMS_WORK_MODE_MC:
                #     self.G_PhrozenFluiddRespondInfo("发送命令: M0模式")
                #     self.Cmds_AMSSerial1Send("M0")

                # if self.G_AMSDeviceWorkMode == AMS_WORK_MODE_MA:
                #     self.G_PhrozenFluiddRespondInfo("发送命令: M0模式")
                #     self.Cmds_AMSSerial1Send("M0")

                self.G_ProzenToolhead.dwell(0.5)

                #lancaigang250619:检查AMS是否重新连接成功
                self.Cmds_USBConnectErrorCheck()
                if self.G_SerialPort1OpenFlag == True:
                    # #获取多色主板详细状态
                    # Lo_AMSDeviceStateRspInfo = self.Cmds_AMSSerialPort1SendWaitRsp("SD", sizeof(AMSDetailInfoBytes))
                    # self.G_PhrozenFluiddRespondInfo("tty串口1接收: %s" % Lo_AMSDeviceStateRspInfo)
                    
                    # if len(Lo_AMSDeviceStateRspInfo) != sizeof(AMSDetailInfoBytes):
                    #     self.G_PhrozenFluiddRespondInfo("AMS1未响应，请检查AMS '%s'" % (gcmd.get_commandline(),))
                    #     #lancaigang240412:AMS多色标签
                    #     self.G_AMSDevice1IfNormal=False
                    # else:
                    #     self.G_PhrozenFluiddRespondInfo("AMS1连接成功 '%s'" % (gcmd.get_commandline(),))
                    #     self.G_PhrozenFluiddRespondInfo("self.G_AMSDevice1IfNormal=True")

                    #     #lancaigang240412:AMS多色标签
                    #     self.G_AMSDevice1IfNormal=True
                    self.Cmds_AMSSerial1Send("SD")
                    self.G_PhrozenFluiddRespondInfo("SD")

                self.G_ProzenToolhead.dwell(2)


                # if self.G_SerialPort2Obj is not None:
                #     if self.G_SerialPort2Obj.is_open:
                #         self.G_PhrozenFluiddRespondInfo("串口2已打开，继续")
                #     else:
                #         self.G_PhrozenFluiddRespondInfo("V-H%s-I%s-F%s" % (HW_VERSION,IMAGE_VERSION,FW_VERSION))
                #         self.G_PhrozenFluiddRespondInfo("+AMSCONNECT:0")
                #         #返回
                #         return
                self.G_SerialPortHaveOpenedCount=self.G_SerialPortHaveOpenedCount+1





        if self.G_SerialPort2Obj is not None:
            if self.G_SerialPort2Obj.is_open:
                self.G_PhrozenFluiddRespondInfo("重复P28串口2已经打开")
                self.G_PhrozenFluiddRespondInfo("重新注册串口2回调函数")
                self.G_SerialPort2RecvTimmer = self.G_PhrozenReactor.register_timer(self.Device_TimmerUart2Recv, self.G_PhrozenReactor.NOW)
                
                #self.G_PhrozenFluiddRespondInfo("V-H%s-I%s-F%s" % (HW_VERSION,IMAGE_VERSION,FW_VERSION))
                #self.G_PhrozenFluiddRespondInfo("+AMSCONNECT:0")

                self.G_ProzenToolhead.dwell(0.5)

                if self.G_SerialPort2OpenFlag == True:
                    # #获取多色主板详细状态
                    # Lo_AMSDeviceStateRspInfo = self.Cmds_AMSSerialPort2SendWaitRsp("SD", sizeof(AMSDetailInfoBytes))
                    # self.G_PhrozenFluiddRespondInfo("tty串口2接收: %s" % Lo_AMSDeviceStateRspInfo)
                    # if len(Lo_AMSDeviceStateRspInfo) != sizeof(AMSDetailInfoBytes):
                    #     self.G_PhrozenFluiddRespondInfo("AMS2未响应，请检查AMS '%s'" % (gcmd.get_commandline(),))
                    #     self.G_AMSDevice2IfNormal=False
                    # else:
                    #     self.G_PhrozenFluiddRespondInfo("AMS2连接成功 '%s'" % (gcmd.get_commandline(),))
                    #     self.G_AMSDevice2IfNormal=True
                    #     self.G_PhrozenFluiddRespondInfo("self.G_AMSDevice2IfNormal=True")
                    self.Cmds_AMSSerial2Send("SD")
                    self.G_PhrozenFluiddRespondInfo("SD")

                self.G_ProzenToolhead.dwell(2)

                self.G_SerialPortHaveOpenedCount=self.G_SerialPortHaveOpenedCount+1

                #return


        #lancaigang241030:
        if self.G_SerialPortHaveOpenedCount>0:
            self.G_PhrozenFluiddRespondInfo("有几台AMS已经打开串口='%d'" % (self.G_SerialPortHaveOpenedCount,))
            self.G_SerialPortHaveOpenedCount=0
            self.G_PhrozenFluiddRespondInfo("V-H%s-I%s-F%s" % (HW_VERSION,IMAGE_VERSION,FW_VERSION))
            self.G_PhrozenFluiddRespondInfo("+AMSCONNECT:0")

            #lancaigang241031:
            if self.G_SerialPort1OpenFlag == True:
                #lancaigang240524：读取AMS主板版本、16HUB主板版本
                self.Cmds_AMSSerial1Send("AT+SB=0")
                self.G_PhrozenFluiddRespondInfo("串口1发送命令: AT+SB=0；获取AMS主板版本、16色HUB主板版本")
            #lancaigang241030:
            if self.G_SerialPort2OpenFlag == True:
                #lancaigang240524：读取AMS主板版本、16HUB主板版本
                self.Cmds_AMSSerial2Send("AT+SB=0")
                self.G_PhrozenFluiddRespondInfo("串口2发送命令: AT+SB=0；获取AMS主板版本、16色HUB主板版本")

            self.G_PhrozenFluiddRespondInfo("返回return")
            #返回
            return


        #lancaigang240511：改为0.5，防止klipper启动time too close
        time.sleep(0.5)
        
        # #lancaigang20231019：打印机异常断电，自动换料如果发现第1个通道喷头残留上次线材，需要切料并退回所有线材
        # #lancaigang20231020：先不检测喷头有料
        # #if self.G_ToolheadIfHaveFilaFlag:
        # # # 0=切线前默认由内部gcode执行
        #lancaigang231128：G28改为PG28
        # if self.G_ChangeChannelIfZLiftingUpByGcode == 0:
        #     self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_CmdP28]全部归位并切线")
        #     command_string = """
        #     PG28
        #     """
        #     self.G_PhrozenGCode.run_script_from_command(command_string)
        #     #lancaigang20231020：挤出头回抽gcode，回抽前需要升温喷头，时间比较久，这里不处理，自动换料才升温并切线
        #     # G92 E0
        #     # G1 E0.0000 F600
        #     # G91
        #     # G1 E-0.385 F8000
        # self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_CmdP28]切线")
        # #lancaigang20231013：切线
        # self.Cmds_MoveToCutFilaAction(gcmd)
        # #self.G_PhrozenFluiddRespondInfo("发送命令: AP，全部后退到停靠位")
        # #// 全部后退到停靠位；//===== P2 A1 所有线料退到停靠位待打印 Yes；"AP"；
        # #Klipper state: Shutdown
        # #!! Internal error on command:"P28"
        # #如果ttyUSB0还没打开而直接发送，klippr系统报错
        # #self.Cmds_AMSSerial1Send("AP")






        #lancaigang241030:串口1
        try:
            #打开tty串口，波特率19200
            self.G_SerialPort1Obj = serial.Serial(self.G_Serialport1Define, SERIAL_PORT_BAUD, timeout=3)
            #串口打开成功
            if self.G_SerialPort1Obj.is_open:
                self.G_PhrozenFluiddRespondInfo("串口1第1次打开成功")
                #lancaigang231213：打开串口
                self.G_SerialPort1Obj.flushInput()  # clean serial write cache
                self.G_SerialPort1Obj.flush()
                self.G_SerialPort1OpenFlag = True
                #lancaigang240524：不管是不是None，都进行串口定时器注册
                #if self.G_SerialPort1RecvTimmer is None:
                #定时器周期线程
                self.G_SerialPort1RecvTimmer = self.G_PhrozenReactor.register_timer(self.Device_TimmerUart1Recv, self.G_PhrozenReactor.NOW)

                #lancaigang240306：如果模式是M1-MC，则发送MC到stm32
                if self.G_AMSDeviceWorkMode == AMS_WORK_MODE_MC:
                    self.G_PhrozenFluiddRespondInfo("AMS_WORK_MODE_MC；发送命令: M1-MC，MC模式")
                    self.Cmds_AMSSerial1Send("MC")

                #lancaigang241031：未知模式，则默认MC
                if self.G_AMSDeviceWorkMode == AMS_WORK_MODE_UNKNOW:
                    self.G_PhrozenFluiddRespondInfo("AMS_WORK_MODE_UNKNOW；发送命令: M1-MC，MC模式")
                    self.Cmds_AMSSerial1Send("MC")


                if self.G_AMSDeviceWorkMode == AMS_WORK_MODE_MA:
                    self.G_PhrozenFluiddRespondInfo("AMS_WORK_MODE_MA；发送命令: M2-MA，MA模式")
                    self.Cmds_AMSSerial1Send("MA")

                if self.G_ToolheadIfHaveFilaFlag:
                    self.G_PhrozenFluiddRespondInfo("喷头上有线材")
                    #lancaigang240113：MC模式或未知模式退线 AMS_WORK_MODE_UNKNOW, 
                    if self.G_AMSDeviceWorkMode == AMS_WORK_MODE_MC:
                        #lancaigang240319：切线之前准备动作
                        #self.Cmds_MoveToCutFilaPrepare()
                    #if self.G_AMSDeviceWorkMode == AMS_WORK_MODE_MC:
                        self.G_PhrozenFluiddRespondInfo("PG107；加热之前擦嘴")
                        command_string = """
                        PG107
                        """
                        self.G_PhrozenGCode.run_script_from_command(command_string)
                        self.G_PhrozenFluiddRespondInfo("command_string='%s'" % command_string)
                        #lancaigang240323：切线之前先擦嘴
                        # self.G_PhrozenFluiddRespondInfo("[(cmds.python)]外部宏命令-PRZ_CZ；切线之前，先擦嘴")
                        # command_string = """
                        # PRZ_CZ
                        # """
                        # self.G_PhrozenGCode.run_script_from_command(command_string)
                        # self.G_PhrozenFluiddRespondInfo("[(cmds.python)]command_string='%s'" % command_string)
                        #lancaigang231202：复位切线并回退
                        self.Cmds_MoveToCutFilaAndRollback(gcmd)
                    #lancaigang240104：单色M2MA续料模式不能切线
                    #if self.G_AMSDeviceWorkMode == AMS_WORK_MODE_MA:
                    #    #lancaigang231202：复位切线并不回退
                    #    self.Cmds_MoveToCutFilaAndNotRollback(gcmd)

                    #延时20s，防止p28后面紧跟其他命令而无法处理
                    #time.sleep(20)
                    #raise gcmd.error("[(cmds.python)Cmds_CmdP28]AMS多色连接失败")
                
                self.G_ProzenToolhead.dwell(2)

                if self.G_SerialPort1OpenFlag == True:
                    # #获取多色主板详细状态
                    # Lo_AMSDeviceStateRspInfo = self.Cmds_AMSSerialPort1SendWaitRsp("SD", sizeof(AMSDetailInfoBytes))
                    # self.G_PhrozenFluiddRespondInfo("tty1串口接收: %s" % Lo_AMSDeviceStateRspInfo)
                    # if len(Lo_AMSDeviceStateRspInfo) != sizeof(AMSDetailInfoBytes):
                    #     self.G_PhrozenFluiddRespondInfo("AMS1未响应，请检查AMS '%s'" % (gcmd.get_commandline(),))
                    #     #lancaigang240412:AMS多色标签
                    #     self.G_AMSDevice1IfNormal=False
                    # else:
                    #     #lancaigang240412:AMS多色标签
                    #     self.G_AMSDevice1IfNormal=True
                    self.Cmds_AMSSerial1Send("SD")
                    self.G_PhrozenFluiddRespondInfo("SD")

                self.G_ProzenToolhead.dwell(2)


                self.G_SerialPortIsOpenCount=self.G_SerialPortIsOpenCount+1

                # self.G_PhrozenFluiddRespondInfo("V-H%s-I%s-F%s" % (HW_VERSION,IMAGE_VERSION,FW_VERSION))
                # self.G_PhrozenFluiddRespondInfo("+AMSCONNECT:0")

            else:
                self.G_PhrozenFluiddRespondInfo("串口1第1次打开失败")
                #self.G_PhrozenFluiddRespondInfo("+AMSCONNECT:1")
                self.G_SerialPort1OpenFlag = False
                # gcmd.respond_info("Unable to connect to Phrozen devs")
                #lancaigang231207：1-AMS多色连接失败
                #lancaigang231207：2-AMS多色串口tty打开失败
                self.G_PhrozenFluiddRespondInfo("+AMSERROR:1")
                self.G_PhrozenFluiddRespondInfo("AMS1多色连接失败")
                #raise gcmd.error("AMS1多色连接失败")
        except:
            self.G_PhrozenFluiddRespondInfo("串口1第1次打开失败")
            #self.G_PhrozenFluiddRespondInfo("+AMSCONNECT:2")
            # gcmd.respond_info("Unable open USB serial port, Please check USB port connect first")
            #lancaigang231207：1-AMS多色连接失败
            #lancaigang231207：2-AMS多色串口tty打开失败
            self.G_PhrozenFluiddRespondInfo("+AMSERROR:2")
            self.G_PhrozenFluiddRespondInfo("未能打开tty1口，请检查USB口或重启尝试")
            #raise gcmd.error("AMS1多色连接失败")
        







        #lancaigang241030:串口2
        try:
            #打开tty串口，波特率19200
            self.G_SerialPort2Obj = serial.Serial(self.G_Serialport2Define, SERIAL_PORT_BAUD, timeout=3)
            #串口打开成功
            if self.G_SerialPort2Obj.is_open:
                self.G_PhrozenFluiddRespondInfo("串口2第1次打开成功")
                self.G_SerialPort2Obj.flushInput()  # clean serial write cache
                self.G_SerialPort2Obj.flush()
                self.G_SerialPort2OpenFlag = True
                self.G_SerialPort2RecvTimmer = self.G_PhrozenReactor.register_timer(self.Device_TimmerUart2Recv, self.G_PhrozenReactor.NOW)

                self.G_ProzenToolhead.dwell(0.5)

                if self.G_SerialPort2OpenFlag == True:
                    # #获取多色主板详细状态
                    # Lo_AMSDeviceStateRspInfo = self.Cmds_AMSSerialPort2SendWaitRsp("SD", sizeof(AMSDetailInfoBytes))
                    # self.G_PhrozenFluiddRespondInfo("tty2串口接收: %s" % Lo_AMSDeviceStateRspInfo)
                    # if len(Lo_AMSDeviceStateRspInfo) != sizeof(AMSDetailInfoBytes):
                    #     self.G_PhrozenFluiddRespondInfo("AMS2未响应，请检查AMS '%s'" % (gcmd.get_commandline(),))
                    #     self.G_AMSDevice2IfNormal=False
                    # else:
                    #     #lancaigang240412:AMS多色标签
                    #     self.G_AMSDevice2IfNormal=True
                    self.Cmds_AMSSerial2Send("SD")
                    self.G_PhrozenFluiddRespondInfo("SD")

                self.G_ProzenToolhead.dwell(2)

                self.G_SerialPortIsOpenCount=self.G_SerialPortIsOpenCount+1


                # self.G_PhrozenFluiddRespondInfo("V-H%s-I%s-F%s" % (HW_VERSION,IMAGE_VERSION,FW_VERSION))
                # self.G_PhrozenFluiddRespondInfo("+AMSCONNECT:0")

            else:
                self.G_PhrozenFluiddRespondInfo("串口2第1次打开失败")
                #self.G_PhrozenFluiddRespondInfo("+AMSCONNECT:1")
                self.G_SerialPort2OpenFlag = False
                self.G_PhrozenFluiddRespondInfo("+AMSERROR:1")
                self.G_PhrozenFluiddRespondInfo("AMS2多色连接失败")
                #raise gcmd.error("AMS2多色连接失败")
        except:
            self.G_PhrozenFluiddRespondInfo("串口2第1次打开失败")
            #self.G_PhrozenFluiddRespondInfo("+AMSCONNECT:2")
            self.G_PhrozenFluiddRespondInfo("+AMSERROR:2")
            self.G_PhrozenFluiddRespondInfo("未能打开tty2口，请检查USB口或重启尝试")
            #raise gcmd.error("AMS1多色连接失败")




        #lancaigang241030:只要成功打开了一个串口，说明可以使用多色
        if self.G_SerialPortIsOpenCount>0:
            self.G_PhrozenFluiddRespondInfo("成功打开AMS多色有几台=%d" % self.G_SerialPortIsOpenCount)
            self.G_SerialPortIsOpenCount=0
            
            self.G_PhrozenFluiddRespondInfo("V-H%s-I%s-F%s" % (HW_VERSION,IMAGE_VERSION,FW_VERSION))
            self.G_PhrozenFluiddRespondInfo("+AMSCONNECT:0")

            #lancaigang241031:
            if self.G_SerialPort1OpenFlag == True:
                #lancaigang240524：读取AMS主板版本、16HUB主板版本
                self.Cmds_AMSSerial1Send("AT+SB=0")
                self.G_PhrozenFluiddRespondInfo("串口1发送命令: AT+SB=0；获取AMS主板版本、16色HUB主板版本")
            #lancaigang241030:
            if self.G_SerialPort2OpenFlag == True:
                #lancaigang240524：读取AMS主板版本、16HUB主板版本
                self.Cmds_AMSSerial2Send("AT+SB=0")
                self.G_PhrozenFluiddRespondInfo("串口2发送命令: AT+SB=0；获取AMS主板版本、16色HUB主板版本")

        #如果为0，说明没有成功打开任何一个串口
        else:
            #self.G_PhrozenFluiddRespondInfo("+AMSCONNECT:2")
            self.G_PhrozenFluiddRespondInfo("+AMSERROR:2")
            self.G_PhrozenFluiddRespondInfo("未能打开任何tty口，请检查USB口或重启尝试")

            raise gcmd.error("没有连接任何AMS多色，连接AMS失败")



    ####################################
    #函数名称：python
    #输入参数：
    #返 回 值:
    #功能描述：蓝才刚-20241101
    ####################################
    #lancaigang241101：
    # P10 S?    参数S[1,5]:吐料次数控制，S1-吐料1次，S2-吐料2次...，最多支持吐料5次
    def Cmds_CmdP10(self, gcmd):
        #获取命令参数
        params = gcmd.get_command_parameters()

        if self.G_KlipperIfPaused == True:
            self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_CmdP10]klipper暂停了，但还收到命令")

        self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_CmdP10]命令='%s'" % (gcmd.get_commandline(),))

        self.G_PhrozenFluiddRespondInfo("命令：'%s'" % (gcmd.get_commandline(),))

        if "S" in params:
            Lo_SpitNum = int(params["S"])
            if not Lo_SpitNum in [1, 2, 3,4,5,6,7,8,9]:
                raise gcmd.error("无效参数命令;cmd '%s', 参数S需在[1/2/3/4/5/6/7/8/9]" % (gcmd.get_commandline(),))

            self.G_P10SpitNum=Lo_SpitNum




        #lancaigang250519:
        self.G_PhrozenFluiddRespondInfo("外部宏命令-PRZ_CUT_WAITINGAREA")
        command_string = """
            PRZ_CUT_WAITINGAREA
            """
        self.G_PhrozenGCode.run_script_from_command(command_string)
        self.G_PhrozenFluiddRespondInfo("外部宏命令-到指定待料区位置；command_string='%s'" % command_string)






        self.G_PhrozenFluiddRespondInfo("吐料次数：'%d'" % (self.G_P10SpitNum,))

    ####################################
    #函数名称：python
    #输入参数：
    #返 回 值:
    #功能描述：蓝才刚-20241101
    ####################################
    # P11 T?;多色切刀测试
    def Cmds_CmdP11(self, gcmd):
        if gcmd is None:
            self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_CmdP11]gcmd-None")
            self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_CmdP11]return")
            return
        if gcmd is not None:
            self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_CmdP11]命令='%s'" % (gcmd.get_commandline(),))
        
        #获取命令参数
        params = gcmd.get_command_parameters()

        self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_CmdP11]命令='%s'；多色切刀测试" % (gcmd.get_commandline(),))

        self.G_PhrozenFluiddRespondInfo("命令：'%s'" % (gcmd.get_commandline(),))

        #lancaigang240524：用于UIUX动态界面
        self.G_PhrozenFluiddRespondInfo("+P11:0,%d" % self.G_ChangeChannelTimeoutNewChan)

        #lancaigang250619:检查AMS是否重新连接成功
        self.Cmds_USBConnectErrorCheck()
        
        #lancaigang240527：未知模式，因为要操作手动命令，默认让STM32进入MC多色模式
        if self.G_AMSDeviceWorkMode == AMS_WORK_MODE_UNKNOW:
            self.G_PhrozenFluiddRespondInfo("未知模式，因为要操作手动命令，默认让STM32进入MC多色模式")
            #lancaigang241030:
            if self.G_SerialPort1OpenFlag == True:
                self.Cmds_AMSSerial1Send("MC")
                self.G_PhrozenFluiddRespondInfo("串口1发送命令：MC")
            #lancaigang241030:
            if self.G_SerialPort2OpenFlag == True:
                self.Cmds_AMSSerial2Send("MC")
                self.G_PhrozenFluiddRespondInfo("串口2发送命令：MC")

            self.G_ProzenToolhead.dwell(2)

        #lancaigang231209：手动调式可不用管暂停
        self.G_KlipperIfPaused=False
        #lancaigang240221：stm32主动上报，开启可以暂停1次
        self.STM32ReprotPauseFlag=0
        self.G_PhrozenFluiddRespondInfo("self.STM32ReprotPauseFlag=0")

        #lancaigang250805:切刀测试
        self.G_CutCheckTest=True
        self.ManualCmdFlag=False


        #if self.G_ToolheadIfHaveFilaFlag:
        self.G_PhrozenFluiddRespondInfo("强制复位，切线；所有AMS先回退")
        #lancaigang231205：复位切线回退
        self.Cmds_MoveToCutFilaAndHomingXY(gcmd)



        self.G_PhrozenFluiddRespondInfo("外部宏命令-PG104-获取换线之前全局变量")
        command_string = """
            PG104
            """
        self.G_PhrozenGCode.run_script_from_command(command_string)
        self.G_PhrozenFluiddRespondInfo("外部宏命令-PG104-获取换线之前全局变量；command_string='%s'" % command_string)
        self.IfDoPG102Flag=True


        #lancaigang240510：换线之前，先跑到待料区
        #lancaigang240306：移动到切线代码里面
        #lancaigang240110：等待区域等待之前，先执行外部宏命令，移动到特定位置进行等待
        #lancaigang240515：换线之前，首先要到待料区
        self.G_PhrozenFluiddRespondInfo("外部宏命令-PG101-回抽")
        command_string = """
            PG101
            """
        self.G_PhrozenGCode.run_script_from_command(command_string)
        self.G_PhrozenFluiddRespondInfo("外部宏命令-到指定待料区位置等待吐料；command_string='%s'" % command_string)
        self.IfDoPG102Flag=True



        #lancaigang240319：切完后，先吐掉残留喷头的线材，防止切成米粒
        self.G_PhrozenFluiddRespondInfo("外部宏命令-PG106；切线之前，先吐掉残留喷头的线材，防止切成米粒")
        self.PG102Flag=True
        self.G_PhrozenFluiddRespondInfo("self.Flag=True")
        command_string = """
        PG106
        """
        self.G_PhrozenGCode.run_script_from_command(command_string)
        self.G_PhrozenFluiddRespondInfo("command_string='%s'" % command_string)
        self.PG102Flag=False
        self.G_PhrozenFluiddRespondInfo("self.Flag=False")




        #lancaigang250619:检查AMS是否重新连接成功
        self.Cmds_USBConnectErrorCheck()


        if self.G_SerialPort1OpenFlag == True:
            self.Cmds_AMSSerial1Send("AP")
            self.G_PhrozenFluiddRespondInfo("串口1发送命令：AP")
        #lancaigang241030:
        if self.G_SerialPort2OpenFlag == True:
            self.Cmds_AMSSerial2Send("AP")
            self.G_PhrozenFluiddRespondInfo("串口2发送命令：AP")

        self.G_ProzenToolhead.dwell(0.5)


        #lancaigang240913：把延時放到外面
        self.G_ProzenToolhead.dwell(6.0)
        #lancaigang231201：检查切线后旧通道线材是否正常退料，不正常则暂停
        self.Cmds_CutFilaIfNormalCheck()
        if self.G_KlipperIfPaused == True:
            self.G_PhrozenFluiddRespondInfo("切线5秒了喷头还检测到线材，切刀异常了，请检查切刀，暂停klipper打印")
            #Lo_ChangeChannelIfSuccess = False
            #lancaigang240524：用于UIUX动态界面
            self.G_PhrozenFluiddRespondInfo("+P11:1,%d" % self.G_ChangeChannelTimeoutNewChan)
            #lancaigang250805:切刀测试
            self.G_CutCheckTest=False
            return


        #lancaigang231207：
        if self.G_IfInFilaBlockFlag:
            self.G_PhrozenFluiddRespondInfo("进料卡线，先手动P1 E?从喷头上料管取出并手动prz_resume恢复")
            #lancaigang240524：用于UIUX动态界面
            self.G_PhrozenFluiddRespondInfo("+P11:1,%d" % self.G_ChangeChannelTimeoutNewChan)
            #lancaigang250805:切刀测试
            self.G_CutCheckTest=False
            return


        if "T" in params:
            #lancaigang240524：用于UIUX动态界面
            self.G_PhrozenFluiddRespondInfo("+P11 Tn:0,%d" % self.G_ChangeChannelTimeoutNewChan)
            self.G_ChangeChannelTimeoutOldChan=self.G_ChangeChannelTimeoutNewChan
            self.G_ChangeChannelTimeoutOldGcmd=self.G_ChangeChannelTimeoutNewGcmd
            self.G_ChangeChannelTimeoutNewChan=int(params["T"])
            self.G_ChangeChannelTimeoutNewGcmd=gcmd


            self.G_P10SpitNum=1

            #lancaigang241030：一般是P1 C1到P1 C32，范围在1到32
            #第1台：1 2 3 4
            #第2台：5 6 7 8
            #第3台：9 10 11 12
            #第4台：13 14 15 16
            #第5台：17 18 19 20
            #第6台：21 22 23 24
            #第7台：25 26 27 28
            #第8台：29 30 31 32
            #手动换料
            self.Cmds_P1TnManualChangeChannel(int(params["T"]), gcmd)
            #lancaigang240524：用于UIUX动态界面
            #self.G_PhrozenFluiddRespondInfo("+P11 Tn:1,%d" % self.G_ChangeChannelTimeoutNewChan)


            self.Cmds_MoveToCutFilaAction(gcmd)

            #lancaigang250519:
            self.G_PhrozenFluiddRespondInfo("外部宏命令-PRZ_CUT_WAITINGAREA")
            command_string = """
                PRZ_CUT_WAITINGAREA
                """
            self.G_PhrozenGCode.run_script_from_command(command_string)
            self.G_PhrozenFluiddRespondInfo("外部宏命令-到指定待料区位置；command_string='%s'" % command_string)


            if self.G_SerialPort1OpenFlag == True:
                self.Cmds_AMSSerial1Send("AP")
                self.G_PhrozenFluiddRespondInfo("串口1发送命令：AP")
            #lancaigang241030:
            if self.G_SerialPort2OpenFlag == True:
                self.Cmds_AMSSerial2Send("AP")
                self.G_PhrozenFluiddRespondInfo("串口2发送命令：AP")

            self.G_ProzenToolhead.dwell(0.5)




            #lancaigang240913：把延時放到外面
            self.G_ProzenToolhead.dwell(6.0)
            #lancaigang231201：检查切线后旧通道线材是否正常退料，不正常则暂停
            self.Cmds_CutFilaIfNormalCheck()
            if self.G_KlipperIfPaused == True:
                self.G_PhrozenFluiddRespondInfo("切线5秒了喷头还检测到线材，切刀异常了，请检查切刀，暂停klipper打印")
                #Lo_ChangeChannelIfSuccess = False
                #lancaigang240524：用于UIUX动态界面
                self.G_PhrozenFluiddRespondInfo("+P11:1,%d" % self.G_ChangeChannelTimeoutNewChan)
                #lancaigang250805:切刀测试
                self.G_CutCheckTest=False
                return




        #lancaigang240524：用于UIUX动态界面
        self.G_PhrozenFluiddRespondInfo("+P11:1,%d" % self.G_ChangeChannelTimeoutNewChan)
        #lancaigang250805:切刀测试
        self.G_CutCheckTest=False

    ####################################
    #函数名称：python
    #输入参数：
    #返 回 值:
    #功能描述：蓝才刚-20241101
    ####################################
    # P12 T?;多色切刀循环测试
    def Cmds_CmdP12(self, gcmd):
        if gcmd is None:
            self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_CmdP12]gcmd-None")
            self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_CmdP12]return")
            return
        if gcmd is not None:
            self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_CmdP12]命令='%s'" % (gcmd.get_commandline(),))
        
        #获取命令参数
        params = gcmd.get_command_parameters()

        self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_CmdP12]命令='%s'；多色切刀循环测试" % (gcmd.get_commandline(),))

        self.G_PhrozenFluiddRespondInfo("命令：'%s'" % (gcmd.get_commandline(),))

        #lancaigang240524：用于UIUX动态界面
        self.G_PhrozenFluiddRespondInfo("+P12:0,%d" % self.G_ChangeChannelTimeoutNewChan)

        #lancaigang250619:检查AMS是否重新连接成功
        self.Cmds_USBConnectErrorCheck()
        
        #lancaigang240527：未知模式，因为要操作手动命令，默认让STM32进入MC多色模式
        if self.G_AMSDeviceWorkMode == AMS_WORK_MODE_UNKNOW:
            self.G_PhrozenFluiddRespondInfo("未知模式，因为要操作手动命令，默认让STM32进入MC多色模式")
            #lancaigang241030:
            if self.G_SerialPort1OpenFlag == True:
                self.Cmds_AMSSerial1Send("MC")
                self.G_PhrozenFluiddRespondInfo("串口1发送命令：MC")
            #lancaigang241030:
            if self.G_SerialPort2OpenFlag == True:
                self.Cmds_AMSSerial2Send("MC")
                self.G_PhrozenFluiddRespondInfo("串口2发送命令：MC")

            self.G_ProzenToolhead.dwell(2)

        #lancaigang231209：手动调式可不用管暂停
        self.G_KlipperIfPaused=False
        #lancaigang240221：stm32主动上报，开启可以暂停1次
        self.STM32ReprotPauseFlag=0
        self.G_PhrozenFluiddRespondInfo("self.STM32ReprotPauseFlag=0")

        #lancaigang250805:切刀测试
        self.G_CutCheckTest=True
        self.ManualCmdFlag=False


        # #if self.G_ToolheadIfHaveFilaFlag:
        # self.G_PhrozenFluiddRespondInfo("强制复位，切线；所有AMS先回退")
        # #lancaigang231205：复位切线回退
        # self.Cmds_MoveToCutFilaAndHomingXY(gcmd)



        self.G_PhrozenFluiddRespondInfo("外部宏命令-PG104-获取换线之前全局变量")
        command_string = """
            PG104
            """
        self.G_PhrozenGCode.run_script_from_command(command_string)
        self.G_PhrozenFluiddRespondInfo("外部宏命令-PG104-获取换线之前全局变量；command_string='%s'" % command_string)
        self.IfDoPG102Flag=True


        #lancaigang240510：换线之前，先跑到待料区
        #lancaigang240306：移动到切线代码里面
        #lancaigang240110：等待区域等待之前，先执行外部宏命令，移动到特定位置进行等待
        #lancaigang240515：换线之前，首先要到待料区
        self.G_PhrozenFluiddRespondInfo("外部宏命令-PG101-回抽")
        command_string = """
            PG101
            """
        self.G_PhrozenGCode.run_script_from_command(command_string)
        self.G_PhrozenFluiddRespondInfo("外部宏命令-到指定待料区位置等待吐料；command_string='%s'" % command_string)
        self.IfDoPG102Flag=True



        #lancaigang240319：切完后，先吐掉残留喷头的线材，防止切成米粒
        self.G_PhrozenFluiddRespondInfo("外部宏命令-PG106；切线之前，先吐掉残留喷头的线材，防止切成米粒")
        self.PG102Flag=True
        self.G_PhrozenFluiddRespondInfo("self.Flag=True")
        command_string = """
        PG106
        """
        self.G_PhrozenGCode.run_script_from_command(command_string)
        self.G_PhrozenFluiddRespondInfo("command_string='%s'" % command_string)
        self.PG102Flag=False
        self.G_PhrozenFluiddRespondInfo("self.Flag=False")




        #lancaigang250619:检查AMS是否重新连接成功
        self.Cmds_USBConnectErrorCheck()


        if self.G_SerialPort1OpenFlag == True:
            self.Cmds_AMSSerial1Send("AP")
            self.G_PhrozenFluiddRespondInfo("串口1发送命令：AP")
        #lancaigang241030:
        if self.G_SerialPort2OpenFlag == True:
            self.Cmds_AMSSerial2Send("AP")
            self.G_PhrozenFluiddRespondInfo("串口2发送命令：AP")

        self.G_ProzenToolhead.dwell(0.5)


        #lancaigang240913：把延時放到外面
        self.G_ProzenToolhead.dwell(6.0)
        #lancaigang231201：检查切线后旧通道线材是否正常退料，不正常则暂停
        self.Cmds_CutFilaIfNormalCheck()
        if self.G_KlipperIfPaused == True:
            self.G_PhrozenFluiddRespondInfo("切线5秒了喷头还检测到线材，切刀异常了，请检查切刀，暂停klipper打印")
            #Lo_ChangeChannelIfSuccess = False
            #lancaigang240524：用于UIUX动态界面
            self.G_PhrozenFluiddRespondInfo("+P12:1,%d" % self.G_ChangeChannelTimeoutNewChan)
            #lancaigang250805:切刀测试
            self.G_CutCheckTest=False
            return


        #lancaigang231207：
        if self.G_IfInFilaBlockFlag:
            self.G_PhrozenFluiddRespondInfo("进料卡线，先手动P1 E?从喷头上料管取出并手动prz_resume恢复")
            #lancaigang240524：用于UIUX动态界面
            self.G_PhrozenFluiddRespondInfo("+P12:1,%d" % self.G_ChangeChannelTimeoutNewChan)
            #lancaigang250805:切刀测试
            self.G_CutCheckTest=False
            return


        if "T" in params:
            #lancaigang240524：用于UIUX动态界面
            self.G_PhrozenFluiddRespondInfo("+P12 Tn:0,%d" % self.G_ChangeChannelTimeoutNewChan)
            self.G_ChangeChannelTimeoutOldChan=self.G_ChangeChannelTimeoutNewChan
            self.G_ChangeChannelTimeoutOldGcmd=self.G_ChangeChannelTimeoutNewGcmd
            self.G_ChangeChannelTimeoutNewChan=int(params["T"])
            self.G_ChangeChannelTimeoutNewGcmd=gcmd


            self.G_P10SpitNum=1

            #lancaigang241030：一般是P1 C1到P1 C32，范围在1到32
            #第1台：1 2 3 4
            #第2台：5 6 7 8
            #第3台：9 10 11 12
            #第4台：13 14 15 16
            #第5台：17 18 19 20
            #第6台：21 22 23 24
            #第7台：25 26 27 28
            #第8台：29 30 31 32
            #手动换料
            self.Cmds_P1TnManualChangeChannel(int(params["T"]), gcmd)
            #lancaigang240524：用于UIUX动态界面
            #self.G_PhrozenFluiddRespondInfo("+P12 Tn:1,%d" % self.G_ChangeChannelTimeoutNewChan)


            self.Cmds_MoveToCutFilaAction(gcmd)

            #lancaigang250519:
            self.G_PhrozenFluiddRespondInfo("外部宏命令-PRZ_CUT_WAITINGAREA")
            command_string = """
                PRZ_CUT_WAITINGAREA
                """
            self.G_PhrozenGCode.run_script_from_command(command_string)
            self.G_PhrozenFluiddRespondInfo("外部宏命令-到指定待料区位置；command_string='%s'" % command_string)


            if self.G_SerialPort1OpenFlag == True:
                self.Cmds_AMSSerial1Send("AP")
                self.G_PhrozenFluiddRespondInfo("串口1发送命令：AP")
            #lancaigang241030:
            if self.G_SerialPort2OpenFlag == True:
                self.Cmds_AMSSerial2Send("AP")
                self.G_PhrozenFluiddRespondInfo("串口2发送命令：AP")

            self.G_ProzenToolhead.dwell(0.5)




            #lancaigang240913：把延時放到外面
            self.G_ProzenToolhead.dwell(6.0)
            #lancaigang231201：检查切线后旧通道线材是否正常退料，不正常则暂停
            self.Cmds_CutFilaIfNormalCheck()
            if self.G_KlipperIfPaused == True:
                self.G_PhrozenFluiddRespondInfo("切线5秒了喷头还检测到线材，切刀异常了，请检查切刀，暂停klipper打印")
                #Lo_ChangeChannelIfSuccess = False
                #lancaigang240524：用于UIUX动态界面
                self.G_PhrozenFluiddRespondInfo("+P12:1,%d" % self.G_ChangeChannelTimeoutNewChan)
                #lancaigang250805:切刀测试
                self.G_CutCheckTest=False
                return




        #lancaigang240524：用于UIUX动态界面
        self.G_PhrozenFluiddRespondInfo("+P12:1,%d" % self.G_ChangeChannelTimeoutNewChan)
        #lancaigang250805:切刀测试
        self.G_CutCheckTest=False




    ####################################
    #函数名称：
    #输入参数：
    #返 回 值:
    #功能描述：蓝才刚-20230830
    ####################################
    #'P9 X195.940 Y242.500 W3.010 H41.450 D?'
    #换线等待区域处理
    # P9 
    # X[x_pos] x_pos:等待区基点X坐标
    # Y[y_pos] y_pos:等待区基点Y坐标
    # W[width] width:等待区宽度 
    # H[height] height:等待区高度 
    # D[0/5] D?:保持原样

    # P9 
    # T[expire]
    # A[0/1];
    # expire:超时时间,单位秒(默认60) 
    # A0:忽略超时,继续打印(默认)   A1:超时后终止打印设定等待超时及处理
    def Cmds_CmdP9(self, gcmd):
        #获取命令参数
        params = gcmd.get_command_parameters()

        if self.G_KlipperIfPaused == True:
            self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_CmdP9]klipper暂停了，但还收到命令")

        self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_CmdP9]命令='%s'" % (gcmd.get_commandline(),))

        #lancaigang20231016：P9后续参数XYWH；X坐标；Y坐标；W等待区宽度；H等待区高度
        #'P9 X195.940 Y242.500 W3.010 H41.450 D0'
        for flag in "XYWH":
            if flag in params:
                self.G_DictChangeChannelWaitAreaParam[flag] = float(params[flag])

        self.G_PhrozenFluiddRespondInfo("命令：'%s'" % (gcmd.get_commandline(),))

        #参数D # D0:以X方向作慢速移动Y方向计数(默认) D1:以Y方向作慢速移动X方向计数设定等待区域
        #'P9 X195.940 Y242.500 W3.010 H41.450 D0'
        if "D" in params:
            direction = int(params["D"])
            # if not direction in [0, 10]:
            #     raise gcmd.error("无效等待区域设置，D参数必须是[0/1] '%s'" % (gcmd.get_commandline(),))
            self.G_DictChangeChannelWaitAreaParam["D"] = direction

        #lancaigang241031：
        self.G_PhrozenFluiddRespondInfo("P9参数;self.G_DictChangeChannelWaitAreaParam[D]='%d'" % (self.G_DictChangeChannelWaitAreaParam["D"],))


        #参数T # expire:超时时间,单位秒(默认60) 
        #'P9 X195.940 Y242.500 W3.010 H41.450 D0'
        if "T" in params:
            expire = int(params["T"])
            #lancaigang20231016：改为60秒
            if expire < 60:
                self.G_PhrozenFluiddRespondInfo("无效超时时间，必须是60秒内 '%s'" % (gcmd.get_commandline(),))
            self.G_DictChangeChannelWaitAreaParam["T"] = expire
            self.G_PhrozenFluiddRespondInfo("换料发送命令: expire=%d" % expire)

        #参数 A# A0:忽略超时,继续打印(默认)   A1:超时后终止打印设定等待超时及处理
        #'P9 X195.940 Y242.500 W3.010 H41.450 D0'
        if "A" in params:
            action = int(params["A"])
            if not action in [0, 1]:
                self.G_PhrozenFluiddRespondInfo("无效超时处理，A参数必须是[0/1] '%s'" % (gcmd.get_commandline(),))
            self.G_DictChangeChannelWaitAreaParam["A"] = action

        # Python 列表(List)
        # 序列是Python中最基本的数据结构。序列中的每个元素都分配一个数字 - 它的位置，或索引，第一个索引是0，第二个索引是1，依此类推。
        # Python有6个序列的内置类型，但最常见的是列表和元组。
        # 序列都可以进行的操作包括索引，切片，加，乘，检查成员。
        # 此外，Python已经内置确定序列的长度以及确定最大和最小的元素的方法。
        # 列表是最常用的Python数据类型，它可以作为一个方括号内的逗号分隔值出现。
        # 列表的数据项不需要具有相同的类型
        # 创建一个列表，只要把逗号分隔的不同的数据项使用方括号括起来即可。如下所示：
        # list1 = ['physics', 'chemistry', 1997, 2000]
        # list2 = [1, 2, 3, 4, 5 ]
        # list3 = ["a", "b", "c", "d"]
        # 与字符串的索引一样，列表索引从0开始。列表可以进行截取、组合等。
        self.ChangeWaitMoveArea = []
        # 默认线宽mm；cfg配置线宽或内部默认线宽
        Lo_LineWidth = self.G_ChangeChannelWaitLineWidth  
        #等待区域宽 高
        Lo_WaitAreaWidth, Lo_WaitAreaHeight = abs(self.G_DictChangeChannelWaitAreaParam["W"]), abs(self.G_DictChangeChannelWaitAreaParam["H"])
        #等待区域X基点坐标 Y基点坐标
        Lo_XBasePosition, Lo_YBasePosition = self.G_DictChangeChannelWaitAreaParam["X"], self.G_DictChangeChannelWaitAreaParam["Y"]
        #lancaigang231216
        self.G_XBasePosition=Lo_XBasePosition
        self.G_YBasePosition=Lo_YBasePosition

        #总移动距离
        Lo_TotalMovingDist = (Lo_WaitAreaWidth * Lo_WaitAreaHeight / Lo_LineWidth)
        #每一个步长;# 步进mm/s
        self.G_WaitAreaEachStepDist = min(Lo_TotalMovingDist / self.G_DictChangeChannelWaitAreaParam["T"], self.G_ChangeChannelWaitMaxMovementSpeed* self.G_MovementSpeedFactor) 

        # D0:以X方向作慢速移动Y方向计数(默认) D1:以Y方向作慢速移动X方向计数设定等待区域
        if self.G_DictChangeChannelWaitAreaParam["D"] == 1:
            Lo_WaitAreaWidth, Lo_WaitAreaHeight = Lo_WaitAreaHeight, Lo_WaitAreaWidth

        if self.G_WaitAreaEachStepDist > Lo_WaitAreaWidth:
             #lancaigang231129：宽度超出也继续等待换线继续打印
             self.G_PhrozenFluiddRespondInfo("无效参数;cmd='%s', that less than minstep: %.03f"% (gcmd.get_commandline(), self.G_WaitAreaEachStepDist))

        #生成等待区域长方形每一步的数据
        for index, y in enumerate(np.arange(0.0, Lo_WaitAreaHeight, Lo_LineWidth)):
            #
            if len(self.ChangeWaitMoveArea) >= self.G_DictChangeChannelWaitAreaParam["T"]:
                break
            if index % 2 == 0:
                for x in np.arange(0, Lo_WaitAreaWidth, self.G_WaitAreaEachStepDist):
                    if x < Lo_WaitAreaWidth - self.G_WaitAreaEachStepDist / 2:
                        self.ChangeWaitMoveArea.append([x, y, True])
                    else:
                        self.ChangeWaitMoveArea.append([Lo_WaitAreaWidth, y, True])
                        if y + Lo_LineWidth < Lo_WaitAreaHeight:
                            self.ChangeWaitMoveArea.append((Lo_WaitAreaWidth, y + Lo_LineWidth, False))
                        break
            else:
                for x in np.arange(Lo_WaitAreaWidth - self.G_WaitAreaEachStepDist, 0.0, -self.G_WaitAreaEachStepDist):
                    if x > self.G_WaitAreaEachStepDist / 2:
                        self.ChangeWaitMoveArea.append([x, y, True])
                    else:
                        self.ChangeWaitMoveArea.append([0, y, False])
                        break

        # D0:以X方向作慢速移动Y方向计数(默认) D1:以Y方向作慢速移动X方向计数设定等待区域
        if self.G_DictChangeChannelWaitAreaParam["D"] == 1:
            self.ChangeWaitMoveArea = [[y, x, b] for [x, y, b] in self.ChangeWaitMoveArea]

        # W宽
        if self.G_DictChangeChannelWaitAreaParam["W"] < 0:
            self.ChangeWaitMoveArea = [[-x, y, b] for [x, y, b] in self.ChangeWaitMoveArea]

        # H高
        if self.G_DictChangeChannelWaitAreaParam["H"] < 0:
            self.ChangeWaitMoveArea = [[x, -y, b] for [x, y, b] in self.ChangeWaitMoveArea]

        self.ChangeWaitMoveArea = [[x + Lo_XBasePosition, y + Lo_YBasePosition, b] for [x, y, b] in self.ChangeWaitMoveArea]


####################################
    #函数名称：
    #输入参数：
    #返 回 值:
    #功能描述：蓝才刚-20230830
    ####################################
    def Cmds_CmdP0M3P8FA(self, AMSNum,gcmd):
        # if not self.G_SerialPort1OpenFlag:
        #     self.G_PhrozenFluiddRespondInfo("AMS多色未连接，请先发送P28")
        #     return
        
        self.G_ProzenToolhead.dwell(2.0)

        self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_CmdP0M3P8FA]命令=P8FA" )

        Lo_MCUSTM32Cmd = G_DictPhrozenCmdP8["mcu_cmd"][0]
        #lancaigang250619:检查AMS是否重新连接成功
        self.Cmds_USBConnectErrorCheck()
        #lancaigang241030:
        if AMSNum==1:
            self.Cmds_AMSSerial1Send("MA")
            self.G_PhrozenFluiddRespondInfo("串口1发送MA")
        elif AMSNum==2:
            self.Cmds_AMSSerial2Send("MA")
            self.G_PhrozenFluiddRespondInfo("串口2发送MA")

        #lancaigang240124：stm32主动上报，开启可以暂停1次
        self.STM32ReprotPauseFlag=0


        #lancaigang240123：如果喷头有线材，不用发送FA到stm32，等待喷头打印完成之后暂停再发送FA，并自动恢复
        if self.G_ToolheadIfHaveFilaFlag==False:
            self.G_PhrozenFluiddRespondInfo("喷头没有线材，FA")
            #lancaigang240115:延时2秒，防止粘包
            #time.sleep(2)
            self.G_ProzenToolhead.dwell(2.0)

            #lancaigang241030:
            if AMSNum==1:
                self.Cmds_AMSSerial1Send("FA")
                self.G_PhrozenFluiddRespondInfo("串口1发送FA")
            elif AMSNum==2:
                self.Cmds_AMSSerial2Send("FA")
                self.G_PhrozenFluiddRespondInfo("串口2发送FA")

            #lancaigang231229:封装函数，等待进料
            self.Cmds_MARetryInFila(gcmd)
            #lancaigang240108：P8命令不用处理恢复命令
            self.G_M2MAModeResumeFlag=False



        else:#喷头有线材
            self.G_PhrozenFluiddRespondInfo("喷头有线材，FB")
            #time.sleep(2)
            self.G_ProzenToolhead.dwell(2.0)

            #lancaigang241030:
            if AMSNum==1:
                self.Cmds_AMSSerial1Send("FB")
                self.G_PhrozenFluiddRespondInfo("串口1发送FB")
            elif AMSNum==2:
                self.Cmds_AMSSerial2Send("FB")
                self.G_PhrozenFluiddRespondInfo("串口2发送FB")

            self.G_M2MAModeResumeFlag=False

    ####################################
    #函数名称：
    #输入参数：
    #返 回 值:
    #功能描述：蓝才刚-20230830
    ####################################
    def Cmds_P8AMS1AutoSelectChannel(self):
        self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_P8AMS1AutoSelectChannel]")

        bitmask1=0b0001
        bitmask2=0b0010
        bitmask4=0b0100
        bitmask8=0b1000
        if self.G_AMS1DeviceState["entry_state"] == 0:
            if self.G_AMS1DeviceState["park_state"] & bitmask1 == 1:#0001
                self.G_PhrozenFluiddRespondInfo("串口1换料发送命令: T1")
                self.Cmds_AMSSerial1Send("T1")
                if self.G_ChangeChannelTimeoutOldChan<0 or self.G_ChangeChannelTimeoutNewChan<0:
                    self.G_ChangeChannelTimeoutOldChan=1
                else:
                    self.G_ChangeChannelTimeoutOldChan=self.G_ChangeChannelTimeoutNewChan
                self.G_ChangeChannelTimeoutNewChan=1
                self.G_PhrozenFluiddRespondInfo("+T:0,1")
            elif self.G_AMS1DeviceState["park_state"] & bitmask2 == 2:#0010
                self.G_PhrozenFluiddRespondInfo("串口1换料发送命令: T2")
                self.Cmds_AMSSerial1Send("T2")
                if self.G_ChangeChannelTimeoutOldChan<0 or self.G_ChangeChannelTimeoutNewChan<0:
                    self.G_ChangeChannelTimeoutOldChan=2
                else:
                    self.G_ChangeChannelTimeoutOldChan=self.G_ChangeChannelTimeoutNewChan
                self.G_ChangeChannelTimeoutNewChan=2
                self.G_PhrozenFluiddRespondInfo("+T:0,2")
            elif self.G_AMS1DeviceState["park_state"] & bitmask4 == 4:#0100
                self.G_PhrozenFluiddRespondInfo("串口1换料发送命令: T3")
                self.Cmds_AMSSerial1Send("T3")
                if self.G_ChangeChannelTimeoutOldChan<0 or self.G_ChangeChannelTimeoutNewChan<0:
                    self.G_ChangeChannelTimeoutOldChan=3
                else:
                    self.G_ChangeChannelTimeoutOldChan=self.G_ChangeChannelTimeoutNewChan
                self.G_ChangeChannelTimeoutNewChan=3
                self.G_PhrozenFluiddRespondInfo("+T:0,3")
            elif self.G_AMS1DeviceState["park_state"] & bitmask8 == 8:#1000
                self.G_PhrozenFluiddRespondInfo("串口1换料发送命令: T4")
                self.Cmds_AMSSerial1Send("T4")
                if self.G_ChangeChannelTimeoutOldChan<0 or self.G_ChangeChannelTimeoutNewChan<0:
                    self.G_ChangeChannelTimeoutOldChan=4
                else:
                    self.G_ChangeChannelTimeoutOldChan=self.G_ChangeChannelTimeoutNewChan
                self.G_ChangeChannelTimeoutNewChan=4
                self.G_PhrozenFluiddRespondInfo("+T:0,4")
            else:
                self.G_PhrozenFluiddRespondInfo("无线材")
        elif self.G_AMS1DeviceState["entry_state"] & bitmask1 == 1:#0001
            self.G_PhrozenFluiddRespondInfo("串口1换料发送命令: T1")
            self.Cmds_AMSSerial1Send("T1")
            if self.G_ChangeChannelTimeoutOldChan<0 or self.G_ChangeChannelTimeoutNewChan<0:
                    self.G_ChangeChannelTimeoutOldChan=1
            else:
                self.G_ChangeChannelTimeoutOldChan=self.G_ChangeChannelTimeoutNewChan
            self.G_ChangeChannelTimeoutNewChan=1
            self.G_PhrozenFluiddRespondInfo("+T:0,1")
        elif self.G_AMS1DeviceState["entry_state"] & bitmask2 == 2:#0010
            if self.G_AMS1DeviceState["park_state"] & bitmask1 == 1:#0001
                self.G_PhrozenFluiddRespondInfo("串口1换料发送命令: T1")
                self.Cmds_AMSSerial1Send("T1")
                if self.G_ChangeChannelTimeoutOldChan<0 or self.G_ChangeChannelTimeoutNewChan<0:
                    self.G_ChangeChannelTimeoutOldChan=1
                else:
                    self.G_ChangeChannelTimeoutOldChan=self.G_ChangeChannelTimeoutNewChan
                self.G_ChangeChannelTimeoutNewChan=1
                self.G_PhrozenFluiddRespondInfo("+T:0,1")
            elif self.G_AMS1DeviceState["park_state"] & bitmask2 == 2:#0010
                self.G_PhrozenFluiddRespondInfo("串口1换料发送命令: T2")
                self.Cmds_AMSSerial1Send("T2")
                if self.G_ChangeChannelTimeoutOldChan<0 or self.G_ChangeChannelTimeoutNewChan<0:
                    self.G_ChangeChannelTimeoutOldChan=2
                else:
                    self.G_ChangeChannelTimeoutOldChan=self.G_ChangeChannelTimeoutNewChan
                self.G_ChangeChannelTimeoutNewChan=2
                self.G_PhrozenFluiddRespondInfo("+T:0,2")
            else:
                self.G_PhrozenFluiddRespondInfo("串口1换料发送命令: T2")
                self.Cmds_AMSSerial1Send("T2")
                if self.G_ChangeChannelTimeoutOldChan<0 or self.G_ChangeChannelTimeoutNewChan<0:
                    self.G_ChangeChannelTimeoutOldChan=2
                else:
                    self.G_ChangeChannelTimeoutOldChan=self.G_ChangeChannelTimeoutNewChan
                self.G_ChangeChannelTimeoutNewChan=2
                self.G_PhrozenFluiddRespondInfo("+T:0,2")
        elif self.G_AMS1DeviceState["entry_state"] & bitmask4 == 4:#0100
            if self.G_AMS1DeviceState["park_state"] & bitmask1 == 1:#0001
                self.G_PhrozenFluiddRespondInfo("串口1换料发送命令: T1")
                self.Cmds_AMSSerial1Send("T1")
                if self.G_ChangeChannelTimeoutOldChan<0 or self.G_ChangeChannelTimeoutNewChan<0:
                    self.G_ChangeChannelTimeoutOldChan=1
                else:
                    self.G_ChangeChannelTimeoutOldChan=self.G_ChangeChannelTimeoutNewChan
                self.G_ChangeChannelTimeoutNewChan=1
                self.G_PhrozenFluiddRespondInfo("+T:0,1")
            elif self.G_AMS1DeviceState["park_state"] & bitmask2 == 2:#0010
                self.G_PhrozenFluiddRespondInfo("串口1换料发送命令: T2")
                self.Cmds_AMSSerial1Send("T2")
                if self.G_ChangeChannelTimeoutOldChan<0 or self.G_ChangeChannelTimeoutNewChan<0:
                    self.G_ChangeChannelTimeoutOldChan=2
                else:
                    self.G_ChangeChannelTimeoutOldChan=self.G_ChangeChannelTimeoutNewChan
                self.G_ChangeChannelTimeoutNewChan=2
                self.G_PhrozenFluiddRespondInfo("+T:0,2")
            elif self.G_AMS1DeviceState["park_state"] & bitmask4 == 4:#0100
                self.G_PhrozenFluiddRespondInfo("串口1换料发送命令: T3")
                self.Cmds_AMSSerial1Send("T3")
                if self.G_ChangeChannelTimeoutOldChan<0 or self.G_ChangeChannelTimeoutNewChan<0:
                    self.G_ChangeChannelTimeoutOldChan=3
                else:
                    self.G_ChangeChannelTimeoutOldChan=self.G_ChangeChannelTimeoutNewChan
                self.G_ChangeChannelTimeoutNewChan=3
                self.G_PhrozenFluiddRespondInfo("+T:0,3")
            else:
                self.G_PhrozenFluiddRespondInfo("串口1换料发送命令: T3")
                self.Cmds_AMSSerial1Send("T3")
                if self.G_ChangeChannelTimeoutOldChan<0 or self.G_ChangeChannelTimeoutNewChan<0:
                    self.G_ChangeChannelTimeoutOldChan=3
                else:
                    self.G_ChangeChannelTimeoutOldChan=self.G_ChangeChannelTimeoutNewChan
                self.G_ChangeChannelTimeoutNewChan=3
                self.G_PhrozenFluiddRespondInfo("+T:0,3")
        elif self.G_AMS1DeviceState["entry_state"] & bitmask8 ==8:#1000
            if self.G_AMS1DeviceState["park_state"] & bitmask1 == 1:#0001
                self.G_PhrozenFluiddRespondInfo("串口1换料发送命令: T1")
                self.Cmds_AMSSerial1Send("T1")
                if self.G_ChangeChannelTimeoutOldChan<0 or self.G_ChangeChannelTimeoutNewChan<0:
                    self.G_ChangeChannelTimeoutOldChan=1
                else:
                    self.G_ChangeChannelTimeoutOldChan=self.G_ChangeChannelTimeoutNewChan
                self.G_ChangeChannelTimeoutNewChan=1
                self.G_PhrozenFluiddRespondInfo("+T:0,1")
            elif self.G_AMS1DeviceState["park_state"] & bitmask2 == 2:#0010
                self.G_PhrozenFluiddRespondInfo("串口1换料发送命令: T2")
                self.Cmds_AMSSerial1Send("T2")
                if self.G_ChangeChannelTimeoutOldChan<0 or self.G_ChangeChannelTimeoutNewChan<0:
                    self.G_ChangeChannelTimeoutOldChan=2
                else:
                    self.G_ChangeChannelTimeoutOldChan=self.G_ChangeChannelTimeoutNewChan
                self.G_ChangeChannelTimeoutNewChan=2
                self.G_PhrozenFluiddRespondInfo("+T:0,2")
            elif self.G_AMS1DeviceState["park_state"] & bitmask4 == 4:#0100
                self.G_PhrozenFluiddRespondInfo("串口1换料发送命令: T3")
                self.Cmds_AMSSerial1Send("T3")
                if self.G_ChangeChannelTimeoutOldChan<0 or self.G_ChangeChannelTimeoutNewChan<0:
                    self.G_ChangeChannelTimeoutOldChan=3
                else:
                    self.G_ChangeChannelTimeoutOldChan=self.G_ChangeChannelTimeoutNewChan
                self.G_ChangeChannelTimeoutNewChan=3
                self.G_PhrozenFluiddRespondInfo("+T:0,3")
            elif self.G_AMS1DeviceState["park_state"] & bitmask8 == 8:#1000
                self.G_PhrozenFluiddRespondInfo("串口1换料发送命令: T4")
                self.Cmds_AMSSerial1Send("T4")
                if self.G_ChangeChannelTimeoutOldChan<0 or self.G_ChangeChannelTimeoutNewChan<0:
                    self.G_ChangeChannelTimeoutOldChan=4
                else:
                    self.G_ChangeChannelTimeoutOldChan=self.G_ChangeChannelTimeoutNewChan
                self.G_ChangeChannelTimeoutNewChan=4
                self.G_PhrozenFluiddRespondInfo("+T:0,4")
            else:
                self.G_PhrozenFluiddRespondInfo("串口1换料发送命令: T4")
                self.Cmds_AMSSerial1Send("T4")
                if self.G_ChangeChannelTimeoutOldChan<0 or self.G_ChangeChannelTimeoutNewChan<0:
                    self.G_ChangeChannelTimeoutOldChan=4
                else:
                    self.G_ChangeChannelTimeoutOldChan=self.G_ChangeChannelTimeoutNewChan
                self.G_ChangeChannelTimeoutNewChan=4
                #lancaigang240524：用于UIUX动态界面
                self.G_PhrozenFluiddRespondInfo("+T:0,4")




    ####################################
    #函数名称：
    #输入参数：
    #返 回 值:
    #功能描述：蓝才刚-20230830
    ####################################
    # P8 执行自动续料 Yes；"FA"；
    def Cmds_CmdP8(self,gcmd):
        # if not self.G_SerialPort1OpenFlag:
        #     self.G_PhrozenFluiddRespondInfo("AMS多色未连接，请先发送P28")
        #     return
        #lancaigang250522：不允许M3断料检测
        self.G_IfChangeFilaOngoing = True

        self.G_ProzenToolhead.dwell(2.0)

        self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_CmdP8]命令=P8" )


        self.G_PhrozenFluiddRespondInfo("当前模式")
        if self.G_AMSDeviceWorkMode == AMS_WORK_MODE_UNKNOW:
            self.G_PhrozenFluiddRespondInfo("+Mode:0,unkown")
        elif self.G_AMSDeviceWorkMode == AMS_WORK_MODE_MC:
            self.G_PhrozenFluiddRespondInfo("+Mode:1,MC")
        elif self.G_AMSDeviceWorkMode == AMS_WORK_MODE_MA:
            self.G_PhrozenFluiddRespondInfo("+Mode:2,MA")
        elif self.G_AMSDeviceWorkMode == AMS_WORK_MODE_FILA_RUNOUT:
            self.G_PhrozenFluiddRespondInfo("+Mode:3,RUNOUT")
        else:
            self.G_PhrozenFluiddRespondInfo("+Mode:-1,error")



        Lo_MCUSTM32Cmd = G_DictPhrozenCmdP8["mcu_cmd"][0]


        #lancaigang240511：恢复的时候，都初始化一下串口，防止热插拔AMS导致的串口通讯异常
        try:
            self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_CmdP8]重新初始化串口1")
            self.G_SerialPort1Obj = serial.Serial(self.G_Serialport1Define, SERIAL_PORT_BAUD, timeout=3)
            #串口打开成功
            if self.G_SerialPort1Obj is not None:
                if self.G_SerialPort1Obj.is_open:
                    self.G_SerialPort1OpenFlag = True
                    self.G_PhrozenFluiddRespondInfo("重新初始化串口1成功")
                    #lancaigang231213：打开串口
                    self.G_SerialPort1Obj.flushInput()  # clean serial write cache
                    self.G_SerialPort1Obj.flush()
                    self.G_PhrozenFluiddRespondInfo("串口1清空")
                    self.G_PhrozenFluiddRespondInfo("重新注册串口1回调函数")
                    self.G_SerialPort1RecvTimmer = self.G_PhrozenReactor.register_timer(self.Device_TimmerUart1Recv, self.G_PhrozenReactor.NOW)
        except:
            self.G_PhrozenFluiddRespondInfo("未能打开tty1口，请检查USB口或重启尝试")

        try:
            self.G_PhrozenFluiddRespondInfo("[(cmds.py)Cmds_PhrozenKlipperResume]重新初始化串口2")
            self.G_SerialPort2Obj = serial.Serial(self.G_Serialport2Define, SERIAL_PORT_BAUD, timeout=3)
            #串口打开成功
            if self.G_SerialPort2Obj is not None:
                if self.G_SerialPort2Obj.is_open:
                    self.G_SerialPort2OpenFlag = True
                    self.G_PhrozenFluiddRespondInfo("重新初始化串口2成功")
                    self.G_SerialPort2Obj.flushInput()  # clean serial write cache
                    self.G_SerialPort2Obj.flush()
                    self.G_PhrozenFluiddRespondInfo("串口2清空")
                    self.G_PhrozenFluiddRespondInfo("重新注册串口2回调函数")
                    self.G_SerialPort2RecvTimmer = self.G_PhrozenReactor.register_timer(self.Device_TimmerUart2Recv, self.G_PhrozenReactor.NOW)
        except:
            self.G_PhrozenFluiddRespondInfo("未能打开tty2口，请检查USB口或重启尝试")







        #lancaigang241030:
        if self.G_SerialPort1OpenFlag == True:
            self.G_PhrozenFluiddRespondInfo("串口1发送MA")
            self.Cmds_AMSSerial1Send("MA")

        if self.G_SerialPort2OpenFlag == True:
            self.G_PhrozenFluiddRespondInfo("串口2发送MA")
            self.Cmds_AMSSerial2Send("MA")


        #lancaigang240124：stm32主动上报，开启可以暂停1次
        self.STM32ReprotPauseFlag=0

        # #lancaigang240123：如果喷头有线材，不用发送FA到stm32，等待喷头打印完成之后暂停再发送FA，并自动恢复
        # if self.G_ToolheadIfHaveFilaFlag==False:
        #     self.G_PhrozenFluiddRespondInfo("喷头没有线材，FA")
        #     #lancaigang240115:延时2秒，防止粘包
        #     #time.sleep(2)
        #     self.G_ProzenToolhead.dwell(2.0)

        #     #lancaigang241030:
        #     if self.G_SerialPort1OpenFlag == True:
        #         self.Cmds_AMSSerial1Send("FA")
        #         self.G_PhrozenFluiddRespondInfo("串口1发送FA")
        #     elif self.G_SerialPort2OpenFlag == True:
        #         self.Cmds_AMSSerial2Send("FA")
        #         self.G_PhrozenFluiddRespondInfo("串口2发送FA")

        #     #lancaigang231229:封装函数
        #     self.Cmds_MARetryInFila(gcmd)
        #     #lancaigang240108：P8命令不用处理恢复命令
        #     self.G_M2MAModeResumeFlag=False



        # else:#喷头有线材
        #     self.G_PhrozenFluiddRespondInfo("喷头有线材，FB")
        #     #time.sleep(2)
        #     self.G_ProzenToolhead.dwell(2.0)

        #     #lancaigang241030:
        #     if self.G_SerialPort1OpenFlag == True:
        #         self.Cmds_AMSSerial1Send("FB")
        #         self.G_PhrozenFluiddRespondInfo("串口1发送FB")
        #     elif self.G_SerialPort2OpenFlag == True:
        #         self.Cmds_AMSSerial2Send("FB")
        #         self.G_PhrozenFluiddRespondInfo("串口2发送FB")

        #     self.G_M2MAModeResumeFlag=False



        # lancaigang241105：如果断电重启后，根本不知道当前喷头里面的线材是哪个AMS哪个通道的，所以先回退所有通道
        #lancaigang231205：不复位切线回退
        self.Cmds_MoveToCutFilaAndRollback(gcmd)


        # #lancaigang231205：复位切线回退
        # self.Cmds_MoveToCutFilaAndNotRollback(gcmd)
        # self.G_PhrozenFluiddRespondInfo("所有AMS先回退")
        # #lancaigang241030:
        # if self.G_SerialPort1OpenFlag == True:
        #     self.Cmds_AMSSerial1Send("AP")
        #     self.G_PhrozenFluiddRespondInfo("串口1发送命令：AP")
        # #lancaigang241030:
        # if self.G_SerialPort2OpenFlag == True:
        #     self.Cmds_AMSSerial2Send("AP")
        #     self.G_PhrozenFluiddRespondInfo("串口2发送命令：AP")
        # #lancaigang240913：把延時放到外面
        # self.G_ProzenToolhead.dwell(6.0)
        # #lancaigang231201：检查切线后旧通道线材是否正常退料，不正常则暂停
        # self.Cmds_CutFilaIfNormalCheck()


        if self.G_KlipperIfPaused == True:
            self.G_PhrozenFluiddRespondInfo("切线5秒了喷头还检测到线材，切刀异常了，请检查切刀，暂停klipper打印")
            #Lo_ChangeChannelIfSuccess = False
            self.G_PauseToLCDString="+PAUSE:8,%d,%d" % (self.G_ChangeChannelTimeoutOldChan,self.G_ChangeChannelTimeoutNewChan)
            self.G_PhrozenFluiddRespondInfo(self.G_PauseToLCDString)
            self.G_IfChangeFilaOngoing= False
            return


        #如果切线正常，则优先选择第一个AMS第一个通道进料
        if self.G_KlipperIfPaused == False:
            self.G_ProzenToolhead.dwell(2.0)

            if self.G_SerialPort1OpenFlag == True:
                try:
                    self.G_PhrozenFluiddRespondInfo("try;Lo_AMSDeviceStateRspInfo")
                    #获取多色主板详细状态
                    Lo_AMSDeviceStateRspInfo = self.Cmds_AMSSerialPort1SendWaitRsp("SD", sizeof(AMSDetailInfoBytes))
                    self.G_PhrozenFluiddRespondInfo("tty串口1接收: %s" % Lo_AMSDeviceStateRspInfo)
                    if len(Lo_AMSDeviceStateRspInfo) != sizeof(AMSDetailInfoBytes):
                        self.G_PhrozenFluiddRespondInfo("AMS1未响应，请检查AMS")
                        #lancaigang240412:AMS多色标签
                        self.G_AMSDevice1IfNormal=False
                    else:
                        self.G_PhrozenFluiddRespondInfo("AMS1连接成功")
                        self.G_PhrozenFluiddRespondInfo("self.G_AMSDevice1IfNormal=True")
                        #lancaigang240412:AMS多色标签
                        self.G_AMSDevice1IfNormal=True

                        Lo_AMSDeviceStateInfo = AMSDetailInfoBytes()
                        Lo_AMSDeviceStateInfo.whole[:] = bytearray(Lo_AMSDeviceStateRspInfo)
                        #self.G_PhrozenFluiddRespondInfo("%s" % SerialRxASCIIStr)
                        #python空字典
                        Lo_AMSDetailState = {}
                        self.G_AMS1DeviceState["dev_id"] = Lo_AMSDetailState["dev_id"] = Lo_AMSDeviceStateInfo.field.dev_id
                        self.G_AMS1DeviceState["active_dev_id"] = Lo_AMSDetailState["active_dev_id"] = Lo_AMSDeviceStateInfo.field.active_dev_id
                        self.G_AMS1DeviceState["dev_mode"] = Lo_AMSDetailState["dev_mode"] = Lo_AMSDeviceStateInfo.field.dev_mode
                        self.G_AMS1DeviceState["cache_empty"] = Lo_AMSDetailState["cache_empty"] = Lo_AMSDeviceStateInfo.field.cache_empty
                        #self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_CmdP114]缓冲器传感器空状态(bool)==%d" % Lo_AMSDeviceStateInfo.field.cache_empty)
                        self.G_AMS1DeviceState["cache_full"] = Lo_AMSDetailState["cache_full"] = Lo_AMSDeviceStateInfo.field.cache_full
                        self.G_PhrozenFluiddRespondInfo("缓冲器传感器满状态(bool)==%d" % Lo_AMSDeviceStateInfo.field.cache_full)
                        self.G_AMS1DeviceState["cache_exist"] = Lo_AMSDetailState["cache_exist"] = Lo_AMSDeviceStateInfo.field.cache_exist
                        #self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_CmdP114]缓冲器传感器线材状态(bool)==%d" % Lo_AMSDeviceStateInfo.field.cache_exist)
                        self.G_AMS1DeviceState["mc_state"] = Lo_AMSDetailState["mc_state"] = Lo_AMSDeviceStateInfo.field.mc_state
                        self.G_AMS1DeviceState["ma_state"] = Lo_AMSDetailState["ma_state"] = Lo_AMSDeviceStateInfo.field.ma_state
                        self.G_AMS1DeviceState["entry_state"] = Lo_AMSDetailState["entry_state"] = Lo_AMSDeviceStateInfo.field.entry_state
                        self.G_PhrozenFluiddRespondInfo("入口位传感器状态(bit位)==%d" % Lo_AMSDeviceStateInfo.field.entry_state)
                        self.G_AMS1DeviceState["park_state"] = Lo_AMSDetailState["park_state"] = Lo_AMSDeviceStateInfo.field.park_state
                        self.G_PhrozenFluiddRespondInfo("停靠位传感器状态(bit位)==%d" % Lo_AMSDeviceStateInfo.field.park_state)
                except:
                    self.G_PhrozenFluiddRespondInfo("except;Lo_AMSDeviceStateRspInfo")
                



            if self.G_SerialPort2OpenFlag == True:
                try:
                    self.G_PhrozenFluiddRespondInfo("try;Lo_AMSDeviceStateRspInfo")
                    Lo_AMSDeviceStateRspInfo = self.Cmds_AMSSerialPort2SendWaitRsp("SD", sizeof(AMSDetailInfoBytes))
                    self.G_PhrozenFluiddRespondInfo("tty串口2接收: %s" % Lo_AMSDeviceStateRspInfo)
                    if len(Lo_AMSDeviceStateRspInfo) != sizeof(AMSDetailInfoBytes):
                        self.G_PhrozenFluiddRespondInfo("AMS2未响应，请检查AMS")
                        #lancaigang240412:AMS多色标签
                        self.G_AMSDevice2IfNormal=False
                    else:
                        self.G_PhrozenFluiddRespondInfo("AMS2连接成功")
                        self.G_PhrozenFluiddRespondInfo("self.G_AMSDevice2IfNormal=True")
                        #lancaigang240412:AMS多色标签
                        self.G_AMSDevice2IfNormal=True

                        Lo_AMSDeviceStateInfo = AMSDetailInfoBytes()
                        Lo_AMSDeviceStateInfo.whole[:] = bytearray(Lo_AMSDeviceStateRspInfo)
                        #python空字典
                        Lo_AMSDetailState = {}
                        self.G_AMS2DeviceState["dev_id"] = Lo_AMSDetailState["dev_id"] = Lo_AMSDeviceStateInfo.field.dev_id
                        self.G_AMS2DeviceState["active_dev_id"] = Lo_AMSDetailState["active_dev_id"] = Lo_AMSDeviceStateInfo.field.active_dev_id
                        self.G_AMS2DeviceState["dev_mode"] = Lo_AMSDetailState["dev_mode"] = Lo_AMSDeviceStateInfo.field.dev_mode
                        self.G_AMS2DeviceState["cache_empty"] = Lo_AMSDetailState["cache_empty"] = Lo_AMSDeviceStateInfo.field.cache_empty
                        #self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_CmdP114]缓冲器传感器空状态(bool)==%d" % Lo_AMSDeviceStateInfo.field.cache_empty)
                        self.G_AMS2DeviceState["cache_full"] = Lo_AMSDetailState["cache_full"] = Lo_AMSDeviceStateInfo.field.cache_full
                        self.G_PhrozenFluiddRespondInfo("缓冲器传感器满状态(bool)==%d" % Lo_AMSDeviceStateInfo.field.cache_full)
                        self.G_AMS2DeviceState["cache_exist"] = Lo_AMSDetailState["cache_exist"] = Lo_AMSDeviceStateInfo.field.cache_exist
                        #self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_CmdP114]缓冲器传感器线材状态(bool)==%d" % Lo_AMSDeviceStateInfo.field.cache_exist)
                        self.G_AMS2DeviceState["mc_state"] = Lo_AMSDetailState["mc_state"] = Lo_AMSDeviceStateInfo.field.mc_state
                        self.G_AMS2DeviceState["ma_state"] = Lo_AMSDetailState["ma_state"] = Lo_AMSDeviceStateInfo.field.ma_state
                        self.G_AMS2DeviceState["entry_state"] = Lo_AMSDetailState["entry_state"] = Lo_AMSDeviceStateInfo.field.entry_state
                        self.G_PhrozenFluiddRespondInfo("入口位传感器状态(bit位)==%d" % Lo_AMSDeviceStateInfo.field.entry_state)
                        self.G_AMS2DeviceState["park_state"] = Lo_AMSDetailState["park_state"] = Lo_AMSDeviceStateInfo.field.park_state
                        self.G_PhrozenFluiddRespondInfo("停靠位传感器状态(bit位)==%d" % Lo_AMSDeviceStateInfo.field.park_state)

                except:
                    self.G_PhrozenFluiddRespondInfo("except;Lo_AMSDeviceStateRspInfo")




        self.G_ProzenToolhead.dwell(2.0)


        if self.G_AMSDevice1IfNormal==True:

            #lancaigang241106:优先第一个AMS第一个通道
            if self.G_AMS1DeviceState["entry_state"] > 0 or self.G_AMS1DeviceState["park_state"] > 0:
                self.G_PhrozenFluiddRespondInfo("第1个AMS有线材")
                #lancaigang250711：如果屏选择了颜色通道，以用户选择通道优先；
                # =====M3模式
                if self.G_AMSDeviceWorkMode == AMS_WORK_MODE_FILA_RUNOUT:#M3 M2
                    #if self.G_ChromaKitNum>0:
                    self.G_PhrozenFluiddRespondInfo("M3模式单色模型，用户选择了多色单个通道打印单色模型；")
                    if self.G_ChromaKitAccessT0>0:
                        self.Cmds_AMSSerial1Send("T%d" % self.G_ChromaKitAccessT0)
                        self.G_PhrozenFluiddRespondInfo("串口1发送命令: T%d" % self.G_ChromaKitAccessT0)
                        if self.G_ChangeChannelTimeoutOldChan<0 or self.G_ChangeChannelTimeoutNewChan<0:
                            self.G_ChangeChannelTimeoutOldChan=self.G_ChromaKitAccessT0
                        else:
                            self.G_ChangeChannelTimeoutOldChan=self.G_ChangeChannelTimeoutNewChan
                        self.G_ChangeChannelTimeoutNewChan=self.G_ChromaKitAccessT0
                    elif self.G_ChromaKitAccessT1>0:
                        self.Cmds_AMSSerial1Send("T%d" % self.G_ChromaKitAccessT1)
                        self.G_PhrozenFluiddRespondInfo("串口1发送命令: T%d" % self.G_ChromaKitAccessT1)
                        if self.G_ChangeChannelTimeoutOldChan<0 or self.G_ChangeChannelTimeoutNewChan<0:
                            self.G_ChangeChannelTimeoutOldChan=self.G_ChromaKitAccessT1
                        else:
                            self.G_ChangeChannelTimeoutOldChan=self.G_ChangeChannelTimeoutNewChan
                        self.G_ChangeChannelTimeoutNewChan=self.G_ChromaKitAccessT1
                    elif self.G_ChromaKitAccessT2>0:
                        self.Cmds_AMSSerial1Send("T%d" % self.G_ChromaKitAccessT2)
                        self.G_PhrozenFluiddRespondInfo("串口1发送命令: T%d" % self.G_ChromaKitAccessT2)
                        if self.G_ChangeChannelTimeoutOldChan<0 or self.G_ChangeChannelTimeoutNewChan<0:
                            self.G_ChangeChannelTimeoutOldChan=self.G_ChromaKitAccessT2
                        else:
                            self.G_ChangeChannelTimeoutOldChan=self.G_ChangeChannelTimeoutNewChan
                        self.G_ChangeChannelTimeoutNewChan=self.G_ChromaKitAccessT2
                    elif self.G_ChromaKitAccessT3>0:
                        self.Cmds_AMSSerial1Send("T%d" % self.G_ChromaKitAccessT3)
                        self.G_PhrozenFluiddRespondInfo("串口1发送命令: T%d" % self.G_ChromaKitAccessT3)
                        if self.G_ChangeChannelTimeoutOldChan<0 or self.G_ChangeChannelTimeoutNewChan<0:
                            self.G_ChangeChannelTimeoutOldChan=self.G_ChromaKitAccessT3
                        else:
                            self.G_ChangeChannelTimeoutOldChan=self.G_ChangeChannelTimeoutNewChan
                        self.G_ChangeChannelTimeoutNewChan=self.G_ChromaKitAccessT3
                    else:
                        self.G_PhrozenFluiddRespondInfo("M3模式单色模型，用户没有选择多色单个通道打印单色模型；自动选择通道打印单色模型")
                        self.Cmds_P8AMS1AutoSelectChannel()
                else:
                    self.G_PhrozenFluiddRespondInfo("其他模式单色模型，用户没有选择多色单个通道打印单色模型；自动选择通道打印单色模型")
                    self.Cmds_P8AMS1AutoSelectChannel()
            else:
                self.G_PhrozenFluiddRespondInfo("第1个AMS无线材")


        if self.G_AMSDevice2IfNormal==True:
            if self.G_AMS2DeviceState["entry_state"]>0:
                self.G_PhrozenFluiddRespondInfo("第2个AMS有线材")

        self.Cmds_PrintMode(self.G_AMSDeviceWorkMode)

         #lancaigang231229:封装函数，等待进料
        self.Cmds_MARetryInFila(gcmd)

        #lancaigang240108：P8命令不用处理恢复命令
        self.G_M2MAModeResumeFlag=False

####################################
    #函数名称：
    #输入参数：
    #返 回 值:
    #功能描述：蓝才刚-20230830
    ####################################
    def Cmds_CmdP8Infila(self):
        #self.G_ProzenToolhead.dwell(2.0)

        self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_CmdP8Infila]" )

        self.G_PhrozenFluiddRespondInfo("当前模式")
        if self.G_AMSDeviceWorkMode == AMS_WORK_MODE_UNKNOW:
            self.G_PhrozenFluiddRespondInfo("+Mode:0,unkown")
        elif self.G_AMSDeviceWorkMode == AMS_WORK_MODE_MC:
            self.G_PhrozenFluiddRespondInfo("+Mode:1,MC")
        elif self.G_AMSDeviceWorkMode == AMS_WORK_MODE_MA:
            self.G_PhrozenFluiddRespondInfo("+Mode:2,MA")
        elif self.G_AMSDeviceWorkMode == AMS_WORK_MODE_FILA_RUNOUT:
            self.G_PhrozenFluiddRespondInfo("+Mode:3,RUNOUT")
        else:
            self.G_PhrozenFluiddRespondInfo("+Mode:-1,error")

        #lancaigang250619:检查AMS是否重新连接成功
        self.Cmds_USBConnectErrorCheck()
        #lancaigang241030:
        if self.G_SerialPort1OpenFlag == True:
            self.Cmds_AMSSerial1Send("MB")
            self.G_PhrozenFluiddRespondInfo("串口1发送MB")
        elif self.G_SerialPort2OpenFlag == True:
            self.Cmds_AMSSerial2Send("MB")
            self.G_PhrozenFluiddRespondInfo("串口2发送MB")

        #lancaigang240124：stm32主动上报，开启可以暂停1次
        self.STM32ReprotPauseFlag=0

        self.G_ProzenToolhead.dwell(2.5)

        if self.G_SerialPort1OpenFlag == True:
            try:
                self.G_PhrozenFluiddRespondInfo("try;Lo_AMSDeviceStateRspInfo")
                #获取多色主板详细状态
                Lo_AMSDeviceStateRspInfo = self.Cmds_AMSSerialPort1SendWaitRsp("SD", sizeof(AMSDetailInfoBytes))
                self.G_PhrozenFluiddRespondInfo("tty串口1接收: %s" % Lo_AMSDeviceStateRspInfo)
                if len(Lo_AMSDeviceStateRspInfo) != sizeof(AMSDetailInfoBytes):
                    self.G_PhrozenFluiddRespondInfo("AMS1未响应，请检查AMS")
                    #lancaigang240412:AMS多色标签
                    self.G_AMSDevice1IfNormal=False
                else:
                    self.G_PhrozenFluiddRespondInfo("AMS1连接成功")
                    self.G_PhrozenFluiddRespondInfo("self.G_AMSDevice1IfNormal=True")
                    #lancaigang240412:AMS多色标签
                    self.G_AMSDevice1IfNormal=True

                    Lo_AMSDeviceStateInfo = AMSDetailInfoBytes()
                    Lo_AMSDeviceStateInfo.whole[:] = bytearray(Lo_AMSDeviceStateRspInfo)
                    #self.G_PhrozenFluiddRespondInfo("%s" % SerialRxASCIIStr)
                    #python空字典
                    Lo_AMSDetailState = {}
                    self.G_AMS1DeviceState["dev_id"] = Lo_AMSDetailState["dev_id"] = Lo_AMSDeviceStateInfo.field.dev_id
                    self.G_AMS1DeviceState["active_dev_id"] = Lo_AMSDetailState["active_dev_id"] = Lo_AMSDeviceStateInfo.field.active_dev_id
                    self.G_AMS1DeviceState["dev_mode"] = Lo_AMSDetailState["dev_mode"] = Lo_AMSDeviceStateInfo.field.dev_mode
                    self.G_AMS1DeviceState["cache_empty"] = Lo_AMSDetailState["cache_empty"] = Lo_AMSDeviceStateInfo.field.cache_empty
                    #self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_CmdP114]缓冲器传感器空状态(bool)==%d" % Lo_AMSDeviceStateInfo.field.cache_empty)
                    self.G_AMS1DeviceState["cache_full"] = Lo_AMSDetailState["cache_full"] = Lo_AMSDeviceStateInfo.field.cache_full
                    self.G_PhrozenFluiddRespondInfo("缓冲器传感器满状态(bool)==%d" % Lo_AMSDeviceStateInfo.field.cache_full)
                    self.G_AMS1DeviceState["cache_exist"] = Lo_AMSDetailState["cache_exist"] = Lo_AMSDeviceStateInfo.field.cache_exist
                    #self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_CmdP114]缓冲器传感器线材状态(bool)==%d" % Lo_AMSDeviceStateInfo.field.cache_exist)
                    self.G_AMS1DeviceState["mc_state"] = Lo_AMSDetailState["mc_state"] = Lo_AMSDeviceStateInfo.field.mc_state
                    self.G_AMS1DeviceState["ma_state"] = Lo_AMSDetailState["ma_state"] = Lo_AMSDeviceStateInfo.field.ma_state
                    self.G_AMS1DeviceState["entry_state"] = Lo_AMSDetailState["entry_state"] = Lo_AMSDeviceStateInfo.field.entry_state
                    self.G_PhrozenFluiddRespondInfo("入口位传感器状态(bit位)==%d" % Lo_AMSDeviceStateInfo.field.entry_state)
                    self.G_AMS1DeviceState["park_state"] = Lo_AMSDetailState["park_state"] = Lo_AMSDeviceStateInfo.field.park_state
                    self.G_PhrozenFluiddRespondInfo("停靠位传感器状态(bit位)==%d" % Lo_AMSDeviceStateInfo.field.park_state)
            except:
                self.G_PhrozenFluiddRespondInfo("except;Lo_AMSDeviceStateRspInfo")




        if self.G_SerialPort2OpenFlag == True:
            try:
                self.G_PhrozenFluiddRespondInfo("try;Lo_AMSDeviceStateRspInfo")
                Lo_AMSDeviceStateRspInfo = self.Cmds_AMSSerialPort2SendWaitRsp("SD", sizeof(AMSDetailInfoBytes))
                self.G_PhrozenFluiddRespondInfo("tty串口2接收: %s" % Lo_AMSDeviceStateRspInfo)
                if len(Lo_AMSDeviceStateRspInfo) != sizeof(AMSDetailInfoBytes):
                    self.G_PhrozenFluiddRespondInfo("AMS2未响应，请检查AMS")
                    #lancaigang240412:AMS多色标签
                    self.G_AMSDevice2IfNormal=False
                else:
                    self.G_PhrozenFluiddRespondInfo("AMS2连接成功")
                    self.G_PhrozenFluiddRespondInfo("self.G_AMSDevice2IfNormal=True")
                    #lancaigang240412:AMS多色标签
                    self.G_AMSDevice2IfNormal=True

                    Lo_AMSDeviceStateInfo = AMSDetailInfoBytes()
                    Lo_AMSDeviceStateInfo.whole[:] = bytearray(Lo_AMSDeviceStateRspInfo)
                    #python空字典
                    Lo_AMSDetailState = {}
                    self.G_AMS2DeviceState["dev_id"] = Lo_AMSDetailState["dev_id"] = Lo_AMSDeviceStateInfo.field.dev_id
                    self.G_AMS2DeviceState["active_dev_id"] = Lo_AMSDetailState["active_dev_id"] = Lo_AMSDeviceStateInfo.field.active_dev_id
                    self.G_AMS2DeviceState["dev_mode"] = Lo_AMSDetailState["dev_mode"] = Lo_AMSDeviceStateInfo.field.dev_mode
                    self.G_AMS2DeviceState["cache_empty"] = Lo_AMSDetailState["cache_empty"] = Lo_AMSDeviceStateInfo.field.cache_empty
                    #self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_CmdP114]缓冲器传感器空状态(bool)==%d" % Lo_AMSDeviceStateInfo.field.cache_empty)
                    self.G_AMS2DeviceState["cache_full"] = Lo_AMSDetailState["cache_full"] = Lo_AMSDeviceStateInfo.field.cache_full
                    self.G_PhrozenFluiddRespondInfo("缓冲器传感器满状态(bool)==%d" % Lo_AMSDeviceStateInfo.field.cache_full)
                    self.G_AMS2DeviceState["cache_exist"] = Lo_AMSDetailState["cache_exist"] = Lo_AMSDeviceStateInfo.field.cache_exist
                    #self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_CmdP114]缓冲器传感器线材状态(bool)==%d" % Lo_AMSDeviceStateInfo.field.cache_exist)
                    self.G_AMS2DeviceState["mc_state"] = Lo_AMSDetailState["mc_state"] = Lo_AMSDeviceStateInfo.field.mc_state
                    self.G_AMS2DeviceState["ma_state"] = Lo_AMSDetailState["ma_state"] = Lo_AMSDeviceStateInfo.field.ma_state
                    self.G_AMS2DeviceState["entry_state"] = Lo_AMSDetailState["entry_state"] = Lo_AMSDeviceStateInfo.field.entry_state
                    self.G_PhrozenFluiddRespondInfo("入口位传感器状态(bit位)==%d" % Lo_AMSDeviceStateInfo.field.entry_state)
                    self.G_AMS2DeviceState["park_state"] = Lo_AMSDetailState["park_state"] = Lo_AMSDeviceStateInfo.field.park_state
                    self.G_PhrozenFluiddRespondInfo("停靠位传感器状态(bit位)==%d" % Lo_AMSDeviceStateInfo.field.park_state)
            except:
                self.G_PhrozenFluiddRespondInfo("except;Lo_AMSDeviceStateRspInfo")
                
        # if self.G_AMSDevice1IfNormal==True:
        #     #lancaigang241106:优先第一个AMS第一个通道
        #     if self.G_AMS1DeviceState["entry_state"] > 0 or self.G_AMS1DeviceState["park_state"] > 0:
        #         self.G_PhrozenFluiddRespondInfo("第1个AMS有线材")
        #         # if self.G_AMS1DeviceState["entry_state"]==0 or self.G_AMS1DeviceState["park_state"]==0:
        #         #     self.G_PhrozenFluiddRespondInfo("串口1换料发送命令: T1")
        #         #     self.Cmds_AMSSerial1Send("T1")
        #         #     self.G_ChangeChannelTimeoutOldChan=self.G_ChangeChannelTimeoutNewChan
        #         #     self.G_ChangeChannelTimeoutNewChan=1
        #         #     #lancaigang240524：用于UIUX动态界面
        #         #     self.G_PhrozenFluiddRespondInfo("+T:0,1")
        #         if self.G_AMS1DeviceState["entry_state"]==1:#0001
        #         #if self.G_AMS1DeviceState["park_state"]==1:#0001
        #             self.G_PhrozenFluiddRespondInfo("串口1换料发送命令: T1")
        #             self.Cmds_AMSSerial1Send("T1")
        #             self.G_ChangeChannelTimeoutOldChan=self.G_ChangeChannelTimeoutNewChan
        #             self.G_ChangeChannelTimeoutNewChan=1
        #             self.G_PhrozenFluiddRespondInfo("+T:0,1")
        #         elif self.G_AMS1DeviceState["entry_state"]==2:#0010
        #             if self.G_AMS1DeviceState["park_state"]==1:#0001
        #                 self.G_PhrozenFluiddRespondInfo("串口1换料发送命令: T1")
        #                 self.Cmds_AMSSerial1Send("T1")
        #                 self.G_ChangeChannelTimeoutOldChan=self.G_ChangeChannelTimeoutNewChan
        #                 self.G_ChangeChannelTimeoutNewChan=1
        #                 self.G_PhrozenFluiddRespondInfo("+T:0,1")
        #             elif self.G_AMS1DeviceState["park_state"]==2:#0010
        #                 self.G_PhrozenFluiddRespondInfo("串口1换料发送命令: T2")
        #                 self.Cmds_AMSSerial1Send("T2")
        #                 self.G_ChangeChannelTimeoutOldChan=self.G_ChangeChannelTimeoutNewChan
        #                 self.G_ChangeChannelTimeoutNewChan=2
        #                 self.G_PhrozenFluiddRespondInfo("+T:0,2")
        #             else:
        #                 self.G_PhrozenFluiddRespondInfo("串口1换料发送命令: T2")
        #                 self.Cmds_AMSSerial1Send("T2")
        #                 self.G_ChangeChannelTimeoutOldChan=self.G_ChangeChannelTimeoutNewChan
        #                 self.G_ChangeChannelTimeoutNewChan=2
        #                 self.G_PhrozenFluiddRespondInfo("+T:0,2")
        #         elif self.G_AMS1DeviceState["entry_state"]==3:#0011
        #             self.G_PhrozenFluiddRespondInfo("串口1换料发送命令: T1")
        #             self.Cmds_AMSSerial1Send("T1")
        #             self.G_ChangeChannelTimeoutOldChan=self.G_ChangeChannelTimeoutNewChan
        #             self.G_ChangeChannelTimeoutNewChan=1
        #             #lancaigang240524：用于UIUX动态界面
        #             self.G_PhrozenFluiddRespondInfo("+T:0,1")
        #         elif self.G_AMS1DeviceState["entry_state"]==4:#0100
        #             if self.G_AMS1DeviceState["park_state"]==1:#0001
        #                 self.G_PhrozenFluiddRespondInfo("串口1换料发送命令: T1")
        #                 self.Cmds_AMSSerial1Send("T1")
        #                 self.G_ChangeChannelTimeoutOldChan=self.G_ChangeChannelTimeoutNewChan
        #                 self.G_ChangeChannelTimeoutNewChan=1
        #                 self.G_PhrozenFluiddRespondInfo("+T:0,1")
        #             elif self.G_AMS1DeviceState["park_state"]==2:#0010
        #                 self.G_PhrozenFluiddRespondInfo("串口1换料发送命令: T2")
        #                 self.Cmds_AMSSerial1Send("T2")
        #                 self.G_ChangeChannelTimeoutOldChan=self.G_ChangeChannelTimeoutNewChan
        #                 self.G_ChangeChannelTimeoutNewChan=2
        #                 self.G_PhrozenFluiddRespondInfo("+T:0,2")
        #             elif self.G_AMS1DeviceState["park_state"]==3:#0011
        #                 self.G_PhrozenFluiddRespondInfo("串口1换料发送命令: T1")
        #                 self.Cmds_AMSSerial1Send("T1")
        #                 self.G_ChangeChannelTimeoutOldChan=self.G_ChangeChannelTimeoutNewChan
        #                 self.G_ChangeChannelTimeoutNewChan=1
        #                 self.G_PhrozenFluiddRespondInfo("+T:0,1")
        #             elif self.G_AMS1DeviceState["park_state"]==4:#0100
        #                 self.G_PhrozenFluiddRespondInfo("串口1换料发送命令: T3")
        #                 self.Cmds_AMSSerial1Send("T3")
        #                 self.G_ChangeChannelTimeoutOldChan=self.G_ChangeChannelTimeoutNewChan
        #                 self.G_ChangeChannelTimeoutNewChan=3
        #                 self.G_PhrozenFluiddRespondInfo("+T:0,3")
        #             elif self.G_AMS1DeviceState["park_state"]==5:#0101
        #                 self.G_PhrozenFluiddRespondInfo("串口1换料发送命令: T1")
        #                 self.Cmds_AMSSerial1Send("T1")
        #                 self.G_ChangeChannelTimeoutOldChan=self.G_ChangeChannelTimeoutNewChan
        #                 self.G_ChangeChannelTimeoutNewChan=1
        #                 self.G_PhrozenFluiddRespondInfo("+T:0,1")
        #             elif self.G_AMS1DeviceState["park_state"]==6:#0110
        #                 self.G_PhrozenFluiddRespondInfo("串口1换料发送命令: T2")
        #                 self.Cmds_AMSSerial1Send("T2")
        #                 self.G_ChangeChannelTimeoutOldChan=self.G_ChangeChannelTimeoutNewChan
        #                 self.G_ChangeChannelTimeoutNewChan=2
        #                 self.G_PhrozenFluiddRespondInfo("+T:0,2")
        #             elif self.G_AMS1DeviceState["park_state"]==7:#0111
        #                 self.G_PhrozenFluiddRespondInfo("串口1换料发送命令: T1")
        #                 self.Cmds_AMSSerial1Send("T1")
        #                 self.G_ChangeChannelTimeoutOldChan=self.G_ChangeChannelTimeoutNewChan
        #                 self.G_ChangeChannelTimeoutNewChan=1
        #                 self.G_PhrozenFluiddRespondInfo("+T:0,1")
        #             else:
        #                 self.G_PhrozenFluiddRespondInfo("串口1换料发送命令: T3")
        #                 self.Cmds_AMSSerial1Send("T3")
        #                 self.G_ChangeChannelTimeoutOldChan=self.G_ChangeChannelTimeoutNewChan
        #                 self.G_ChangeChannelTimeoutNewChan=3
        #                 self.G_PhrozenFluiddRespondInfo("+T:0,3")
        #         elif self.G_AMS1DeviceState["entry_state"]==5:#0101
        #             self.G_PhrozenFluiddRespondInfo("串口1换料发送命令: T1")
        #             self.Cmds_AMSSerial1Send("T1")
        #             self.G_ChangeChannelTimeoutOldChan=self.G_ChangeChannelTimeoutNewChan
        #             self.G_ChangeChannelTimeoutNewChan=1
        #             #lancaigang240524：用于UIUX动态界面
        #             self.G_PhrozenFluiddRespondInfo("+T:0,1")
        #         elif self.G_AMS1DeviceState["entry_state"]==6:#0110
        #             if self.G_AMS1DeviceState["park_state"]==1:#0001
        #                 self.G_PhrozenFluiddRespondInfo("串口1换料发送命令: T1")
        #                 self.Cmds_AMSSerial1Send("T1")
        #                 self.G_ChangeChannelTimeoutOldChan=self.G_ChangeChannelTimeoutNewChan
        #                 self.G_ChangeChannelTimeoutNewChan=1
        #                 self.G_PhrozenFluiddRespondInfo("+T:0,1")
        #             elif self.G_AMS1DeviceState["park_state"]==2:#0010
        #                 self.G_PhrozenFluiddRespondInfo("串口1换料发送命令: T2")
        #                 self.Cmds_AMSSerial1Send("T2")
        #                 self.G_ChangeChannelTimeoutOldChan=self.G_ChangeChannelTimeoutNewChan
        #                 self.G_ChangeChannelTimeoutNewChan=2
        #                 self.G_PhrozenFluiddRespondInfo("+T:0,2")
        #             else:
        #                 self.G_PhrozenFluiddRespondInfo("串口1换料发送命令: T2")
        #                 self.Cmds_AMSSerial1Send("T2")
        #                 self.G_ChangeChannelTimeoutOldChan=self.G_ChangeChannelTimeoutNewChan
        #                 self.G_ChangeChannelTimeoutNewChan=2
        #                 #lancaigang240524：用于UIUX动态界面
        #                 self.G_PhrozenFluiddRespondInfo("+T:0,2")
        #         elif self.G_AMS1DeviceState["entry_state"]==7:#0111
        #             self.G_PhrozenFluiddRespondInfo("串口1换料发送命令: T1")
        #             self.Cmds_AMSSerial1Send("T1")
        #             self.G_ChangeChannelTimeoutOldChan=self.G_ChangeChannelTimeoutNewChan
        #             self.G_ChangeChannelTimeoutNewChan=1
        #             #lancaigang240524：用于UIUX动态界面
        #             self.G_PhrozenFluiddRespondInfo("+T:0,1")
        #         elif self.G_AMS1DeviceState["entry_state"]==8:#1000
        #             if self.G_AMS1DeviceState["park_state"]==1:#0001
        #                 self.G_PhrozenFluiddRespondInfo("串口1换料发送命令: T1")
        #                 self.Cmds_AMSSerial1Send("T1")
        #                 self.G_ChangeChannelTimeoutOldChan=self.G_ChangeChannelTimeoutNewChan
        #                 self.G_ChangeChannelTimeoutNewChan=1
        #                 self.G_PhrozenFluiddRespondInfo("+T:0,1")
        #             elif self.G_AMS1DeviceState["park_state"]==2:#0010
        #                 self.G_PhrozenFluiddRespondInfo("串口1换料发送命令: T2")
        #                 self.Cmds_AMSSerial1Send("T2")
        #                 self.G_ChangeChannelTimeoutOldChan=self.G_ChangeChannelTimeoutNewChan
        #                 self.G_ChangeChannelTimeoutNewChan=2
        #                 self.G_PhrozenFluiddRespondInfo("+T:0,2")
        #             elif self.G_AMS1DeviceState["park_state"]==3:#0011
        #                 self.G_PhrozenFluiddRespondInfo("串口1换料发送命令: T1")
        #                 self.Cmds_AMSSerial1Send("T1")
        #                 self.G_ChangeChannelTimeoutOldChan=self.G_ChangeChannelTimeoutNewChan
        #                 self.G_ChangeChannelTimeoutNewChan=1
        #                 self.G_PhrozenFluiddRespondInfo("+T:0,1")
        #             elif self.G_AMS1DeviceState["park_state"]==4:#0100
        #                 self.G_PhrozenFluiddRespondInfo("串口1换料发送命令: T3")
        #                 self.Cmds_AMSSerial1Send("T3")
        #                 self.G_ChangeChannelTimeoutOldChan=self.G_ChangeChannelTimeoutNewChan
        #                 self.G_ChangeChannelTimeoutNewChan=3
        #                 self.G_PhrozenFluiddRespondInfo("+T:0,3")
        #             elif self.G_AMS1DeviceState["park_state"]==5:#0101
        #                 self.G_PhrozenFluiddRespondInfo("串口1换料发送命令: T1")
        #                 self.Cmds_AMSSerial1Send("T1")
        #                 self.G_ChangeChannelTimeoutOldChan=self.G_ChangeChannelTimeoutNewChan
        #                 self.G_ChangeChannelTimeoutNewChan=1
        #                 self.G_PhrozenFluiddRespondInfo("+T:0,1")
        #             elif self.G_AMS1DeviceState["park_state"]==6:#0110
        #                 self.G_PhrozenFluiddRespondInfo("串口1换料发送命令: T2")
        #                 self.Cmds_AMSSerial1Send("T2")
        #                 self.G_ChangeChannelTimeoutOldChan=self.G_ChangeChannelTimeoutNewChan
        #                 self.G_ChangeChannelTimeoutNewChan=2
        #                 self.G_PhrozenFluiddRespondInfo("+T:0,2")
        #             elif self.G_AMS1DeviceState["park_state"]==7:#0111
        #                 self.G_PhrozenFluiddRespondInfo("串口1换料发送命令: T1")
        #                 self.Cmds_AMSSerial1Send("T1")
        #                 self.G_ChangeChannelTimeoutOldChan=self.G_ChangeChannelTimeoutNewChan
        #                 self.G_ChangeChannelTimeoutNewChan=1
        #                 self.G_PhrozenFluiddRespondInfo("+T:0,1")
        #             elif self.G_AMS1DeviceState["park_state"]==8:#1000
        #                 self.G_PhrozenFluiddRespondInfo("串口1换料发送命令: T4")
        #                 self.Cmds_AMSSerial1Send("T4")
        #                 self.G_ChangeChannelTimeoutOldChan=self.G_ChangeChannelTimeoutNewChan
        #                 self.G_ChangeChannelTimeoutNewChan=4
        #                 self.G_PhrozenFluiddRespondInfo("+T:0,4")
        #             elif self.G_AMS1DeviceState["park_state"]==9:#1001
        #                 self.G_PhrozenFluiddRespondInfo("串口1换料发送命令: T1")
        #                 self.Cmds_AMSSerial1Send("T1")
        #                 self.G_ChangeChannelTimeoutOldChan=self.G_ChangeChannelTimeoutNewChan
        #                 self.G_ChangeChannelTimeoutNewChan=1
        #                 self.G_PhrozenFluiddRespondInfo("+T:0,1")
        #             elif self.G_AMS1DeviceState["park_state"]==10:#1010
        #                 self.G_PhrozenFluiddRespondInfo("串口1换料发送命令: T2")
        #                 self.Cmds_AMSSerial1Send("T2")
        #                 self.G_ChangeChannelTimeoutOldChan=self.G_ChangeChannelTimeoutNewChan
        #                 self.G_ChangeChannelTimeoutNewChan=2
        #                 self.G_PhrozenFluiddRespondInfo("+T:0,2")
        #             elif self.G_AMS1DeviceState["park_state"]==11:#1011
        #                 self.G_PhrozenFluiddRespondInfo("串口1换料发送命令: T1")
        #                 self.Cmds_AMSSerial1Send("T1")
        #                 self.G_ChangeChannelTimeoutOldChan=self.G_ChangeChannelTimeoutNewChan
        #                 self.G_ChangeChannelTimeoutNewChan=1
        #                 self.G_PhrozenFluiddRespondInfo("+T:0,1")
        #             elif self.G_AMS1DeviceState["park_state"]==12:#1100
        #                 self.G_PhrozenFluiddRespondInfo("串口1换料发送命令: T3")
        #                 self.Cmds_AMSSerial1Send("T3")
        #                 self.G_ChangeChannelTimeoutOldChan=self.G_ChangeChannelTimeoutNewChan
        #                 self.G_ChangeChannelTimeoutNewChan=3
        #                 self.G_PhrozenFluiddRespondInfo("+T:0,3")
        #             elif self.G_AMS1DeviceState["park_state"]==13:#1101
        #                 self.G_PhrozenFluiddRespondInfo("串口1换料发送命令: T1")
        #                 self.Cmds_AMSSerial1Send("T1")
        #                 self.G_ChangeChannelTimeoutOldChan=self.G_ChangeChannelTimeoutNewChan
        #                 self.G_ChangeChannelTimeoutNewChan=1
        #                 self.G_PhrozenFluiddRespondInfo("+T:0,1")
        #             elif self.G_AMS1DeviceState["park_state"]==14:#1110
        #                 self.G_PhrozenFluiddRespondInfo("串口1换料发送命令: T2")
        #                 self.Cmds_AMSSerial1Send("T2")
        #                 self.G_ChangeChannelTimeoutOldChan=self.G_ChangeChannelTimeoutNewChan
        #                 self.G_ChangeChannelTimeoutNewChan=2
        #                 self.G_PhrozenFluiddRespondInfo("+T:0,2")
        #             elif self.G_AMS1DeviceState["park_state"]==15:#1111
        #                 self.G_PhrozenFluiddRespondInfo("串口1换料发送命令: T1")
        #                 self.Cmds_AMSSerial1Send("T1")
        #                 self.G_ChangeChannelTimeoutOldChan=self.G_ChangeChannelTimeoutNewChan
        #                 self.G_ChangeChannelTimeoutNewChan=1
        #                 self.G_PhrozenFluiddRespondInfo("+T:0,1")
        #             else:
        #                 self.G_PhrozenFluiddRespondInfo("串口1换料发送命令: T4")
        #                 self.Cmds_AMSSerial1Send("T4")
        #                 self.G_ChangeChannelTimeoutOldChan=self.G_ChangeChannelTimeoutNewChan
        #                 self.G_ChangeChannelTimeoutNewChan=4
        #                 #lancaigang240524：用于UIUX动态界面
        #                 self.G_PhrozenFluiddRespondInfo("+T:0,4")
        #         elif self.G_AMS1DeviceState["entry_state"]==9:#1001
        #             self.G_PhrozenFluiddRespondInfo("串口1换料发送命令: T1")
        #             self.Cmds_AMSSerial1Send("T1")
        #             self.G_ChangeChannelTimeoutOldChan=self.G_ChangeChannelTimeoutNewChan
        #             self.G_ChangeChannelTimeoutNewChan=1
        #             #lancaigang240524：用于UIUX动态界面
        #             self.G_PhrozenFluiddRespondInfo("+T:0,1")
        #         elif self.G_AMS1DeviceState["entry_state"]==10:#1010
        #             if self.G_AMS1DeviceState["park_state"]==1:#0001
        #                 self.G_PhrozenFluiddRespondInfo("串口1换料发送命令: T1")
        #                 self.Cmds_AMSSerial1Send("T1")
        #                 self.G_ChangeChannelTimeoutOldChan=self.G_ChangeChannelTimeoutNewChan
        #                 self.G_ChangeChannelTimeoutNewChan=1
        #                 self.G_PhrozenFluiddRespondInfo("+T:0,1")
        #             elif self.G_AMS1DeviceState["park_state"]==2:#0010
        #                 self.G_PhrozenFluiddRespondInfo("串口1换料发送命令: T2")
        #                 self.Cmds_AMSSerial1Send("T2")
        #                 self.G_ChangeChannelTimeoutOldChan=self.G_ChangeChannelTimeoutNewChan
        #                 self.G_ChangeChannelTimeoutNewChan=2
        #                 self.G_PhrozenFluiddRespondInfo("+T:0,2")
        #             else:
        #                 self.G_PhrozenFluiddRespondInfo("串口1换料发送命令: T2")
        #                 self.Cmds_AMSSerial1Send("T2")
        #                 self.G_ChangeChannelTimeoutOldChan=self.G_ChangeChannelTimeoutNewChan
        #                 self.G_ChangeChannelTimeoutNewChan=2
        #                 #lancaigang240524：用于UIUX动态界面
        #                 self.G_PhrozenFluiddRespondInfo("+T:0,2")
        #         elif self.G_AMS1DeviceState["entry_state"]==11:#1011
        #             self.G_PhrozenFluiddRespondInfo("串口1换料发送命令: T1")
        #             self.Cmds_AMSSerial1Send("T1")
        #             self.G_ChangeChannelTimeoutOldChan=self.G_ChangeChannelTimeoutNewChan
        #             self.G_ChangeChannelTimeoutNewChan=1
        #             #lancaigang240524：用于UIUX动态界面
        #             self.G_PhrozenFluiddRespondInfo("+T:0,1")
        #         elif self.G_AMS1DeviceState["entry_state"]==12:#1100
        #             if self.G_AMS1DeviceState["park_state"]==1:#0001
        #                 self.G_PhrozenFluiddRespondInfo("串口1换料发送命令: T1")
        #                 self.Cmds_AMSSerial1Send("T1")
        #                 self.G_ChangeChannelTimeoutOldChan=self.G_ChangeChannelTimeoutNewChan
        #                 self.G_ChangeChannelTimeoutNewChan=1
        #                 self.G_PhrozenFluiddRespondInfo("+T:0,1")
        #             elif self.G_AMS1DeviceState["park_state"]==2:#0010
        #                 self.G_PhrozenFluiddRespondInfo("串口1换料发送命令: T2")
        #                 self.Cmds_AMSSerial1Send("T2")
        #                 self.G_ChangeChannelTimeoutOldChan=self.G_ChangeChannelTimeoutNewChan
        #                 self.G_ChangeChannelTimeoutNewChan=2
        #                 self.G_PhrozenFluiddRespondInfo("+T:0,2")
        #             elif self.G_AMS1DeviceState["park_state"]==3:#0011
        #                 self.G_PhrozenFluiddRespondInfo("串口1换料发送命令: T1")
        #                 self.Cmds_AMSSerial1Send("T1")
        #                 self.G_ChangeChannelTimeoutOldChan=self.G_ChangeChannelTimeoutNewChan
        #                 self.G_ChangeChannelTimeoutNewChan=1
        #                 self.G_PhrozenFluiddRespondInfo("+T:0,1")
        #             elif self.G_AMS1DeviceState["park_state"]==4:#0100
        #                 self.G_PhrozenFluiddRespondInfo("串口1换料发送命令: T3")
        #                 self.Cmds_AMSSerial1Send("T3")
        #                 self.G_ChangeChannelTimeoutOldChan=self.G_ChangeChannelTimeoutNewChan
        #                 self.G_ChangeChannelTimeoutNewChan=3
        #                 self.G_PhrozenFluiddRespondInfo("+T:0,3")
        #             elif self.G_AMS1DeviceState["park_state"]==5:#0101
        #                 self.G_PhrozenFluiddRespondInfo("串口1换料发送命令: T1")
        #                 self.Cmds_AMSSerial1Send("T1")
        #                 self.G_ChangeChannelTimeoutOldChan=self.G_ChangeChannelTimeoutNewChan
        #                 self.G_ChangeChannelTimeoutNewChan=1
        #                 self.G_PhrozenFluiddRespondInfo("+T:0,1")
        #             elif self.G_AMS1DeviceState["park_state"]==6:#0110
        #                 self.G_PhrozenFluiddRespondInfo("串口1换料发送命令: T2")
        #                 self.Cmds_AMSSerial1Send("T2")
        #                 self.G_ChangeChannelTimeoutOldChan=self.G_ChangeChannelTimeoutNewChan
        #                 self.G_ChangeChannelTimeoutNewChan=2
        #                 self.G_PhrozenFluiddRespondInfo("+T:0,2")
        #             elif self.G_AMS1DeviceState["park_state"]==7:#0111
        #                 self.G_PhrozenFluiddRespondInfo("串口1换料发送命令: T1")
        #                 self.Cmds_AMSSerial1Send("T1")
        #                 self.G_ChangeChannelTimeoutOldChan=self.G_ChangeChannelTimeoutNewChan
        #                 self.G_ChangeChannelTimeoutNewChan=1
        #                 self.G_PhrozenFluiddRespondInfo("+T:0,1")
        #             else:
        #                 self.G_PhrozenFluiddRespondInfo("串口1换料发送命令: T3")
        #                 self.Cmds_AMSSerial1Send("T3")
        #                 self.G_ChangeChannelTimeoutOldChan=self.G_ChangeChannelTimeoutNewChan
        #                 self.G_ChangeChannelTimeoutNewChan=3
        #                 self.G_PhrozenFluiddRespondInfo("+T:0,3")
        #         elif self.G_AMS1DeviceState["entry_state"]==13:#1101
        #             self.G_PhrozenFluiddRespondInfo("串口1换料发送命令: T1")
        #             self.Cmds_AMSSerial1Send("T1")
        #             self.G_ChangeChannelTimeoutOldChan=self.G_ChangeChannelTimeoutNewChan
        #             self.G_ChangeChannelTimeoutNewChan=1
        #             #lancaigang240524：用于UIUX动态界面
        #             self.G_PhrozenFluiddRespondInfo("+T:0,1")
        #         elif self.G_AMS1DeviceState["entry_state"]==14:#1110
        #             if self.G_AMS1DeviceState["park_state"]==1:#0001
        #                 self.G_PhrozenFluiddRespondInfo("串口1换料发送命令: T1")
        #                 self.Cmds_AMSSerial1Send("T1")
        #                 self.G_ChangeChannelTimeoutOldChan=self.G_ChangeChannelTimeoutNewChan
        #                 self.G_ChangeChannelTimeoutNewChan=1
        #                 self.G_PhrozenFluiddRespondInfo("+T:0,1")
        #             elif self.G_AMS1DeviceState["park_state"]==2:#0010
        #                 self.G_PhrozenFluiddRespondInfo("串口1换料发送命令: T2")
        #                 self.Cmds_AMSSerial1Send("T2")
        #                 self.G_ChangeChannelTimeoutOldChan=self.G_ChangeChannelTimeoutNewChan
        #                 self.G_ChangeChannelTimeoutNewChan=2
        #                 self.G_PhrozenFluiddRespondInfo("+T:0,2")
        #             else:
        #                 self.G_PhrozenFluiddRespondInfo("串口1换料发送命令: T2")
        #                 self.Cmds_AMSSerial1Send("T2")
        #                 self.G_ChangeChannelTimeoutOldChan=self.G_ChangeChannelTimeoutNewChan
        #                 self.G_ChangeChannelTimeoutNewChan=2
        #                 #lancaigang240524：用于UIUX动态界面
        #                 self.G_PhrozenFluiddRespondInfo("+T:0,2")
        #         elif self.G_AMS1DeviceState["entry_state"]==15:#1111
        #             self.G_PhrozenFluiddRespondInfo("串口1换料发送命令: T1")
        #             self.Cmds_AMSSerial1Send("T1")
        #             self.G_ChangeChannelTimeoutOldChan=self.G_ChangeChannelTimeoutNewChan
        #             self.G_ChangeChannelTimeoutNewChan=1
        #             #lancaigang240524：用于UIUX动态界面
        #             self.G_PhrozenFluiddRespondInfo("+T:0,1")
        if self.G_AMSDevice1IfNormal==True:
            bitmask1=0b0001
            bitmask2=0b0010
            bitmask4=0b0100
            bitmask8=0b1000
            #lancaigang241106:优先第一个AMS第一个通道
            if self.G_AMS1DeviceState["entry_state"] > 0 or self.G_AMS1DeviceState["park_state"] > 0:
                self.G_PhrozenFluiddRespondInfo("第1个AMS有线材")
                if self.G_AMS1DeviceState["entry_state"] == 0:
                    if self.G_AMS1DeviceState["park_state"] & bitmask1 == 1:#0001
                        self.G_PhrozenFluiddRespondInfo("串口1换料发送命令: T1")
                        self.Cmds_AMSSerial1Send("T1")
                        self.G_ChangeChannelTimeoutOldChan=self.G_ChangeChannelTimeoutNewChan
                        self.G_ChangeChannelTimeoutNewChan=1
                        self.G_PhrozenFluiddRespondInfo("+T:0,1")
                    elif self.G_AMS1DeviceState["park_state"] & bitmask2 == 2:#0010
                        self.G_PhrozenFluiddRespondInfo("串口1换料发送命令: T2")
                        self.Cmds_AMSSerial1Send("T2")
                        self.G_ChangeChannelTimeoutOldChan=self.G_ChangeChannelTimeoutNewChan
                        self.G_ChangeChannelTimeoutNewChan=2
                        self.G_PhrozenFluiddRespondInfo("+T:0,2")
                    elif self.G_AMS1DeviceState["park_state"] & bitmask4 == 4:#0100
                        self.G_PhrozenFluiddRespondInfo("串口1换料发送命令: T3")
                        self.Cmds_AMSSerial1Send("T3")
                        self.G_ChangeChannelTimeoutOldChan=self.G_ChangeChannelTimeoutNewChan
                        self.G_ChangeChannelTimeoutNewChan=3
                        self.G_PhrozenFluiddRespondInfo("+T:0,3")
                    elif self.G_AMS1DeviceState["park_state"] & bitmask8 == 8:#1000
                        self.G_PhrozenFluiddRespondInfo("串口1换料发送命令: T4")
                        self.Cmds_AMSSerial1Send("T4")
                        self.G_ChangeChannelTimeoutOldChan=self.G_ChangeChannelTimeoutNewChan
                        self.G_ChangeChannelTimeoutNewChan=4
                        self.G_PhrozenFluiddRespondInfo("+T:0,4")
                    else:
                        self.G_PhrozenFluiddRespondInfo("无线材")
                elif self.G_AMS1DeviceState["entry_state"] & bitmask1 == 1:#0001
                    self.G_PhrozenFluiddRespondInfo("串口1换料发送命令: T1")
                    self.Cmds_AMSSerial1Send("T1")
                    self.G_ChangeChannelTimeoutOldChan=self.G_ChangeChannelTimeoutNewChan
                    self.G_ChangeChannelTimeoutNewChan=1
                    self.G_PhrozenFluiddRespondInfo("+T:0,1")
                elif self.G_AMS1DeviceState["entry_state"] & bitmask2 == 2:#0010
                    if self.G_AMS1DeviceState["park_state"] & bitmask1 == 1:#0001
                        self.G_PhrozenFluiddRespondInfo("串口1换料发送命令: T1")
                        self.Cmds_AMSSerial1Send("T1")
                        self.G_ChangeChannelTimeoutOldChan=self.G_ChangeChannelTimeoutNewChan
                        self.G_ChangeChannelTimeoutNewChan=1
                        self.G_PhrozenFluiddRespondInfo("+T:0,1")
                    elif self.G_AMS1DeviceState["park_state"] & bitmask2 == 2:#0010
                        self.G_PhrozenFluiddRespondInfo("串口1换料发送命令: T2")
                        self.Cmds_AMSSerial1Send("T2")
                        self.G_ChangeChannelTimeoutOldChan=self.G_ChangeChannelTimeoutNewChan
                        self.G_ChangeChannelTimeoutNewChan=2
                        self.G_PhrozenFluiddRespondInfo("+T:0,2")
                    else:
                        self.G_PhrozenFluiddRespondInfo("串口1换料发送命令: T2")
                        self.Cmds_AMSSerial1Send("T2")
                        self.G_ChangeChannelTimeoutOldChan=self.G_ChangeChannelTimeoutNewChan
                        self.G_ChangeChannelTimeoutNewChan=2
                        self.G_PhrozenFluiddRespondInfo("+T:0,2")
                elif self.G_AMS1DeviceState["entry_state"] & bitmask4 == 4:#0100
                    if self.G_AMS1DeviceState["park_state"] & bitmask1 == 1:#0001
                        self.G_PhrozenFluiddRespondInfo("串口1换料发送命令: T1")
                        self.Cmds_AMSSerial1Send("T1")
                        self.G_ChangeChannelTimeoutOldChan=self.G_ChangeChannelTimeoutNewChan
                        self.G_ChangeChannelTimeoutNewChan=1
                        self.G_PhrozenFluiddRespondInfo("+T:0,1")
                    elif self.G_AMS1DeviceState["park_state"] & bitmask2 == 2:#0010
                        self.G_PhrozenFluiddRespondInfo("串口1换料发送命令: T2")
                        self.Cmds_AMSSerial1Send("T2")
                        self.G_ChangeChannelTimeoutOldChan=self.G_ChangeChannelTimeoutNewChan
                        self.G_ChangeChannelTimeoutNewChan=2
                        self.G_PhrozenFluiddRespondInfo("+T:0,2")
                    elif self.G_AMS1DeviceState["park_state"] & bitmask4 == 4:#0100
                        self.G_PhrozenFluiddRespondInfo("串口1换料发送命令: T3")
                        self.Cmds_AMSSerial1Send("T3")
                        self.G_ChangeChannelTimeoutOldChan=self.G_ChangeChannelTimeoutNewChan
                        self.G_ChangeChannelTimeoutNewChan=3
                        self.G_PhrozenFluiddRespondInfo("+T:0,3")
                    else:
                        self.G_PhrozenFluiddRespondInfo("串口1换料发送命令: T3")
                        self.Cmds_AMSSerial1Send("T3")
                        self.G_ChangeChannelTimeoutOldChan=self.G_ChangeChannelTimeoutNewChan
                        self.G_ChangeChannelTimeoutNewChan=3
                        self.G_PhrozenFluiddRespondInfo("+T:0,3")
                elif self.G_AMS1DeviceState["entry_state"] & bitmask8 ==8:#1000
                    if self.G_AMS1DeviceState["park_state"] & bitmask1 == 1:#0001
                        self.G_PhrozenFluiddRespondInfo("串口1换料发送命令: T1")
                        self.Cmds_AMSSerial1Send("T1")
                        self.G_ChangeChannelTimeoutOldChan=self.G_ChangeChannelTimeoutNewChan
                        self.G_ChangeChannelTimeoutNewChan=1
                        self.G_PhrozenFluiddRespondInfo("+T:0,1")
                    elif self.G_AMS1DeviceState["park_state"] & bitmask2 == 2:#0010
                        self.G_PhrozenFluiddRespondInfo("串口1换料发送命令: T2")
                        self.Cmds_AMSSerial1Send("T2")
                        self.G_ChangeChannelTimeoutOldChan=self.G_ChangeChannelTimeoutNewChan
                        self.G_ChangeChannelTimeoutNewChan=2
                        self.G_PhrozenFluiddRespondInfo("+T:0,2")
                    elif self.G_AMS1DeviceState["park_state"] & bitmask4 == 4:#0100
                        self.G_PhrozenFluiddRespondInfo("串口1换料发送命令: T3")
                        self.Cmds_AMSSerial1Send("T3")
                        self.G_ChangeChannelTimeoutOldChan=self.G_ChangeChannelTimeoutNewChan
                        self.G_ChangeChannelTimeoutNewChan=3
                        self.G_PhrozenFluiddRespondInfo("+T:0,3")
                    elif self.G_AMS1DeviceState["park_state"] & bitmask8 == 8:#1000
                        self.G_PhrozenFluiddRespondInfo("串口1换料发送命令: T4")
                        self.Cmds_AMSSerial1Send("T4")
                        self.G_ChangeChannelTimeoutOldChan=self.G_ChangeChannelTimeoutNewChan
                        self.G_ChangeChannelTimeoutNewChan=4
                        self.G_PhrozenFluiddRespondInfo("+T:0,4")
                    else:
                        self.G_PhrozenFluiddRespondInfo("串口1换料发送命令: T4")
                        self.Cmds_AMSSerial1Send("T4")
                        self.G_ChangeChannelTimeoutOldChan=self.G_ChangeChannelTimeoutNewChan
                        self.G_ChangeChannelTimeoutNewChan=4
                        #lancaigang240524：用于UIUX动态界面
                        self.G_PhrozenFluiddRespondInfo("+T:0,4")
            else:
                self.G_PhrozenFluiddRespondInfo("第1个AMS无线材")

        self.Cmds_PrintMode(self.G_AMSDeviceWorkMode)

        if self.G_AMSDevice2IfNormal==True:
            if self.G_AMS2DeviceState["entry_state"]>0:
                self.G_PhrozenFluiddRespondInfo("第2个AMS有线材")

        #lancaigang240108：P8命令不用处理恢复命令
        self.G_M2MAModeResumeFlag=False


    ####################################
    #函数名称：
    #输入参数：
    #返 回 值:
    #功能描述：蓝才刚-20230830
    ####################################
    # P4 紧急停止设备；紧急停止Stop命令(次优先级)："SP"；
    def Cmds_CmdP4(self, gcmd):
        # if not self.G_SerialPort1OpenFlag:
        #     self.G_PhrozenFluiddRespondInfo("AMS多色未连接，请先发送P28")
        #     return
        
        self.G_PhrozenFluiddRespondInfo("[(cmds.py)Cmds_CmdP4]命令:紧急停止")

        mcu_cmd = G_DictPhrozenCmdP4["mcu_cmd"][0]
        self.G_PhrozenFluiddRespondInfo("mcu命令")



        #lancaigang241031:
        if self.G_SerialPort1OpenFlag == True:
            #lancaigang231207：stm32暂停
            self.Cmds_AMSSerial1Send(mcu_cmd)
            self.G_PhrozenFluiddRespondInfo("串口1发送命令")
        #lancaigang241030:
        if self.G_SerialPort2OpenFlag == True:
            self.Cmds_AMSSerial2Send(mcu_cmd)
            self.G_PhrozenFluiddRespondInfo("串口2发送命令")

        #lancaigang240125：
        #lancaigang231207：klipper暂停+stm32暂停
        #klipper主动暂停
        

        if self.G_KlipperInPausing == False:
            self.G_PhrozenFluiddRespondInfo("不在暂停中，允许新的暂停")
            #lancaigang250607:
            self.G_PhrozenFluiddRespondInfo("启用快速暂停")
            self.G_KlipperQuickPause = True
            #klipper主动暂停
            self.Cmds_PhrozenKlipperPause(None)
        else:
            self.G_PhrozenFluiddRespondInfo("暂停中，不允许新的暂停")
        # logging.info("SendCmd: %s" % mcu_cmd)
        # logging.info("stop dev running at once")



    ####################################
    #函数名称：
    #输入参数：
    #返 回 值:
    #功能描述：蓝才刚-20230830
    ####################################
    # P2 A1 所有线料后退到停靠位打印待位置 Yes；====="AP";
    # P2 A2；退出所有线材 Yes；"CL";
    # P2 A3 切断线材
    # P2 A4 切断线材并回退线材
    # P2 A7 切断线材并回退线材，不检测暂停，只用于打印完成AMS回退所有线材
    def Cmds_CmdP2(self, gcmd):
        # if not self.G_SerialPort1OpenFlag:
        #     self.G_PhrozenFluiddRespondInfo("AMS多色未连接，请先发送P28")
        #     return
        
        self.G_PhrozenFluiddRespondInfo("[(cmds.py)Cmds_CmdP2]命令='%s'" % (gcmd.get_commandline(),))


        #获取命令参数
        params = gcmd.get_command_parameters()


        self.G_PhrozenFluiddRespondInfo("当前模式")
        if self.G_AMSDeviceWorkMode == AMS_WORK_MODE_UNKNOW:
            self.G_PhrozenFluiddRespondInfo("+Mode:0,unkown")
        elif self.G_AMSDeviceWorkMode == AMS_WORK_MODE_MC:
            self.G_PhrozenFluiddRespondInfo("+Mode:1,MC")
        elif self.G_AMSDeviceWorkMode == AMS_WORK_MODE_MA:
            self.G_PhrozenFluiddRespondInfo("+Mode:2,MA")
        elif self.G_AMSDeviceWorkMode == AMS_WORK_MODE_FILA_RUNOUT:
            self.G_PhrozenFluiddRespondInfo("+Mode:3,RUNOUT")
        else:
            self.G_PhrozenFluiddRespondInfo("+Mode:-1,error")


        # if not "A" in params:
        #     return


        #time.sleep(0.5)
        self.G_PhrozenFluiddRespondInfo("延时0.5")
        self.G_ProzenToolhead.dwell(0.5)



        #lancaigang250619:检查AMS是否重新连接成功
        self.Cmds_USBConnectErrorCheck()




        if "A" in params:
            action = int(params["A"])
            if not action in [1, 2, 3,4,5,6,7]:
                raise gcmd.error("无效参数命令;cmd '%s', that must is A[1/2/3/4/5/6/7]" % (gcmd.get_commandline(),))
            # P2 A1 所有线料后退到停靠位打印待位置 Yes；====="AP";
            if action == 1:
                #lancaigang250515：单机打多色，不处理P2A?
                if self.G_P0M1MCNoneAMS == 1:
                    self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_CmdP2]单机打多色，不处理P2A?")
                    return
                #lancaigang250427：
                if self.G_AMSDeviceWorkMode==AMS_WORK_MODE_FILA_RUNOUT:
                    self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_CmdP2]P0M3单色模式，不处理P2 A1")
                    return
                if self.G_AMSDeviceWorkMode==AMS_WORK_MODE_MA:
                    self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_CmdP2]P0M2MA单色续料模式，不处理P2 A1")
                    return


                self.G_PhrozenFluiddRespondInfo("命令='%s'；所有线材回退到停靠位" % (gcmd.get_commandline(),))
                #lancaigang240524：用于UIUX动态界面
                self.G_PhrozenFluiddRespondInfo("+P2A1:0,%d" % self.G_ChangeChannelTimeoutNewChan)
                #lancaigang231201：打印完成后，如果复位，可能会碰到打印好的模型，不能复位但又需要切线回退线材
                
                #lancaigang250323：
                if self.G_ToolheadIfHaveFilaFlag==True:
                    #lancaigang231205：复位切线回退
                    #self.Cmds_MoveToCutFilaAndNotRollback(gcmd)
                    self.G_PhrozenFluiddRespondInfo("喷头有线材")
                    #lancaigang20231024复位切线；不能碰到模型
                    #lancaigang240109：喷头有线材才允许切线
                    #if self.G_ToolheadIfHaveFilaFlag==True:
                    #lancaigang240319：切线之前准备动作
                    #self.Cmds_MoveToCutFilaPrepare()
                    self.Cmds_MoveToCutFilaAbsolutePositionNotReset(gcmd)
                    #lancaigang241031:
                    if self.G_SerialPort1OpenFlag == True:
                        self.Cmds_AMSSerial1Send("AP")
                        self.G_PhrozenFluiddRespondInfo("串口1发送命令: AP；所有通道线材回退到停靠位")
                    #lancaigang241030:
                    if self.G_SerialPort2OpenFlag == True:
                        self.Cmds_AMSSerial2Send("AP")
                        self.G_PhrozenFluiddRespondInfo("串口2发送命令: AP；所有通道线材回退到停靠位")

                    self.G_PhrozenFluiddRespondInfo("外部宏命令-PRZ_WAITINGAREA-等待区")
                    command_string = """
                        PRZ_WAITINGAREA
                        """
                    self.G_PhrozenGCode.run_script_from_command(command_string)
                    self.G_PhrozenFluiddRespondInfo("外部宏命令-PRZ_WAITINGAREA；command_string='%s'" % command_string)

                    #lancaigang240913：把延時放到外面
                    self.G_ProzenToolhead.dwell(6.0)

                    #lancaigang231201：检查切线后是否正常退料，不正常则暂停
                    #lancaigang231225：里面延时可能导致klipper打印完成homing归位异常，先屏蔽
                    #lancaigang240224：需要检查是否切线成功
                    self.Cmds_CutFilaIfNormalCheck()
                else:
                    #lancaigang241031:
                    if self.G_SerialPort1OpenFlag == True:
                        self.Cmds_AMSSerial1Send("AP")
                        self.G_PhrozenFluiddRespondInfo("串口1发送命令: AP；所有通道线材回退到停靠位")
                    #lancaigang241030:
                    if self.G_SerialPort2OpenFlag == True:
                        self.Cmds_AMSSerial2Send("AP")
                        self.G_PhrozenFluiddRespondInfo("串口2发送命令: AP；所有通道线材回退到停靠位")

                    self.G_PhrozenFluiddRespondInfo("外部宏命令-PRZ_WAITINGAREA-等待区")
                    command_string = """
                        PRZ_WAITINGAREA
                        """
                    self.G_PhrozenGCode.run_script_from_command(command_string)
                    self.G_PhrozenFluiddRespondInfo("外部宏命令-PRZ_WAITINGAREA；command_string='%s'" % command_string)






                #lancaigang240113：清除手动命令标志
                self.ManualCmdFlag=False


                # self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_CmdP2]全部归位并切线")
                # command_string = """
                # PG28
                # """
                # self.G_PhrozenGCode.run_script_from_command(command_string)

                #lancaigang240524：用于UIUX动态界面
                self.G_PhrozenFluiddRespondInfo("+P2A1:1,%d" % self.G_ChangeChannelTimeoutNewChan)

                #time.sleep(0.5)
                self.G_PhrozenFluiddRespondInfo("延时0.5")
                self.G_ProzenToolhead.dwell(0.5)

                #lancaigang250409：手動進料則讀取AMS狀態
                self.Cmds_CmdP114(None)

                #time.sleep(0.5)
                self.G_PhrozenFluiddRespondInfo("延时0.5")
                self.G_ProzenToolhead.dwell(0.5)

                return





            # P2 A2；退出所有线材 Yes；"CL";
            if action == 2:
                #lancaigang250515：单机打多色，不处理P2A?
                if self.G_P0M1MCNoneAMS == 1:
                    self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_CmdP2]单机打多色，不处理P2A?")
                    return
                #lancaigang250427：
                if self.G_AMSDeviceWorkMode==AMS_WORK_MODE_FILA_RUNOUT:
                    self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_CmdP2]单色模式，不处理P2 A2")
                    return
                self.G_PhrozenFluiddRespondInfo("命令='%s'；所有线材完全退出" % (gcmd.get_commandline(),))
                #lancaigang240524：用于UIUX动态界面
                self.G_PhrozenFluiddRespondInfo("+P2A2:0,%d" % self.G_ChangeChannelTimeoutNewChan)
                #lancaigang240319：切线之前准备动作
                #self.Cmds_MoveToCutFilaPrepare()


                if self.G_ToolheadIfHaveFilaFlag:
                    #lancaigang231205：复位切线回退
                    self.Cmds_MoveToCutFilaAndNotRollback(gcmd)
                    self.G_PhrozenFluiddRespondInfo("喷头有线材，所有AMS先回退")
                    # self.Cmds_AMSSerial1Send("G%d" % self.G_ChangeChannelTimeoutOldChan)
                    # self.G_PhrozenFluiddRespondInfo("G%d" % self.G_ChangeChannelTimeoutOldChan)
                    # self.G_PhrozenFluiddRespondInfo("AMS旧通道先回退一段距离: G%d" % self.G_ChangeChannelTimeoutOldChan)
                    #lancaigang241030:
                    if self.G_SerialPort1OpenFlag == True:
                        self.Cmds_AMSSerial1Send("AP")
                        self.G_PhrozenFluiddRespondInfo("串口1发送命令：AP")
                    #lancaigang241030:
                    if self.G_SerialPort2OpenFlag == True:
                        self.Cmds_AMSSerial2Send("AP")
                        self.G_PhrozenFluiddRespondInfo("串口2发送命令：AP")

                    self.G_ProzenToolhead.dwell(0.5)

                    # self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_CmdP1]外部宏命令-PG101")
                    # command_string = """
                    #     PG101
                    #     """
                    # self.G_PhrozenGCode.run_script_from_command(command_string)
                    # self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_CmdP1]外部宏命令-到指定待料区位置等待吐料；command_string='%s'" % command_string)
                    # self.IfDoPG102Flag=True

                    #lancaigang240913：把延時放到外面
                    self.G_ProzenToolhead.dwell(6.0)
                    #lancaigang231201：检查切线后旧通道线材是否正常退料，不正常则暂停
                    self.Cmds_CutFilaIfNormalCheck()
                    if self.G_KlipperIfPaused == True:
                            self.G_PhrozenFluiddRespondInfo("切线5秒了喷头还检测到线材，切刀异常了，请检查切刀，暂停klipper打印")
                            #Lo_ChangeChannelIfSuccess = False
                            return



                #lancaigang250619:检查AMS是否重新连接成功
                self.Cmds_USBConnectErrorCheck()
                #lancaigang241031:
                if self.G_SerialPort1OpenFlag == True:
                    self.Cmds_AMSSerial1Send("CL")
                    self.G_PhrozenFluiddRespondInfo("串口1发送命令: CL")
                #lancaigang241030:
                if self.G_SerialPort2OpenFlag == True:
                    self.Cmds_AMSSerial2Send("CL")
                    self.G_PhrozenFluiddRespondInfo("串口2发送命令: CL")




                # #lancaigang240913：把延時放到外面
                # self.G_ProzenToolhead.dwell(6.0)
                # #lancaigang231201：检查切线后是否正常退料，不正常则暂停
                # self.Cmds_CutFilaIfNormalCheck()

                #lancaigang240524：用于UIUX动态界面
                self.G_PhrozenFluiddRespondInfo("+P2A2:1,%d" % self.G_ChangeChannelTimeoutNewChan)

                #time.sleep(0.5)
                self.G_PhrozenFluiddRespondInfo("延时0.5")
                self.G_ProzenToolhead.dwell(0.5)

                return






            # P2 A3 切断线材
            if action == 3:
                # #lancaigang250515：单机打多色，不处理P2A?
                # if self.G_P0M1MCNoneAMS == 1:
                #     self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_CmdP2]单机打多色，不处理P2A?")
                #     return
                self.G_PhrozenFluiddRespondInfo("命令='%s'；切线" % (gcmd.get_commandline(),))
                #lancaigang240524：用于UIUX动态界面
                self.G_PhrozenFluiddRespondInfo("+P2A3:0,%d" % self.G_ChangeChannelTimeoutNewChan)
                #lancaigang240319：切线之前准备动作
                #self.Cmds_MoveToCutFilaPrepare()

                self.Cmds_MoveToCutFilaAbsolutePositionNotReset(gcmd)
                #lancaigang240524：用于UIUX动态界面
                self.G_PhrozenFluiddRespondInfo("+P2A3:1,%d" % self.G_ChangeChannelTimeoutNewChan)

                #lancaigang250104：P2A3标志位
                self.G_P2A3Flag = 1
                #lancaigang240516：防止粘包
                #time.sleep(0.5)
                self.G_PhrozenFluiddRespondInfo("延时0.5")
                self.G_ProzenToolhead.dwell(0.5)


            # P2 A4 切断线材并回退线材
            if action == 4:
                #lancaigang250515：单机打多色，不处理P2A?
                if self.G_P0M1MCNoneAMS == 1:
                    self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_CmdP2]单机打多色，不处理P2A?")
                    return
                self.G_PhrozenFluiddRespondInfo("命令='%s'；切线并回退线材到停靠位" % (gcmd.get_commandline(),))
                #lancaigang240524：用于UIUX动态界面
                self.G_PhrozenFluiddRespondInfo("+P2A4:0,%d" % self.G_ChangeChannelTimeoutNewChan)
                #lancaigang240319：切线之前准备动作
                #self.Cmds_MoveToCutFilaPrepare()

                self.Cmds_MoveToCutFilaAbsolutePositionNotReset(gcmd)
                #lancaigang240524：用于UIUX动态界面
                self.G_PhrozenFluiddRespondInfo("+P2A4:1,%d" % self.G_ChangeChannelTimeoutNewChan)






            # P2 A5 打印完成切断线材并回退线材，不能碰到模型
            if action == 5:
                #lancaigang250515：单机打多色，不处理P2A?
                if self.G_P0M1MCNoneAMS == 1:
                    self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_CmdP2]单机打多色，不处理P2A?")
                    return
                self.G_PhrozenFluiddRespondInfo("命令='%s'打印完成切断线材并回退线材，不能碰到模型" % (gcmd.get_commandline(),))
                #lancaigang240524：用于UIUX动态界面
                self.G_PhrozenFluiddRespondInfo("+P2A5:0,%d" % self.G_ChangeChannelTimeoutNewChan)
                #lancaigang240319：切线之前准备动作
                #self.Cmds_MoveToCutFilaPrepare()

                self.Cmds_MoveToCutFilaAbsolutePositionNotReset(gcmd)
                #lancaigang240524：用于UIUX动态界面
                self.G_PhrozenFluiddRespondInfo("+P2A5:0,%d" % self.G_ChangeChannelTimeoutNewChan)


            # P2 A6 复位并切线回退
            if action == 6:
                #lancaigang250515：单机打多色，不处理P2A?
                if self.G_P0M1MCNoneAMS == 1:
                    self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_CmdP2]单机打多色，不处理P2A?")
                    return
                self.G_PhrozenFluiddRespondInfo("命令='%s'；复位并切线回退" % (gcmd.get_commandline(),))
                #lancaigang240524：用于UIUX动态界面
                self.G_PhrozenFluiddRespondInfo("+P2A6:0,%d" % self.G_ChangeChannelTimeoutNewChan)
                #lancaigang231201：打印完成后，如果复位，可能会碰到打印好的模型，不能复位但又需要切线回退线材
                
                #lancaigang250323：
                if self.G_ToolheadIfHaveFilaFlag==True:
                    #lancaigang231205：复位切线回退
                    #self.Cmds_MoveToCutFilaAndNotRollback(gcmd)
                    self.G_PhrozenFluiddRespondInfo("喷头有线材，复位XY切线并回退")
                    #self.Cmds_MoveToCutFilaAndNotRollback(gcmd)
                    self.Cmds_MoveToCutFilaAndHomingXY(gcmd)
                    #lancaigang241031:
                    if self.G_SerialPort1OpenFlag == True:
                        self.Cmds_AMSSerial1Send("AP")
                        self.G_PhrozenFluiddRespondInfo("串口1发送命令: AP；所有通道线材回退到停靠位")
                    #lancaigang241030:
                    if self.G_SerialPort2OpenFlag == True:
                        self.Cmds_AMSSerial2Send("AP")
                        self.G_PhrozenFluiddRespondInfo("串口2发送命令: AP；所有通道线材回退到停靠位")

                    # self.G_PhrozenFluiddRespondInfo("外部宏命令-PRZ_WAITINGAREA-等待区")
                    # command_string = """
                    #     PRZ_WAITINGAREA
                    #     """
                    # self.G_PhrozenGCode.run_script_from_command(command_string)
                    # self.G_PhrozenFluiddRespondInfo("外部宏命令-PRZ_WAITINGAREA；command_string='%s'" % command_string)

                    #lancaigang240913：把延時放到外面
                    self.G_ProzenToolhead.dwell(6.0)

                    #lancaigang231201：检查切线后是否正常退料，不正常则暂停
                    #lancaigang231225：里面延时可能导致klipper打印完成homing归位异常，先屏蔽
                    #lancaigang240224：需要检查是否切线成功
                    self.Cmds_CutFilaIfNormalCheck()
                else:
                    #lancaigang241031:
                    if self.G_SerialPort1OpenFlag == True:
                        self.Cmds_AMSSerial1Send("AP")
                        self.G_PhrozenFluiddRespondInfo("串口1发送命令: AP；所有通道线材回退到停靠位")
                    #lancaigang241030:
                    if self.G_SerialPort2OpenFlag == True:
                        self.Cmds_AMSSerial2Send("AP")
                        self.G_PhrozenFluiddRespondInfo("串口2发送命令: AP；所有通道线材回退到停靠位")

                    # self.G_PhrozenFluiddRespondInfo("外部宏命令-PRZ_WAITINGAREA-等待区")
                    # command_string = """
                    #     PRZ_WAITINGAREA
                    #     """
                    # self.G_PhrozenGCode.run_script_from_command(command_string)
                    # self.G_PhrozenFluiddRespondInfo("外部宏命令-PRZ_WAITINGAREA；command_string='%s'" % command_string)






                #lancaigang240113：
                self.ManualCmdFlag=True


                # self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_CmdP2]全部归位并切线")
                # command_string = """
                # PG28
                # """
                # self.G_PhrozenGCode.run_script_from_command(command_string)

                #lancaigang240524：用于UIUX动态界面
                self.G_PhrozenFluiddRespondInfo("+P2A6:1,%d" % self.G_ChangeChannelTimeoutNewChan)

                #time.sleep(0.5)
                self.G_PhrozenFluiddRespondInfo("延时0.5")
                self.G_ProzenToolhead.dwell(0.5)

                #lancaigang250409：手動進料則讀取AMS狀態
                #self.Cmds_CmdP114(None)

                #time.sleep(0.5)
                self.G_PhrozenFluiddRespondInfo("延时0.5")
                self.G_ProzenToolhead.dwell(0.5)

                return

            # P2 A7 切断线材并回退线材，不检测暂停，只用于打印完成AMS回退所有线材
            if action == 7:
                #lancaigang251014：打印完成；清空标志位；
                self.G_P0M1MCNoneAMS = 0
                # #lancaigang250515：单机打多色，不处理P2A?
                # if self.G_P0M1MCNoneAMS == 1:
                #     self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_CmdP2]单机打多色，不处理P2A?")
                #     return
                #lancaigang240524：用于UIUX动态界面
                self.G_PhrozenFluiddRespondInfo("+P2A7:0,%d" % self.G_ChangeChannelTimeoutNewChan)
                
                #lancaigang250427：
                if self.G_AMSDeviceWorkMode==AMS_WORK_MODE_UNKNOW:
                    self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_CmdP2]P0 M0未知模式")
                    #return
                
                #lancaigang250618:单色和单色续料断料检测退出
                self.G_P0M3Flag = False
                self.G_P0M2MAStartPrintFlag=0

                #lancaigang250619:检查AMS是否重新连接成功
                self.Cmds_USBConnectErrorCheck()

                #lancaigang250427：
                if self.G_AMSDeviceWorkMode==AMS_WORK_MODE_FILA_RUNOUT:
                    self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_CmdP2]P0 M3;单色模式")

                    
                #lancaigang2521:
                if self.G_SerialPort1OpenFlag == True:
                    try:
                        self.G_PhrozenFluiddRespondInfo("try;Lo_AMSDeviceStateRspInfo")
                        #获取多色主板详细状态
                        Lo_AMSDeviceStateRspInfo = self.Cmds_AMSSerialPort1SendWaitRsp("SD", sizeof(AMSDetailInfoBytes))
                        self.G_PhrozenFluiddRespondInfo("tty1串口接收: %s" % Lo_AMSDeviceStateRspInfo)
                        if len(Lo_AMSDeviceStateRspInfo) != sizeof(AMSDetailInfoBytes):
                            self.G_PhrozenFluiddRespondInfo("AMS1未响应，请检查AMS1='%s'" % (gcmd.get_commandline(),))
                            #lancaigang240412:AMS多色标签
                            self.G_AMSDevice1IfNormal=False
                        else:
                            #lancaigang240412:AMS多色标签
                            self.G_AMSDevice1IfNormal=True
                    except:
                        self.G_PhrozenFluiddRespondInfo("except;Lo_AMSDeviceStateRspInfo")

                if self.G_SerialPort2OpenFlag == True:
                    try:
                        self.G_PhrozenFluiddRespondInfo("try;Lo_AMSDeviceStateRspInfo")
                        #获取多色主板详细状态
                        Lo_AMSDeviceStateRspInfo = self.Cmds_AMSSerialPort2SendWaitRsp("SD", sizeof(AMSDetailInfoBytes))
                        self.G_PhrozenFluiddRespondInfo("tty2串口接收: %s" % Lo_AMSDeviceStateRspInfo)
                        if len(Lo_AMSDeviceStateRspInfo) != sizeof(AMSDetailInfoBytes):
                            self.G_PhrozenFluiddRespondInfo("AMS2未响应，请检查AMS2='%s'" % (gcmd.get_commandline(),))
                            self.G_AMSDevice2IfNormal=False
                        else:
                            self.G_AMSDevice2IfNormal=True
                    except:
                        self.G_PhrozenFluiddRespondInfo("except;Lo_AMSDeviceStateRspInfo")

                #lancaigang241107:
                if self.G_AMSDevice1IfNormal==True or self.G_AMSDevice2IfNormal==True:
                    self.G_PhrozenFluiddRespondInfo("有AMS多色，处理P2 A7")
                else:
                    self.G_PhrozenFluiddRespondInfo("没有AMS多色，不处理P2 A7")
                    #lancaigang250619:检查AMS是否重新连接成功
                    self.Cmds_USBConnectErrorCheck()
                    if self.G_SerialPort1OpenFlag == True:
                        self.Cmds_AMSSerial1Send("M0")
                        self.G_PhrozenFluiddRespondInfo("串口1发送命令: M0")
                    #lancaigang241030:
                    if self.G_SerialPort2OpenFlag == True:
                        self.Cmds_AMSSerial2Send("M0")
                        self.G_PhrozenFluiddRespondInfo("串口2发送命令: M0")
                    
                    #lancaigang240524：用于UIUX动态界面
                    self.G_PhrozenFluiddRespondInfo("+P2A7:1,%d" % self.G_ChangeChannelTimeoutNewChan)
                    self.G_PhrozenFluiddRespondInfo("return")
                    return

                self.G_PhrozenFluiddRespondInfo("命令='%s'；所有线材回退到停靠位" % (gcmd.get_commandline(),))
                #lancaigang240524：用于UIUX动态界面
                self.G_PhrozenFluiddRespondInfo("+P2A7:0,%d" % self.G_ChangeChannelTimeoutNewChan)
                #lancaigang231201：打印完成后，如果复位，可能会碰到打印好的模型，不能复位但又需要切线回退线材
                
                #lancaigang250323：
                if self.G_ToolheadIfHaveFilaFlag==True:
                    #lancaigang231205：复位切线回退
                    #self.Cmds_MoveToCutFilaAndNotRollback(gcmd)
                    self.G_PhrozenFluiddRespondInfo("喷头有线材")
                    #lancaigang20231024复位切线；不能碰到模型
                    #lancaigang240109：喷头有线材才允许切线
                    #if self.G_ToolheadIfHaveFilaFlag==True:
                    #lancaigang240319：切线之前准备动作
                    #self.Cmds_MoveToCutFilaPrepare()
                    self.Cmds_MoveToCutFilaAbsolutePositionNotReset(gcmd)
                    #lancaigang241031:
                    if self.G_SerialPort1OpenFlag == True:
                        self.Cmds_AMSSerial1Send("RD")
                        self.G_PhrozenFluiddRespondInfo("串口1发送命令: RD；所有通道线材回退到停靠位")
                    #lancaigang241030:
                    if self.G_SerialPort2OpenFlag == True:
                        self.Cmds_AMSSerial2Send("RD")
                        self.G_PhrozenFluiddRespondInfo("串口2发送命令: RD；所有通道线材回退到停靠位")

                    self.G_PhrozenFluiddRespondInfo("外部宏命令-PRZ_WAITINGAREA-等待区")
                    command_string = """
                        PRZ_WAITINGAREA
                        """
                    self.G_PhrozenGCode.run_script_from_command(command_string)
                    self.G_PhrozenFluiddRespondInfo("外部宏命令-PRZ_WAITINGAREA；command_string='%s'" % command_string)

                    self.G_PhrozenFluiddRespondInfo("延时16秒")
                    # #lancaigang240913：把延時放到外面
                    self.G_ProzenToolhead.dwell(16)
                    self.G_PhrozenFluiddRespondInfo("延时16秒")

                    #lancaigang250619:检查AMS是否重新连接成功
                    self.Cmds_USBConnectErrorCheck()
                    if self.G_SerialPort1OpenFlag == True:
                        self.Cmds_AMSSerial1Send("M0")
                        self.G_PhrozenFluiddRespondInfo("串口1发送命令: M0")
                    #lancaigang241030:
                    if self.G_SerialPort2OpenFlag == True:
                        self.Cmds_AMSSerial2Send("M0")
                        self.G_PhrozenFluiddRespondInfo("串口2发送命令: M0")
                else:
                    #lancaigang241031:
                    if self.G_SerialPort1OpenFlag == True:
                        self.Cmds_AMSSerial1Send("RD")
                        self.G_PhrozenFluiddRespondInfo("串口1发送命令: RD；所有通道线材回退到停靠位")
                    #lancaigang241030:
                    if self.G_SerialPort2OpenFlag == True:
                        self.Cmds_AMSSerial2Send("RD")
                        self.G_PhrozenFluiddRespondInfo("串口2发送命令: RD；所有通道线材回退到停靠位")

                    self.G_PhrozenFluiddRespondInfo("外部宏命令-PRZ_WAITINGAREA-等待区")
                    command_string = """
                        PRZ_WAITINGAREA
                        """
                    self.G_PhrozenGCode.run_script_from_command(command_string)
                    self.G_PhrozenFluiddRespondInfo("外部宏命令-PRZ_WAITINGAREA；command_string='%s'" % command_string)

                    self.G_PhrozenFluiddRespondInfo("延时12秒")
                    # #lancaigang240913：把延時放到外面
                    self.G_ProzenToolhead.dwell(12)
                    self.G_PhrozenFluiddRespondInfo("延时12秒")

                    #lancaigang250619:检查AMS是否重新连接成功
                    self.Cmds_USBConnectErrorCheck()
                    if self.G_SerialPort1OpenFlag == True:
                        self.Cmds_AMSSerial1Send("M0")
                        self.G_PhrozenFluiddRespondInfo("串口1发送命令: M0")
                    #lancaigang241030:
                    if self.G_SerialPort2OpenFlag == True:
                        self.Cmds_AMSSerial2Send("M0")
                        self.G_PhrozenFluiddRespondInfo("串口2发送命令: M0")





                #lancaigang240113：清除手动命令标志
                self.ManualCmdFlag=False


                # self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_CmdP2]全部归位并切线")
                # command_string = """
                # PG28
                # """
                # self.G_PhrozenGCode.run_script_from_command(command_string)

                

                #time.sleep(0.5)
                self.G_PhrozenFluiddRespondInfo("延时0.5")
                self.G_ProzenToolhead.dwell(0.5)

                #lancaigang250409：手動進料則讀取AMS狀態
                self.Cmds_CmdP114(None)

                #time.sleep(0.5)
                #time.sleep(0.5)
                self.G_PhrozenFluiddRespondInfo("延时0.5")
                self.G_ProzenToolhead.dwell(0.5)

                #lancaigang240524：用于UIUX动态界面
                self.G_PhrozenFluiddRespondInfo("+P2A7:1,%d" % self.G_ChangeChannelTimeoutNewChan)

                return




        #lancaigang240801：P2 B?
        if "B" in params:
            #self.Cmds_P1CnAutoChangeChannel(int(params["C"]), gcmd)
            #lancaigang240524：用于UIUX动态界面
            self.G_PhrozenFluiddRespondInfo(gcmd.get_commandline())


        #lancaigang240516：防止粘包
        #time.sleep(0.5)
        self.G_PhrozenFluiddRespondInfo("延时0.5")
        self.G_ProzenToolhead.dwell(0.5)








    ####################################
    #函数名称：
    #输入参数：
    #返 回 值:
    #功能描述：蓝才刚-20230830
    ####################################
    # P1 S0 所有线材进料到停靠位；====="RD";
    # P1 T[n]n:1 ~32(设备无组网,取1 ~4)手动换到指定通道,仅换线(用于测试)；====="T"；
    # P1 B[n]n:1 ~32(设备无组网,取1 ~4)指定通道线料完全退出 Yes；====="B"；
    # P1 D[n]；n:1~32(设备无组网,取1~4)；指定通道的线料后退停泊在停靠位待命状态 Yes；====="P"；
    # P1 C[n] n:1~32(设备无组网,取1~4) 自动换到指定通道(多动作命令,包含切线, 换线, 等待)；====="T"；
    #lancaigang231202:
    # P1 E[n]；n:1~32(设备无组网,取1~4)；指定通道的线料强制前转，需要注意取出喷头上的料管 Yes；====="E?"；
    # lancaigang240228：喷头回抽一段距离，需要stm32先回退一段距离
    # P1 G[n]；n:1~32(设备无组网,取1~4)；指定通道的线料回退一段距离 Yes；====="G?"；
    # lancaigang240319：
    # =====P1 H[n]；n:1~32(设备无组网,取1~4)；换料前回抽 Yes；====="H?"；
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
    #lancaigang240418：
    # =====P1 V[n]；用于版本号
    # =====P1 W[n]；
    # =====P1 X[n]；
    # =====P1 Y[n]；
    # =====P1 Z[n]；
    def Cmds_CmdP1(self, gcmd):
        self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_CmdP1]命令='%s'" % (gcmd.get_commandline(),))

        if self.G_AMSDevice1IfNormal==False and self.G_AMSDevice2IfNormal==False:
            self.G_PhrozenFluiddRespondInfo("没有AMS多色，所有AMS多色未连接，不处理P1 ??命令")



            # #lancaigang250828:
            # self.G_PhrozenFluiddRespondInfo("外部宏命令-PRZ_PAUSE_WAITINGAREA")
            # command_string = """
            #     PRZ_PAUSE_WAITINGAREA
            #     """
            # self.G_PhrozenGCode.run_script_from_command(command_string)
            # self.G_PhrozenFluiddRespondInfo("外部宏命令；command_string='%s'" % command_string)




            #获取命令参数
            params = gcmd.get_command_parameters()

            # =====P1 I[n]；手动挤料时stm32需要补料；====="I?"；
            if "I" in params:
                self.G_PhrozenFluiddRespondInfo("AMS多色P28未连接，手动挤料使用单色M3模式")
                #lancaigang240524：用于UIUX动态界面
                self.G_PhrozenFluiddRespondInfo("+P1In:0,%d" % self.G_ChangeChannelTimeoutNewChan)
                if not int(params["I"]) in range(-1000, 1000):
                    raise gcmd.error("无效参数命令;cmd '%s', 手动挤料过长" % (gcmd.get_commandline()))
                # command_string = """
                #                 M106 S0
                #                 M83
                #                 G92 E0
                #                 G1 E%f F300
                #                 """ %(int(params["I"]),)
                # self.G_PhrozenGCode.run_script_from_command(command_string)
                # self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_CmdP1]GCODE命令: %s" % command_string)

                #lancaigang240705：不经过AMS，直接使用gcode命令，速度快
                self.Cmds_P1InExtrudeManualIn(int(params["I"]))


                #lancaigang240524：用于UIUX动态界面
                self.G_PhrozenFluiddRespondInfo("+P1In:1,%d" % self.G_ChangeChannelTimeoutNewChan)
            return
        


        # #lancaigang240705：如果P114没有AMS，则直接挤料
        # if self.G_AMSDevice1IfNormal==False:
        #     self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_CmdP1]self.G_AMSDevice1IfNormal==False")
        #     #获取命令参数
        #     params = gcmd.get_command_parameters()
        #     # =====P1 I[n]；手动挤料时stm32需要补料；====="I?"；
        #     if "I" in params:
        #         self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_CmdP1]AMS多色P114未连接，直接挤料")
        #         #lancaigang240524：用于UIUX动态界面
        #         self.G_PhrozenFluiddRespondInfo("+P1In:0,%d" % self.G_ChangeChannelTimeoutNewChan)
        #         if not int(params["I"]) in range(-1000, 1000):
        #             raise gcmd.error("无效参数命令;cmd '%s', 手动挤料过长" % (gcmd.get_commandline()))
        #         # command_string = """
        #         #                 M106 S0
        #         #                 M83
        #         #                 G92 E0
        #         #                 G1 E%f F300
        #         #                 """ %(int(params["I"]),)
        #         # self.G_PhrozenGCode.run_script_from_command(command_string)
        #         # self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_CmdP1]GCODE命令: %s" % command_string)

        #         #lancaigang240705：封装函数
        #         self.Cmds_P1InExtrudeManualIn(int(params["I"]))

        #         #lancaigang240524：用于UIUX动态界面
        #         self.G_PhrozenFluiddRespondInfo("+P1In:1,%d" % self.G_ChangeChannelTimeoutNewChan)

        #         return

        self.G_PhrozenFluiddRespondInfo("当前模式")
        if self.G_AMSDeviceWorkMode == AMS_WORK_MODE_UNKNOW:
            self.G_PhrozenFluiddRespondInfo("+Mode:0,unkown")
        elif self.G_AMSDeviceWorkMode == AMS_WORK_MODE_MC:
            self.G_PhrozenFluiddRespondInfo("+Mode:1,MC")
        elif self.G_AMSDeviceWorkMode == AMS_WORK_MODE_MA:
            self.G_PhrozenFluiddRespondInfo("+Mode:2,MA")
        elif self.G_AMSDeviceWorkMode == AMS_WORK_MODE_FILA_RUNOUT:
            self.G_PhrozenFluiddRespondInfo("+Mode:3,RUNOUT")
        else:
            self.G_PhrozenFluiddRespondInfo("+Mode:-1,error")


        #lancaigang240529：phrozen插件版本
        self.G_PhrozenFluiddRespondInfo("V-H%s-I%s-F%s-SN1" % (HW_VERSION,IMAGE_VERSION,FW_VERSION))


        #lancaigang231228：防止随后的命令导致stm32的AT命令粘包
        #time.sleep(0.5)
        #lancaigang240516：防止time too close
        #self.G_ProzenToolhead.dwell(0.5)


        #lancaigang240105：加一条AT命令
        self.G_PhrozenFluiddRespondInfo("+P1START:0,%d" % self.G_ChangeChannelTimeoutNewChan)

        #lancaigang20231019：如果发现喷头上检测到线材，先切断线材再退出所有线程到停靠位
        #if self.G_ToolheadIfHaveFilaFlag:
        #    gcmd.respond_info("[(cmds.python)Cmds_CmdP1]检测到喷头上有线材，先切断线材，再退出所有线程到停靠位")
        #    gcmd.respond_info("[(cmds.python)Cmds_CmdP1]喷头切线")
        #    self.Cmds_MoveToCutFilaAction(gcmd)
        #    self.Cmds_AMSSerial1Send("AP")
        #    gcmd.respond_info("发送命令: AP，全部后退到停靠位")

        #获取命令参数
        params = gcmd.get_command_parameters()


        #lancaigang250619:检查AMS是否重新连接成功
        self.Cmds_USBConnectErrorCheck()





        # P1 S0；所有线材进料到停靠位
        # P1 S1；回退一小段距离
        if "S" in params:
            self.G_PhrozenFluiddRespondInfo("Cmds_CmdP1]P1 S?")


            # #lancaigang250515：单机打多色，不处理T?
            # if self.G_P0M1MCNoneAMS == 1:
            #     self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_CmdT0]单机打多色，不处理T?")
            #     return
            # #lancaigang250429：
            # if self.G_AMSDeviceWorkMode==AMS_WORK_MODE_FILA_RUNOUT:
            #     self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_CmdT0]单色模式，不处理T0")
            #     return
            # #lancaigang250514：
            # if self.G_AMSDeviceWorkMode==AMS_WORK_MODE_MA :
            #     self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_CmdT0]单色续料模式，不处理T0")
            #     return



            #lancaigang240527：未知模式，因为要操作手动命令，默认让STM32进入MC多色模式
            if self.G_AMSDeviceWorkMode == AMS_WORK_MODE_UNKNOW:
                self.G_PhrozenFluiddRespondInfo("未知模式，因为要操作手动命令，默认让STM32进入MC多色模式")
                #lancaigang241030:
                if self.G_SerialPort1OpenFlag == True:
                    self.G_PhrozenFluiddRespondInfo("串口1发送命令：MC")
                    self.Cmds_AMSSerial1Send("MC")
                    
                #lancaigang241030:
                if self.G_SerialPort2OpenFlag == True:
                    self.G_PhrozenFluiddRespondInfo("串口2发送命令：MC")
                    self.Cmds_AMSSerial2Send("MC")
                    

                self.G_ProzenToolhead.dwell(2)

                

            if self.G_ToolheadIfHaveFilaFlag:
                #lancaigang231205：复位切线回退
                self.Cmds_MoveToCutFilaAndNotRollback(gcmd)
                self.G_PhrozenFluiddRespondInfo("喷头有线材，所有AMS先回退")
                # self.Cmds_AMSSerial1Send("G%d" % self.G_ChangeChannelTimeoutOldChan)
                # self.G_PhrozenFluiddRespondInfo("G%d" % self.G_ChangeChannelTimeoutOldChan)
                # self.G_PhrozenFluiddRespondInfo("AMS旧通道先回退一段距离: G%d" % self.G_ChangeChannelTimeoutOldChan)
                #lancaigang241030:
                if self.G_SerialPort1OpenFlag == True:
                    self.Cmds_AMSSerial1Send("AP")
                    self.G_PhrozenFluiddRespondInfo("串口1发送命令：AP")
                #lancaigang241030:
                if self.G_SerialPort2OpenFlag == True:
                    self.Cmds_AMSSerial2Send("AP")
                    self.G_PhrozenFluiddRespondInfo("串口2发送命令：AP")

                self.G_ProzenToolhead.dwell(0.5)

                # self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_CmdP1]外部宏命令-PG101")
                # command_string = """
                #     PG101
                #     """
                # self.G_PhrozenGCode.run_script_from_command(command_string)
                # self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_CmdP1]外部宏命令-到指定待料区位置等待吐料；command_string='%s'" % command_string)
                # self.IfDoPG102Flag=True

                #lancaigang240913：把延時放到外面
                self.G_ProzenToolhead.dwell(6.0)
                #lancaigang231201：检查切线后旧通道线材是否正常退料，不正常则暂停
                self.Cmds_CutFilaIfNormalCheck()
                if self.G_KlipperIfPaused == True:
                        self.G_PhrozenFluiddRespondInfo("切线5秒了喷头还检测到线材，切刀异常了，请检查切刀，暂停klipper打印")
                        #Lo_ChangeChannelIfSuccess = False
                        return

                
            self.G_PhrozenFluiddRespondInfo("命令='%s'；一小段距离" % (gcmd.get_commandline(),))
            #lancaigang240524：用于UIUX动态界面
            self.G_PhrozenFluiddRespondInfo("+P1S:0,%d" % self.G_ChangeChannelTimeoutNewChan)

            #lancaigang231207：
            if self.G_IfInFilaBlockFlag:
                self.G_PhrozenFluiddRespondInfo("进料卡线，先手动P1 E?从喷头上料管取出并手动prz_resume恢复")
                self.G_PhrozenFluiddRespondInfo("+P1END:0,%d" % self.G_ChangeChannelTimeoutNewChan)
                #lancaigang240524：用于UIUX动态界面
                self.G_PhrozenFluiddRespondInfo("+P1S:1,%d" % self.G_ChangeChannelTimeoutNewChan)
                return

            if int(params["S"])==0:
                #进料到停靠位
                #lancaigang241030:
                if self.G_SerialPort1OpenFlag == True:
                    self.Cmds_AMSSerial1Send("RD")
                    self.G_PhrozenFluiddRespondInfo("串口1发送命令：RD")
                #lancaigang241030:
                if self.G_SerialPort2OpenFlag == True:
                    self.Cmds_AMSSerial2Send("RD")
                    self.G_PhrozenFluiddRespondInfo("串口2发送命令：RD")

                self.G_PhrozenFluiddRespondInfo("发送命令=RD；所有通道线材进料到停靠位")
            if int(params["S"])==1:
                #进料到停靠位
                #lancaigang241030:
                if self.G_SerialPort1OpenFlag == True:
                    self.Cmds_AMSSerial1Send("RB")
                    self.G_PhrozenFluiddRespondInfo("串口1发送命令：RB")
                #lancaigang241030:
                if self.G_SerialPort2OpenFlag == True:
                    self.Cmds_AMSSerial2Send("RB")
                    self.G_PhrozenFluiddRespondInfo("串口2发送命令：RB")
                self.G_PhrozenFluiddRespondInfo("发送命令=RB；回退一小段距离")




            #lancaigang240113：手动命令标志
            self.ManualCmdFlag=True


            #lancaigang231201：检查切线后是否正常退料，不正常则暂停
            #lancaigang240528：屏蔽不检测切线
            #self.Cmds_CutFilaIfNormalCheck()

            self.G_PhrozenFluiddRespondInfo("+P1END:0,%d" % self.G_ChangeChannelTimeoutNewChan)
            #lancaigang240524：用于UIUX动态界面
            self.G_PhrozenFluiddRespondInfo("+P1S:1,%d" % self.G_ChangeChannelTimeoutNewChan)
            return




        #lancaigang20231013：自动换料
        # P1 C[n] 自动换料
        if "C" in params:
            self.G_PhrozenFluiddRespondInfo("P1 C?")
            self.G_PhrozenFluiddRespondInfo("=====self.G_ChangeChannelTimeoutOldChan=%d" % self.G_ChangeChannelTimeoutOldChan)
            self.G_PhrozenFluiddRespondInfo("=====self.G_ChangeChannelTimeoutNewChan=%d" % self.G_ChangeChannelTimeoutNewChan)

            #lancaigang250515：单机打多色，不处理T?
            if self.G_P0M1MCNoneAMS == 1:
                self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_CmdT0]单机打多色，不处理T?")
                return
            #lancaigang250429：
            if self.G_AMSDeviceWorkMode==AMS_WORK_MODE_FILA_RUNOUT:
                self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_CmdT0]单色模式，不处理T?")
                return
            #lancaigang250514：
            if self.G_AMSDeviceWorkMode==AMS_WORK_MODE_MA :
                self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_CmdT0]单色续料模式，不处理T?")
                return

            #lancaigang240527：未知模式，因为要操作手动命令，默认让STM32进入MC多色模式
            if self.G_AMSDeviceWorkMode == AMS_WORK_MODE_UNKNOW:
                self.G_PhrozenFluiddRespondInfo("未知模式，因为要操作手动命令，默认让STM32进入MC多色模式")
                self.G_PhrozenFluiddRespondInfo("如果收到T?命令，但模式是未知模式，强制转换为MC多色模式")
                self.G_AMSDeviceWorkMode = AMS_WORK_MODE_MC
                #lancaigang241030:
                if self.G_SerialPort1OpenFlag == True:
                    self.G_PhrozenFluiddRespondInfo("串口1发送命令：MC")
                    self.Cmds_AMSSerial1Send("MC")
                    
                #lancaigang241030:
                if self.G_SerialPort2OpenFlag == True:
                    self.G_PhrozenFluiddRespondInfo("串口2发送命令：MC")
                    self.Cmds_AMSSerial2Send("MC")
                    
            
                self.G_ProzenToolhead.dwell(2)

            #lancaigang250913:导致return异常
            #self.Cmds_CmdOrcaPre()
            
            self.G_PhrozenFluiddRespondInfo("命令='%s'；自动换料" % (gcmd.get_commandline(),))
            self.G_PhrozenFluiddRespondInfo("自动换料")
            #lancaigang240524：用于UIUX动态界面
            self.G_PhrozenFluiddRespondInfo("+P1Cn:0,%d" % self.G_ChangeChannelTimeoutNewChan)
            if not int(params["C"]) in range(1, AMS_MAX_CHANNEL + 1):
                raise gcmd.error("无效参数命令;cmd '%s', that must is C?" % (gcmd.get_commandline()))
            
            #lancaigang240113：清除手动命令标志
            self.ManualCmdFlag=False
            #lancaigang240221：stm32主动上报，开启可以暂停1次
            self.STM32ReprotPauseFlag=0
            self.G_PhrozenFluiddRespondInfo("self.STM32ReprotPauseFlag=0")
            # #cancel取消命令
            # self.G_PhrozenPrinterCancelPauseResume.cmd_CANCEL_PRINT(None)
            #lancaigang250517：
            Lo_PauseStatus=self.G_PhrozenPrinterCancelPauseResume.get_status(None)
            self.G_PhrozenFluiddRespondInfo("当前暂停状态-Lo_PauseStatus='%s'" % Lo_PauseStatus)
            self.G_PhrozenFluiddRespondInfo("Lo_PauseStatus['is_paused']='%s'" % Lo_PauseStatus['is_paused'])
            #// 当前暂停状态-Lo_PauseStatus='{'is_paused': True}'
            if Lo_PauseStatus['is_paused'] == True:
                self.G_PhrozenFluiddRespondInfo("已是暂停状态")
            else:
                self.G_PhrozenFluiddRespondInfo("未暂停状态")
            #lancaigang240113：清除手动命令标志
            self.ManualCmdFlag=False
            #lancaigang240221：stm32主动上报，开启可以暂停1次
            self.STM32ReprotPauseFlag=0
            self.G_PhrozenFluiddRespondInfo("self.STM32ReprotPauseFlag=0")

            #lancaigang241030：一般是P1 C1到P1 C32，范围在1到32
            #第1台：1 2 3 4
            #第2台：5 6 7 8
            #第3台：9 10 11 12
            #第4台：13 14 15 16
            #第5台：17 18 19 20
            #第6台：21 22 23 24
            #第7台：25 26 27 28
            #第8台：29 30 31 32
            #自动换料
            #self.Cmds_P1CnAutoChangeChannel(int(params["C"]), gcmd)
            chan=int(params["C"])

            if chan==1:
                #lancaigang250515:判断串口屏配置的颜色匹对通道
                if self.G_ChromaKitAccessT0 > 0:
                    self.G_PhrozenFluiddRespondInfo("用户选择匹配通道；self.G_ChromaKitAccessT0=%d" % self.G_ChromaKitAccessT0)
                    self.Cmds_P1CnAutoChangeChannel(self.G_ChromaKitAccessT0, gcmd)
                else:
                    self.G_PhrozenFluiddRespondInfo("用户未选择匹配通道，默认通道；chan=%d" % chan)
                    self.Cmds_P1CnAutoChangeChannel(chan, gcmd)
            elif chan==2:
                #lancaigang250515:判断串口屏配置的颜色匹对通道
                if self.G_ChromaKitAccessT1 > 0:
                    self.G_PhrozenFluiddRespondInfo("用户选择匹配通道；self.G_ChromaKitAccessT1=%d" % self.G_ChromaKitAccessT1)
                    self.Cmds_P1CnAutoChangeChannel(self.G_ChromaKitAccessT1, gcmd)
                else:
                    self.G_PhrozenFluiddRespondInfo("用户未选择匹配通道，默认通道；chan=%d" % chan)
                    self.Cmds_P1CnAutoChangeChannel(chan, gcmd)
            elif chan==3:
                #lancaigang250515:判断串口屏配置的颜色匹对通道
                if self.G_ChromaKitAccessT2 > 0:
                    self.G_PhrozenFluiddRespondInfo("用户选择匹配通道；self.G_ChromaKitAccessT2=%d" % self.G_ChromaKitAccessT2)
                    self.Cmds_P1CnAutoChangeChannel(self.G_ChromaKitAccessT2, gcmd)
                else:
                    self.G_PhrozenFluiddRespondInfo("用户未选择匹配通道，默认通道；chan=%d" % chan)
                    self.Cmds_P1CnAutoChangeChannel(chan, gcmd)
            elif chan==4:
                #lancaigang250515:判断串口屏配置的颜色匹对通道
                if self.G_ChromaKitAccessT3 > 0:
                    self.G_PhrozenFluiddRespondInfo("用户选择匹配通道；self.G_ChromaKitAccessT3=%d" % self.G_ChromaKitAccessT3)
                    self.Cmds_P1CnAutoChangeChannel(self.G_ChromaKitAccessT3, gcmd)
                else:
                    self.G_PhrozenFluiddRespondInfo("用户未选择匹配通道，默认通道；chan=%d" % chan)
                    self.Cmds_P1CnAutoChangeChannel(chan, gcmd)


            #lancaigang240524：用于UIUX动态界面
            self.G_PhrozenFluiddRespondInfo("+P1Cn:1,%d" % self.G_ChangeChannelTimeoutNewChan)















        #lancaigang20231013：手动换料
        # P1 T[n] 手动换料
        if "T" in params:
            self.G_PhrozenFluiddRespondInfo("P1 T?")
            #lancaigang240527：未知模式，因为要操作手动命令，默认让STM32进入MC多色模式
            if self.G_AMSDeviceWorkMode == AMS_WORK_MODE_UNKNOW:
                self.G_PhrozenFluiddRespondInfo("未知模式，因为要操作手动命令，默认让STM32进入MC多色模式")
                #lancaigang241030:
                if self.G_SerialPort1OpenFlag == True:
                    self.Cmds_AMSSerial1Send("MC")
                    self.G_PhrozenFluiddRespondInfo("串口1发送命令：MC")
                #lancaigang241030:
                if self.G_SerialPort2OpenFlag == True:
                    self.Cmds_AMSSerial2Send("MC")
                    self.G_PhrozenFluiddRespondInfo("串口2发送命令：MC")

                self.G_ProzenToolhead.dwell(2)
            
            self.G_PhrozenFluiddRespondInfo("命令='%s'；手动换料" % (gcmd.get_commandline(),))
            self.G_PhrozenFluiddRespondInfo("手动换料")
            #lancaigang240524：用于UIUX动态界面
            self.G_PhrozenFluiddRespondInfo("+P1Tn:0,%d" % self.G_ChangeChannelTimeoutNewChan)
            if not int(params["T"]) in range(1, AMS_MAX_CHANNEL + 1):
                raise gcmd.error("无效参数命令;cmd '%s', that must is T?" % (gcmd.get_commandline()))
            
            #lancaigang231209：手动调式可不用管暂停
            self.G_KlipperIfPaused=False
            #lancaigang240221：stm32主动上报，开启可以暂停1次
            self.STM32ReprotPauseFlag=0
            self.G_PhrozenFluiddRespondInfo("self.STM32ReprotPauseFlag=0")

            #lancaigang240113：手动命令标志
            self.ManualCmdFlag=True
            # #lancaigang240529：补料过程中不暂停
            # self.Cmds_AMSSerial1Send("M0")
            # self.G_PhrozenFluiddRespondInfo("发送命令=M0")
            # self.G_ProzenToolhead.dwell(1)

            #lancaigang231207：
            if self.G_IfInFilaBlockFlag:
                self.G_PhrozenFluiddRespondInfo("进料卡线，先手动P1 E?从喷头上料管取出并手动prz_resume恢复")
                self.G_PhrozenFluiddRespondInfo("+P1END:0,%d" % self.G_ChangeChannelTimeoutNewChan)
                #lancaigang240524：用于UIUX动态界面
                self.G_PhrozenFluiddRespondInfo("+P1Tn:0,%d" % self.G_ChangeChannelTimeoutNewChan)
                return

            #lancaigang231202：不复位切线不回退
            #self.Cmds_MoveToCutFilaAbsolutePositionNotReset(gcmd)
            #lancaigang240319：切线之前准备动作
            #self.G_ChangeChannelTimeoutOldChan=int(params["T"])
            #self.Cmds_MoveToCutFilaPrepare()


            if self.G_ToolheadIfHaveFilaFlag:
                #lancaigang231205：复位切线回退
                self.Cmds_MoveToCutFilaAndNotRollback(gcmd)
                self.G_PhrozenFluiddRespondInfo("喷头有线材，所有AMS先回退")
                # self.Cmds_AMSSerial1Send("G%d" % self.G_ChangeChannelTimeoutOldChan)
                # self.G_PhrozenFluiddRespondInfo("G%d" % self.G_ChangeChannelTimeoutOldChan)
                # self.G_PhrozenFluiddRespondInfo("AMS旧通道先回退一段距离: G%d" % self.G_ChangeChannelTimeoutOldChan)
                #lancaigang241030:
                if self.G_SerialPort1OpenFlag == True:
                    self.Cmds_AMSSerial1Send("AP")
                    self.G_PhrozenFluiddRespondInfo("串口1发送命令：AP")
                #lancaigang241030:
                if self.G_SerialPort2OpenFlag == True:
                    self.Cmds_AMSSerial2Send("AP")
                    self.G_PhrozenFluiddRespondInfo("串口2发送命令：AP")

                self.G_ProzenToolhead.dwell(0.5)

                # self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_CmdP1]外部宏命令-PG101")
                # command_string = """
                #     PG101
                #     """
                # self.G_PhrozenGCode.run_script_from_command(command_string)
                # self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_CmdP1]外部宏命令-到指定待料区位置等待吐料；command_string='%s'" % command_string)
                # self.IfDoPG102Flag=True

                #lancaigang240913：把延時放到外面
                self.G_ProzenToolhead.dwell(6.0)
                #lancaigang231201：检查切线后旧通道线材是否正常退料，不正常则暂停
                self.Cmds_CutFilaIfNormalCheck()
                if self.G_KlipperIfPaused == True:
                    self.G_PhrozenFluiddRespondInfo("切线5秒了喷头还检测到线材，切刀异常了，请检查切刀，暂停klipper打印")
                    #Lo_ChangeChannelIfSuccess = False
                    return




            # self.G_PhrozenFluiddRespondInfo("外部宏命令-PG109；切线后，先加热并吐掉残留喷头的线材")
            # self.PG102Flag=True
            # self.G_PhrozenFluiddRespondInfo("self.Flag=True")
            # command_string = """
            # PG109
            # """
            # self.G_PhrozenGCode.run_script_from_command(command_string)
            # self.G_PhrozenFluiddRespondInfo("command_string='%s'" % command_string)
            # self.PG102Flag=False
            # self.G_PhrozenFluiddRespondInfo("self.Flag=False")




            self.G_ChangeChannelTimeoutOldChan=self.G_ChangeChannelTimeoutNewChan
            self.G_ChangeChannelTimeoutOldGcmd=self.G_ChangeChannelTimeoutNewGcmd
            self.G_ChangeChannelTimeoutNewChan=int(params["T"])
            self.G_ChangeChannelTimeoutNewGcmd=gcmd

            #lancaigang241030：一般是P1 C1到P1 C32，范围在1到32
            #第1台：1 2 3 4
            #第2台：5 6 7 8
            #第3台：9 10 11 12
            #第4台：13 14 15 16
            #第5台：17 18 19 20
            #第6台：21 22 23 24
            #第7台：25 26 27 28
            #第8台：29 30 31 32
            #手动换料
            self.Cmds_P1TnManualChangeChannel(int(params["T"]), gcmd)



            #lancaigang240524：用于UIUX动态界面
            self.G_PhrozenFluiddRespondInfo("+P1Tn:1,%d" % self.G_ChangeChannelTimeoutNewChan)





        # P1 B[n] 手动完全回退料
        if "B" in params:
            self.G_PhrozenFluiddRespondInfo("P1 B?")
            #lancaigang240527：未知模式，因为要操作手动命令，默认让STM32进入MC多色模式
            if self.G_AMSDeviceWorkMode == AMS_WORK_MODE_UNKNOW:
                self.G_PhrozenFluiddRespondInfo("未知模式，因为要操作手动命令，默认让STM32进入MC多色模式")
                #lancaigang241030:
                if self.G_SerialPort1OpenFlag == True:
                    self.Cmds_AMSSerial1Send("MC")
                    self.G_PhrozenFluiddRespondInfo("串口1发送命令：MC")
                #lancaigang241030:
                if self.G_SerialPort2OpenFlag == True:
                    self.Cmds_AMSSerial2Send("MC")
                    self.G_PhrozenFluiddRespondInfo("串口2发送命令：MC")

                self.G_ProzenToolhead.dwell(2)
            
            self.G_PhrozenFluiddRespondInfo("命令='%s'；线材完全退出" % (gcmd.get_commandline(),))
            #lancaigang240524：用于UIUX动态界面
            self.G_PhrozenFluiddRespondInfo("+P1Bn:0,%d" % self.G_ChangeChannelTimeoutNewChan)
            if not int(params["B"]) in range(1, AMS_MAX_CHANNEL + 1):
                raise gcmd.error("无效参数命令;cmd '%s', that must is B?" % (gcmd.get_commandline()))
            
            #lancaigang231209：手动调式可不用管暂停
            self.G_KlipperIfPaused=False
            #lancaigang240221：stm32主动上报，开启可以暂停1次
            self.STM32ReprotPauseFlag=0
            self.G_PhrozenFluiddRespondInfo("self.STM32ReprotPauseFlag=0")

            #lancaigang240113：手动命令标志
            self.ManualCmdFlag=True
            # #lancaigang240529：补料过程中不暂停
            # self.Cmds_AMSSerial1Send("M0")
            # self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_CmdP1]发送命令=M0")
            # self.G_ProzenToolhead.dwell(1)

            #lancaigang240319：切线之前准备动作
            #self.G_ChangeChannelTimeoutNewChan=int(params["B"])
            #self.Cmds_MoveToCutFilaPrepare()

            # #lancaigang231202：不复位切线不回退
            # #self.Cmds_MoveToCutFilaAbsolutePositionNotReset(gcmd)
            # #lancaigang231205：复位切线回退
            # #lancaigang240328：复位切线不回退
            # self.Cmds_MoveToCutFilaAndNotRollback(gcmd)


            if self.G_ToolheadIfHaveFilaFlag==True:
                #lancaigang231205：复位切线回退
                self.Cmds_MoveToCutFilaAndNotRollback(gcmd)
                self.G_PhrozenFluiddRespondInfo("喷头有线材，所有AMS先回退")
                # self.Cmds_AMSSerial1Send("G%d" % self.G_ChangeChannelTimeoutOldChan)
                # self.G_PhrozenFluiddRespondInfo("G%d" % self.G_ChangeChannelTimeoutOldChan)
                # self.G_PhrozenFluiddRespondInfo("AMS旧通道先回退一段距离: G%d" % self.G_ChangeChannelTimeoutOldChan)
                #lancaigang241030:
                if self.G_SerialPort1OpenFlag == True:
                    self.Cmds_AMSSerial1Send("AP")
                    self.G_PhrozenFluiddRespondInfo("串口1发送命令：AP")
                #lancaigang241030:
                if self.G_SerialPort2OpenFlag == True:
                    self.Cmds_AMSSerial2Send("AP")
                    self.G_PhrozenFluiddRespondInfo("串口2发送命令：AP")

                self.G_ProzenToolhead.dwell(0.5)

                # self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_CmdP1]外部宏命令-PG101")
                # command_string = """
                #     PG101
                #     """
                # self.G_PhrozenGCode.run_script_from_command(command_string)
                # self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_CmdP1]外部宏命令-到指定待料区位置等待吐料；command_string='%s'" % command_string)
                # self.IfDoPG102Flag=True

                #lancaigang240913：把延時放到外面
                self.G_ProzenToolhead.dwell(6.0)
                #lancaigang231201：检查切线后旧通道线材是否正常退料，不正常则暂停
                self.Cmds_CutFilaIfNormalCheck()
                if self.G_KlipperIfPaused == True:
                        self.G_PhrozenFluiddRespondInfo("切线5秒了喷头还检测到线材，切刀异常了，请检查切刀，暂停klipper打印")
                        #Lo_ChangeChannelIfSuccess = False
                        return


            # self.G_PhrozenFluiddRespondInfo("[(cmds.python)]外部宏命令-PG109；切线后，先吐掉残留喷头的线材")
            # self.PG102Flag=True
            # self.G_PhrozenFluiddRespondInfo("[(dev.python)]self.Flag=True")
            # command_string = """
            # PG109
            # """
            # self.G_PhrozenGCode.run_script_from_command(command_string)
            # self.G_PhrozenFluiddRespondInfo("[(cmds.python)]command_string='%s'" % command_string)
            # self.PG102Flag=False
            # self.G_PhrozenFluiddRespondInfo("[(dev.python)]self.Flag=False")



            #lancaigang231207：
            if self.G_IfInFilaBlockFlag:
                self.G_PhrozenFluiddRespondInfo("进料卡线，先手动P1 E?从喷头上料管取出并手动prz_resume恢复")
                self.G_PhrozenFluiddRespondInfo("+P1END:0,%d" % self.G_ChangeChannelTimeoutNewChan)
                #lancaigang240524：用于UIUX动态界面
                self.G_PhrozenFluiddRespondInfo("+P1Bn:1,%d" % self.G_ChangeChannelTimeoutNewChan)

                return

            
            self.G_ChangeChannelTimeoutOldChan=self.G_ChangeChannelTimeoutNewChan
            self.G_ChangeChannelTimeoutOldGcmd=self.G_ChangeChannelTimeoutNewGcmd
            self.G_ChangeChannelTimeoutNewChan=int(params["B"])
            self.G_ChangeChannelTimeoutNewGcmd=gcmd


            #手动完全回退料
            self.Cmds_P1BnWholeRollbackAction(int(params["B"]), gcmd)

            #lancaigang240115:延时1秒
            time.sleep(1)
            #lancaigang240524：用于UIUX动态界面
            self.G_PhrozenFluiddRespondInfo("+P1Bn:1,%d" % self.G_ChangeChannelTimeoutNewChan)





        # P1 D[n] 手动到停靠位
        if "D" in params:
            self.G_PhrozenFluiddRespondInfo("P1 D?")
            #lancaigang240527：未知模式，因为要操作手动命令，默认让STM32进入MC多色模式
            if self.G_AMSDeviceWorkMode == AMS_WORK_MODE_UNKNOW:
                self.G_PhrozenFluiddRespondInfo("未知模式，因为要操作手动命令，默认让STM32进入MC多色模式")
                #lancaigang241030:
                if self.G_SerialPort1OpenFlag == True:
                    self.Cmds_AMSSerial1Send("MC")
                    self.G_PhrozenFluiddRespondInfo("串口1发送命令：MC")
                #lancaigang241030:
                if self.G_SerialPort2OpenFlag == True:
                    self.Cmds_AMSSerial2Send("MC")
                    self.G_PhrozenFluiddRespondInfo("串口2发送命令：MC")
                
                self.G_ProzenToolhead.dwell(2)
            
            self.G_PhrozenFluiddRespondInfo("命令='%s'；手动到停靠位" % (gcmd.get_commandline(),))
            #lancaigang240524：用于UIUX动态界面
            self.G_PhrozenFluiddRespondInfo("+P1Dn:0,%d" % self.G_ChangeChannelTimeoutNewChan)
            if not int(params["D"]) in range(1, AMS_MAX_CHANNEL + 1):
                raise gcmd.error("无效参数命令;cmd '%s', that must is D?" % (gcmd.get_commandline()))
            
            #lancaigang231209：手动调式可不用管暂停
            self.G_KlipperIfPaused=False
            #lancaigang240221：stm32主动上报，开启可以暂停1次
            self.STM32ReprotPauseFlag=0
            self.G_PhrozenFluiddRespondInfo("self.STM32ReprotPauseFlag=0")

            #lancaigang240113：手动命令标志
            self.ManualCmdFlag=True
            # #lancaigang240529：补料过程中不暂停
            # self.Cmds_AMSSerial1Send("M0")
            # self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_CmdP1]发送命令=M0")
            # self.G_ProzenToolhead.dwell(1)

            #lancaigang240319：切线之前准备动作
            #self.G_ChangeChannelTimeoutNewChan=int(params["D"])
            #self.Cmds_MoveToCutFilaPrepare()



            if self.G_ToolheadIfHaveFilaFlag:
                #lancaigang231205：复位切线回退
                self.Cmds_MoveToCutFilaAndNotRollback(gcmd)
                self.G_PhrozenFluiddRespondInfo("喷头有线材，所有AMS先回退")
                # self.Cmds_AMSSerial1Send("G%d" % self.G_ChangeChannelTimeoutOldChan)
                # self.G_PhrozenFluiddRespondInfo("G%d" % self.G_ChangeChannelTimeoutOldChan)
                # self.G_PhrozenFluiddRespondInfo("AMS旧通道先回退一段距离: G%d" % self.G_ChangeChannelTimeoutOldChan)
                #lancaigang241030:
                if self.G_SerialPort1OpenFlag == True:
                    self.Cmds_AMSSerial1Send("AP")
                    self.G_PhrozenFluiddRespondInfo("串口1发送命令：AP")
                #lancaigang241030:
                if self.G_SerialPort2OpenFlag == True:
                    self.Cmds_AMSSerial2Send("AP")
                    self.G_PhrozenFluiddRespondInfo("串口2发送命令：AP")

                self.G_ProzenToolhead.dwell(0.5)

                # self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_CmdP1]外部宏命令-PG101")
                # command_string = """
                #     PG101
                #     """
                # self.G_PhrozenGCode.run_script_from_command(command_string)
                # self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_CmdP1]外部宏命令-到指定待料区位置等待吐料；command_string='%s'" % command_string)
                # self.IfDoPG102Flag=True

                #lancaigang240913：把延時放到外面
                self.G_ProzenToolhead.dwell(6.0)
                #lancaigang231201：检查切线后旧通道线材是否正常退料，不正常则暂停
                self.Cmds_CutFilaIfNormalCheck()
                if self.G_KlipperIfPaused == True:
                        self.G_PhrozenFluiddRespondInfo("切线5秒了喷头还检测到线材，切刀异常了，请检查切刀，暂停klipper打印")
                        #Lo_ChangeChannelIfSuccess = False
                        return


            # self.G_PhrozenFluiddRespondInfo("[(cmds.python)]外部宏命令-PG109；切线后，先吐掉残留喷头的线材")
            # self.PG102Flag=True
            # self.G_PhrozenFluiddRespondInfo("[(dev.python)]self.Flag=True")
            # command_string = """
            # PG109
            # """
            # self.G_PhrozenGCode.run_script_from_command(command_string)
            # self.G_PhrozenFluiddRespondInfo("[(cmds.python)]command_string='%s'" % command_string)
            # self.PG102Flag=False
            # self.G_PhrozenFluiddRespondInfo("[(dev.python)]self.Flag=False")

            #lancaigang231207：
            if self.G_IfInFilaBlockFlag:
                self.G_PhrozenFluiddRespondInfo("进料卡线，先手动P1 E?从喷头上料管取出并手动prz_resume恢复")
                self.G_PhrozenFluiddRespondInfo("+P1END:0,%d" % self.G_ChangeChannelTimeoutNewChan)
                #lancaigang240524：用于UIUX动态界面
                self.G_PhrozenFluiddRespondInfo("+P1Dn:1,%d" % self.G_ChangeChannelTimeoutNewChan)
                return


            self.G_ChangeChannelTimeoutOldChan=self.G_ChangeChannelTimeoutNewChan
            self.G_ChangeChannelTimeoutOldGcmd=self.G_ChangeChannelTimeoutNewGcmd
            self.G_ChangeChannelTimeoutNewChan=int(params["D"])
            self.G_ChangeChannelTimeoutNewGcmd=gcmd

            #手动到停靠位
            self.Cmds_P1DnMoveToParkPositonAction(int(params["D"]), gcmd)

            #lancaigang240115:延时1秒
            time.sleep(1)

            #lancaigang240524：用于UIUX动态界面
            self.G_PhrozenFluiddRespondInfo("+P1Dn:1,%d" % self.G_ChangeChannelTimeoutNewChan)





        #lancaigang231202：强制前转电机，取出喷头料管拿出卡料
        # P1 E[n]
        if "E" in params:
            self.G_PhrozenFluiddRespondInfo("P1 E?")
            # #lancaigang240527：未知模式，因为要操作手动命令，默认让STM32进入MC多色模式
            # if self.G_AMSDeviceWorkMode == AMS_WORK_MODE_UNKNOW:
            #     self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_CmdP1]未知模式，因为要操作手动命令，默认让STM32进入MC多色模式")
            #     self.Cmds_AMSSerial1Send("MC")
            #     self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_CmdP1]发送命令：MC")
            
            self.G_PhrozenFluiddRespondInfo("命令='%s'；强制前转电机，取出喷头料管拿出卡料" % (gcmd.get_commandline(),))
            #lancaigang240524：用于UIUX动态界面
            self.G_PhrozenFluiddRespondInfo("+P1En:0,%d" % self.G_ChangeChannelTimeoutNewChan)
            if not int(params["E"]) in range(1, AMS_MAX_CHANNEL + 1):
                raise gcmd.error("无效参数命令;cmd '%s', that must is E?" % (gcmd.get_commandline()))
            
            #lancaigang231202：不复位切线不回退
            #lancaigang231214：喷头强制取出线材，不用自动切线，需要手工切线
            #self.Cmds_MoveToCutFilaAbsolutePositionNotReset(gcmd)

            #lancaigang240603：防止粘包
            #time.sleep(2)

            #手动到停靠位
            self.Cmds_P1EnForceForward(int(params["E"]), gcmd)

            #lancaigang240524：用于UIUX动态界面
            self.G_PhrozenFluiddRespondInfo("+P1En:1,%d" % self.G_ChangeChannelTimeoutNewChan)





        # lancaigang240228：喷头回抽一段距离，需要stm32先回退一段距离
        # P1 G[n]；n:1~32(设备无组网,取1~4)；指定通道的线料回退一段距离 Yes；====="G?"；
        if "G" in params:
            self.G_PhrozenFluiddRespondInfo("P1 G?")
            # #lancaigang240527：未知模式，因为要操作手动命令，默认让STM32进入MC多色模式
            # if self.G_AMSDeviceWorkMode == AMS_WORK_MODE_UNKNOW:
            #     self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_CmdP1]未知模式，因为要操作手动命令，默认让STM32进入MC多色模式")
            #     self.Cmds_AMSSerial1Send("MC")
            #     self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_CmdP1]发送命令：MC")
            
            self.G_PhrozenFluiddRespondInfo("命令='%s'AMS强制先回退一段距离" % (gcmd.get_commandline(),))
            #lancaigang240524：用于UIUX动态界面
            self.G_PhrozenFluiddRespondInfo("+P1Gn:0,%d" % self.G_ChangeChannelTimeoutNewChan)
            if not int(params["G"]) in range(1, AMS_MAX_CHANNEL + 1):
                raise gcmd.error("无效参数命令;cmd '%s', that must is G?" % (gcmd.get_commandline()))
            

            if self.G_ToolheadIfHaveFilaFlag:
                #lancaigang231205：复位切线回退
                self.Cmds_MoveToCutFilaAndNotRollback(gcmd)
                self.G_PhrozenFluiddRespondInfo("喷头有线材，所有AMS先回退")
                # self.Cmds_AMSSerial1Send("G%d" % self.G_ChangeChannelTimeoutOldChan)
                # self.G_PhrozenFluiddRespondInfo("G%d" % self.G_ChangeChannelTimeoutOldChan)
                # self.G_PhrozenFluiddRespondInfo("AMS旧通道先回退一段距离: G%d" % self.G_ChangeChannelTimeoutOldChan)
                #lancaigang241030:
                if self.G_SerialPort1OpenFlag == True:
                    self.Cmds_AMSSerial1Send("AP")
                    self.G_PhrozenFluiddRespondInfo("串口1发送命令：AP")
                #lancaigang241030:
                if self.G_SerialPort2OpenFlag == True:
                    self.Cmds_AMSSerial2Send("AP")
                    self.G_PhrozenFluiddRespondInfo("串口2发送命令：AP")

                self.G_ProzenToolhead.dwell(0.5)

                # self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_CmdP1]外部宏命令-PG101")
                # command_string = """
                #     PG101
                #     """
                # self.G_PhrozenGCode.run_script_from_command(command_string)
                # self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_CmdP1]外部宏命令-到指定待料区位置等待吐料；command_string='%s'" % command_string)
                # self.IfDoPG102Flag=True

                #lancaigang240913：把延時放到外面
                self.G_ProzenToolhead.dwell(6.0)
                #lancaigang231201：检查切线后旧通道线材是否正常退料，不正常则暂停
                self.Cmds_CutFilaIfNormalCheck()
                if self.G_KlipperIfPaused == True:
                        self.G_PhrozenFluiddRespondInfo("切线5秒了喷头还检测到线材，切刀异常了，请检查切刀，暂停klipper打印")
                        #Lo_ChangeChannelIfSuccess = False
                        return

            

            # self.G_PhrozenFluiddRespondInfo("[(cmds.python)]外部宏命令-PG109；切线后，先吐掉残留喷头的线材")
            # self.PG102Flag=True
            # self.G_PhrozenFluiddRespondInfo("[(dev.python)]self.Flag=True")
            # command_string = """
            # PG109
            # """
            # self.G_PhrozenGCode.run_script_from_command(command_string)
            # self.G_PhrozenFluiddRespondInfo("[(cmds.python)]command_string='%s'" % command_string)
            # self.PG102Flag=False
            # self.G_PhrozenFluiddRespondInfo("[(dev.python)]self.Flag=False")



            self.G_ChangeChannelTimeoutOldChan=self.G_ChangeChannelTimeoutNewChan
            self.G_ChangeChannelTimeoutOldGcmd=self.G_ChangeChannelTimeoutNewGcmd
            self.G_ChangeChannelTimeoutNewChan=int(params["G"])
            self.G_ChangeChannelTimeoutNewGcmd=gcmd

            self.Cmds_P1GnExtruderBack(int(params["G"]), gcmd)

            #lancaigang240524：用于UIUX动态界面
            self.G_PhrozenFluiddRespondInfo("+P1Gn:1,%d" % self.G_ChangeChannelTimeoutNewChan)





        if "H" in params:
            self.G_PhrozenFluiddRespondInfo("P1 H?")
            # #lancaigang240527：未知模式，因为要操作手动命令，默认让STM32进入MC多色模式
            # if self.G_AMSDeviceWorkMode == AMS_WORK_MODE_UNKNOW:
            #     self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_CmdP1]未知模式，因为要操作手动命令，默认让STM32进入MC多色模式")
            #     self.Cmds_AMSSerial1Send("MC")
            #     self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_CmdP1]发送命令：MC")
            
            self.G_PhrozenFluiddRespondInfo("命令='%s'特殊补料" % (gcmd.get_commandline(),))
            #lancaigang240524：用于UIUX动态界面
            self.G_PhrozenFluiddRespondInfo("+P1Hn:0,%d" % self.G_ChangeChannelTimeoutNewChan)
            if not int(params["H"]) in range(1, AMS_MAX_CHANNEL + 1):
                raise gcmd.error("无效参数命令;cmd '%s', that must is H?" % (gcmd.get_commandline()))
            
            

            self.Cmds_P1HnSpecialInfila(int(params["H"]), gcmd)


            #lancaigang240524：用于UIUX动态界面
            self.G_PhrozenFluiddRespondInfo("+P1Hn:1,%d" % self.G_ChangeChannelTimeoutNewChan)





        # =====P1 I[n]；手动挤料时stm32需要补料；====="I?"；
        if "I" in params:
            self.G_PhrozenFluiddRespondInfo("P1 I?")
            # #lancaigang240527：未知模式，因为要操作手动命令，默认让STM32进入MC多色模式
            # if self.G_AMSDeviceWorkMode == AMS_WORK_MODE_UNKNOW:
            #     self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_CmdP1]未知模式，因为要操作手动命令，默认让STM32进入MC多色模式")
            #     self.Cmds_AMSSerial1Send("MC")
            #     self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_CmdP1]发送命令：MC")
            
            self.G_PhrozenFluiddRespondInfo("命令='%s'手动挤料时stm32需要补料" % (gcmd.get_commandline(),))
            #lancaigang240524：用于UIUX动态界面
            self.G_PhrozenFluiddRespondInfo("+P1In:0,%d" % self.G_ChangeChannelTimeoutNewChan)
            if not int(params["I"]) in range(-1000, 1000):
                raise gcmd.error("无效参数命令;cmd '%s', 手动挤料过长" % (gcmd.get_commandline()))
            
            

            self.Cmds_P1InExtruderBack(int(params["I"]), gcmd)


            #lancaigang240524：用于UIUX动态界面
            self.G_PhrozenFluiddRespondInfo("+P1In:1,%d" % self.G_ChangeChannelTimeoutNewChan)


        # =====P1 J[n]；多色手动吐料；缓冲器不满时补料；
        if "J" in params:
            self.G_PhrozenFluiddRespondInfo("P1 J?")

            self.G_PhrozenFluiddRespondInfo("命令='%s'手动挤料时stm32需要补料" % (gcmd.get_commandline(),))
            #lancaigang240524：用于UIUX动态界面
            self.G_PhrozenFluiddRespondInfo("+P1Jn:0,%d" % self.G_ChangeChannelTimeoutNewChan)
            if not int(params["J"]) in range(-1000, 1000):
                raise gcmd.error("无效参数命令;cmd '%s', 手动挤料参数异常" % (gcmd.get_commandline()))
            
            

            self.Cmds_P1JnManualSpitFila(int(params["J"]), gcmd)


            #lancaigang240524：用于UIUX动态界面
            self.G_PhrozenFluiddRespondInfo("+P1Jn:1,%d" % self.G_ChangeChannelTimeoutNewChan)






        #lancaigang240105：命令后加一条完成AT命令
        self.G_PhrozenFluiddRespondInfo("+P1END:0,%d" % self.G_ChangeChannelTimeoutNewChan)
    


    ####################################
    #函数名称：
    #输入参数：
    #返 回 值:
    #功能描述：蓝才刚-20230830
    ####################################
    # P0 M1；多色模式模式(需连接外部设备) Yes；"MC";P0 M1;P28;P2 A1;
    # P0 M2；多色中单色续料模式(需连接外部设备)；"MA";P0 M2;P28;P8;
    # P0 M3; 单色断料模式;P0 M3;
    #lancaigang240801:
    # P0 B?
    def Cmds_CmdP0(self, gcmd):
        self.G_PhrozenFluiddRespondInfo("[(cmds.py)Cmds_CmdP0]命令='%s'" % (gcmd.get_commandline(),))

        self.G_PhrozenFluiddRespondInfo("V-H%s-I%s-F%s" % (HW_VERSION,IMAGE_VERSION,FW_VERSION))

        #获取命令参数M?
        params = gcmd.get_command_parameters()

        # if not "M" in params:
        #     return


        #解锁
        self.Base_AMSSerialCmdUnlock()







        #lancaigang240801：P2 M?
        if "M" in params:
            #lancaigang250522：清空AMS连接
            self.G_AMSDevice1IfNormal=False
            self.G_AMSDevice2IfNormal=False

            #lancaigang250526：
            self.G_IfToolheadHaveFilaInitiativePauseFlag=False
            #lancaigang250526：暂停中，不允许新的gcode命令，需等待暂停完成
            self.G_KlipperInPausing = False
            #lancaigang250527：暂停快速执行
            self.G_KlipperQuickPause = False
            #lancaigang250607：打印状态；1-退料中；2-进料中；3-打印中；4-暂停
            self.G_KlipperPrintStatus= -1
            self.G_ASM1DisconnectErrorCount=0
            #lancaigang250812:单色断料检测，补充回到暂停区
            self.G_RetryToPauseAreaFlag = False
            self.G_RetryToPauseAreaCount = 0
            self.G_P10SpitNum=0
            self.G_IfChangeFilaOngoing= False
            #lancaigang240223：喷头切线失败标记
            self.ToolheadCutFlag = False











            #lancaigang250618：单色M3断料检测
            self.G_P0M3Flag = False
            #lancaigang250618：单色续料M2断料检测
            self.G_P0M2MAStartPrintFlag = 0
            self.ManualCmdFlag=False
            #lancaigang250805:切刀测试
            self.G_CutCheckTest=False


            #lancaigang250515:清空串口屏配置数据
            self.Cmds_GetUartScreenCfgClear()

            #lancaigang250514：读取json文件，获取单色续料配置和通道线材颜色配对
            #/home/prz/klipper/klippy/extras/phrozen_dev/serial-screen/test.json
            self.Cmds_GetUartScreenCfg()
            
            self.G_PhrozenFluiddRespondInfo("当前模式")
            if self.G_AMSDeviceWorkMode == AMS_WORK_MODE_UNKNOW:
                self.G_PhrozenFluiddRespondInfo("+Mode:0,unkown")
            elif self.G_AMSDeviceWorkMode == AMS_WORK_MODE_MC:
                self.G_PhrozenFluiddRespondInfo("+Mode:1,MC")
            elif self.G_AMSDeviceWorkMode == AMS_WORK_MODE_MA:
                self.G_PhrozenFluiddRespondInfo("+Mode:2,MA")
            elif self.G_AMSDeviceWorkMode == AMS_WORK_MODE_FILA_RUNOUT:
                self.G_PhrozenFluiddRespondInfo("+Mode:3,RUNOUT")
            else:
                self.G_PhrozenFluiddRespondInfo("+Mode:-1,error")


            #time.sleep(0.5)
            self.G_PhrozenFluiddRespondInfo("延时1")
            self.G_ProzenToolhead.dwell(1)

            #lancaigang250619:检查AMS是否重新连接成功
            self.Cmds_USBConnectErrorCheck()


            # #cancel取消命令
            # self.G_PhrozenPrinterCancelPauseResume.cmd_CANCEL_PRINT(None)
            #lancaigang250517：
            #self.G_PhrozenPrinterCancelPauseResume.cmd_CLEAR_PAUSE
            # #cancel取消命令
            # self.G_PhrozenPrinterCancelPauseResume.cmd_CANCEL_PRINT(None)
            #lancaigang250517：
            Lo_PauseStatus=self.G_PhrozenPrinterCancelPauseResume.get_status(None)
            self.G_PhrozenFluiddRespondInfo("当前暂停状态-Lo_PauseStatus='%s'" % Lo_PauseStatus)
            self.G_PhrozenPrinterCancelPauseResume.cmd_CLEAR_PAUSE(None)
            self.G_PhrozenFluiddRespondInfo("清空暂停状态")
            Lo_PauseStatus=self.G_PhrozenPrinterCancelPauseResume.get_status(None)
            self.G_PhrozenFluiddRespondInfo("当前暂停状态-Lo_PauseStatus='%s'" % Lo_PauseStatus)
            self.G_PhrozenFluiddRespondInfo("Lo_PauseStatus['is_paused']='%s'" % Lo_PauseStatus['is_paused'])
            #// 当前暂停状态-Lo_PauseStatus='{'is_paused': True}'
            if Lo_PauseStatus['is_paused'] == True:
                self.G_PhrozenFluiddRespondInfo("已是暂停状态")
            else:
                self.G_PhrozenFluiddRespondInfo("未暂停状态")
            #lancaigang240511：初始化一下串口，防止热插拔AMS导致的串口通讯异常
            try:
                self.G_PhrozenFluiddRespondInfo("重新初始化串口1")
                self.G_SerialPort1Obj = serial.Serial(self.G_Serialport1Define, SERIAL_PORT_BAUD, timeout=3)
                #串口打开成功
                if self.G_SerialPort1Obj is not None:
                    if self.G_SerialPort1Obj.is_open:
                        self.G_SerialPort1OpenFlag = True
                        self.G_PhrozenFluiddRespondInfo("重新初始化串口1成功")
                        #lancaigang231213：打开串口
                        self.G_SerialPort1Obj.flushInput()  # clean serial write cache
                        self.G_SerialPort1Obj.flush()
                        self.G_PhrozenFluiddRespondInfo("串口1清空")
                        self.G_PhrozenFluiddRespondInfo("重新注册串口1回调函数")
                        self.G_SerialPort1RecvTimmer = self.G_PhrozenReactor.register_timer(self.Device_TimmerUart1Recv, self.G_PhrozenReactor.NOW)
            except:
                self.G_PhrozenFluiddRespondInfo("未能打开tty1口，请检查USB口或重启尝试")

            try:
                self.G_PhrozenFluiddRespondInfo("重新初始化串口2")
                self.G_SerialPort2Obj = serial.Serial(self.G_Serialport2Define, SERIAL_PORT_BAUD, timeout=3)
                #串口打开成功
                if self.G_SerialPort2Obj is not None:
                    if self.G_SerialPort2Obj.is_open:
                        self.G_SerialPort2OpenFlag = True
                        self.G_PhrozenFluiddRespondInfo("重新初始化串口2成功")
                        self.G_SerialPort2Obj.flushInput()  # clean serial write cache
                        self.G_SerialPort2Obj.flush()
                        self.G_PhrozenFluiddRespondInfo("串口2清空")
                        self.G_PhrozenFluiddRespondInfo("重新注册串口2回调函数")
                        self.G_SerialPort2RecvTimmer = self.G_PhrozenReactor.register_timer(self.Device_TimmerUart2Recv, self.G_PhrozenReactor.NOW)
            except:
                self.G_PhrozenFluiddRespondInfo("未能打开tty2口，请检查USB口或重启尝试")




            #lancaigang250323：
            self.G_PhrozenFluiddRespondInfo("外部宏命令-PG103-获取喷头热端温度；全局")
            command_string = """
                PG103
                """
            self.G_PhrozenGCode.run_script_from_command(command_string)
            self.G_PhrozenFluiddRespondInfo("外部宏命令-PG103；command_string='%s'" % command_string)





            #获取命令模式参数
            Lo_AMSWorkMode = int(params["M"])

            if not Lo_AMSWorkMode in [
                AMS_WORK_MODE_UNKNOW,#未知模式 0
                AMS_WORK_MODE_MC,#MC模式 1
                AMS_WORK_MODE_MA,#单色MA模式 2
                AMS_WORK_MODE_FILA_RUNOUT,#断线处理模式 3
            ]:
                raise gcmd.error("无效参数命令;cmd '%s', that must is M[0/1/2/3]" % (gcmd.get_commandline(),))
            



            self.G_AMSDeviceWorkMode = Lo_AMSWorkMode
            self.Cmds_PrintMode(self.G_AMSDeviceWorkMode)


        
            self.G_PhrozenFluiddRespondInfo("当前模式")
            if self.G_AMSDeviceWorkMode == AMS_WORK_MODE_UNKNOW:
                self.G_PhrozenFluiddRespondInfo("+Mode:0,unkown")
            elif self.G_AMSDeviceWorkMode == AMS_WORK_MODE_MC:
                self.G_PhrozenFluiddRespondInfo("+Mode:1,MC")
            elif self.G_AMSDeviceWorkMode == AMS_WORK_MODE_MA:
                self.G_PhrozenFluiddRespondInfo("+Mode:2,MA")
            elif self.G_AMSDeviceWorkMode == AMS_WORK_MODE_FILA_RUNOUT:
                self.G_PhrozenFluiddRespondInfo("+Mode:3,RUNOUT")
            else:
                self.G_PhrozenFluiddRespondInfo("+Mode:-1,error")



            #lancaigang240410：
            self.G_CancelFlag=False
            #lancaigang240413：暂停状态
            self.G_KlipperIfPaused = False
            #lancaigang240413：stm32主动上报，开启可以暂停1次
            self.STM32ReprotPauseFlag=0

            #lancaigang250515：
            self.G_P0M1MCNoneAMS=0
            self.G_PhrozenFluiddRespondInfo("self.G_P0M1MCNoneAMS=0")


            self.G_PhrozenFluiddRespondInfo("延时1")
            self.G_ProzenToolhead.dwell(1)


            #=====M0;未知模式
            if self.G_AMSDeviceWorkMode == AMS_WORK_MODE_UNKNOW:#0
                self.G_ToolheadFirstInputFila = False
                self.G_PhrozenFluiddRespondInfo("P0 M0未知模式")

                #lancaigang240411：如果没有收到P0 M3命令，不使用断料检测机制
                self.G_P0M3Flag = False
                
                self.G_P0M1MCNoneAMS=0
                self.G_PhrozenFluiddRespondInfo("self.G_P0M1MCNoneAMS=0")


                #lancaigang250327：进入多色换料之前，不允许AMS多色暂停
                self.ManualCmdFlag=True
                self.G_PhrozenFluiddRespondInfo("self.ManualCmdFlag=True")

                #lancaigang250104：P2A3标志位
                if self.G_P2A3Flag == 1:
                    self.G_P2A3Flag = 0
                    #lancaigang240416:
                    if self.G_SerialPort1OpenFlag == True:
                        self.Cmds_AMSSerial1Send("AT+IDLE")
                        self.G_PhrozenFluiddRespondInfo("串口1发送命令：AT+IDLE")
                    #lancaigang241030:
                    if self.G_SerialPort2OpenFlag == True:
                        self.Cmds_AMSSerial2Send("AT+IDLE")
                        self.G_PhrozenFluiddRespondInfo("串口2发送命令：AT+IDLE")
                
                else:
                    #lancaigang240416:
                    if self.G_SerialPort1OpenFlag == True:
                        self.Cmds_AMSSerial1Send("M0")
                        self.G_PhrozenFluiddRespondInfo("串口1发送命令：M0")
                    #lancaigang241030:
                    if self.G_SerialPort2OpenFlag == True:
                        self.Cmds_AMSSerial2Send("M0")
                        self.G_PhrozenFluiddRespondInfo("串口2发送命令：M0")

                self.G_ProzenToolhead.dwell(0.5)

            #=====M1;多色模式
            #P0 M1
            #P28
            #P2 A1
            #T?
            elif self.G_AMSDeviceWorkMode == AMS_WORK_MODE_MC:  #1
                self.G_PhrozenFluiddRespondInfo("P0 M1多色模式: MC")

                #lancaigang250520：不允許手動
                self.ManualCmdFlag=False

                #lancaigang250304：每次P0M1初始化多色通道，防止记录的通道号导致回退异常
                self.G_ChangeChannelTimeoutOldChan=-1
                self.G_PhrozenFluiddRespondInfo("self.G_ChangeChannelTimeoutOldChan=-1")
                self.G_ChangeChannelTimeoutOldGcmd=None
                self.G_PhrozenFluiddRespondInfo("self.G_ChangeChannelTimeoutOldGcmd=None")
                self.G_ChangeChannelTimeoutNewChan=-1
                self.G_PhrozenFluiddRespondInfo("self.G_ChangeChannelTimeoutNewChan=-1")
                self.G_ChangeChannelTimeoutNewGcmd=None
                self.G_PhrozenFluiddRespondInfo("self.G_ChangeChannelTimeoutNewGcmd=None")


                #lancaigang250102：打印换料次数计算
                self.G_PrintCountNum=0

                #lancaigang240125：不用P28连接也可以先复位切线
                #lancaigang231219：复位切线不回退
                #lancaigang240319：PG28复位太多会导致坐标异常
                #self.Cmds_MoveToCutFilaAndNotRollback(gcmd)


                #lancaigang240416:
                if self.G_SerialPort1OpenFlag == True:
                    self.Cmds_AMSSerial1Send("MC")
                    self.G_PhrozenFluiddRespondInfo("串口1发送命令：MC")

                #lancaigang241030:
                if self.G_SerialPort2OpenFlag == True:
                    self.Cmds_AMSSerial2Send("MC")
                    self.G_PhrozenFluiddRespondInfo("串口2发送命令：MC")



                self.G_ChangeChannelFirstFilaFlag = True


                #time.sleep(0.5)
                self.G_ProzenToolhead.dwell(2.5)


                self.G_PhrozenFluiddRespondInfo("检查是否有AMS")

                if self.G_SerialPort1OpenFlag == True:
                    try:
                        self.G_PhrozenFluiddRespondInfo("try;Lo_AMSDeviceStateRspInfo")
                        #获取多色主板详细状态
                        Lo_AMSDeviceStateRspInfo = self.Cmds_AMSSerialPort1SendWaitRsp("SD", sizeof(AMSDetailInfoBytes))
                        self.G_PhrozenFluiddRespondInfo("tty1串口接收: %s" % Lo_AMSDeviceStateRspInfo)
                        if len(Lo_AMSDeviceStateRspInfo) != sizeof(AMSDetailInfoBytes):
                            self.G_PhrozenFluiddRespondInfo("AMS1未响应，请检查AMS1='%s'" % (gcmd.get_commandline(),))
                            #lancaigang240412:AMS多色标签
                            self.G_AMSDevice1IfNormal=False
                        else:
                            #lancaigang240412:AMS多色标签
                            self.G_AMSDevice1IfNormal=True
                    except:
                        self.G_PhrozenFluiddRespondInfo("except;Lo_AMSDeviceStateRspInfo")

                if self.G_SerialPort2OpenFlag == True:
                    try:
                        self.G_PhrozenFluiddRespondInfo("try;Lo_AMSDeviceStateRspInfo")
                        #获取多色主板详细状态
                        Lo_AMSDeviceStateRspInfo = self.Cmds_AMSSerialPort2SendWaitRsp("SD", sizeof(AMSDetailInfoBytes))
                        self.G_PhrozenFluiddRespondInfo("tty2串口接收: %s" % Lo_AMSDeviceStateRspInfo)
                        if len(Lo_AMSDeviceStateRspInfo) != sizeof(AMSDetailInfoBytes):
                            self.G_PhrozenFluiddRespondInfo("AMS2未响应，请检查AMS2='%s'" % (gcmd.get_commandline(),))
                            self.G_AMSDevice2IfNormal=False
                        else:
                            self.G_AMSDevice2IfNormal=True
                    except:
                        self.G_PhrozenFluiddRespondInfo("except;Lo_AMSDeviceStateRspInfo")



                self.G_ProzenToolhead.dwell(1.0)



                #lancaigang250515:P0 M1多色模型，需要兼容未接AMS处理
                if self.G_AMSDevice1IfNormal==True or self.G_AMSDevice2IfNormal==True:
                    self.G_PhrozenFluiddRespondInfo("=====多色打多色模型P0 M1，有AMS")
                    self.G_PhrozenFluiddRespondInfo("=====多色打多色模型P0 M1，执行P2 A1")
                    self.G_PhrozenFluiddRespondInfo("=====多色打多色模型P0 M1，执行T?")
                    #lancaigang250722：多色自动续料；
                    if self.G_AutoReplaceState == 1:
                        self.G_PhrozenFluiddRespondInfo("=====多色打多色模型自动续料;P0 M1自动转换为P0 M2，开启续料检测")
                        self.G_AMSDeviceWorkMode = AMS_WORK_MODE_MA

                        # #lancaigang240416:
                        # if self.G_SerialPort1OpenFlag == True:
                        #     self.Cmds_AMSSerial1Send("MA")
                        #     self.G_PhrozenFluiddRespondInfo("串口1发送命令：MA")
                        # #lancaigang241030:
                        # if self.G_SerialPort2OpenFlag == True:
                        #     self.Cmds_AMSSerial2Send("MA")
                        #     self.G_PhrozenFluiddRespondInfo("串口2发送命令：MA")

                        self.Cmds_PrintMode(self.G_AMSDeviceWorkMode)
                        self.G_PhrozenFluiddRespondInfo("self.G_AMSDeviceWorkMode = AMS_WORK_MODE_MA")
                        self.G_PhrozenFluiddRespondInfo("P8")
                        #lancaigang241106：
                        self.Cmds_CmdP8(gcmd)

                        if self.G_ToolheadIfHaveFilaFlag:
                            #lancaigang250607:
                            self.G_PhrozenFluiddRespondInfo("可以恢复，STM32打印中快速报错")
                            self.G_KlipperQuickPause = True
                            # #lancaigang250427：
                            # if self.G_SerialPort1OpenFlag == True:
                            #     self.Cmds_AMSSerial1Send("AT+EBLOCKEND")
                            #     self.G_PhrozenFluiddRespondInfo("串口1-AMS结束计时缓冲器满时间")
                            # if self.G_SerialPort2OpenFlag == True:
                            #     self.Cmds_AMSSerial2Send("AT+EBLOCKEND")
                            #     self.G_PhrozenFluiddRespondInfo("串口2-AMS结束计时缓冲器满时间")
                            # #self.G_ProzenToolhead.dwell(1.5)
                            #lancaigang251120：进入吐料，添加标志位，防止PG108吐料过程中喷头霍尔没有线材暂停，导致暂停位置在吐料区，恢复的时候会撞到吐料盒；
                            self.G_PG108Ingoing=1
                            command_string = """
                            PG108
                            """
                            self.G_PhrozenGCode.run_script_from_command(command_string)
                            self.G_PG108Ingoing=0
                            self.G_PhrozenFluiddRespondInfo("command_string='%s'" % command_string)
                            self.G_PhrozenFluiddRespondInfo("吐料完成，喷头检测到有线材，打印")

                    else:
                        self.G_PhrozenFluiddRespondInfo("=====多色打多色模型")
                else:
                    self.G_PhrozenFluiddRespondInfo("=====单色打多色模型P0 M1，没有AMS，执行P0 M3单色打印，屏蔽P2 A1和T?")
                    self.G_PhrozenFluiddRespondInfo("=====P0 M1转换为P0 M3")
                    self.G_AMSDeviceWorkMode = AMS_WORK_MODE_FILA_RUNOUT
                    self.Cmds_PrintMode(self.G_AMSDeviceWorkMode)
                    self.G_PhrozenFluiddRespondInfo("self.G_AMSDeviceWorkMode = AMS_WORK_MODE_FILA_RUNOUT")
                    self.G_P0M1MCNoneAMS=1
                    self.G_PhrozenFluiddRespondInfo("self.G_P0M1MCNoneAMS=1")
                    #lancaigang240411：使用断料检测机制
                    self.G_P0M3Flag = True
                    self.G_PhrozenFluiddRespondInfo("self.G_P0M3Flag = True")
                    if self.G_AutoReplaceState == 1:
                        self.G_PhrozenFluiddRespondInfo("=====单色打多色模型自动续料;")
                    else:
                        self.G_PhrozenFluiddRespondInfo("=====单色打多色模型")

                    self.G_PhrozenFluiddRespondInfo("Lo_PauseStatus['is_paused']='%s'" % Lo_PauseStatus['is_paused'])
                    #// 当前暂停状态-Lo_PauseStatus='{'is_paused': True}'
                    if Lo_PauseStatus['is_paused'] == True:
                        self.G_PhrozenFluiddRespondInfo("已是暂停状态")
                    else:
                        self.G_PhrozenFluiddRespondInfo("未暂停状态")

                    if self.G_ToolheadIfHaveFilaFlag==True:
                        self.G_PhrozenFluiddRespondInfo("检测到线材，开始打印")
                        #lancaigang240412：如果有多色AMS，则执行MA单色续料
                        #lancaigang241030:多台AMS，按顺序优先从第1台开始，只能选1台
                        if self.G_AMSDevice1IfNormal==True:
                            self.G_PhrozenFluiddRespondInfo("检测到线材，AMS1多色连接，请优先使用多色AMS1的线材")
                            self.G_ChangeChannelFirstFilaFlag = True
                        elif self.G_AMSDevice2IfNormal==True:
                            self.G_PhrozenFluiddRespondInfo("检测到线材，AMS2多色连接，请优先使用多色AMS2的线材")
                            self.G_ChangeChannelFirstFilaFlag = True
                        else:
                            self.G_PhrozenFluiddRespondInfo("检测到线材，AMS多色未连接，请手动放进线材")
                            #lancaigang240411：使用断料检测机制
                            self.G_P0M3Flag = True
                            #lancaigang240415：喷头有线材，第一次不用吐料
                            self.G_P0M3ToolheadHaveFilaNotSpittingFlag = True
                        #lancaigang251120：进入吐料，添加标志位，防止PG108吐料过程中喷头霍尔没有线材暂停，导致暂停位置在吐料区，恢复的时候会撞到吐料盒；
                        self.G_PG108Ingoing=1
                        command_string = """
                        PG108
                        """
                        self.G_PhrozenGCode.run_script_from_command(command_string)
                        self.G_PG108Ingoing=0
                        self.G_PhrozenFluiddRespondInfo("command_string='%s'" % command_string)
                        self.G_PhrozenFluiddRespondInfo("吐料完成，喷头检测到有线材，打印")

                    else:
                        self.G_PhrozenFluiddRespondInfo("未检测到线材，暂停")
                        #lancaigang240407：调平前不能暂停
                        self.Cmds_PhrozenKlipperPauseM2M3NoneCmdToSTM32(None)
                        #lancaigang240411：使用断料检测机制
                        self.G_P0M3Flag = True
                        #self.G_PhrozenFluiddRespondInfo("+PAUSE:b,%d" % self.G_ChangeChannelTimeoutNewChan)
                        self.G_PhrozenFluiddRespondInfo("+PAUSE:b,%d,%d" % (self.G_ChangeChannelTimeoutOldChan,self.G_ChangeChannelTimeoutNewChan))

                self.G_ProzenToolhead.dwell(0.5)



            #=====M2;多色中单色自动续料模式
            #P0 M2
            #P28
            #P8
            elif self.G_AMSDeviceWorkMode == AMS_WORK_MODE_MA:  #2
                self.G_PhrozenFluiddRespondInfo("=====P0 M2单色续料模式: MA")

                #lancaigang250520：不允許手動
                self.ManualCmdFlag=False


                #lancaigang250102：打印换料次数计算
                self.G_PrintCountNum=0

                #lancaigang240416:
                if self.G_SerialPort1OpenFlag == True:
                    self.Cmds_AMSSerial1Send("MA")
                    self.G_PhrozenFluiddRespondInfo("串口1发送命令：MA")
                #lancaigang241030:
                if self.G_SerialPort2OpenFlag == True:
                    self.Cmds_AMSSerial2Send("MA")
                    self.G_PhrozenFluiddRespondInfo("串口2发送命令：MA")
    
                self.G_ChangeChannelFirstFilaFlag = True



                self.G_ProzenToolhead.dwell(0.5)

                #time.sleep(1)
                #lancaigang240104：单色M2MA续料模式不能切线
                #lancaigang20231219：复位切线回退
                #self.Cmds_MoveToCutFilaAndNotRollback(gcmd)


            #=====M3;单色断料检测模式
            #lancaigang250511：如果存在AMS多色，则自动启用自动续料模式；P0 M3转换为P0 M2
            elif self.G_AMSDeviceWorkMode == AMS_WORK_MODE_FILA_RUNOUT:#3
                self.G_PhrozenFluiddRespondInfo("P0 M3单色等待线材")

                #lancaigang250520：不允許手動
                self.ManualCmdFlag=False

                #lancaigang250102：打印换料次数计算
                self.G_PrintCountNum=0

                if self.G_SerialPort1OpenFlag == True:
                    try:
                        self.G_PhrozenFluiddRespondInfo("try;Lo_AMSDeviceStateRspInfo")
                        #获取多色主板详细状态
                        Lo_AMSDeviceStateRspInfo = self.Cmds_AMSSerialPort1SendWaitRsp("SD", sizeof(AMSDetailInfoBytes))
                        self.G_PhrozenFluiddRespondInfo("tty1串口接收: %s" % Lo_AMSDeviceStateRspInfo)
                        if len(Lo_AMSDeviceStateRspInfo) != sizeof(AMSDetailInfoBytes):
                            self.G_PhrozenFluiddRespondInfo("AMS1未响应，请检查AMS1='%s'" % (gcmd.get_commandline(),))
                            #lancaigang240412:AMS多色标签
                            self.G_AMSDevice1IfNormal=False
                        else:
                            #lancaigang240412:AMS多色标签
                            self.G_AMSDevice1IfNormal=True
                    except:
                        self.G_PhrozenFluiddRespondInfo("except;Lo_AMSDeviceStateRspInfo")



                if self.G_SerialPort2OpenFlag == True:
                    try:
                        self.G_PhrozenFluiddRespondInfo("try;Lo_AMSDeviceStateRspInfo")
                        #获取多色主板详细状态
                        Lo_AMSDeviceStateRspInfo = self.Cmds_AMSSerialPort2SendWaitRsp("SD", sizeof(AMSDetailInfoBytes))
                        self.G_PhrozenFluiddRespondInfo("tty2串口接收: %s" % Lo_AMSDeviceStateRspInfo)
                        if len(Lo_AMSDeviceStateRspInfo) != sizeof(AMSDetailInfoBytes):
                            self.G_PhrozenFluiddRespondInfo("AMS2未响应，请检查AMS2='%s'" % (gcmd.get_commandline(),))
                            self.G_AMSDevice2IfNormal=False
                        else:
                            self.G_AMSDevice2IfNormal=True
                    except:
                        self.G_PhrozenFluiddRespondInfo("except;Lo_AMSDeviceStateRspInfo")
                        


                #lancaigang241107:
                if self.G_AMSDevice1IfNormal==True or self.G_AMSDevice2IfNormal==True:
                    #lancaigang241106：
                    self.G_P0M2MAStartPrintFlag=0

                    #lancaigang250104：防止串口异常
                    #self.Cmds_CmdP28(None)


                    self.G_PhrozenFluiddRespondInfo("=====多色打单色模型P0 M3")
                    self.G_PhrozenFluiddRespondInfo("self.G_AutoReplaceState=%d" % self.G_AutoReplaceState)



                    #lancaigang250514:如果开启单色自动续料，则P0 M3转换为P0 M2
                    if self.G_AutoReplaceState == 1:
                        #lancaigang250511：如果有AMS多色，转换为单色自动续料模式
                        #P0 M2
                        #P8
                        self.G_PhrozenFluiddRespondInfo("=====多色打单色模型自动续料;P0 M3自动转换为P0 M2，开启续料检测")
                        self.G_AMSDeviceWorkMode = AMS_WORK_MODE_MA
                        self.Cmds_PrintMode(self.G_AMSDeviceWorkMode)
                        self.G_PhrozenFluiddRespondInfo("self.G_AMSDeviceWorkMode = AMS_WORK_MODE_MA")
                        self.G_PhrozenFluiddRespondInfo("P8")
                        #lancaigang241106：
                        self.Cmds_CmdP8(gcmd)

                        if self.G_ToolheadIfHaveFilaFlag:
                            #lancaigang250607:
                            self.G_PhrozenFluiddRespondInfo("可以恢复，STM32打印中快速报错")
                            self.G_KlipperQuickPause = True
                            # #lancaigang250427：
                            # if self.G_SerialPort1OpenFlag == True:
                            #     self.Cmds_AMSSerial1Send("AT+EBLOCKEND")
                            #     self.G_PhrozenFluiddRespondInfo("串口1-AMS结束计时缓冲器满时间")
                            # if self.G_SerialPort2OpenFlag == True:
                            #     self.Cmds_AMSSerial2Send("AT+EBLOCKEND")
                            #     self.G_PhrozenFluiddRespondInfo("串口2-AMS结束计时缓冲器满时间")
                            # #self.G_ProzenToolhead.dwell(1.5)

                    else:
                        self.G_PhrozenFluiddRespondInfo("=====多色打单色P0 M3，开启断线检测")
                        self.G_PhrozenFluiddRespondInfo("P8")
                        #lancaigang241106：
                        self.Cmds_CmdP8(gcmd)
                        if self.G_ToolheadIfHaveFilaFlag:
                            #lancaigang250607:
                            self.G_PhrozenFluiddRespondInfo("可以恢复，STM32打印中快速报错")
                            self.G_KlipperQuickPause = True
                            # #lancaigang250427：
                            # if self.G_SerialPort1OpenFlag == True:
                            #     self.Cmds_AMSSerial1Send("AT+EBLOCKEND")
                            #     self.G_PhrozenFluiddRespondInfo("串口1-AMS结束计时缓冲器满时间")
                            # if self.G_SerialPort2OpenFlag == True:
                            #     self.Cmds_AMSSerial2Send("AT+EBLOCKEND")
                            #     self.G_PhrozenFluiddRespondInfo("串口2-AMS结束计时缓冲器满时间")
                            # #self.G_ProzenToolhead.dwell(1.5)
                        #lancaigang240411：使用断料检测机制
                        self.G_P0M3Flag = True
                        self.G_PhrozenFluiddRespondInfo("self.G_P0M3Flag = True")

                    # #lancaigang250511：如果有AMS多色，单色模式
                    # #P0 M3
                    # #P8
                    # #lancaigang250514：多色打单色
                    # self.G_PhrozenFluiddRespondInfo("P8")
                    # #lancaigang241106：
                    # self.Cmds_CmdP8(gcmd)

                    #lancaigang241106:喷头成功进料
                    if self.G_P0M2MAStartPrintFlag==1:
                        self.G_PhrozenFluiddRespondInfo("喷头有线材")
                    else:
                        self.G_PhrozenFluiddRespondInfo("喷头无线材")
                else:
                    self.G_PhrozenFluiddRespondInfo("=====单色打单色模型P0 M3")
                    self.G_PhrozenFluiddRespondInfo("self.G_AutoReplaceState=%d" % self.G_AutoReplaceState)


                #lancaigang231220：有线材才能打印
                for i in range(10):#
                    self.G_ProzenToolhead.dwell(1.0)
                    #time.sleep(1)
                    self.G_PhrozenFluiddRespondInfo("等待手动放线材；i=%d" % (i))

                    if self.G_ToolheadIfHaveFilaFlag==True:
                        self.G_PhrozenFluiddRespondInfo("检测到线材，开始打印")

                        #lancaigang240412：如果有多色AMS，则执行MA单色续料
                        #lancaigang241030:多台AMS，按顺序优先从第1台开始，只能选1台
                        if self.G_AMSDevice1IfNormal==True:
                            self.G_PhrozenFluiddRespondInfo("检测到线材，AMS1多色连接，请优先使用多色AMS1的线材")
                            self.G_ChangeChannelFirstFilaFlag = True
                        elif self.G_AMSDevice2IfNormal==True:
                            self.G_PhrozenFluiddRespondInfo("检测到线材，AMS2多色连接，请优先使用多色AMS2的线材")
                            self.G_ChangeChannelFirstFilaFlag = True
                        else:
                            self.G_PhrozenFluiddRespondInfo("检测到线材，AMS多色未连接，请手动放进线材")
                            #lancaigang240411：使用断料检测机制
                            self.G_P0M3Flag = True
                            #lancaigang240415：喷头有线材，第一次不用吐料
                            self.G_P0M3ToolheadHaveFilaNotSpittingFlag = True

                        #lancaigang251120：进入吐料，添加标志位，防止PG108吐料过程中喷头霍尔没有线材暂停，导致暂停位置在吐料区，恢复的时候会撞到吐料盒；
                        self.G_PG108Ingoing=1
                        command_string = """
                        PG108
                        """
                        self.G_PhrozenGCode.run_script_from_command(command_string)
                        self.G_PhrozenFluiddRespondInfo("command_string='%s'" % command_string)
                        self.G_PhrozenFluiddRespondInfo("吐料完成，喷头检测到有线材，打印")
                        self.G_PG108Ingoing=0
                        break
                    if i>=9:
                        #lancaigang240412：如果有多色AMS，则执行MA单色续料
                        if self.G_AMSDevice1IfNormal==True:
                            self.G_PhrozenFluiddRespondInfo("AMS1多色连接，请优先使用多色AMS1的线材")
                            self.G_ChangeChannelFirstFilaFlag = True
                        elif self.G_AMSDevice2IfNormal==True:
                            self.G_PhrozenFluiddRespondInfo("AMS2多色连接，请优先使用多色AMS2的线材")
                            self.G_ChangeChannelFirstFilaFlag = True
                        else:
                            self.G_PhrozenFluiddRespondInfo("AMS多色未连接，请手动放进线材")
                            self.G_PhrozenFluiddRespondInfo("等待线材进料超时;暂停")
                            

                            self.G_PhrozenFluiddRespondInfo("Lo_PauseStatus['is_paused']='%s'" % Lo_PauseStatus['is_paused'])
                            #// 当前暂停状态-Lo_PauseStatus='{'is_paused': True}'
                            if Lo_PauseStatus['is_paused'] == True:
                                self.G_PhrozenFluiddRespondInfo("已是暂停状态")
                            else:
                                self.G_PhrozenFluiddRespondInfo("未暂停状态")
                            
                                #lancaigang240407：调平前不能暂停
                                self.Cmds_PhrozenKlipperPauseM2M3NoneCmdToSTM32(None)
                                #lancaigang240411：使用断料检测机制
                                self.G_P0M3Flag = True

                                #self.G_PhrozenFluiddRespondInfo("+PAUSE:b,%d" % self.G_ChangeChannelTimeoutNewChan)
                                self.G_PhrozenFluiddRespondInfo("+PAUSE:b,%d,%d" % (self.G_ChangeChannelTimeoutOldChan,self.G_ChangeChannelTimeoutNewChan))

                            return
                        
                self.G_ProzenToolhead.dwell(0.5)

            self.G_PhrozenFluiddRespondInfo("延时0.5")
            #lancaigang231228：防止随后的命令导致stm32的AT命令粘包
            self.G_ProzenToolhead.dwell(0.5)
            #self.G_ProzenToolhead.dwell(1.0)


        #lancaigang240801：P0 B?
        if "B" in params:
            #self.Cmds_P1CnAutoChangeChannel(int(params["C"]), gcmd)
            #lancaigang240524：用于UIUX动态界面
            self.G_PhrozenFluiddRespondInfo(gcmd.get_commandline())







    ####################################
    #函数名称：
    #输入参数：
    #返 回 值:
    #功能描述：蓝才刚-20230830
    ####################################
    def Cmds_RegisterCmds(self):
        self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_RegisterCmds]注册phrozen自定义gcode命令")
        # P114 S；简单状态；"SB"；
        # P114；所有状态 ；"SD"；
        self.G_PhrozenGCode.register_command(G_DictPhrozenCmdP114["cmd"],self.Cmds_CmdP114,desc=G_DictPhrozenCmdP114["desc"])
        # P28 连接设备
        self.G_PhrozenGCode.register_command(G_DictPhrozenCmdP28["cmd"],self.Cmds_CmdP28,desc=G_DictPhrozenCmdP28["desc"])
        # P29 断开连接
        self.G_PhrozenGCode.register_command(G_DictPhrozenCmdP29["cmd"],self.Cmds_CmdP29,desc=G_DictPhrozenCmdP29["desc"])
        # P30 自动编排设备ID(用于多设备自动组网)；"I";处理自动编排设备ID命令
        self.G_PhrozenGCode.register_command(G_DictPhrozenCmdP30["cmd"],self.Cmds_CmdP30,desc=G_DictPhrozenCmdP30["desc"])
        # P0 M1；多色模式模式(需连接外部设备) Yes；"MC";
        # P0 M2；多色单色续料模式(需连接外部设备)；"MA";
        # P0 M3; 单色断料模式
        #lancaigang240801:
        # P0 B?; 自定义；
        self.G_PhrozenGCode.register_command(G_DictPhrozenP0["cmd"],self.Cmds_CmdP0,desc=G_DictPhrozenP0["desc"])
        # P2 A1 所有线料后退到停靠位打印待位置 Yes；====="AP";
        # P2 A2；退出所有线材 Yes；"CL";
        # P2 A3 切断线材
        # P2 A4 切断线材并回退线材
        # P2 A5 打印完成切断线材并回退线材，不能碰到模型
        self.G_PhrozenGCode.register_command(G_DictPhrozenCmdP2["cmd"],self.Cmds_CmdP2,desc=G_DictPhrozenCmdP2["desc"])
        # P1 S0 所有通道在停靠位准备好进料到打印机状态, 可以进料到停靠位或后退到停靠位；====="RD";
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
        #lancaigang240418：
        # =====P1 V[n]；用于版本号
        # =====P1 W[n]；
        # =====P1 X[n]；
        # =====P1 Y[n]；
        # =====P1 Z[n]；
        self.G_PhrozenGCode.register_command(G_DictPhrozenCmdP1["cmd"],self.Cmds_CmdP1,desc=G_DictPhrozenCmdP1["desc"])
        # P9 X[x_pos]Y[y_pos]W[width]H[height]D[0/1];x_pos:等待区基点X坐标y_pos:等待区基点Y坐标width:等待区宽度
        # height:等待区高度D0:以X方向作慢速移动Y方向计数(默认)D1:以Y方向作慢速移动X方向计数设定等待区域
        # P9 T[expire]A[0/1];expire:超时时间,单位秒(默认60)A0:忽略超时,继续打印(默认)A1:超时后终止打印设定等待超时及处理
        self.G_PhrozenGCode.register_command(G_DictPhrozenCmdP9["cmd"],self.Cmds_CmdP9,desc=G_DictPhrozenCmdP9["desc"])

        #lancaigang241101：
        # P10 S?    参数S[1,5]:吐料次数控制，S1-吐料1次，S2-吐料2次...，最多支持吐料5次
        self.G_PhrozenGCode.register_command(G_DictPhrozenCmdP10["cmd"],self.Cmds_CmdP10,desc=G_DictPhrozenCmdP10["desc"])

        #lancaigang250805：
        # P11 多色切刀测试
        self.G_PhrozenGCode.register_command("P11",self.Cmds_CmdP11,desc="P11")
        #lancaigang250805：
        # P12 多色切刀循环测试
        self.G_PhrozenGCode.register_command("P12",self.Cmds_CmdP12,desc="P12")

        # P8 执行自动续料 Yes；"FA"；
        self.G_PhrozenGCode.register_command(G_DictPhrozenCmdP8["cmd"],self.Cmds_CmdP8,desc=G_DictPhrozenCmdP8["desc"])
        # PRZ_ADC
        self.G_PhrozenGCode.register_command(G_DictPhrozenCmdToolheadAdc["cmd"],self.Cmds_PhrozenAdc,desc=G_DictPhrozenCmdToolheadAdc["desc"])
        # PRZ_PAUSE暂停
        self.G_PhrozenGCode.register_command("PRZ_PAUSE",self.Cmds_PhrozenKlipperPauseScreen,desc="PHROZEN_PAUSE")
        # PRZ_RESUME 恢复
        self.G_PhrozenGCode.register_command("PRZ_RESUME",self.Cmds_PhrozenKlipperResume,desc="PHROZEN_RESUME")
        # PRZ_CANCEL 取消打印
        self.G_PhrozenGCode.register_command("PRZ_CANCEL",self.Cmds_PhrozenKlipperCancel,desc="PHROZEN_CANCEL")
        # PRZ_VERSION 查询版本
        self.G_PhrozenGCode.register_command("PRZ_VERSION",self.Cmds_PhrozenVersion,desc="PHROZEN_VERSION")
        # P4 紧急停止设备；紧急停止Stop命令(次优先级)："SP"；
        self.G_PhrozenGCode.register_command(G_DictPhrozenCmdP4["cmd"],self.Cmds_CmdP4,desc=G_DictPhrozenCmdP4["desc"])

        self.G_PhrozenGCode.register_command("PRZ_BM1",self.Cmds_PhrozenBM1,desc="PRZ_BM1")
        self.G_PhrozenGCode.register_command("PRZ_BM0",self.Cmds_PhrozenBM0,desc="PRZ_BM0")

        self.G_PhrozenGCode.register_command("PRZ_PRINT_START",self.Cmds_PrzPrintStart,desc="PRZ_PRINT_START")
        
        #self.G_PhrozenGCode.register_command("PRINT_END",self.Cmds_PrzPrintEnd,desc="PRINT_END")
        #lancaigang250514:
        self.G_PhrozenGCode.register_command("homing_override_end",self.Cmds_HomingOverrideEnd,desc="homing_override_end")

        #lancaigang250115：
        self.G_PhrozenGCode.register_command("PRZ_RESTORE",self.Cmds_PrzATRestore,desc="PRZ_RESTORE")
        self.G_PhrozenGCode.register_command("PRZ_IDLE",self.Cmds_PrzATIdle,desc="PRZ_IDLE")


        #lancaigang250324：兼容orca切片软件的T0 T1 T2 T3换色命令
        self.G_PhrozenGCode.register_command("T0",self.Cmds_CmdT0,desc="T0")
        self.G_PhrozenGCode.register_command("T1",self.Cmds_CmdT1,desc="T1")
        self.G_PhrozenGCode.register_command("T2",self.Cmds_CmdT2,desc="T2")
        self.G_PhrozenGCode.register_command("T3",self.Cmds_CmdT3,desc="T3")
        self.G_PhrozenGCode.register_command("T4",self.Cmds_CmdT4,desc="T4")
        self.G_PhrozenGCode.register_command("T5",self.Cmds_CmdT5,desc="T5")
        self.G_PhrozenGCode.register_command("T6",self.Cmds_CmdT6,desc="T6")
        self.G_PhrozenGCode.register_command("T7",self.Cmds_CmdT7,desc="T7")
        self.G_PhrozenGCode.register_command("T8",self.Cmds_CmdT8,desc="T8")
        self.G_PhrozenGCode.register_command("T9",self.Cmds_CmdT9,desc="T9")
        self.G_PhrozenGCode.register_command("T10",self.Cmds_CmdT10,desc="T10")
        self.G_PhrozenGCode.register_command("T11",self.Cmds_CmdT11,desc="T11")
        self.G_PhrozenGCode.register_command("T12",self.Cmds_CmdT12,desc="T12")
        self.G_PhrozenGCode.register_command("T13",self.Cmds_CmdT13,desc="T13")
        self.G_PhrozenGCode.register_command("T14",self.Cmds_CmdT14,desc="T14")
        self.G_PhrozenGCode.register_command("T15",self.Cmds_CmdT15,desc="T15")







        



