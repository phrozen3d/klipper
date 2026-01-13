####################################
#项目名称：
#芯片类型: 
#功能: 
#研发人员：蓝才刚
#开发时间: 20230830
####################################

import binascii
import logging
import time
import struct
import serial
import re

from .cwebsocketapis import *




####################################
#类名：
#功能描述：蓝才刚-20230830
####################################
class PhrozenDev(Apis):
    ####################################
    #函数名称：
    #输入参数：
    #返 回 值:
    #功能描述：蓝才刚-20230830
    ####################################
    #构造函数初始化
    def __init__(self, config):
        super(PhrozenDev, self).__init__(config)
        #初始化事件连接klipper
        self.G_PhrozenPrinter.register_event_handler("klippy:connect", self.Device_KlipperConnectHandle)
        #初始化事件取消连接klipper
        self.G_PhrozenPrinter.register_event_handler("klippy:disconnect", self.Device_KlipperDisconnectHandle)

        # dev.py；重置AMS运行参数
        self.Device_ResetParams()

        # cmds.py；phrozen自定义GCODE命令
        self.Cmds_RegisterCmds()

        # cwebsocketapis.py；网页websocket api
        self.WebsocketAPIs_RegisterAPIs()

        # dev.py；测试命令PRZ_TEST
        self.G_PhrozenGCode.register_command("PRZ_TEST", self.Device_CmdPhrozenTest, desc="Phrozen多色机测试命令")
    ####################################
    #函数名称：
    #输入参数：
    #返 回 值:
    #功能描述：蓝才刚-20230830
    ####################################
    #AMS重置参数
    def Device_ResetParams(self):
        self.G_PhrozenFluiddRespondInfo("[(dev.python)Device_ResetParams]重置AMS运行参数")
        self.G_FilaRunoutTimmer = None  # 断线处理定时器
        self.G_SerialPort1RecvTimmer = None  # 串口接收定时器
        #lancaigang241030：
        self.G_SerialPort2RecvTimmer = None  # 串口接收定时器

        self.AMSRunoutPauseTimeCount = 0  # 守护线程中暂等时间计数
        self.G_ToolheadFirstInputFila = False  # 首次供料
        self.P0M3FilaRunoutSpittingFinished = False
        self.AMSErrorRetryTimes = 0  # 出错重试次数
        #AMS多色机状态
        self.G_AMS1DeviceState = {}
        #lancaigang241105:
        self.G_AMS2DeviceState = {}

    ####################################
    #函数名称：
    #输入参数：
    #返 回 值:
    #功能描述：蓝才刚-20230830
    ####################################
    #注册定时器断线周期线程
    def Device_RegisterRunoutErrorThread(self):
        self.G_PhrozenFluiddRespondInfo("[(dev.python)Device_RegisterRunoutErrorThread]")
        # 注册断线处理周期线程
        self.G_FilaRunoutTimmer = self.G_PhrozenReactor.register_timer(self.Device_TimmerRunoutCheck, self.G_PhrozenReactor.NOW + 0.5)
    ####################################
    #函数名称：
    #输入参数：
    #返 回 值:
    #功能描述：蓝才刚-20230830
    ####################################
    def Device_UnregisterDaemonThread(self):
        self.G_PhrozenFluiddRespondInfo("[(dev.python)Device_UnregisterDaemonThread]")
        #取消注册
        self.G_PhrozenReactor.unregister_timer(self.G_FilaRunoutTimmer)
        # self.G_PhrozenReactor.unregister_timer(self.G_SerialPort1RecvTimmer)
    ####################################
    #函数名称：
    #输入参数：
    #返 回 值:
    #功能描述：蓝才刚-20230830
    ####################################
    def Device_ConnectAMSDevice(self):
        self.G_PhrozenFluiddRespondInfo("[(dev.python)Device_ConnectAMSDevice]phrozen扩展python模块连接AMS多色")
        #是否自动连接AMS多色机
        #lancaigang240116：不自动连接AMS
        #if self.G_AMSIfAutoConnectFlag:
            #ttyUSB0串口连接AMS多色机
            #self.Cmds_CmdP28(None)
                # #lancaigang231122：使用ttyUSB0之前，需要关掉后台IAP升级程序hdl_zigbee_gateway


    ####################################
    #函数名称：
    #输入参数：
    #返 回 值:
    #功能描述：蓝才刚-20230830
    ####################################
    def Device_DisconnectAMSDevice(self):
        self.G_PhrozenFluiddRespondInfo("[(dev.python)Device_DisconnectAMSDevice]phrozen扩展python模块断开连接AMS多色")
        self.Cmds_CmdP29(None)
    
    ####################################
    #函数名称：
    #输入参数：
    #返 回 值:
    #功能描述：蓝才刚-20230830
    ####################################
    def Device_CmdPhrozenTest(self, gcmd):
        self.G_PhrozenFluiddRespondInfo("[(dev.python)Device_CmdPhrozenTest]gcmd.prz_test测试='%s'" % (gcmd.get_commandline(),))
        self.G_PhrozenFluiddRespondInfo("self.prz_test测试='%s'" % (gcmd.get_commandline(),))
        #klipper暂停
        self.Cmds_PhrozenKlipperPause(None)



    ####################################
    #函数名称：
    #输入参数：
    #返 回 值:
    #功能描述：蓝才刚-20230830
    ####################################
    #初始注册事件；phrozen插件连接klipper
    def Device_KlipperConnectHandle(self):
        self.G_PhrozenFluiddRespondInfo("[(dev.python)Device_KlipperConnectHandle]phrozen扩展python模块连接klipper")
        
        #lancaigang250724：读取系统镜像id，区分不同产品不同主板不同固件
        #lancaigang250724:读取镜像id
        self.Cmds_GetImageId()
        if self.G_ImageId==16:
            self.G_PhrozenFluiddRespondInfo("镜像Id==16：ARCO300-MKS-RK3328-STM32F407VET6-I16")
            os.system('sh /home/mks/klipper/klippy/extras/phrozen_dev/stop.sh &')
            self.G_PhrozenFluiddRespondInfo("sh /home/mks/klipper/klippy/extras/phrozen_dev/stop.sh &")
        elif self.G_ImageId==31:
            self.G_PhrozenFluiddRespondInfo("镜像Id==31：ARCO300-phrozen-RK3308-STM32F407VET6-I31")
            os.system('sh /home/prz/klipper/klippy/extras/phrozen_dev/stop.sh &')
            self.G_PhrozenFluiddRespondInfo("sh /home/prz/klipper/klippy/extras/phrozen_dev/stop.sh &")
        elif self.G_ImageId==-1:
            self.G_PhrozenFluiddRespondInfo("镜像Id==-1，默认：ARCO300-MKS-RK3328-STM32F407VET6-I16")
            os.system('sh /home/mks/klipper/klippy/extras/phrozen_dev/stop.sh &')
            self.G_PhrozenFluiddRespondInfo("sh /home/mks/klipper/klippy/extras/phrozen_dev/stop.sh &")
        else:
            self.G_PhrozenFluiddRespondInfo("镜像Id读不到，默认：ARCO300-MKS-RK3328-STM32F407VET6-I16")
            os.system('sh /home/mks/klipper/klippy/extras/phrozen_dev/stop.sh &')
            self.G_PhrozenFluiddRespondInfo("sh /home/mks/klipper/klippy/extras/phrozen_dev/stop.sh &")

        # 获取喷头动作
        self.G_ProzenToolhead = self.G_PhrozenPrinter.lookup_object("toolhead")
        #喷头手动移动
        self.G_ToolheadManualMovement = self.G_ProzenToolhead.manual_move
        #喷头等待移动结束
        self.G_ToolheadWaitMovementEnd = self.G_ProzenToolhead.wait_moves
        #喷头最后位置
        self.G_ToolheadLastPosition = self.G_ProzenToolhead.get_position()
        # 注册周期断线周期线程
        self.Device_RegisterRunoutErrorThread()

        #lancaigang240430：因为有断电续打功能，如果AMS已经保存了状态，断电重启后不能随意被更改
        #lancaigang240428：如果klipper重启连接，则告诉AMS进入idle状态
        try:
            #打开串口1，波特率19200
            self.G_SerialPort1Obj = serial.Serial(self.G_Serialport1Define, SERIAL_PORT_BAUD, timeout=3)
            if self.G_SerialPort1Obj.is_open:
                #lancaigang231213：打开串口
                self.G_SerialPort1Obj.flushInput()
                self.G_SerialPort1Obj.flush()
                #lancaigang250115:多色断电续打
                self.G_PhrozenFluiddRespondInfo("发送命令: M0")
                self.G_SerialPort1Obj.write("M0".encode())
                self.G_SerialPort1Obj.flush()
                #关闭串口，防止后续的P28异常
                self.G_SerialPort1Obj.close()
        except:
            self.G_PhrozenFluiddRespondInfo("未能打开tty1口，请检查USB口或重启尝试")

        #lancaigang241108：
        try:
            #打开串口2，波特率19200
            self.G_SerialPort2Obj = serial.Serial(self.G_Serialport2Define, SERIAL_PORT_BAUD, timeout=3)
            if self.G_SerialPort2Obj.is_open:
                self.G_SerialPort2Obj.flushInput()
                self.G_SerialPort2Obj.flush()
                self.G_PhrozenFluiddRespondInfo("发送命令:  M0")
                self.G_SerialPort2Obj.write("M0".encode())
                self.G_SerialPort2Obj.flush()
                #关闭串口，防止后续的P28异常
                self.G_SerialPort2Obj.close()
        except:
            self.G_PhrozenFluiddRespondInfo("未能打开tty2口，请检查USB口或重启尝试")


        #lancaigang240427：AMS异常重启，需要记录
        self.G_AMS1ErrorRestartFlag = False
        self.G_AMS1ErrorRestartCount = 0

        #lancaigang241030:
        self.G_AMS2ErrorRestartFlag = False
        self.G_AMS2ErrorRestartCount = 0


        #lancaigang250514：读取json文件，获取单色续料配置和通道线材颜色配对
        #/home/prz/klipper/klippy/extras/phrozen_dev/serial-screen/test.json






    ####################################
    #函数名称：
    #输入参数：
    #返 回 值:
    #功能描述：蓝才刚-20230830
    ####################################
    #初始注册事件；phrozen插件取消连接klipper
    def Device_KlipperDisconnectHandle(self):
        self.G_PhrozenFluiddRespondInfo("[(dev.python)Device_KlipperDisconnectHandle]phrozen扩展python模块断开连接klipper")
        #取消连接AMS多色机
        self.Device_DisconnectAMSDevice()
        self.Device_UnregisterDaemonThread()
        #重置AMS运行参数
        self.Device_ResetParams()
    
    ####################################
    #函数名称：
    #输入参数：
    #返 回 值:
    #功能描述：蓝才刚-20230830
    ####################################
    #单色M3断线
    #单色续料MA断线
    #2s
    def Device_TimmerRunoutCheck(self, eventtime):
        #lancaigang240528:如果是P114读取状态期间，不允许处理smt32上报数据
        if self.G_P114RunFlag>=1:
            self.G_P114RunFlag=self.G_P114RunFlag+1
            if self.G_P114RunFlag>=3:
                self.G_PhrozenFluiddRespondInfo("[(dev.python)Device_TimmerRunoutCheck]P114失败")
                #self.G_PhrozenFluiddRespondInfo("+P114:2")
                #self.G_P114RunFlag=0
                #python空字典
                Lo_AMSDetailState = {"dev_id": -1, "active_dev_id": -1, "dev_mode": -1, "cache_empty": -1, "cache_full": -1, "cache_exist": -1, "mc_state": -1, "ma_state": -1, "entry_state": -1, "park_state": -1}
                # 响应数据json转换
                self.G_PhrozenFluiddRespondInfo(json.dumps(Lo_AMSDetailState))

                #lancaigang250708：
                self.G_PhrozenFluiddRespondInfo("P114失败")
                self.G_PhrozenFluiddRespondInfo("+P114:2")
                self.G_P114RunFlag=0
            

            #self.G_PhrozenFluiddRespondInfo("+P114:1")
            #self.G_P114RunFlag=False
            #return eventtime + AMS_FILA_RUNOUT_TIMER

        #默认为未知模式
        if self.G_AMSDeviceWorkMode == AMS_WORK_MODE_UNKNOW:#M0
            #self.G_PhrozenFluiddRespondInfo("[(dev.python)Device_TimmerRunoutCheck]if self.G_AMSDeviceWorkMode == AMS_WORK_MODE_UNKNOW:")
            return eventtime + AMS_FILA_RUNOUT_TIMER


        #lancaigang240410：
        if self.G_CancelFlag==True:
            #self.G_PhrozenFluiddRespondInfo("[(dev.python)Device_TimmerRunoutCheck]已取消打印")
            return eventtime + AMS_FILA_RUNOUT_TIMER



            


        #lancaigang240105：如果上一次打印的是单机单色，这次打印的是单色续料，会导致喷头如果没线材，一直报错暂停，后续M3 M2单独处理
        # =====M3断线处理模式
        if self.G_AMSDeviceWorkMode == AMS_WORK_MODE_FILA_RUNOUT:#M3 M2
            #self.G_PhrozenFluiddRespondInfo("[(dev.python)Device_TimmerRunoutCheck]单色模式定时器")
            #lancaigang240411：如果没有收到P0 M3命令，不使用断料检测机制
            if self.G_P0M3Flag == False:
                #self.G_PhrozenFluiddRespondInfo("[(dev.python)Device_TimmerRunoutCheck]未收到P0M3命令或有AMS多色，不执行单色M3模式检测机制，使用AMS多色打印单色")
                return eventtime + AMS_FILA_RUNOUT_TIMER
            #else:
                #self.G_PhrozenFluiddRespondInfo("[(dev.python)Device_TimmerRunoutCheck]没有AMS多色并收到P0M3命令，执行单色M3模式检测机制")

            if self.G_ToolheadIfHaveFilaFlag==True:
                self.G_ToolheadFirstInputFila = True
            if self.G_ToolheadFirstInputFila==False:
                self.G_PhrozenFluiddRespondInfo("未检测到线材第1次进料")
                return eventtime + AMS_FILA_RUNOUT_TIMER
            if self.G_ToolheadIfHaveFilaFlag==True:
                if self.P0M3FilaRunoutSpittingFinished==True:#吐料完成
                    #self.G_PhrozenFluiddRespondInfo("[(dev.python)Device_TimmerRunoutCheck]吐料完成")
                    return eventtime + AMS_FILA_RUNOUT_TIMER
                self.G_PhrozenFluiddRespondInfo("检测到线材，开始吐料")
                self.G_PhrozenFluiddRespondInfo("调用外部宏-PG108-单色M3模式开始吐料，已屏蔽不吐料")
                #lancaigang240407：调用了吐料功能，放在吐料之前，防止喷头进料又马上出料，导致执行多次命令报错
                self.P0M3FilaRunoutSpittingFinished = True#吐料完成，防止多次调用命令
                # command = """
                #     G90
                #     G1 X250 Y10 F10000
                #     G91
                #     G1 Z10 F500
                #     G92 E0
                #     G1 E100 F500
                #     G92 E0
                #     G0
                # """
                # self.G_PhrozenGCode.run_script_from_command(command)
                # self.G_PhrozenFluiddRespondInfo("[(dev.python)Device_TimmerRunoutCheck]command=%s" % command)
                if self.G_P0M3ToolheadHaveFilaNotSpittingFlag==True:
                    self.G_PhrozenFluiddRespondInfo("P0M3进入打印发现喷头有线材，不用吐料")
                    self.G_P0M3ToolheadHaveFilaNotSpittingFlag=False
                else:
                    self.G_PhrozenFluiddRespondInfo("不用自动吐料，需要手动恢复再吐料")
                    # command_string = """
                    # PG108
                    # """
                    # self.G_PhrozenGCode.run_script_from_command(command_string)
                    # self.G_PhrozenFluiddRespondInfo("command_string='%s'" % command_string)
                    # self.G_PhrozenFluiddRespondInfo("吐料完成，喷头检测到有线材恢复打印")

                self.STM32ReprotPauseFlag=0
                return self.G_PhrozenReactor.NOW + AMS_FILA_RUNOUT_TIMER
            
            #lancaigang240108：如果已经暂停了，不能重复暂停
            if self.G_KlipperIfPaused==True:
                #lancaigang251127：怀疑导致mcu报错timer too close；
                #self.G_PhrozenFluiddRespondInfo("P0M3单机模式，已经暂停了")
                if self.G_RetryToPauseAreaFlag==False:
                    self.G_RetryToPauseAreaCount=self.G_RetryToPauseAreaCount+1
                    self.G_PhrozenFluiddRespondInfo("self.G_RetryToPauseAreaCount=%d" % self.G_RetryToPauseAreaCount)
                    #lancaigang251124:暂停后多发几次暂停，防止断料暂停有时候停不住；
                    if self.G_RetryToPauseAreaCount >= 6:
                        self.G_RetryToPauseAreaCount=0
                        self.G_RetryToPauseAreaFlag=True
                    else:
                        #lancaigang251124:
                        if self.G_PG108Ingoing==1:
                            self.G_PhrozenFluiddRespondInfo("PG108正在吐料中，喷头霍尔突然发现线材用完了")
                            self.G_PhrozenFluiddRespondInfo("PG108正在吐料中，不能马上暂停，因为暂停会记录当前吐料位置做暂停位置，导致恢复撞到吐料盒")
                        else:
                            self.G_PhrozenFluiddRespondInfo("PG108未在吐料中，断料可以正常暂停")

                            if self.G_KlipperInPausing == True:
                                self.G_PhrozenFluiddRespondInfo("暂停中，不允许重复暂停")
                            else:
                                self.G_PhrozenFluiddRespondInfo("不在暂停中，允许暂停")
                                #lancaigang250527：暂停待料区
                                self.G_PhrozenFluiddRespondInfo("开始调用外部宏命令-PRZ_PAUSE_WAITINGAREA")
                                command = """
                                PRZ_PAUSE_WAITINGAREA
                                """
                                self.G_PhrozenGCode.run_script_from_command(command)
                                self.G_PhrozenFluiddRespondInfo("结束调用外部宏命令:command=%s" % (command))
                
                return eventtime + AMS_FILA_RUNOUT_TIMER
            
            #lancaigang240407：如果喷头没有线材，进入暂停
            if self.G_ToolheadIfHaveFilaFlag==False:
                self.G_PhrozenFluiddRespondInfo("P0M3单机模式，未检测到线材")
                self.G_PhrozenFluiddRespondInfo("self.G_IfChangeFilaOngoing=%d" % self.G_IfChangeFilaOngoing)
                #lancaigang250522：不在AMS多色进料情况下，才可以断料检测
                if self.G_IfChangeFilaOngoing==False:
                    self.AMSRunoutPauseTimeCount = 0
                    self.G_PhrozenFluiddRespondInfo("单机M3单色断线处理;暂停")
                    
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

                        #lancaigang250607:
                        self.G_PhrozenFluiddRespondInfo("不启用快速暂停")
                        self.G_KlipperQuickPause = False

                        if self.G_KlipperInPausing == True:
                            self.G_PhrozenFluiddRespondInfo("暂停中，不允许重复暂停")
                        else:
                            self.G_PhrozenFluiddRespondInfo("不在暂停中，允许暂停")
                            #lancaigang251124:
                            if self.G_PG108Ingoing==1:
                                self.G_PhrozenFluiddRespondInfo("PG108正在吐料中，喷头霍尔突然发现线材用完了")
                                self.G_PhrozenFluiddRespondInfo("PG108正在吐料中，不能马上暂停，因为暂停会记录当前吐料位置做暂停位置，导致恢复撞到吐料盒")
                            else:
                                self.G_PhrozenFluiddRespondInfo("PG108未在吐料中，断料可以正常暂停")

                                self.Cmds_PhrozenKlipperPauseM2M3ToSTM32(None)
                                #lancaigang250812:单色断料检测，补充回到暂停区
                                self.G_RetryToPauseAreaFlag = False
                                self.G_RetryToPauseAreaCount = 0
                                #lancaigang250527：暂停待料区
                                self.G_PhrozenFluiddRespondInfo("开始调用外部宏命令-PRZ_PAUSE_WAITINGAREA")
                                command = """
                                PRZ_PAUSE_WAITINGAREA
                                """
                                self.G_PhrozenGCode.run_script_from_command(command)
                                self.G_PhrozenFluiddRespondInfo("结束调用外部宏命令:command=%s" % (command))
                                #lancaigang250521:有AMS多色
                                #if self.G_AMSDevice1IfNormal==True or self.G_AMSDevice2IfNormal==True:
                                #    self.G_PhrozenFluiddRespondInfo("+PAUSE:4,%d,%d" % (self.G_ChangeChannelTimeoutOldChan,self.G_ChangeChannelTimeoutNewChan))
                                #else:
                                self.G_PhrozenFluiddRespondInfo("+PAUSE:b,%d,%d" % (self.G_ChangeChannelTimeoutOldChan,self.G_ChangeChannelTimeoutNewChan))

                                #lancaigang250527：暂停待料区
                                self.G_PhrozenFluiddRespondInfo("开始调用外部宏命令-PRZ_PAUSE_WAITINGAREA")
                                command = """
                                PRZ_PAUSE_WAITINGAREA
                                """
                                self.G_PhrozenGCode.run_script_from_command(command)
                                self.G_PhrozenFluiddRespondInfo("结束调用外部宏命令:command=%s" % (command))

            self.P0M3FilaRunoutSpittingFinished = False#等待下次吐料
            return self.G_PhrozenReactor.NOW + AMS_FILA_RUNOUT_TIMER


        # #=====MA单色续料
        # if self.G_AMSDeviceWorkMode == AMS_WORK_MODE_MA:#M2
        #     #lancaigang241106：P8进料成功前提下，才执行断料检测并补料
        #     if self.G_P0M2MAStartPrintFlag==1:
        #         #self.G_PhrozenFluiddRespondInfo("[(dev.python)Device_TimmerRunoutCheck]P8进料成功，执行断料检测补料")
        #         #if self.G_ToolheadIfHaveFilaFlag==True:
        #         #    self.G_PhrozenFluiddRespondInfo("P8进料成功，喷头有线材")
        #         if self.G_ToolheadIfHaveFilaFlag==False:
        #             self.G_PhrozenFluiddRespondInfo("P8打印完一个通道，喷头无线材，执行自动补料新通道，移动到待料区等待超时")
        #             #self.Cmds_CmdP8(None)

        #             #lancaigang240104：换料过程中不允许暂停
        #             if self.G_IfChangeFilaOngoing==False:
        #                 self.G_PhrozenFluiddRespondInfo("单色续料临时暂停，等待stm32进新料")
        #                 #喷头无线材，导致klipper暂停
        #                 self.Cmds_PhrozenKlipperPauseNoneCmdToSTM32(None)
        #                 self.AMSRunoutPauseTimeCount = 0
        #                 self.AMSRunoutPauseTimeoutFlag=0

        #     self.P0M3FilaRunoutSpittingFinished = False
        #     #self.G_PhrozenFluiddRespondInfo("[(dev.python)Device_TimmerRunoutCheck]return;self.P0M3FilaRunoutSpittingFinished = False")
        #     return self.G_PhrozenReactor.NOW + AMS_FILA_RUNOUT_TIMER




        #=====M2MA单色续料
        if self.G_AMSDeviceWorkMode == AMS_WORK_MODE_MA:#M2
            #lancaigang250607：打印状态；1-退料中；2-进料中；3-打印中；4-暂停
            if self.G_KlipperPrintStatus == 3:
                #lancaigang250619:如果发现串口异常，则开始计数
                if self.G_SerialPort1OpenFlag==False:
                    self.G_PhrozenFluiddRespondInfo("单色续料打印中；if self.G_KlipperPrintStatus == 3")
                    self.G_ASM1DisconnectErrorCount=self.G_ASM1DisconnectErrorCount+1
                    self.G_PhrozenFluiddRespondInfo("self.G_ASM1DisconnectErrorCount=%d" % self.G_ASM1DisconnectErrorCount)
                    if self.G_ASM1DisconnectErrorCount >= 2: #4s
                        try:
                            self.G_PhrozenFluiddRespondInfo("重新初始化串口1")
                            self.G_SerialPort1Obj = serial.Serial(self.G_Serialport1Define, SERIAL_PORT_BAUD, timeout=3)
                            #串口打开成功
                            if self.G_SerialPort1Obj is not None:
                                if self.G_SerialPort1Obj.is_open:
                                    self.G_SerialPort1OpenFlag = True
                                    self.G_PhrozenFluiddRespondInfo("重新初始化串口1成功")
                                    self.G_ASM1DisconnectErrorCount=0
                                    #self.G_PauseToLCDString=""
                                    #lancaigang231213：打开串口
                                    self.G_SerialPort1Obj.flushInput()  # clean serial write cache
                                    self.G_SerialPort1Obj.flush()
                                    self.G_PhrozenFluiddRespondInfo("串口1清空")
                                    self.G_PhrozenFluiddRespondInfo("重新注册串口1回调函数")
                                    self.G_SerialPort1RecvTimmer = self.G_PhrozenReactor.register_timer(self.Device_TimmerUart1Recv, self.G_PhrozenReactor.NOW)
                        except:
                            self.G_PhrozenFluiddRespondInfo("未能打开tty1口，请检查USB口或重启尝试")
                            self.G_SerialPort1OpenFlag=False
                            self.G_ASM1DisconnectErrorCount=self.G_ASM1DisconnectErrorCount+1
                            self.G_PhrozenFluiddRespondInfo("self.G_ASM1DisconnectErrorCount=%d" % self.G_ASM1DisconnectErrorCount)
                            if self.G_ASM1DisconnectErrorCount >= 5: #10s
                                self.G_ASM1DisconnectErrorCount=0
                                self.G_PhrozenFluiddRespondInfo("AMS1连接断料超过10s，暂停")
                                if self.G_KlipperIfPaused==False:
                                    self.G_KlipperIfPaused = True
                                    #self.Cmds_PhrozenKlipperPauseNoneCmdToSTM32(None)
                                    if self.G_CancelFlag==False:
                                        self.G_PhrozenFluiddRespondInfo("AMS1连接异常暂停")
                                        #lancaigang250604:
                                        if self.G_AMSDeviceWorkMode == AMS_WORK_MODE_UNKNOW:#M0
                                            self.G_PhrozenFluiddRespondInfo("未知模式，不用暂停")
                                        else:
                                            if self.STM32ReprotPauseFlag==0:
                                                self.G_PauseTriggerWhileChangeChannelFlag=True
                                                if self.PG102Flag==True:
                                                    self.G_PhrozenFluiddRespondInfo("正在吐料中，暂缓暂停，待吐料完成再暂停")
                                                    self.PG102DelayPauseFlag=True
                                                    #self.G_PhrozenFluiddRespondInfo("+PAUSE:g,%d,%d" % (self.G_ChangeChannelTimeoutOldChan,self.G_ChangeChannelTimeoutNewChan))
                                                    self.G_PauseToLCDString="+PAUSE:g,%d,%d" % (self.G_ChangeChannelTimeoutOldChan,self.G_ChangeChannelTimeoutNewChan)
                                                else:
                                                    self.G_PhrozenFluiddRespondInfo("未吐料，可以直接暂停")


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
                                                    #self.Cmds_PhrozenKlipperPauseNoneCmdToSTM32(None)
                                                    self.STM32ReprotPauseFlag=1
                                                    #lancaigang231202：P1 C?自动换料时，如果第1次通道就进料异常暂停，如果要恢复，也继续从第1次通道开始
                                                    self.G_ChangeChannelFirstFilaFlag=True
                                                    self.G_PhrozenFluiddRespondInfo("+PAUSE:g,%d,%d" % (self.G_ChangeChannelTimeoutOldChan,self.G_ChangeChannelTimeoutNewChan))
                                                    self.G_PauseToLCDString="+PAUSE:g,%d,%d" % (self.G_ChangeChannelTimeoutOldChan,self.G_ChangeChannelTimeoutNewChan)
                                            else:
                                                self.G_PauseTriggerWhileChangeChannelFlag=True
                                                self.G_PauseToLCDString="+PAUSE:g,%d,%d" % (self.G_ChangeChannelTimeoutOldChan,self.G_ChangeChannelTimeoutNewChan)


                                #if self.G_KlipperIfPaused==True:
                                else:
                                    self.G_PhrozenFluiddRespondInfo("USB异常，当前已经是暂停状态")
                                    self.G_PauseToLCDString="+PAUSE:g,%d,%d" % (self.G_ChangeChannelTimeoutOldChan,self.G_ChangeChannelTimeoutNewChan)


            #lancaigang241106：P8进料成功前提下，才执行断料检测并补料
            if self.G_P0M2MAStartPrintFlag==1:
                #self.G_PhrozenFluiddRespondInfo("[(dev.python)Device_TimmerRunoutCheck]P8进料成功，执行断料检测补料")
                #if self.G_ToolheadIfHaveFilaFlag==True:
                #    self.G_PhrozenFluiddRespondInfo("P8进料成功，喷头有线材")
                # if self.G_ToolheadIfHaveFilaFlag==False:
                #     self.G_PhrozenFluiddRespondInfo("P8打印完一个通道，喷头无线材，执行自动补料新通道，移动到待料区等待超时")
                    #self.Cmds_CmdP8(None)
                #第1次检测进入线材，开始记录，喷头是否有线材
                if self.G_ToolheadIfHaveFilaFlag==True:
                    #喷头第1次检测到线材
                    self.G_ToolheadFirstInputFila = True
                # 第1次没有手动放入线材，返回
                if self.G_ToolheadFirstInputFila==False:
                    #断线处理;未有首次进线情况;if not self.G_ToolheadFirstInputFila:")
                    return eventtime + AMS_FILA_RUNOUT_TIMER
                
                if self.G_ToolheadIfHaveFilaFlag==True:
                    #self.G_PhrozenFluiddRespondInfo("[(dev.python)Device_TimmerRunoutCheck]if self.G_ToolheadIfHaveFilaFlag==True:")
                    
                    if self.P0M3FilaRunoutSpittingFinished==True:
                        #self.G_PhrozenFluiddRespondInfo("[(dev.python)Device_TimmerRunoutCheck]return;if self.P0M3FilaRunoutSpittingFinished==True:")
                        #lancaigang241106：喷头检测到有线后，如果后续一直都是有线状态，则不往下
                        return eventtime + AMS_FILA_RUNOUT_TIMER
                    else:
                        self.P0M3FilaRunoutSpittingFinished = True

                    #lancaigang240123：最后没有线材超时后再进料，不允许自动恢复
                    if self.AMSRunoutPauseTimeoutFlag==1:
                        #lancaigang240221：喷头无料超时后，需要手动点击恢复按钮
                        #self.AMSRunoutPauseTimeoutFlag=0
                        self.G_PhrozenFluiddRespondInfo("单色续料超时，不自动恢复，需要手动恢复")
                        return eventtime + AMS_FILA_RUNOUT_TIMER
                    
                    self.G_PhrozenFluiddRespondInfo("单色续料；喷头从无到有检测到线材恢复打印")

                    if self.AMSRunoutPauseTimeCount>0:
                        self.G_PhrozenFluiddRespondInfo("AMSRunoutPauseTimeCount=%d" % self.AMSRunoutPauseTimeCount)
                        self.AMSRunoutPauseTimeCount=0
                        self.G_M2MAModeResumeFlag=True
                    #lancaigang241106：count为0或超时为0
                    else:
                        self.G_PhrozenFluiddRespondInfo("AMSRunoutPauseTimeCount=%d" % self.AMSRunoutPauseTimeCount)
                        if self.G_KlipperIfPaused == True:
                            self.G_PhrozenFluiddRespondInfo("已经暂停了，需要手动恢复")
                            self.G_PhrozenFluiddRespondInfo("+PAUSE:4,%d,%d" % (self.G_ChangeChannelTimeoutOldChan,self.G_ChangeChannelTimeoutNewChan))
                    #lancaigang240108：单色续料进料，恢复进料正常，可以恢复数据
                    if self.G_M2MAModeResumeFlag==True:
                        #self.Cmds_AMSSerial1Send("FA")
                        #self.G_PhrozenFluiddRespondInfo("单色续料；FA；stm32进新料")
                        self.G_PhrozenFluiddRespondInfo("单色续料；恢复打印")
                        #self.G_PhrozenFluiddRespondInfo("[(dev.python)Device_TimmerRunoutCheck]if self.G_M2MAModeResumeFlag==True:")
                        #lancaigang250611：
                        # self.G_PhrozenFluiddRespondInfo("外部宏命令-PG108-升温吐料擦嘴")
                        # command_string = """
                        #     PG108
                        #     """
                        # self.G_PhrozenGCode.run_script_from_command(command_string)
                        #lancaigang250619:检查AMS是否重新连接成功
                        self.Cmds_USBConnectErrorCheck()
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
                        
                        #lancaigang251124：如果stm32有暂停报错，不能恢复打印；
                        if self.STM32ReprotPauseFlag == 1:
                            self.G_PhrozenFluiddRespondInfo("自动续料模式，检测到有线材，但吐料期间STM32上报有暂停，不能自动恢复")
                            #lancaigang240125：封装函数
                            #self.Cmds_PhrozenKlipperResumeCommon()

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
                            #self.Cmds_PhrozenKlipperPauseNoneCmdToSTM32(None)
                            self.STM32ReprotPauseFlag=1
                            #lancaigang231202：P1 C?自动换料时，如果第1次通道就进料异常暂停，如果要恢复，也继续从第1次通道开始
                            self.G_ChangeChannelFirstFilaFlag=True
                            self.G_PhrozenFluiddRespondInfo(self.G_PauseToLCDString)
                            #lancaigang241106：
                            self.G_P0M2MAStartPrintFlag=0
                        else:
                            self.G_PhrozenFluiddRespondInfo("喷头有线材，恢复")
                            self.G_M2MAModeResumeFlag=False
                            #lancaigang240125：封装函数
                            self.Cmds_PhrozenKlipperResumeCommon()
                            self.G_KlipperIfPaused = False
                            #lancaigang240124：stm32主动上报，开启可以暂停1次
                            self.STM32ReprotPauseFlag=0

                        #self.G_PhrozenFluiddRespondInfo("[(dev.python)Device_TimmerRunoutCheck]self.G_KlipperIfPaused = False")
                        self.G_PhrozenFluiddRespondInfo("+RESUME:2,%d" % self.G_ChangeChannelTimeoutNewChan)

                    #self.G_PhrozenFluiddRespondInfo("[(dev.python)Device_TimmerRunoutCheck]return self.G_PhrozenReactor.NOW + AMS_FILA_RUNOUT_TIMER")
                    #lancaigang240109：改为eventtime
                    return self.G_PhrozenReactor.NOW + AMS_FILA_RUNOUT_TIMER
                    #return eventtime + AMS_FILA_RUNOUT_TIMER
                


                #lancaigang240108：如果已经暂停了，不能重复暂停
                if self.G_KlipperIfPaused==True:
                    self.G_PhrozenFluiddRespondInfo("[(dev.python)Device_TimmerRunoutCheck]单色续料；临时暂停，等待stm32重新进新料")
                    #lancaigang240224：
                    if self.AMSRunoutPauseTimeCount==0:
                        #lancaigang240122：暂停后，马上发送命令给stm32进新料
                        #time.sleep(1)
                        #self.G_ProzenToolhead.dwell(0.5)

                        #self.Cmds_AMSSerial1Send("FA")
                        #lancaigang241106:
                        self.G_PhrozenFluiddRespondInfo("单色续料临时暂停后，P8Infila；stm32进新料")

                        #lancaigang240511：恢复的时候，都初始化一下串口，防止热插拔AMS导致的串口通讯异常
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
                        #lancaigang250515：重新进料
                        self.Cmds_CmdP8Infila()

                    #lancaigang240122：暂停多少s定时等待新的线材；
                    self.AMSRunoutPauseTimeCount=self.AMSRunoutPauseTimeCount+1
                    self.G_PhrozenFluiddRespondInfo("AMSRunoutPauseTimeCount=%d" % self.AMSRunoutPauseTimeCount)

                    #等待stm32进料，如果喷头检测到线材，说明新料已经到达，可以恢复打印
                    if self.G_ToolheadIfHaveFilaFlag==True:
                        self.G_M2MAModeResumeFlag=True
                        self.AMSRunoutPauseTimeCount=0

                        #lancaigang250619:检查AMS是否重新连接成功
                        self.Cmds_USBConnectErrorCheck()
                        if self.G_SerialPort1OpenFlag == True:
                            self.Cmds_AMSSerial1Send("AT+EBLOCKCHECK")
                            self.G_PhrozenFluiddRespondInfo("串口1-AMS开始计时缓冲器满时间")
                        if self.G_SerialPort2OpenFlag == True:
                            self.Cmds_AMSSerial2Send("AT+EBLOCKCHECK")
                            self.G_PhrozenFluiddRespondInfo("串口2-AMS开始计时缓冲器满时间")

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


                        #lancaigang251124：如果stm32有暂停报错，不能恢复打印；
                        if self.STM32ReprotPauseFlag == 1:
                            self.G_PhrozenFluiddRespondInfo("自动续料模式，检测到有线材，但吐料期间STM32上报有暂停，不能自动恢复")
                            #lancaigang240125：封装函数
                            #self.Cmds_PhrozenKlipperResumeCommon()

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
                            #self.Cmds_PhrozenKlipperPauseNoneCmdToSTM32(None)
                            self.STM32ReprotPauseFlag=1
                            #lancaigang231202：P1 C?自动换料时，如果第1次通道就进料异常暂停，如果要恢复，也继续从第1次通道开始
                            self.G_ChangeChannelFirstFilaFlag=True
                            self.G_PhrozenFluiddRespondInfo(self.G_PauseToLCDString)
                            #lancaigang241106：
                            self.G_P0M2MAStartPrintFlag=0
                        else:
                            # self.G_PhrozenFluiddRespondInfo("喷头有线材，恢复")
                            # self.G_M2MAModeResumeFlag=False
                            # #lancaigang240125：封装函数
                            # self.Cmds_PhrozenKlipperResumeCommon()
                            # self.G_KlipperIfPaused = False
                            # #lancaigang240124：stm32主动上报，开启可以暂停1次
                            # self.STM32ReprotPauseFlag=0

                            #lancaigang240125：封装函数
                            self.Cmds_PhrozenKlipperResumeCommon()
                            self.G_PhrozenFluiddRespondInfo("MA单色续料；喷头检测到线材，自动恢复打印")
                            self.G_KlipperIfPaused = False
                            #lancaigang240124：stm32主动上报，开启可以暂停1次
                            self.STM32ReprotPauseFlag=0

                    if self.AMSRunoutPauseTimeCount>=50:
                        self.AMSRunoutPauseTimeCount=0
                        self.AMSRunoutPauseTimeoutFlag=1
                        #self.Cmds_PhrozenKlipperPauseMAToSTM32(None)
                        self.G_PhrozenFluiddRespondInfo("M2MA单色续料；stm32进新料超时100s")
                        self.G_PhrozenFluiddRespondInfo("+PAUSE:4,%d,%d" % (self.G_ChangeChannelTimeoutOldChan,self.G_ChangeChannelTimeoutNewChan))
                        
                    return eventtime + AMS_FILA_RUNOUT_TIMER

                #lancaigang241106:
                if self.G_ToolheadIfHaveFilaFlag==False:
                    #lancaigang240104：换料过程中不允许暂停
                    if self.G_IfChangeFilaOngoing==False:
                        self.G_PhrozenFluiddRespondInfo("M2MA单色续料临时暂停，等待stm32进新料")

                        if self.G_KlipperInPausing == False:
                            self.G_PhrozenFluiddRespondInfo("不在暂停中，允许新的暂停")
                            #lancaigang250607:
                            #self.G_PhrozenFluiddRespondInfo("启用快速暂停")
                            #self.G_KlipperQuickPause = True
                            #喷头无线材，导致klipper暂停
                            self.Cmds_PhrozenKlipperPauseMAToSTM32(None)
                        else:
                            self.G_PhrozenFluiddRespondInfo("暂停中，不允许新的暂停")

                        


                        self.AMSRunoutPauseTimeCount = 0
                        self.AMSRunoutPauseTimeoutFlag=0

            self.P0M3FilaRunoutSpittingFinished = False


            



            return eventtime + AMS_FILA_RUNOUT_TIMER
            #return self.G_PhrozenReactor.NOW + AMS_FILA_RUNOUT_TIMER





        # =====M1MC多色模式
        if self.G_AMSDeviceWorkMode == AMS_WORK_MODE_MC:#M1
            #self.G_PhrozenFluiddRespondInfo("[(dev.python)Device_TimmerRunoutCheck]if self.G_AMSDeviceWorkMode == AMS_WORK_MODE_MC:")
            #self.G_PhrozenFluiddRespondInfo("[(dev.python)Device_TimmerRunoutCheck]断线处理;多色模式下检测处理")

            #lancaigang240407：如果多色模式下打印过程中发现喷头没有线材，需要暂停
            #lancaigang240527：不为none，可以确定是收到了P1Cn命令了
            # if self.G_ChangeChannelTimeoutOldGcmd is not None:
            #     if self.G_ToolheadIfHaveFilaFlag==False:
            #         if self.G_ToolheadIfHaveFilaFlag==False:
            #             self.G_PhrozenFluiddRespondInfo("[(cmds.python)Device_TimmerRunoutCheck]MC多色打印中检测到喷头无线材")

            #lancaigang250607：打印状态；1-退料中；2-进料中；3-打印中；4-暂停
            if self.G_KlipperPrintStatus == 3:
                
                #lancaigang250619:如果发现串口异常，则开始计数
                if self.G_SerialPort1OpenFlag==False:
                    self.G_PhrozenFluiddRespondInfo("多色打印中；if self.G_KlipperPrintStatus == 3")
                    self.G_ASM1DisconnectErrorCount=self.G_ASM1DisconnectErrorCount+1
                    self.G_PhrozenFluiddRespondInfo("多色尝试重新连接；self.G_ASM1DisconnectErrorCount=%d" % self.G_ASM1DisconnectErrorCount)
                    #lancaigang250619:检查AMS是否重新连接成功
                    self.Cmds_USBConnectErrorCheck()

                    if self.G_ASM1DisconnectErrorCount >= 5: #10s
                        try:
                            self.G_PhrozenFluiddRespondInfo("重新初始化串口1")
                            self.G_SerialPort1Obj = serial.Serial(self.G_Serialport1Define, SERIAL_PORT_BAUD, timeout=3)
                            #串口打开成功
                            if self.G_SerialPort1Obj is not None:
                                if self.G_SerialPort1Obj.is_open:
                                    self.G_SerialPort1OpenFlag = True
                                    self.G_PhrozenFluiddRespondInfo("重新初始化串口1成功")
                                    self.G_ASM1DisconnectErrorCount=0
                                    #self.G_PauseToLCDString=""
                                    #lancaigang231213：打开串口
                                    self.G_SerialPort1Obj.flushInput()  # clean serial write cache
                                    self.G_SerialPort1Obj.flush()
                                    self.G_PhrozenFluiddRespondInfo("串口1清空")
                                    self.G_PhrozenFluiddRespondInfo("重新注册串口1回调函数")
                                    self.G_SerialPort1RecvTimmer = self.G_PhrozenReactor.register_timer(self.Device_TimmerUart1Recv, self.G_PhrozenReactor.NOW)
                        except:
                            self.G_PhrozenFluiddRespondInfo("未能打开tty1口，请检查USB口或重启尝试")
                            self.G_SerialPort1OpenFlag=False
                            self.G_ASM1DisconnectErrorCount=self.G_ASM1DisconnectErrorCount+1
                            self.G_PhrozenFluiddRespondInfo("self.G_ASM1DisconnectErrorCount=%d" % self.G_ASM1DisconnectErrorCount)
                            if self.G_ASM1DisconnectErrorCount >= 20: #40s
                                self.G_ASM1DisconnectErrorCount=0
                                self.G_PhrozenFluiddRespondInfo("AMS1连接断料超过40s，暂停")
                                if self.G_KlipperIfPaused==False:
                                    self.G_KlipperIfPaused = True
                                    #self.Cmds_PhrozenKlipperPauseNoneCmdToSTM32(None)
                                    if self.G_CancelFlag==False:
                                        self.G_PhrozenFluiddRespondInfo("AMS1连接异常暂停")
                                        #lancaigang250604:
                                        if self.G_AMSDeviceWorkMode == AMS_WORK_MODE_UNKNOW:#M0
                                            self.G_PhrozenFluiddRespondInfo("未知模式，不用暂停")
                                        else:
                                            if self.STM32ReprotPauseFlag==0:
                                                self.G_PauseTriggerWhileChangeChannelFlag=True
                                                if self.PG102Flag==True:
                                                    self.G_PhrozenFluiddRespondInfo("正在吐料中，暂缓暂停，待吐料完成再暂停")
                                                    self.PG102DelayPauseFlag=True
                                                    #self.G_PhrozenFluiddRespondInfo("+PAUSE:g,%d,%d" % (self.G_ChangeChannelTimeoutOldChan,self.G_ChangeChannelTimeoutNewChan))
                                                    self.G_PauseToLCDString="+PAUSE:g,%d,%d" % (self.G_ChangeChannelTimeoutOldChan,self.G_ChangeChannelTimeoutNewChan)
                                                else:
                                                    self.G_PhrozenFluiddRespondInfo("未吐料，可以直接暂停")
                                                    if self.PG102Flag==True:
                                                        self.G_PhrozenFluiddRespondInfo("正在吐料中，暂缓暂停，待吐料完成再暂停")
                                                        self.PG102DelayPauseFlag=True
                                                        self.G_PauseToLCDString="+PAUSE:g,%d,%d" % (self.G_ChangeChannelTimeoutOldChan,self.G_ChangeChannelTimeoutNewChan)
                                                    else:
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
                                            else:
                                                self.G_PauseTriggerWhileChangeChannelFlag=True
                                                self.G_PauseToLCDString="+PAUSE:g,%d,%d" % (self.G_ChangeChannelTimeoutOldChan,self.G_ChangeChannelTimeoutNewChan)


                                #if self.G_KlipperIfPaused==True:
                                else:
                                    self.G_PhrozenFluiddRespondInfo("USB异常，当前已经是暂停状态")
                                    self.G_PauseToLCDString="+PAUSE:g,%d,%d" % (self.G_ChangeChannelTimeoutOldChan,self.G_ChangeChannelTimeoutNewChan)


            return eventtime + AMS_FILA_RUNOUT_TIMER

        # 多重保护, 预防以上情况失效,定时器停止
        return eventtime + AMS_FILA_RUNOUT_TIMER
    

    ####################################
    #函数名称：
    #输入参数：
    #返 回 值:
    #功能描述：蓝才刚-20230830
    ####################################
    #100ms
    def Device_TimmerUartRecvHandler(self,AMSNum,SerialRxBytes, SerialRxASCIIStr):
        #lancaigang240603:暂停不用打印
        if "+PAUSE" in SerialRxASCIIStr:
            self.G_PhrozenFluiddRespondInfo("[(dev.py)Device_TimmerUartRecvHandler]暂停；%s" % SerialRxASCIIStr)
        else:
            self.G_PhrozenFluiddRespondInfo("[(dev.py)Device_TimmerUartRecvHandler]%s" % SerialRxASCIIStr)

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

        #self.G_PhrozenFluiddRespondInfo("串口接收G_PauseToLCDString: %s" % self.G_PauseToLCDString)

        # # // AMS主板2固件-1 1
        # if "V-H1-I1-F?" in SerialRxASCIIStr:
        #     #=====DriveCodeFile.dat
        #     # 1 , 1 , 24053 , 1 , 0
        #     # 2 , 0 , 0 , 0 , 0
        #     # 3 , 0 , 0 , 0 , 0
        #     # 4 , 0 , 0 , 0 , 0
        #     # 5 , 5 , 24046 , 5 , 0
        #     # 6 , 0 , 0 , 0 , 0
        #     # 7 , 7 , 24051 , 7 , 0
        #     # 8 , 0 , 0 , 0 , 0
        #     # 9 , 0 , 0 , 0 , 0
        #     # 10 , 10 , 24054 , 10 , 0
        #     # 11 , 11 , 24047 , 11 , 0
        #     # 12 , 0 , 0 , 0 , 0
        #     # 13 , 0 , 0 , 0 , 0
        #     # 14 , 0 , 0 , 0 , 0
        #     # 15 , 0 , 0 , 0 , 0
        #     # 16 , 0 , 0 , 0 , 0
        #     #lancaigang240530：版本写到dat文件；DriveCodeJson.dat
        #     filename='/home/prz/hdlDat/DriveCodeFile.dat'
        #     self.G_PhrozenFluiddRespondInfo("filename=%s" % filename)
        #     Lo_AllLine=""
        #     #data = [{"DriveCode":16,"DriveImageType":0,"DriveHwVersion":0,"DriveFwVersion":0,"DriveId":0},{"DriveCode":15,"DriveImageType":0,"DriveHwVersion":0,"DriveFwVersion":0,"DriveId":0},{"DriveCode":14,"DriveImageType":0,"DriveHwVersion":0,"DriveFwVersion":0,"DriveId":0},{"DriveCode":13,"DriveImageType":0,"DriveHwVersion":0,"DriveFwVersion":0,"DriveId":0},{"DriveCode":12,"DriveImageType":0,"DriveHwVersion":0,"DriveFwVersion":0,"DriveId":0},{"DriveCode":11,"DriveImageType":0,"DriveHwVersion":0,"DriveFwVersion":0,"DriveId":0},{"DriveCode":10,"DriveImageType":10,"DriveHwVersion":10,"DriveFwVersion":24045,"DriveId":0},{"DriveCode":9,"DriveImageType":0,"DriveHwVersion":0,"DriveFwVersion":0,"DriveId":0},{"DriveCode":8,"DriveImageType":0,"DriveHwVersion":0,"DriveFwVersion":0,"DriveId":0},{"DriveCode":7,"DriveImageType":0,"DriveHwVersion":0,"DriveFwVersion":0,"DriveId":0},{"DriveCode":6,"DriveImageType":0,"DriveHwVersion":0,"DriveFwVersion":0,"DriveId":0},{"DriveCode":5,"DriveImageType":5,"DriveHwVersion":5,"DriveFwVersion":24046,"DriveId":0},{"DriveCode":4,"DriveImageType":0,"DriveHwVersion":0,"DriveFwVersion":0,"DriveId":0},{"DriveCode":3,"DriveImageType":0,"DriveHwVersion":0,"DriveFwVersion":0,"DriveId":0},{"DriveCode":2,"DriveImageType":0,"DriveHwVersion":0,"DriveFwVersion":0,"DriveId":0},{"DriveCode":1,"DriveImageType":1,"DriveHwVersion":1,"DriveFwVersion":24042,"DriveId":0}]
        #     #f = open(filename, 'a')
        #     #json.dump(data, f)  #对象序列号为字节流
        #     #f.close()
        #     with open(filename,'r') as file:
        #         #for line in file:
        #         # # realine() 读取整行内容，包括 "\n" 字符
        #         # self.G_PhrozenFluiddRespondInfo(file.readline().strip())
        #         # #time.sleep(1)
        #         Lo_FileDataList=file.readlines()
        #         for line in Lo_FileDataList:
        #             #split = [i[:-1].split(',') for i in file.readlines()]
        #             #self.G_PhrozenFluiddRespondInfo(type(split))
        #             #self.G_PhrozenFluiddRespondInfo(split[1])
        #             #self.G_PhrozenFluiddRespondInfo(split[2])
        #             #self.G_PhrozenFluiddRespondInfo(split[3])
        #             #line_strip=line.strip()
        #             #self.G_PhrozenFluiddRespondInfo(line)
        #             #self.G_PhrozenFluiddRespondInfo("line.count=%d" % line.count)
        #             split=line.split(',')
        #             #self.G_PhrozenFluiddRespondInfo(type(split))
        #             #self.G_PhrozenFluiddRespondInfo("".join(split))
        #             #self.G_PhrozenFluiddRespondInfo(split[0])
        #             split[0]=split[0].strip()#驱动号
        #             split[1]=split[1].strip()#硬件id
        #             split[2]=split[2].strip()#固件版本
        #             split[3]=split[3].strip()#镜像id
        #             split[4]=split[4].strip()#是否在线
        #             #split[4]='0'#是否在线，默认给0
        #             if "SN1" in SerialRxASCIIStr:
        #                 if split[0] == "1":
        #                     self.G_PhrozenFluiddRespondInfo(split[0])
        #                     self.G_PhrozenFluiddRespondInfo(split[1])
        #                     self.G_PhrozenFluiddRespondInfo(split[2])
        #                     self.G_PhrozenFluiddRespondInfo(split[3])
        #                     self.G_PhrozenFluiddRespondInfo(split[4])
        #                     #line=("%d,%d,%d," % (HW_VERSION,,))
        #                     line_modify=split[0]+','+'1'+','+SerialRxASCIIStr[9:14]+','+'1'+','+'1'
        #                     self.G_PhrozenFluiddRespondInfo(line_modify)
        #                     Lo_AllLine=Lo_AllLine+line_modify+"\r\n"#0x0D 0x0A
        #                 else:
        #                     Lo_AllLine=Lo_AllLine+line
        #             if "SN2" in SerialRxASCIIStr:
        #                 if split[0] == "2":
        #                     self.G_PhrozenFluiddRespondInfo(split[0])
        #                     self.G_PhrozenFluiddRespondInfo(split[1])
        #                     self.G_PhrozenFluiddRespondInfo(split[2])
        #                     self.G_PhrozenFluiddRespondInfo(split[3])
        #                     self.G_PhrozenFluiddRespondInfo(split[4])
        #                     #line=("%d,%d,%d," % (HW_VERSION,,))
        #                     line_modify=split[0]+','+'1'+','+SerialRxASCIIStr[9:14]+','+'1'+','+'1'
        #                     self.G_PhrozenFluiddRespondInfo(line_modify)
        #                     Lo_AllLine=Lo_AllLine+line_modify+"\r\n"#0x0D 0x0A
        #                 else:
        #                     Lo_AllLine=Lo_AllLine+line
        #             if "SN3" in SerialRxASCIIStr:
        #                 if split[0] == "3":
        #                     self.G_PhrozenFluiddRespondInfo(split[0])
        #                     self.G_PhrozenFluiddRespondInfo(split[1])
        #                     self.G_PhrozenFluiddRespondInfo(split[2])
        #                     self.G_PhrozenFluiddRespondInfo(split[3])
        #                     self.G_PhrozenFluiddRespondInfo(split[4])
        #                     #line=("%d,%d,%d," % (HW_VERSION,,))
        #                     line_modify=split[0]+','+'1'+','+SerialRxASCIIStr[9:14]+','+'1'+','+'1'
        #                     self.G_PhrozenFluiddRespondInfo(line_modify)
        #                     Lo_AllLine=Lo_AllLine+line_modify+"\r\n"#0x0D 0x0A
        #                 else:
        #                     Lo_AllLine=Lo_AllLine+line
        #             if "SN4" in SerialRxASCIIStr:
        #                 if split[0] == "4":
        #                     self.G_PhrozenFluiddRespondInfo(split[0])
        #                     self.G_PhrozenFluiddRespondInfo(split[1])
        #                     self.G_PhrozenFluiddRespondInfo(split[2])
        #                     self.G_PhrozenFluiddRespondInfo(split[3])
        #                     self.G_PhrozenFluiddRespondInfo(split[4])
        #                     #line=("%d,%d,%d," % (HW_VERSION,,))
        #                     line_modify=split[0]+','+'1'+','+SerialRxASCIIStr[9:14]+','+'1'+','+'1'
        #                     self.G_PhrozenFluiddRespondInfo(line_modify)
        #                     Lo_AllLine=Lo_AllLine+line_modify+"\r\n"#0x0D 0x0A
        #                 else:
        #                     Lo_AllLine=Lo_AllLine+line
        #     #self.G_PhrozenFluiddRespondInfo(Lo_AllLine)
        #     with open(filename,"w+") as file_w:
        #         file_w.write(Lo_AllLine)


        # # 16色HUB板固件-7 7
        # if "V-H7-I7-F" in SerialRxASCIIStr:
        #     #lancaigang240530：版本写到dat文件；DriveCodeJson.dat
        #     filename='/home/prz/hdlDat/DriveCodeFile.dat'
        #     self.G_PhrozenFluiddRespondInfo("filename=%s" % filename)
        #     Lo_AllLine=""
        #     #data = [{"DriveCode":16,"DriveImageType":0,"DriveHwVersion":0,"DriveFwVersion":0,"DriveId":0},{"DriveCode":15,"DriveImageType":0,"DriveHwVersion":0,"DriveFwVersion":0,"DriveId":0},{"DriveCode":14,"DriveImageType":0,"DriveHwVersion":0,"DriveFwVersion":0,"DriveId":0},{"DriveCode":13,"DriveImageType":0,"DriveHwVersion":0,"DriveFwVersion":0,"DriveId":0},{"DriveCode":12,"DriveImageType":0,"DriveHwVersion":0,"DriveFwVersion":0,"DriveId":0},{"DriveCode":11,"DriveImageType":0,"DriveHwVersion":0,"DriveFwVersion":0,"DriveId":0},{"DriveCode":10,"DriveImageType":10,"DriveHwVersion":10,"DriveFwVersion":24045,"DriveId":0},{"DriveCode":9,"DriveImageType":0,"DriveHwVersion":0,"DriveFwVersion":0,"DriveId":0},{"DriveCode":8,"DriveImageType":0,"DriveHwVersion":0,"DriveFwVersion":0,"DriveId":0},{"DriveCode":7,"DriveImageType":0,"DriveHwVersion":0,"DriveFwVersion":0,"DriveId":0},{"DriveCode":6,"DriveImageType":0,"DriveHwVersion":0,"DriveFwVersion":0,"DriveId":0},{"DriveCode":5,"DriveImageType":5,"DriveHwVersion":5,"DriveFwVersion":24046,"DriveId":0},{"DriveCode":4,"DriveImageType":0,"DriveHwVersion":0,"DriveFwVersion":0,"DriveId":0},{"DriveCode":3,"DriveImageType":0,"DriveHwVersion":0,"DriveFwVersion":0,"DriveId":0},{"DriveCode":2,"DriveImageType":0,"DriveHwVersion":0,"DriveFwVersion":0,"DriveId":0},{"DriveCode":1,"DriveImageType":1,"DriveHwVersion":1,"DriveFwVersion":24042,"DriveId":0}]
        #     #f = open(filename, 'a')
        #     #json.dump(data, f)  #对象序列号为字节流
        #     #f.close()
        #     with open(filename,'r') as file:
        #         #for line in file:
        #         # # realine() 读取整行内容，包括 "\n" 字符
        #         # self.G_PhrozenFluiddRespondInfo(file.readline().strip())
        #         # #time.sleep(1)
        #         Lo_FileDataList=file.readlines()
        #         for line in Lo_FileDataList:
        #             #split = [i[:-1].split(',') for i in file.readlines()]
        #             #self.G_PhrozenFluiddRespondInfo(type(split))
        #             #self.G_PhrozenFluiddRespondInfo(split[1])
        #             #self.G_PhrozenFluiddRespondInfo(split[2])
        #             #self.G_PhrozenFluiddRespondInfo(split[3])
        #             #line_strip=line.strip()
        #             #self.G_PhrozenFluiddRespondInfo(line)
        #             #self.G_PhrozenFluiddRespondInfo("line.count=%d" % line.count)
        #             split=line.split(',')
        #             #self.G_PhrozenFluiddRespondInfo(type(split))
        #             #self.G_PhrozenFluiddRespondInfo("".join(split))
        #             #self.G_PhrozenFluiddRespondInfo(split[0])
        #             split[0]=split[0].strip()#驱动号
        #             split[1]=split[1].strip()#硬件id
        #             split[2]=split[2].strip()#固件版本
        #             split[3]=split[3].strip()#镜像id
        #             split[4]=split[4].strip()#是否在线
        #             if split[0]== "7":
        #                 self.G_PhrozenFluiddRespondInfo(split[0])
        #                 self.G_PhrozenFluiddRespondInfo(split[1])
        #                 self.G_PhrozenFluiddRespondInfo(split[2])
        #                 self.G_PhrozenFluiddRespondInfo(split[3])
        #                 self.G_PhrozenFluiddRespondInfo(split[4])
        #                 #line=("%d,%d,%d," % (HW_VERSION,,))
        #                 line_modify=split[0]+','+'7'+','+SerialRxASCIIStr[9:14]+','+'7'+','+'1'
        #                 self.G_PhrozenFluiddRespondInfo(line_modify)
        #                 Lo_AllLine=Lo_AllLine+line_modify+"\r\n"#0x0D 0x0A
        #             else:
        #                 Lo_AllLine=Lo_AllLine+line
        #     #self.G_PhrozenFluiddRespondInfo(Lo_AllLine)
        #     with open(filename,"w+") as file_w:
        #         file_w.write(Lo_AllLine)


        #lancaigang240326:
        #self.G_PauseToLCDString=SerialRxASCIIStr
        #// ttyUSB0串口接收: CS00N0M03T04C0
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


        #lancaigang240524：未知模式，不是M1-MC M2-MA M3模式，不执行后面暂停操作
        #lancaigang240521：如果没有进入打印模式，不执行暂停
        if self.G_AMSDeviceWorkMode == AMS_WORK_MODE_UNKNOW:#M1
            self.G_PhrozenFluiddRespondInfo("未知模式，不执行串口数据")
            return
            #lancaigang240524：永远退出回调函数
            #return self.G_PhrozenReactor.NEVER




        #旧AMS
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

        #新AMS
        # // lancaigang231202:+PAUSE:1,oldchannel,newchannel;1-新AMS不用
        # // lancaigang231202:+PAUSE:2,oldchannel,newchannel;2-暂停ACK
        # // lancaigang231204:+PAUSE:3,oldchannel,newchannel;3-
        # // lancaigang231205:+PAUSE:4,oldchannel,newchannel;4-进料超时，暂停(1、进料途中卡线超时60s；2、进料途中)
        # // lancaigang231205:+PAUSE:5,oldchannel,newchannel;5-
        # // lancaigang231205:+PAUSE:6,oldchannel,newchannel;6-入口位到缓冲器超时20s，暂停
        # // lancaigang231205:+PAUSE:7,oldchannel,newchannel;7-缓冲器满状态超时60s，暂停(报错可能原因：进线异常顶满或喷头卡料顶满或热端堵料顶满)
        # // lancaigang231205:+PAUSE:8,oldchannel,newchannel;8-喷头切刀或传感器异常，6s超时；暂停(报错可能原因：旧通道用完料无法退料或料盘料太少无法退料或喷头切刀异常)
        # // lancaigang231205:+PAUSE:9,oldchannel,newchannel;9-
        # // lancaigang231202:+PAUSE:a,oldchannel,newchannel;a-
        # // lancaigang231202:+PAUSE:b,oldchannel,newchannel;b-单色断线检测；检测不到线材3s左右暂停
        # // lancaigang231202:+PAUSE:c,oldchannel,newchannel;c-吐料中喷头堵头；超时20s
        # // lancaigang231202:+PAUSE:d,oldchannel,newchannel;d-吐料中AMS无法送料，线材有咬坑；超时20s
        # // lancaigang231202:+PAUSE:e,oldchannel,newchannel;e-启动打印时，AMS未在烘干状态下，AMS温度超过45度，暂停不允许打印
        # // lancaigang231202:+PAUSE:f,oldchannel,newchannel;f-启动打印时，当前AMS在烘干状态下，AMS温度超过45度，暂停不允许打印，并停止AMS烘干功能
        # // lancaigang231202:+PAUSE:g,oldchannel,newchannel;g-AMS多色USB线异常，打印中超时10s，则报告暂停
        # // lancaigang231202:+PAUSE:h,oldchannel,newchannel;h-
        # // lancaigang231202:+PAUSE:i,oldchannel,newchannel;i-
        # // lancaigang231202:+PAUSE:j,oldchannel,newchannel;j-
        # // lancaigang231202:+PAUSE:10,oldchannel,newchannel;10-触摸屏或fluidd网页主动暂停

        #MSG消息
         # // lancaigang250516:+MSG:1,0/1,oldchannel,newchannel;0-吐料开始 1-吐料结束


        #lancaigang241128：
        #lancaigang250712:如果是取消打印，只过滤AMS暂停命令
        if self.G_CancelFlag==True:
            self.G_PhrozenFluiddRespondInfo("已取消打印，过滤暂停命令")
            return
    



        if "+PAUSE:1" in SerialRxASCIIStr:
            #lancaigang240106：单色续料如果已经暂停，不允许再暂停
            if self.G_AMSDeviceWorkMode == AMS_WORK_MODE_MA:
                if self.G_KlipperIfPaused == True:
                    self.G_PhrozenFluiddRespondInfo("单色续料MA模式，重复暂停了if self.G_KlipperIfPaused == True:")
                    return
            #lancaigang240413：单色模式，如果已经暂停，不允许再暂停
            if self.G_AMSDeviceWorkMode == AMS_WORK_MODE_FILA_RUNOUT:
                if self.G_KlipperIfPaused == True:
                    self.G_PhrozenFluiddRespondInfo("单色M3模式，有AMS多色，重复暂停了:")
                    return
            self.G_PhrozenFluiddRespondInfo("进料用完卡线")
            #lancaigang240103：如果是屏幕主动暂停，不处理stm32的主动上报
            if self.G_ToolheadIfHaveFilaFlag == True:
                    if self.G_IfToolheadHaveFilaInitiativePauseFlag==True:
                        self.G_PhrozenFluiddRespondInfo("屏幕主动暂停，不处理stm32主动上报")
                        return
            #lancaigang240113：如果是手动命令，过滤stm32的暂停上报
            if self.ManualCmdFlag==True:
                #lancaigang240611：手动命令也上报给串口屏
                self.G_PhrozenFluiddRespondInfo(SerialRxASCIIStr)
                #self.ManualCmdFlag=False
                self.G_PhrozenFluiddRespondInfo("手动测试命令，不处理stm32主动暂停上报")
                return
            
            #lancaigang240325:恢复过程中需要检测是否有暂停上报
            self.G_ResumeProcessCheckPauseStatus=True
            self.G_PauseToLCDString=SerialRxASCIIStr
            #if self.G_IfChangeFilaOngoing== False:
            #lancaigang240124：stm32上报暂停只能暂停1次
            if self.STM32ReprotPauseFlag==0:
                self.G_PauseTriggerWhileChangeChannelFlag=True
                if self.PG102Flag==True:
                    #先进行强制进料，防止入口传感器状态异常
                    self.Cmds_AMSSerial1Send("E%d" % self.G_ChangeChannelTimeoutNewChan)
                    self.G_PhrozenFluiddRespondInfo("发送命令: E%d" % self.G_ChangeChannelTimeoutNewChan)

                    self.G_PhrozenFluiddRespondInfo("正在吐料中，暂缓暂停，待吐料完成再暂停")
                    self.PG102DelayPauseFlag=True
                    self.G_PauseToLCDString="+PAUSE:1,%d,%d" % (self.G_ChangeChannelTimeoutOldChan,self.G_ChangeChannelTimeoutNewChan)
                else:
                    #特殊补料状态
                    #self.Cmds_AMSSerial1Send("H%d" % self.G_ChangeChannelTimeoutNewChan)
                    #self.G_PhrozenFluiddRespondInfo("[(cmds.python)]发送命令: H%d" % self.G_ChangeChannelTimeoutNewChan)

                    #lancaigang231207：换料过程中，如果进料用完卡料，需要从喷头上料管取出，不能回退线材
                    self.G_IfInFilaBlockFlag=True
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

                    self.STM32ReprotPauseFlag=1
                    #lancaigang231202：P1 C?自动换料时，如果第1次通道就进料异常暂停，如果要恢复，也继续从第1次通道开始
                    self.G_ChangeChannelFirstFilaFlag=True
                    #self.Cmds_PhrozenKlipperPauseNoneCmdToSTM32(None)

                    #self.Cmds_PhrozenKlipperPauseNoneCmdToSTM32(None)
                    if "+PAUSE:1,1" in SerialRxASCIIStr:
                        self.G_PhrozenFluiddRespondInfo("1")
                        self.G_PhrozenFluiddRespondInfo("+PAUSE:1,1")
                        self.G_PauseToLCDString="+PAUSE:1,1"
                        self.G_Pause1Channel=1
                    elif "+PAUSE:1,2" in SerialRxASCIIStr:
                        self.G_PhrozenFluiddRespondInfo("2")
                        self.G_PhrozenFluiddRespondInfo("+PAUSE:1,2")
                        self.G_PauseToLCDString="+PAUSE:1,2"
                        self.G_Pause1Channel=2
                    elif "+PAUSE:1,3" in SerialRxASCIIStr:
                        self.G_PhrozenFluiddRespondInfo("3")
                        self.G_PhrozenFluiddRespondInfo("+PAUSE:1,3")
                        self.G_PauseToLCDString="+PAUSE:1,3"
                        self.G_Pause1Channel=3
                    elif "+PAUSE:1,4" in SerialRxASCIIStr:
                        self.G_PhrozenFluiddRespondInfo("4")
                        self.G_PhrozenFluiddRespondInfo("+PAUSE:1,4")
                        self.G_PauseToLCDString="+PAUSE:1,3"
                        self.G_Pause1Channel=4
                    elif "+PAUSE:1,5" in SerialRxASCIIStr:
                        self.G_PhrozenFluiddRespondInfo("5")
                        self.G_PhrozenFluiddRespondInfo("+PAUSE:1,5")
                        self.G_PauseToLCDString="+PAUSE:1,5"
                        self.G_Pause1Channel=5
                    elif "+PAUSE:1,6" in SerialRxASCIIStr:
                        self.G_PhrozenFluiddRespondInfo("6")
                        self.G_PhrozenFluiddRespondInfo("+PAUSE:1,6")
                        self.G_PauseToLCDString="+PAUSE:1,6"
                        self.G_Pause1Channel=6
                    elif "+PAUSE:1,7" in SerialRxASCIIStr:
                        self.G_PhrozenFluiddRespondInfo("7")
                        self.G_PhrozenFluiddRespondInfo("+PAUSE:1,7")
                        self.G_PauseToLCDString="+PAUSE:1,7"
                        self.G_Pause1Channel=7
                    elif "+PAUSE:1,8" in SerialRxASCIIStr:
                        self.G_PhrozenFluiddRespondInfo("8")
                        self.G_PhrozenFluiddRespondInfo("+PAUSE:1,8")
                        self.G_PauseToLCDString="+PAUSE:1,8"
                        self.G_Pause1Channel=8
                    elif "+PAUSE:1,9" in SerialRxASCIIStr:
                        self.G_PhrozenFluiddRespondInfo("9")
                        self.G_PhrozenFluiddRespondInfo("+PAUSE:1,9")
                        self.G_PauseToLCDString="+PAUSE:1,9"
                        self.G_Pause1Channel=9
                    elif "+PAUSE:1,10" in SerialRxASCIIStr:
                        self.G_PhrozenFluiddRespondInfo("10")
                        self.G_PhrozenFluiddRespondInfo("+PAUSE:1,10")
                        self.G_PauseToLCDString="+PAUSE:1,10"
                        self.G_Pause1Channel=10
                    elif "+PAUSE:1,11" in SerialRxASCIIStr:
                        self.G_PhrozenFluiddRespondInfo("11")
                        self.G_PhrozenFluiddRespondInfo("+PAUSE:1,11")
                        self.G_PauseToLCDString="+PAUSE:1,11"
                        self.G_Pause1Channel=11
                    elif "+PAUSE:1,12" in SerialRxASCIIStr:
                        self.G_PhrozenFluiddRespondInfo("12")
                        self.G_PhrozenFluiddRespondInfo("+PAUSE:1,12")
                        self.G_PauseToLCDString="+PAUSE:1,12"
                        self.G_Pause1Channel=12
                    elif "+PAUSE:1,13" in SerialRxASCIIStr:
                        self.G_PhrozenFluiddRespondInfo("13")
                        self.G_PhrozenFluiddRespondInfo("+PAUSE:1,13")
                        self.G_PauseToLCDString="+PAUSE:1,13"
                        self.G_Pause1Channel=13
                    elif "+PAUSE:1,14" in SerialRxASCIIStr:
                        self.G_PhrozenFluiddRespondInfo("14")
                        self.G_PhrozenFluiddRespondInfo("+PAUSE:1,14")
                        self.G_PauseToLCDString="+PAUSE:1,14"
                        self.G_Pause1Channel=14
                    elif "+PAUSE:1,15" in SerialRxASCIIStr:
                        self.G_PhrozenFluiddRespondInfo("15")
                        self.G_PhrozenFluiddRespondInfo("+PAUSE:1,15")
                        self.G_PauseToLCDString="+PAUSE:1,15"
                        self.G_Pause1Channel=15
                    elif "+PAUSE:1,16" in SerialRxASCIIStr:
                        self.G_PhrozenFluiddRespondInfo("16")
                        self.G_PhrozenFluiddRespondInfo("+PAUSE:1,16")
                        self.G_PauseToLCDString="+PAUSE:1,16"
                        self.G_Pause1Channel=16
                    else:
                        self.G_PhrozenFluiddRespondInfo("self.G_ChangeChannelTimeoutNewChan=%d" % self.G_ChangeChannelTimeoutNewChan)
                        self.G_PhrozenFluiddRespondInfo("+PAUSE:1,%d,%d" % (self.G_ChangeChannelTimeoutOldChan,self.G_ChangeChannelTimeoutNewChan))
                        self.G_PauseToLCDString="+PAUSE:1,%d,%d" % (self.G_ChangeChannelTimeoutOldChan,self.G_ChangeChannelTimeoutNewChan)

            else:
                self.G_PauseTriggerWhileChangeChannelFlag=True
                self.G_PhrozenFluiddRespondInfo("stm32主动暂停上报，重复暂停了")
                #lancaigang240325：重复暂停了，也要上报给串口屏
                #self.G_PhrozenFluiddRespondInfo(self.G_PauseToLCDString)
                self.G_PauseToLCDString=SerialRxASCIIStr
                self.G_PhrozenFluiddRespondInfo("+PAUSE:1,%d,%d" % (self.G_ChangeChannelTimeoutOldChan,self.G_ChangeChannelTimeoutNewChan))

            return


        if "+PAUSE:2" in SerialRxASCIIStr:
            self.G_PhrozenFluiddRespondInfo("暂停ACK")
            #self.G_PhrozenFluiddRespondInfo("+PAUSE:2,%d" % self.G_ChangeChannelTimeoutNewChan)

            return
        

        if "+PAUSE:3" in SerialRxASCIIStr:
            #lancaigang240106：单色续料如果已经暂停，不允许再暂停
            if self.G_AMSDeviceWorkMode == AMS_WORK_MODE_MA:
                if self.G_KlipperIfPaused == True:
                    self.G_PhrozenFluiddRespondInfo("单色续料MA模式，重复暂停了if self.G_KlipperIfPaused == True:")
                    return
            #lancaigang240413：单色模式，如果已经暂停，不允许再暂停
            if self.G_AMSDeviceWorkMode == AMS_WORK_MODE_FILA_RUNOUT:
                if self.G_KlipperIfPaused == True:
                    self.G_PhrozenFluiddRespondInfo("单色M3模式，有AMS多色，重复暂停了:")
                    return

            self.G_PhrozenFluiddRespondInfo("新通道打印过程中慢速补料超时10s，暂停")

            #lancaigang240103：如果是屏幕主动暂停，不处理stm32的主动上报
            if self.G_ToolheadIfHaveFilaFlag == True:
                    if self.G_IfToolheadHaveFilaInitiativePauseFlag==True:
                        self.G_PhrozenFluiddRespondInfo("屏幕主动暂停，不处理stm32主动上报")
                        return
            #lancaigang240113：如果是手动命令，过滤stm32的暂停上报
            if self.ManualCmdFlag==True or self.G_CutCheckTest==True:
                #lancaigang240611：手动命令也上报给串口屏
                self.G_PhrozenFluiddRespondInfo(SerialRxASCIIStr)
                #self.ManualCmdFlag=False
                self.G_PhrozenFluiddRespondInfo("手动测试命令，不处理stm32主动暂停上报")
                return
            

            
            # #if self.G_IfChangeFilaOngoing== False:
            # #lancaigang240124：stm32上报暂停只能暂停1次
            # if self.STM32ReprotPauseFlag==0:
            #     self.G_PhrozenFluiddRespondInfo("stm32主动暂停上报，暂停1次")
            #     self.STM32ReprotPauseFlag=1
            #     self.G_KlipperIfPaused = True
            #     self.G_ChangeChannelFirstFilaFlag=True
            #     #self.Cmds_PhrozenKlipperPauseNoneCmdToSTM32(None)
            #     self.G_PhrozenFluiddRespondInfo("+PAUSE:3,%d" % self.G_ChangeChannelTimeoutNewChan)
            #     #lancaigang231209：定时器中处理业务，会导致业务异常，后面要用线程处理中断业务
            #     self.Cmds_PhrozenKlipperPauseNoneCmdToSTM32(None)
            # else:
            #     self.G_PhrozenFluiddRespondInfo("stm32主动暂停上报，重复暂停了")
            #lancaigang240325:恢复过程中需要检测是否有暂停上报
            self.G_ResumeProcessCheckPauseStatus=True
            self.G_PauseToLCDString=SerialRxASCIIStr
            #lancaigang240124：stm32上报暂停只能暂停1次
            if self.STM32ReprotPauseFlag==0:
                self.G_PauseTriggerWhileChangeChannelFlag=True
                if self.PG102Flag==True:
                    #先进行强制进料，防止入口传感器状态异常
                    #lancaigang240323：容易导致堵料，暂屏蔽
                    #self.Cmds_AMSSerial1Send("E%d" % self.G_ChangeChannelTimeoutNewChan)
                    #self.G_PhrozenFluiddRespondInfo("[(cmds.python)]发送命令: E%d" % self.G_ChangeChannelTimeoutNewChan)

                    self.G_PhrozenFluiddRespondInfo("正在吐料中，暂缓暂停，待吐料完成再暂停")
                    self.PG102DelayPauseFlag=True
                    self.G_PauseToLCDString="+PAUSE:3,%d,%d" % (self.G_ChangeChannelTimeoutOldChan,self.G_ChangeChannelTimeoutNewChan)

                else:
                    #lancaigang250702：
                    if self.G_KlipperInPausing == False:
                        self.G_PhrozenFluiddRespondInfo("不在暂停中，允许新的暂停")
                        #特殊补料状态
                        #self.Cmds_AMSSerial1Send("H%d" % self.G_ChangeChannelTimeoutNewChan)
                        #self.G_PhrozenFluiddRespondInfo("[(cmds.python)]发送命令: H%d" % self.G_ChangeChannelTimeoutNewChan)

                        

                        #lancaigang231209：定时器中处理业务，会导致业务异常，后面要用线程处理中断业务
                        self.G_PhrozenFluiddRespondInfo("stm32主动暂停上报，暂停1次")
                        self.G_PhrozenFluiddRespondInfo("启用快速暂停")
                        self.G_KlipperQuickPause = True
                        self.Cmds_PhrozenKlipperPauseNoneCmdToSTM32(None)
                        self.G_KlipperIfPaused = True
                        #self.Cmds_PhrozenKlipperPauseNoneCmdToSTM32(None)

                        self.STM32ReprotPauseFlag=1
                        #lancaigang231202：P1 C?自动换料时，如果第1次通道就进料异常暂停，如果要恢复，也继续从第1次通道开始
                        self.G_ChangeChannelFirstFilaFlag=True
                        #self.Cmds_PhrozenKlipperPauseNoneCmdToSTM32(None)

                        self.G_PhrozenFluiddRespondInfo("+PAUSE:3,%d,%d" % (self.G_ChangeChannelTimeoutOldChan,self.G_ChangeChannelTimeoutNewChan))
                        self.G_PauseToLCDString="+PAUSE:3,%d,%d" % (self.G_ChangeChannelTimeoutOldChan,self.G_ChangeChannelTimeoutNewChan)

                    else:
                        self.G_PhrozenFluiddRespondInfo("暂停中，不允许新的暂停")

            else:
                self.G_PauseTriggerWhileChangeChannelFlag=True
                self.G_PhrozenFluiddRespondInfo("stm32主动暂停上报，重复暂停了")
                #lancaigang240325：重复暂停了，也要上报给串口屏
                #self.G_PhrozenFluiddRespondInfo("+PAUSE:3,%d" % self.G_ChangeChannelTimeoutNewChan)
                #self.G_PhrozenFluiddRespondInfo(self.G_PauseToLCDString)
                self.G_PhrozenFluiddRespondInfo("+PAUSE:3,%d,%d" % (self.G_ChangeChannelTimeoutOldChan,self.G_ChangeChannelTimeoutNewChan))
                self.G_PauseToLCDString="+PAUSE:3,%d,%d" % (self.G_ChangeChannelTimeoutOldChan,self.G_ChangeChannelTimeoutNewChan)




            return
        

        if "+PAUSE:5" in SerialRxASCIIStr:
            #lancaigang240106：单色续料如果已经暂停，不允许再暂停
            if self.G_AMSDeviceWorkMode == AMS_WORK_MODE_MA:
                if self.G_KlipperIfPaused == True:
                    self.G_PhrozenFluiddRespondInfo("单色续料MA模式了；重复暂停了if self.G_KlipperIfPaused == True:")
                    return
            #lancaigang240413：单色模式，如果已经暂停，不允许再暂停
            if self.G_AMSDeviceWorkMode == AMS_WORK_MODE_FILA_RUNOUT:
                if self.G_KlipperIfPaused == True:
                    self.G_PhrozenFluiddRespondInfo("单色M3模式，有AMS多色，重复暂停了:")
                    return
            self.G_PhrozenFluiddRespondInfo("新通道打印过程中快速补料超时10s，暂停")
            
            #lancaigang240103：如果是屏幕主动暂停，不处理stm32的主动上报
            if self.G_ToolheadIfHaveFilaFlag == True:
                    if self.G_IfToolheadHaveFilaInitiativePauseFlag==True:
                        self.G_PhrozenFluiddRespondInfo("屏幕主动暂停，不处理stm32主动上报")
                        return
            #lancaigang240113：如果是手动命令，过滤stm32的暂停上报
            if self.ManualCmdFlag==True or self.G_CutCheckTest==True:
                #lancaigang240611：手动命令也上报给串口屏
                self.G_PhrozenFluiddRespondInfo(SerialRxASCIIStr)
                #self.ManualCmdFlag=False
                self.G_PhrozenFluiddRespondInfo("手动测试命令，不处理stm32主动暂停上报")
                return
            
            # #if self.G_IfChangeFilaOngoing== False:
            # #lancaigang240124：stm32上报暂停只能暂停1次
            # if self.STM32ReprotPauseFlag==0:
            #     self.G_PhrozenFluiddRespondInfo("stm32主动暂停上报，暂停1次")
            #     self.STM32ReprotPauseFlag=1
            #     self.G_KlipperIfPaused = True
            #     self.G_ChangeChannelFirstFilaFlag=True
            #     #self.Cmds_PhrozenKlipperPauseNoneCmdToSTM32(None)
            #     self.G_PhrozenFluiddRespondInfo("+PAUSE:5,%d" % self.G_ChangeChannelTimeoutNewChan)
            #     #lancaigang231209：定时器中处理业务，会导致业务异常，后面要用线程处理中断业务
            #     self.Cmds_PhrozenKlipperPauseNoneCmdToSTM32(None)
            # else:
            #     self.G_PhrozenFluiddRespondInfo("stm32主动暂停上报，重复暂停了")
            #lancaigang240325:恢复过程中需要检测是否有暂停上报
            self.G_ResumeProcessCheckPauseStatus=True
            self.G_PauseToLCDString=SerialRxASCIIStr
            #lancaigang240124：stm32上报暂停只能暂停1次
            if self.STM32ReprotPauseFlag==0:
                self.G_PauseTriggerWhileChangeChannelFlag=True
                if self.PG102Flag==True:
                    #先进行强制进料，防止入口传感器状态异常
                    #lancaigang240323：容易导致堵料，暂屏蔽
                    #self.Cmds_AMSSerial1Send("E%d" % self.G_ChangeChannelTimeoutNewChan)
                    #self.G_PhrozenFluiddRespondInfo("[(cmds.python)]发送命令: E%d" % self.G_ChangeChannelTimeoutNewChan)

                    self.G_PhrozenFluiddRespondInfo("正在吐料中，暂缓暂停，待吐料完成再暂停")
                    self.PG102DelayPauseFlag=True
                    self.G_PauseToLCDString="+PAUSE:5,%d,%d" % (self.G_ChangeChannelTimeoutOldChan,self.G_ChangeChannelTimeoutNewChan)

                else:
                    #lancaigang250702：
                    if self.G_KlipperInPausing == False:
                        self.G_PhrozenFluiddRespondInfo("不在暂停中，允许新的暂停")
                        #特殊补料状态
                        #self.Cmds_AMSSerial1Send("H%d" % self.G_ChangeChannelTimeoutNewChan)
                        #self.G_PhrozenFluiddRespondInfo("[(cmds.python)]发送命令: H%d" % self.G_ChangeChannelTimeoutNewChan)

                        #lancaigang231209：定时器中处理业务，会导致业务异常，后面要用线程处理中断业务
                        self.G_PhrozenFluiddRespondInfo("stm32主动暂停上报，暂停1次")
                        self.G_PhrozenFluiddRespondInfo("启用快速暂停")
                        self.G_KlipperQuickPause = True
                        self.Cmds_PhrozenKlipperPauseNoneCmdToSTM32(None)
                        self.G_KlipperIfPaused = True
                        #self.Cmds_PhrozenKlipperPauseNoneCmdToSTM32(None)

                        self.STM32ReprotPauseFlag=1
                        #lancaigang231202：P1 C?自动换料时，如果第1次通道就进料异常暂停，如果要恢复，也继续从第1次通道开始
                        self.G_ChangeChannelFirstFilaFlag=True
                        #self.Cmds_PhrozenKlipperPauseNoneCmdToSTM32(None)

                        self.G_PhrozenFluiddRespondInfo("+PAUSE:5,%d,%d" % (self.G_ChangeChannelTimeoutOldChan,self.G_ChangeChannelTimeoutNewChan))
                        self.G_PauseToLCDString="+PAUSE:5,%d,%d" % (self.G_ChangeChannelTimeoutOldChan,self.G_ChangeChannelTimeoutNewChan)
            
                    else:
                        self.G_PhrozenFluiddRespondInfo("暂停中，不允许新的暂停")
    
            else:
                self.G_PauseTriggerWhileChangeChannelFlag=True
                self.G_PhrozenFluiddRespondInfo("stm32主动暂停上报，重复暂停了")
                #lancaigang240325：重复暂停了，也要上报给串口屏
                #self.G_PhrozenFluiddRespondInfo("+PAUSE:5,%d" % self.G_ChangeChannelTimeoutNewChan)
                #self.G_PhrozenFluiddRespondInfo(self.G_PauseToLCDString)
                self.G_PhrozenFluiddRespondInfo("+PAUSE:5,%d,%d" % (self.G_ChangeChannelTimeoutOldChan,self.G_ChangeChannelTimeoutNewChan))
                self.G_PauseToLCDString="+PAUSE:5,%d,%d" % (self.G_ChangeChannelTimeoutOldChan,self.G_ChangeChannelTimeoutNewChan)

            return
        

        if "+PAUSE:4" in SerialRxASCIIStr:
            #lancaigang240106：单色续料如果已经暂停，不允许再暂停
            if self.G_AMSDeviceWorkMode == AMS_WORK_MODE_MA:
                if self.G_KlipperIfPaused == True:
                    self.G_PhrozenFluiddRespondInfo("单色续料MA模式；重复暂停了if self.G_KlipperIfPaused == True:")
                    return
            #lancaigang240413：单色模式，如果已经暂停，不允许再暂停
            if self.G_AMSDeviceWorkMode == AMS_WORK_MODE_FILA_RUNOUT:
                if self.G_KlipperIfPaused == True:
                    self.G_PhrozenFluiddRespondInfo("单色M3模式，有AMS多色，重复暂停了:")
                    return
            self.G_PhrozenFluiddRespondInfo("新通道进料超时50s，暂停")
            
            #lancaigang240103：如果是屏幕主动暂停，不处理stm32的主动上报
            if self.G_ToolheadIfHaveFilaFlag == True:
                    if self.G_IfToolheadHaveFilaInitiativePauseFlag==True:
                        self.G_PhrozenFluiddRespondInfo("屏幕主动暂停，不处理stm32主动上报")
                        return
            #lancaigang240113：如果是手动命令，过滤stm32的暂停上报
            if self.ManualCmdFlag==True or self.G_CutCheckTest==True:
                #lancaigang240611：手动命令也上报给串口屏
                self.G_PhrozenFluiddRespondInfo(SerialRxASCIIStr)
                #self.ManualCmdFlag=False
                self.G_PhrozenFluiddRespondInfo("手动测试命令，不处理stm32主动暂停上报")
                return
            
            # #if self.G_IfChangeFilaOngoing== False:
            # #lancaigang240124：stm32上报暂停只能暂停1次
            # if self.STM32ReprotPauseFlag==0:
            #     self.G_PhrozenFluiddRespondInfo("stm32主动暂停上报，暂停1次")
            #     self.STM32ReprotPauseFlag=1
            #     self.G_KlipperIfPaused = True
            #     self.G_ChangeChannelFirstFilaFlag=True
            #     #self.Cmds_PhrozenKlipperPauseNoneCmdToSTM32(None)
            #     self.G_PhrozenFluiddRespondInfo("+PAUSE:4,%d" % self.G_ChangeChannelTimeoutNewChan)
            #     #lancaigang231209：定时器中处理业务，会导致业务异常，后面要用线程处理中断业务
            #     self.Cmds_PhrozenKlipperPauseNoneCmdToSTM32(None)
            # else:
            #     self.G_PhrozenFluiddRespondInfo("stm32主动暂停上报，重复暂停了")
            #lancaigang240325:恢复过程中需要检测是否有暂停上报
            self.G_ResumeProcessCheckPauseStatus=True
            self.G_PauseToLCDString=SerialRxASCIIStr
            #lancaigang240124：stm32上报暂停只能暂停1次
            if self.STM32ReprotPauseFlag==0:
                self.G_PauseTriggerWhileChangeChannelFlag=True
                if self.PG102Flag==True:
                    #lancaigang240323：容易导致堵料，暂屏蔽
                    #self.Cmds_AMSSerial1Send("E%d" % self.G_ChangeChannelTimeoutNewChan)
                    #self.G_PhrozenFluiddRespondInfo("[(cmds.python)]发送命令: E%d" % self.G_ChangeChannelTimeoutNewChan)

                    self.G_PhrozenFluiddRespondInfo("正在吐料中，暂缓暂停，待吐料完成再暂停")
                    self.PG102DelayPauseFlag=True
                    self.G_PauseToLCDString="+PAUSE:4,%d,%d" % (self.G_ChangeChannelTimeoutOldChan,self.G_ChangeChannelTimeoutNewChan)

                else:
                    #lancaigang250702：
                    if self.G_KlipperInPausing == False:
                        self.G_PhrozenFluiddRespondInfo("不在暂停中，允许新的暂停")
                        #特殊补料状态
                        #self.Cmds_AMSSerial1Send("H%d" % self.G_ChangeChannelTimeoutNewChan)
                        #self.G_PhrozenFluiddRespondInfo("[(cmds.python)]发送命令: H%d" % self.G_ChangeChannelTimeoutNewChan)

                        #self.Cmds_PhrozenKlipperPauseNoneCmdToSTM32(None)

                        #lancaigang231209：定时器中处理业务，会导致业务异常，后面要用线程处理中断业务
                        self.G_PhrozenFluiddRespondInfo("stm32主动暂停上报，暂停1次")
                        self.G_PhrozenFluiddRespondInfo("启用快速暂停")
                        self.G_KlipperQuickPause = True
                        self.Cmds_PhrozenKlipperPauseNoneCmdToSTM32(None)
                        self.G_KlipperIfPaused = True
                        #self.Cmds_PhrozenKlipperPauseNoneCmdToSTM32(None)
                        self.STM32ReprotPauseFlag=1
                        #lancaigang231202：P1 C?自动换料时，如果第1次通道就进料异常暂停，如果要恢复，也继续从第1次通道开始
                        self.G_ChangeChannelFirstFilaFlag=True

                        self.G_PhrozenFluiddRespondInfo("+PAUSE:4,%d,%d" % (self.G_ChangeChannelTimeoutOldChan,self.G_ChangeChannelTimeoutNewChan))
                        self.G_PauseToLCDString="+PAUSE:4,%d,%d" % (self.G_ChangeChannelTimeoutOldChan,self.G_ChangeChannelTimeoutNewChan)
            
                    else:
                        self.G_PhrozenFluiddRespondInfo("暂停中，不允许新的暂停")
    
            else:
                self.G_PauseTriggerWhileChangeChannelFlag=True
                self.G_PhrozenFluiddRespondInfo("stm32主动暂停上报，重复暂停了")
                #lancaigang240325：重复暂停了，也要上报给串口屏
                #self.G_PhrozenFluiddRespondInfo("+PAUSE:4,%d" % self.G_ChangeChannelTimeoutNewChan)
                #self.G_PhrozenFluiddRespondInfo(self.G_PauseToLCDString)
                self.G_PhrozenFluiddRespondInfo("+PAUSE:4,%d,%d" % (self.G_ChangeChannelTimeoutOldChan,self.G_ChangeChannelTimeoutNewChan))
                self.G_PauseToLCDString="+PAUSE:4,%d,%d" % (self.G_ChangeChannelTimeoutOldChan,self.G_ChangeChannelTimeoutNewChan)

            return
        

        if "+PAUSE:6" in SerialRxASCIIStr:
            #lancaigang240106：单色续料如果已经暂停，不允许再暂停
            if self.G_AMSDeviceWorkMode == AMS_WORK_MODE_MA:
                if self.G_KlipperIfPaused == True:
                    self.G_PhrozenFluiddRespondInfo("单色续料MA模式，重复暂停了if self.G_KlipperIfPaused == True:")
                    return
            #lancaigang240413：单色模式，如果已经暂停，不允许再暂停
            if self.G_AMSDeviceWorkMode == AMS_WORK_MODE_FILA_RUNOUT:
                if self.G_KlipperIfPaused == True:
                    self.G_PhrozenFluiddRespondInfo("单色M3模式，有AMS多色，重复暂停了:")
                    return
            self.G_PhrozenFluiddRespondInfo("入口位到停靠位超时10s，暂停")
            
            #lancaigang240103：如果是屏幕主动暂停，不处理stm32的主动上报
            if self.G_ToolheadIfHaveFilaFlag == True:
                    if self.G_IfToolheadHaveFilaInitiativePauseFlag==True:
                        self.G_PhrozenFluiddRespondInfo("屏幕主动暂停，不处理stm32主动上报")
                        return
            #lancaigang240113：如果是手动命令，过滤stm32的暂停上报
            if self.ManualCmdFlag==True or self.G_CutCheckTest==True:
                #lancaigang240611：手动命令也上报给串口屏
                self.G_PhrozenFluiddRespondInfo(SerialRxASCIIStr)
                #self.ManualCmdFlag=False
                self.G_PhrozenFluiddRespondInfo("手动测试命令，不处理stm32主动暂停上报")
                return
            
            # #if self.G_IfChangeFilaOngoing== False:
            # #lancaigang240124：stm32上报暂停只能暂停1次
            # if self.STM32ReprotPauseFlag==0:
            #     self.G_PhrozenFluiddRespondInfo("stm32主动暂停上报，暂停1次")
            #     self.STM32ReprotPauseFlag=1
            #     self.G_KlipperIfPaused = True
            #     self.G_ChangeChannelFirstFilaFlag=True
            #     #self.Cmds_PhrozenKlipperPauseNoneCmdToSTM32(None)
            #     self.G_PhrozenFluiddRespondInfo("+PAUSE:6,%d" % self.G_ChangeChannelTimeoutNewChan)
            #     #lancaigang231209：定时器中处理业务，会导致业务异常，后面要用线程处理中断业务
            #     self.Cmds_PhrozenKlipperPauseNoneCmdToSTM32(None)
            # else:
            #     self.G_PhrozenFluiddRespondInfo("stm32主动暂停上报，重复暂停了")
            #lancaigang240325:恢复过程中需要检测是否有暂停上报
            self.G_ResumeProcessCheckPauseStatus=True
            self.G_PauseToLCDString=SerialRxASCIIStr
            #lancaigang240124：stm32上报暂停只能暂停1次
            if self.STM32ReprotPauseFlag==0:
                self.G_PauseTriggerWhileChangeChannelFlag=True
                if self.PG102Flag==True:
                    #先进行强制进料，防止入口传感器状态异常
                    #lancaigang240323：容易导致堵料，暂屏蔽
                    #self.Cmds_AMSSerial1Send("E%d" % self.G_ChangeChannelTimeoutNewChan)
                    #self.G_PhrozenFluiddRespondInfo("[(cmds.python)]发送命令: E%d" % self.G_ChangeChannelTimeoutNewChan)

                    self.G_PhrozenFluiddRespondInfo("正在吐料中，暂缓暂停，待吐料完成再暂停")
                    self.PG102DelayPauseFlag=True
                    self.G_PauseToLCDString="+PAUSE:6,%d,%d" % (self.G_ChangeChannelTimeoutOldChan,self.G_ChangeChannelTimeoutNewChan)

                else:
                    #lancaigang250702：
                    if self.G_KlipperInPausing == False:
                        self.G_PhrozenFluiddRespondInfo("不在暂停中，允许新的暂停")
                        #特殊补料状态
                        #self.Cmds_AMSSerial1Send("H%d" % self.G_ChangeChannelTimeoutNewChan)
                        #self.G_PhrozenFluiddRespondInfo("[(cmds.python)]发送命令: H%d" % self.G_ChangeChannelTimeoutNewChan)

                        #lancaigang231209：定时器中处理业务，会导致业务异常，后面要用线程处理中断业务
                        self.G_PhrozenFluiddRespondInfo("stm32主动暂停上报，暂停1次")
                        self.G_PhrozenFluiddRespondInfo("启用快速暂停")
                        self.G_KlipperQuickPause = True
                        self.Cmds_PhrozenKlipperPauseNoneCmdToSTM32(None)
                        self.G_KlipperIfPaused = True
                        #self.Cmds_PhrozenKlipperPauseNoneCmdToSTM32(None)
                        
                        self.STM32ReprotPauseFlag=1
                        #lancaigang231202：P1 C?自动换料时，如果第1次通道就进料异常暂停，如果要恢复，也继续从第1次通道开始
                        self.G_ChangeChannelFirstFilaFlag=True
                        #self.Cmds_PhrozenKlipperPauseNoneCmdToSTM32(None)

                        self.G_PhrozenFluiddRespondInfo("+PAUSE:6,%d,%d" % (self.G_ChangeChannelTimeoutOldChan,self.G_ChangeChannelTimeoutNewChan))
                        self.G_PauseToLCDString="+PAUSE:6,%d,%d" % (self.G_ChangeChannelTimeoutOldChan,self.G_ChangeChannelTimeoutNewChan)
            
                    else:
                        self.G_PhrozenFluiddRespondInfo("暂停中，不允许新的暂停")
    
            else:
                self.G_PauseTriggerWhileChangeChannelFlag=True
                self.G_PhrozenFluiddRespondInfo("stm32主动暂停上报，重复暂停了")
                #lancaigang240325：重复暂停了，也要上报给串口屏
                #self.G_PhrozenFluiddRespondInfo("+PAUSE:6,%d" % self.G_ChangeChannelTimeoutNewChan)
                #self.G_PhrozenFluiddRespondInfo(self.G_PauseToLCDString)
                self.G_PhrozenFluiddRespondInfo("+PAUSE:6,%d,%d" % (self.G_ChangeChannelTimeoutOldChan,self.G_ChangeChannelTimeoutNewChan))
                self.G_PauseToLCDString="+PAUSE:6,%d,%d" % (self.G_ChangeChannelTimeoutOldChan,self.G_ChangeChannelTimeoutNewChan)

            return
        

        if "+PAUSE:7" in SerialRxASCIIStr:
            #lancaigang240106：单色续料如果已经暂停，不允许再暂停
            if self.G_AMSDeviceWorkMode == AMS_WORK_MODE_MA:
                if self.G_KlipperIfPaused == True:
                    self.G_PhrozenFluiddRespondInfo("单色续料MA模式，重复暂停了if self.G_KlipperIfPaused == True:")
                    return
            #lancaigang240413：单色模式，如果已经暂停，不允许再暂停
            if self.G_AMSDeviceWorkMode == AMS_WORK_MODE_FILA_RUNOUT:
                if self.G_KlipperIfPaused == True:
                    self.G_PhrozenFluiddRespondInfo("单色M3模式，有AMS多色，重复暂停了:")
                    return
                
            self.G_PhrozenFluiddRespondInfo("缓冲器满状态超时30s，暂停")
            
            #lancaigang231215:
            self.G_STM32PauseCount+=1
            if self.G_STM32PauseCount==5:
                self.G_PhrozenFluiddRespondInfo("if self.G_STM32PauseCount==5;G_STM32PauseCount=%d" % self.G_STM32PauseCount)
                self.G_STM32PauseCount=0
            else:
                self.G_PhrozenFluiddRespondInfo("else;G_STM32PauseCount=%d" % self.G_STM32PauseCount)
        
            #lancaigang240103：如果是屏幕主动暂停，不处理stm32的主动上报
            if self.G_ToolheadIfHaveFilaFlag == True:
                    if self.G_IfToolheadHaveFilaInitiativePauseFlag==True:
                        self.G_PhrozenFluiddRespondInfo("屏幕主动暂停，不处理stm32主动上报")
                        #lancaigang240103：恢复之后，发送命令给stm32恢复上一次状态机状态
                        #恢复状态RS=F,即恢复上一次状态
                        #恢复状态RS=0,即恢复上IDLE_STANDBY状态
                        #恢复状态RS=X,...
                        #恢复状态RS=Y,...
                        #恢复状态RS=Z,...
                        if self.G_AMSDeviceWorkMode == AMS_WORK_MODE_MA:
                            self.Cmds_AMSSerial1Send("AT+MARS=F")
                            self.G_PhrozenFluiddRespondInfo("重复暂停了MA;AT+MARS=F；STM32恢复上次状态")

                        if self.G_AMSDeviceWorkMode == AMS_WORK_MODE_MC:
                            self.Cmds_AMSSerial1Send("AT+MCRS=F")
                            self.G_PhrozenFluiddRespondInfo("重复暂停了MC;AT+MCRS=F；STM32恢复上次状态")

                        
                        
                        # self.G_ProzenToolhead.dwell(1.0)
                        # self.Cmds_AMSSerial1Send("AT+MARS=F")
                        # self.G_PhrozenFluiddRespondInfo("AT+MARS=F")

                        return
            #lancaigang240113：如果是手动命令，过滤stm32的暂停上报
            if self.ManualCmdFlag==True or self.G_CutCheckTest==True:
                #lancaigang240611：手动命令也上报给串口屏
                self.G_PhrozenFluiddRespondInfo(SerialRxASCIIStr)
                #self.ManualCmdFlag=False
                self.G_PhrozenFluiddRespondInfo("手动测试命令，不处理stm32主动暂停上报")
                return
            
            # #if self.G_IfChangeFilaOngoing== False:
            # #lancaigang240124：stm32上报暂停只能暂停1次
            # if self.STM32ReprotPauseFlag==0:
            #     self.G_PhrozenFluiddRespondInfo("stm32主动暂停上报，暂停1次")
            #     self.STM32ReprotPauseFlag=1
            #     self.G_KlipperIfPaused = True
            #     self.G_ChangeChannelFirstFilaFlag=True
            #     #self.Cmds_PhrozenKlipperPauseNoneCmdToSTM32(None)
            #     self.G_PhrozenFluiddRespondInfo("+PAUSE:7,%d" % self.G_ChangeChannelTimeoutNewChan)
            #     #lancaigang231209：定时器中处理业务，会导致业务异常，后面要用线程处理中断业务
            #     self.Cmds_PhrozenKlipperPauseNoneCmdToSTM32(None)
            # else:
            #     self.G_PhrozenFluiddRespondInfo("stm32主动暂停上报，重复暂停了")
            #lancaigang240325:恢复过程中需要检测是否有暂停上报
            self.G_ResumeProcessCheckPauseStatus=True
            self.G_PauseToLCDString=SerialRxASCIIStr
            #lancaigang240124：stm32上报暂停只能暂停1次
            if self.STM32ReprotPauseFlag==0:
                self.G_PauseTriggerWhileChangeChannelFlag=True
                if self.PG102Flag==True:
                    #先进行强制进料，防止入口传感器状态异常
                    #self.Cmds_AMSSerial1Send("E%d" % self.G_ChangeChannelTimeoutNewChan)
                    #self.G_PhrozenFluiddRespondInfo("[(cmds.python)]发送命令: E%d" % self.G_ChangeChannelTimeoutNewChan)

                    self.G_PhrozenFluiddRespondInfo("正在吐料中，暂缓暂停，待吐料完成再暂停")
                    self.PG102DelayPauseFlag=True
                    
                    #lancaigang250725:如果喷头霍尔检测到线材，说明是打印中堵头
                    if self.G_ToolheadIfHaveFilaFlag==True:
                        self.G_PhrozenFluiddRespondInfo("吐料中喷头霍尔检测到线材，堵头")
                        self.G_PauseToLCDString="+PAUSE:c,%d,%d" % (self.G_ChangeChannelTimeoutOldChan,self.G_ChangeChannelTimeoutNewChan)
                    else:
                        self.G_PhrozenFluiddRespondInfo("吐料中缓冲器异常满，喷头霍尔未检测到线材，归类为进料超时")
                        self.G_PauseToLCDString="+PAUSE:4,%d,%d" % (self.G_ChangeChannelTimeoutOldChan,self.G_ChangeChannelTimeoutNewChan)

                else:
                    #特殊补料状态
                    #self.Cmds_AMSSerial1Send("H%d" % self.G_ChangeChannelTimeoutNewChan)
                    #self.G_PhrozenFluiddRespondInfo("[(cmds.python)]发送命令: H%d" % self.G_ChangeChannelTimeoutNewChan)

                    
                    if self.G_KlipperInPausing == False:
                        self.G_PhrozenFluiddRespondInfo("不在暂停中，允许新的暂停")
                        #lancaigang231209：定时器中处理业务，会导致业务异常，后面要用线程处理中断业务
                        self.G_PhrozenFluiddRespondInfo("stm32主动暂停上报，暂停1次")
                        self.G_PhrozenFluiddRespondInfo("启用快速暂停")
                        self.G_KlipperQuickPause = True
                        self.Cmds_PhrozenKlipperPauseNoneCmdToSTM32(None)
                        self.G_KlipperIfPaused = True
                        #self.Cmds_PhrozenKlipperPauseNoneCmdToSTM32(None)

                        self.STM32ReprotPauseFlag=1
                        #lancaigang231202：P1 C?自动换料时，如果第1次通道就进料异常暂停，如果要恢复，也继续从第1次通道开始
                        self.G_ChangeChannelFirstFilaFlag=True
                        #self.Cmds_PhrozenKlipperPauseNoneCmdToSTM32(None)


                        #lancaigang250725:如果喷头霍尔检测到线材，说明是打印中堵头
                        if self.G_ToolheadIfHaveFilaFlag==True:
                            self.G_PhrozenFluiddRespondInfo("打印中喷头霍尔检测到线材，打印中堵头")
                            self.G_PhrozenFluiddRespondInfo("+PAUSE:7,%d,%d" % (self.G_ChangeChannelTimeoutOldChan,self.G_ChangeChannelTimeoutNewChan))
                            self.G_PauseToLCDString="+PAUSE:7,%d,%d" % (self.G_ChangeChannelTimeoutOldChan,self.G_ChangeChannelTimeoutNewChan)
                        else:
                            self.G_PhrozenFluiddRespondInfo("进线中缓冲器异常满，喷头霍尔未检测到线材，归类为进料超时")
                            self.G_PhrozenFluiddRespondInfo("+PAUSE:4,%d,%d" % (self.G_ChangeChannelTimeoutOldChan,self.G_ChangeChannelTimeoutNewChan))
                            self.G_PauseToLCDString="+PAUSE:4,%d,%d" % (self.G_ChangeChannelTimeoutOldChan,self.G_ChangeChannelTimeoutNewChan)
                    else:
                        self.G_PhrozenFluiddRespondInfo("暂停中，不允许新的暂停")
            
            else:
                self.G_PauseTriggerWhileChangeChannelFlag=True
                self.G_PhrozenFluiddRespondInfo("stm32主动暂停上报，重复暂停了")
                #lancaigang240325：重复暂停了，也要上报给串口屏
                #self.G_PhrozenFluiddRespondInfo("+PAUSE:7,%d" % self.G_ChangeChannelTimeoutNewChan)
                #self.G_PhrozenFluiddRespondInfo(self.G_PauseToLCDString)
                self.G_PhrozenFluiddRespondInfo("+PAUSE:7,%d,%d" % (self.G_ChangeChannelTimeoutOldChan,self.G_ChangeChannelTimeoutNewChan))
                self.G_PauseToLCDString="+PAUSE:7,%d,%d" % (self.G_ChangeChannelTimeoutOldChan,self.G_ChangeChannelTimeoutNewChan)

            return



        if "+PAUSE:a" in SerialRxASCIIStr:
            #lancaigang240106：单色续料如果已经暂停，不允许再暂停
            if self.G_AMSDeviceWorkMode == AMS_WORK_MODE_MA:
                if self.G_KlipperIfPaused == True:
                    self.G_PhrozenFluiddRespondInfo("单色续料MA模式；重复暂停了if self.G_KlipperIfPaused == True:")
                    return
            #lancaigang240413：单色模式，如果已经暂停，不允许再暂停
            if self.G_AMSDeviceWorkMode == AMS_WORK_MODE_FILA_RUNOUT:
                if self.G_KlipperIfPaused == True:
                    self.G_PhrozenFluiddRespondInfo("单色M3模式，有AMS多色，重复暂停了:")
                    return
            self.G_PhrozenFluiddRespondInfo("停靠位到缓冲器入口超时10s，暂停")
            

            #lancaigang240103：如果是屏幕主动暂停，不处理stm32的主动上报
            if self.G_ToolheadIfHaveFilaFlag == True:
                    if self.G_IfToolheadHaveFilaInitiativePauseFlag==True:
                        self.G_PhrozenFluiddRespondInfo("屏幕主动暂停，不处理stm32主动上报")
                        return
            #lancaigang240113：如果是手动命令，过滤stm32的暂停上报
            if self.ManualCmdFlag==True or self.G_CutCheckTest==True:
                #lancaigang240611：手动命令也上报给串口屏
                self.G_PhrozenFluiddRespondInfo(SerialRxASCIIStr)
                #self.ManualCmdFlag=False
                self.G_PhrozenFluiddRespondInfo("手动测试命令，不处理stm32主动暂停上报")
                return
            
            # #if self.G_IfChangeFilaOngoing== False:
            # #lancaigang240124：stm32上报暂停只能暂停1次
            # if self.STM32ReprotPauseFlag==0:
            #     self.G_PhrozenFluiddRespondInfo("stm32主动暂停上报，暂停1次")
            #     self.STM32ReprotPauseFlag=1
            #     self.G_KlipperIfPaused = True
            #     self.G_ChangeChannelFirstFilaFlag=True
            #     #self.Cmds_PhrozenKlipperPauseNoneCmdToSTM32(None)
            #     self.G_PhrozenFluiddRespondInfo("+PAUSE:a,%d" % self.G_ChangeChannelTimeoutNewChan)
            #     #lancaigang231209：定时器中处理业务，会导致业务异常，后面要用线程处理中断业务
            #     self.Cmds_PhrozenKlipperPauseNoneCmdToSTM32(None)
            # else:
            #     self.G_PhrozenFluiddRespondInfo("stm32主动暂停上报，重复暂停了")
            #lancaigang240325:恢复过程中需要检测是否有暂停上报
            self.G_ResumeProcessCheckPauseStatus=True
            self.G_PauseToLCDString=SerialRxASCIIStr
            #lancaigang240124：stm32上报暂停只能暂停1次
            if self.STM32ReprotPauseFlag==0:
                self.G_PauseTriggerWhileChangeChannelFlag=True
                if self.PG102Flag==True:
                    #先进行强制进料，防止入口传感器状态异常
                    #lancaigang240323：容易导致堵料，暂屏蔽
                    #self.Cmds_AMSSerial1Send("E%d" % self.G_ChangeChannelTimeoutNewChan)
                    #self.G_PhrozenFluiddRespondInfo("[(cmds.python)]发送命令: E%d" % self.G_ChangeChannelTimeoutNewChan)

                    self.G_PhrozenFluiddRespondInfo("正在吐料中，暂缓暂停，待吐料完成再暂停")
                    self.PG102DelayPauseFlag=True
                    self.G_PauseToLCDString="+PAUSE:a,%d,%d" % (self.G_ChangeChannelTimeoutOldChan,self.G_ChangeChannelTimeoutNewChan)

                else:
                    #lancaigang250702：
                    if self.G_KlipperInPausing == False:
                        self.G_PhrozenFluiddRespondInfo("不在暂停中，允许新的暂停")
                        #特殊补料状态
                        #self.Cmds_AMSSerial1Send("H%d" % self.G_ChangeChannelTimeoutNewChan)
                        #self.G_PhrozenFluiddRespondInfo("[(cmds.python)]发送命令: H%d" % self.G_ChangeChannelTimeoutNewChan)

                        #lancaigang231209：定时器中处理业务，会导致业务异常，后面要用线程处理中断业务
                        self.G_PhrozenFluiddRespondInfo("stm32主动暂停上报，暂停1次")
                        self.G_PhrozenFluiddRespondInfo("启用快速暂停")
                        self.G_KlipperQuickPause = True
                        self.Cmds_PhrozenKlipperPauseNoneCmdToSTM32(None)
                        self.G_KlipperIfPaused = True
                        #self.Cmds_PhrozenKlipperPauseNoneCmdToSTM32(None)

                        self.STM32ReprotPauseFlag=1
                        #lancaigang231202：P1 C?自动换料时，如果第1次通道就进料异常暂停，如果要恢复，也继续从第1次通道开始
                        self.G_ChangeChannelFirstFilaFlag=True
                        #self.Cmds_PhrozenKlipperPauseNoneCmdToSTM32(None)a

                        self.G_PhrozenFluiddRespondInfo("+PAUSE:a,%d,%d" % (self.G_ChangeChannelTimeoutOldChan,self.G_ChangeChannelTimeoutNewChan))
                        self.G_PauseToLCDString="+PAUSE:a,%d,%d" % (self.G_ChangeChannelTimeoutOldChan,self.G_ChangeChannelTimeoutNewChan)
                
                    else:
                        self.G_PhrozenFluiddRespondInfo("暂停中，不允许新的暂停")

            else:
                self.G_PauseTriggerWhileChangeChannelFlag=True
                self.G_PhrozenFluiddRespondInfo("stm32主动暂停上报，重复暂停了")
                #lancaigang240325：重复暂停了，也要上报给串口屏
                #self.G_PhrozenFluiddRespondInfo("+PAUSE:a,%d" % self.G_ChangeChannelTimeoutNewChan)
                #self.G_PhrozenFluiddRespondInfo(self.G_PauseToLCDString)
                self.G_PhrozenFluiddRespondInfo("+PAUSE:a,%d,%d" % (self.G_ChangeChannelTimeoutOldChan,self.G_ChangeChannelTimeoutNewChan))
                self.G_PauseToLCDString="+PAUSE:a,%d,%d" % (self.G_ChangeChannelTimeoutOldChan,self.G_ChangeChannelTimeoutNewChan)

            return

        #lancaigang250423:打印中喷头堵头检测
        if "+PAUSE:c" in SerialRxASCIIStr:
            #lancaigang240106：单色续料如果已经暂停，不允许再暂停
            if self.G_AMSDeviceWorkMode == AMS_WORK_MODE_MA:
                if self.G_KlipperIfPaused == True:
                    self.G_PhrozenFluiddRespondInfo("单色续料MA模式；重复暂停了if self.G_KlipperIfPaused == True:")
                    
                    #lancaigang251124：
                    self.G_PhrozenFluiddRespondInfo("单色续料MA模式；喷头检测到线材，但吐料期间stm32暂停报错，不能直接return；")
                    self.STM32ReprotPauseFlag=1
                    #lancaigang231202：P1 C?自动换料时，如果第1次通道就进料异常暂停，如果要恢复，也继续从第1次通道开始
                    #self.G_ChangeChannelFirstFilaFlag=True
                    #self.Cmds_PhrozenKlipperPauseNoneCmdToSTM32(None)
                    #self.G_PhrozenFluiddRespondInfo("+PAUSE:c,%d,%d" % (self.G_ChangeChannelTimeoutOldChan,self.G_ChangeChannelTimeoutNewChan))
                    self.G_PauseToLCDString="+PAUSE:c,%d,%d" % (self.G_ChangeChannelTimeoutOldChan,self.G_ChangeChannelTimeoutNewChan)
        
                    return
            #lancaigang240413：单色模式，如果已经暂停，不允许再暂停
            if self.G_AMSDeviceWorkMode == AMS_WORK_MODE_FILA_RUNOUT:
                if self.G_KlipperIfPaused == True:
                    self.G_PhrozenFluiddRespondInfo("单色M3模式，有AMS多色，重复暂停了:")
                    return
            self.G_PhrozenFluiddRespondInfo("喷头堵头，暂停")
            

            #lancaigang240103：如果是屏幕主动暂停，不处理stm32的主动上报
            if self.G_ToolheadIfHaveFilaFlag == True:
                    if self.G_IfToolheadHaveFilaInitiativePauseFlag==True:
                        self.G_PhrozenFluiddRespondInfo("屏幕主动暂停，不处理stm32主动上报")
                        return
            #lancaigang240113：如果是手动命令，过滤stm32的暂停上报
            if self.ManualCmdFlag==True or self.G_CutCheckTest==True:
                #lancaigang240611：手动命令也上报给串口屏
                self.G_PhrozenFluiddRespondInfo(SerialRxASCIIStr)
                #self.ManualCmdFlag=False
                self.G_PhrozenFluiddRespondInfo("手动测试命令，不处理stm32主动暂停上报")
                return

            self.G_ResumeProcessCheckPauseStatus=True
            self.G_PauseToLCDString=SerialRxASCIIStr
            #lancaigang240124：stm32上报暂停只能暂停1次
            if self.STM32ReprotPauseFlag==0:
                self.G_PauseTriggerWhileChangeChannelFlag=True
                if self.PG102Flag==True:
                    self.G_PhrozenFluiddRespondInfo("正在吐料中，暂缓暂停，待吐料完成再暂停")
                    self.PG102DelayPauseFlag=True
                    self.G_PauseToLCDString="+PAUSE:c,%d,%d" % (self.G_ChangeChannelTimeoutOldChan,self.G_ChangeChannelTimeoutNewChan)

                else:
                    #lancaigang250702：
                    if self.G_KlipperInPausing == False:
                        self.G_PhrozenFluiddRespondInfo("不在暂停中，允许新的暂停")
                        #self.Cmds_PhrozenKlipperPauseNoneCmdToSTM32(None)
                        #lancaigang231209：定时器中处理业务，会导致业务异常，后面要用线程处理中断业务
                        self.G_PhrozenFluiddRespondInfo("stm32主动暂停上报，暂停1次")
                        self.G_PhrozenFluiddRespondInfo("启用快速暂停")
                        self.G_KlipperQuickPause = True
                        self.Cmds_PhrozenKlipperPauseNoneCmdToSTM32(None)
                        self.G_KlipperIfPaused = True

                        self.STM32ReprotPauseFlag=1
                        #lancaigang231202：P1 C?自动换料时，如果第1次通道就进料异常暂停，如果要恢复，也继续从第1次通道开始
                        self.G_ChangeChannelFirstFilaFlag=True
                        #self.Cmds_PhrozenKlipperPauseNoneCmdToSTM32(None)a

                        self.G_PhrozenFluiddRespondInfo("+PAUSE:c,%d,%d" % (self.G_ChangeChannelTimeoutOldChan,self.G_ChangeChannelTimeoutNewChan))
                        self.G_PauseToLCDString="+PAUSE:c,%d,%d" % (self.G_ChangeChannelTimeoutOldChan,self.G_ChangeChannelTimeoutNewChan)
            
                    else:
                        self.G_PhrozenFluiddRespondInfo("暂停中，不允许新的暂停")
    
            else:
                self.G_PauseTriggerWhileChangeChannelFlag=True
                self.G_PhrozenFluiddRespondInfo("stm32主动暂停上报，重复暂停了")
                #lancaigang240325：重复暂停了，也要上报给串口屏
                #self.G_PhrozenFluiddRespondInfo("+PAUSE:a,%d" % self.G_ChangeChannelTimeoutNewChan)
                #self.G_PhrozenFluiddRespondInfo(self.G_PauseToLCDString)
                self.G_PhrozenFluiddRespondInfo("+PAUSE:c,%d,%d" % (self.G_ChangeChannelTimeoutOldChan,self.G_ChangeChannelTimeoutNewChan))
                self.G_PauseToLCDString="+PAUSE:c,%d,%d" % (self.G_ChangeChannelTimeoutOldChan,self.G_ChangeChannelTimeoutNewChan)

            return


        #lancaigang250506:吐料中补料异常，线材有咬坑
        if "+PAUSE:d" in SerialRxASCIIStr:
            #lancaigang240106：单色续料如果已经暂停，不允许再暂停
            if self.G_AMSDeviceWorkMode == AMS_WORK_MODE_MA:
                if self.G_KlipperIfPaused == True:
                    self.G_PhrozenFluiddRespondInfo("单色续料MA模式；重复暂停了if self.G_KlipperIfPaused == True:")
                    
                    
                    #lancaigang251124：
                    self.G_PhrozenFluiddRespondInfo("单色续料MA模式；喷头检测到线材，但补料期间stm32暂停报错，不能直接return；")
                    self.STM32ReprotPauseFlag=1
                    #lancaigang231202：P1 C?自动换料时，如果第1次通道就进料异常暂停，如果要恢复，也继续从第1次通道开始
                    #self.G_ChangeChannelFirstFilaFlag=True
                    #self.Cmds_PhrozenKlipperPauseNoneCmdToSTM32(None)
                    #self.G_PhrozenFluiddRespondInfo("+PAUSE:c,%d,%d" % (self.G_ChangeChannelTimeoutOldChan,self.G_ChangeChannelTimeoutNewChan))
                    self.G_PauseToLCDString="+PAUSE:d,%d,%d" % (self.G_ChangeChannelTimeoutOldChan,self.G_ChangeChannelTimeoutNewChan)
        
                    
                    return
            #lancaigang240413：单色模式，如果已经暂停，不允许再暂停
            if self.G_AMSDeviceWorkMode == AMS_WORK_MODE_FILA_RUNOUT:
                if self.G_KlipperIfPaused == True:
                    self.G_PhrozenFluiddRespondInfo("单色M3模式，有AMS多色，重复暂停了:")
                    return
            self.G_PhrozenFluiddRespondInfo("吐料补料异常，线材有咬坑，暂停")
            

            #lancaigang240103：如果是屏幕主动暂停，不处理stm32的主动上报
            if self.G_ToolheadIfHaveFilaFlag == True:
                    if self.G_IfToolheadHaveFilaInitiativePauseFlag==True:
                        self.G_PhrozenFluiddRespondInfo("屏幕主动暂停，不处理stm32主动上报")
                        return
            #lancaigang240113：如果是手动命令，过滤stm32的暂停上报
            if self.ManualCmdFlag==True or self.G_CutCheckTest==True:
                #lancaigang240611：手动命令也上报给串口屏
                self.G_PhrozenFluiddRespondInfo(SerialRxASCIIStr)
                #self.ManualCmdFlag=False
                self.G_PhrozenFluiddRespondInfo("手动测试命令，不处理stm32主动暂停上报")
                return

            self.G_ResumeProcessCheckPauseStatus=True
            self.G_PauseToLCDString=SerialRxASCIIStr
            #lancaigang240124：stm32上报暂停只能暂停1次
            if self.STM32ReprotPauseFlag==0:
                self.G_PauseTriggerWhileChangeChannelFlag=True
                if self.PG102Flag==True:
                    self.G_PhrozenFluiddRespondInfo("正在吐料中，暂缓暂停，待吐料完成再暂停")
                    self.PG102DelayPauseFlag=True
                    self.G_PauseToLCDString="+PAUSE:d,%d,%d" % (self.G_ChangeChannelTimeoutOldChan,self.G_ChangeChannelTimeoutNewChan)

                else:
                    #lancaigang250702：
                    if self.G_KlipperInPausing == False:
                        self.G_PhrozenFluiddRespondInfo("不在暂停中，允许新的暂停")
                        #self.Cmds_PhrozenKlipperPauseNoneCmdToSTM32(None)
                        #lancaigang231209：定时器中处理业务，会导致业务异常，后面要用线程处理中断业务
                        self.G_PhrozenFluiddRespondInfo("stm32主动暂停上报，暂停1次")
                        self.G_PhrozenFluiddRespondInfo("启用快速暂停")
                        self.G_KlipperQuickPause = True
                        self.Cmds_PhrozenKlipperPauseNoneCmdToSTM32(None)
                        self.G_KlipperIfPaused = True
                        self.STM32ReprotPauseFlag=1
                        #lancaigang231202：P1 C?自动换料时，如果第1次通道就进料异常暂停，如果要恢复，也继续从第1次通道开始
                        self.G_ChangeChannelFirstFilaFlag=True
                        #self.Cmds_PhrozenKlipperPauseNoneCmdToSTM32(None)a

                        self.G_PhrozenFluiddRespondInfo("+PAUSE:d,%d,%d" % (self.G_ChangeChannelTimeoutOldChan,self.G_ChangeChannelTimeoutNewChan))
                        self.G_PauseToLCDString="+PAUSE:d,%d,%d" % (self.G_ChangeChannelTimeoutOldChan,self.G_ChangeChannelTimeoutNewChan)
            
                    else:
                        self.G_PhrozenFluiddRespondInfo("暂停中，不允许新的暂停")
    
            else:
                self.G_PauseTriggerWhileChangeChannelFlag=True
                self.G_PhrozenFluiddRespondInfo("stm32主动暂停上报，重复暂停了")
                #lancaigang240325：重复暂停了，也要上报给串口屏
                #self.G_PhrozenFluiddRespondInfo("+PAUSE:a,%d" % self.G_ChangeChannelTimeoutNewChan)
                #self.G_PhrozenFluiddRespondInfo(self.G_PauseToLCDString)
                self.G_PhrozenFluiddRespondInfo("+PAUSE:d,%d,%d" % (self.G_ChangeChannelTimeoutOldChan,self.G_ChangeChannelTimeoutNewChan))
                self.G_PauseToLCDString="+PAUSE:d,%d,%d" % (self.G_ChangeChannelTimeoutOldChan,self.G_ChangeChannelTimeoutNewChan)

            return

        #//lancaigang250507:+PAUSE:e,oldchannel,newchannel;e-未烘干状态下，AMS腔内温度过高，不允许打印
        if "+PAUSE:e" in SerialRxASCIIStr:
            #lancaigang240106：单色续料如果已经暂停，不允许再暂停
            if self.G_AMSDeviceWorkMode == AMS_WORK_MODE_MA:
                if self.G_KlipperIfPaused == True:
                    self.G_PhrozenFluiddRespondInfo("单色续料MA模式；重复暂停了if self.G_KlipperIfPaused == True:")
                    return
            #lancaigang240413：单色模式，如果已经暂停，不允许再暂停
            if self.G_AMSDeviceWorkMode == AMS_WORK_MODE_FILA_RUNOUT:
                if self.G_KlipperIfPaused == True:
                    self.G_PhrozenFluiddRespondInfo("单色M3模式，有AMS多色，重复暂停了:")
                    return
            
            #lancaigang250510：未在打印模式，不允许暂停klipper，但要提示串口屏
            if self.G_AMSDeviceWorkMode == AMS_WORK_MODE_UNKNOW:
                self.G_PhrozenFluiddRespondInfo("未在打印模式，不允许暂停klipper，但要提示串口屏")
                self.G_PhrozenFluiddRespondInfo("+PAUSE:e,%d,%d" % (self.G_ChangeChannelTimeoutOldChan,self.G_ChangeChannelTimeoutNewChan))
                self.G_PauseToLCDString="+PAUSE:e,%d,%d" % (self.G_ChangeChannelTimeoutOldChan,self.G_ChangeChannelTimeoutNewChan)
                return

            self.G_PhrozenFluiddRespondInfo("未烘干状态下，AMS腔内温度过高，不允许打印，暂停")
            

            #lancaigang240103：如果是屏幕主动暂停，不处理stm32的主动上报
            if self.G_ToolheadIfHaveFilaFlag == True:
                    if self.G_IfToolheadHaveFilaInitiativePauseFlag==True:
                        self.G_PhrozenFluiddRespondInfo("屏幕主动暂停，不处理stm32主动上报")
                        return
            #lancaigang240113：如果是手动命令，过滤stm32的暂停上报
            if self.ManualCmdFlag==True or self.G_CutCheckTest==True:
                #lancaigang240611：手动命令也上报给串口屏
                self.G_PhrozenFluiddRespondInfo(SerialRxASCIIStr)
                #self.ManualCmdFlag=False
                self.G_PhrozenFluiddRespondInfo("手动测试命令，不处理stm32主动暂停上报")
                return

            self.G_ResumeProcessCheckPauseStatus=True
            self.G_PauseToLCDString=SerialRxASCIIStr
            #lancaigang240124：stm32上报暂停只能暂停1次
            if self.STM32ReprotPauseFlag==0:
                self.G_PauseTriggerWhileChangeChannelFlag=True
                if self.PG102Flag==True:
                    self.G_PhrozenFluiddRespondInfo("正在吐料中，暂缓暂停，待吐料完成再暂停")
                    self.PG102DelayPauseFlag=True
                    self.G_PauseToLCDString="+PAUSE:e,%d,%d" % (self.G_ChangeChannelTimeoutOldChan,self.G_ChangeChannelTimeoutNewChan)

                else:
                    #lancaigang250702：
                    if self.G_KlipperInPausing == False:
                        self.G_PhrozenFluiddRespondInfo("不在暂停中，允许新的暂停")
                        #self.Cmds_PhrozenKlipperPauseNoneCmdToSTM32(None)
                        #lancaigang231209：定时器中处理业务，会导致业务异常，后面要用线程处理中断业务
                        self.G_PhrozenFluiddRespondInfo("stm32主动暂停上报，暂停1次")
                        self.G_PhrozenFluiddRespondInfo("启用快速暂停")
                        self.G_KlipperQuickPause = True
                        self.Cmds_PhrozenKlipperPauseNoneCmdToSTM32(None)
                        self.G_KlipperIfPaused = True
                        self.STM32ReprotPauseFlag=1
                        #lancaigang231202：P1 C?自动换料时，如果第1次通道就进料异常暂停，如果要恢复，也继续从第1次通道开始
                        self.G_ChangeChannelFirstFilaFlag=True
                        #self.Cmds_PhrozenKlipperPauseNoneCmdToSTM32(None)a

                        self.G_PhrozenFluiddRespondInfo("+PAUSE:e,%d,%d" % (self.G_ChangeChannelTimeoutOldChan,self.G_ChangeChannelTimeoutNewChan))
                        self.G_PauseToLCDString="+PAUSE:e,%d,%d" % (self.G_ChangeChannelTimeoutOldChan,self.G_ChangeChannelTimeoutNewChan)
            
                    else:
                        self.G_PhrozenFluiddRespondInfo("暂停中，不允许新的暂停")
    
            else:
                self.G_PauseTriggerWhileChangeChannelFlag=True
                self.G_PhrozenFluiddRespondInfo("stm32主动暂停上报，重复暂停了")
                #lancaigang240325：重复暂停了，也要上报给串口屏
                #self.G_PhrozenFluiddRespondInfo("+PAUSE:e,%d" % self.G_ChangeChannelTimeoutNewChan)
                #self.G_PhrozenFluiddRespondInfo(self.G_PauseToLCDString)
                self.G_PhrozenFluiddRespondInfo("+PAUSE:e,%d,%d" % (self.G_ChangeChannelTimeoutOldChan,self.G_ChangeChannelTimeoutNewChan))
                self.G_PauseToLCDString="+PAUSE:e,%d,%d" % (self.G_ChangeChannelTimeoutOldChan,self.G_ChangeChannelTimeoutNewChan)

            return

        #//lancaigang250507:+PAUSE:f,oldchannel,newchannel;f-烘干状态下，不允许打印
        if "+PAUSE:f" in SerialRxASCIIStr:
            #lancaigang240106：单色续料如果已经暂停，不允许再暂停
            if self.G_AMSDeviceWorkMode == AMS_WORK_MODE_MA:
                if self.G_KlipperIfPaused == True:
                    self.G_PhrozenFluiddRespondInfo("单色续料MA模式；重复暂停了if self.G_KlipperIfPaused == True:")
                    return
            #lancaigang240413：单色模式，如果已经暂停，不允许再暂停
            if self.G_AMSDeviceWorkMode == AMS_WORK_MODE_FILA_RUNOUT:
                if self.G_KlipperIfPaused == True:
                    self.G_PhrozenFluiddRespondInfo("单色M3模式，有AMS多色，重复暂停了:")
                    return
            self.G_PhrozenFluiddRespondInfo("烘干状态下，不允许打印，暂停")
            
            #lancaigang250510：未在打印模式，不允许暂停klipper，但要提示串口屏
            if self.G_AMSDeviceWorkMode == AMS_WORK_MODE_UNKNOW:
                self.G_PhrozenFluiddRespondInfo("未在打印模式，不允许暂停klipper，但要提示串口屏")
                self.G_PhrozenFluiddRespondInfo("+PAUSE:f,%d,%d" % (self.G_ChangeChannelTimeoutOldChan,self.G_ChangeChannelTimeoutNewChan))
                self.G_PauseToLCDString="+PAUSE:f,%d,%d" % (self.G_ChangeChannelTimeoutOldChan,self.G_ChangeChannelTimeoutNewChan)
                return
            

            #lancaigang240103：如果是屏幕主动暂停，不处理stm32的主动上报
            if self.G_ToolheadIfHaveFilaFlag == True:
                    if self.G_IfToolheadHaveFilaInitiativePauseFlag==True:
                        self.G_PhrozenFluiddRespondInfo("屏幕主动暂停，不处理stm32主动上报")
                        return
            #lancaigang240113：如果是手动命令，过滤stm32的暂停上报
            if self.ManualCmdFlag==True or self.G_CutCheckTest==True:
                #lancaigang240611：手动命令也上报给串口屏
                self.G_PhrozenFluiddRespondInfo(SerialRxASCIIStr)
                #self.ManualCmdFlag=False
                self.G_PhrozenFluiddRespondInfo("手动测试命令，不处理stm32主动暂停上报")
                return

            self.G_ResumeProcessCheckPauseStatus=True
            self.G_PauseToLCDString=SerialRxASCIIStr
            #lancaigang240124：stm32上报暂停只能暂停1次
            if self.STM32ReprotPauseFlag==0:
                self.G_PauseTriggerWhileChangeChannelFlag=True
                if self.PG102Flag==True:
                    self.G_PhrozenFluiddRespondInfo("正在吐料中，暂缓暂停，待吐料完成再暂停")
                    self.PG102DelayPauseFlag=True
                    self.G_PauseToLCDString="+PAUSE:f,%d,%d" % (self.G_ChangeChannelTimeoutOldChan,self.G_ChangeChannelTimeoutNewChan)

                else:
                    #lancaigang250702：
                    if self.G_KlipperInPausing == False:
                        self.G_PhrozenFluiddRespondInfo("不在暂停中，允许新的暂停")
                        #self.Cmds_PhrozenKlipperPauseNoneCmdToSTM32(None)
                        #lancaigang231209：定时器中处理业务，会导致业务异常，后面要用线程处理中断业务
                        self.G_PhrozenFluiddRespondInfo("stm32主动暂停上报，暂停1次")
                        self.G_PhrozenFluiddRespondInfo("启用快速暂停")
                        self.G_KlipperQuickPause = True
                        self.Cmds_PhrozenKlipperPauseNoneCmdToSTM32(None)
                        self.G_KlipperIfPaused = True
                        self.STM32ReprotPauseFlag=1
                        #lancaigang231202：P1 C?自动换料时，如果第1次通道就进料异常暂停，如果要恢复，也继续从第1次通道开始
                        self.G_ChangeChannelFirstFilaFlag=True
                        #self.Cmds_PhrozenKlipperPauseNoneCmdToSTM32(None)a

                        self.G_PhrozenFluiddRespondInfo("+PAUSE:f,%d,%d" % (self.G_ChangeChannelTimeoutOldChan,self.G_ChangeChannelTimeoutNewChan))
                        self.G_PauseToLCDString="+PAUSE:f,%d,%d" % (self.G_ChangeChannelTimeoutOldChan,self.G_ChangeChannelTimeoutNewChan)
            
                    else:
                        self.G_PhrozenFluiddRespondInfo("暂停中，不允许新的暂停")
    
            else:
                self.G_PauseTriggerWhileChangeChannelFlag=True
                self.G_PhrozenFluiddRespondInfo("stm32主动暂停上报，重复暂停了")
                #lancaigang240325：重复暂停了，也要上报给串口屏
                #self.G_PhrozenFluiddRespondInfo("+PAUSE:a,%d" % self.G_ChangeChannelTimeoutNewChan)
                #self.G_PhrozenFluiddRespondInfo(self.G_PauseToLCDString)
                self.G_PhrozenFluiddRespondInfo("+PAUSE:f,%d,%d" % (self.G_ChangeChannelTimeoutOldChan,self.G_ChangeChannelTimeoutNewChan))
                self.G_PauseToLCDString="+PAUSE:f,%d,%d" % (self.G_ChangeChannelTimeoutOldChan,self.G_ChangeChannelTimeoutNewChan)

            return













        if "+FORCEFORWARD:1" in SerialRxASCIIStr:
            self.G_PhrozenFluiddRespondInfo("取出喷头料管，强制取出卡料")
            return



        #lancaigang231202：如果收到stm32暂停响应，则暂停klipper




        # // CS设备id   运行模式 前个mc状态   当前mc状态  通道号
        # // CS00       N0      M09         T09         C5
        # // CS00       N0      M02         T03         C0
        # // CS00       N0      M08         T10         C1
        #    deviceid   mode    pre_state   state       chan
        #正则表达式解析串口数据
        #CS00N0M03T04C0
        message_obj = re.match(
            AMS_SERIALPORT_RECEIV_PARSE_PATTERN,#正则表达式
            SerialRxASCIIStr,
            re.M | re.I,
        )


        # 解析的串口数据错误
        if not message_obj:
            return
        

        if int(message_obj.group("mode")) is AMS_MC_MODE:
            self.G_PhrozenFluiddRespondInfo("模式mode==多色模式==%d" % AMS_MC_MODE)
        if int(message_obj.group("mode")) is AMS_MA_MODE:
            self.G_PhrozenFluiddRespondInfo("模式mode==续料模式==%d" % AMS_MA_MODE)

        if int(message_obj.group("state")) is MC_STANDBY:
            self.G_PhrozenFluiddRespondInfo("当前状态state==待机阶段==%d" % MC_STANDBY)
        if int(message_obj.group("state")) is MC_PREPARTION:
            self.G_PhrozenFluiddRespondInfo("当前状态state==备料停靠阶段==%d" % MC_STANDBY)
        if int(message_obj.group("state")) is MC_CHANGING_P1:
            self.G_PhrozenFluiddRespondInfo("当前状态state==换料阶段1==%d" % MC_CHANGING_P1)
        if int(message_obj.group("state")) is MC_CHANGING_P2:
            self.G_PhrozenFluiddRespondInfo("当前状态state==换料阶段2==%d" % MC_CHANGING_P2)
        if int(message_obj.group("state")) is MC_FORCE_FEED:
            self.G_PhrozenFluiddRespondInfo("当前状态state==换料阶段强制补料==%d" % MC_FORCE_FEED)
        if int(message_obj.group("state")) is MC_PRINTING:
            self.G_PhrozenFluiddRespondInfo("当前状态state==打印阶段补料==%d" % MC_PRINTING)
        if int(message_obj.group("state")) is MC_ROLLBACK:
            self.G_PhrozenFluiddRespondInfo("当前状态state==完全退料==%d" % MC_ROLLBACK)
        if int(message_obj.group("state")) is MC_PARKBACK:
            self.G_PhrozenFluiddRespondInfo("当前状态state==退料到停靠位==%d" % MC_PARKBACK)
        if int(message_obj.group("state")) is MC_PARKALL:
            self.G_PhrozenFluiddRespondInfo("当前状态state==全部退料到停靠位==%d" % MC_PARKALL)
        if int(message_obj.group("state")) is MC_CLEANING:
            self.G_PhrozenFluiddRespondInfo("当前状态state==所有线料清空==%d" % MC_CLEANING)
        if int(message_obj.group("state")) is MC_ERR_TIMEOUT:
            self.G_PhrozenFluiddRespondInfo("当前状态state==超时出错状态==%d" % MC_ERR_TIMEOUT)
        if int(message_obj.group("state")) is MC_ERR_RUNOUT:
            self.G_PhrozenFluiddRespondInfo("当前状态state==断料出错状态==%d" % MC_ERR_RUNOUT)
        if int(message_obj.group("state")) is MC_ERR_BLOCKUP:
            self.G_PhrozenFluiddRespondInfo("当前状态state==堵料出错状态==%d" % MC_ERR_BLOCKUP)
            #raise self.error("电机堵料出错")
            #self.Cmds_PhrozenKlipperPause(None)

        self.G_PhrozenFluiddRespondInfo("通道电机号chan==%d" % int(message_obj.group("chan")))
        #raise self.error("测试；通道电机号")

        # lancaigang20231013：换料阶段处理；卡线重新进料
        if int(message_obj.group("mode")) is AMS_MC_MODE:
            #lancaigang20231114：有时候不断的重试进料多次，先屏蔽
            cur_chan = int(message_obj.group("chan")) + 1
            # #lancaigang20231013：换料阶段2-->强制补料
            # if (int(message_obj.group("pre_state")) is MC_CHANGING_P2) and (int(message_obj.group("state")) is MC_FORCE_FEED):
            #     #lancaigang20231013：喷头上没有线材, 但缓冲器满状态, 说明卡线, 重新退线进线
            #     if not self.G_ToolheadIfHaveFilaFlag:
            #         self.AMSErrorRetryTimes += 1
            #         if self.AMSErrorRetryTimes < 5:
            #             #// =====T1~Tn命令；PRZ_T[n] P1 T[n]n:1 ~32(设备无组网,取1 ~4)手动换到指定通道,仅换线(用于测试)
            #             self.Cmds_AMSSerial1Send("T%d" % cur_chan)
            #             self.G_PhrozenFluiddRespondInfo("换料时喷头没检测到线材，命令T?重试；cmd T%s at %d times" % (cur_chan, self.AMSErrorRetryTimes))
            #         else:
            #             self.G_PhrozenFluiddRespondInfo("换料时喷头没检测到线材，命令T?重试了5次, 命令P?回退到停靠位")
            #             #// 后退到停泊位；// =====P1 D[n]；n:1~32(设备无组网,取1~4)；指定通道的线料后退到停泊在停靠位待命状态 Yes；====="P?"；
            #             self.Cmds_AMSSerial1Send("P%d" % cur_chan)
            #             self.Cmds_PhrozenKlipperPause(None)
            #             self.AMSErrorRetryTimes = 0
            #     #lancaigang20231013：喷头上检测到线材
            #     else:
            #         # 状态正常后, 重置出错重试次数
            #         self.AMSErrorRetryTimes = 0

            #     return self.G_PhrozenReactor.NOW + AMS_SERIALPORT_RECV_TIMER

            #lancaigang231103：先屏蔽stm32返回的超时状态处理，没什么用，导致执行错乱
            #lancaigang20231013：stm32超时状态处理
            # if int(message_obj.group("state")) is MC_ERR_TIMEOUT:
            #     # typedef enum Enum_MCStateMachine {
            #     #     // 00； Idle待机阶段
            #     #     MCSTATEMACHINE_IDLE_STANDBY,
            #     #     // 01； 停靠位待进料到打印机阶段；// =====P1 S0 所有通道在停靠位准备好进料到打印机状态, 可以进料到停靠位或后退到停靠位；====="RD";
            #     #     MCSTATEMACHINE_PARKPOSITION_ISREADY_INFILA_TO_PRINTER,
            #     #     // 02； 换料阶段1；// =====P1 T[n]n:1 ~32(设备无组网,取1 ~4)手动换到指定通道,仅换线(用于测试)；====="T?"；
            #     #     MCSTATEMACHINE_CHANGING_FILA_STAGE_P1,
            #     #     // 03； 换料阶段2；// =====P1 T[n]n:1 ~32(设备无组网,取1 ~4)手动换到指定通道,仅换线(用于测试)；====="T?"；
            #     #     MCSTATEMACHINE_CHANGING_FILA_STAGE_P2,
            #     #     // 04； 强制补料到打印头，对应P1 T?
            #     #     MCSTATEMACHINE_FORCE_FEED_INFILA_TO_PRINTER,
            #     #     // 05； 打印过程中阶段(补料)
            #     #     MCSTATEMACHINE_PRINTING_INPROCESS_FEED,
            #     #     // 06； 完全退料；// =====B1~Bn命令；PRZ_B[n] P1 B[n]n:1 ~32(设备无组网,取1 ~4)指定通道线料完全退出 Yes
            #     #     MCSTATEMACHINE_FULLY_ROLLBACK,
            #     #     // 07； 后退到停靠位；//"P"；P1 D[n]；n:1~32(设备无组网,取1~4)；指定通道的线料后退停靠位待命状态 Yes
            #     #     MCSTATEMACHINE_ROLLBACK_TO_PARKPOSITION,
            #     #     // 08； 全部后退到停靠位；// "AP"；P2 A1 所有线料退到停靠位待打印 Yes
            #     #     MCSTATEMACHINE_ROLLBACK_ALL_TO_PARKPOSITION,
            #     #     // 09； 清空所有线；//====="CL"； P2 A2；退出所有线材 Yes
            #     #     MCSTATEMACHINE_CLEAN_ALL_CHANNEL,
            #     #     // 10； 超时出错状态
            #     #     MCSTATEMACHINE_ERROR_TIMEOUT,
            #     #     // 11； 断料出错状态
            #     #     MCSTATEMACHINE_ERROR_RUNOUT,
            #     # } Enum_MCStateMachine;
            #     self.AMSErrorRetryTimes += 1
            #     if self.AMSErrorRetryTimes < 5:
            #         #// =====T1~Tn命令；PRZ_T[n] P1 T[n]n:1 ~32(设备无组网,取1 ~4)手动换到指定通道,仅换线(用于测试)
            #         self.G_PhrozenFluiddRespondInfo("stm32错误状态，命令T?重试；cmd T%s at %d times" % (message_obj.group("chan"), self.AMSErrorRetryTimes))
            #         self.Cmds_AMSSerial1Send("T%d" % cur_chan)
            #     else:
            #         self.G_PhrozenFluiddRespondInfo("stm32错误状态，命令T?重试了5次, 命令P?回退到停靠位")
            #         #// 后退到停泊位；// =====P1 D[n]；n:1~32(设备无组网,取1~4)；指定通道的线料后退到停泊在停靠位待命状态 Yes；====="P?"；
            #         self.Cmds_AMSSerial1Send("P%d" % cur_chan)
            #         self.Cmds_PhrozenKlipperPause(None)
            #         self.AMSErrorRetryTimes = 0

            #     return self.G_PhrozenReactor.NOW + AMS_SERIALPORT_RECV_TIMER

            

        #lancaigang20231013：续料模式
        if int(message_obj.group("mode")) is AMS_MA_MODE:
            pass



    
    ####################################
    #函数名称：
    #输入参数：
    #返 回 值:
    #功能描述：蓝才刚-20230830
    ####################################
    #lancaigang20231013：串口接收处理周期定时器
    #100ms
    def Device_TimmerUart1Recv(self, eventtime):
        #self.G_PhrozenFluiddRespondInfo("[(dev.python)Device_TimmerUart1Recv]")
        #lancaigang240427：try catch
        try:
            # if self.G_SerialPort1OpenFlag==False:
            #     self.G_PhrozenFluiddRespondInfo("[(dev.python)Device_TimmerUart1Recv]串口1已经关闭")
            # if self.G_SerialPort2OpenFlag==False:
            #     self.G_PhrozenFluiddRespondInfo("[(dev.python)Device_TimmerUart1Recv]串口2已经关闭")

            #tty1连接失败
            if self.G_SerialPort1OpenFlag==False:
                self.G_ASM1DisconnectErrorCount=0
                #self.G_PhrozenFluiddRespondInfo("[(dev.python)Device_TimmerUart1Recv]串口1连接异常，永远退出回调函数")
                #self.G_PhrozenFluiddRespondInfo("self.G_AMS1ErrorRestartCount=%d" % self.G_AMS1ErrorRestartCount)
                try:
                    if self.G_SerialPort1Obj is not None:
                        if self.G_SerialPort1Obj.is_open:
                            #tty1关闭
                            self.G_SerialPort1Obj.close()
                            self.G_PhrozenFluiddRespondInfo("关闭串口1成功")
                            self.G_PhrozenFluiddRespondInfo("AMS1连接失败")
                            #self.G_PauseToLCDString="+PAUSE:g,%d,%d" % (self.G_ChangeChannelTimeoutOldChan,self.G_ChangeChannelTimeoutNewChan)
                            self.G_PhrozenFluiddRespondInfo("缓存暂停命令+PAUSE:g")
                except:
                    self.G_PhrozenFluiddRespondInfo("关闭串口1异常")

                self.G_AMS1ErrorRestartCount=self.G_AMS1ErrorRestartCount+1

                #lancaigang241108:延时几秒再暂停，防止AMS重启需要一些时间
                if self.G_AMS1ErrorRestartCount>=5:
                    #self.G_PhrozenFluiddRespondInfo("if self.G_AMS1ErrorRestartCount>=5:")

                    self.G_AMS1ErrorRestartCount=0
                    #lancaigang250619:如果USB异常，待换色异常时才报错
                    self.G_PauseToLCDString="+PAUSE:g,%d,%d" % (self.G_ChangeChannelTimeoutOldChan,self.G_ChangeChannelTimeoutNewChan)
                    #self.G_PhrozenFluiddRespondInfo("缓存暂停命令+PAUSE:g")

                    # if self.G_KlipperIfPaused==False:
                    #     self.G_KlipperIfPaused = True
                    #     #self.Cmds_PhrozenKlipperPauseNoneCmdToSTM32(None)
                    #     if self.G_CancelFlag==False:
                    #         # self.G_PhrozenFluiddRespondInfo("+PAUSE:g,%d,%d" % (self.G_ChangeChannelTimeoutOldChan,self.G_ChangeChannelTimeoutNewChan))
                    #         # self.G_PauseToLCDString="+PAUSE:g,%d,%d" % (self.G_ChangeChannelTimeoutOldChan,self.G_ChangeChannelTimeoutNewChan)
                    #         self.G_PhrozenFluiddRespondInfo("AMS1连接异常暂停")

                    #         #lancaigang250604:
                    #         if self.G_AMSDeviceWorkMode == AMS_WORK_MODE_UNKNOW:#M0
                    #             self.G_PhrozenFluiddRespondInfo("未知模式，不用暂停")
                    #         else:
                    #             if self.STM32ReprotPauseFlag==0:
                    #                 self.G_PauseTriggerWhileChangeChannelFlag=True
                    #                 if self.PG102Flag==True:
                    #                     self.G_PhrozenFluiddRespondInfo("正在吐料中，暂缓暂停，待吐料完成再暂停")
                    #                     self.PG102DelayPauseFlag=True
                    #                     #self.G_PhrozenFluiddRespondInfo("+PAUSE:g,%d,%d" % (self.G_ChangeChannelTimeoutOldChan,self.G_ChangeChannelTimeoutNewChan))
                    #                     self.G_PauseToLCDString="+PAUSE:g,%d,%d" % (self.G_ChangeChannelTimeoutOldChan,self.G_ChangeChannelTimeoutNewChan)
                    #                 else:
                    #                     self.G_PhrozenFluiddRespondInfo("未吐料，可以直接暂停")
                    #                     self.Cmds_PhrozenKlipperPauseNoneCmdToSTM32(None)
                    #                     self.G_KlipperIfPaused = True
                    #                     #self.Cmds_PhrozenKlipperPauseNoneCmdToSTM32(None)
                    #                     self.STM32ReprotPauseFlag=1
                    #                     #lancaigang231202：P1 C?自动换料时，如果第1次通道就进料异常暂停，如果要恢复，也继续从第1次通道开始
                    #                     self.G_ChangeChannelFirstFilaFlag=True
                    #                     self.G_PhrozenFluiddRespondInfo("+PAUSE:g,%d,%d" % (self.G_ChangeChannelTimeoutOldChan,self.G_ChangeChannelTimeoutNewChan))
                    #                     self.G_PauseToLCDString="+PAUSE:g,%d,%d" % (self.G_ChangeChannelTimeoutOldChan,self.G_ChangeChannelTimeoutNewChan)
                    #             else:
                    #                 self.G_PauseTriggerWhileChangeChannelFlag=True
                    #                 self.G_PauseToLCDString="+PAUSE:g,%d,%d" % (self.G_ChangeChannelTimeoutOldChan,self.G_ChangeChannelTimeoutNewChan)

                    #         #     self.G_PhrozenFluiddRespondInfo("+PAUSE:g,%d,%d" % (self.G_ChangeChannelTimeoutOldChan,self.G_ChangeChannelTimeoutNewChan))
                    #         #lancaigang20231013：断开连接
                    #         self.Device_DisconnectAMSDevice()

                    # #if self.G_KlipperIfPaused==True:
                    # else:
                    #     self.G_PhrozenFluiddRespondInfo("USB异常，当前已经是暂停状态")
                    #     self.G_PauseToLCDString="+PAUSE:g,%d,%d" % (self.G_ChangeChannelTimeoutOldChan,self.G_ChangeChannelTimeoutNewChan)


                    #lancaigang240524：永远退出回调函数
                    return self.G_PhrozenReactor.NEVER


                return eventtime + AMS_SERIALPORT_RECV_TIMER

            #lancaigang250619:USB连接正常，则清空
            #self.G_PauseToLCDString=""
            self.G_AMS1ErrorRestartCount=0






            # #lancaigang240427：AMS异常重启，需要记录
            # if self.G_AMS1ErrorRestartFlag == True:
            #     self.G_PhrozenFluiddRespondInfo("AMS1异常或重启;self.G_AMSErrorRestartCount=%d" % self.G_AMSErrorRestartCount)
            #     self.G_PhrozenFluiddRespondInfo("+AMSReboot:%d" % self.G_AMSErrorRestartCount)
            #     self.G_AMS1ErrorRestartFlag = False
                
            #     try:
            #         self.G_PhrozenFluiddRespondInfo("重新初始化串口1")
            #         self.G_SerialPort1Obj = serial.Serial(self.G_Serialport1Define, SERIAL_PORT_BAUD, timeout=3)
            #         #串口1打开成功
            #         if self.G_SerialPort1Obj.is_open:
            #             self.G_SerialPort1OpenFlag = True
            #             self.G_PhrozenFluiddRespondInfo("重新初始化串口1成功")
            #             #lancaigang231213：打开串口1
            #             self.G_SerialPort1Obj.flushInput()  # clean serial write cache
            #             self.G_SerialPort1Obj.flush()
            #             self.G_PhrozenFluiddRespondInfo("串口1清空")
            #             self.G_PhrozenFluiddRespondInfo("重新注册串口1回调函数")
            #             self.G_SerialPort1RecvTimmer = self.G_PhrozenReactor.register_timer(self.Device_TimmerUart1Recv, self.G_PhrozenReactor.NOW)
            #     except:
            #         self.G_PhrozenFluiddRespondInfo("未能打开tty1口，请检查USB口或重启尝试")

            #     return eventtime + AMS_SERIALPORT_RECV_TIMER



            # #lancaigang240410：
            # if self.G_CancelFlag==True:
            #     #self.G_PhrozenFluiddRespondInfo("已取消打印")
            #     return eventtime + AMS_SERIALPORT_RECV_TIMER



            #lancaigang231103:tty1串口有数据
            if self.G_SerialPort1Obj.inWaiting() > 0:
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

                self.G_PhrozenFluiddRespondInfo("[(dev.python)Device_TimmerUart1Recv]串口1读取数据")
                Lo_SerialRxLen=self.G_SerialPort1Obj.inWaiting()
                self.G_PhrozenFluiddRespondInfo("字节个数Lo_SerialRxLen=%d" % Lo_SerialRxLen)
                #self.G_PhrozenFluiddRespondInfo("串口定时器接收")
                Lo_SerialRxBytes=self.G_SerialPort1Obj.read(Lo_SerialRxLen)
                self.G_PhrozenFluiddRespondInfo("字节流Lo_SerialRxBytes=%s" % Lo_SerialRxBytes)
                self.G_PhrozenFluiddRespondInfo("字节流binascii.hexlify(Lo_SerialRxBytes)=%s" % binascii.hexlify(Lo_SerialRxBytes))
                #self.G_PhrozenFluiddRespondInfo("%x" % binascii.hexlify(Lo_SerialRxBytes))
                self.G_PhrozenFluiddRespondInfo("字节个数len(Lo_SerialRxBytes)=%d" % len(Lo_SerialRxBytes))
                #self.G_PhrozenFluiddRespondInfo("Lo_SerialRxBytes.count=%d" % Lo_SerialRxBytes.count)
                #for i in Lo_SerialRxBytes:
                    #self.G_PhrozenFluiddRespondInfo("%x" % i)

                self.G_PhrozenFluiddRespondInfo("Lo_SerialRxBytes[0]-16进制字节0x%2x" % Lo_SerialRxBytes[0])
                self.G_PhrozenFluiddRespondInfo("Lo_SerialRxBytes[0]-ASCII码字符%c" % Lo_SerialRxBytes[0])
                #self.G_PhrozenFluiddRespondInfo("Lo_SerialRxBytes[1]-16进制字节0x%2x" % Lo_SerialRxBytes[1])
                #self.G_PhrozenFluiddRespondInfo("Lo_SerialRxBytes[1]-ASCII码字符%c" % Lo_SerialRxBytes[1])



                #lancaigang240705：存在AMS多色
                self.G_AMSDevice1IfNormal=True


                try:
                    #lancaigang250411：AMS状态上报
                    #if "R" in self.G_SerialRxASCIIStr:
                    if Lo_SerialRxBytes[0]==0x52 and Lo_SerialRxLen==16:
                        self.G_PhrozenFluiddRespondInfo("AMS第1台异步返回")

                        #self.G_PhrozenFluiddRespondInfo("%s" % SerialRxASCIIStr)
                        Lo_AMSDeviceStateInfo = AMSDetailInfoBytes()
                        Lo_AMSDeviceStateInfo.whole[:] = Lo_SerialRxBytes
                        #python空字典
                        Lo_AMSDetailState = {}
                        self.G_AMS1DeviceState["dev_id"] = Lo_AMSDetailState["dev_id"] = Lo_AMSDeviceStateInfo.field.dev_id
                        self.G_AMS1DeviceState["active_dev_id"] = Lo_AMSDetailState["active_dev_id"] = Lo_AMSDeviceStateInfo.field.active_dev_id
                        self.G_AMS1DeviceState["dev_mode"] = Lo_AMSDetailState["dev_mode"] = Lo_AMSDeviceStateInfo.field.dev_mode
                        self.G_AMS1DeviceState["cache_empty"] = Lo_AMSDetailState["cache_empty"] = Lo_AMSDeviceStateInfo.field.cache_empty
                        #self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_CmdP114]缓冲器传感器空状态(bool)==%d" % Lo_AMSDeviceStateInfo.field.cache_empty)
                        self.G_AMS1DeviceState["cache_full"] = Lo_AMSDetailState["cache_full"] = Lo_AMSDeviceStateInfo.field.cache_full
                        #self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_CmdP114]缓冲器传感器满状态(bool)==%d" % Lo_AMSDeviceStateInfo.field.cache_full)
                        self.G_AMS1DeviceState["cache_exist"] = Lo_AMSDetailState["cache_exist"] = Lo_AMSDeviceStateInfo.field.cache_exist
                        #self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_CmdP114]缓冲器传感器线材状态(bool)==%d" % Lo_AMSDeviceStateInfo.field.cache_exist)
                        self.G_AMS1DeviceState["mc_state"] = Lo_AMSDetailState["mc_state"] = Lo_AMSDeviceStateInfo.field.mc_state
                        self.G_AMS1DeviceState["ma_state"] = Lo_AMSDetailState["ma_state"] = Lo_AMSDeviceStateInfo.field.ma_state
                        self.G_AMS1DeviceState["entry_state"] = Lo_AMSDetailState["entry_state"] = Lo_AMSDeviceStateInfo.field.entry_state
                        #self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_CmdP114]入口位传感器状态(bit位)==%d" % Lo_AMSDeviceStateInfo.field.entry_state)
                        self.G_AMS1DeviceState["park_state"] = Lo_AMSDetailState["park_state"] = Lo_AMSDeviceStateInfo.field.park_state
                        #self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_CmdP114]停靠位传感器状态(bit位)==%d" % Lo_AMSDeviceStateInfo.field.park_state)
                        
                        # 响应数据json转换
                        self.G_PhrozenFluiddRespondInfo(json.dumps(Lo_AMSDetailState))

                        #lancaigang250708：
                        self.G_PhrozenFluiddRespondInfo("P114成功")
                        self.G_PhrozenFluiddRespondInfo("+P114:1")
                        self.G_P114RunFlag=0

                    else:
                        self.G_PhrozenFluiddRespondInfo("AMS固件版本")
                        #lancaigang20231013：读取ttyUSB0串口字节流转换为ASCII码
                        #lancaigang240530：16进制字节转换为ASCII码字符
                        self.G_SerialRxASCIIStr = Lo_SerialRxBytes.decode("ascii")
                        self.G_PhrozenFluiddRespondInfo("ASCII码字符串self.G_SerialRxASCIIStr=%s" % self.G_SerialRxASCIIStr)


                        #lancaigang250411：AMS固件版本

                        # // AMS主板2固件-1 1
                        if "V-H18-I18-F" in self.G_SerialRxASCIIStr:
                            self.G_PhrozenFluiddRespondInfo("AMS段码屏烘干第1台固件版本")
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
                            # 主题:c0f535790a90/GetZbGwInfo_Respon
                            # {
                            #     "Data_ID": 95,
                            #     "Data": {
                            #         "GwId": "c0f535790a90",
                            #         "HomeId": "",
                            #         "GWSN": "0000000000000000000",
                            #         "AccountId": "",
                            #         "GwMac": "c0f535790a90",
                            #         "GwIP": "192.168.3.53",
                            #         "GwName": "Name-c0f535790a90",
                            #         "ProductId": "ARCO",
                            #         "MainImage": 15,
                            #         "MainHWVersion": 15,
                            #         "MainFWVersion": 24064,
                            #         "Gw_Ram": 248584,
                            #         "Gw_Rom": 826536,
                            #         "JoinMode": 1,
                            #         "ESSID": "",
                            #         "MqttClientEMQfd": 31,
                            #         "MqttClientId": "c0f535790a90",
                            #         "MqttBrokerUserName": "",
                            #         "MqttBrokerPwd": "",
                            #         "DriveCodeList": [
                            #             {
                            #                 "DriveCode": 1,
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
                            #                 "DriveCode": 3,
                            #                 "DriveImageType": 0,
                            #                 "DriveHwVersion": 0,
                            #                 "DriveFwVersion": 0,
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
                            #                 "DriveCode": 5,
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
                            #                 "DriveCode": 7,
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
                            #                 "DriveCode": 9,
                            #                 "DriveImageType": 0,
                            #                 "DriveHwVersion": 0,
                            #                 "DriveFwVersion": 0,
                            #                 "DriveId": 0
                            #             },
                            #             {
                            #                 "DriveCode": 10,
                            #                 "DriveImageType": 10,
                            #                 "DriveHwVersion": 10,
                            #                 "DriveFwVersion": 25033,
                            #                 "DriveId": 0
                            #             },
                            #             {
                            #                 "DriveCode": 11,
                            #                 "DriveImageType": 11,
                            #                 "DriveHwVersion": 11,
                            #                 "DriveFwVersion": 25022,
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
                            #                 "DriveCode": 13,
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
                            #                 "DriveCode": 15,
                            #                 "DriveImageType": 0,
                            #                 "DriveHwVersion": 0,
                            #                 "DriveFwVersion": 0,
                            #                 "DriveId": 0
                            #             },
                            #             {
                            #                 "DriveCode": 16,
                            #                 "DriveImageType": 0,
                            #                 "DriveHwVersion": 0,
                            #                 "DriveFwVersion": 0,
                            #                 "DriveId": 0
                            #             },
                            #             {
                            #                 "DriveCode": 17,
                            #                 "DriveImageType": 0,
                            #                 "DriveHwVersion": 0,
                            #                 "DriveFwVersion": 0,
                            #                 "DriveId": 0
                            #             },
                            #             {
                            #                 "DriveCode": 18,
                            #                 "DriveImageType": 0,
                            #                 "DriveHwVersion": 0,
                            #                 "DriveFwVersion": 0,
                            #                 "DriveId": 0
                            #             },
                            #             {
                            #                 "DriveCode": 19,
                            #                 "DriveImageType": 0,
                            #                 "DriveHwVersion": 0,
                            #                 "DriveFwVersion": 0,
                            #                 "DriveId": 0
                            #             },
                            #             {
                            #                 "DriveCode": 20,
                            #                 "DriveImageType": 0,
                            #                 "DriveHwVersion": 0,
                            #                 "DriveFwVersion": 0,
                            #                 "DriveId": 0
                            #             }
                            #         ]
                            #     }
                            # }
                            #lancaigang250724：读取系统镜像id，区分不同产品不同主板不同固件
                            #lancaigang250724:读取镜像id
                            self.Cmds_GetImageId()
                            if self.G_ImageId==16:
                                self.G_PhrozenFluiddRespondInfo("镜像Id==16：ARCO300-MKS-RK3328-STM32F407VET6-I16")
                                #lancaigang240530：版本写到dat文件；DriveCodeJson.dat
                                filename='/home/mks/hdlDat/DriveCodeFile.dat'
                            elif self.G_ImageId==31:
                                self.G_PhrozenFluiddRespondInfo("镜像Id==31：ARCO300-phrozen-RK3308-STM32F407VET6-I31")
                                #lancaigang240530：版本写到dat文件；DriveCodeJson.dat
                                filename='/home/prz/hdlDat/DriveCodeFile.dat'
                            elif self.G_ImageId==-1:
                                self.G_PhrozenFluiddRespondInfo("镜像Id==-1，默认：ARCO300-MKS-RK3328-STM32F407VET6-I16")
                                #lancaigang240530：版本写到dat文件；DriveCodeJson.dat
                                filename='/home/mks/hdlDat/DriveCodeFile.dat'
                            else:
                                self.G_PhrozenFluiddRespondInfo("镜像Id读不到，默认：ARCO300-MKS-RK3328-STM32F407VET6-I16")
                                #lancaigang240530：版本写到dat文件；DriveCodeJson.dat
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
                                    # 1 , 18 , 24053 , 18 , 0
                                    split[0]=split[0].strip()#驱动号
                                    split[1]=split[1].strip()#硬件id
                                    split[2]=split[2].strip()#固件版本
                                    split[3]=split[3].strip()#镜像id
                                    split[4]=split[4].strip()#是否在线
                                    #split[4]='0'#是否在线，默认给0
                                    #if "SN1" in self.G_SerialRxASCIIStr:
                                    if split[0] == "1":
                                        self.G_PhrozenFluiddRespondInfo("AMS段码屏烘干第1台固件版本")
                                        self.G_PhrozenFluiddRespondInfo(split[0])
                                        self.G_PhrozenFluiddRespondInfo(split[1])
                                        self.G_PhrozenFluiddRespondInfo(split[2])
                                        self.G_PhrozenFluiddRespondInfo(split[3])
                                        self.G_PhrozenFluiddRespondInfo(split[4])
                                        #line=("%d,%d,%d," % (HW_VERSION,,))
                                        line_modify=split[0]+','+'18'+','+self.G_SerialRxASCIIStr[11:16]+','+'18'+','+'1'
                                        self.G_PhrozenFluiddRespondInfo(line_modify)
                                        Lo_AllLine=Lo_AllLine+line_modify+"\r\n"#0x0D 0x0A
                                    else:
                                        Lo_AllLine=Lo_AllLine+line
                                    # if "SN2" in self.G_SerialRxASCIIStr:
                                    #     if split[0] == "2":
                                    #         self.G_PhrozenFluiddRespondInfo(split[0])
                                    #         self.G_PhrozenFluiddRespondInfo(split[1])
                                    #         self.G_PhrozenFluiddRespondInfo(split[2])
                                    #         self.G_PhrozenFluiddRespondInfo(split[3])
                                    #         self.G_PhrozenFluiddRespondInfo(split[4])
                                    #         #line=("%d,%d,%d," % (HW_VERSION,,))
                                    #         line_modify=split[0]+','+'1'+','+self.G_SerialRxASCIIStr[9:14]+','+'1'+','+'1'
                                    #         self.G_PhrozenFluiddRespondInfo(line_modify)
                                    #         Lo_AllLine=Lo_AllLine+line_modify+"\r\n"#0x0D 0x0A
                                    #     else:
                                    #         Lo_AllLine=Lo_AllLine+line
                                    # if "SN3" in self.G_SerialRxASCIIStr:
                                    #     if split[0] == "3":
                                    #         self.G_PhrozenFluiddRespondInfo(split[0])
                                    #         self.G_PhrozenFluiddRespondInfo(split[1])
                                    #         self.G_PhrozenFluiddRespondInfo(split[2])
                                    #         self.G_PhrozenFluiddRespondInfo(split[3])
                                    #         self.G_PhrozenFluiddRespondInfo(split[4])
                                    #         #line=("%d,%d,%d," % (HW_VERSION,,))
                                    #         line_modify=split[0]+','+'1'+','+self.G_SerialRxASCIIStr[9:14]+','+'1'+','+'1'
                                    #         self.G_PhrozenFluiddRespondInfo(line_modify)
                                    #         Lo_AllLine=Lo_AllLine+line_modify+"\r\n"#0x0D 0x0A
                                    #     else:
                                    #         Lo_AllLine=Lo_AllLine+line
                                    # if "SN4" in self.G_SerialRxASCIIStr:
                                    #     if split[0] == "4":
                                    #         self.G_PhrozenFluiddRespondInfo(split[0])
                                    #         self.G_PhrozenFluiddRespondInfo(split[1])
                                    #         self.G_PhrozenFluiddRespondInfo(split[2])
                                    #         self.G_PhrozenFluiddRespondInfo(split[3])
                                    #         self.G_PhrozenFluiddRespondInfo(split[4])
                                    #         #line=("%d,%d,%d," % (HW_VERSION,,))
                                    #         line_modify=split[0]+','+'1'+','+self.G_SerialRxASCIIStr[9:14]+','+'1'+','+'1'
                                    #         self.G_PhrozenFluiddRespondInfo(line_modify)
                                    #         Lo_AllLine=Lo_AllLine+line_modify+"\r\n"#0x0D 0x0A
                                    #     else:
                                    #         Lo_AllLine=Lo_AllLine+line
                            #self.G_PhrozenFluiddRespondInfo(Lo_AllLine)
                            with open(filename,"w+") as file_w:
                                file_w.write(Lo_AllLine)


                        self.Device_TimmerUartRecvHandler(1,Lo_SerialRxBytes,self.G_SerialRxASCIIStr)

                except:
                    self.G_PhrozenFluiddRespondInfo("串口数据异常，无法解析AMS状态")


            return eventtime + AMS_SERIALPORT_RECV_TIMER

        except Exception as e:
            self.G_PhrozenFluiddRespondInfo("串口1读取错误，AMS1异常或重启，请检查AMS1是否正常")
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
            #lancaigang0427：如果AMS异常重启，需要记录，并重启成功发送命令让stm32进入慢速补料阶段
            #lancaigang240427：AMS异常重启，需要记录
            self.G_AMS1ErrorRestartFlag = True
            self.G_AMS1ErrorRestartCount=self.G_AMS1ErrorRestartCount+1

            #lancaigang241011：串口异常，不允许发送数据
            self.G_SerialPort1OpenFlag=False
            
            #lancaigang240521：恢复的时候，如果发现AMS异常重启，可以认为是热插拔AMS，执行完整的退料换料过程
            self.G_ResumeCheckAMS1ErrorRestartFlag = True

            
            return eventtime + AMS_SERIALPORT_RECV_TIMER


    ####################################
    #函数名称：
    #输入参数：
    #返 回 值:
    #功能描述：蓝才刚-20230830
    ####################################
    #100ms
    def Device_TimmerUart2Recv(self, eventtime):
        try:
            #tty2连接失败
            if self.G_SerialPort2OpenFlag==False:
                self.G_ASM1DisconnectErrorCount=0
                #self.G_PhrozenFluiddRespondInfo("[(dev.python)Device_TimmerUart2Recv]串口2连接异常，永远退出回调函数")
                #self.G_PhrozenFluiddRespondInfo("self.G_AMS2ErrorRestartCount=%d" % self.G_AMS2ErrorRestartCount)

                self.G_AMS2ErrorRestartCount=self.G_AMS2ErrorRestartCount+1

                try:
                    if self.G_SerialPort2Obj is not None:
                        if self.G_SerialPort2Obj.is_open:
                            #tty2关闭
                            self.G_SerialPort2Obj.close()
                            self.G_PhrozenFluiddRespondInfo("关闭串口2成功")
                            self.G_PhrozenFluiddRespondInfo("AMS2连接失败")
                            self.G_PhrozenFluiddRespondInfo("缓存暂停命令+PAUSE:g")
                except:
                    self.G_PhrozenFluiddRespondInfo("关闭串口2异常")

                #lancaigang241108:延时几秒再暂停，防止AMS重启需要一些时间
                if self.G_AMS2ErrorRestartCount>=5:
                    #self.G_PhrozenFluiddRespondInfo("if self.G_AMS2ErrorRestartCount>=5:")

                    self.G_AMS2ErrorRestartCount=0
                    #lancaigang250619:如果USB异常，待换色异常时才报错
                    self.G_PauseToLCDString="+PAUSE:g,%d,%d" % (self.G_ChangeChannelTimeoutOldChan,self.G_ChangeChannelTimeoutNewChan)
                    

                    # if self.G_KlipperIfPaused==False:
                    #     self.G_KlipperIfPaused = True
                    #     #self.Cmds_PhrozenKlipperPauseNoneCmdToSTM32(None)
                    #     if self.G_CancelFlag==False:
                    #         # self.G_PhrozenFluiddRespondInfo("+PAUSE:g,%d,%d" % (self.G_ChangeChannelTimeoutOldChan,self.G_ChangeChannelTimeoutNewChan))
                    #         # self.G_PauseToLCDString="+PAUSE:g,%d,%d" % (self.G_ChangeChannelTimeoutOldChan,self.G_ChangeChannelTimeoutNewChan)
                    #         self.G_PhrozenFluiddRespondInfo("AMS2连接异常暂停")

                    #         #lancaigang250604:
                    #         if self.G_AMSDeviceWorkMode == AMS_WORK_MODE_UNKNOW:#M0
                    #             self.G_PhrozenFluiddRespondInfo("未知模式，不用暂停")
                    #         else:
                    #             if self.STM32ReprotPauseFlag==0:
                    #                 self.G_PauseTriggerWhileChangeChannelFlag=True
                    #                 if self.PG102Flag==True:
                    #                     self.G_PhrozenFluiddRespondInfo("正在吐料中，暂缓暂停，待吐料完成再暂停")
                    #                     self.PG102DelayPauseFlag=True
                    #                     #self.G_PhrozenFluiddRespondInfo("+PAUSE:g,%d,%d" % (self.G_ChangeChannelTimeoutOldChan,self.G_ChangeChannelTimeoutNewChan))
                    #                     self.G_PauseToLCDString="+PAUSE:g,%d,%d" % (self.G_ChangeChannelTimeoutOldChan,self.G_ChangeChannelTimeoutNewChan)
                    #                 else:
                    #                     self.G_PhrozenFluiddRespondInfo("未吐料，可以直接暂停")
                    #                     self.Cmds_PhrozenKlipperPauseNoneCmdToSTM32(None)
                    #                     self.G_KlipperIfPaused = True
                    #                     #self.Cmds_PhrozenKlipperPauseNoneCmdToSTM32(None)
                    #                     self.STM32ReprotPauseFlag=1
                    #                     #lancaigang231202：P1 C?自动换料时，如果第1次通道就进料异常暂停，如果要恢复，也继续从第1次通道开始
                    #                     self.G_ChangeChannelFirstFilaFlag=True
                    #                     self.G_PhrozenFluiddRespondInfo("+PAUSE:g,%d,%d" % (self.G_ChangeChannelTimeoutOldChan,self.G_ChangeChannelTimeoutNewChan))
                    #                     self.G_PauseToLCDString="+PAUSE:g,%d,%d" % (self.G_ChangeChannelTimeoutOldChan,self.G_ChangeChannelTimeoutNewChan)
                    #             else:
                    #                 self.G_PauseTriggerWhileChangeChannelFlag=True
                    #                 self.G_PauseToLCDString="+PAUSE:g,%d,%d" % (self.G_ChangeChannelTimeoutOldChan,self.G_ChangeChannelTimeoutNewChan)

                    #         #     self.G_PhrozenFluiddRespondInfo("+PAUSE:g,%d,%d" % (self.G_ChangeChannelTimeoutOldChan,self.G_ChangeChannelTimeoutNewChan))
                    #         #lancaigang20231013：断开连接
                    #         self.Device_DisconnectAMSDevice()

                    # #if self.G_KlipperIfPaused==True:
                    # else:
                    #     self.G_PhrozenFluiddRespondInfo("USB异常，当前已经是暂停状态")
                    #     self.G_PauseToLCDString="+PAUSE:g,%d,%d" % (self.G_ChangeChannelTimeoutOldChan,self.G_ChangeChannelTimeoutNewChan)


                    #lancaigang240524：永远退出回调函数
                    return self.G_PhrozenReactor.NEVER

                return eventtime + AMS_SERIALPORT_RECV_TIMER

            #lancaigang250619:USB连接正常，则清空
            #self.G_PauseToLCDString=""
            self.G_AMS2ErrorRestartCount=0


            #lancaigang241128：
            if self.G_CancelFlag==True:
                #self.G_PhrozenFluiddRespondInfo("[(dev.python)Device_TimmerRunoutCheck]已取消打印")
                return eventtime + AMS_SERIALPORT_RECV_TIMER
        


            # #lancaigang240427：AMS异常重启，需要记录
            # if self.G_AMS1ErrorRestartFlag == True:
            #     self.G_PhrozenFluiddRespondInfo("AMS1异常或重启;self.G_AMSErrorRestartCount=%d" % self.G_AMSErrorRestartCount)
            #     self.G_PhrozenFluiddRespondInfo("+AMSReboot:%d" % self.G_AMSErrorRestartCount)
            #     self.G_AMS1ErrorRestartFlag = False
                
            #     try:
            #         self.G_PhrozenFluiddRespondInfo("重新初始化串口1")
            #         self.G_SerialPort1Obj = serial.Serial(self.G_Serialport1Define, SERIAL_PORT_BAUD, timeout=3)
            #         #串口1打开成功
            #         if self.G_SerialPort1Obj.is_open:
            #             self.G_SerialPort1OpenFlag = True
            #             self.G_PhrozenFluiddRespondInfo("重新初始化串口1成功")
            #             #lancaigang231213：打开串口1
            #             self.G_SerialPort1Obj.flushInput()  # clean serial write cache
            #             self.G_SerialPort1Obj.flush()
            #             self.G_PhrozenFluiddRespondInfo("串口1清空")
            #             self.G_PhrozenFluiddRespondInfo("重新注册串口1回调函数")
            #             self.G_SerialPort1RecvTimmer = self.G_PhrozenReactor.register_timer(self.Device_TimmerUart1Recv, self.G_PhrozenReactor.NOW)
            #     except:
            #         self.G_PhrozenFluiddRespondInfo("未能打开tty1口，请检查USB口或重启尝试")

            #     return eventtime + AMS_SERIALPORT_RECV_TIMER



            # #lancaigang240410：
            # if self.G_CancelFlag==True:
            #     #self.G_PhrozenFluiddRespondInfo("已取消打印")
            #     return eventtime + AMS_SERIALPORT_RECV_TIMER



            #lancaigang231103:tty2串口有数据
            if self.G_SerialPort2Obj.inWaiting() > 0:
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

                self.G_PhrozenFluiddRespondInfo("[(dev.python)Device_TimmerUart2Recv]串口2读取数据")
                Lo_SerialRxLen=self.G_SerialPort2Obj.inWaiting()
                self.G_PhrozenFluiddRespondInfo("字节个数Lo_SerialRxLen=%d" % Lo_SerialRxLen)
                #self.G_PhrozenFluiddRespondInfo("串口定时器接收")
                Lo_SerialRxBytes=self.G_SerialPort2Obj.read(Lo_SerialRxLen)
                self.G_PhrozenFluiddRespondInfo("字节流Lo_SerialRxBytes=%s" % Lo_SerialRxBytes)
                self.G_PhrozenFluiddRespondInfo("字节流binascii.hexlify(Lo_SerialRxBytes)=%s" % binascii.hexlify(Lo_SerialRxBytes))
                #self.G_PhrozenFluiddRespondInfo("%x" % binascii.hexlify(Lo_SerialRxBytes))
                self.G_PhrozenFluiddRespondInfo("字节个数len(Lo_SerialRxBytes)=%d" % len(Lo_SerialRxBytes))
                #self.G_PhrozenFluiddRespondInfo("Lo_SerialRxBytes.count=%d" % Lo_SerialRxBytes.count)
                #for i in Lo_SerialRxBytes:
                    #self.G_PhrozenFluiddRespondInfo("%x" % i)

                self.G_PhrozenFluiddRespondInfo("Lo_SerialRxBytes[0]-16进制字节0x%2x" % Lo_SerialRxBytes[0])
                self.G_PhrozenFluiddRespondInfo("Lo_SerialRxBytes[0]-ASCII码字符%c" % Lo_SerialRxBytes[0])
                #self.G_PhrozenFluiddRespondInfo("Lo_SerialRxBytes[1]-16进制字节0x%2x" % Lo_SerialRxBytes[1])
                #self.G_PhrozenFluiddRespondInfo("Lo_SerialRxBytes[1]-ASCII码字符%c" % Lo_SerialRxBytes[1])


                #lancaigang20231013：读取ttyUSB0串口字节流转换为ASCII码
                #lancaigang240530：16进制字节转换为ASCII码字符
                self.G_SerialRxASCIIStr = Lo_SerialRxBytes.decode("ascii")
                #self.G_PhrozenFluiddRespondInfo("ASCII码字符串self.G_SerialRxASCIIStr=%s" % self.G_SerialRxASCIIStr)



                #lancaigang240705：存在AMS多色
                self.G_AMSDevice2IfNormal=True


                try:
                    # #if "R" in self.G_SerialRxASCIIStr:
                    # if Lo_SerialRxBytes[0]==0x52:
                    #     self.G_PhrozenFluiddRespondInfo("AMS第2台异步返回")

                    #     #self.G_PhrozenFluiddRespondInfo("%s" % SerialRxASCIIStr)
                    #     Lo_AMSDeviceStateInfo = AMSDetailInfoBytes()
                    #     Lo_AMSDeviceStateInfo.whole[:] = Lo_SerialRxBytes
                    #     #python空字典
                    #     Lo_AMSDetailState = {}
                    #     self.G_AMS2DeviceState["dev_id"] = Lo_AMSDetailState["dev_id"] = Lo_AMSDeviceStateInfo.field.dev_id
                    #     self.G_AMS2DeviceState["active_dev_id"] = Lo_AMSDetailState["active_dev_id"] = Lo_AMSDeviceStateInfo.field.active_dev_id
                    #     self.G_AMS2DeviceState["dev_mode"] = Lo_AMSDetailState["dev_mode"] = Lo_AMSDeviceStateInfo.field.dev_mode
                    #     self.G_AMS2DeviceState["cache_empty"] = Lo_AMSDetailState["cache_empty"] = Lo_AMSDeviceStateInfo.field.cache_empty
                    #     #self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_CmdP114]缓冲器传感器空状态(bool)==%d" % Lo_AMSDeviceStateInfo.field.cache_empty)
                    #     self.G_AMS2DeviceState["cache_full"] = Lo_AMSDetailState["cache_full"] = Lo_AMSDeviceStateInfo.field.cache_full
                    #     #self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_CmdP114]缓冲器传感器满状态(bool)==%d" % Lo_AMSDeviceStateInfo.field.cache_full)
                    #     self.G_AMS2DeviceState["cache_exist"] = Lo_AMSDetailState["cache_exist"] = Lo_AMSDeviceStateInfo.field.cache_exist
                    #     #self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_CmdP114]缓冲器传感器线材状态(bool)==%d" % Lo_AMSDeviceStateInfo.field.cache_exist)
                    #     self.G_AMS2DeviceState["mc_state"] = Lo_AMSDetailState["mc_state"] = Lo_AMSDeviceStateInfo.field.mc_state
                    #     self.G_AMS2DeviceState["ma_state"] = Lo_AMSDetailState["ma_state"] = Lo_AMSDeviceStateInfo.field.ma_state
                    #     self.G_AMS2DeviceState["entry_state"] = Lo_AMSDetailState["entry_state"] = Lo_AMSDeviceStateInfo.field.entry_state
                    #     #self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_CmdP114]入口位传感器状态(bit位)==%d" % Lo_AMSDeviceStateInfo.field.entry_state)
                    #     self.G_AMS2DeviceState["park_state"] = Lo_AMSDetailState["park_state"] = Lo_AMSDeviceStateInfo.field.park_state
                    #     #self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_CmdP114]停靠位传感器状态(bit位)==%d" % Lo_AMSDeviceStateInfo.field.park_state)
                        
                    #     # 响应数据json转换
                    #     self.G_PhrozenFluiddRespondInfo(json.dumps(Lo_AMSDetailState))


                    #if "R" in self.G_SerialRxASCIIStr:
                    if Lo_SerialRxBytes[0]==0x52 and Lo_SerialRxLen==16:
                        self.G_PhrozenFluiddRespondInfo("AMS第2台异步返回")

                        #self.G_PhrozenFluiddRespondInfo("%s" % SerialRxASCIIStr)
                        Lo_AMSDeviceStateInfo = AMSDetailInfoBytes()
                        Lo_AMSDeviceStateInfo.whole[:] = Lo_SerialRxBytes
                        #python空字典
                        Lo_AMSDetailState = {}
                        self.G_AMS1DeviceState["dev_id"] = Lo_AMSDetailState["dev_id"] = Lo_AMSDeviceStateInfo.field.dev_id
                        self.G_AMS1DeviceState["active_dev_id"] = Lo_AMSDetailState["active_dev_id"] = Lo_AMSDeviceStateInfo.field.active_dev_id
                        self.G_AMS1DeviceState["dev_mode"] = Lo_AMSDetailState["dev_mode"] = Lo_AMSDeviceStateInfo.field.dev_mode
                        self.G_AMS1DeviceState["cache_empty"] = Lo_AMSDetailState["cache_empty"] = Lo_AMSDeviceStateInfo.field.cache_empty
                        #self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_CmdP114]缓冲器传感器空状态(bool)==%d" % Lo_AMSDeviceStateInfo.field.cache_empty)
                        self.G_AMS1DeviceState["cache_full"] = Lo_AMSDetailState["cache_full"] = Lo_AMSDeviceStateInfo.field.cache_full
                        #self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_CmdP114]缓冲器传感器满状态(bool)==%d" % Lo_AMSDeviceStateInfo.field.cache_full)
                        self.G_AMS1DeviceState["cache_exist"] = Lo_AMSDetailState["cache_exist"] = Lo_AMSDeviceStateInfo.field.cache_exist
                        #self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_CmdP114]缓冲器传感器线材状态(bool)==%d" % Lo_AMSDeviceStateInfo.field.cache_exist)
                        self.G_AMS1DeviceState["mc_state"] = Lo_AMSDetailState["mc_state"] = Lo_AMSDeviceStateInfo.field.mc_state
                        self.G_AMS1DeviceState["ma_state"] = Lo_AMSDetailState["ma_state"] = Lo_AMSDeviceStateInfo.field.ma_state
                        self.G_AMS1DeviceState["entry_state"] = Lo_AMSDetailState["entry_state"] = Lo_AMSDeviceStateInfo.field.entry_state
                        #self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_CmdP114]入口位传感器状态(bit位)==%d" % Lo_AMSDeviceStateInfo.field.entry_state)
                        self.G_AMS1DeviceState["park_state"] = Lo_AMSDetailState["park_state"] = Lo_AMSDeviceStateInfo.field.park_state
                        #self.G_PhrozenFluiddRespondInfo("[(cmds.python)Cmds_CmdP114]停靠位传感器状态(bit位)==%d" % Lo_AMSDeviceStateInfo.field.park_state)
                        
                        # 响应数据json转换
                        self.G_PhrozenFluiddRespondInfo(json.dumps(Lo_AMSDetailState))

                        #lancaigang250708：
                        self.G_PhrozenFluiddRespondInfo("P114成功")
                        self.G_PhrozenFluiddRespondInfo("+P114:1")
                        self.G_P114RunFlag=0

                    else:
                        self.G_PhrozenFluiddRespondInfo("AMS固件版本")
                        #lancaigang20231013：读取ttyUSB0串口字节流转换为ASCII码
                        #lancaigang240530：16进制字节转换为ASCII码字符
                        self.G_SerialRxASCIIStr = Lo_SerialRxBytes.decode("ascii")
                        self.G_PhrozenFluiddRespondInfo("ASCII码字符串self.G_SerialRxASCIIStr=%s" % self.G_SerialRxASCIIStr)


                        #lancaigang250411：AMS固件版本

                        # // AMS主板2固件-1 1
                        if "V-H18-I18-F" in self.G_SerialRxASCIIStr:
                            self.G_PhrozenFluiddRespondInfo("AMS段码屏烘干第2台固件版本")
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
                            # 主题:c0f535790a90/GetZbGwInfo_Respon
                            # {
                            #     "Data_ID": 95,
                            #     "Data": {
                            #         "GwId": "c0f535790a90",
                            #         "HomeId": "",
                            #         "GWSN": "0000000000000000000",
                            #         "AccountId": "",
                            #         "GwMac": "c0f535790a90",
                            #         "GwIP": "192.168.3.53",
                            #         "GwName": "Name-c0f535790a90",
                            #         "ProductId": "ARCO",
                            #         "MainImage": 15,
                            #         "MainHWVersion": 15,
                            #         "MainFWVersion": 24064,
                            #         "Gw_Ram": 248584,
                            #         "Gw_Rom": 826536,
                            #         "JoinMode": 1,
                            #         "ESSID": "",
                            #         "MqttClientEMQfd": 31,
                            #         "MqttClientId": "c0f535790a90",
                            #         "MqttBrokerUserName": "",
                            #         "MqttBrokerPwd": "",
                            #         "DriveCodeList": [
                            #             {
                            #                 "DriveCode": 1,
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
                            #                 "DriveCode": 3,
                            #                 "DriveImageType": 0,
                            #                 "DriveHwVersion": 0,
                            #                 "DriveFwVersion": 0,
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
                            #                 "DriveCode": 5,
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
                            #                 "DriveCode": 7,
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
                            #                 "DriveCode": 9,
                            #                 "DriveImageType": 0,
                            #                 "DriveHwVersion": 0,
                            #                 "DriveFwVersion": 0,
                            #                 "DriveId": 0
                            #             },
                            #             {
                            #                 "DriveCode": 10,
                            #                 "DriveImageType": 10,
                            #                 "DriveHwVersion": 10,
                            #                 "DriveFwVersion": 25033,
                            #                 "DriveId": 0
                            #             },
                            #             {
                            #                 "DriveCode": 11,
                            #                 "DriveImageType": 11,
                            #                 "DriveHwVersion": 11,
                            #                 "DriveFwVersion": 25022,
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
                            #                 "DriveCode": 13,
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
                            #                 "DriveCode": 15,
                            #                 "DriveImageType": 0,
                            #                 "DriveHwVersion": 0,
                            #                 "DriveFwVersion": 0,
                            #                 "DriveId": 0
                            #             },
                            #             {
                            #                 "DriveCode": 16,
                            #                 "DriveImageType": 0,
                            #                 "DriveHwVersion": 0,
                            #                 "DriveFwVersion": 0,
                            #                 "DriveId": 0
                            #             },
                            #             {
                            #                 "DriveCode": 17,
                            #                 "DriveImageType": 0,
                            #                 "DriveHwVersion": 0,
                            #                 "DriveFwVersion": 0,
                            #                 "DriveId": 0
                            #             },
                            #             {
                            #                 "DriveCode": 18,
                            #                 "DriveImageType": 0,
                            #                 "DriveHwVersion": 0,
                            #                 "DriveFwVersion": 0,
                            #                 "DriveId": 0
                            #             },
                            #             {
                            #                 "DriveCode": 19,
                            #                 "DriveImageType": 0,
                            #                 "DriveHwVersion": 0,
                            #                 "DriveFwVersion": 0,
                            #                 "DriveId": 0
                            #             },
                            #             {
                            #                 "DriveCode": 20,
                            #                 "DriveImageType": 0,
                            #                 "DriveHwVersion": 0,
                            #                 "DriveFwVersion": 0,
                            #                 "DriveId": 0
                            #             }
                            #         ]
                            #     }
                            # }
                            #lancaigang250724：读取系统镜像id，区分不同产品不同主板不同固件
                            #lancaigang250724:读取镜像id
                            self.Cmds_GetImageId()
                            if self.G_ImageId==16:
                                self.G_PhrozenFluiddRespondInfo("镜像Id==16：ARCO300-MKS-RK3328-STM32F407VET6-I16")
                                #lancaigang240530：版本写到dat文件；DriveCodeJson.dat
                                filename='/home/mks/hdlDat/DriveCodeFile.dat'
                            elif self.G_ImageId==31:
                                self.G_PhrozenFluiddRespondInfo("镜像Id==31：ARCO300-phrozen-RK3308-STM32F407VET6-I31")
                                #lancaigang240530：版本写到dat文件；DriveCodeJson.dat
                                filename='/home/prz/hdlDat/DriveCodeFile.dat'
                            elif self.G_ImageId==-1:
                                self.G_PhrozenFluiddRespondInfo("镜像Id==-1，默认：ARCO300-MKS-RK3328-STM32F407VET6-I16")
                                #lancaigang240530：版本写到dat文件；DriveCodeJson.dat
                                filename='/home/mks/hdlDat/DriveCodeFile.dat'
                            else:
                                self.G_PhrozenFluiddRespondInfo("镜像Id读不到，默认：ARCO300-MKS-RK3328-STM32F407VET6-I16")
                                #lancaigang240530：版本写到dat文件；DriveCodeJson.dat
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
                                    # 2 , 18 , 24053 , 18 , 0
                                    split[0]=split[0].strip()#驱动号
                                    split[1]=split[1].strip()#硬件id
                                    split[2]=split[2].strip()#固件版本
                                    split[3]=split[3].strip()#镜像id
                                    split[4]=split[4].strip()#是否在线
                                    #split[4]='0'#是否在线，默认给0
                                    # #if "SN1" in self.G_SerialRxASCIIStr:
                                    # if split[0] == "1":
                                    #     self.G_PhrozenFluiddRespondInfo(split[0])
                                    #     self.G_PhrozenFluiddRespondInfo(split[1])
                                    #     self.G_PhrozenFluiddRespondInfo(split[2])
                                    #     self.G_PhrozenFluiddRespondInfo(split[3])
                                    #     self.G_PhrozenFluiddRespondInfo(split[4])
                                    #     #line=("%d,%d,%d," % (HW_VERSION,,))
                                    #     line_modify=split[0]+','+'1'+','+self.G_SerialRxASCIIStr[9:14]+','+'1'+','+'1'
                                    #     self.G_PhrozenFluiddRespondInfo(line_modify)
                                    #     Lo_AllLine=Lo_AllLine+line_modify+"\r\n"#0x0D 0x0A
                                    # else:
                                    #     Lo_AllLine=Lo_AllLine+line

                                    #if "SN2" in self.G_SerialRxASCIIStr:
                                    if split[0] == "2":
                                        self.G_PhrozenFluiddRespondInfo("AMS第2台固件版本")
                                        self.G_PhrozenFluiddRespondInfo(split[0])
                                        self.G_PhrozenFluiddRespondInfo(split[1])
                                        self.G_PhrozenFluiddRespondInfo(split[2])
                                        self.G_PhrozenFluiddRespondInfo(split[3])
                                        self.G_PhrozenFluiddRespondInfo(split[4])
                                        #line=("%d,%d,%d," % (HW_VERSION,,))
                                        line_modify=split[0]+','+'18'+','+self.G_SerialRxASCIIStr[11:16]+','+'18'+','+'1'
                                        self.G_PhrozenFluiddRespondInfo(line_modify)
                                        Lo_AllLine=Lo_AllLine+line_modify+"\r\n"#0x0D 0x0A
                                    else:
                                        Lo_AllLine=Lo_AllLine+line

                                    # if "SN3" in self.G_SerialRxASCIIStr:
                                    #     if split[0] == "3":
                                    #         self.G_PhrozenFluiddRespondInfo(split[0])
                                    #         self.G_PhrozenFluiddRespondInfo(split[1])
                                    #         self.G_PhrozenFluiddRespondInfo(split[2])
                                    #         self.G_PhrozenFluiddRespondInfo(split[3])
                                    #         self.G_PhrozenFluiddRespondInfo(split[4])
                                    #         #line=("%d,%d,%d," % (HW_VERSION,,))
                                    #         line_modify=split[0]+','+'1'+','+self.G_SerialRxASCIIStr[9:14]+','+'1'+','+'1'
                                    #         self.G_PhrozenFluiddRespondInfo(line_modify)
                                    #         Lo_AllLine=Lo_AllLine+line_modify+"\r\n"#0x0D 0x0A
                                    #     else:
                                    #         Lo_AllLine=Lo_AllLine+line
                                    # if "SN4" in self.G_SerialRxASCIIStr:
                                    #     if split[0] == "4":
                                    #         self.G_PhrozenFluiddRespondInfo(split[0])
                                    #         self.G_PhrozenFluiddRespondInfo(split[1])
                                    #         self.G_PhrozenFluiddRespondInfo(split[2])
                                    #         self.G_PhrozenFluiddRespondInfo(split[3])
                                    #         self.G_PhrozenFluiddRespondInfo(split[4])
                                    #         #line=("%d,%d,%d," % (HW_VERSION,,))
                                    #         line_modify=split[0]+','+'1'+','+self.G_SerialRxASCIIStr[9:14]+','+'1'+','+'1'
                                    #         self.G_PhrozenFluiddRespondInfo(line_modify)
                                    #         Lo_AllLine=Lo_AllLine+line_modify+"\r\n"#0x0D 0x0A
                                    #     else:
                                    #         Lo_AllLine=Lo_AllLine+line
                            #self.G_PhrozenFluiddRespondInfo(Lo_AllLine)
                            with open(filename,"w+") as file_w:
                                file_w.write(Lo_AllLine)


                        self.Device_TimmerUartRecvHandler(2,Lo_SerialRxBytes,self.G_SerialRxASCIIStr)

                except:
                    self.G_PhrozenFluiddRespondInfo("串口数据异常，无法解析AMS状态")

            return eventtime + AMS_SERIALPORT_RECV_TIMER

        except Exception as e:
            self.G_PhrozenFluiddRespondInfo("串口2读取错误，AMS2异常或重启，请检查AMS2是否正常")
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
            #lancaigang0427：如果AMS异常重启，需要记录，并重启成功发送命令让stm32进入慢速补料阶段
            #lancaigang240427：AMS异常重启，需要记录
            self.G_AMS2ErrorRestartFlag = True
            self.G_AMS2ErrorRestartCount=self.G_AMS2ErrorRestartCount+1

            #lancaigang241011：串口2异常，不允许发送数据
            self.G_SerialPort2OpenFlag=False
            
            #lancaigang240521：恢复的时候，如果发现AMS异常重启，可以认为是热插拔AMS，执行完整的退料换料过程
            self.G_ResumeCheckAMS2ErrorRestartFlag = True

            
            return eventtime + AMS_SERIALPORT_RECV_TIMER


    
    
    ####################################
    #函数名称：
    #输入参数：
    #返 回 值:
    #功能描述：蓝才刚-20230830
    ####################################
#lancaigang0914：不能挪动位置；调用PhrozenDev类
def load_config(config):
    return PhrozenDev(config)
