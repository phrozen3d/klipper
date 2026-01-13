####################################
#项目名称：
#芯片类型: 
#功能: 
#研发人员：蓝才刚
#开发时间: 20230830
####################################


from .cmds import *

####################################
#类名：
#功能描述：蓝才刚-20230830
####################################
class Apis(Commands):
    ####################################
    #函数名称：
    #输入参数：
    #返 回 值:
    #功能描述：蓝才刚-20230830
    ####################################
    #构造函数初始化
    def __init__(self, config):
        super(Apis, self).__init__(config)
        self.G_WebsocketWebhooks = self.G_PhrozenPrinter.lookup_object("webhooks")
    ####################################
    #函数名称：
    #输入参数：
    #返 回 值:
    #功能描述：蓝才刚-20230830
    ####################################
    # 注册websocket api
    def WebsocketAPIs_RegisterAPIs(self):
        self.G_PhrozenFluiddRespondInfo("[(dev.python)WebsocketAPIs_RegisterAPIs]注册phrozen自定义websocket接口api")
        self.G_WebsocketWebhooks.register_endpoint("phrozen/soft_ver", self.WebsocketAPIs_SoftVersion)
    ####################################
    #函数名称：
    #输入参数：
    #返 回 值:
    #功能描述：蓝才刚-20230830
    ####################################
    def WebsocketAPIs_SoftVersion(self, web_request):
        self.G_PhrozenFluiddRespondInfo("[(dev.python)WebsocketAPIs_SoftVersion]")
        #websocket发送
        web_request.send({"soft_version": FW_VERSION})
