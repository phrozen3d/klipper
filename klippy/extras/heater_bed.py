####################################
#项目名称：
#芯片类型: 
#功能: 
#研发人员：蓝才刚
#开发时间: 20230830
####################################
####################################
#类名：
#功能描述：蓝才刚-20230830
####################################
class PrinterHeaterBed:
    ####################################
    #函数名称：
    #输入参数：
    #返 回 值:
    #功能描述：蓝才刚-20230830
    ####################################
    def __init__(self, config):
        self.printer = config.get_printer()
        pheaters = self.printer.load_object(config, 'heaters')
        self.heater = pheaters.setup_heater(config, 'B')
        self.get_status = self.heater.get_status
        self.stats = self.heater.stats
        # Register commands
        gcode = self.printer.lookup_object('gcode')
        gcode.register_command("M140", self.cmd_M140)
        gcode.register_command("M190", self.cmd_M190)
    ####################################
    #函数名称：
    #输入参数：
    #返 回 值:
    #功能描述：蓝才刚-20230830
    ####################################
    def cmd_M140(self, gcmd, wait=False):
        # Set Bed Temperature
        temp = gcmd.get_float('S', 0.)
        pheaters = self.printer.lookup_object('heaters')
        pheaters.set_temperature(self.heater, temp, wait)
    ####################################
    #函数名称：
    #输入参数：
    #返 回 值:
    #功能描述：蓝才刚-20230830
    ####################################
    def cmd_M190(self, gcmd):
        # Set Bed Temperature and Wait
        self.printer.lookup_object('gcode').respond_info("[(Phrozen)Klipper] run M190")
        self.cmd_M140(gcmd, wait=True)
        self.printer.lookup_object('gcode').respond_info("[(Phrozen)Klipper] M190 complete")
####################################
#函数名称：
#输入参数：
#返 回 值:
#功能描述：蓝才刚-20230830
####################################
def load_config(config):
    return PrinterHeaterBed(config)
